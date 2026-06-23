#!/usr/bin/env python3
import json
import os
import re
import urllib.request
import yaml

DATA_FILE = "_data/books.json"
OUTPUT_DIR = "books"

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")

def download_cover(cover_edition_key, dest_path):
    url = f"https://covers.openlibrary.org/b/olid/{cover_edition_key}-M.jpg"
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print(f"Cover download failed for {cover_edition_key}: {e}")
        return False


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        isbn_list = book.get("isbn", [])
        isbn = isbn_list[0] if isbn_list else None

        title = book.get("title", "Untitled")
        slug = slugify(title) or isbn or "unknown"

        # Start with layout, then dump everything from the JSON
        front_matter = {"layout": "book"}
        front_matter.update(book)

        page_dir = os.path.join(OUTPUT_DIR, isbn if isbn else slug)
        os.makedirs(page_dir, exist_ok=True)

        # Download cover
        cover_edition_key = book.get("cover_edition_key")
        if cover_edition_key:
            cover_path = os.path.join(page_dir, "cover.jpg")
            if not os.path.exists(cover_path):
                if download_cover(cover_edition_key, cover_path):
                    front_matter["cover_local"] = f"/books/{isbn if isbn else slug}/cover.jpg"
            else:
                front_matter["cover_local"] = f"/books/{isbn if isbn else slug}/cover.jpg"

        with open(os.path.join(page_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(front_matter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n")