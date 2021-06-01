import json
import requests
from base64 import b64encode


headers = {
    'Authorization': 'Token 5e6871e179a87b0143ae153024f90495918c4467',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

data = json.load(open('corpora.json', 'r'))

files = {
    'file': open('corpus/hansard-reo-māori.txt', 'rb')
}

response = requests.post('https://koreromaori.com/api/text/', headers=headers, data=json.dumps(data))

print('Status code:', response.status_code)
print('Response', response.text)
