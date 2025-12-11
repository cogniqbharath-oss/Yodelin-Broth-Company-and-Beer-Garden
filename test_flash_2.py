import google.generativeai as genai
import os
import time

GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
genai.configure(api_key=GEMINI_API_KEY)

print("Testing gemini-2.0-flash-exp...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Hello")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error: {e}")
