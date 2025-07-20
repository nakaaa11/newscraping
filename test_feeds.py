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
        else:
            print('No entries found')
    except Exception as e:
        print(f'Error: {e}')

def main():
    config = json.load(open('config.json', 'r', encoding='utf-8'))
    
    for feed in config['feeds']:
        test_feed(feed['name'], feed['url'])

if __name__ == '__main__':
    main() 