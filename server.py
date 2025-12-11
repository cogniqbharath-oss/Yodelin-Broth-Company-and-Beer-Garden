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
            
            # Get message from user
            data = json.loads(post_data)
            user_message = data.get('message', '')
                
                if not user_message:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "No message provided"}')
                    return

                # Check if gemini_api is available
                try:
                    import gemini_api
                    reply = gemini_api.get_chat_response(user_message)
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
                    
                except ImportError:
                    print("Error: gemini_api module not found")
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Configuration Error: gemini_api missing"}')
                    
                except Exception as e:
                    print(f"Gemini API Error: {e}")
                    self.send_response(502) # Bad Gateway
                    self.end_headers()
                    error_msg = str(e)
                    self.wfile.write(json.dumps({'error': f"AI Service Error: {error_msg}"}).encode('utf-8'))
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
