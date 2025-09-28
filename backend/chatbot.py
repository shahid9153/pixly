import os
import google.generativeai as genai
from dotenv import load_dotenv
from .screenshot import get_recent_screenshots, get_screenshot_by_id, get_screenshot_stats
import base64
import json
system_prompt_file = open("PROMPTS.txt","r")
system_prompt = system_prompt_file.read()
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'),)
model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite",system_instruction=system_prompt)

async def chat_with_gemini(message: str):
    try:
        # Check if user is asking about screenshots
        screenshot_keywords = ['screenshot', 'screen', 'capture', 'git', 'visual', 'see', 'show me']
        if any(keyword in message.lower() for keyword in screenshot_keywords):
            # Get recent screenshots
            recent_screenshots = get_recent_screenshots(limit=5)
            screenshot_stats = get_screenshot_stats()
            
            # Prepare screenshot context
            screenshot_context = f"""
            SCREENSHOT DATA AVAILABLE:
            - Total screenshots stored: {screenshot_stats['total_screenshots']}
            - Recent applications captured: {[app[0] for app in screenshot_stats['applications'][:5]]}
            - Recent screenshots: {recent_screenshots}
            
            You can analyze these screenshots to help with gaming-related questions. 
            The screenshots are automatically captured and show what applications the user was using.
            """
            
            # Add screenshot context to the message
            enhanced_message = f"{message}\n\n{screenshot_context}"
            response = model.generate_content(enhanced_message)
            return {"response": response.text}
        else:
            response = model.generate_content(message)
            return {"response": response.text}
    except Exception as e:
        print(e)
        return {"response": f"Error processing request: {str(e)}"}