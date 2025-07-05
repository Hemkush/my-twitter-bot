# schedule_manager.py
from crontab import CronTab

# --- IMPORTANT: DEFINE YOUR ABSOLUTE PATHS ---
# 1. Find your Python interpreter path by running `which python3` in your terminal
python_path = "C:/Python313/python.exe"  

# 2. Define the absolute path to the script you want to run
script_path = "C:/Users/kushw/Downloads/Coding Practice/my-twitter-bot/task_to_run.py" 

# Initialize a CronTab object for the current user
# user=True is a shortcut for the user running the script
cron = CronTab(user=True)

# Define the command that the cron job will execute
command = f"{python_path} {script_path}"

# Create a new cron job. The comment is a unique identifier.
job = cron.new(command=command, comment='my_awesome_task')

# Set the schedule. For this example, we'll run it every minute.
job.minute.every(1)

# Write the job to the system's crontab.
# This is the crucial step that saves your changes.
cron.write()

print(f"Cron job '{job.comment}' created successfully.")
print(f"It is scheduled to run: {job.schedule}")