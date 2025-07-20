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

if __name__ == '__main__':
    main() 