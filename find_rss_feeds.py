#!/usr/bin/env python3
"""
金融庁とInvesting.comの正しいRSSフィードURLを探索
"""

import feedparser
import requests
from bs4 import BeautifulSoup

def test_rss_url(url, name):
    print(f'\n=== Testing {name} ===')
    print(f'URL: {url}')
    try:
        parsed = feedparser.parse(url)
        print(f'Status: {parsed.status if hasattr(parsed, "status") else "Unknown"}')
        print(f'Entries found: {len(parsed.entries)}')
        if parsed.entries:
            print(f'First entry title: {parsed.entries[0].get("title", "No title")}')
            return True
        else:
            print('No entries found')
            return False
    except Exception as e:
        print(f'Error: {e}')
        return False

def find_rss_links(base_url, name):
    print(f'\n=== Searching for RSS links on {name} ===')
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # RSSリンクを探す
        rss_links = []
        for link in soup.find_all('link'):
            if link.get('type') in ['application/rss+xml', 'application/atom+xml']:
                href = link.get('href')
                if href:
                    rss_links.append(href)
        
        # 相対URLを絶対URLに変換
        for i, link in enumerate(rss_links):
            if link.startswith('/'):
                rss_links[i] = base_url.rstrip('/') + link
            elif not link.startswith('http'):
                rss_links[i] = base_url.rstrip('/') + '/' + link
        
        print(f'Found {len(rss_links)} RSS links:')
        for link in rss_links:
            print(f'  {link}')
        
        return rss_links
    except Exception as e:
        print(f'Error searching {base_url}: {e}')
        return []

def main():
    # 金融庁のRSSフィード候補
    fsa_candidates = [
        "https://www.fsa.go.jp/rss/rss.xml",
        "https://www.fsa.go.jp/kouhou/rss.xml",
        "https://www.fsa.go.jp/news/rss.xml",
        "https://www.fsa.go.jp/policy/rss.xml"
    ]
    
    # Investing.comのRSSフィード候補
    investing_candidates = [
        "https://jp.investing.com/rss/news.xml",
        "https://jp.investing.com/rss/markets.xml",
        "https://jp.investing.com/rss/economic-calendar.xml",
        "https://jp.investing.com/rss/analysis.xml"
    ]
    
    print("=== 金融庁 RSSフィードテスト ===")
    fsa_working = False
    for url in fsa_candidates:
        if test_rss_url(url, f"金融庁 - {url}"):
            fsa_working = True
            print(f"✅ 金融庁の動作するRSSフィード: {url}")
            break
    
    if not fsa_working:
        print("❌ 金融庁のRSSフィードが見つかりませんでした")
        # 金融庁のサイトからRSSリンクを探す
        find_rss_links("https://www.fsa.go.jp/", "金融庁")
    
    print("\n=== Investing.com RSSフィードテスト ===")
    investing_working = False
    for url in investing_candidates:
        if test_rss_url(url, f"Investing.com - {url}"):
            investing_working = True
            print(f"✅ Investing.comの動作するRSSフィード: {url}")
            break
    
    if not investing_working:
        print("❌ Investing.comのRSSフィードが見つかりませんでした")
        # Investing.comのサイトからRSSリンクを探す
        find_rss_links("https://jp.investing.com/", "Investing.com")

if __name__ == '__main__':
    main() 