import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, List
import datetime
import os

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
    
    def send_news_summary(self, df, total_articles: int, sources: Dict[str, int], sheet_name: str = None) -> bool:
        """
        ニュース収集完了のサマリーをSlackに送信（リッチ版）
        """
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # カテゴリ別件数
            cat_summary = ""
            if 'category' in df.columns:
                cat_counts = df['category'].value_counts()
                for cat, cnt in cat_counts.items():
                    cat_summary += f"• {cat}: {cnt}件\n"
            # 重要度ランキング上位3件
            top_articles = ""
            if 'importance' in df.columns and 'rank' in df.columns:
                top_df = df.sort_values('importance', ascending=False).head(3)
                for _, row in top_df.iterrows():
                    title = row['title'][:80] + "..." if len(row['title']) > 80 else row['title']
                    link = row.get('link', '')
                    summary = row.get('summary', '')[:100] + "..." if len(row.get('summary', '')) > 100 else row.get('summary', '')
                    category = row.get('category', 'N/A')
                    score = row.get('importance', 'N/A')
                    top_articles += f"• <{link}|{title}>\n　カテゴリ: {category}｜重要度: {score}\n　要約: {summary}\n"
            # エラー件数
            error_count = 0
            error_summary = ""
            try:
                if os.path.exists("error.log"):
                    with open("error.log", encoding="utf-8") as f:
                        lines = f.readlines()
                        error_count = sum(1 for l in lines if "[ERROR]" in l)
                        last_error = next((l for l in reversed(lines) if "[ERROR]" in l), None)
                        if last_error:
                            error_summary = last_error.strip()
            except Exception:
                pass

            message = f"""
📰 *ニュース収集完了通知* 📰

🕐 実行時刻: {now}
📊 総記事数: {total_articles}件
📈 ソース数: {len(sources)}件
📋 書き込み先シート: {sheet_name or 'N/A'}
💾 DB/CSV保存: news.db, news_data.csv

📋 *カテゴリ別記事数:*
{cat_summary if cat_summary else 'N/A'}

📝 *重要度ランキング上位3件:*
{top_articles if top_articles else 'N/A'}

{'⚠️ *直近エラー:* ' + error_summary if error_count else '✅ エラーなし'}

✅ Google Sheets/DB/CSV保存完了
"""
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