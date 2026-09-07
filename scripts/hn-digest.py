#!/usr/bin/env python3
"""
Fetch top Hacker News stories and send a daily digest to Telegram.

Requires environment variables:
  TELEGRAM_BOT_TOKEN - your bot token from @BotFather
  TELEGRAM_CHAT_ID   - your numeric chat ID (get it from @userinfobot)

Optional:
  HN_STORY_COUNT     - how many stories to include (default 10)
  HN_MIN_SCORE       - minimum score to be considered "interesting" (default 100)
"""

import os
import sys
import html
import requests

HN_API = "https://hacker-news.firebaseio.com/v0"
TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def get_top_story_ids(limit=60):
    resp = requests.get(f"{HN_API}/topstories.json", timeout=10)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_item(item_id):
    resp = requests.get(f"{HN_API}/item/{item_id}.json", timeout=10)
    resp.raise_for_status()
    return resp.json()


def build_digest(story_count=10, min_score=100):
    ids = get_top_story_ids(limit=80)
    stories = []
    for sid in ids:
        item = get_item(sid)
        if not item or item.get("type") != "story":
            continue
        if item.get("score", 0) < min_score:
            continue
        stories.append(item)
        if len(stories) >= story_count:
            break

    if not stories:
        # Fallback: relax score filter if nothing cleared the bar
        stories = [get_item(sid) for sid in ids[:story_count]]

    lines = ["<b>📰 Hacker News Daily Digest</b>", ""]
    for i, s in enumerate(stories, 1):
        title = html.escape(s.get("title", "(no title)"))
        score = s.get("score", 0)
        comments = s.get("descendants", 0)
        hn_link = f"https://news.ycombinator.com/item?id={s['id']}"
        url = s.get("url", hn_link)
        lines.append(f"{i}. <a href=\"{html.escape(url)}\">{title}</a>")
        lines.append(f"   ⬆ {score} | 💬 <a href=\"{html.escape(hn_link)}\">{comments} comments</a>")
        lines.append("")

    return "\n".join(lines)


def send_telegram_message(text, token, chat_id):
    resp = requests.post(
        TELEGRAM_API.format(token=token),
        data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=10,
    )
    if not resp.ok:
        print(f"Telegram API error: {resp.status_code} {resp.text}", file=sys.stderr)
        resp.raise_for_status()
    return resp.json()


def main():
    token = os.environ.get("TELEGRAM_API_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Missing TELEGRAM_API_TOKEN or TELEGRAM_CHAT_ID", file=sys.stderr)
        sys.exit(1)

    story_count = int(os.environ.get("HN_STORY_COUNT", "10"))
    min_score = int(os.environ.get("HN_MIN_SCORE", "100"))

    digest = build_digest(story_count=story_count, min_score=min_score)

    # Telegram messages are capped at 4096 chars; split if needed
    max_len = 4000
    for i in range(0, len(digest), max_len):
        send_telegram_message(digest[i:i + max_len], token, chat_id)

    print("Digest sent successfully.")


if __name__ == "__main__":
    main()
