# main.py

# Import functions from our client files
from twitter_client import post_tweet
from gemini_client import generate_post_from_prompt
from reddit_client import post_reddit


# --- THIS IS THE ONLY PLACE YOU NEED TO EDIT ---
#
# Create a detailed prompt for the AI.
# Be specific! Tell it the topic, tone, and format you want.

#
my_prompt =""" 

The tweet should be about the importance of embracing change and constantly learning new skills (both technical and soft skills).
Mention that this proactive approach is key to not getting left behind in the fast-paced tech industry.

The tone should be positive and motivational.

Include these relevant hashtags such as: #SoftwareDeveloper #AI #Upskilling #FutureOfWork #Tech
Tag these companies such as: @Google @Meta @OpenAI @Microsoft
"""
# ---------------------------------------------
print("🔵 Prompt for AI:", my_prompt)

if __name__ == "__main__":
    # 1. Generate the tweet content using Gemini AI
    generated_text = generate_post_from_prompt(my_prompt)

    # 2. Check if the text was generated successfully
    if generated_text:
        print("---")
        print("🤖 AI Generated Tweet:")
        print(generated_text)
        print("---")
        # 3. Post the generated tweet to X
        post_tweet(generated_text)
        post_reddit(generated_text)
        print("✅ Tweet and Reddit posted successfully!")
    else:
        print("🔴 Failed to generate tweet content. Aborting post.")