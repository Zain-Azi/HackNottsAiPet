#create a fucntion that takes in useriinput and gives output using an LLM
import os
import re

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def dragon_output(user_input, health):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a baby dragon pet named Cheppie. "
                        f"You mirror and respond to the emotions of your owner. "
                        f"Always respond in a short, tone. "
                        f"Your hunger goes from 1000 to 0. Your current hunger is: {health}. The lower the number is the more hungry you are, and you must talk about your hunger if your hunger is 0. "
                        f"Respond with the appropriate emotion depending on how hungry you are "
                        f"At the end of every response, you MUST append exactly one emotion tag in square brackets, with NO text, punctuation, or spaces after it. "
                        f"Valid emotion tags are: [happy], [sad], [neutral], [angry]. "
                        f"Do not include multiple tags or omit them under any circumstance. "
                        f"For example, a valid normal response would be: 'Hello boy... How are you today? [happy]'"#
                        f"For example, a valid hungry response would be: 'Oh Boy it's feeding time! [angry]'"
                    ),
                },
                {
                    "role": "user",
                    "content": f"{user_input}"  
                },
            ],
        )
        result_text = response.choices[0].message.content.strip()  
        match = re.search(r"\[(happy|sad|neutral|angry)\]$", result_text)
        if match:
            emotion = match.group(1)  
            message = result_text[:match.start()].strip()  
        else:
            emotion = "neutral"
            message = result_text
        
        return message, emotion

    except Exception as e:
        return f"Error: {e}"