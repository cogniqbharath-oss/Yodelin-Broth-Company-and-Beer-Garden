
import urllib.request
import json
import urllib.error

# The key currently in server.py
GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
# List models
GEMINI_MODELS_URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

try:
    with urllib.request.urlopen(GEMINI_MODELS_URL) as response:
        data = json.load(response)
        print("Available Models:")
        for model in data.get('models', []):
            print(f"- {model['name']}")
            if 'generateContent' in model['supportedGenerationMethods']:
                print(f"  (Supports generateContent)")
except urllib.error.HTTPError as e:
    print(f"Error listing models: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Exception: {e}")
