import base64
import hashlib

#from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES as cryptoAES

BLOCK_SIZE = cryptoAES.block_size

key = "my_secret_key".encode()
__key__ = hashlib.sha256(key).digest()
print("key ={}".format(__key__))


# The Advanced Encryption Standard (AES) is a block cipher that iterate 10
# times a round transformation.


def encrypt(raw):
    BS = cryptoAES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(cryptoAES.block_size)
    cipher = cryptoAES.new(key= __key__, mode= cryptoAES.MODE_CFB,iv= iv)
    a= base64.b64encode(iv + cipher.encrypt(raw))
    IV = Random.new().read(BLOCK_SIZE)
    aes = cryptoAES.new(__key__, cryptoAES.MODE_CFB, IV)
    b = base64.b64encode(IV + aes.encrypt(a))
    return b

def decrypt(enc):
    passphrase = __key__
    encrypted = base64.b64decode(enc)
    IV = encrypted[:BLOCK_SIZE]
    aes = cryptoAES.new(passphrase, cryptoAES.MODE_CFB, IV)
    enc = aes.decrypt(encrypted[BLOCK_SIZE:])
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:cryptoAES.block_size]
    cipher = cryptoAES.new(__key__, cryptoAES.MODE_CFB, iv)
    b=  unpad(base64.b64decode(cipher.decrypt(enc[cryptoAES.block_size:])).decode('utf8'))
    return b

encrypted_data =encrypt("Hi Steven!!!!!")
print(encrypted_data)
print("=======")
decrypted_data = decrypt(encrypted_data)
print(decrypted_data)