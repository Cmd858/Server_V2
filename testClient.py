import requests

ip = ''

headers = {'user-agent': 'Python script', 'Content-Length': str(b'bytes :)'.__sizeof__())}

r = requests.post(f'http://{ip}:8084/postbytes?input=testing', data=b'bytes :)')

print(r.text)

r = requests.get(f'http://{ip}:8084/ping?input=testing', headers=headers)

print(r.text)

r = requests.get(f'http://{ip}:8084/byteping?input=testing', headers=headers)

print(r.text)

r = requests.get(f'http://{ip}:8084/gethtml?input=Buy_Stuff_Home.html', headers=headers)

print(r.text)