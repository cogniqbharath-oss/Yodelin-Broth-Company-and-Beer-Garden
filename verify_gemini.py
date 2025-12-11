
import gemini_api
import sys

try:
    print("Testing gemini_api...")
    response = gemini_api.get_chat_response("Hello, are you working?")
    print(f"Response received: {response}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
