from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):

    @staticmethod
    def bytes_from_file(filename):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(1)
                if chunk:
                    for b in chunk:
                        yield b
                else:
                    break

    def do_GET(self):
        data: bytes = bytes()
        if self.path == '/':
            self.path = '/index.html'
        try:
            self.path = f"/web{self.path}"
            print(self.path[1:])
            data = bytes(Serv.bytes_from_file(self.path[1:]))
            self.send_response(200)
        except:
            data = b"File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(data)
        def log_message(self, format, *args):
            return