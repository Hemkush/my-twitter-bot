import schedule
import time
from app import App

def start():
    schedule.every(1).minutes.do(App().mainloop)
    print("Scheduler started. Running every 1 minute.")
    while True:
        schedule.run_pending()
        time.sleep(60)
        print("Scheduler ticked. Waiting for next run...")

if __name__ == "__main__":
    start()