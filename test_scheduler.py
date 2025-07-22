#!/usr/bin/env python3
"""
Test script to verify the scheduler functionality works correctly.
This can be used to test the implementation without running the full bot.
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path to import our modules
sys.path.insert(0, '/workspace')

def test_scheduler_imports():
    """Test that all scheduler modules can be imported successfully"""
    print("🔍 Testing scheduler imports...")
    
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        print("✅ APScheduler imported successfully")
    except ImportError as e:
        print(f"❌ APScheduler import failed: {e}")
        return False
    
    try:
        from crontab import CronTab
        print("✅ python-crontab imported successfully")
    except ImportError as e:
        print(f"❌ python-crontab import failed: {e}")
        return False
    
    try:
        import scheduler
        print("✅ Custom scheduler module imported successfully")
    except ImportError as e:
        print(f"❌ Custom scheduler import failed: {e}")
        return False
    
    try:
        import schedule_manager
        print("✅ Schedule manager module imported successfully")
    except ImportError as e:
        print(f"❌ Schedule manager import failed: {e}")
        return False
    
    return True

def test_scheduler_creation():
    """Test creating a basic scheduler instance"""
    print("\n🔧 Testing scheduler creation...")
    
    try:
        from scheduler import BotScheduler
        
        # Create a scheduler instance
        bot_scheduler = BotScheduler()
        print("✅ BotScheduler instance created successfully")
        
        # Test adding a job (but don't start it)
        bot_scheduler.add_daily_schedule(hour=10, minute=0)
        print("✅ Daily schedule added successfully")
        
        # Test listing jobs
        bot_scheduler.list_jobs()
        print("✅ Job listing works")
        
        return True
        
    except Exception as e:
        print(f"❌ Scheduler creation failed: {e}")
        return False

def test_task_runner():
    """Test the simple task runner"""
    print("\n📝 Testing task runner...")
    
    try:
        import task_to_run
        print("✅ Task runner module imported successfully")
        
        # Test the logging function
        task_to_run.log_execution("Test log message from scheduler test")
        print("✅ Logging function works")
        
        return True
        
    except Exception as e:
        print(f"❌ Task runner test failed: {e}")
        return False

def main():
    """Run all scheduler tests"""
    print("=" * 60)
    print("🤖 Testing AI Twitter/Reddit Bot Scheduler")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Imports
    if test_scheduler_imports():
        tests_passed += 1
    
    # Test 2: Scheduler creation
    if test_scheduler_creation():
        tests_passed += 1
    
    # Test 3: Task runner
    if test_task_runner():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Scheduler is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set up your .env file with API credentials")
        print("2. Choose your scheduling method:")
        print("   - python scheduler.py (APScheduler)")
        print("   - python schedule_manager.py (Cron)")
        print("   - python task_to_run.py (Manual)")
        print("3. Monitor logs for execution status")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)