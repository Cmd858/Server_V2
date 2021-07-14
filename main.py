import sys
import colorama
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from RequestHandler import RequestHandler, log
from Minimise import ConsoleManager
from dotenv import load_dotenv


sys.stderr = open('errorLog.txt', 'w+')

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
        #log((data, rtype, response_code), 'info')
        if rtype == 'file':
            self.handler.returnResponse(self, data, response_code, rtype)  # send the response back to requester
        else:
            bytedata = self.handler.typeData(data, rtype)  # convert data to bytes
            self.handler.returnResponse(self, bytedata, response_code, rtype)


class threadedServer(ThreadingMixIn, HTTPServer):
    pass  # define a class that inherits above

class Main:
    def __init__(self):
        colorama.init()
        self.mgr = self.ConsoleControl()
        self.server_address = ('0.0.0.0', int(os.getenv('port')))
        # self.httpdpy = HTTPServer(server_address, MyHandler)  # single-threaded
        self.httpdpy = threadedServer(self.server_address, MyHandler)  # multi-threaded
        self.runServer()  # start the server

    def runServer(self):
        log(f'Server started on {self.server_address}', 'info')

        try:
            self.httpdpy.serve_forever(poll_interval=1)  # start the server and serve forever
        except (KeyboardInterrupt, SystemExit, OSError) as e:  # except KeyBoardInterrupt
            log(e, 'warning')


    def ConsoleControl(self):
        mgr = ConsoleManager(self.killServer)
        mgr.StartTrayIcon()
        return mgr

    def killServer(self):
        log('Exiting', 'info')
        self.httpdpy.shutdown()  # close server gracefully
        colorama.deinit()
        sys.exit()


if __name__ == '__main__':
    Main()
