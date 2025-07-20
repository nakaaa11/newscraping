# RSS フィードを取得し、記事情報を抽出する

# scraper.py
import feedparser
import pandas as pd
import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

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
            'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
        })
    return items

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
                        'published': datetime.datetime.now(datetime.UTC).isoformat(),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
                    if len(news_items) >= 10:  # 最新10件まで
                        break
        
        print(f"金融庁から {len(news_items)} 件のニュースを取得")
        return news_items
        
    except Exception as e:
        print(f"金融庁のスクレイピングエラー: {e}")
        return []

def scrape_nhk_news() -> List[Dict]:
    """NHKニュースのウェブサイトからニュースをスクレイピング"""
    try:
        print("NHKニュースのウェブサイトをスクレイピング中...")
        urls = [
            "https://www3.nhk.or.jp/news/",
            "https://www3.nhk.or.jp/news/easy/",
            "https://www3.nhk.or.jp/news/special/",
            "https://www3.nhk.or.jp/news/politics/",
            "https://www3.nhk.or.jp/news/economy/",
            "https://www3.nhk.or.jp/news/society/",
            "https://www3.nhk.or.jp/news/world/",
            "https://www3.nhk.or.jp/news/science/",
            "https://www3.nhk.or.jp/news/sports/"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # ニュース記事のリンクを探す
                news_links = soup.find_all('a', href=True)
                
                for link in news_links:
                    href = link.get('href')
                    if href and '/news/' in href and not href.startswith('http'):
                        # 相対URLを絶対URLに変換
                        if href.startswith('/'):
                            full_url = f"https://www3.nhk.or.jp{href}"
                        else:
                            full_url = f"https://www3.nhk.or.jp/{href}"
                        
                        title = link.get_text(strip=True)
                        if title and len(title) > 10:  # 意味のあるタイトルのみ
                            all_news_items.append({
                                'source': 'NHKニュース',
                                'title': title,
                                'link': full_url,
                                'published': datetime.datetime.now(datetime.UTC).isoformat(),
                                'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                            })
                
            except Exception as e:
                print(f"NHK {url} のスクレイピングエラー: {e}")
                continue
        
        # 最新50件まで取得（以前は20件）
        all_news_items = all_news_items[:50]
        print(f"NHKニュースから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"NHKニュースのスクレイピングエラー: {e}")
        return []

def scrape_investing_news() -> List[Dict]:
    """Investing.comのウェブサイトからニュースをスクレイピング"""
    try:
        print("Investing.comのニュースをスクレイピング中...")
        # 複数のURLを試す
        urls = [
            "https://jp.investing.com/news/",
            "https://jp.investing.com/news/economic-indicators/",
            "https://jp.investing.com/news/forex-news/"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
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
                                'published': datetime.datetime.now(datetime.UTC).isoformat(),
                                'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                            })
                            
                            if len(news_items) >= 10:  # 最新10件まで
                                break
                
                if news_items:
                    break  # 成功したらループを抜ける
                    
            except Exception as e:
                print(f"Investing.com {url} のスクレイピングエラー: {e}")
                continue
        
        print(f"Investing.comから {len(news_items)} 件のニュースを取得")
        return news_items
        
    except Exception as e:
        print(f"Investing.comのスクレイピングエラー: {e}")
        return []

def scrape_bloomberg_news() -> List[Dict]:
    """BloombergのRSSフィードからニュースを取得"""
    try:
        print("Bloombergのニュースを取得中...")
        url = "https://feeds.bloomberg.com/markets/news.rss"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # RSSフィードとして解析
        parsed = feedparser.parse(response.content)
        news_items = []
        
        for entry in parsed.entries[:10]:  # 最新10件
            news_items.append({
                'source': 'Bloomberg',
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
            })
        
        print(f"Bloombergから {len(news_items)} 件のニュースを取得")
        return news_items
        
    except Exception as e:
        print(f"Bloombergの取得エラー: {e}")
        return []

def scrape_wsj_news() -> List[Dict]:
    """Wall Street JournalのRSSフィードからニュースを取得"""
    try:
        print("Wall Street Journalのニュースを取得中...")
        urls = [
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "https://feeds.a.dj.com/rss/RSSBusinessNews.xml"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'Wall Street Journal',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"WSJ {url} の取得エラー: {e}")
                continue
        
        print(f"Wall Street Journalから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"Wall Street Journalの取得エラー: {e}")
        return []

def scrape_bss_news() -> List[Dict]:
    """BSS（Business Standard）のRSSフィードからニュースを取得"""
    try:
        print("BSSのニュースを取得中...")
        urls = [
            "https://www.business-standard.com/rss/economy-policy-103.rss",
            "https://www.business-standard.com/rss/markets-102.rss",
            "https://www.business-standard.com/rss/companies-101.rss",
            # 代替URL
            "https://www.business-standard.com/rss/current-news-1.rss",
            "https://www.business-standard.com/rss/top-stories-1.rss"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'BSS',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"BSS {url} の取得エラー: {e}")
                continue
        
        print(f"BSSから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"BSSの取得エラー: {e}")
        return []

def scrape_reuters_news() -> List[Dict]:
    """ReutersのRSSフィードからニュースを取得（BSSの代替）"""
    try:
        print("Reutersのニュースを取得中...")
        urls = [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.reuters.com/reuters/worldNews",
            "https://feeds.reuters.com/reuters/marketsNews"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'Reuters',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"Reuters {url} の取得エラー: {e}")
                continue
        
        print(f"Reutersから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"Reutersの取得エラー: {e}")
        return []

def scrape_cnbc_news() -> List[Dict]:
    """CNBCのRSSフィードからニュースを取得（Investing.comの代替）"""
    try:
        print("CNBCのニュースを取得中...")
        urls = [
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://www.cnbc.com/id/10000664/device/rss/rss.html",
            "https://www.cnbc.com/id/100727362/device/rss/rss.html"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'CNBC',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"CNBC {url} の取得エラー: {e}")
                continue
        
        print(f"CNBCから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"CNBCの取得エラー: {e}")
        return []

def scrape_financial_times_news() -> List[Dict]:
    """Financial TimesのRSSフィードからニュースを取得"""
    try:
        print("Financial Timesのニュースを取得中...")
        urls = [
            "https://www.ft.com/rss/home",
            "https://www.ft.com/rss/world",
            "https://www.ft.com/rss/companies"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'Financial Times',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"Financial Times {url} の取得エラー: {e}")
                continue
        
        print(f"Financial Timesから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"Financial Timesの取得エラー: {e}")
        return []

def scrape_economist_news() -> List[Dict]:
    """The EconomistのRSSフィードからニュースを取得"""
    try:
        print("The Economistのニュースを取得中...")
        urls = [
            "https://www.economist.com/finance-and-economics/rss.xml",
            "https://www.economist.com/business/rss.xml",
            "https://www.economist.com/international/rss.xml"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'The Economist',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"The Economist {url} の取得エラー: {e}")
                continue
        
        print(f"The Economistから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"The Economistの取得エラー: {e}")
        return []

def scrape_nikkei_news() -> List[Dict]:
    """日経新聞のウェブサイトからニュースをスクレイピング"""
    try:
        print("日経新聞のニュースをスクレイピング中...")
        urls = [
            "https://www.nikkei.com/news/",
            "https://www.nikkei.com/news/politics/",
            "https://www.nikkei.com/news/economy/",
            "https://www.nikkei.com/news/society/",
            "https://www.nikkei.com/news/world/",
            "https://www.nikkei.com/news/technology/",
            "https://www.nikkei.com/news/companies/",
            "https://www.nikkei.com/news/markets/",
            "https://www.nikkei.com/news/finance/",
            "https://www.nikkei.com/news/industry/",
            "https://www.nikkei.com/news/energy/",
            "https://www.nikkei.com/news/automotive/",
            "https://www.nikkei.com/news/electronics/",
            "https://www.nikkei.com/news/construction/",
            "https://www.nikkei.com/news/retail/",
            "https://www.nikkei.com/news/services/",
            "https://www.nikkei.com/news/it/",
            "https://www.nikkei.com/news/media/",
            "https://www.nikkei.com/news/healthcare/",
            "https://www.nikkei.com/news/food/",
            "https://www.nikkei.com/news/chemicals/",
            "https://www.nikkei.com/news/materials/",
            "https://www.nikkei.com/news/machinery/",
            "https://www.nikkei.com/news/steel/",
            "https://www.nikkei.com/news/nonferrous/",
            "https://www.nikkei.com/news/transportation/",
            "https://www.nikkei.com/news/information_communications/",
            "https://www.nikkei.com/news/finance_insurance/",
            "https://www.nikkei.com/news/real_estate/"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # ニュース記事のリンクを探す
                news_links = soup.find_all('a', href=True)
                
                for link in news_links:
                    href = link.get('href')
                    if href and '/news/' in href and not href.startswith('http'):
                        # 相対URLを絶対URLに変換
                        if href.startswith('/'):
                            full_url = f"https://www.nikkei.com{href}"
                        else:
                            full_url = f"https://www.nikkei.com/{href}"
                        
                        title = link.get_text(strip=True)
                        if title and len(title) > 10:  # 意味のあるタイトルのみ
                            all_news_items.append({
                                'source': '日経新聞',
                                'title': title,
                                'link': full_url,
                                'published': datetime.datetime.now(datetime.UTC).isoformat(),
                                'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                            })
                
            except Exception as e:
                print(f"日経新聞 {url} のスクレイピングエラー: {e}")
                continue
        
        # 最新100件まで取得（以前は16件）
        all_news_items = all_news_items[:100]
        print(f"日経新聞から {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"日経新聞のスクレイピングエラー: {e}")
        return []

def scrape_yahoo_finance_news() -> List[Dict]:
    """Yahoo FinanceのRSSフィードからニュースを取得"""
    try:
        print("Yahoo Financeのニュースを取得中...")
        urls = [
            "https://feeds.finance.yahoo.com/rss/2.0/headline",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^DJI"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'Yahoo Finance',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"Yahoo Finance {url} の取得エラー: {e}")
                continue
        
        print(f"Yahoo Financeから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"Yahoo Financeの取得エラー: {e}")
        return []

def scrape_marketwatch_news() -> List[Dict]:
    """MarketWatchのRSSフィードからニュースを取得"""
    try:
        print("MarketWatchのニュースを取得中...")
        urls = [
            "https://feeds.marketwatch.com/marketwatch/topstories/",
            "https://feeds.marketwatch.com/marketwatch/marketpulse/",
            "https://feeds.marketwatch.com/marketwatch/realheadlines/"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'MarketWatch',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"MarketWatch {url} の取得エラー: {e}")
                continue
        
        print(f"MarketWatchから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"MarketWatchの取得エラー: {e}")
        return []

def scrape_techcrunch_news() -> List[Dict]:
    """TechCrunchのRSSフィードからニュースを取得"""
    try:
        print("TechCrunchのニュースを取得中...")
        urls = [
            "https://techcrunch.com/feed/",
            "https://techcrunch.com/category/startups/feed/",
            "https://techcrunch.com/category/enterprise/feed/"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_news_items = []
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # RSSフィードとして解析
                parsed = feedparser.parse(response.content)
                
                for entry in parsed.entries[:5]:  # 各フィードから最新5件
                    all_news_items.append({
                        'source': 'TechCrunch',
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'fetched_at': datetime.datetime.now(datetime.UTC).isoformat()
                    })
                    
            except Exception as e:
                print(f"TechCrunch {url} の取得エラー: {e}")
                continue
        
        print(f"TechCrunchから {len(all_news_items)} 件のニュースを取得")
        return all_news_items
        
    except Exception as e:
        print(f"TechCrunchの取得エラー: {e}")
        return []

def collect_all(feeds: List[Dict]) -> pd.DataFrame:
    """複数のフィードからデータを収集し、DataFrame を返す"""
    all_items = []
    
    # RSSフィードからデータを収集
    for feed in feeds:
        try:
            items = fetch_feed(feed['url'], feed['name'])
            all_items.extend(items)
        except Exception as e:
            print(f"RSSフィード {feed['name']} の取得エラー: {e}")
    
    # ウェブスクレイピングでデータを収集
    fsa_items = scrape_fsa_news()
    all_items.extend(fsa_items)
    
    nhk_items = scrape_nhk_news()
    all_items.extend(nhk_items)
    
    investing_items = scrape_investing_news()
    all_items.extend(investing_items)
    
    # Bloombergのニュースを追加
    bloomberg_items = scrape_bloomberg_news()
    all_items.extend(bloomberg_items)
    
    # Wall Street Journalのニュースを追加
    wsj_items = scrape_wsj_news()
    all_items.extend(wsj_items)
    
    # BSSのニュースを追加
    bss_items = scrape_bss_news()
    all_items.extend(bss_items)
    
    # Reutersのニュースを追加
    reuters_items = scrape_reuters_news()
    all_items.extend(reuters_items)

    # CNBCのニュースを追加
    cnbc_items = scrape_cnbc_news()
    all_items.extend(cnbc_items)
    
    # Financial Timesのニュースを追加
    financial_times_items = scrape_financial_times_news()
    all_items.extend(financial_times_items)

    # The Economistのニュースを追加
    economist_items = scrape_economist_news()
    all_items.extend(economist_items)

    # 日経新聞のニュースを追加
    nikkei_items = scrape_nikkei_news()
    all_items.extend(nikkei_items)

    # Yahoo Financeのニュースを追加
    yahoo_finance_items = scrape_yahoo_finance_news()
    all_items.extend(yahoo_finance_items)

    # MarketWatchのニュースを追加
    marketwatch_items = scrape_marketwatch_news()
    all_items.extend(marketwatch_items)

    # TechCrunchのニュースを追加
    techcrunch_items = scrape_techcrunch_news()
    all_items.extend(techcrunch_items)
    
    # 重複を除去
    seen_titles = set()
    unique_items = []
    for item in all_items:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_items.append(item)
    
    df = pd.DataFrame(unique_items)
    return df