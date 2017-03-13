#!/usr/bin/env python3
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Send message back to client
        message = 'Hello world!\n'
        message = message + run_webinject()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
    
        self.wfile.write("Lorem Ipsum".encode("utf-8"))

 
def run():
    print('starting server...')
    
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

def run_webinject():
    print ("Running WebInject")
    result = subprocess.run(["perl", "..\WebInject-Framework\wif.pl", "..\WebInject\examples\get.xml"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print ("Args:", result.args)
    #print (result.stdout.decode())
    print ("Return Code:", result.returncode)
    return result.stdout.decode()
 
 
run()
# https://daanlenaerts.com/blog/2015/06/03/create-a-simple-http-server-with-python-3/