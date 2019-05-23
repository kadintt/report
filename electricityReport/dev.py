#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import AES
import os


def ByteToHex(bins):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join(["%02X" % x for x in bins]).strip()


'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数. ZeroPadding

'''
    在PKCS5Padding中，明确定义Block的大小是8位
    而在PKCS7Padding定义中，对于块的大小是不确定的，可以在1-255之间
    PKCS #7 填充字符串由一个字节序列组成，每个字节填充该字节序列的长度。
    假定块长度为 8，数据长度为 9，
    数据： FF FF FF FF FF FF FF FF FF
    PKCS7 填充： FF FF FF FF FF FF FF FF FF 01 01 01 01 01 01 01   ?应该是填充01

    python3:填充bytes(这个说法不对,AES的参数是字符串,不是byte)
    length = 16 - (len(data) % 16)
    data += bytes([length])*length

    python2:填充字符串
    length = 16 - (len(data) % 16)
    data += chr(length)*length

    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]
'''


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


def ZeroPadding(value, bs):
    while len(value) % bs != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 对于python,不需要zerounpadding?  去掉尾部的\0

def PKCS7Padding(value, bs):
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7
    return str.encode(pad(value))  # 返回bytes


def PKCS7UnPadding(value):
    # value = value[:-value[-1]]
    unpad = lambda s: s[0:-ord(s[-1])]  # 获得数据的长度,截取
    return unpad(value)


# 加密方法
def encrypt_oracle(text):
    # 秘钥
    # key = '123456'
    key = 'sycmsycmsycmsycm'
    # 待加密文本
    # text = 'abc123def456'
    iv = add_to_16("mcysmcysmcysmcys")  # 多了个iv
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)
    bs = AES.block_size
    pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7

    # 先进行aes加密
    # encrypt_aes = aes.encrypt(add_to_16(text))
    # Zeropadding
    # encrypt_aes = aes.encrypt(add_to_16(text))
    # Pkcs7 padding
    encrypt_aes = aes.encrypt(str.encode(pad2(text)))
    # 转为hex
    print(ByteToHex(encrypt_aes))  # 转为字符串 71462668992DB7B3FE76ABFE22376CF6
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    print(encrypted_text)  # zeropadding:   UR5c4C1iW5mIdxrv5rxo4w==     Pkcs7/Pkcs7: jE7BUAKWpdJWb2ulcFWd/g==
    # 和js的 结果相同 http://tool.chacuo.net/cryptaes
    return encrypted_text


# 解密方法
def decrypt_oralce(text):
    # 秘钥
    # key = '123456'
    key = 'sycmsycmsycmsycm'
    # 密文
    # text = 'qR/TQk4INsWeXdMSbCDDdA=='
    # text = 'cUYmaJktt7P+dqv+Ijds9g=='
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_CBC, add_to_16("mcysmcysmcysmcys"))
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str
    unpad = lambda s: s[0:-ord(s[-1])]
    # PADDING = '\0'
    # print decrypted_text.rstrip(PADDING)  #zeropadding只见诶去掉结尾\0
    print(unpad(decrypted_text))

    return unpad(decrypted_text)


