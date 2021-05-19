# noinspection PyUnresolvedReferences
import Functions

class RequestHandler():
    def __init__(self, port):
        self.port = port

    def handleRequest(self, request):  # request parameter takes myHandler class
        path = request.path
        headers = request.headers
        #path = request  # raw string testing
        file = checkFiles(path)
        if file == None:
            func = getFunc(path)
            #print(func)
            if func is not None:
                args = extractArgs(path)
                #print(args)
                if request.command == 'GET':
                    out, rtype = func(args)
                    return out, rtype
                elif request.command == 'POST':
                    data = request.rfile.read(int(headers['Content-Length']))
                    #print(data)
                    #print('post')
                    #args['data'] = request
                    out, rtype = func(args, data)
                    #print(out, rtype)
                    #print('posted')
                    return out, rtype
                else:
                    raise TypeError('Unsupported request type')
            else:
                return None, 'str'
        else:
            return file, 'bytes'

    def typeData(self, data, rtype):
        if rtype == 'str':
            bytedata = bytes(str(data), 'utf8')
        elif rtype == 'bytes':
            bytedata = data
        else:
            raise TypeError('Invalid data type supplied by function')
        #print(bytedata)
        return bytedata


def checkFiles(path):
    print(path)
    try:
        f = open(f'files{path}', 'rb')
        return f.read(f.__sizeof__())
    except FileNotFoundError:
        print('FNFerror')
        return None


def getFunc(path):
    try:
        try:
            qindex = path.index('?')
        except Exception as e:
            print(e)
            qindex = len(path)

        fstr = path[1:qindex]  # when path is eg '/ping'
        func = eval(f'Functions.{fstr}')
        return func
    except Exception as e:
        #print(e)
        #raise e
        return None

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
            indexPoint = ampersandIndex
    return args


if __name__ == '__main__':
    p = 'http://localhost:8084/ping?input=testing&pingnum=20'  # testing extractArgs
    print(RequestHandler().handleRequest(p))