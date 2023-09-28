import http.server

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        temperature = post_data.decode('utf-8')

        # Here you can process or save the temperature data as needed
        print(f'Received temperature data: {temperature}°C')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Received temperature data')

with http.server.HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler) as httpd:
    print('Server started at http://localhost:8000')
    httpd.serve_forever()