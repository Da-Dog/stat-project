from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from data import get_data, print_availability_report, log_data


def job():
    try:
        print("Job started at", datetime.now())
        spaces_names, slot_counter = get_data()
        print("Logging data...")
        log_data(spaces_names, slot_counter)
        print("Job finished at", datetime.now())
        print("==================================")
    except Exception as e:
        print(f"Job failed at {datetime.now()}: {e}")


def alive_check():
    print(f"Running... Time is: {datetime.now().isoformat()}")


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour='*', minute=0)

    print("Scheduler starting. Press Ctrl+C to exit.")

    scheduler.start()