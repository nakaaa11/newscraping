# ニュース収集システム

このプロジェクトは、複数のニュースソースからRSSフィードを取得し、Google Sheetsに書き込むPythonアプリケーションです。

## 機能

- 複数のニュースソースからのRSSフィード取得
- Google Sheetsへの自動書き込み
- Slack通知機能
- エラーハンドリングとログ出力

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 設定ファイルの作成

`config.template.json`を`config.json`にコピーして、以下の情報を設定してください：

#### Google Sheets設定
- `spreadsheet_id`: Google SheetsのスプレッドシートID
- `client_id`: Google OAuth2クライアントID
- `client_secret`: Google OAuth2クライアントシークレット

#### Slack設定
- `token`: Slack Bot User OAuth Token
- `channel`: 通知先チャンネル名（例: "#general"）
- `enabled`: 通知機能の有効/無効

### 3. Google Sheets API設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Google Sheets APIを有効化
3. OAuth2クライアントIDとシークレットを取得
4. スプレッドシートの共有設定でサービスアカウントに権限を付与

### 4. Slack API設定

1. [Slack API](https://api.slack.com/apps)でアプリを作成
2. Bot Token Scopesを設定：
   - `chat:write`
   - `chat:write.public`
   - `channels:read`
3. アプリをワークスペースにインストール
4. Bot User OAuth Tokenを取得

## 使用方法

### 基本的な実行

```bash
python main.py
```

### デバッグ用スクリプト

```bash
# スクレイピングテスト
python debug_scraper.py

# Google Sheets認証テスト
python debug_auth.py

# Google Sheets書き込みテスト
python debug_sheets.py

# 詳細統計表示
python test_details.py
```

## ニュースソース

現在サポートされているニュースソース：

- NHK総合
- 朝日新聞
- 金融庁
- Bloomberg
- Wall Street Journal
- CNBC
- Financial Times
- The Economist
- 日経新聞
- Yahoo Finance
- MarketWatch
- TechCrunch

## ファイル構成

```
news_scraping/
├── main.py              # メインアプリケーション
├── scraper.py           # スクレイピング機能
├── auth.py              # Google認証
├── sheets.py            # Google Sheets操作
├── slack_notifier.py    # Slack通知機能
├── config.json          # 設定ファイル（機密情報）
├── config.template.json # 設定テンプレート
├── requirements.txt     # 依存関係
└── README.md           # このファイル
```

## 注意事項

- `config.json`には機密情報が含まれているため、Gitにコミットされません
- 初回実行時はGoogle OAuth2認証が必要です
- Slack通知機能を使用する場合は、適切なスコープ設定が必要です

## トラブルシューティング

### Google Sheets認証エラー
- OAuth2クライアントIDとシークレットが正しく設定されているか確認
- スプレッドシートの共有設定を確認

### Slack通知エラー
- Bot Tokenが正しく設定されているか確認
- チャンネル名が正しいか確認
- ボットがチャンネルに参加しているか確認

### RSSフィードエラー
- URLが有効か確認
- ネットワーク接続を確認
- 一部のサイトはアクセス制限がある場合があります 