# ニューススクレイピングプロジェクト

RSSフィードからニュース記事を自動取得し、Google Sheetsに書き込むPythonプロジェクトです。

## 機能

- RSSフィードからのニュース記事自動取得
- Google Sheetsへの自動書き込み
- スケジュール実行機能（APScheduler）
- エラーハンドリング機能

## 対応RSSフィード

- NHK総合
- 朝日新聞

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Consoleでの設定

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成
3. Google Sheets APIを有効化
4. OAuth 2.0クライアントIDを作成
5. OAuth同意画面を設定

### 3. 設定ファイルの更新

`config.json`ファイルを編集して、以下を設定：

```json
{
  "feeds": [
    {"name": "NHK総合", "url": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    {"name": "朝日新聞", "url": "https://www.asahi.com/rss/asahi/newsheadlines.rdf"}
  ],
  "spreadsheet_id": "YOUR_SPREADSHEET_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

### 4. Googleスプレッドシートの準備

1. 新しいGoogleスプレッドシートを作成
2. スプレッドシートIDを取得（URLの一部）
3. `config.json`の`spreadsheet_id`を更新

## 使用方法

### 単発実行

```bash
python main.py
```

### スケジュール実行

`main.py`のコメントアウトされた部分を有効化して、定期的な実行を設定できます。

## ファイル構成

- `main.py`: メインアプリケーション
- `scraper.py`: RSSフィード取得機能
- `sheets.py`: Google Sheets書き込み機能
- `auth.py`: Google認証機能
- `config.json`: 設定ファイル
- `requirements.txt`: 依存関係リスト

## デバッグ

各機能を個別にテストするためのデバッグスクリプトが含まれています：

- `debug_scraper.py`: スクレイパーテスト
- `debug_auth.py`: 認証テスト
- `debug_sheets.py`: Google Sheets書き込みテスト

## 注意事項

- `token.pickle`ファイルは認証情報を含むため、`.gitignore`に含まれています
- 初回実行時はOAuth認証が必要です
- Google Sheets APIの利用制限に注意してください

## ライセンス

MIT License 