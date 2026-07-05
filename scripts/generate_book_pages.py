#!/usr/bin/env python3
import json
import os
import re
import traceback
import urllib.request
import yaml

DATA_FILE = "_data/books.json"
OUTPUT_DIR = "books"


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def get_isbn(book):
    """Extract ISBN-13 preferentially, fall back to ISBN-10, from Google Books industryIdentifiers."""
    identifiers = book.get("industryIdentifiers", [])
    isbn13 = next((e["identifier"] for e in identifiers if e.get("type") == "ISBN_13"), None)
    isbn10 = next((e["identifier"] for e in identifiers if e.get("type") == "ISBN_10"), None)
    return isbn13 or isbn10, [e["identifier"] for e in identifiers]


def get_cover_url(book):
    """Extract cover thumbnail URL from Google Books imageLinks."""
    image_links = book.get("imageLinks", {})
    url = image_links.get("thumbnail") or image_links.get("smallThumbnail")
    if url:
        # Google Books returns http:// — upgrade to https
        return url.replace("http://", "https://")
    return None


def download_cover(url, dest_path):
    print(f"    → Downloading cover from {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"    ✓ Cover saved to {dest_path}")
        return True
    except Exception as e:
        print(f"    ✗ Cover download failed: {e}")
        return False


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        books = json.load(f)

    print(f"📚 Found {len(books)} books to process\n")

    for i, book in enumerate(books):
        try:
            title = book.get("title", "Untitled")
            slug = slugify(title) or "unknown"

            isbn, isbn_list = get_isbn(book)
            page_dir = os.path.join(OUTPUT_DIR, slug if slug else isbn)

            # Rename any existing folder that used an ISBN-based name
            for old_id in isbn_list:
                old_dir = os.path.join(OUTPUT_DIR, old_id)
                if old_dir != page_dir and os.path.exists(old_dir):
                    print(f"    ↩ Renaming {old_dir} → {page_dir}")
                    os.rename(old_dir, page_dir)
                    break

            print(f"[{i+1}/{len(books)}] {title}")
            print(f"    ISBN: {isbn or 'none'} | folder: {page_dir}")

            front_matter = {"layout": "book"}
            front_matter.update(book)

            os.makedirs(page_dir, exist_ok=True)
            print(f"    ✓ Folder ready")

            cover_url = get_cover_url(book)
            if cover_url:
                cover_path = os.path.join(page_dir, "cover.jpg")
                if not os.path.exists(cover_path):
                    if download_cover(cover_url, cover_path):
                        front_matter["cover_local"] = f"/books/{slug if slug else isbn}/cover.jpg"
                else:
                    print(f"    ↩ Cover already exists, skipping download")
                    front_matter["cover_local"] = f"/books/{slug if slug else isbn}/cover.jpg"
            else:
                print(f"    ⚠ No cover URL, skipping cover")

            with open(os.path.join(page_dir, "index.md"), "w", encoding="utf-8") as f:
                f.write("---\n")
                yaml.dump(front_matter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
                f.write("---\n")

            print(f"    ✓ index.md written\n")

        except Exception:
            print(f"[{i+1}] ✗ ERROR on: {book.get('title', '?')}")
            traceback.print_exc()
            print()

    print("✅ Done")


if __name__ == "__main__":
    main()