#a
import requests
import os
from dotenv import load_dotenv

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
load_dotenv() #do not forget this, os.getenv doesnt work if you dont have this.
from google import genai

class AIGen:
    def __init__(self):
        pass
    def generate(self, re):
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=f"""Could you please write something about this question? And put your writing with a @ at the start and end:
            {re}"""
        )
        return response.text
