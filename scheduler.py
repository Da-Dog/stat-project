from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from data import get_data, print_availability_report, log_data


def job():
    try:
        spaces_names, slot_counter = get_data()
        print_availability_report(spaces_names, slot_counter)
        log_data(spaces_names, slot_counter)
    except Exception as e:
        print(f"Job failed at {datetime.now()}: {e}")


def alive_check():
    print(f"Running... Time is: {datetime.now().isoformat()}")


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour='8,20', minute=0)
    scheduler.add_job(alive_check, 'interval', minutes=30)  # Run every hour

    print("Scheduler starting. Press Ctrl+C to exit.")

    scheduler.start()