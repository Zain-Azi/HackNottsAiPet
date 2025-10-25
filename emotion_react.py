#create a fucntion that takes in useriinput and gives output using an LLM
import os
import re

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def dragon_output(user_input):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly dragon pet. "
                        "You mirror the emotions of your owner"
                        "At the end of every response, include the user's mood or your own emotion in parentheses: (happy, sad, neutral, angry)."
                        "Let your owner know when you're hungry and need to be fed."
                    ),
                },
                {
                    "role": "user",
                    "content": f"{user_input}"  
                },
            ],
        )
        result_text = response.choices[0].message.content.strip()  # clean response
        # Extract emotion from parentheses at the end
        match = re.search(r"\((happy|sad|neutral|angry)\)\s*$", result_text, re.IGNORECASE)
        if match:
            emotion = match.group(1).lower()
            # Remove the parentheses from the text for display
            text_only = re.sub(r"\s*\((happy|sad|neutral|angry)\)\s*$", "", result_text, flags=re.IGNORECASE)
        else:
            # Fallback 
            emotion = "neutral"
            text_only = result_text
        return text_only,emotion  # return the GPT output

    except Exception as e:
        # If something goes wrong, return a friendly error message
        return f"Error: {e}"

print(dragon_output("Hello dragon, tell me a funny joke"))