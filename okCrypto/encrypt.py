import ipfshttpclient as client
import okKey
import mfl
import os
import time
import argparse
import csv
import base64
import sys
from base64 import b32encode, b16encode

#  pre-requisite IPFS 0.5
#  C:\Users\yhkan\Desktop\go-ipfs>ipfs daemon

def parse_argument():
    usage = 'python encrypt.py -i [CDM file] -c [# of run] -s [size of key] \n       run with --help for argument descriptions'
    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('-i', '--input', type=str, help='input CDM file name')
    parser.add_argument('-c', '--count', type=int, help='input execute no')
    parser.add_argument('-s', '--size', type=int, help='size of symmetric key')
    args=parser.parse_args() 
    return args

if __name__ == '__main__':
    args = parse_argument()
    sz = args.size

    # read text file
    f = open(args.input, mode='rb')
    teststr = f.read()
    f.close()

    # change string to byte and split into two bytearray
    b1, b2 = mfl.split_even_odd(teststr)

    # create symmetric key
    symKey = os.urandom(sz)
    iv = os.urandom(16)

    # encrypt b1 with symKey and return iv and cb
    count = args.count
    for i in range(count):
        with open('pef.csv', mode='a') as pef:
           pw = csv.writer(pef, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           fSize = len(teststr)

           t0 = time.time()
           # 대칭키 암호화
           cb1 = okKey.encrypt(symKey, iv, b1)
           cb2 = okKey.encrypt(symKey, iv, b2)
           elapsed = time.time() - t0
           print ("size = {}, elaped time = {}".format(fSize, elapsed))
           pw.writerow([fSize, elapsed])

    fcb1 = open('first.txt', 'wb')
    fcb1.write(cb1)
    fcb1.close()

    fcb2 = open('second.txt', 'wb')
    fcb2.write(cb2)
    fcb2.close()

    try:
        c = client.connect('/ip4/127.0.0.1/tcp/5001/http')
        if c == None:
            Exception("There is a problem when getting hash values")
    except:
        print("An exception occurred when connecting IPFS[getIPFS_hash]")
        sys.exit(1)

    # 2개 cid
    add1 = c.add('first.txt')
    res1 = add1['Hash']
    add2 = c.add('second.txt')
    res2 = add2['Hash']

    # blockchain에 유지
    test_list = []
    test_list.append(b32encode(symKey).decode())
    test_list.append(b16encode(iv).decode())
    test_list.append(res1)
    test_list.append(res2)


    # read pub key for sending test_list
    yrpubkey = okKey.readPubKey("yrpubkey.pem").to_cryptography_key()

    # asymmetric encryption 블록체인에 자료접근시 비대칭키 사용
    enList = []
    for item in test_list:
        enList.append(okKey.pubEncrypt(yrpubkey, item))

    # sign the enList with my private key
    se = str(enList)

    # write (비대칭 암호화 내용) file information - this can be changed(how to send)
    f1 = open('sendfile.txt', 'w')
    f1.write(se)
    f1.close()

# sign test
    # 서명  DigSign
    sign = okKey.getHash(se.encode())
    f2 = open('signfile.txt', 'w')
    f2.write(str(sign))
    f2.close()