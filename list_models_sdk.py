import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
genai.configure(api_key=GEMINI_API_KEY)

print("Listing models...")
try:
    with open("models_output.txt", "w") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(m.name + "\n")
except Exception as e:
    with open("models_output.txt", "w") as f:
        f.write(f"Error: {e}")
