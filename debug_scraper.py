#!/usr/bin/env python3
"""
スクレイパーモジュールのデバッグ用スクリプト
"""

import json
from scraper import collect_all

def test_scraper():
    print("=== スクレイパーテスト開始 ===")
    
    try:
        # 設定ファイルの読み込み
        print("1. 設定ファイルの読み込み...")
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"   設定読み込み成功: {len(config['feeds'])}個のフィード")
        
        # RSSフィードの取得
        print("2. RSSフィードの取得...")
        df = collect_all(config['feeds'])
        print(f"   取得成功: {len(df)}件の記事")
        
        # データの詳細確認
        print("3. データの詳細確認...")
        print(f"   列名: {list(df.columns)}")
        print(f"   ソース別件数:")
        for source in df['source'].unique():
            count = len(df[df['source'] == source])
            print(f"     {source}: {count}件")
        
        # サンプルデータの表示
        print("4. サンプルデータ:")
        print(df.head(3).to_string())
        
        print("=== スクレイパーテスト完了 ===")
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        print(f"エラータイプ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_scraper() 