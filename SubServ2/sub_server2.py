from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from ast import literal_eval


messages_list = list()


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):   # POST request handler
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = "Message recived:"+bytes.decode(post_data)
        self.wfile.write(bytes(message, "utf8"))
        msg = literal_eval(post_data.decode('utf-8'))['message']
        messages_list.append(msg)  # Saving received message to list
        print("POST handler <- Message recived:", msg)


    def do_GET(self):  # GET request handler
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        str_messages = ''
        for msg in messages_list:
            str_messages += msg+',\n'
        print("GET handler -> Listing saved messages...")
        # Listing saved messages of current node to client
        self.wfile.write(bytes(str_messages, 'utf8'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8090)
    httpd = server_class(server_address, handler_class)
    try:
        print("Server started...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutdown...")
        httpd.server_close()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


# using class ThreadedHTTPServer instead of HTTPServer for multithreading
run(server_class=ThreadedHTTPServer, handler_class=HttpHandler)
