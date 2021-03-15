import okKey

# create my asymmetric keys
mykey = okKey.getKey()
# write rsa pri key at file
okKey.writeKey("myprikey.pem", mykey)
# write rsa pub key at file
okKey.writePubKey("mypubkey.pem", mykey)

# create your asymmetric keys
# create my asymmetric keys
yrkey = okKey.getKey()
# write rsa pri key at file
okKey.writeKey("yrprikey.pem", yrkey)
# write rsa pub key at file
okKey.writePubKey("yrpubkey.pem", yrkey)


alicekey = okKey.getKey()
# write rsa pri key at file
okKey.writeKey("aliceprikey.pem", alicekey)
# write rsa pub key at file
okKey.writePubKey("alicepubkey.pem", alicekey)

