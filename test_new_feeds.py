#!/usr/bin/env python3
"""
金融庁とInvesting.comのRSSフィードテスト
"""

import feedparser
import json

def test_feed(name, url):
    print(f'\n=== Testing {name} ===')
    print(f'URL: {url}')
    try:
        parsed = feedparser.parse(url)
        print(f'Status: {parsed.status if hasattr(parsed, "status") else "Unknown"}')
        print(f'Entries found: {len(parsed.entries)}')
        if parsed.entries:
            print(f'First entry title: {parsed.entries[0].get("title", "No title")}')
            print(f'First entry link: {parsed.entries[0].get("link", "No link")}')
        else:
            print('No entries found')
    except Exception as e:
        print(f'Error: {e}')

def main():
    # 金融庁とInvesting.comのテスト用URL
    test_feeds = [
        {"name": "金融庁", "url": "https://www.fsa.go.jp/kouhou/rss.html"},
        {"name": "Investing.com", "url": "https://jp.investing.com/webmaster-tools/rss"},
        {"name": "金融庁（修正版）", "url": "https://www.fsa.go.jp/rss/rss.xml"},
        {"name": "Investing.com（修正版）", "url": "https://jp.investing.com/rss/news_301.xml"}
    ]
    
    for feed in test_feeds:
        test_feed(feed['name'], feed['url'])

if __name__ == '__main__':
    main() 