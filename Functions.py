def ping(args):
    return f"ping with input {args['input']}", 'str'  # return output and return type


def byteping(args):
    return bytes(f"ping with input {args['input']}", 'utf8'), 'bytes'

def postbytes(args, data):
    return data, 'bytes'

def gethtml(args):
    try:
        with open(f"files/{args['input']}", 'rb') as html:
            return html.read(html.__sizeof__()), 'bytes'
    except Exception as e:
        print(e)
        return None, 'str'
