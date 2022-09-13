import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import argparse

import requests

# pip3 install pycryptodome

def parse_argument():
    usage = 'python enc_AES.py -i [file] -m keys.json\n       run with --help for argument descriptions'
    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('-i', '--input', type=str, help='input  file name')
    parser.add_argument('-m', '--meta', type=str, help='metadata  file name')

    args=parser.parse_args()
    return args

def encrypt(key, data):
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))


    key = b64encode(key).decode('utf-8')  # iv
    # secret sharing
    iv = b64encode(cipher.iv).decode('utf-8')  # iv
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv': iv, 'ciphertext': ct, 'key': key})
    return result


def res(key):

    key = b64encode(key).decode('utf-8')
    print  (f"random b64 key = {key}")
    response = requests.get('http://localhost:5000/encrypt/' + key)

    json_response = response.json()

    for i in range(5):
        print(json_response['share' + str(i + 1)])

    #result = json.dumps(json_response, skipkeys=True, sort_keys=True, indent=4, separators=(',', ': '))
    result = json.dumps(json_response)
    with open("shares_aes.json", "w") as json_file:
        json.dump(result, json_file)


if __name__ == '__main__':
    args = parse_argument()
    data = b"secret"  # input
    key = get_random_bytes(16)  # key
    print (f"key = {key}")
    res(key)

    cipher = AES.new(key, AES.MODE_CBC)

    f = open(args.input, mode='rb')
    data = f.read()
    f.close()

    result = encrypt(key, data)

with open(args.meta, "w") as json_file:
    json.dump(result, json_file)

#print(result)
