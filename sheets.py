from auth import get_sheets_client
import pandas as pd
import datetime

def write_to_sheet(df: pd.DataFrame, config: dict):
    """DataFrame を指定スプレッドシートに月ごとのシートに蓄積書き込み（ソース、タイトル、リンクのみ）"""
    try:
        print("Starting Google Sheets authentication...")
        client = get_sheets_client(
            config['google_sheets']['client_id'], 
            config['google_sheets']['client_secret']
        )
        print("Authentication successful!")
        
        print(f"Opening spreadsheet with ID: {config['google_sheets']['spreadsheet_id']}")
        sh = client.open_by_key(config['google_sheets']['spreadsheet_id'])
        
        # 現在の年月を取得してシート名を生成
        current_date = datetime.datetime.now()
        sheet_name = current_date.strftime("%Y%m")  # 例: 202507, 202508
        
        print(f"Target sheet: {sheet_name}")
        
        # シートが存在するかチェック
        try:
            worksheet = sh.worksheet(sheet_name)
            print(f"Sheet '{sheet_name}' already exists, using existing sheet")
        except:
            print(f"Creating new sheet '{sheet_name}'")
            worksheet = sh.add_worksheet(title=sheet_name, rows=1000, cols=3)
        
        print("Spreadsheet opened successfully!")

        # 既存データの行数を取得
        try:
            existing_data = worksheet.get_all_values()
            next_row = len(existing_data) + 1
            print(f"Next row to write: {next_row}")
        except:
            next_row = 1
            print("Starting from row 1")

        # ヘッダーが存在しない場合は追加
        if next_row == 1:
            print("Adding headers...")
            headers = ['source', 'title', 'link']
            worksheet.update('A1:C1', [headers])
            next_row = 2

        # 必要な列のみを選択してデータを準備
        selected_columns = ['source', 'title', 'link']
        df_selected = df[selected_columns]
        
        # データを追加書き込み
        values = df_selected.values.tolist()
        print(f"Writing {len(values)} rows to sheet starting from row {next_row}...")
        
        # データを書き込み
        if values:
            # 行の範囲を計算（3列: A, B, C）
            end_row = next_row + len(values) - 1
            range_name = f'A{next_row}:C{end_row}'
            
            worksheet.update(range_name, values)
            print(f"Data written successfully to range {range_name}!")
        else:
            print("No data to write")
        
    except KeyError as e:
        print(f"Configuration error: Missing key {e}")
        print("Please check your config.json file")
        raise
    except Exception as e:
        print(f"Error in write_to_sheet: {e}")
        print(f"Error type: {type(e).__name__}")
        raise