import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, List
import datetime

class SlackNotifier:
    def __init__(self, token: str, channel: str = "#scraping"):
        """
        Slack通知クラス
        
        Args:
            token (str): Slack Bot User OAuth Token
            channel (str): 通知先チャンネル名
        """
        self.client = WebClient(token=token)
        self.channel = channel
        
    def send_notification(self, message: str) -> bool:
        """
        Slackにメッセージを送信
        
        Args:
            message (str): 送信するメッセージ
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=message
            )
            print(f"Slack通知送信成功: {response['ts']}")
            return True
            
        except SlackApiError as e:
            print(f"Slack通知送信エラー: {e.response['error']}")
            return False
        except Exception as e:
            print(f"Slack通知送信エラー: {e}")
            return False
    
    def send_news_summary(self, df, total_articles: int, sources: Dict[str, int]) -> bool:
        """
        ニュース収集完了のサマリーをSlackに送信
        
        Args:
            df: 収集されたニュースのDataFrame
            total_articles (int): 総記事数
            sources (Dict[str, int]): ソース別記事数
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            # 現在時刻を取得
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # メッセージを作成
            message = f"""
📰 *ニュース収集完了通知* 📰

🕐 実行時刻: {now}
📊 総記事数: {total_articles}件
📈 ソース数: {len(sources)}件

📋 *ソース別記事数:*
"""
            
            # ソース別記事数を追加
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                message += f"• {source}: {count}件\n"
            
            # 最新記事のサンプルを追加
            message += "\n📝 *最新記事サンプル:*\n"
            for i, row in df.head(5).iterrows():
                source = row['source']
                title = row['title'][:100] + "..." if len(row['title']) > 100 else row['title']
                message += f"• [{source}] {title}\n"
            
            message += "\n✅ Google Sheetsに正常に書き込み完了"
            
            return self.send_notification(message)
            
        except Exception as e:
            print(f"Slack通知作成エラー: {e}")
            return False
    
    def send_error_notification(self, error_message: str) -> bool:
        """
        エラー通知をSlackに送信
        
        Args:
            error_message (str): エラーメッセージ
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            message = f"""
⚠️ *ニュース収集エラー通知* ⚠️

🕐 発生時刻: {now}
❌ エラー内容: {error_message}

🔧 システム管理者に連絡してください。
"""
            
            return self.send_notification(message)
            
        except Exception as e:
            print(f"Slackエラー通知作成エラー: {e}")
            return False 