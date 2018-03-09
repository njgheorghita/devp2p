def encode_rlp(value):
    if isinstance(value,str):
        if len(value) is 1 and ord(value) < 0x80: 
            return value
        else: 
            return list(encode_length(len(value), 0x80) + value)
    elif isinstance(value,list):
        encoded_array = [encode_rlp(item) for item in value] 
        encoded_flat = [item for sublist in encoded_array for item in sublist]
        length = list(encode_length(len(encoded_flat), 0xc0))
        return length + encoded_flat
    else:
        raise TypeError("Value must be string or list type.")


def encode_length(length, offset):
    if length < 56:
         return chr(length + offset)
    elif length < 256**8:
         binary_length = to_binary(length)
         return chr(len(binary_length) + offset + 55) + binary_length
    else:
         raise TypeError("Value too long")


def decode_rlp(value):
    if len(value) is 0: return

    (offset, data_length, type) = decode_length(value)
    if type is str:
        output = substr(value, offset, data_length)
        return ''.join(output)
    elif type is list:
        output = substr(value, offset, data_length)
        return decoded_string_to_array(''.join(output))


def decode_length(value):
    length = len(value)
    if length is 0:
        raise TypeError("Value is null")

    prefix = ord(value[0])
    
    # string:
    # prefix in [0x00.. 0x0f]
    if prefix <= 0x7f:
        return (0, 1, str)
    # string:
    # prefix in [0x80 .. 0xb7]
    # string_length = prefix - 0x80
    elif prefix <= 0xb7 and length > prefix - 0x80:
        string_length = prefix - 0x80
        return (1, string_length, str)
    # string:
    # prefix in [0xb8 .. 0xbf]
    # string_length = prefix - 0xb7 (follows prefix)
    # string follows second byte
    elif prefix <= 0xbf and length > prefix - 0xb7 and length > prefix - 0xb7 + to_integer(substr(value, 1, prefix - 0xb7)):
        length_of_string_length = prefix - 0xb7
        string_length = to_integer(substr(value, 1, length_of_string_length))
        return (1 + length_of_string_length, string_length, str)
    # list:
    # prefix in [0xc0 .. 0xf7]
    # payload length: prefix - 0xc0 (follows prefix)
    # payload follows second byte
    elif prefix <= 0xf7 and length > prefix - 0xc0:
        list_length = prefix - 0xc0;
        return (1, list_length, list)
    # list:
    # prefix in [0xf8 .. 0xff]
    # payload length: prefix - 0xf7 (follows prefix)
    # payload follows second byte
    elif prefix <= 0xff and length > prefix - 0xf7 and length > prefix - 0xf7 + to_integer(substr(value, 1, prefix - 0xf7)):
        length_of_list_length = prefix - 0xf7
        list_length = to_integer(substr(value, 1, length_of_list_length))
        return (1 + length_of_list_length, list_length, list)
    else:
        raise TypeError("Value doesn't conform to RLP encoding.")


### UTILS

def to_integer(b):
    length = len(b)
    if length is 0:
        raise TypeError("Value is none.")
    elif length is 1:
        return ord(b[0])
    else:
        return ord(substr(b, -1)) + to_integer(substr(b, 0, -1)) * 256


def substr(string, beginning, length=0):
    return string[beginning:(beginning + length)]


def decoded_string_to_array(string):
    return string.split('\x83')[1:]


def to_binary(x):
    if x is 0:
        return ''
    else: 
        return to_binary(int(x / 256)) + chr(x % 256)
