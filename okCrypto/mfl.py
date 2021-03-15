import copy
#import mfl

def print_string_byte(getstring):
    print("The original string: " + str(getstring))
    
def string_to_byte(getstring):
    conv_byte = bytearray()
    conv_byte.extend(getstring.encode())
    return conv_byte

def print_byte(getstring):
    getbyte = string_to_byte(getstring)
    print("The converted byte: " + str(getbyte))

def split_even_odd(getbyte):
    cb1 = bytearray()
    cb2 = bytearray()
    
    for i in range(len(getbyte)):
        if i % 2 == 0:
            cb1.append(getbyte[i])
        else:
            cb2.append(getbyte[i])

    return cb1, cb2

def print_splited(getbyte):
    cb1, cb2 = split_even_odd(getbyte)
    print(cb1)
    print(cb2)
    return cb1, cb2

def mergeToString(cb1, cb2):
    #cb1, cb2 = split_even_odd(getbyte)
    mergetwobytearray = bytearray()
   
    j = 0
    for i in range(len(cb1+cb2)):
        if i % 2 == 0:
            mergetwobytearray.append(cb1[j])
        else:
            mergetwobytearray.append(cb2[j])
            j = j + 1

    return mergetwobytearray

def print_merged_string(cb1, cb2):
    mgstring = mergeToString(cb1, cb2)
    print(mgstring)
    print("Bytearray to string: " + mgstring.decode())

def bytearray_to_byte(getbyte):
    cb1, cb2 = split_even_odd(getbyte)
    divb1 = bytes(cb1)
    divb2 = bytes(cb2)
    return divb1, divb2

#teststr = "hello world byte test"
#print_string_byte(teststr)

#print_byte(teststr)

#testbyte = string_to_byte(teststr)
#cb1, cb2 = print_splited(testbyte)

#print(mergeToString(cb1, cb2))
