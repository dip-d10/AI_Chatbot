import openai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (new method)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to get response from OpenAI
def chatbot_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Example test
print("Bot:", chatbot_response("Hello, how are you?"))
