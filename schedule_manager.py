# schedule_manager.py
"""
Alternative cron-based scheduler using python-crontab.
This is an alternative to scheduler.py for users who prefer system cron.
"""

import os
import sys
from crontab import CronTab

from pathlib import Path

def setup_cron_scheduler():
    """
    Sets up cron jobs for the Twitter/Reddit bot using system cron.
    This is an alternative to the APScheduler-based scheduler.py
    """
    
    # Get the current working directory (workspace)
    workspace_path = Path("/workspace")
    
    # Get Python interpreter path
    python_path = sys.executable
    
    # Define paths
    main_script_path = workspace_path / "main.py"
    scheduler_script_path = workspace_path / "scheduler.py"
    
    print(f"🔧 Setting up cron jobs...")
    print(f"Python path: {python_path}")
    print(f"Workspace: {workspace_path}")
    print(f"Main script: {main_script_path}")
    
    # Initialize a CronTab object for the current user
    try:
        cron = CronTab(user=True)
    except Exception as e:
        print(f"❌ Error accessing crontab: {e}")
        print("💡 Make sure cron is installed: sudo apt-get install cron")
        return False
    
    # Remove any existing jobs with our comment to avoid duplicates
    cron.remove_all(comment='ai_twitter_bot')
    # Option 1: Run main.py daily at 10:00 AM
    daily_command = f"{python_path} {main_script_path}"
    daily_job = cron.new(command=daily_command, comment='ai_twitter_bot_daily')
    daily_job.setall('0 10 * * *')  # Every day at 10:00 AM
    
    # Option 2: Run main.py every 6 hours (uncomment if desired)
    # interval_command = f"{python_path} {main_script_path}"
    # interval_job = cron.new(command=interval_command, comment='ai_twitter_bot_interval')
    # interval_job.setall('0 */6 * * *')  # Every 6 hours
    
    # Option 3: Run on specific days (Mon, Wed, Fri at 2:30 PM)
    # weekly_command = f"{python_path} {main_script_path}"
    # weekly_job = cron.new(command=weekly_command, comment='ai_twitter_bot_weekly')
    # weekly_job.setall('30 14 * * 1,3,5')  # Mon, Wed, Fri at 2:30 PM
    
    try:
        # Write the jobs to the system's crontab
        cron.write()
        
        print("✅ Cron jobs created successfully!")
        print("\n📋 Scheduled jobs:")
        
        # List all our jobs
        for job in cron.find_comment('ai_twitter_bot'):
            print(f"  - {job.comment}: {job} (Next run: {job.schedule})")
            
        print(f"\n💡 To view all cron jobs, run: crontab -l")
        print(f"💡 To edit cron jobs manually, run: crontab -e")
        print(f"💡 To remove all bot jobs, run this script with --remove")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing to crontab: {e}")
        return False

def remove_cron_jobs():
    """Remove all cron jobs related to the AI Twitter bot"""
    try:
        cron = CronTab(user=True)
        removed_count = len(list(cron.find_comment('ai_twitter_bot')))
        cron.remove_all(comment='ai_twitter_bot')
        cron.write()
        
        print(f"✅ Removed {removed_count} cron job(s)")
        return True
        
    except Exception as e:
        print(f"❌ Error removing cron jobs: {e}")
        return False

def list_cron_jobs():
    """List all cron jobs related to the AI Twitter bot"""
    try:
        cron = CronTab(user=True)
        jobs = list(cron.find_comment('ai_twitter_bot'))
        
        if jobs:
            print("📋 Current AI Twitter Bot cron jobs:")
            for job in jobs:
                print(f"  - {job.comment}: {job}")
        else:
            print("ℹ️ No AI Twitter Bot cron jobs found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error listing cron jobs: {e}")
        return False
def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--remove':
            remove_cron_jobs()
        elif sys.argv[1] == '--list':
            list_cron_jobs()
        else:
            print("Usage:")
            print("  python schedule_manager.py        # Set up cron jobs")
            print("  python schedule_manager.py --list # List existing jobs")
            print("  python schedule_manager.py --remove # Remove all bot jobs")
    else:
        setup_cron_scheduler()

if __name__ == "__main__":
    main()