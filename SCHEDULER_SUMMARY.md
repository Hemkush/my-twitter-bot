# AI Twitter/Reddit Bot Scheduler Implementation

## Overview

This project now includes a comprehensive automated scheduling system that allows the AI-powered Twitter/Reddit bot to run automatically without manual intervention.

## What Was Implemented

### 1. 🚀 APScheduler-based Scheduler (`scheduler.py`)
- **Recommended option** for most users
- Runs as a Python process with built-in logging
- Supports multiple scheduling patterns:
  - Daily at specific times
  - Interval-based (every X hours)
  - Weekly schedules (specific days of week)
- Features:
  - Multiple prompt rotation for varied content
  - Comprehensive logging to `scheduler.log`
  - Graceful shutdown handling
  - Easy monitoring and management

### 2. ⏰ System Cron Integration (`schedule_manager.py`)
- Alternative option using system cron jobs
- Works independently of Python processes
- Linux/macOS compatible with proper paths
- Features:
  - Automatic cron job creation/removal
  - Multiple schedule options
  - System-level reliability
  - Command-line management tools

### 3. 📝 Enhanced Task Runner (`task_to_run.py`)
- Improved version of the original task runner
- Integrates with main bot functionality
- Features:
  - Comprehensive logging to `task_execution.log`
  - Error handling and reporting
  - Can be used standalone or with cron

### 4. 🔧 Interactive Setup Wizard (`setup_scheduler.py`)
- User-friendly configuration interface
- Guides users through scheduling options
- Automatically detects and installs dependencies
- Provides customization options for different use cases

### 5. 🧪 Testing Framework (`test_scheduler.py`)
- Validates all scheduler components
- Tests imports, functionality, and integration
- Provides clear success/failure feedback
- Helps diagnose setup issues

## Key Features Added

### Multiple Prompt Rotation
The scheduler now includes multiple predefined prompts that rotate automatically:
1. Learning and upskilling in tech
2. AI and machine learning trends
3. Clean code and best practices

### Comprehensive Logging
- **APScheduler**: Logs to `scheduler.log`
- **Task Runner**: Logs to `task_execution.log`
- **Console Output**: Real-time status updates

### Robust Error Handling
- API authentication errors
- Network connectivity issues
- Platform-specific failures (Twitter vs Reddit)
- Graceful degradation

### Flexible Configuration
- Environment variable support for API keys
- Customizable schedules via code or command line
- Multiple deployment options

## Files Created/Modified

### New Files
- `scheduler.py` - Main APScheduler implementation
- `setup_scheduler.py` - Interactive setup wizard
- `test_scheduler.py` - Testing framework
- `SCHEDULER_SUMMARY.md` - This documentation

### Modified Files
- `schedule_manager.py` - Updated for Linux compatibility
- `task_to_run.py` - Enhanced with logging and integration
- `requirements.txt` - Added scheduler dependencies
- `README.md` - Updated with scheduler documentation

### Dependencies Added
- `APScheduler` - Advanced Python scheduler
- `python-crontab` - Cron job management
- `feedparser` - RSS feed parsing
- `praw` - Reddit API integration

## Usage Examples

### Option 1: APScheduler (Recommended)
```bash
# Start with default daily schedule at 10:00 AM
python scheduler.py

# Or use the setup wizard
python setup_scheduler.py
```

### Option 2: System Cron
```bash
# Set up cron jobs
python schedule_manager.py

# List existing jobs
python schedule_manager.py --list

# Remove all bot jobs
python schedule_manager.py --remove
```

### Option 3: Manual Execution
```bash
# Run once with main prompt
python main.py

# Run once with logging
python task_to_run.py
```

## Testing
```bash
# Verify everything works
python test_scheduler.py
```

## Configuration Requirements

### Environment Variables (.env file)
```
API_KEY=your_twitter_api_key
API_KEY_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
GEMINI_API_KEY=your_gemini_api_key
```

### System Requirements
- Python 3.x with virtual environment support
- Linux/macOS for cron functionality
- Internet connectivity for API calls

## Next Steps for Users

1. **Set up API credentials** in a `.env` file
2. **Choose scheduling method** based on preferences:
   - APScheduler for ease of use
   - Cron for system-level reliability
   - Manual for testing/development
3. **Test the setup** using `python test_scheduler.py`
4. **Start the scheduler** and monitor logs
5. **Customize prompts** in `scheduler.py` as needed

## Troubleshooting

### Common Issues
1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **API authentication**: Verify `.env` file configuration
3. **Cron not working**: Check if cron service is running
4. **Permission errors**: Ensure proper file permissions

### Log Files
- Check `scheduler.log` for APScheduler issues
- Check `task_execution.log` for execution problems
- Use `python test_scheduler.py` for diagnostics

## Benefits Achieved

✅ **Automated posting** - No manual intervention required
✅ **Multiple scheduling options** - Flexibility for different use cases
✅ **Robust error handling** - Continues working despite issues
✅ **Comprehensive logging** - Easy monitoring and debugging
✅ **Easy setup** - Interactive wizard and testing tools
✅ **Linux compatibility** - Fixed Windows-specific paths
✅ **Professional deployment** - Production-ready scheduler
✅ **Content variety** - Multiple prompt rotation
✅ **Platform independence** - Works with both Twitter and Reddit

The scheduler implementation transforms this from a manual bot into a fully automated social media posting system that can run reliably in production environments.