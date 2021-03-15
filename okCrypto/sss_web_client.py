import requests
from base64 import b64encode
from Crypto.Random import get_random_bytes
from base64 import b64decode, b64encode
import json

key = get_random_bytes(16)  # key

print (f"Generated key = {key}")
key = b64encode(key).decode('utf-8')
#print  (f"random b64 key = {key}")
response = requests.get('http://localhost:5000/encrypt/' + key)

json_response = response.json()

for i in range(5):
    print (json_response['share'+str(i+1)])


json_shares = { 'share1' : '1-cbe3fae4029234e91b00996a577ee0a2388db3963515048f999469dd53a5ded3b',
                'share2': '2-79b0b76ee0ce5d9de42870be03b01bc30268c9ea30f08ebb86df64f7b51368f89b',
                'share3': '3-6be5efae43bb02ec99a03433eaf9730ff2ea9d4d4d6978b925ead91627e83f5cb'}


url = 'http://localhost:5000/decrypt'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data= json.dumps(json_response), headers=headers)

key = b64decode(response.content)
print (f"Received  key = {key}")


