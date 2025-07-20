#!/usr/bin/env python3
"""
金融庁とInvesting.comのウェブサイトから直接ニュースをスクレイピング
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from typing import List, Dict
import time

def scrape_fsa_news() -> List[Dict]:
    """金融庁のウェブサイトからニュースをスクレイピング"""
    try:
        print("金融庁のニュースをスクレイピング中...")
        url = "https://www.fsa.go.jp/news/index.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        news_items = []
        
        # ニュース一覧を探す
        news_links = soup.find_all('a', href=True)
        
        for link in news_links:
            href = link.get('href')
            if href and '/news/' in href and not href.startswith('http'):
                # 相対URLを絶対URLに変換
                if href.startswith('/'):
                    full_url = f"https://www.fsa.go.jp{href}"
                else:
                    full_url = f"https://www.fsa.go.jp/{href}"
                
                title = link.get_text(strip=True)
                if title and len(title) > 10:  # 意味のあるタイトルのみ
                    news_items.append({
                        'source': '金融庁',
                        'title': title,
                        'link': full_url,
                        'published': datetime.datetime.now().isoformat(),
                        'fetched_at': datetime.datetime.utcnow().isoformat()
                    })
                    
                    if len(news_items) >= 10:  # 最新10件まで
                        break
        
        print(f"金融庁から {len(news_items)} 件のニュースを取得")
        return news_items
        
    except Exception as e:
        print(f"金融庁のスクレイピングエラー: {e}")
        return []

def scrape_investing_news() -> List[Dict]:
    """Investing.comのウェブサイトからニュースをスクレイピング"""
    try:
        print("Investing.comのニュースをスクレイピング中...")
        url = "https://jp.investing.com/news/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        news_items = []
        
        # ニュース記事のリンクを探す
        news_links = soup.find_all('a', href=True)
        
        for link in news_links:
            href = link.get('href')
            if href and '/news/' in href and not href.startswith('http'):
                # 相対URLを絶対URLに変換
                if href.startswith('/'):
                    full_url = f"https://jp.investing.com{href}"
                else:
                    full_url = f"https://jp.investing.com/{href}"
                
                title = link.get_text(strip=True)
                if title and len(title) > 10:  # 意味のあるタイトルのみ
                    news_items.append({
                        'source': 'Investing.com',
                        'title': title,
                        'link': full_url,
                        'published': datetime.datetime.now().isoformat(),
                        'fetched_at': datetime.datetime.utcnow().isoformat()
                    })
                    
                    if len(news_items) >= 10:  # 最新10件まで
                        break
        
        print(f"Investing.comから {len(news_items)} 件のニュースを取得")
        return news_items
        
    except Exception as e:
        print(f"Investing.comのスクレイピングエラー: {e}")
        return []

def collect_web_news() -> pd.DataFrame:
    """ウェブスクレイピングでニュースを収集"""
    all_items = []
    
    # 金融庁のニュースを取得
    fsa_items = scrape_fsa_news()
    all_items.extend(fsa_items)
    
    # Investing.comのニュースを取得
    investing_items = scrape_investing_news()
    all_items.extend(investing_items)
    
    # 重複を除去
    seen_titles = set()
    unique_items = []
    for item in all_items:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_items.append(item)
    
    df = pd.DataFrame(unique_items)
    return df

if __name__ == '__main__':
    df = collect_web_news()
    print(f"\n総取得件数: {len(df)}")
    print("\n取得されたニュース:")
    for i, row in df.iterrows():
        print(f"{i+1}. [{row['source']}] {row['title']}") 