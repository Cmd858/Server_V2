# noinspection PyUnresolvedReferences
import Functions
import os
import colorama
import datetime


class RequestHandler():
    def __init__(self, port):
        self.port = port  # not needed but here anyway

    def handleRequest(self, request):  # request parameter takes myHandler class
        try:
            path = request.path  # get path in local variable
            headers = request.headers  # get headers in local variable
            log(request.command, 'info')
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
                    log(e, 'warning')
                    return 'Resource could not be created', 'str', 500
            elif request.command == 'DELETE':
                try:
                    os.remove(f'{os.getcwd()}/files{path}')  # only removal from the files folder is allowed
                    return 'Resource Successfully Removed', 'str', 500
                except FileNotFoundError:
                    return 'Requested Resource Not Found', 'str', 404
                except Exception as e:  # handle exceptions
                    log(e, 'warning')
                    return 'Could not delete the resource', 'str', 500
            else:
                file = checkFiles(path)  # check if the file exists
                log(file, 'info')
                if file == None:
                    func = getFunc(path)  # get function reference of requested function
                    if func is not None:  # check if function exists
                        args = extractArgs(path)  # get arguments for functions
                        if request.command == 'GET':  # special cases for each request
                            out, rtype, response_code = func(args)
                            return out, rtype, response_code  # return output of GET function
                        elif request.command == 'POST':
                            data = request.rfile.read(int(headers['Content-Length']))
                            log(data, 'data')
                            out, rtype, response_code = func(args, data)
                            return out, rtype, response_code  # return output of POST function
                        elif request.command == 'PUT':
                            return 'Not Implemented', 'str', 501  # not implemented
                        else:
                            return 'Method Not Allowed', 'str', 405  # method not allowed
                    else:
                        return 'Resource Not Found', 'str', 404  # return not found error
                else:
                    return file, 'file', 200  # successful request return
        except TypeError:
            return 'Incorrect Method Type', 'str', 400
        except Exception as e:
            log(e, 'warning')
            return 'Internal Server Error', 'str', 500  # return internal server error

    def handleRequestBetter(self, request):  # request parameter takes myHandler class
        try:
            path = request.path  # get path in local variable
            headers = request.headers  # get headers in local variable
            log(request.command, 'info')
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
                    log(e, 'warning')
                    return 'Resource could not be created', 'str', 500
            elif request.command == 'DELETE':
                try:
                    os.remove(f'{os.getcwd()}/files{path}')  # only removal from the files folder is allowed
                    return 'Resource Successfully Removed', 'str', 500
                except FileNotFoundError:
                    return 'Requested Resource Not Found', 'str', 404
                except Exception as e:  # handle exceptions
                    log(e, 'warning')
                    return 'Could not delete the resource', 'str', 500
            elif request.command == 'POST':
                try:
                    log(path, 'data')
                    data = request.rfile.read(int(headers['Content-Length']))  # read data from request body
                        # log(part, 'data')
                    #log(data, 'data')
                    #data = b'teststr'
                    #todo make multipart parser
                    if data.startswith(b'------WebKitFormBoundary'):
                        #log(data, 'info')
                        data = data[data.index(b'\r\n')+2:]  # snip out boundary
                        disposition = data[:data.index(b'\r\n')]
                        #log(data, 'info')
                        data = data[data.index(b'\r\n')+2:]  # lmao so inefficient i think
                        ctype = data[:data.index(b'\r\n')]
                        #log(data, 'info')
                        data = data[data.index(b'\r\n')+2:]
                        data = data[data.index(b'\r\n')+2:]
                        filedat = data[:-46]  # enough space to remove multipart form boundary
                        #log(data, 'info')
                        #log(disposition, 'data')
                        #log(ctype, 'data')
                        #log(filedat, 'data')
                        filenamestart = disposition.index(b'filename="')+10
                        fname = disposition[filenamestart:disposition.index(b'"', filenamestart)].decode('utf8')
                        #log(fname, 'data')
                        file = open(f'{os.getcwd()}/files/{fname}', 'w+b')  # create and open file
                        file.write(filedat)  # write data to file
                        file.close()  # TODO: probs unnecessary but maybe lazy iterator with yield
                    else:
                        return 'Invalid Form Type', 'str', 501
                    return 'Resource Created', 'str', 201
                except KeyError:
                    return 'Content-Length Header Required', 'str', 411  # require content-length header
                except Exception as e:
                    log(e, 'warning')
                    return 'Resource could not be created', 'str', 500
            else:
                file = checkFiles(path)  # check if the file exists
                #log(file, 'info')
                if file == None:
                    func = getFunc(path)  # get function reference of requested function
                    if func is not None:  # check if function exists
                        args = extractArgs(path)  # get arguments for functions
                        if request.command == 'GET':  # special cases for each request
                            out, rtype, response_code = func(args)
                            return out, rtype, response_code  # return output of GET function
                        elif request.command == 'POST':
                            data = request.rfile.read(int(headers['Content-Length']))
                            #log(data, 'data')
                            out, rtype, response_code = func(args, data)
                            return out, rtype, response_code  # return output of POST function
                        elif request.command == 'PUT':
                            return 'Not Implemented', 'str', 501  # not implemented
                        else:
                            return 'Method Not Allowed', 'str', 405  # method not allowed
                    else:
                        return 'Resource Not Found', 'str', 404  # return not found error
                else:
                    return file, 'file', 200  # successful request return
        except TypeError:
            return 'Incorrect Method Type', 'str', 400
        except Exception as e:
            log(e, 'warning')
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
            if not chunk:
                break
            yield chunk

    def returnResponse(self, server, data, response_code, datatype):
        headers = {'Accept-Language': 'en'}
        if datatype == 'file':
            headers['Content-Length'] = f'{os.path.getsize(data.name)}'
            server.send_response(response_code)  # send response code eg 200
            for header in headers:
                server.send_header(header, headers[header])  # send every header in headers
            server.end_headers()  # indicate that all headers have been sent
            for chunk in self.chunkdata(data):
                server.wfile.write(chunk)
            server.close_connection = True  # close connection, idk if this is necessary
            log('File Upload Complete', 'info')
        else:
            headers['Content-Length'] = f'{data.__sizeof__()}'
            server.send_response(response_code)  # send response code eg 200
            for header in headers:
                server.send_header(header, headers[header])  # send every header in headers
            #log(data[:30], 'data')
            server.end_headers()  # indicate that all headers have been sent
            server.wfile.write(data)
            server.close_connection = True
            log('Request Complete', 'info')


def checkFiles(path):
    if 'favicon.ico' in path:
        f = open(f'files/favicon.png', 'rb')
        log('Request for favicon.png', 'info')
        return f  #.read(f.__sizeof__())
    try:
        #  with open(f'files{path}', 'rb') as f:  # context manager closes file which can't happen
        f = open(f'files{path}', 'rb')
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
            log(e, 'warning')
            qindex = len(path)  # run if ? is not in the request

        fstr = path[1:qindex]  # when path is eg '/ping' fstr is 'ping'
        func = eval(f'Functions.{fstr}')  # fancy import and run function by getting function reference
        return func  # return function reference
    except Exception as e:
        log(e, 'warning')
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
    return args  # return arguments

def log(msg, msgType):
    clrs = {'warning': colorama.Fore.RED, 'info': colorama.Fore.WHITE, 'clientError': colorama.Fore.YELLOW}
    now = datetime.datetime.now()
    modnow = now.strftime(f'%Y-%m-%d %H:%M:%S')
    prtstr = f'[{modnow}] {msg}'
    if msgType in clrs:
        print(f'{clrs[msgType]}{prtstr}')
    else:
        print(f'{colorama.Fore.CYAN}{prtstr}')
