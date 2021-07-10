# noinspection PyUnresolvedReferences
import Functions
import os

class RequestHandler():
    def __init__(self, port):
        self.port = port  # not needed but here anyway

    def handleRequest(self, request):  # request parameter takes myHandler class
        try:
            path = request.path  # get path in local variable
            headers = request.headers  # get headers in local variable
            if request.command == 'PUT':
                try:
                    file = open(f'{os.getcwd()}/files{path}', 'w+b')  # create and open file
                    data = request.rfile.read(int(headers['Content-Length']))  # read data from request body
                    file.write(data)  # write data to file
                    file.close()
                    return 'Resource Created', 'str', 201
                except KeyError:
                    return 'Content-Length Header Required', 'str', 411  # require content-length header
                except Exception as e:
                    print(e)
                    return 'Resource could not be created', 'str', 500
            elif request.command == 'DELETE':
                try:
                    os.remove(f'{os.getcwd()}/files{path}')  # only removal from the files folder is allowed
                    return 'Resource Successfully Removed', 'str', 500
                except FileNotFoundError:
                    return 'Requested Resource Not Found', 'str', 404
                except Exception as e:  # handle exceptions
                    print(e)
                    return 'Could not delete the resource', 'str', 500
            else:
                file = checkFiles(path)  # check if the file exists
                if file == None:
                    func = getFunc(path)  # get function reference of requested function
                    if func is not None:  # check if function exists
                        args = extractArgs(path)  # get arguments for functions
                        #print(request.command)
                        if request.command == 'GET':  # special cases for each request
                            #print(request.command)
                            out, rtype, response_code = func(args)
                            return out, rtype, response_code  # return output of GET function
                        elif request.command == 'POST':
                            #print(request.command)
                            data = request.rfile.read(int(headers['Content-Length']))
                            out, rtype, response_code = func(args, data)
                            return out, rtype, response_code  # return output of POST function
                        elif request.command == 'PUT':
                            #print(request.command)
                            return 'Not Implemented', 'str', 501  # not implemented
                        else:
                            #print(request.command)
                            return 'Method Not Allowed', 'str', 405  # method not allowed
                    else:
                        return 'Resource Not Found', 'str', 404  # return not found error
                else:
                    return file, 'file', 200  # successful request return
        except TypeError:
            return 'Incorrect Method Type', 'str', 400
        except Exception as e:
            print(e)
            return 'Internal Server Error', 'str', 500  # return internal server error

    def typeData(self, data, rtype):  # convert data to bytes from indicated value (rtype)
        if rtype == 'str':
            bytedata = bytes(str(data), 'utf8')
        elif rtype == 'bytes':
            bytedata = data
        else:
            raise TypeError('Invalid data type supplied by function')
        return bytedata

    def chunkdata(self, file):
        chunksize = 4096
        while 1:
            chunk = file.read(chunksize)
            #print(chunk)
            if not chunk:
                break
            yield chunk
            #data = data[chunksize:]
        #raise StopIteration

    def returnResponse(self, server, data, response_code, datatype):
        headers = {'Accept-Language': 'en'}
        if datatype == 'file':
            #print(os.path.getsize(data.name))
            headers['Content-Length'] = f'{os.path.getsize(data.name)}'
            server.send_response(response_code)  # send response code eg 200
            for header in headers:
                server.send_header(header, headers[header])  # send every header in headers
            server.end_headers()  # indicate that all headers have been sent
            for chunk in self.chunkdata(data):
                server.wfile.write(chunk)
            server.close_connection = True  # close connection, idk if this is necessary
            log('File Upload Complete')
            #print('filedone')
        else:
            headers['Content-Length'] = f'{data.__sizeof__()}'
            server.send_response(response_code)  # send response code eg 200
            for header in headers:
                server.send_header(header, headers[header])  # send every header in headers
            server.end_headers()  # indicate that all headers have been sent
            #print(data)
            server.wfile.write(data)
            server.close_connection = True
            #print('done')
            log('Request Complete')


def checkFiles(path):
    #print(path)
    if 'favicon.ico' in path:
        f = open(f'files/favicon.png', 'rb')
        print('favicon.png')
        return f.read(f.__sizeof__())
    try:
        #  with open(f'files{path}', 'rb') as f:  # context manager closes file which can't happen
        f = open(f'files{path}', 'rb')
        #print(f.__sizeof__())
        return f
    except FileNotFoundError:
        return None
    except OSError:
        return None


def getFunc(path):
    try:
        try:
            qindex = path.index('?')  # get index of ? character if it exists
        except Exception as e:
            print(e)
            qindex = len(path)  # run if ? is not in the request

        fstr = path[1:qindex]  # when path is eg '/ping' fstr is 'ping'
        func = eval(f'Functions.{fstr}')  # fancy import and run function by getting function reference
        return func  # return function reference
    except Exception as e:
        return None  # return None if function does not exist

def extractArgs(path):
    args = {}
    if '?' in path:
        indexPoint = path.index('?')  # get starting point of args
        complete = 0  # var to exit loop when needed
        while complete == 0:
            equalsIndex = path.index('=', indexPoint)  # find sep between keyword and arg
            try:
                ampersandIndex = path.index('&', indexPoint+1)  # find sep between keyword-arg pairs
            except ValueError:  # handles the end of the args
                ampersandIndex = len(path)  # set final index to end of path
                complete = 1  # exits after last arg is processed
            args[path[indexPoint+1:equalsIndex]] = path[equalsIndex+1:ampersandIndex]  # assigns args to key in dict
            indexPoint = ampersandIndex  # set new index point to get next key value pair
    #print(args)
    return args  # return arguments

def log(msg):
    print(msg)