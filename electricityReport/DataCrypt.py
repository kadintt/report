#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
from Crypto.Cipher import AES

class WXBizDataCrypt:
    def __init__(self, sessionKey):

        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))


        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
