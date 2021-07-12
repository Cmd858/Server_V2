# mostly for testing purposes
import urllib.parse

def ping(args):
    return f"ping with input {args['input']}", 'str', 200  # return output, return type and response code


def byteping(args):
    return bytes(f"ping with input {args['input']}", 'utf8'), 'bytes', 200


def postbytes(args, data):  # args + data for post requests
    return data, 'bytes', 200


def gethtml(args):
    try:
        with open(f"files/{args['input']}", 'rb') as f:
            return f.read(f.__sizeof__()), 'bytes', 200
    except Exception:
        return 'Bad Request', 'str', 400

def gethtmlfile(args):
    try:
        #with open(f"files/{args['input']}", 'rb') as f:
        f = open(f"files/{args['input']}", 'rb')
        return f, 'file', 200
    except Exception:
        return 'Bad Request', 'str', 400

def anagram(args):
    anagram = args['input'].lower()
    wordlist = open('wordlist.txt')
    matches = []
    chars = 'abcdefghijklmnopqrstuvwxyz'
    for i in wordlist.read().splitlines():
        count = 0
        if len(anagram) == len(i):
            #print('len')
            for j in range(26):
                if anagram.count(chars[j]) == i.count(chars[j]):
                    count += 1
            #print(count)
            if count == 26:
                matches.append(i)
    return matches


def scrabble(args):
    l = []
    letterset = args['input']
    #print('Enter LetterSet')
    #letterset = input('>>> ')
    wordlist = open('wordlist.txt')
    chars = 'abcdefghijklmnopqrstuvwxyz'
    count = 0
    for i in wordlist.read().splitlines():
        for j in range(26):
            # print(chars[j])
            if i.count(chars[j]) > letterset.count(chars[j]):
                j -= 1
                break
        if j == 25:
            #print(i)
            l.append(i)
            count += 1
        # print(i)
        # print(j)
    return l

def crossword(args):
    print(args['input'])
    solveword = bytes(urllib.parse.unquote(args['input']), 'utf8').replace(b'\xe2\x80\x93',b'--').decode('utf8')
    #solveword = args['input']
    print(solveword)
    solveword = solveword.replace('\xe2\x80\x93', '--')
    print(solveword)
    wordlen = len(solveword)
    wordlist = open('wordlist.txt')
    #wordlist2 = open('wordlist2.txt')
    countries = open('countrys.txt')
    names = open('names.txt')
    surnames = open('surnames.txt')
    #frwords = open('FrWordlist.txt')
    wordcount = 0
    #wordcount2 = 0
    countrycount = 0  # add count for each
    namecount = 0
    #frcount = 0
    snamecount = 0
    countlist = [wordcount, countrycount , namecount, snamecount] #add count var here
    checklist = [wordlist, countries , names, surnames]  #add list here
    subjectlist = ['Words' , 'Countries' , 'Names' , 'Surnames', ] # name
    words = []
    for k in range(len(checklist)):
        for i in checklist[k].read().splitlines():
            if wordlen == len(i):
                for j in range(len(i)):
                    #print(solveword)
                    if solveword[j] == '_':
                        #print('yay')
                        pass
                    elif i[j] != solveword[j]:
                        j-=1
                        break
                if j+1 == len(i):
                    print(f'{subjectlist[k]}: {i}')
                    words.append(f'{subjectlist[k]}: {i}')
                    countlist[k] += 1
    print(f'words: {words}')
    return words
    #return bluetoothtest([])

