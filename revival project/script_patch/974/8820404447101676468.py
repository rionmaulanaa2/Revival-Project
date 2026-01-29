# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/RpcMethodArgs.py
from __future__ import absolute_import
import six_ex
import sys
import six
if six.PY2:
    try:
        sys.setdefaultencoding('utf-8')
    except:
        reload(sys)
        sys.setdefaultencoding('utf-8')

from .IdManager import IdManager

class ConvertError(Exception):
    pass


class RpcMethodArg(object):

    def __init__(self, name):
        super(RpcMethodArg, self).__init__()
        self.name = name

    def getname(self):
        return self.name

    def convert(self, _data):
        raise Exception('Not implemented!')

    def get_type(self):
        raise Exception('Not implemented!')

    def genametype(self):
        return '%s(%s)' % (self.getname(), self.get_type())

    def default_val(self):
        raise Exception('Not implemented!')

    def errstr(self, data):
        return '%s is not valid %s' % (data, self.get_type())

    def tostr(self, value):
        return str(value)

    def __str__(self):
        return self.genametype()


class NoLimit(object):

    def isvalide(self, _data):
        return True

    def __str__(self):
        return ''


class NumeralLimit(object):

    def __init__(self, min=None, max=None, range=None):
        super(NumeralLimit, self).__init__()
        self.min = min
        self.max = max
        self.range = range

    def isvalide(self, data):
        if self.min != None and data < self.min:
            return False
        else:
            if self.max != None and data > self.max:
                return False
            if self.range != None and data not in self.range:
                return False
            return True

    def __str__(self):
        extra = ''
        if self.min != None or self.max != None:
            extra = '['
            if self.min != None:
                extra += str(self.min)
            extra += '-'
            if self.max != None:
                extra += str(self.max)
            extra += ']'
        elif self.range != None:
            extra = repr(list(self.range)).replace(' ', '')
        return extra


class Int(RpcMethodArg):

    def __init__(self, name, min=None, max=None, range=None):
        super(Int, self).__init__(name)
        if min == None and max == None and range == None:
            self.limit = NoLimit()
        else:
            self.limit = NumeralLimit(min, max, range)
        return

    def convert(self, data):
        try:
            d = int(data)
        except:
            raise ConvertError(self.errstr(data))

        if self.limit and not self.limit.isvalide(data):
            raise ConvertError(self.errstr(data))
        return d

    def get_type(self):
        return 'Int' + str(self.limit)

    def default_val(self):
        return 0


class Long(RpcMethodArg):

    def __init__(self, name, min=None, max=None, range=None):
        super(Long, self).__init__(name)
        if min == None and max == None and range == None:
            self.limit = NoLimit()
        else:
            self.limit = NumeralLimit(min, max, range)
        return

    def convert(self, data):
        try:
            d = six_ex.long_type(data)
        except:
            raise ConvertError(self.errstr(data))

        if self.limit and not self.limit.isvalide(data):
            raise ConvertError(self.errstr(data))
        return d

    def get_type(self):
        return 'Long' + str(self.limit)

    def default_val(self):
        return 0


class Float(RpcMethodArg):

    def __init__(self, name, min=None, max=None, range=None):
        super(Float, self).__init__(name)
        if min == None and max == None and range == None:
            self.limit = NoLimit()
        else:
            self.limit = NumeralLimit(min, max, range)
        return

    def convert(self, data):
        try:
            d = float(data)
        except:
            raise ConvertError(self.errstr(data))

        if self.limit and not self.limit.isvalide(data):
            raise ConvertError(self.errstr(data))
        return d

    def get_type(self):
        return 'Float' + str(self.limit)

    def default_val(self):
        return 0


class Str(RpcMethodArg):

    def __init__(self, name):
        super(Str, self).__init__(name)

    def convert(self, data):
        if type(data) not in (six.text_type, six.binary_type):
            raise ConvertError(self.errstr(data))
        try:
            out_put_data = six.ensure_str(data)
        except Exception as e:
            out_put_data = data

        return out_put_data

    def get_type(self):
        return 'Str'

    def default_val(self):
        return ''


class BinData(RpcMethodArg):

    def __init__(self, name):
        super(BinData, self).__init__(name)

    def convert(self, data):
        return data

    def get_type(self):
        return 'BinData'

    def default_val(self):
        return ''


class Avatar(RpcMethodArg):

    def __init__(self, name='Avatar'):
        super(Avatar, self).__init__(name)


class MailBox(RpcMethodArg):

    def __init__(self, name='MailBox'):
        super(MailBox, self).__init__(name)


class Response(RpcMethodArg):

    def __init__(self, name='Response'):
        super(Response, self).__init__(name)


class ClientInfo(RpcMethodArg):

    def __init__(self, name='ClientInfo'):
        super(ClientInfo, self).__init__(name)


class GateMailBox(RpcMethodArg):

    def __init__(self, name='GateMailBox'):
        super(GateMailBox, self).__init__(name)


class List(RpcMethodArg):

    def __init__(self, name):
        super(List, self).__init__(name)

    def convert(self, data):
        if type(data) not in (list, tuple):
            raise ConvertError(self.errstr(data))
        return data

    def get_type(self):
        return 'List'

    def default_val(self):
        return []


class Tuple(RpcMethodArg):

    def __init__(self, name):
        super(Tuple, self).__init__(name)

    def convert(self, data):
        if type(data) not in (list, tuple):
            raise ConvertError(self.errstr(data))
        return tuple(data)

    def get_type(self):
        return 'Tuple'

    def default_val(self):
        return ()


class Dict(RpcMethodArg):

    def __init__(self, name):
        super(Dict, self).__init__(name)

    def convert(self, data):
        if type(data) != dict:
            raise ConvertError(self.errstr(data))
        return data

    def get_type(self):
        return 'Dict'

    def default_val(self):
        return {}


class Bool(RpcMethodArg):

    def __init__(self, name):
        super(Bool, self).__init__(name)

    def convert(self, data):
        if type(data) != bool:
            raise ConvertError(self.errstr(data))
        return data

    def get_type(self):
        return 'Bool'

    def default_val(self):
        return False


class Uuid(RpcMethodArg):

    def __init__(self, name):
        super(Uuid, self).__init__(name)

    def convert(self, data):
        if data is None or IdManager.is_id_type(data):
            return data
        else:
            if type(data) in (str, six.text_type):
                if type(data) == six.text_type:
                    data = str(data)
                try:
                    return IdManager.bytes2id(data)
                except:
                    return IdManager.str2id(data)

            raise ConvertError(self.errstr(data))
            return

    def get_type(self):
        return 'Uuid'

    def default_val(self):
        return None