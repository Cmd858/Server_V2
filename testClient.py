import time

import requests
from dotenv import load_dotenv
import os

load_dotenv()

ip = os.getenv('ip')

headers = {'user-agent': 'Python script', 'Content-Length': str(b'bytes :)'.__sizeof__())}


r = requests.post(f'http://{ip}:8084/postbytes?input=testing', data=b'bytes :)')
print(r.text)
print(r.status_code)

r = requests.get(f'http://{ip}:8084/ping?input=testing', headers=headers)
print(r.text)
print(r.status_code)


r = requests.get(f'http://{ip}:8084/byteping?input=bytetesting', headers=headers)
print(r.text)
print(r.status_code)


r = requests.get(f'http://{ip}:8084/gethtml?input=Buy_Stuff_Home.html', headers=headers)
#print(r.text)
print(r.status_code)


r = requests.get(f'http://{ip}:8084/gethtml?input==?0=Buy_\ghrjS=tuf/f_/ome.html', headers=headers)
print(r.text)
print(r.status_code)

r = requests.delete(f'http://{ip}:8084/icon.ico', headers=headers)
#r = requests.put(f'http://{ip}:8084/icon.ico', headers=headers, data=open('files/favicon.ico', 'rb'))
print(r.text)
print(r.status_code)


r = requests.get(f'http://{ip}:8084/postbytes?input=testing', headers=headers)
print(r.text)
print(r.status_code)


r = requests.post(f'http://{ip}:8084/postbytes?input=testing', data=b'bytes :)')
print(r.text)
print(r.status_code)
