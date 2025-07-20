import json
from scraper import collect_all

def main():
    config = json.load(open('config.json', 'r', encoding='utf-8'))
    df = collect_all(config['feeds'])
    
    print(f'Total articles: {len(df)}')
    print(f'Sources: {df["source"].value_counts().to_dict()}')
    print('\nLatest articles from each source:')
    for source in df['source'].unique():
        source_df = df[df['source'] == source]
        latest = source_df.iloc[0]
        print(f'{source}: {latest["title"]}')
    
    print('\n=== 詳細統計 ===')
    print(f'総記事数: {len(df)}')
    print('\nソース別記事数:')
    source_counts = df['source'].value_counts()
    for source, count in source_counts.items():
        print(f'  {source}: {count}件')
    
    print('\n最新記事（各ソースから1件ずつ）:')
    for source in df['source'].unique():
        source_df = df[df['source'] == source]
        latest = source_df.iloc[0]
        print(f'  [{source}] {latest["title"]}')

if __name__ == '__main__':
    main() 