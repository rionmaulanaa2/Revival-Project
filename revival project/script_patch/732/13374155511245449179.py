# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/base.py
from .utils import JSONSerializable

class JSONRPCBaseRequest(JSONSerializable):

    def __init__(self, method=None, params=None, _id=None, is_notification=None):
        self.data = dict()
        self.method = method
        self.params = params
        self._id = _id
        self.is_notification = is_notification

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data should be dict')
        self._data = value

    @property
    def args(self):
        if isinstance(self.params, list):
            return tuple(self.params)
        return ()

    @property
    def kwargs(self):
        if isinstance(self.params, dict):
            return self.params
        return {}


class JSONRPCBaseResponse(JSONSerializable):

    def __init__(self, **kwargs):
        self.data = dict()
        try:
            self.result = kwargs['result']
        except KeyError:
            pass

        try:
            self.error = kwargs['error']
        except KeyError:
            pass

        self._id = kwargs.get('_id')
        if 'result' not in kwargs and 'error' not in kwargs:
            raise ValueError('Either result or error should be used')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data should be dict')
        self._data = value