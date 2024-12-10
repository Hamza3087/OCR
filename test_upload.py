import requests

url = 'http://127.0.0.1:8082/upload'
file = {'image': open('./temp_image.png', 'rb')}
response = requests.post(url, files=file)
print(response.json())
