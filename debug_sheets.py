#!/usr/bin/env python3
"""
Google Sheets書き込み機能のデバッグ用スクリプト
"""

import json
import pandas as pd
from scraper import collect_all
from sheets import write_to_sheet

def test_sheets_write():
    print("=== Google Sheets書き込みテスト開始 ===")
    
    try:
        # 設定ファイルの読み込み
        print("1. 設定ファイルの読み込み...")
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"   設定読み込み成功")
        
        # テストデータの作成
        print("2. テストデータの作成...")
        df = collect_all(config['feeds'])
        print(f"   テストデータ作成成功: {len(df)}件の記事")
        
        # Google Sheetsへの書き込みテスト
        print("3. Google Sheetsへの書き込みテスト...")
        write_to_sheet(df, config)
        print("   Google Sheetsへの書き込み成功")
        
        print("=== Google Sheets書き込みテスト完了 ===")
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        print(f"エラータイプ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_sheets_write() 