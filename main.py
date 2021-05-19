from http.server import BaseHTTPRequestHandler, HTTPServer
from RequestHandler import RequestHandler

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.port = 8084
        self.getHandler = RequestHandler(self.port)
        #print('handler created')
        data, rtype = self.getHandler.handleRequest(self)
        #print('dat got')
        bytedata = self.getHandler.typeData(data, rtype)
        self.send_response(200)
        self.send_header('response', 'True')
        self.end_headers()
        self.wfile.write(bytedata)
        print('writteng')


    def do_POST(self):
        self.port = 8084
        self.getHandler = RequestHandler(self.port)
        #print('handler created')
        data, rtype = self.getHandler.handleRequest(self)
        #print('dat got')
        bytedata = self.getHandler.typeData(data, rtype)
        self.send_response(200)
        self.send_header('response', 'True')
        self.end_headers()
        self.wfile.write(bytedata)
        print('written')

def main():
    server_address = ('0.0.0.0', 8084)
    httpdpy = HTTPServer(server_address, MyHandler)
    httpdpy.serve_forever()


main()