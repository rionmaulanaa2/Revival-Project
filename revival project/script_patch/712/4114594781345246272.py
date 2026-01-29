# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/utils/ShortUUID.py
import binascii
import math
import os
import uuid as _uu

class ShortUUID(object):

    def __init__(self, alphabet=None):
        if alphabet is None:
            alphabet = list('23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
        self.set_alphabet(alphabet)
        return

    @property
    def _length(self):
        return int(math.ceil(math.log(340282366920938463463374607431768211456L, self._alpha_len)))

    def _num_to_string(self, number, pad_to_length=None):
        output = ''
        while number:
            number, digit = divmod(number, self._alpha_len)
            output += self._alphabet[digit]

        if pad_to_length:
            remainder = max(pad_to_length - len(output), 0)
            output = output + self._alphabet[0] * remainder
        return output

    def _string_to_int(self, string):
        number = 0
        for char in string[::-1]:
            number = number * self._alpha_len + self._alphabet.index(char)

        return number

    def encode(self, uuid, pad_length=None):
        if pad_length is None:
            pad_length = self._length
        return self._num_to_string(uuid.int, pad_to_length=pad_length)

    def decode(self, string):
        return _uu.UUID(int=self._string_to_int(string))

    def uuid(self, name=None, pad_length=None):
        if pad_length is None:
            pad_length = self._length
        if name is None:
            u = _uu.uuid4()
        elif 'http' not in name.lower():
            u = _uu.uuid5(_uu.NAMESPACE_DNS, name)
        else:
            u = _uu.uuid5(_uu.NAMESPACE_URL, name)
        return self.encode(u, pad_length)

    def random(self, length=None):
        if length is None:
            length = self._length
        random_num = int(binascii.b2a_hex(os.urandom(length)), 16)
        return self._num_to_string(random_num, pad_to_length=length)[:length]

    def get_alphabet(self):
        return ''.join(self._alphabet)

    def set_alphabet(self, alphabet):
        new_alphabet = list(sorted(set(alphabet)))
        if len(new_alphabet) > 1:
            self._alphabet = new_alphabet
            self._alpha_len = len(self._alphabet)
        else:
            raise ValueError('Alphabet with more than one unique symbols required.')

    def encoded_length(self, num_bytes=16):
        factor = math.log(256) / math.log(self._alpha_len)
        return int(math.ceil(factor * num_bytes))


_global_instance = ShortUUID()
encode = _global_instance.encode
decode = _global_instance.decode
uuid = _global_instance.uuid
random = _global_instance.random
get_alphabet = _global_instance.get_alphabet
set_alphabet = _global_instance.set_alphabet