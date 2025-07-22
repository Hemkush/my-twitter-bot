#!/usr/bin/env python3
"""
Simple task runner that executes the main bot functionality and logs the execution.
This can be used as a standalone script or called by cron jobs.
"""

from datetime import datetime
import os
from pathlib import Path

# Import the main bot functionality
from twitter_client import post_tweet
from gemini_client import generate_post_from_prompt
from reddit_client import post_reddit

def log_execution(message, log_file_path="/workspace/task_execution.log"):
    """Log a message with timestamp to the log file"""
    try:
        with open(log_file_path, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
    except Exception as e:
        print(f"Failed to write to log: {e}")

def run_bot_task():
    """Execute the main bot task with logging"""
    log_execution("🚀 Starting scheduled bot task execution")
    
    try:
        # Define the prompt (you can modify this or make it dynamic)
        prompt = """
        The tweet should be about the importance of embracing change and constantly learning new skills (both technical and soft skills).
        Mention that this proactive approach is key to not getting left behind in the fast-paced tech industry.
        
        The tone should be positive and motivational.
        
        Include these relevant hashtags such as: #SoftwareDeveloper #AI #Upskilling #FutureOfWork #Tech
        Tag these companies such as: @Google @Meta @OpenAI @Microsoft
        """
        
        log_execution(f"📝 Using prompt: {prompt[:100]}...")
        
        # Generate content using AI
        generated_text = generate_post_from_prompt(prompt)
        
        if generated_text:
            log_execution(f"🤖 Generated content: {generated_text}")
            
            # Post to platforms
            twitter_success = post_tweet(generated_text)
            reddit_success = post_reddit(generated_text)
            
            if twitter_success and reddit_success:
                log_execution("✅ Successfully posted to both Twitter and Reddit")
            elif twitter_success:
                log_execution("⚠️ Posted to Twitter but failed on Reddit")
            elif reddit_success:
                log_execution("⚠️ Posted to Reddit but failed on Twitter")
            else:
                log_execution("❌ Failed to post to both platforms")
                
        else:
            log_execution("❌ Failed to generate content with AI")
            
    except Exception as e:
        log_execution(f"❌ Error during task execution: {str(e)}")
        raise

if __name__ == "__main__":
    print(f"Task executed at: {datetime.now()}")
    run_bot_task()
    print("Task completed. Check /workspace/task_execution.log for details.")