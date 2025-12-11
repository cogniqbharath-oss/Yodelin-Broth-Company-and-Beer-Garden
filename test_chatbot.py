import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
genai.configure(api_key=GEMINI_API_KEY)

try:
    # Try 1.5-flash first
    print("Testing gemini-1.5-flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print(f"Success 1.5-flash: {response.text}")
except Exception as e:
    print(f"Error 1.5-flash: {e}")
    try:
        # Try gemini-pro as fallback
        print("Testing gemini-pro...")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        print(f"Success gemini-pro: {response.text}")
    except Exception as e2:
        print(f"Error gemini-pro: {e2}")
        try:
            # Try gemini-1.5-flash-latest
            print("Testing gemini-1.5-flash-latest...")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content("Hello")
            print(f"Success 1.5-flash-latest: {response.text}")
        except Exception as e3:
            print(f"Error 1.5-flash-latest: {e3}")
            try:
                # Try gemini-2.0-flash-exp
                print("Testing gemini-2.0-flash-exp...")
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                response = model.generate_content("Hello")
                print(f"Success 2.0-flash-exp: {response.text}")
            except Exception as e4:
                print(f"Error 2.0-flash-exp: {e4}")
