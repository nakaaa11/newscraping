import json
import pandas as pd
from scraper import collect_all
from sheets import write_to_sheet
from auth import get_sheets_client
from slack_notifier import SlackNotifier
import traceback
import datetime
import os
from dotenv import load_dotenv

def load_config():
    """設定ファイルを読み込む"""
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    # .envの読み込み
    load_dotenv()
    # Slack情報を環境変数で上書き
    if 'slack' not in config:
        config['slack'] = {}
    config['slack']['token'] = os.getenv('SLACK_TOKEN', config['slack'].get('token'))
    config['slack']['channel'] = os.getenv('SLACK_CHANNEL', config['slack'].get('channel'))
    return config

def get_current_sheet_name():
    """現在の年月を取得してシート名を生成"""
    current_date = datetime.datetime.now()
    return current_date.strftime("%Y%m")  # 例: 202507, 202508

def job():
    """メインのジョブ関数"""
    try:
        print("Starting news collection job...")
        
        # 設定を読み込み
        config = load_config()
        
        # Slack通知を初期化
        slack_enabled = config.get('slack', {}).get('enabled', False)
        slack_notifier = None
        
        if slack_enabled:
            slack_config = config['slack']
            slack_notifier = SlackNotifier(
                token=slack_config['token'],
                channel=slack_config['channel']
            )
            print("Slack通知機能が有効化されました")
        
        # ニュースを収集
        df = collect_all(config.get('rss_feeds', []))
        
        if df.empty:
            error_msg = "ニュースの収集に失敗しました"
            print(error_msg)
            if slack_notifier:
                slack_notifier.send_error_notification(error_msg)
            return
        
        print(f"Job executed: {len(df)} articles collected.")
        print("Sample articles:")
        print(df.head())
        
        # Google Sheets認証
        print("Starting Google Sheets authentication...")
        try:
            gc = get_sheets_client(
                config['google_sheets']['client_id'],
                config['google_sheets']['client_secret']
            )
            print("Google Sheets認証成功")
        except Exception as e:
            error_msg = f"Google Sheets認証に失敗しました: {str(e)}"
            print(error_msg)
            if slack_notifier:
                slack_notifier.send_error_notification(error_msg)
            return
        
        # シート名を取得
        sheet_name = get_current_sheet_name()
        print(f"Target sheet: {sheet_name}")
        
        # Google Sheetsに書き込み
        try:
            write_to_sheet(df, config)
            print("Successfully wrote to Google Sheets!")
            
            # Slack通知を送信
            if slack_notifier:
                # ソース別記事数を計算
                sources = df['source'].value_counts().to_dict()
                total_articles = len(df)
                
                # 成功通知を送信（シート名を含む）
                slack_success = slack_notifier.send_news_summary(df, total_articles, sources, sheet_name)
                if slack_success:
                    print("Slack通知送信完了")
                else:
                    print("Slack通知送信に失敗しました")
        except Exception as e:
            error_msg = f"Google Sheetsへの書き込みに失敗しました: {str(e)}"
            print(error_msg)
            if slack_notifier:
                slack_notifier.send_error_notification(error_msg)
                
    except Exception as e:
        error_msg = f"予期しないエラーが発生しました: {str(e)}"
        print(error_msg)
        print("詳細エラー情報:")
        traceback.print_exc()
        
        # Slack通知を送信
        try:
            config = load_config()
            slack_enabled = config.get('slack', {}).get('enabled', False)
            if slack_enabled:
                slack_config = config['slack']
                slack_notifier = SlackNotifier(
                    token=slack_config['token'],
                    channel=slack_config['channel']
                )
                slack_notifier.send_error_notification(error_msg)
        except Exception as slack_error:
            print(f"Slack通知送信エラー: {slack_error}")

if __name__ == "__main__":
    # 一度実行
    job()
    print("実行完了")