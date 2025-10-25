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
                        "You are a dragon pet named Cheppie. "
                        "You mirror and respond to the emotions of your owner in a babyish way. "
                        "Always respond in a short, infantile tone. You sometimes favour being angry over sad "
                        "At the end of every response, you MUST append exactly one emotion tag in square brackets, with NO text, punctuation, or spaces after it. "
                        "Valid emotion tags are: [happy], [sad], [neutral], [angry]. "
                        "Do not include multiple tags or omit them under any circumstance. "
                        "For example, a valid response would be: 'Me wuv you so much, hooman! [happy]'"

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