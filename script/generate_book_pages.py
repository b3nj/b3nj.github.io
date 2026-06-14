#!/usr/bin/env python3
import json
import os
import re
import yaml

DATA_FILE = "_data/books.json"
OUTPUT_DIR = "books"

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")

def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        books = json.load(f)

    for entry in books:
        isbn_key = next(iter(entry))
        book = entry[isbn_key]
        isbn = isbn_key.replace("ISBN:", "")

        title = book.get("title", "Untitled")
        slug = slugify(title) or isbn

        front_matter = {
            "layout": "book",
            "isbn": isbn,
            "title": title,
        }

        if book.get("subtitle"):
            front_matter["subtitle"] = book["subtitle"]

        if book.get("authors"):
            front_matter["authors"] = [a.get("name") for a in book["authors"] if a.get("name")]

        if book.get("publishers"):
            front_matter["publishers"] = [p.get("name") for p in book["publishers"] if p.get("name")]

        if book.get("publish_date"):
            front_matter["publish_date"] = book["publish_date"]

        if book.get("number_of_pages"):
            front_matter["number_of_pages"] = book["number_of_pages"]

        if book.get("weight"):
            front_matter["weight"] = book["weight"]

        if book.get("cover"):
            front_matter["cover"] = book["cover"]

        if book.get("url"):
            front_matter["source_url"] = book["url"]

        if book.get("identifiers"):
            front_matter["identifiers"] = book["identifiers"]

        page_dir = os.path.join(OUTPUT_DIR, isbn)
        os.makedirs(page_dir, exist_ok=True)

        with open(os.path.join(page_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(front_matter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n")

if __name__ == "__main__":
    main()