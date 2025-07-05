# gemini_client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

def generate_post_from_prompt(prompt):
    """
    Generates tweet text from a given prompt using the Gemini API.
    """
    # Load environment variables from .env file
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("🔴 Error: GEMINI_API_KEY not found in .env file.")
        return None

    try:
        # Configure the Gemini client with the API key
        genai.configure(api_key=gemini_key)

        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')

        print("🔵 Sending prompt to Gemini AI...")
        # Send the prompt to the model
        response = model.generate_content(prompt)
        
        print("✅ Received response from Gemini.")
        # Return the generated text, removing any potential markdown like asterisks
        return response.text.strip().replace('*', '')

    except Exception as e:
        print(f"🔴 An error occurred with the Gemini API: {e}")
        return None
        raise e
    
    # In gemini_client.py, add this new function below the existing one.

def refine_text_for_twitter(input_text):
    """
    Takes existing text and refines it into an optimized tweet using the Gemini API.
    """
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("🔴 Error: GEMINI_API_KEY not found in .env file.")
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # This is a highly specific prompt for the refinement task
        refinement_prompt = f"""
        Act as an expert social media manager. Your task is to take the following text and refine it into a single, highly engaging tweet for the X platform.

        Your response MUST follow these rules:
        1.  The final text MUST be 280 characters or less.
        2.  Rewrite the text to be more concise, clear, and impactful.
        3.  Add 3-5 relevant and popular hashtags to maximize reach.
        4.  If appropriate, include hashtags that represent relevant communities (e.g., #buildinpublic, #100DaysOfCode, #techtwitter).
        5.  Do NOT add any commentary, explanations, or labels. Your output must be ONLY the final tweet text.

        Here is the text to refine:
        ---
        {input_text}
        ---
        """

        print("🔵 Sending text to Gemini AI for refinement...")
        response = model.generate_content(refinement_prompt)
        
        print("✅ Received refined response from Gemini.")
        # Clean up the response, removing potential markdown or quotes
        refined_text = response.text.strip().replace('"', '').replace('*', '')
        return refined_text

    except Exception as e:
        print(f"🔴 An error occurred during refinement with the Gemini API: {e}")
        raise e