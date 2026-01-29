# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/SimpleHttpClient2.py
from __future__ import absolute_import
from __future__ import print_function
import six
import functools
from ..mobilelog.LogManager import LogManager
import six_ex.moves.cStringIO
import six.moves.http_client
from ..mobilerpc.HttpBase import HttpRequest, HttpReply
from ..common.mobilecommon import asiocore
_logger = LogManager.get_logger('mobilerpc.SimpleHttpClient2')

class SimpleAsyncHTTPClient2(object):

    def __init__(self, max_clients=10, max_buffer_size=10240, etcd_use=False):
        super(SimpleAsyncHTTPClient2, self).__init__()
        self.max_clients = max_clients
        self.active = {}
        self.max_buffer_size = max_buffer_size
        self._etcd_use = etcd_use
        self.this_time_error = None
        _logger.info('__init__: max_clients %d, max_buffer_size %d ', max_clients, max_buffer_size)
        return

    def http_request(self, request, timeout, callback):
        func_code = callback.__code__
        callback_code = (func_code.co_filename, func_code.co_firstlineno)
        self._process_request(request, timeout, callback, callback_code)
        if len(self.active) > self.max_clients:
            _logger.warn('[HTTPClient] max_clients(%s) limit reached, %d active http request, callback: %s', self.max_clients, len(self.active), callback_code)

    def _process_request(self, request, timeout, callback, callback_code):
        key = object()
        self.active[key] = callback
        wrapper_callback = functools.partial(self._callback, key, request)
        setattr(wrapper_callback, 'etcd_use', self._etcd_use)
        _HTTPConnection(request, timeout, wrapper_callback, self.max_buffer_size, callback_code)

    def _callback(self, key, request, err, reply):
        if key in self.active:
            callback = self.active[key]
            del self.active[key]
            self.this_time_error = err
            callback(request, reply)


class HTTPClient(asiocore.http_client_proxy):

    def __init__(self, host, port, method, path, headers, timeout, usessl, content, keep_alive, handler, handler_code=None):
        super(HTTPClient, self).__init__(host, port, method, path, headers, timeout, usessl, content, keep_alive)
        self.handler = handler
        self.handler_code = handler_code

    def callback(self, err, headers, content):
        if not callable(self.handler):
            return
        else:
            if err == asiocore.http_error_types.http_no_error:
                msg = six.moves.http_client.HTTPMessage(six_ex.moves.cStringIO.StringIO())
                msg.status = ''
                msg.dict = headers
                reply = HttpReply(msg, content)
                self.handler(err, reply)
            else:
                if not (err is asiocore.http_error_types.http_err_timeout and getattr(self.handler, 'etcd_use', False)):
                    _logger.error('[HTTPClient][Error %s] - callback : %s', err, self.handler_code)
                if getattr(self.handler, 'etcd_use', False):
                    msg = six.moves.http_client.HTTPMessage(six_ex.moves.cStringIO.StringIO())
                    msg.status = ''
                    msg.dict = headers
                    reply = HttpReply(msg, content)
                    self.handler(err, reply)
                else:
                    self.handler(err, None)
            return


class _HTTPConnection(object):
    HTTP_PORT = 80
    HTTPS_PORT = 443

    def __init__(self, request, timeout, wrapper_callback, max_buffer_size, callback_code=None):
        super(_HTTPConnection, self).__init__()
        self.callback = wrapper_callback
        self.default_port = self.HTTPS_PORT if request.usessl else self.HTTP_PORT
        self.headers = ''
        self._set_hostport(request.host, request.port)
        self.putheaders(request.headers)
        body = request.body if request.body is not None else ''
        self.http_client = HTTPClient(self.host, self.port, request.method, request.url, self.headers, timeout, request.usessl, body, False, self.callback, callback_code)
        self.http_client.start()
        return

    def putheaders(self, headers):
        buf = []
        for hdr, value in six.iteritems(headers):
            hdr = '%s: %s' % (hdr, value)
            buf.append(hdr)

        self.headers = '\r\n'.join(buf)

    def _set_hostport(self, host, port):
        if port is None:
            i = host.rfind(':')
            j = host.rfind(']')
            if i > j:
                try:
                    port = int(host[i + 1:])
                except ValueError:
                    if host[i + 1:] == '':
                        port = self.default_port
                    else:
                        raise six.moves.http_client.InvalidURL("nonnumeric port: '%s'" % host[i + 1:])

                host = host[:i]
            else:
                port = self.default_port
            if host and host[0] == '[' and host[-1] == ']':
                host = host[1:-1]
        self.host = host
        self.port = port
        return


if __name__ == '__main__':

    def callback(request, reply):
        print('entering http callback')
        if reply != None:
            print(request, reply, reply.body)
        else:
            print('failed to fetch the request', str(request))
        return


    asiocore.start(True)
    client = SimpleAsyncHTTPClient2(10)
    request = HttpRequest('reg.163.com', 'GET', '/services/checkMobToken?userip=10.12.1.2&token=7287c60ead2a841f7c97bfb08bfc2aac&id=9BCE35B69832E767E085421C3D22691AE96E0873A4DD583B9D89DA079D1D7F92', usessl=False)
    client.http_request(request, 1, callback)
    import time
    while 1:
        asiocore.poll()
        time.sleep(0.1)