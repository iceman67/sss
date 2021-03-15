import os
import okKey
from OpenSSL import crypto

def test_getKey():
    testKey = okKey.getKey()
    if testKey.check():
        print(testKey)
        assert 1
    else:
        print("corrupted key consistency")
        assert 0

def test_rewriteKey():
    orgKey = okKey.getKey()
    orgKeyDump = okKey.writeKey("test.pem", orgKey)
    cpyKey = okKey.readKey("test.pem")
    assert crypto.dump_privatekey(crypto.FILETYPE_PEM, orgKey) \
        == crypto.dump_privatekey(crypto.FILETYPE_PEM, cpyKey)

def test_rewritePubKey():
    orgKey = okKey.getKey()
    orgKeyDump = okKey.writePubKey("test.pub", orgKey)
    cpyKey = okKey.readPubKey("test.pub")
    assert orgKeyDump == crypto.dump_publickey(crypto.FILETYPE_PEM, cpyKey)

def test_rewriteCert():
    key= okKey.getKey()
    orgCertDump = okKey.writeCert("test.cert", key)
    cpyCert = okKey.readCert("test.cert")
    assert orgCertDump == crypto.dump_certificate(crypto.FILETYPE_PEM, cpyCert)

def test_getHash():
    message = "This is a message with 한글 입니다"
    assert okKey.getHash(message.encode()) == \
        b'.\x9a\x1a\xc7\xeaZ\x14\xb3\xa1(DS\xdc\xa8*1\xe8E\x00Lo\x14\xda\x10_\xcd*L\xe63D\xc6'

def test_pubEncrypt(msg) -> bool:
#    key=okKey.getRsaKey(okKey.getKey())
    key = okKey.getKey().to_cryptography_key()
    pubKey = key.public_key()
    cMessage = okKey.pubEncrypt(pubKey, "My message")
    rMessage = okKey.priDecrypt(key, cMessage)
    assert rMessage.decode() == "My message"

def test_pubEncrypt_1(msg) -> str:
#    key=okKey.getRsaKey(okKey.getKey())
    key = okKey.getKey().to_cryptography_key()
    pubKey = key.public_key()
    cMessage = okKey.pubEncrypt(pubKey, msg)
    rMessage = okKey.priDecrypt(key, cMessage)
    return rMessage

def test_certRsaPubKey():
    key = okKey.getKey()
    rsaKey = key.to_cryptography_key()
    okKey.writePubKey("test.pub", key)
    pubKey = okKey.readPubKey("test.pub")
    rsaPubKey = pubKey.to_cryptography_key()

    # public key 로 암호화/private key로 복호화
    cMessage = okKey.pubEncrypt(rsaPubKey, "My message")
    rMessage = okKey.priDecrypt(rsaKey, cMessage)
    assert rMessage.decode() == "My message"

def test_cipherEncrypt():
    key = os.urandom(32)
    iv = os.urandom(16)
    message = "This is a test. 그리고 한글"
    ciphertext= okKey.encrypt(key, iv, message.encode())
    okKey.decrypt(key, iv, ciphertext).decode()

if __name__ == '__main__':
    # pubKey 암호/secKey 복호
    print(test_pubEncrypt_1('HelloWorld').decode())