import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
from RequestHandler import RequestHandler
from SigListener import SigListener

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.processRequest()  # post and get requests are separated later

    def do_POST(self):
        self.processRequest()

    def processRequest(self):
        self.port = 8084
        self.getHandler = RequestHandler(self.port)
        # print('handler created')
        data, rtype = self.getHandler.handleRequest(self)
        # print('dat got')
        bytedata = self.getHandler.typeData(data, rtype)
        self.send_response(200)
        self.send_header('response', 'True')
        self.end_headers()
        self.wfile.write(bytedata)
        #print('written')
        self.close_connection = True

class threadedServer(ThreadingMixIn, HTTPServer):
    pass  # define a class that inherits above

def runServer():
    server_address = ('0.0.0.0', 8084)
    httpdpy = threadedServer(server_address, MyHandler)
    httpdpy.serve_forever()

def listen():
    listener = SigListener(54320)
    listener.start()

def main():
    listen()
    runServer()

main()
