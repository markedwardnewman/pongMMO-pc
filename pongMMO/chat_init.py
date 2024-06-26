#  chat_init.py
import openai
import os

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_client():
    return openai
