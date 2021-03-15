import requests
import okKey
import mfl
import os
import io
from ast import literal_eval
import base64
from base64 import b64encode, b32decode, b64decode

import time
import argparse
import csv
import sys


def parse_argument():
    usage = 'python decrypt.py -i [input sendfile.txt] -o [output file] -s [signfile] -k [private key]\n       run wi    th --help for argument descriptions'
    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('-i', '--input', type=str, help='input sendfile.txt', required=True)
    parser.add_argument('-o', '--output', type=str, help='output file',  required=True)
    parser.add_argument('-s', '--sign', default='signfile.txt', type=str, help='input signiture.txt')
    parser.add_argument('-k', '--pk', type=str, default='yrprikey.pem', help='private key, yrprikey.pem')
    parser.add_argument('-c', '--count', default=1, type=int, help='input execute no')
    args=parser.parse_args() 
    return args

def verify(input_file, sign_file):
    sf = open(input_file, 'r')
    sendfile = sf.read()
    sf.close()
    enList = literal_eval(sendfile)

    # sign verification
    ### open a signature file - sign is a string type
    vf = open(sign_file, 'r')
    signf = vf.read()
    vf.close()
    ### get hash of enList and change a type same as a signf
    se = str(enList)
    cEnList = okKey.getHash(se.encode())
    assert signf == str(cEnList)

    return enList

def decrypt(pk_file, enList):
    yrprikey = okKey.readKey(pk_file).to_cryptography_key()
    deList = []

    for item in enList:
        a = okKey.priDecrypt(yrprikey, item)
        deList.append(a)
        #deList.append(a.decode())
    return deList

def getIPFS_hash(deList):
    deList[0] = base64.b32decode(deList[0])  # SymKey
    deList[1] = base64.b16decode(deList[1])  # IV

    oneipfsaddr = deList[2]   # Hash 1
    oneipfsaddr = oneipfsaddr.decode()
    twoipfsaddr = deList[3]   # Hash 2
    twoipfsaddr = twoipfsaddr.decode()

    print ("oneipfsaddr={}".format(oneipfsaddr))
    req1 = requests.get('http://127.0.0.1:8080/ipfs/' + oneipfsaddr)
    req2 = requests.get('http://127.0.0.1:8080/ipfs/' + twoipfsaddr)

    return req1, req2


if __name__ == '__main__':
    args = parse_argument()

    input_file = args.input
    sign_file = args.sign
    pk_file  = args.pk
    output_file = args.output


    # DigSign 검증
    cEnList = verify(input_file, sign_file)
    deList = decrypt(pk_file, cEnList)


    try:
       req1, req2 = getIPFS_hash(deList)

       if req1 == None or req2 == None:
           Exception("There is a problem when getting hash values")
    except:
       print("An exception occurred when connecting IPFS[getIPFS_hash]")
       sys.exit(1)

    getcb1 = req1.content
    getcb2 = req2.content


    count = args.count
    for i in range(count):
        with open('pef.csv', mode='a') as pef:
           pw = csv.writer(pef, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

           t0 = time.time()

           db1 = okKey.decrypt(deList[0], deList[1], getcb1)
           db2 = okKey.decrypt(deList[0], deList[1], getcb2)

           mergedbs = mfl.mergeToString(db1, db2)
           getmyfile = open(output_file, 'wb')

           getmyfile.write(mergedbs)

           getmyfile.close()

           elapsed = time.time() - t0
           fSize = len(mergedbs)
           print ("size = {}, elaped time = {}".format(fSize, elapsed))
           pw.writerow([fSize, elapsed])
