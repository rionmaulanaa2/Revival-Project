# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/rpcdecorator.py
from __future__ import absolute_import
from six.moves import range
from ..mobilelog.LogManager import LogManager
from ..common.RpcMethodArgs import RpcMethodArg, ConvertError, Avatar, MailBox, ClientInfo, GateMailBox, Response
from ..common.EntityManager import EntityManager
from ..common.FilterMessageBroker import FilterMessageBroker
from ..simplerpc.rpc_code import RPC_CODE
CLIENT_ONLY = 0
SERVER_ONLY = 1
CLIENT_SERVER = 2
CLIENT_STUB = 3
_logger = LogManager.get_logger('server.RpcMethod')

class RpcMethod(object):

    def __init__(self, func, rpctype, argtypes, pub):
        super(RpcMethod, self).__init__()
        self._has_response = False
        self.func = func
        self.rpctype = rpctype
        self.argtypes = tuple(argtypes)
        self.pub = pub
        self._check_index()

    def _check_index(self):
        placeholder_index, response_index = (-1, -1)
        for index in range(len(self.argtypes)):
            argtype = self.argtypes[index]
            if isinstance(argtype, Avatar) or type(argtype) in (MailBox, ClientInfo, GateMailBox):
                placeholder_index = index
            if isinstance(argtype, Response) or type(argtype) is Response:
                response_index = index

        if response_index > -1:
            self._has_response = True
        if response_index > 1 or placeholder_index > 0:
            raise Exception('argtype index error')

    def get_placeholder(self, argtype, placeholder):
        if isinstance(argtype, Avatar):
            avatar = EntityManager.getentity(placeholder)
            return avatar
        else:
            if type(argtype) in (MailBox, ClientInfo, GateMailBox):
                return placeholder
            return None

    def call(self, entity, placeholder, parameters):
        if not self.argtypes:
            return self.func(entity)
        else:
            if self._has_response is not isinstance(placeholder, tuple):
                if self._has_response:
                    raise Exception('%s need a response, check you call define' % self.func)
                else:
                    placeholder[0].send_response(code=RPC_CODE.NOT_RESPONSE, error='%s do not have response define' % self.func.__name__)
                    raise Exception('%s do not have response define, check your caller or %s define' % (self.func, self.func))
            if isinstance(parameters, dict):
                auto_parameters = parameters.get('_')
                if auto_parameters:
                    parameters = auto_parameters
                return self.call_with_key(entity, placeholder, parameters)
            return self.call_without_key(entity, placeholder, parameters)

    def call_without_key(self, entity, placeholder, parameters):
        response = None
        if isinstance(placeholder, tuple):
            response = placeholder[0]
            placeholder = placeholder[1]
        args = []
        argtypes = self.argtypes
        holder = self.get_placeholder(argtypes[0], placeholder)
        if holder:
            args.append(holder)
            argtypes = argtypes[1:]
        if response:
            argtypes = argtypes[1:]
            args.append(response)
        for index in range(len(argtypes)):
            argtype = argtypes[index]
            try:
                arg = parameters[index]
            except IndexError:
                _logger.warn('call_without_key: parameter %s not found in RPC call %s, using default value', argtype.getname(), self.func.__name__)
                arg = argtype.default_val()

            try:
                arg = argtype.convert(arg)
            except ConvertError as e:
                _logger.error("call_without_key: parameter %s can't convert input %s for RPC call %s exception %s", argtype.getname(), str(arg), self.func.__name__, str(e))
                return

            args.append(arg)

        return self.func(entity, *args)

    def call_with_key(self, entity, placeholder, parameters):
        response = None
        if isinstance(placeholder, tuple):
            response = placeholder[0]
            placeholder = placeholder[1]
        args = []
        argtypes = self.argtypes
        holder = self.get_placeholder(argtypes[0], placeholder)
        if holder:
            args.append(holder)
            argtypes = argtypes[1:]
        if response:
            argtypes = argtypes[1:]
            args.append(response)
        for argtype in argtypes:
            try:
                arg = parameters[argtype.getname()]
            except KeyError:
                _logger.warn('call_with_key: parameter %s not found in RPC call %s, using default value', argtype.getname(), self.func.__name__)
                arg = argtype.default_val()

            try:
                arg = argtype.convert(arg)
            except ConvertError as e:
                _logger.error("call_with_key: parameter %s can't convert input %s for RPC call %s exception %s", argtype.getname(), str(arg), self.func.__name__, str(e))
                return

            args.append(arg)

        return self.func(entity, *args)


def rpc_method(rpctype, argtypes=(), pub=True):
    for argtype in argtypes:
        pass

    def _rpc_method(func):
        rpcmethod = RpcMethod(func, rpctype, argtypes, pub)
        call_func = rpcmethod.call

        def call_rpc_method_CLIENT_STUB(self, *args):
            fun_for_reload = func
            return call_func(self, None, *args)

        def call_rpc_method_Others(self, *args):
            fun_for_reload = func
            return call_func(self, *args)

        if rpctype == CLIENT_STUB:
            call_rpc_method = call_rpc_method_CLIENT_STUB
        else:
            call_rpc_method = call_rpc_method_Others
        call_rpc_method.rpcmethod = rpcmethod
        return call_rpc_method

    return _rpc_method


def expose_to_client(method):
    try:
        rpctype = method.rpcmethod.rpctype
        if rpctype == CLIENT_ONLY or rpctype == CLIENT_SERVER:
            return True
        return False
    except AttributeError:
        return False


def expose_to_server(method):
    try:
        rpctype = method.rpcmethod.rpctype
        if rpctype == SERVER_ONLY or rpctype == CLIENT_SERVER:
            return True
        return False
    except AttributeError:
        return False


def filter_method(func):
    FilterMessageBroker.register(func.__name__, func)
    return func