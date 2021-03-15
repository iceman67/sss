from flask import Flask
from flask import Flask, request, jsonify
from base64 import b64decode, b64encode
from sss_py.sss import io_reader, shamir
import json
import sys

from sss_py.sss.io_reader import decode_secret

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

def print_shares(shares):
    # Print as hex strings
    share_dic = {}
    for x, y in shares:
        print("{:1x}-{:2x}".format(x,y))
        share_dic['share' + str(x)] =  "{:1x}-{:2x}".format(x,y)

        # Skip the secret

    result = json.dumps(share_dic,  skipkeys=True, sort_keys=True, indent=4, separators=(',', ': '))
    with open("shares1.json", "w") as json_file:
         json.dump(result, json_file)

    return result

# http://localhost:5000//encrypt/0CBlj2pgtGpMYQAVP%2BADlg%3D%3D
@app.route('/encrypt/<key>')
def encrypt(key=0):
    key = b64decode(key)
    print (f'Received key from Enc ={key}')
    threshold = 3
    shares = 5
    result = print_shares(
        shamir.encrypt(io_reader.parse_secret2(key, threshold, shares), threshold, shares))
    return result


@app.route('/decrypt', methods = ['POST'])
def decrypt():
    threshold = 3
    shares = 5
    if request.is_json:
         shares = request.get_json()
         print(f'Received shares from Dec = {shares}')
    else:
        return "Request was not JSON", 400


    #result = io_reader.print_secret2(
    #    shamir.decrypt(io_reader.parse_shares2(threshold), threshold, shares))

    result = shamir.decrypt(io_reader.parse_shares3(shares, threshold), threshold, shares)
    print (f"key = {decode_secret(result)}")
    okey = b64decode(decode_secret(result))

    print("Resulting secret: {}".format(okey))

    key = b64encode(okey).decode('utf-8')
    #return str(okey)
    return key



if __name__ == '__main__':
    app.run()