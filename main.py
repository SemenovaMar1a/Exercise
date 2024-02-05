from http.server import BaseHTTPRequestHandler, HTTPServer
from Functions import *


def process_request(path):
    if path.startswith('/city/'):
        return Tasks.first_task(path)
    elif path.startswith('/cities?'):
        return Tasks.second_task(path)
    elif path.startswith('/compare?'):
        return Tasks.third_task(path)
    else:
        return json.dumps({"error": "Invalid path"})


print(process_request("/compare?city1=Moscow&city2=Trostnikovka"))
print(process_request('/city/817114'))
print(process_request('/cities?page=1&page_size=5'))


class GeoNamesRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = process_request(self.path)
        self.wfile.write(response.encode())


def run(server_class=HTTPServer, handler_class=GeoNamesRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
