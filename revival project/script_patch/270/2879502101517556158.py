# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/exceptions.py
import json
from .... import integer_types, string_types

class JSONRPCError(object):
    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    def __init__(self, code=None, message=None, data=None):
        self._data = dict()
        self.code = getattr(self.__class__, 'CODE', code)
        self.message = getattr(self.__class__, 'MESSAGE', message)
        self.data = data

    def __get_code(self):
        return self._data['code']

    def __set_code(self, value):
        if not isinstance(value, integer_types):
            raise ValueError('Error code should be integer')
        self._data['code'] = value

    code = property(__get_code, __set_code)

    def __get_message(self):
        return self._data['message']

    def __set_message(self, value):
        if not isinstance(value, string_types):
            raise ValueError('Error message should be string')
        self._data['message'] = value

    message = property(__get_message, __set_message)

    def __get_data(self):
        return self._data.get('data')

    def __set_data(self, value):
        if value is not None:
            self._data['data'] = value
        return

    data = property(__get_data, __set_data)

    @property
    def json(self):
        return self.serialize(self._data)


class JSONRPCParseError(JSONRPCError):
    CODE = -32700
    MESSAGE = 'Parse error'


class JSONRPCInvalidRequest(JSONRPCError):
    CODE = -32600
    MESSAGE = 'Invalid Request'


class JSONRPCMethodNotFound(JSONRPCError):
    CODE = -32601
    MESSAGE = 'Method not found'


class JSONRPCInvalidParams(JSONRPCError):
    CODE = -32602
    MESSAGE = 'Invalid params'


class JSONRPCInternalError(JSONRPCError):
    CODE = -32603
    MESSAGE = 'Internal error'


class JSONRPCServerError(JSONRPCError):
    CODE = -32000
    MESSAGE = 'Server error'


class JSONRPCException(Exception):
    pass


class JSONRPCInvalidRequestException(JSONRPCException):
    pass


class JSONRPCDispatchException(JSONRPCException):

    def __init__(self, code=None, message=None, data=None, *args, **kwargs):
        super(JSONRPCDispatchException, self).__init__(args, kwargs)
        self.error = JSONRPCError(code=code, data=data, message=message)


class JSONRPCRemoteException(JSONRPCException):

    def __init__(self, data, *args, **kwargs):
        super(JSONRPCRemoteException, self).__init__(args, kwargs)
        self.error = JSONRPCError(data['code'], data['message'], data['data'])

    def __repr__(self):
        return 'JSONRPCRemoteException(code=%s, message=%s, data=%s)' % (self.error.code, self.error.message, self.error.data)

    def __str__(self):
        data = self.error.data
        message = 'An error was caught during remote method call\nCode: %s\nMessage: %s\n\nDetails\nMethod: %s\nRequest args: %s\n' % (self.error.code, self.error.message, data.get('method', ''), data.get('request_args', ''))
        if 'traceback' in data:
            message += 'Remote exception call stack:\n%s\n' % data['traceback']
        else:
            message += 'Data: %s\n' % data
        return message