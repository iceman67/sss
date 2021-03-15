import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

#json_input = result

import argparse

# pip3 install pycryptodome

def parse_argument():
    usage = 'python enc_AES.py -i [file] \n       run with --help for argument descriptions'
    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('-o', '--output', type=str, help='output file name')
    parser.add_argument('-m', '--meta', type=str, help='metadata file name')

    args=parser.parse_args()
    return args



def repeated_key_xor(plain_text, key):
    # returns plain text by repeatedly xoring it with key
    pt = plain_text
    len_key = len(key)
    encoded = []

    for i in range(0, len(pt)):
        encoded.append(pt[i] ^ key[i % len_key])
    return bytes(encoded)

def decrypt(json_input):
    try:
        b64 = json.loads(json_input)

        key = b64decode(b64['key'])
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        # to decrpt ciper into plain by key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        print("size of block = {}".format(AES.block_size))
        pt = unpad(cipher.decrypt(ct), AES.block_size)
    except ValueError:
        print("Incorrect decryption")
    except KeyError:
        print("Incorrect decryption")

    return pt


def decrypt2(json_input):
    try:
        b64 = json.loads(json_input)

        key = b64decode(b64['key'])

        # Encrypt using XOR Cipher with Repeating Key
        # https://www.geeksforgeeks.org/encrypt-using-xor-cipher-with-repeating-key/
        print ("key = {}".format(key))
        mask1 = b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
        print("Plain text: {}".format(mask1))

        # mask
        x =  repeated_key_xor(key, mask1)
        print("xor key = {}".format(x))

        # restore
        key = repeated_key_xor(x, mask1)
        print("key = {}".format(key))

        # mask
        '''
        Incorrect decryption
        '''
        key = repeated_key_xor(key, mask1)
        print("xor key = {}".format(key))

        # restore
        key = repeated_key_xor(key, mask1)




        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        # to decrpt ciper into plain by key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        print("size of block = {}".format(AES.block_size))
        pt = unpad(cipher.decrypt(ct), AES.block_size)
    except ValueError:
        print("Incorrect decryption")
    except KeyError:
        print("Incorrect decryption")

    return pt


if __name__ == '__main__':
    args = parse_argument()
    data = b"secret"  # input

    with open(args.meta, "r") as key_json:
        json_input = json.load(key_json)

    pt = decrypt(json_input)
    f = open(args.output, mode='wb')
    f.write(pt)
    f.close()