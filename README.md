Overview
This is an AI-powered tweet co-pilot application that helps users generate and refine tweets and Reddit posts. The application is built using Python and includes automated scheduling capabilities to run posts automatically.

Features
- Select and fetch articles from TechCrunch
- Generate and refine tweets and Reddit posts using AI-powered text refinement
- Preview and edit tweets and Reddit posts before posting
- Post tweets and Reddit posts to respective platforms
- Display character count and limit for tweets and Reddit posts
- **🆕 Automated scheduling with multiple options (APScheduler, Cron, Manual)**
- **🆕 Multiple prompt rotation for varied content**
- **🆕 Comprehensive logging and monitoring**

Getting Started

Prerequisites

- Python 3.x installed on the system
- Required dependencies (see requirements.txt)

Installation

1. Clone the repository to a local directory
2. Install the required libraries by running `pip install -r requirements.txt`
3. Set up your API credentials in a `.env` file

## Scheduler Setup

This bot now includes three different scheduling options:

### Option 1: APScheduler (Recommended) 🚀

**Best for**: Most users who want easy setup and management

```bash
# Run the setup wizard
python setup_scheduler.py

# Or start directly with default settings (daily at 10:00 AM)
python scheduler.py
```

**Features:**
- Runs as a Python process
- Built-in logging to `scheduler.log`
- Multiple prompt rotation
- Easy to monitor and manage
- Supports daily, interval, and weekly schedules

### Option 2: System Cron ⏰

**Best for**: Users who prefer system-level scheduling

```bash
# Set up cron jobs (Linux/macOS)
python schedule_manager.py

# List existing jobs
python schedule_manager.py --list

# Remove all bot jobs
python schedule_manager.py --remove
```

**Features:**
- Uses system cron service
- Runs independently of Python process
- System-level reliability
- Requires cron service to be running

### Option 3: Manual Task Runner 📝

**Best for**: Testing and development

```bash
# Run once with main prompt
python main.py

# Run once with logging
python task_to_run.py
```

## Running the Application

### Manual Execution
Run the application by executing `python main.py`

### Automated Execution
1. Choose your preferred scheduling method using `python setup_scheduler.py`
2. Configure your schedule preferences
3. Start the scheduler
4. Monitor logs for execution status

## Configuration

### Environment Variables
Create a `.env` file with the following variables:
```
API_KEY=your_twitter_api_key
API_KEY_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
GEMINI_API_KEY=your_gemini_api_key
```

### Customizing Schedules

#### APScheduler Configuration
Edit `scheduler.py` to modify:
- Posting schedules (daily, interval, weekly)
- Prompt rotation
- Logging preferences

#### Cron Configuration
Edit `schedule_manager.py` to modify:
- Cron timing expressions
- Command execution paths

### Customizing Prompts
Modify the prompts in `scheduler.py` or `main.py` to change the content generation themes.

## Logging and Monitoring

The bot provides comprehensive logging:

- **`scheduler.log`**: APScheduler execution logs
- **`task_execution.log`**: Manual and cron execution logs
- **Console output**: Real-time status updates

## Troubleshooting

### Common Issues

1. **Dependencies not installed**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cron jobs not working**
   ```bash
   # Check if cron is running
   sudo systemctl status cron
   
   # View cron logs
   sudo tail -f /var/log/cron.log
   ```

3. **API authentication errors**
   - Verify your `.env` file is properly configured
   - Check API key permissions and limits

4. **Scheduler not starting**
   ```bash
   # Check for port conflicts or permission issues
   python setup_scheduler.py
   ```

## API Documentation

The application uses:
- **Google Generative AI library** for text generation
- **Tweepy** for Twitter API integration
- **PRAW** for Reddit API integration
- **APScheduler** for advanced scheduling

The main functions are:
- `generate_post_from_prompt()`: AI content generation
- `post_tweet()`: Twitter posting
- `post_reddit()`: Reddit posting

## File Structure

```
├── main.py              # Main application entry point
├── scheduler.py         # APScheduler implementation
├── schedule_manager.py  # Cron-based scheduler
├── task_to_run.py      # Simple task runner with logging
├── setup_scheduler.py  # Interactive setup wizard
├── twitter_client.py   # Twitter API integration
├── reddit_client.py    # Reddit API integration
├── gemini_client.py    # AI content generation
├── requirements.txt    # Python dependencies
└── .env               # API credentials (create this)
```

## Acknowledgments

- customtkinter library for providing a customizable and modern GUI framework
- Google Generative AI library for providing text refinement capabilities
- APScheduler for robust task scheduling
- python-crontab for cron integration
