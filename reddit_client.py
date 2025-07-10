# file: reddit_auto_post_bot.py
import os
import praw
from dotenv import load_dotenv


load_dotenv()
# Replace with your Reddit app credentials
id=os.getenv("YOUR_CLIENT_ID")
secret=os.getenv("YOUR_CLIENT_SECRET")
user_name=os.getenv("YOUR_REDDIT_USERNAME")
password_=os.getenv("YOUR_REDDIT_PASSWORD")
userAgent="python:reddit.auto.poster:v1.0 (by u/Different-Sugar-8262)"  # e.g., 'python:reddit.auto.poster:v1.0 (by u/yourusername)'


def create_reddit_instance():
    return praw.Reddit(
        client_id=id,
        client_secret=secret,
        username=user_name,
        password=password_,
        user_agent=userAgent
    )


def submit_text_post(reddit, subreddit_name, title, body):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.submit(title=title, selftext=body)


# def submit_link_post(reddit, subreddit_name, title, url):
#     subreddit = reddit.subreddit(subreddit_name)
#     return subreddit.submit(title=title, url=url)


def post_reddit(text_to_post):
    reddit = create_reddit_instance()

    subreddit_name = "test"  # Change this to your desired subreddit
    post_type = "Technology"  # or 'link', you can change this as needed
    title = text_to_post
    body = "text_to_post"    

    if post_type == 'Technology':
        # body = input("Post body text: ").strip()
        post = submit_text_post(reddit, subreddit_name, title, body)
        print(reddit, subreddit_name, title, body)
    
    else:
        print("Invalid post type.")
        exit()

    print(f"Post submitted: {post.shortlink}")
    print(reddit, subreddit_name, title, body)

   