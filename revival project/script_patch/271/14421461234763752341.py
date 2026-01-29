# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileUtil.py
from __future__ import absolute_import
from six.moves import zip
from six.moves import range
import hashlib
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import six
if six.PY2:
    from six.moves.urllib.parse import urlparse
else:
    from urllib.parse import urlparse
from ..Utils.NileCallbackWeakRef import NileCallbackWeakRef

class NileUtil(object):

    @staticmethod
    def UrlEncode(content):
        return six.moves.urllib.parse.quote(content)

    @staticmethod
    def ParseUrl(url):
        return urlparse(url)

    @staticmethod
    def GetTraceback():
        return NileCallbackWeakRef.GetTraceback()

    @staticmethod
    def CalculateSign(param_dict, sb, deep, token):
        combineSign = NileUtil.CombineSign(param_dict, sb, deep) + token
        combineSign = six.ensure_binary(combineSign)
        m = hashlib.md5()
        m.update(combineSign)
        sign = m.hexdigest().upper()
        return sign

    @staticmethod
    def CombineSign(param_dict, sb, deep):
        if type(param_dict) == dict:
            sorted_param = sorted(param_dict)
            for index in range(len(sorted_param)):
                if deep < 2 and (type(param_dict[sorted_param[index]]) == dict or type(param_dict[sorted_param[index]]) == list):
                    sb = sb + sorted_param[index]
                    sb = NileUtil.CombineSign(param_dict[sorted_param[index]], sb, deep + 1)
                elif type(param_dict[sorted_param[index]]) == dict or type(param_dict[sorted_param[index]]) == list:
                    continue
                    sb = sb + sorted_param[index] + str(param_dict[sorted_param[index]])

        if type(param_dict) == list:
            for index in range(len(param_dict)):
                if deep < 2 and (type(param_dict[index]) == dict or type(param_dict[index]) == list):
                    sb = NileUtil.CombineSign(param_dict[index], sb, deep + 1)
                elif type(param_dict[index]) == dict or type(param_dict[index]) == list:
                    continue
                    sb = sb + str(param_dict[index])

        return sb

    @staticmethod
    def StrToBool(string):
        if string is None:
            return False
        else:
            if string.lower() == 'true':
                return True
            return False


class Singleton(type):
    CLASS_METHOD_IS_INITIALIZED = classmethod(lambda klass: klass in Singleton._instances)
    CLASS_METHOD_FINIALIZE = classmethod(lambda klass: Singleton._instances.pop(klass, None))
    _instances = {}

    def __new__(cls, name, bases, attrs):
        attrs.setdefault('is_initialized', classmethod(lambda klass: klass in Singleton._instances))
        attrs.setdefault('finialize', classmethod(lambda klass: Singleton._instances.pop(klass, None)))
        classtype = type.__new__(cls, name, bases, attrs)
        return classtype

    def __call__(klass, *args, **kwargs):
        try:
            return Singleton._instances[klass]
        except KeyError:
            instance = Singleton._instances[klass] = super(Singleton, klass).__call__(*args, **kwargs)
            return instance


def enum(*sequential, **named):
    enums = dict(list(zip(sequential, list(range(len(sequential))))), **named)
    return type('Enum', (), enums)


def clamp(val, low, high):
    return min(max(low, val), high)