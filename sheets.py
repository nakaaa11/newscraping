from auth import get_sheets_client
import pandas as pd

def write_to_sheet(df: pd.DataFrame, config: dict):
    """DataFrame を指定スプレッドシートに書き込む"""
    try:
        print("Starting Google Sheets authentication...")
        client = get_sheets_client(config['client_id'], config['client_secret'])
        print("Authentication successful!")
        
        print(f"Opening spreadsheet with ID: {config['spreadsheet_id']}")
        sh = client.open_by_key(config['spreadsheet_id'])
        worksheet = sh.sheet1  # sheet1 を利用
        print("Spreadsheet opened successfully!")

        # シートをクリア
        print("Clearing existing data...")
        worksheet.clear()
        print("Sheet cleared!")

        # ヘッダ＋データを一括書き込み
        values = [df.columns.values.tolist()] + df.values.tolist()
        print(f"Writing {len(values)} rows to sheet...")
        worksheet.update(values)
        print("Data written successfully!")
        
    except KeyError as e:
        print(f"Configuration error: Missing key {e}")
        print("Please check your config.json file")
        raise
    except Exception as e:
        print(f"Error in write_to_sheet: {e}")
        print(f"Error type: {type(e).__name__}")
        raise