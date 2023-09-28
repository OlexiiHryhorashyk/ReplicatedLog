from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from ast import literal_eval
from threading import Thread
import requests


messages_list = list()
ports = [8080, 8090]  # local ports to link with same ports of other nodes in network
# url = [f'http://localhost:{port}/' for port in ports] # for running without docker locally
url = [f'http://node1:{ports[0]}', f'http://node2:{ports[1]}']  # for docker containers


class HttpHandler(BaseHTTPRequestHandler):
    def send_to_sub(self, url_addres, msg):  # attempt to send received message to secondary by url
        try:
            requests.post(url_addres, json=msg)
            print("POST request -> Message send to "+str(url.index(url_addres)+1)+" subsequent server - "+msg)
        except requests.exceptions.ConnectionError:
            print("POST ERROR -> No connection to the "+str(url.index(url_addres)+1)+"sub server! Message not passed!")
        return

    def do_POST(self):  # POST request handler
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = "Message recived:"+bytes.decode(post_data)
        self.wfile.write(bytes(message, "utf8"))
        msg = literal_eval(post_data.decode('utf-8'))
        print("POST handler <- Message recived:", msg)
        # Saving received message and replicating to secondary nodes
        messages_list.append(msg)
        # requests.post(url[0], json=msg) # simple sequential log replication (not slower then multithreading)
        # requests.post(url[1], json=msg)
        thread_list = []
        for i in range(len(url)):  # generating threads for simultaneous request sending to all secondary nodes
            # Pseudo multithreading, python executes threads sequentially
            thread = Thread(target=self.send_to_sub, args=(url[i], msg))
            thread.run()
            thread_list.append(thread)

    def do_GET(self):  # GET request handler
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        str_messages = ''
        for msg in messages_list:
            str_messages += msg+',\n'
        print("GET handler -> Listing saved messages...")
        # Listing saved messages of master node to client
        self.wfile.write(bytes(str_messages, 'utf8'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Server started...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutdown...")
        httpd.server_close()


run(handler_class=HttpHandler)
