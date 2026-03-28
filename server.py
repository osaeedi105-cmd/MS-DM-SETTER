from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PORT = int(os.environ.get("PORT", 8080))

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_file("static/index.html", "text/html")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            self.handle_chat()
        elif self.path == "/api/score":
            self.handle_score()
        else:
            self.send_response(404)
            self.end_headers()

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def call_anthropic(self, system, messages, max_tokens=500):
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]

    def handle_chat(self):
        try:
            body = self.read_body()
            system = body["system"]
            messages = body["messages"]
            reply = self.call_anthropic(system, messages, 500)
            self.send_json({"reply": reply})
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def handle_score(self):
        try:
            body = self.read_body()
            system = body["system"]
            messages = body["messages"]
            reply = self.call_anthropic(system, messages, 700)
            self.send_json({"reply": reply})
        except Exception as e:
            self.send_json({"error": str(e)}, 500)


if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
