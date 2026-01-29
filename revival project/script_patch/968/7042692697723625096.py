# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/jsonrpc.py
import json
from .exceptions import JSONRPCError, JSONRPCInvalidRequestException
from .base import JSONRPCBaseRequest, JSONRPCBaseResponse
from .... import string_types, integer_types, PY2

class JSONRPCRequest(JSONRPCBaseRequest):
    JSONRPC_VERSION = '2.0'
    REQUIRED_FIELDS = {'jsonrpc', 'method'}
    POSSIBLE_FIELDS = {'jsonrpc', 'method', 'params', 'id'}

    @property
    def data(self):
        data = dict(((k, v) for k, v in self._data.items() if not (k == 'id' and self.is_notification)))
        data['jsonrpc'] = self.JSONRPC_VERSION
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data should be dict')
        self._data = value

    @property
    def method(self):
        return self._data.get('method')

    @method.setter
    def method(self, value):
        if not isinstance(value, string_types):
            raise ValueError('Method should be string')
        if value.startswith('rpc.'):
            raise ValueError('Method names that begin with the word rpc followed by a ' + 'period character (U+002E or ASCII 46) are reserved for ' + 'rpc-internal methods and extensions and MUST NOT be used ' + 'for anything else.')
        self._data['method'] = str(value)

    @property
    def params(self):
        return self._data.get('params')

    @params.setter
    def params(self, value):
        if value is not None and not isinstance(value, (list, tuple, dict)):
            raise ValueError('Incorrect params {0}'.format(value))
        value = list(value) if isinstance(value, tuple) else value
        if value is not None:
            self._data['params'] = value
        return

    @property
    def _id(self):
        return self._data.get('id')

    @_id.setter
    def _id(self, value):
        types = integer_types + (string_types,) if PY2 else (string_types, integer_types)
        if value is not None and not isinstance(value, types):
            raise ValueError('id should be string or integer')
        self._data['id'] = value
        return

    @classmethod
    def from_data(cls, data):
        is_batch = isinstance(data, list)
        if is_batch:
            data = data if 1 else [data]
            if not data:
                raise JSONRPCInvalidRequestException('[] value is not accepted')
            raise all((isinstance(d, dict) for d in data)) or JSONRPCInvalidRequestException('Each request should be an object (dict)')
        result = []
        for d in data:
            if not cls.REQUIRED_FIELDS <= set(d.keys()) <= cls.POSSIBLE_FIELDS:
                extra = set(d.keys()) - cls.POSSIBLE_FIELDS
                missed = cls.REQUIRED_FIELDS - set(d.keys())
                msg = 'Invalid request. Extra fields: {0}, Missed fields: {1}'
                raise JSONRPCInvalidRequestException(msg.format(extra, missed))
            try:
                result.append(JSONRPCRequest(method=d['method'], params=d.get('params'), _id=d.get('id'), is_notification='id' not in d))
            except ValueError as e:
                raise JSONRPCInvalidRequestException(str(e))

        if is_batch:
            return JSONRPC20BatchRequest(*result)
        return result[0]


class JSONRPC20BatchRequest(object):
    JSONRPC_VERSION = '2.0'

    def __init__(self, *requests):
        self.requests = requests

    @classmethod
    def from_json(cls, json_str):
        return JSONRPCRequest.from_data(json_str)

    @property
    def json(self):
        return json.dumps([ r.data for r in self.requests ])

    def __iter__(self):
        return iter(self.requests)


class JSONRPC20Response(JSONRPCBaseResponse):
    JSONRPC_VERSION = '2.0'

    @property
    def data(self):
        data = dict(((k, v) for k, v in self._data.items()))
        data['jsonrpc'] = self.JSONRPC_VERSION
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data should be dict')
        self._data = value

    @property
    def result(self):
        return self._data.get('result')

    @result.setter
    def result(self, value):
        if self.error:
            raise ValueError('Either result or error should be used')
        self._data['result'] = value

    @property
    def error(self):
        return self._data.get('error')

    @error.setter
    def error(self, value):
        self._data.pop('value', None)
        if value:
            self._data['error'] = value
            JSONRPCError(**value)
        return

    @property
    def _id(self):
        return self._data.get('id')

    @_id.setter
    def _id(self, value):
        types = integer_types + (string_types,) if PY2 else (string_types, integer_types)
        if value is not None and not isinstance(value, types):
            raise ValueError('id should be string or integer')
        self._data['id'] = value
        return


class JSONRPC20BatchResponse(object):
    JSONRPC_VERSION = '2.0'

    def __init__(self, *responses):
        self.responses = responses

    @property
    def data(self):
        return [ r.data for r in self.responses ]

    @property
    def json(self):
        return json.dumps(self.data)

    def __iter__(self):
        return iter(self.responses)