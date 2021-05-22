import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
from RequestHandler import RequestHandler
from SigListener import SigListener

class MyHandler(BaseHTTPRequestHandler):

    # All http methods apart from some maybe, using lambda to make it neat
    do_GET = lambda self: self.processRequest()
    do_POST = lambda self: self.processRequest()
    do_HEAD = lambda self: self.processRequest()
    do_PUT = lambda self: self.processRequest()
    do_PATCH = lambda self: self.processRequest()
    do_DELETE = lambda self: self.processRequest()
    do_OPTIONS = lambda self: self.processRequest()
    # violates PEP but looks cool

    def processRequest(self):
        self.port = 8084  # set port number
        self.handler = RequestHandler(self.port)  # get RequestHandler
        data, rtype, response_code = self.handler.handleRequest(self)  # handle request and receive data, type and code
        print(data, rtype, response_code)
        bytedata = self.handler.typeData(data, rtype)  # convert data to bytes
        self.handler.returnResponse(self, bytedata, response_code)  # send the response back to requester
        #self.send_response()

class threadedServer(ThreadingMixIn, HTTPServer):
    pass  # define a class that inherits above

def runServer():
    server_address = ('0.0.0.0', 8084)
    httpdpy = threadedServer(server_address, MyHandler)  # multi-threaded
    #httpdpy = HTTPServer(server_address, MyHandler)  # single-threaded
    httpdpy.serve_forever()  # start the server and serve forever

def listen():
    listener = SigListener(54320)  # get SigListener class
    listener.start()  # starts listener

def main():
    listen()  # activate systray listener
    runServer()  # start the server


main()
