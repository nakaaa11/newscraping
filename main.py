import json
from scraper import collect_all
from sheets import write_to_sheet
from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore

def load_config(path: str = 'config.json') -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def job():
    try:
        config = load_config()
        df = collect_all(config['feeds'])
        print('Job executed:', df.shape[0], 'articles collected.')
        print('Sample articles:')
        print(df.head())
        
        # Google Sheetsへの書き込み
        try:
            write_to_sheet(df, config)
            print('Successfully wrote to Google Sheets!')
        except Exception as e:
            print(f'Error writing to Google Sheets: {e}')
            print('Continuing without Google Sheets...')
            
    except Exception as e:
        print(f'Error in job: {e}')


if __name__ == '__main__':
    # 直接実行時は一度だけ実行
    job()
    # スケジューラ起動（毎日 09:00 実行例）
    # sched = BlockingScheduler()
    # sched.add_job(job, 'cron', hour=9, minute=0)
    # print('Scheduler started. Waiting for next run...')
    # sched.start()