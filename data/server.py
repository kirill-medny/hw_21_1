import http.server
import socketserver
import urllib.parse

PORT = 8000


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/":
            self.path = "contacts.html"  # Default page
        try:
            # Read the HTML file
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("File not found".encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

    def do_POST(self) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = urllib.parse.parse_qs(post_data)

        print("Received POST data:")
        for key, value in parsed_data.items():
            print(f"{key}: {value}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("POST request received and processed!".encode("utf-8"))


Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
