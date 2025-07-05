import os
import tweepy
from dotenv import load_dotenv

def post_tweet(text_to_post):
    """
    Authenticates with the X API using credentials from .env
    and posts a tweet.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get credentials from environment variables
    api_key = os.getenv("API_KEY")
    api_key_secret = os.getenv("API_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Check if all keys are present
    if not all([api_key, api_key_secret, access_token, access_token_secret]):
        print("🔴 Error: Missing one or more API credentials in the .env file.")
        return

    try:
        # Authenticate using the X API v2 client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        # Create the tweet
        print("🔵 Attempting to post tweet...")
        response = client.create_tweet(text=text_to_post)
        
        tweet_id = response.data['id']
        tweet_text = response.data['text']
        
        print("✅ Tweet posted successfully!")
        print(f"   ID: {tweet_id}")
        print(f"   Text: \"{tweet_text[:60]}...\"")
        print(f"   View it here: https://twitter.com/user/status/{tweet_id}")

    except tweepy.errors.TweepyException as e:
        print(f"🔴 Error posting tweet: {e}")
        raise e
    except Exception as e:
        print(f"🔴 An unexpected error occurred: {e}")
        raise e