# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/SessionEncrypter.py
from __future__ import absolute_import
import os
from Crypto.Cipher import ARC4, PKCS1_OAEP
from Crypto.Hash import SHA
from Crypto import Random
from keyczar.keyczar import Crypter, Encrypter
from Crypto.PublicKey import RSA

class LoginKeyDecrypterNokeyczar(object):

    def __init__(self, loginkeypath=None, keycontent=None):
        super(LoginKeyDecrypterNokeyczar, self).__init__()
        if loginkeypath:
            keycontent = open(loginkeypath).read()
        key = RSA.importKey(keycontent)
        self.decypter = PKCS1_OAEP.new(key)

    def decrypt(self, encryptstr):
        return self.decypter.decrypt(encryptstr)


class LoginKeyEncrypterNokeyczar(object):

    def __init__(self, loginkeypath=None, keycontent=None):
        super(LoginKeyEncrypterNokeyczar, self).__init__()
        if loginkeypath:
            keycontent = open(loginkeypath).read()
        key = RSA.importKey(keycontent)
        self.encypter = PKCS1_OAEP.new(key)

    def encrypte(self, encryptstr):
        return self.encypter.encrypt(encryptstr)


class LoginKeyDecrypter(object):

    def __init__(self, loginkeypath):
        super(LoginKeyDecrypter, self).__init__()
        self.decypter = Crypter.Read(loginkeypath)

    def decrypt(self, encryptstr):
        return self.decypter.Decrypt(encryptstr, None)


class LoginKeyEncrypter(object):

    def __init__(self, loginkeypath):
        super(LoginKeyEncrypter, self).__init__()
        self.encypter = Encrypter.Read(loginkeypath)

    def encrypte(self, data):
        return self.encypter.Encrypt(data, None)


class ARC4Crypter(object):

    def __init__(self, key=None):
        super(ARC4Crypter, self).__init__()
        if key == None:
            seed = os.urandom(256)
            nonce = Random.new().read(256)
            key = SHA.new(seed + nonce).digest()
        self.cipher = ARC4.new(key)
        return

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_txt):
        return self.cipher.decrypt(encrypted_txt)