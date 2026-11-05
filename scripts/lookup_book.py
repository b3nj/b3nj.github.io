#!/usr/bin/env python3
"""Look up a book and append it to the books JSON file.

Sources, in order: BnF (SRU, Dublin Core) -> Google Books -> Open Library.
BnF has no covers/descriptions, so a BnF hit is enriched from Google Books by ISBN.

Input (env):  INPUT_ISBN, INPUT_TITLE, INPUT_AUTHOR, TARGET_FILE
Optional env: GOOGLE_BOOKS_API_KEY, TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, SITE_URL
Output:       appends a Google-Books-style volumeInfo object to TARGET_FILE and
              sets GITHUB_OUTPUT: result=added|duplicate|notfound, title, author, isbn
"""
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "bkraft-book-lookup/1.0 (+https://bkraft.fr)"
TIMEOUT = 15

LANG_MAP = {
    "fre": "fr", "fra": "fr", "eng": "en", "ger": "de", "deu": "de", "spa": "es",
    "ita": "it", "por": "pt", "dut": "nl", "nld": "nl", "lat": "la", "rus": "ru",
    "jpn": "ja", "chi": "zh", "zho": "zh", "ara": "ar",
}
ROLES = (
    r"(Auteur du texte|Traducteur|Illustrateur|Pr[ée]facier|Postfacier|"
    r"Directeur de publication|[ÉE]diteur scientifique|Adaptateur|Photographe)"
)
FILL_KEYS = (
    "subtitle", "authors", "publisher", "publishedDate", "pageCount",
    "description", "categories", "language", "imageLinks", "canonicalVolumeLink",
)


# ---------------------------------------------------------------- helpers
def slugify(text):
    text = re.sub(r"[^\w\s-]", "", (text or "").lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def clean_isbn(s):
    return re.sub(r"[^0-9Xx]", "", s or "").upper()


def isbn10_to_13(i10):
    core = "978" + i10[:9]
    total = sum(int(d) * (1 if k % 2 == 0 else 3) for k, d in enumerate(core))
    return core + str((10 - total % 10) % 10)


def norm13(i):
    i = clean_isbn(i)
    if len(i) == 13:
        return i
    if len(i) == 10:
        return isbn10_to_13(i)
    return None


def keys(vol):
    """Identity keys of a book: normalised ISBN-13s plus any other identifier."""
    out = set()
    for e in vol.get("industryIdentifiers", []):
        ident = e.get("identifier", "")
        if e.get("type") in ("ISBN_10", "ISBN_13"):
            n = norm13(ident)
            if n:
                out.add("isbn:" + n)
        elif ident:
            out.add("id:" + ident)
    return out


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def local(tag):
    return tag.rsplit("}", 1)[-1]


def attempt(name, fn):
    try:
        res = fn()
        print(f"[{name}] {'hit' if res else 'no result'}")
        return res
    except Exception as e:  # network error, bad XML/JSON... fall through to next source
        print(f"[{name}] error: {e}")
        return None


def set_output(**kv):
    lines = "".join(f"{k}={str(v).replace(chr(10), ' ')}\n" for k, v in kv.items())
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(lines)
    else:
        print(lines)


def telegram(text, buttons=None):
    token = os.environ.get("TELEGRAM_API_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("Telegram not configured, skipping notification")
        return
    payload = {"chat_id": chat, "parse_mode": "HTML", "text": text,
               "disable_web_page_preview": True}
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": [buttons]}
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            print("Telegram:", json.loads(r.read()).get("ok"))
    except Exception as e:
        print(f"Telegram failed: {e}")


# ---------------------------------------------------------------- BnF
def clean_person(s):
    s = re.sub(r"\s*\(.*$", "", s)                       # drop dates + role after "("
    s = re.sub(r"[.,]?\s*" + ROLES + r"\s*$", "", s)     # role without dates
    s = s.strip(" ,;")
    if s.endswith(".") and not re.search(r"(^|[\s.])[A-ZÀ-Ý]\.$", s):
        s = s[:-1]
    if "," in s:
        last, first = [p.strip() for p in s.split(",", 1)]
        s = f"{first} {last}".strip()
    return s


def clean_title(raw):
    t = re.sub(r"\s*\[[^\]]*\]", "", raw)                # [Texte imprimé]
    t = t.split(" / ")[0].strip(" .;")
    title, _, sub = t.partition(" : ")
    return title.strip(), sub.strip()


def bnf_records(query, max_records=1):
    params = urllib.parse.urlencode(
        {"version": "1.2", "operation": "searchRetrieve", "recordSchema": "dublincore",
         "maximumRecords": str(max_records), "query": query},
        quote_via=urllib.parse.quote,
    )
    raw, err = None, None
    for scheme in ("https", "http"):
        try:
            raw = http_get(f"{scheme}://catalogue.bnf.fr/api/SRU?{params}")
            break
        except Exception as e:
            err = e
    if raw is None:
        raise err
    root = ET.fromstring(raw)
    records = []
    for rd in root.iter():
        if local(rd.tag) != "recordData":
            continue
        fields = {}
        for e in rd.iter():
            name = local(e.tag)
            if name in ("recordData", "dc") or not (e.text and e.text.strip()):
                continue
            fields.setdefault(name, []).append(e.text.strip())
        if fields:
            records.append(fields)
    return records


def bnf_to_volume(f):
    title, sub = clean_title(f["title"][0]) if f.get("title") else ("", "")
    people = f.get("creator") or f.get("contributor") or []
    authors = [p for p in (clean_person(x) for x in people) if p]

    publisher = (f.get("publisher") or [""])[0]
    publisher = re.sub(r"\s*\(.*?\)", "", publisher.split(" : ")[-1]).strip(" ,;")

    m = re.search(r"\b(1[4-9]\d{2}|20\d{2})\b", " ".join(f.get("date", [])))
    pages = re.search(r"(\d{1,5})\s*p\b", " ".join(f.get("format", [])))
    lang = (f.get("language") or [""])[0].lower()

    idents, canonical = [], ""
    for ident in f.get("identifier", []):
        if ident.startswith("http") and "ark:" in ident and not canonical:
            canonical = ident
        im = re.search(r"ISBN\s*:?\s*([0-9][0-9Xx\- ]{8,})", ident)
        if im:
            n = clean_isbn(im.group(1))
            kind = {13: "ISBN_13", 10: "ISBN_10"}.get(len(n))
            entry = {"type": kind, "identifier": n}
            if kind and entry not in idents:
                idents.append(entry)

    vol = {
        "title": title, "subtitle": sub, "authors": authors, "publisher": publisher,
        "publishedDate": m.group(1) if m else "",
        "pageCount": int(pages.group(1)) if pages else None,
        "language": LANG_MAP.get(lang, lang),
        "industryIdentifiers": idents, "canonicalVolumeLink": canonical,
        "lookupSource": "bnf",
    }
    return {k: v for k, v in vol.items() if v not in (None, "", [])}


def from_bnf(query, max_records=1):
    records = bnf_records(query, max_records)
    if not records:
        return None
    rec = next((r for r in records
                if any("ISBN" in i for i in r.get("identifier", []))), records[0])
    vol = bnf_to_volume(rec)
    if not vol.get("title"):
        return None
    # BnF has no cover / description: enrich from Google Books by ISBN
    isbn = next((e["identifier"] for e in vol.get("industryIdentifiers", [])), None)
    if isbn:
        extra = attempt("Google enrich", lambda: google_search(f"isbn:{isbn}"))
        vol = merge(vol, extra)
    return vol


# ---------------------------------------------------------------- Google Books
def google_search(query):
    params = {"q": query, "maxResults": "1"}
    if os.environ.get("GOOGLE_BOOKS_API_KEY"):
        params["key"] = os.environ["GOOGLE_BOOKS_API_KEY"]
    url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote)
    items = json.loads(http_get(url)).get("items") or []
    if not items:
        return None
    vi = items[0].get("volumeInfo", {})
    if not vi.get("title"):
        return None
    links = vi.get("imageLinks")
    if links:
        vi["imageLinks"] = {k: v.replace("http://", "https://") for k, v in links.items()}
    vi["lookupSource"] = "google"
    return vi


# ---------------------------------------------------------------- Open Library
def openlibrary_by_isbn(isbn):
    url = (f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}"
           "&format=json&jscmd=data")
    d = json.loads(http_get(url)).get(f"ISBN:{isbn}")
    if not d or not d.get("title"):
        return None
    ids = d.get("identifiers", {})
    idents = [{"type": "ISBN_13", "identifier": i} for i in ids.get("isbn_13", [])[:1]]
    idents += [{"type": "ISBN_10", "identifier": i} for i in ids.get("isbn_10", [])[:1]]
    year = re.search(r"\b(1[4-9]\d{2}|20\d{2})\b", d.get("publish_date", ""))
    lang = ((d.get("languages") or [{}])[0].get("key", "")).rsplit("/", 1)[-1]
    vol = {
        "title": d["title"], "subtitle": d.get("subtitle", ""),
        "authors": [a["name"] for a in d.get("authors", [])],
        "publisher": (d.get("publishers") or [{}])[0].get("name", ""),
        "publishedDate": year.group(1) if year else "",
        "pageCount": d.get("number_of_pages"),
        "language": LANG_MAP.get(lang, lang),
        "industryIdentifiers": idents, "canonicalVolumeLink": d.get("url", ""),
        "lookupSource": "openlibrary",
    }
    cover = (d.get("cover") or {}).get("medium")
    if cover:
        vol["imageLinks"] = {"thumbnail": cover}
    return {k: v for k, v in vol.items() if v not in (None, "", [])}


def openlibrary_by_title(title, author):
    params = {"title": title, "limit": "1", "fields": "isbn"}
    if author:
        params["author"] = author
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote)
    docs = json.loads(http_get(url)).get("docs") or []
    isbns = docs[0].get("isbn", []) if docs else []
    isbn = next((i for i in isbns if len(i) == 13), None) or (isbns[0] if isbns else None)
    return openlibrary_by_isbn(isbn) if isbn else None


# ---------------------------------------------------------------- merge / lookup
def merge(primary, extra):
    if not extra:
        return primary
    for k in FILL_KEYS:
        if not primary.get(k) and extra.get(k):
            primary[k] = extra[k]
    have = {(e.get("type"), e.get("identifier")) for e in primary.get("industryIdentifiers", [])}
    for e in extra.get("industryIdentifiers", []):
        if e.get("type") in ("ISBN_10", "ISBN_13") and (e["type"], e["identifier"]) not in have:
            primary.setdefault("industryIdentifiers", []).append(e)
    return primary


def find_book(isbn, title, author):
    vol = None
    if isbn:
        vol = attempt("BnF/ISBN", lambda: from_bnf(f'bib.fuzzyISBN all "{isbn}"'))
        vol = vol or attempt("Google/ISBN", lambda: google_search(f"isbn:{isbn}"))
        vol = vol or attempt("OpenLibrary/ISBN", lambda: openlibrary_by_isbn(isbn))
    if not vol and title:
        t, a = title.replace('"', " "), author.replace('"', " ")
        bq = f'(bib.title all "{t}")' + (f' and (bib.author all "{a}")' if a else "")
        gq = f"intitle:{title}" + (f" inauthor:{author}" if author else "")
        vol = attempt("BnF/title", lambda: from_bnf(bq, 5))
        vol = vol or attempt("Google/title", lambda: google_search(gq))
        vol = vol or attempt("OpenLibrary/title", lambda: openlibrary_by_title(title, author))
    return vol


def finalize(vol, isbn_in):
    ids = vol.setdefault("industryIdentifiers", [])
    if isbn_in and ("isbn:" + (norm13(isbn_in) or "")) not in keys(vol):
        ids.append({"type": "ISBN_13" if len(isbn_in) == 13 else "ISBN_10",
                    "identifier": isbn_in})
    if not keys(vol):  # no ISBN anywhere: stable synthetic id so dedup still works
        ids.append({"type": "OTHER", "identifier": "noisbn-" + slugify(vol.get("title", ""))})
    return vol


def find_existing(books, vol):
    k = keys(vol)
    slug = slugify(vol.get("title", ""))
    author = (vol.get("authors") or [""])[0].lower()
    for b in books:
        if k & keys(b):
            return b
        b_author = (b.get("authors") or [""])[0].lower()
        if slug and slugify(b.get("title", "")) == slug and (not author or not b_author or author == b_author):
            return b
    return None


# ---------------------------------------------------------------- main
def main():
    import html
    isbn_in = clean_isbn(os.environ.get("INPUT_ISBN", ""))
    if len(isbn_in) not in (10, 13):
        isbn_in = ""
    title_in = os.environ.get("INPUT_TITLE", "").strip()
    author_in = os.environ.get("INPUT_AUTHOR", "").strip()
    target = os.environ.get("TARGET_FILE") or "_data/books.json"
    site = os.environ.get("SITE_URL", "")

    if not isbn_in and not title_in:
        raise SystemExit("Need a valid ISBN or a title")
    query_label = isbn_in or f"{title_in} {author_in}".strip()

    vol = find_book(isbn_in, title_in, author_in)
    if not vol:
        telegram(f"❌ No match in BnF, Google Books or Open Library for: "
                 f"<b>{html.escape(query_label)}</b>")
        set_output(result="notfound")
        return

    vol = finalize(vol, isbn_in)
    print("Resolved book:\n" + json.dumps(vol, ensure_ascii=False, indent=2))

    books = []
    if os.path.exists(target):
        with open(target, encoding="utf-8") as f:
            books = json.load(f)

    existing = find_existing(books, vol)
    title = vol.get("title", "Unknown title")
    author = (vol.get("authors") or ["Unknown author"])[0]
    isbn_show = next((e["identifier"] for e in vol["industryIdentifiers"]), "")

    if existing:
        print(f"Duplicate of: {existing.get('title')}")
        slug = existing.get("slug") or slugify(existing.get("title", ""))
        buttons = [{"text": "📖 View in library", "url": f"{site}/books/{slug}/"}] if site and slug else None
        telegram(f"📚 <b>{html.escape(existing.get('title', title))}</b> is already in your "
                 f"library.\n🔖 <code>{html.escape(isbn_show)}</code>", buttons)
        set_output(result="duplicate", title=title, isbn=isbn_show)
        return

    books.append(vol)
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    set_output(result="added", title=title, author=author, isbn=isbn_show)


if __name__ == "__main__":
    main()