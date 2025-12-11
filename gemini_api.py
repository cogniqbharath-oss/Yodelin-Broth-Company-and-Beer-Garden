import google.generativeai as genai
import os

# Configure the API key
GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the models to try in order
# gemini-1.5-flash-8b is often faster/cheaper.
# gemini-1.5-flash is standard.
# gemini-2.0-flash-exp is experimental and may have separate quota.
MODELS_TO_TRY = [
    'gemini-2.0-flash',
    'gemini-flash-latest',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b'
]

def get_chat_response(message):
    """
    Sends a message to Gemini and returns the response text.
    Includes context about Yodelin Broth Company.
    Retries with different models if one fails (e.g. quota).
    """
    context = """
    You are the helpful AI assistant for Yodelin Broth Company & Beer Garden in Leavenworth, WA. 
    We are a stylish, rustic joint offering bone broth, burgers, salads, and craft beer with mountain views.
    Location: 633 Front St #1346, Leavenworth, WA.
    Hours: Mon-Thu 11am-9pm, Fri-Sun 11am-10pm.
    We do takeout (ToastTab) and have a beer garden.
    We specialize in Bone Broth (healing, 24hr simmer) and Craft Beer interactions (inventory varies).
    Tone: Friendly, rustic, helpful, slightly hipster/outdoorsy but professional.
    Keep answers concise (under 50 words usually).
    """
    full_prompt = f"{context}\nUser asked: {message}"

    last_error = None

    for model_name in MODELS_TO_TRY:
        try:
            # Configure model
            model = genai.GenerativeModel(model_name)
            chat = model.start_chat(history=[])
            response = chat.send_message(full_prompt)
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            # Continue to next model
    
    # If all failed
    raise last_error

