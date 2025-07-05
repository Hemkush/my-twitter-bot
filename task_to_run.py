# task_to_run.py
from datetime import datetime

# The path to the log file (use an absolute path)
log_file = "C:/Users/kushw/Downloads/Coding Practice/my-twitter-bot/task_log.log"

with open(log_file, "a") as f:
    f.write(f"Task executed at: {datetime.now()}\n")