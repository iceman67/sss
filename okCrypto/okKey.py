import os
import OpenSSL
from OpenSSL import crypto
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

def getKey():
    key = crypto.PKey()
    try:
        key.generate_key(crypto.TYPE_RSA, 2048)
    except Exception as e:
        print(e)
    return key

def readKey(fName):
    keyFile = open(fName, 'r')
    keyDump = keyFile.read()
    keyFile.close()
    key = crypto.load_privatekey(crypto.FILETYPE_PEM, keyDump,
                passphrase=b'okCrypto')
    return key

def writeKey(fName, pKey):
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pKey, cipher='aes256',
                passphrase=b'okCrypto')
    keyFile = open(fName, 'w')
    keyFile.write(key.decode())
    keyFile.close()
    return key

def getPubKey(pKey):
    keyDump = crypto.dump_publickey(crypto.FILETYPE_PEM, pKey)
    key = crypto.load_publickey(crypto.FILETYPE_PEM, keyDump)
    return key

def getPubID(pKey):
    id = getHash(crypto.dump_publickey(crypto.FILETYPE_PEM, pKey))
    return base64.b64encode(id).decode()

def readPubKey(fName):
    keyFile = open(fName, 'r')
    keyDump = keyFile.read()
    keyFile.close()
    key = crypto.load_publickey(crypto.FILETYPE_PEM, keyDump)
    return key

def writePubKey(fName, pKey):
    key = crypto.dump_publickey(crypto.FILETYPE_PEM, pKey)
    keyFile = open(fName, 'w')
    keyFile.write(key.decode())
    keyFile.close()
    return key

def readCert(fName):
    certFile = open(fName, 'r')
    x509Dump = certFile.read()
    certFile.close()
    print(x509Dump)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, x509Dump)
    return cert

def writeCert(fName, pKey):
    cert = crypto.X509()
    cert.get_subject().commonName = "ok root CA"
    cert.get_issuer().commonName = "ok root CA"
    cert.set_notAfter('20201030235959Z'.encode("ascii"))
    cert.set_notBefore('20200101000000Z'.encode("ascii"))
    cert.set_pubkey(pKey)
    cert.add_extensions([])
    cert.sign(pKey, 'sha1')
    x509Dump = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    certFile = open(fName, 'w')
    certFile.write(x509Dump.decode())
    certFile.close()
    return x509Dump

# def getRsaKey(pKey):  <-- Use pKey.to_cryptography_key() instead.
#     keyDump = crypto.dump_privatekey(crypto.FILETYPE_PEM, pKey)
#     rsaKey = serialization.load_pem_private_key(keyDump, password=None,
#                 backend=default_backend())
#     return rsaKey
def writeRsaKey():
    pass

def readRsaKey():
    pass

def wirteRsaPubKey():
    pass

def readRsaPubKey():
    pass

def getHash(message):
    hasher = hashes.Hash(hashes.SHA256(), default_backend())
    for index in range(0, len(message), 80):
        hasher.update(message[index:index+80])
    hDigest = hasher.finalize()
    return hDigest

def pubEncrypt(pubKey, message):
    cMessage = pubKey.encrypt(message.encode(),
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(), label=None))
    return cMessage

def priDecrypt(priKey, cMessage):
    message = priKey.decrypt(cMessage,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(), label=None))
    return message

def encrypt(key, iv, bMessage):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    tail = 16 - (len(bMessage) % 16)
    #print(tail)
    plain = bMessage + bytes(tail)
    #print(plain)

    cMessage = encryptor.update(plain) + encryptor.finalize()
    return cMessage

def decrypt(key, iv, cMessage):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    return decryptor.update(cMessage) + decryptor.finalize()
