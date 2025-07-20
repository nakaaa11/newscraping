import json
import gspread # type: ignore
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_sheets_client(client_id: str, client_secret: str):
    """
    OAuth2クライアント認証を使って gspread クライアントを生成
    """
    try:
        print("Checking for existing token...")
        creds = None
        
        # トークンファイルが存在する場合は読み込み
        if os.path.exists('token.pickle'):
            print("Found existing token file, loading...")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            print("Token loaded successfully!")
        else:
            print("No existing token found.")
        
        # 有効な認証情報がない場合は新しいトークンを取得
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Token expired, refreshing...")
                creds.refresh(Request())
                print("Token refreshed successfully!")
            else:
                print("Getting new token...")
                # OAuth2クライアント情報を設定
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                        }
                    },
                    SCOPES
                )
                print("Starting OAuth flow...")
                creds = flow.run_local_server(port=0)
                print("OAuth flow completed!")
            
            # トークンを保存
            print("Saving token...")
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            print("Token saved successfully!")
        
        print("Authorizing gspread client...")
        gc = gspread.authorize(creds)
        print("gspread client authorized successfully!")
        return gc
        
    except Exception as e:
        print(f"Error in get_sheets_client: {e}")
        print(f"Error type: {type(e).__name__}")
        raise