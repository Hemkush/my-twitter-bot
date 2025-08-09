
"""
Scheduler for the AI-powered Twitter/Reddit bot.
This module handles automatic scheduling of posts using APScheduler.
"""

import logging
import sys
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import signal

# Import our bot functions
from twitter_client import post_tweet
from gemini_client import generate_post_from_prompt
from reddit_client import post_reddit
from app import App

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BotScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.prompts = [
            """
            The tweet should be about the importance of embracing change and constantly learning new skills (both technical and soft skills).
            Mention that this proactive approach is key to not getting left behind in the fast-paced tech industry.
            
            The tone should be positive and motivational.
            
            Include these relevant hashtags such as: #SoftwareDeveloper #AI #Upskilling #FutureOfWork #Tech
            Tag these companies such as: @Google @Meta @OpenAI @Microsoft
            """,
            """
            Write about the latest trends in AI and machine learning. 
            Focus on practical applications and how developers can leverage these technologies.
            
            The tone should be informative and engaging.
            
            Include hashtags: #AI #MachineLearning #DevCommunity #TechTrends #Innovation
            Tag: @OpenAI @huggingface @nvidia @DeepMind
            """,
            """
            Discuss the importance of clean code and best practices in software development.
            Mention how good coding practices lead to maintainable and scalable applications.
            
            The tone should be educational and professional.
            
            Include hashtags: #CleanCode #SoftwareDevelopment #BestPractices #CodeQuality #Programming
            Tag: @github @stackoverflow @jetbrains
            """
        ]
        self.current_prompt_index = 0

    def run_bot_task(self):
        """Execute the main bot functionality"""
        try:
            logger.info("Starting scheduled bot task...")
            App().mainloop()
            # Get the current prompt and rotate to next one
            current_prompt = self.prompts[self.current_prompt_index]
            self.current_prompt_index = (self.current_prompt_index + 1) % len(self.prompts)
            
            logger.info(f"Using prompt: {current_prompt[:100]}...")
            
            # Generate content using AI
            generated_text = generate_post_from_prompt(current_prompt)
            
            if generated_text:
                logger.info(f"Generated content: {generated_text}")
                
                # Post to both platforms
                # success_twitter = post_tweet(generated_text)
                # success_reddit = post_reddit(generated_text)
                
                # if success_twitter and success_reddit:
                #     logger.info("✅ Successfully posted to both Twitter and Reddit")
                # elif success_twitter:
                #     logger.warning("⚠️ Posted to Twitter but failed on Reddit")
                # elif success_reddit:
                #     logger.warning("⚠️ Posted to Reddit but failed on Twitter")
                # else:
                #     logger.error("❌ Failed to post to both platforms")
                    
            else:
                logger.error("❌ Failed to generate content with AI")
                
        except Exception as e:
            logger.error(f"❌ Error in scheduled task: {str(e)}")

    def add_daily_schedule(self, hour=10, minute=0):
        """Add a daily scheduled task"""
        self.scheduler.add_job(
            func=self.run_bot_task,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_post',
            name='Daily Twitter/Reddit Post',
            replace_existing=True
        )
        logger.info(f"Added daily schedule at {hour:02d}:{minute:02d}")
    
    def add_interval_schedule(self, minutes=6):
        """Add an interval-based scheduled task"""
        self.scheduler.add_job(
            func=self.run_bot_task,
            trigger=IntervalTrigger(minutes=minutes),
            id='interval_post',
            name=f'Post every {minutes} minutes',
            replace_existing=True
        )
        logger.info(f"Added interval schedule every {minutes} minutes")
    
    def add_weekly_schedule(self, day_of_week='mon,wed,fri', hour=14, minute=30):
        """Add a weekly scheduled task"""
        self.scheduler.add_job(
            func=self.run_bot_task,
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
            id='weekly_post',
            name=f'Weekly posts on {day_of_week}',
            replace_existing=True
        )
        logger.info(f"Added weekly schedule on {day_of_week} at {hour:02d}:{minute:02d}")

    def list_jobs(self):
        """List all scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            logger.info("📋 Scheduled jobs:")
            for job in jobs:
                # For jobs that haven't started yet, next_run_time might not be available
                next_run = getattr(job, 'next_run_time', 'Not started')
                logger.info(f"  - {job.name} (ID: {job.id}) - Next run: {next_run}")
        else:
            logger.info("No scheduled jobs found")
    
    def start(self):
        """Start the scheduler"""
        try:
            logger.info("🚀 Starting scheduler...")
            self.list_jobs()
            
            # Register shutdown handlers
            atexit.register(lambda: self.scheduler.shutdown())
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            self.scheduler.start()
            
        except KeyboardInterrupt:
            logger.info("Scheduler interrupted by user")
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.scheduler.shutdown()
        sys.exit(0)

def main():
    """Main function to set up and start the scheduler"""
    bot_scheduler = BotScheduler()
    
    # Add different scheduling options (you can customize these)
    
    # Option 1: Post daily at 10:00 AM
    # bot_scheduler.add_daily_schedule(hour=3, minute=0)
    
    # Option 2: Post every 6 hours (comment out if you don't want this)
    bot_scheduler.add_interval_schedule(minutes=60)
    
    # Option 3: Post on specific days (comment out if you don't want this)
    # bot_scheduler.add_weekly_schedule(day_of_week='mon,wed,fri', hour=14, minute=30)
    
    # Start the scheduler
    bot_scheduler.start()

if __name__ == "__main__":
    main()