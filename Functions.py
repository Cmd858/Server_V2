# mostly for testing purposes

def ping(args):
    return f"ping with input {args['input']}", 'str', 200  # return output, return type and response code


def byteping(args):
    return bytes(f"ping with input {args['input']}", 'utf8'), 'bytes', 200

def postbytes(args, data):
    return data, 'bytes', 200

def gethtml(args):
    try:
        with open(f"files/{args['input']}", 'rb') as f:
            return f.read(f.__sizeof__()), 'bytes', 200
    except Exception:
        return 'Bad Request', 'str', 400
