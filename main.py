import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from RequestHandler import RequestHandler
from SigListener import SigListener
from Minimise import ConsoleManager
from dotenv import load_dotenv
import os


load_dotenv()

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
        self.port = os.getenv('port')  # set port number
        self.handler = RequestHandler(self.port)  # get RequestHandler
        data, rtype, response_code = self.handler.handleRequest(self)  # handle request and receive data, type and code
        print(data, rtype, response_code)
        if rtype == 'file':
            self.handler.returnResponse(self, data, response_code, rtype)  # send the response back to requester
        else:
            bytedata = self.handler.typeData(data, rtype)  # convert data to bytes
            self.handler.returnResponse(self, bytedata, response_code, rtype)


class threadedServer(ThreadingMixIn, HTTPServer):
    pass  # define a class that inherits above

def runServer():
    server_address = ('0.0.0.0', int(os.getenv('port')))
    print(f'Server started on {server_address}')
    httpdpy = threadedServer(server_address, MyHandler)  # multi-threaded
    # httpdpy = HTTPServer(server_address, MyHandler)  # single-threaded
    try:
        httpdpy.serve_forever()  # start the server and serve forever
    except (KeyboardInterrupt, SystemExit):  # except KeyBoardInterrupt
        httpdpy.server_close()  # close server gracefully
        print('Successfully exiting')

def ConsoleControl():
    mgr = ConsoleManager(killServer)
    mgr.StartTrayIcon()

def listen():
    listener = SigListener(54320)  # get SigListener class
    listener.start()  # starts listener
    # depreciated because it requires 2 programs so bit useless tbh

def killServer():
    raise SyntaxError
    print('Exiting')
    sys.exit(0)  # TODO: get this to work properly bc doesn't exit

def main():
    ConsoleControl()
    runServer()  # start the server

if __name__ == '__main__':
    main()
