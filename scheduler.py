from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import main


def job():
    try:
        main.main()
    except Exception as e:
        print(f"Job failed at {datetime.now()}: {e}")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', hour='8,20', minute=0)
    scheduler.start()