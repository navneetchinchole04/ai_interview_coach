import google.generativeai as genai
import os

# Load your .env file if you’re using one
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\n🔍 Available Gemini Models:\n")
for m in genai.list_models():
    print(m.name)
