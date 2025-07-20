#!/usr/bin/env python3
"""
認証モジュールのデバッグ用スクリプト
"""

import json
from auth import get_sheets_client

def test_auth():
    print("=== 認証テスト開始 ===")
    
    try:
        # 設定ファイルの読み込み
        print("1. 設定ファイルの読み込み...")
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"   クライアントID: {config['client_id']}")
        print(f"   クライアントシークレット: {config['client_secret'][:10]}...")
        
        # 認証クライアントの作成
        print("2. 認証クライアントの作成...")
        client = get_sheets_client(config['client_id'], config['client_secret'])
        print("   認証クライアント作成成功")
        
        # スプレッドシートへのアクセステスト
        print("3. スプレッドシートへのアクセステスト...")
        print(f"   スプレッドシートID: {config['spreadsheet_id']}")
        sh = client.open_by_key(config['spreadsheet_id'])
        print("   スプレッドシートアクセス成功")
        
        # ワークシートの確認
        print("4. ワークシートの確認...")
        worksheet = sh.sheet1
        print(f"   ワークシート名: {worksheet.title}")
        
        print("=== 認証テスト完了 ===")
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        print(f"エラータイプ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_auth() 