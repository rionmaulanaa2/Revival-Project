# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/simplerpc.py
import time
import traceback
import sys
import logging.handlers
from .jsonrpc import JSONRPCResponseManager, Dispatcher
from .jsonrpc.jsonrpc import JSONRPC20Response
from .jsonrpc.exceptions import JSONRPCServerError, JSONRPCParseError
ENCODING = None
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    import asyncio
logger = logging.getLogger('simplerpc')
logger.setLevel(logging.INFO)

class Callback(object):
    WAITING, RESULT, ERROR, CANCELED = (0, 1, 2, 3)

    def __init__(self, rid, func, agent=None):
        super(Callback, self).__init__()
        self.func = func
        self.rid = rid
        self.agent = agent
        self.result_callback = None
        self.error_callback = None
        self.timeout_threshold = 0
        self.timeout_callback = None
        self.start_time = time.time()
        self.status = self.WAITING
        self.result = None
        self.error = None
        return

    def on_result(self, func):
        if not callable(func):
            raise RuntimeError('%s should be callable' % func)
        self.result_callback = func
        if self.status == self.RESULT:
            try:
                self.result_callback(self.result)
            except:
                traceback.print_exc()

        return self

    def on_error(self, func):
        if not callable(func):
            raise RuntimeError('%s should be callable' % func)
        self.error_callback = func
        if self.status == self.ERROR:
            try:
                self.error_callback(self.error)
            except:
                traceback.print_exc()

        return self

    def timeout(self, seconds):
        self.timeout_threshold = seconds
        return self

    def on_timeout(self, cb):
        if not callable(cb):
            raise RuntimeError('%s should be callable' % cb)
        self.timeout_callback = cb
        return self

    def rpc_result(self, data):
        self.result = data
        if callable(self.result_callback):
            try:
                self.result_callback(data)
            except Exception:
                traceback.print_exc()

        self.status = self.RESULT

    def rpc_error(self, data):
        self.error = data
        if callable(self.error_callback):
            try:
                self.error_callback(data)
            except Exception:
                traceback.print_exc()

        self.status = self.ERROR

    def cancel(self):
        self.result_callback = None
        self.error_callback = None
        self.status = self.CANCELED
        return

    def wait(self):
        while True:
            if self.status == self.WAITING:
                if self.agent:
                    self.agent.update()
                time.sleep(0.05)
            else:
                break

        return (
         self.result, self.error)


class AsyncResponse(object):

    def __init__(self):
        self.conn = None
        self.rid = None
        self.serializer = None
        return

    def setup(self, conn, rid, serializer=None):
        self.conn = conn
        self.rid = rid
        if serializer is None:
            from .serializers.json_serializer import JsonSerializer
            serializer = JsonSerializer
        self.serializer = serializer
        return

    def result(self, result):
        ret = JSONRPC20Response(_id=self.rid, result=result)
        self.conn.send(self.serializer.dump(ret.data))

    def error(self, error):
        data = {'type': error.__class__.__name__,
           'args': error.args,
           'message': str(error)
           }
        ret = JSONRPC20Response(_id=self.rid, error=JSONRPCServerError(data=data)._data)
        self.conn.send(self.serializer.dump(ret.data))


class Context(object):

    def __init__(self, rid, method, params):
        self.rid = rid
        self.method = method
        self.params = params

    def call_peer(self, func, *args, **kwargs):
        raise NotImplementedError

    def peer_info(self):
        raise NotImplementedError


class RpcAgent(object):
    REQUEST = 0
    RESPONSE = 1

    def __init__(self, eventMode=False, protocol='json'):
        self._id = 0
        self._callbacks = {}
        self.eventMode = eventMode
        self._debug = True
        self.dispatcher = Dispatcher()
        self._inputSerializer = None
        if protocol == 'msgpack':
            from .serializers.msgpack_serializer import MsgPackSerializer
            self._outputSerializer = MsgPackSerializer
        else:
            from .serializers.json_serializer import JsonSerializer
            self._outputSerializer = JsonSerializer
        self._postCallInterceptors = []
        return

    def set_debug(self, debug=True):
        self._debug = debug

    def add_post_call_interceptor(self, interceptor):
        self._postCallInterceptors.insert(0, interceptor)

    def add_method(self, func, name=None):
        self.dispatcher.add_method(func, name)

    def call(self, *args, **kwargs):
        raise NotImplementedError

    def format_request(self, func, *args, **kwargs):
        rid = self._id
        self._id += 1
        payload = {'method': func,
           'params': args or kwargs,
           'jsonrpc': '2.0',
           'id': rid
           }
        req = self._encode_message(payload)
        cb = Callback(rid, func, self)
        self._callbacks[rid] = cb
        return (
         req, cb)

    def handle_transport_message(self, conn, msg):
        raise NotImplementedError

    def handle_request(self, req, context):
        res = JSONRPCResponseManager.handle(req, context, self.dispatcher).data
        return res

    def create_context(self, conn, data):
        return Context(data['id'], data['method'], data['params'])

    def _encode_message(self, data):
        return self._outputSerializer.dump(data)

    def _decode_message(self, msg):
        if self._inputSerializer is None:
            try:
                from .serializers.json_serializer import JsonSerializer
                JsonSerializer.load(msg)
                self._inputSerializer = JsonSerializer
            except:
                try:
                    from .serializers.msgpack_serializer import MsgPackSerializer
                except ImportError:
                    logger.fatal('Unable to decode msgpack-packed data because msgpack is not installed.')
                    raise
                else:
                    self._inputSerializer = MsgPackSerializer

        return self._inputSerializer.load(msg)

    def handle_message(self, msg, conn):
        try:
            data = self._decode_message(msg)
        except:
            traceback.print_exc()
            ret = JSONRPC20Response(error=JSONRPCParseError()._data)
            conn.send(self._encode_message(ret.data))
            return

        if self._debug:
            logger.debug('handle message: %s', data)
        if 'method' in data:
            message_type = self.REQUEST
            context = self.create_context(conn, data)
            result = self.handle_request(data, context)
            _result = result.get('result')
            if IS_PY3 and (asyncio.iscoroutine(_result) or asyncio.isfuture(_result)):
                _res = asyncio.ensure_future(_result)
                asyncResponse = AsyncResponse()
                asyncResponse.setup(conn, result['id'], self._outputSerializer)
                _res.add_done_callback(lambda f: asyncResponse.result(f.result()))
            elif isinstance(result.get('result'), AsyncResponse):
                result['result'].setup(conn, result['id'], self._outputSerializer)
            else:
                self.handle_rpc_result(data, result, conn)
            if result.get('error'):
                self.show_rpc_error(result)
        else:
            message_type = self.RESPONSE
            result = None
            callback = self._callbacks.pop(data['id'], None)
            if callback:
                if 'result' in data:
                    callback.rpc_result(data['result'])
                elif 'error' in data:
                    callback.rpc_error(data['error'])
        return (
         message_type, result)

    def show_rpc_error(self, result):
        if 'error' not in result:
            return
        error = result['error']
        errorData = error.get('data', {})
        if error['code'] == -32601:
            logger.warning('RPC not found: %s' % errorData['method'])
        elif errorData.get('type') == 'NotImplementedError':
            logger.warning('[RPC ERROR] RPC not implemented: %s' % errorData['method'])
        else:
            logger.error('[RPC ERROR] Exception occurs when calling method %s, args: %s, kwargs: %s' % (
             errorData['method'], errorData['request_args'], errorData['request_kwargs']))
            logger.error(errorData.get('traceback'))

    def handle_rpc_result(self, data, result, conn):
        for interceptor in self._postCallInterceptors:
            if interceptor(self, result, conn):
                if 'result' in result:
                    result['result'] = ''
                break

        try:
            msg = self._encode_message(result)
        except:
            logger.warning('Unable to dump result object: %s, method=%s' % (result, data['method']))
        else:
            conn.send(msg)

    def update_timeout(self):
        now = time.time()
        for cid in list(self._callbacks.keys()):
            callback = self._callbacks[cid]
            if now - callback.start_time > callback.timeout_threshold > 0:
                del self._callbacks[cid]
                if callback.timeout_callback:
                    callback.timeout_callback()

    def update(self):
        self.update_timeout()

    def run(self, backend=False):

        def _run():
            while True:
                self.update()
                time.sleep(0.1)

        if backend:
            from threading import Thread
            t = Thread(target=_run, name='simplerpc_update')
            t.daemon = True
            t.start()
        else:
            _run()

    def console_run(self, local_dict=None):
        self.run(backend=True)
        from code import InteractiveInterpreter
        i = InteractiveInterpreter(local_dict)
        while True:
            prompt = '>>>'
            try:
                line = raw_input(prompt)
            except EOFError:
                print 'closing..'
                return

            i.runcode(line)