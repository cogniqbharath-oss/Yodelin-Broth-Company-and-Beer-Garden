import google.generativeai as genai
import os

# Configure the API key
GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
# Using gemini-1.5-flash as it is fast and efficient for chat
model = genai.GenerativeModel('gemini-1.5-flash')

def get_chat_response(message):
    """
    Sends a message to Gemini and returns the response text.
    Includes context about Yodelin Broth Company.
    """
    try:
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
        
        chat = model.start_chat(history=[])
        full_prompt = f"{context}\nUser asked: {message}"
        
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Return a user-friendly error or raise
        raise e
