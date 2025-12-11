from http import server
import socketserver
import os
import json
import urllib.request
import urllib.error

PORT = 8000
# IMPORTANT: Replace the placeholder below with your actual Google Gemini API key
GEMINI_API_KEY = "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

class Handler(server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                user_message = data.get('message', '')
                
                if not user_message:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "No message provided"}')
                    return

                # Construct the prompt for Gemini
                context = f"""
                You are the helpful AI assistant for Yodelin Broth Company & Beer Garden in Leavenworth, WA. 
                We are a stylish, rustic joint offering bone broth, burgers, salads, and craft beer with mountain views.
                Location: 633 Front St #1346, Leavenworth, WA.
                Hours: Mon-Thu 11am-9pm, Fri-Sun 11am-10pm.
                We do takeout (ToastTab) and have a beer garden.
                We specialize in Bone Broth (healing, 24hr simmer) and Craft Beer interactions (inventory varies).
                Tone: Friendly, rustic, helpful, slightly hipster/outdoorsy but professional.
                Keep answers concise (under 50 words usually).
                User asked: {user_message}
                """
                
                payload = {
                    "contents": [{
                        "parts": [{"text": context}]
                    }]
                }
                
                # Call Gemini API
                req = urllib.request.Request(
                    GEMINI_API_URL,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                
                try:
                    with urllib.request.urlopen(req) as response:
                        response_data = json.load(response)
                        # Extract the text
                        reply = response_data['candidates'][0]['content']['parts'][0]['text']
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
                        
                except urllib.error.HTTPError as e:
                    print(f"Gemini API Error: {e.code} - {e.read()}")
                    self.send_response(502) # Bad Gateway
                    self.end_headers()
                    self.wfile.write(b'{"error": "Failed to contact AI service"}')
                    
            except Exception as e:
                print(f"Server Error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"error": "Internal Server Error"}')
        else:
            self.send_error(404, "File not found")

# Change to the directory where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Serving at http://localhost:{PORT}")
print(f"API Key configured (snippet): {GEMINI_API_KEY[:5]}...")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
