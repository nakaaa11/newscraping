# RSS フィードを取得し、記事情報を抽出する

# scraper.py
import feedparser
import pandas as pd
import datetime
from typing import List, Dict

def fetch_feed(feed_url: str, source_name: str) -> List[Dict]:
    """RSS フィードを解析し、記事のリストを返す"""
    parsed = feedparser.parse(feed_url)
    items = []
    for entry in parsed.entries:
        items.append({
            'source': source_name,
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': entry.get('published', ''),
            'fetched_at': datetime.datetime.utcnow().isoformat()
        })
    return items


def collect_all(feeds: List[Dict]) -> pd.DataFrame:
    """複数のフィードからデータを収集し、DataFrame を返す"""
    all_items = []
    for feed in feeds:
        items = fetch_feed(feed['url'], feed['name'])
        all_items.extend(items)
    df = pd.DataFrame(all_items)
    return df