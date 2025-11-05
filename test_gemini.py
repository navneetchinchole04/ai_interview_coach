import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env variables

# Configure Gemini using your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    # ✅ List all available models
    models = genai.list_models()
    print("\n✅ Available Gemini Models:\n")
    for m in models:
        print(" -", m.name)
    
    # ✅ Test with a basic prompt
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a simple Python program that prints Hello World.")
    print("\n✅ Gemini Response:\n")
    print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")
