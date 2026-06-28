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

def download_cover(cover_edition_key, dest_path):
    url = f"https://covers.openlibrary.org/b/olid/{cover_edition_key}-M.jpg"
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
            # Prefer ISBN-13 (13 digits) over ISBN-10
            isbn_list = book.get("isbn", [])
            isbn = next((i for i in isbn_list if len(i) == 13), None) or (isbn_list[0] if isbn_list else None)

            page_dir = os.path.join(OUTPUT_DIR, isbn if isbn else slug)

            # Rename any existing folder that used a different ISBN
            if isbn_list:
                for old_isbn in isbn_list:
                    old_dir = os.path.join(OUTPUT_DIR, old_isbn)
                    if old_dir != page_dir and os.path.exists(old_dir):
                        print(f"    ↩ Renaming {old_dir} → {page_dir}")
                        os.rename(old_dir, page_dir)
                        break

            title = book.get("title", "Untitled")
            slug = slugify(title) or isbn or "unknown"
            page_dir = os.path.join(OUTPUT_DIR, isbn if isbn else slug)

            print(f"[{i+1}/{len(books)}] {title}")
            print(f"    ISBN: {isbn or 'none'} | folder: {page_dir}")

            front_matter = {"layout": "book"}
            front_matter.update(book)

            os.makedirs(page_dir, exist_ok=True)
            print(f"    ✓ Folder ready")

            cover_edition_key = book.get("cover_edition_key")
            if cover_edition_key:
                cover_path = os.path.join(page_dir, "cover.jpg")
                if not os.path.exists(cover_path):
                    if download_cover(cover_edition_key, cover_path):
                        front_matter["cover_local"] = f"/books/{isbn if isbn else slug}/cover.jpg"
                else:
                    print(f"    ↩ Cover already exists, skipping download")
                    front_matter["cover_local"] = f"/books/{isbn if isbn else slug}/cover.jpg"
            else:
                print(f"    ⚠ No cover_edition_key, skipping cover")

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