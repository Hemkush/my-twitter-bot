#!/usr/bin/env python3
"""
Setup script for configuring the Twitter/Reddit bot scheduler.
This script helps users choose between different scheduling options.
"""

import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print a welcome banner"""
    print("=" * 60)
    print("🤖 AI Twitter/Reddit Bot Scheduler Setup")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import apscheduler
        print("✅ APScheduler is installed")
        apscheduler_available = True
    except ImportError:
        print("❌ APScheduler is not installed")
        apscheduler_available = False
    
    try:
        import crontab
        print("✅ python-crontab is installed")
        crontab_available = True
    except ImportError:
        print("❌ python-crontab is not installed")
        crontab_available = False
    
    if not (apscheduler_available or crontab_available):
        print("\n❌ No scheduling libraries are installed!")
        print("💡 Please install dependencies: pip install -r requirements.txt")
        return False
    
    print()
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def show_scheduling_options():
    """Display available scheduling options"""
    print("📅 Available Scheduling Options:")
    print()
    print("1. 🚀 APScheduler (Recommended)")
    print("   - Runs as a Python process")
    print("   - Easy to manage and monitor")
    print("   - Built-in logging")
    print("   - Multiple prompt rotation")
    print()
    print("2. ⏰ System Cron")
    print("   - Uses system cron jobs")
    print("   - Runs independently of Python process")
    print("   - System-level scheduling")
    print("   - Requires cron service")
    print()
    print("3. 📝 Manual Task Runner")
    print("   - Run tasks manually when needed")
    print("   - Good for testing and development")
    print("   - No automatic scheduling")
    print()

def setup_apscheduler():
    """Set up APScheduler"""
    print("🚀 Setting up APScheduler...")
    print()
    print("Available schedule types:")
    print("1. Daily (runs once per day)")
    print("2. Interval (runs every X hours)")
    print("3. Weekly (runs on specific days)")
    print("4. Custom configuration")
    print()
    
    choice = input("Choose schedule type (1-4): ").strip()
    
    if choice == "1":
        hour = input("Enter hour (0-23, default 10): ").strip() or "10"
        minute = input("Enter minute (0-59, default 0): ").strip() or "0"
        print(f"\n✅ Configuration: Daily at {hour}:{minute}")
        
    elif choice == "2":
        hours = input("Enter interval in hours (default 6): ").strip() or "6"
        print(f"\n✅ Configuration: Every {hours} hours")
        
    elif choice == "3":
        days = input("Enter days (e.g., 'mon,wed,fri', default 'mon,wed,fri'): ").strip() or "mon,wed,fri"
        hour = input("Enter hour (0-23, default 14): ").strip() or "14"
        minute = input("Enter minute (0-59, default 30): ").strip() or "30"
        print(f"\n✅ Configuration: {days} at {hour}:{minute}")
        
    else:
        print("\n✅ Custom configuration - edit scheduler.py manually")
    
    print("\n🔧 To start the scheduler, run:")
    print("   python scheduler.py")
    print("\n📋 The scheduler will run continuously and log to scheduler.log")

def setup_cron():
    """Set up system cron"""
    print("⏰ Setting up system cron...")
    print()
    print("This will create cron jobs that run automatically.")
    print("Default: Daily at 10:00 AM")
    print()
    
    confirm = input("Proceed with cron setup? (y/N): ").strip().lower()
    
    if confirm == 'y':
        try:
            subprocess.run([sys.executable, "schedule_manager.py"], check=True)
            print("\n🔧 To manage cron jobs:")
            print("   python schedule_manager.py --list   # List jobs")
            print("   python schedule_manager.py --remove # Remove jobs")
            print("   crontab -l                          # View all cron jobs")
        except subprocess.CalledProcessError:
            print("❌ Failed to set up cron jobs")
    else:
        print("❌ Cron setup cancelled")

def setup_manual():
    """Set up manual task runner"""
    print("📝 Manual task runner setup...")
    print()
    print("No automatic scheduling will be configured.")
    print("You can run tasks manually using:")
    print()
    print("🔧 Available commands:")
    print("   python main.py        # Run once with main prompt")
    print("   python task_to_run.py # Run once with logging")
    print("   python scheduler.py   # Start APScheduler")

def main():
    """Main setup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        install_deps = input("Install dependencies now? (y/N): ").strip().lower()
        if install_deps == 'y':
            if not install_dependencies():
                return
        else:
            print("❌ Cannot proceed without dependencies")
            return
    
    # Show options
    show_scheduling_options()
    
    choice = input("Choose scheduling method (1-3): ").strip()
    print()
    
    if choice == "1":
        setup_apscheduler()
    elif choice == "2":
        setup_cron()
    elif choice == "3":
        setup_manual()
    else:
        print("❌ Invalid choice")
        return
    
    print()
    print("=" * 60)
    print("🎉 Setup complete!")
    print("=" * 60)
    print()
    print("💡 Next steps:")
    print("1. Make sure your .env file is configured with API keys")
    print("2. Test the bot manually: python main.py")
    print("3. Start your chosen scheduler")
    print()
    print("📚 Check the logs for execution details:")
    print("   - scheduler.log (APScheduler)")
    print("   - task_execution.log (Manual/Cron)")

if __name__ == "__main__":
    main()