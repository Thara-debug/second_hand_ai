import os
import time
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv

# 1. Load your secret key from the hidden .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Setup your API client using the secure variable
client = genai.Client(api_key=api_key)

prompt = """
Suggest 2 popular second-hand items for a student looking for a 'budget laptop for coding'.
For each item, provide:
1. Item Name
2. Estimated Original Price (in INR)
3. Estimated Second-hand Price (in INR)
4. Why it's a great deal
Keep the response clean and structured.
"""

# Try multiple models automatically if one experiences a 503 server busy error
models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]

success = False
for model_name in models_to_try:
    try:
        print(f"Trying model: {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        print("\n--- AI Response ---")
        print(response.text)
        success = True
        break
    except ServerError as e:
        print(f"Server busy for {model_name}, trying next model...")
        time.sleep(2)

if not success:
    print("\nAll models are currently experiencing high demand. Please wait 1 minute and try running python test_ai.py again.")