# sss
I change it
* Prerequsite 
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install pycryptodomex
$ pip install pycryptodome
$ pip install pycrypto
$ pip install flask
$ pip install requests
$ cd okCrypto
$ git clone https://github.com/ergl/sss_py
```


* run encryption and description by  using symmetric key 
```
python enc_AES.py -i Halra.jpg -m keys.json
python dec_AES.py  -o  m1.jpg -m keys.json
```


## Following is underconstruction
* Flask WebApp
> send a key and receive a set of shares
```
python sss_web.py
python  sss_web_client.py

```
* Encryption 
> enc_AES_sss.py get shares to execute a function sss_gen_shares()  via sss_web
> IV is stored in  keys.json 

```
response = requests.get('http://localhost:5000/encrypt/' + key)
```

* Decrpption 

 > decc_AES_sss.py  get a key from **sss_restuct_shares()**  via sss_web 

```
url = 'http://localhost:5000/decrypt'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
```
> **decrypt_sss()** get IV from keys.json

key1 = b64decode(b64['key'])

```
$ python enc_AES_sss.py  -i Halra.jpg -m keys.json
key = b'\n\xc7\xbd(4,\x9fZ\x97q\x85<\xc0\xc5\xd9\x83'
1-7594442c5b46f11b373d95a2b336c6c4e54ac7feddacac587cbea2bf088278ecc5
2-41f1859ba78e9f6b04f0d07aa3e422310f9c6cff46c6f63f8b45da94e6d2da61d2
3-524487163b10a4f007c571e140d07c368bd593d9a677a2498f20044cc030ad12d
4-5f3910d10e883126c0ff5cbe0c6b28a96707c584df437b21daa81f398ebd796f9f
5-1016d673aa601533183b7af87b8b22881dc7403f07f07302e69e209d81ad47d396

$ python dec_AES.py  -o  m1.jpg -m keys.json
size of block = 16

```



---
* NEXT 
repeated_key_xor() 

