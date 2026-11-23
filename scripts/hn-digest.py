#!/usr/bin/env python3
"""
Daily Hacker News digest:
  - writes a Jekyll collection document to _hackers/YYYY-MM-DD-hackers-digest.md
  - optionally sends the digest to Telegram (if credentials are set)

Env vars:
  TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID  - optional; Telegram is skipped if missing
  HN_STORY_COUNT  - stories to include (default 10)
  HN_MIN_SCORE    - minimum score (default 100)
  OUT_DIR         - output dir (default _hackers)
"""

import datetime as dt
import html
import os
import re
import sys
import requests

HN_API = "https://hacker-news.firebaseio.com/v0"
TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def get_item(item_id):
    r = requests.get(f"{HN_API}/item/{item_id}.json", timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_stories(count, min_score):
    r = requests.get(f"{HN_API}/topstories.json", timeout=10)
    r.raise_for_status()
    ids = r.json()[:80]
    stories = []
    for sid in ids:
        item = get_item(sid)
        if not item or item.get("type") != "story" or item.get("score", 0) < min_score:
            continue
        stories.append(item)
        if len(stories) >= count:
            break
    if not stories:
        stories = [get_item(sid) for sid in ids[:count]]
    return stories


def md_escape(text):
    return re.sub(r"([\\`*_\[\]<>])", r"\\\1", text)


def hn_link(s):
    return f"https://news.ycombinator.com/item?id={s['id']}"


def build_markdown(stories, today):
    front = (
        "---\n"
        "layout: post\n"
        f"title: \"Hackers digest - {today:%Y-%m-%d}\"\n"
        f"date: {today:%Y-%m-%d} 07:00:00 +0000\n"
        "category: hackers\n"
        "tags: [hacker-news, digest]\n"
        "---\n\n"
    )
    lines = []
    for i, s in enumerate(stories, 1):
        title = md_escape(s.get("title", "(no title)"))
        url = s.get("url", hn_link(s))
        lines.append(f"{i}. [{title}]({url})  ")
        lines.append(f"   ⬆ {s.get('score', 0)} · [{s.get('descendants', 0)} comments]({hn_link(s)})")
        lines.append("")
    return front + "\n".join(lines) + "\n"


def build_telegram(stories):
    lines = ["<b>📰 Hacker News Daily Digest</b>", ""]
    for i, s in enumerate(stories, 1):
        url = s.get("url", hn_link(s))
        lines.append(f"{i}. <a href=\"{html.escape(url)}\">{html.escape(s.get('title', '(no title)'))}</a>")
        lines.append(f"   ⬆ {s.get('score', 0)} | 💬 <a href=\"{hn_link(s)}\">{s.get('descendants', 0)} comments</a>")
        lines.append("")
    return "\n".join(lines)


def send_telegram(text, token, chat_id):
    r = requests.post(
        TELEGRAM_API.format(token=token),
        data={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
        timeout=10,
    )
    if not r.ok:
        print(f"Telegram error: {r.status_code} {r.text}", file=sys.stderr)
        r.raise_for_status()


def main():
    count = int(os.environ.get("HN_STORY_COUNT", "10"))
    min_score = int(os.environ.get("HN_MIN_SCORE", "100"))
    out_dir = os.environ.get("OUT_DIR", "_hackers")
    today = dt.datetime.now(dt.timezone.utc).date()

    stories = fetch_stories(count, min_score)

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{today:%Y-%m-%d}-hackers-digest.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_markdown(stories, today))
    print(f"Wrote {path}")

    token = os.environ.get("TELEGRAM_API_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        send_telegram(build_telegram(stories)[:4000], token, chat_id)
        print("Telegram message sent")
    else:
        print("Telegram credentials not set, skipping")


if __name__ == "__main__":
    main()
