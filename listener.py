from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def handle_any(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode(errors="replace")
        print("---", self.command, self.path)
        print("Body:", body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"message": "Wrong Credentials"}')

    do_GET = handle_any
    do_POST = handle_any

    def log_message(self, *args):
        pass

HTTPServer(("127.0.0.1", 8888), Handler).serve_forever()