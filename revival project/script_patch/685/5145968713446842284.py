# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/SimpleHttpClient.py
from __future__ import absolute_import
from __future__ import print_function
import re
import six.moves.collections_abc
import collections
import functools
from ..mobilelog.LogManager import LogManager
import asynchat
import socket
import six_ex.moves.cStringIO
import six.moves.http_client
from ..mobilerpc.HttpBase import HttpRequest, HttpReply
from ..common import Timer
import ssl
import select
import asyncore
_logger = LogManager.get_logger('mobilerpc.SimpleAsyncHTTPClient')

class SimpleAsyncHTTPClient(object):

    def __init__(self, max_clients=10, max_buffer_size=10240):
        super(SimpleAsyncHTTPClient, self).__init__()
        self.max_clients = max_clients
        self.queue = collections.deque()
        self.active = {}
        self.max_buffer_size = max_buffer_size
        _logger.info('__init__: max_clients %d, max_buffer_size %d ', max_clients, max_buffer_size)
        _logger.warn('SimpleHttpClient.SimpleAsyncHTTPClient is deprecated, please use SimpleHttpClient2.SimpleAsyncHTTPClient2 instead!')

    def http_request(self, request, timeout, callback):
        self.queue.append((request, timeout, callback))
        self._process_queue()
        if self.queue:
            _logger.debug('max_clients limit reached, request queued. %d active, %d queued requests.' % (
             len(self.active), len(self.queue)))

    def _process_queue(self):
        while self.queue and len(self.active) < self.max_clients:
            request, timeout, callback = self.queue.popleft()
            key = object()
            self.active[key] = callback
            wrapper_callback = functools.partial(self._callback, key, request)
            _HTTPConnection(request, timeout, wrapper_callback, self.max_buffer_size)

    def _callback(self, key, request, reply):
        try:
            if key in self.active:
                callback = self.active[key]
                del self.active[key]
                callback(request, reply)
        finally:
            self._process_queue()


class _HttpResponse(six.moves.http_client.HTTPResponse):

    def __init__(self, f, debuglevel=0, strict=0, method=None):
        self.fp = f
        self.debuglevel = debuglevel
        self.strict = strict
        self._method = method
        self.msg = None
        self.version = six.moves.http_client._UNKNOWN
        self.status = six.moves.http_client._UNKNOWN
        self.reason = six.moves.http_client._UNKNOWN
        self.chunked = six.moves.http_client._UNKNOWN
        self.chunk_left = six.moves.http_client._UNKNOWN
        self.length = six.moves.http_client._UNKNOWN
        self.will_close = six.moves.http_client._UNKNOWN
        return


class SSLConnector(asyncore.dispatcher):
    ST_INIT = 0
    ST_ESTABLISHED = 1
    ST_HANDSHAKE = 2

    def __init__(self, certfile, channel_interface_obj):
        print('SSLConnector.__init__')
        asyncore.dispatcher.__init__(self)
        self.status = SSLConnector.ST_INIT
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel_interface_obj = channel_interface_obj
        self.handshake_status = 0
        self.certfile = certfile

    def disconnect(self):
        self.close()
        self.status = SSLConnector.ST_INIT
        self.channel_interface_obj = None
        self.handshake_status = 0
        return

    def handle_connect(self):
        print('SSLConnector.handle_connect')
        self.socket = ssl.wrap_socket(self.socket, ca_certs=self.certfile, cert_reqs=ssl.CERT_NONE, do_handshake_on_connect=False)
        self.status = SSLConnector.ST_HANDSHAKE
        self._handshake()

    def _handshake(self):
        try:
            self.socket.do_handshake()
            self.handshake_status = 0
            self.on_handshaked()
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                self.handshake_status = ssl.SSL_ERROR_WANT_READ
            elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                self.handshake_status = ssl.SSL_ERROR_WANT_WRITE
            else:
                self.channel_interface_obj.on_connect_failed()
                self.disconnect()

    def handle_handshake(self):
        if self.handshake_status == ssl.SSL_ERROR_WANT_READ:
            select.select([self.socket], [], [], 0)
        elif self.handshake_status == ssl.SSL_ERROR_WANT_WRITE:
            select.select([], [self.socket], [], 0)
        else:
            self.channel_interface_obj.on_connect_failed()
            self.disconnect()
        self._handshake()

    def on_handshaked(self):
        self.status = SSLConnector.ST_ESTABLISHED
        self.channel_interface_obj.connected = True
        self.channel_interface_obj.connecting = False
        self.channel_interface_obj.handle_connect()

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        self.channel_interface_obj.on_connect_failed()

    def handle_expt(self):
        asyncore.dispatcher.handle_expt(self)
        self.channel_interface_obj.on_connect_failed()

    def handle_error(self):
        asyncore.dispatcher.handle_error(self)
        self.channel_interface_obj.on_connect_failed()

    def readable(self):
        if self.status == SSLConnector.ST_HANDSHAKE:
            self.handle_handshake()
            return False
        if isinstance(self.socket, ssl.SSLSocket):
            while self.socket.pending() > 0:
                self.handle_read_event()

        return True


STATE_BEGIN = 1
STATE_CHUNK_HEAD = 2
STATE_CHUNK_BODY = 3
STATE_CHUNK_BOUND = 4
STATE_CHUNK_END = 5
STATE_FINISH = 0
_RE_TRANSFER_ENCODING = re.compile('Transfer-Encoding:', re.IGNORECASE)
_RE_CONTENT_LENGTH = re.compile('Content-Length:', re.IGNORECASE)

class _HTTPConnection(asynchat.async_chat):

    def __init__(self, request, timeout, wrapper_callback, max_buffer_size):
        asynchat.async_chat.__init__(self)
        self.set_terminator('\r\n\r\n')
        self.request = request
        self.callback = wrapper_callback
        self.state = STATE_BEGIN
        self.received_data = []
        self.remaining = max_buffer_size
        self.httpconnection = six.moves.http_client.HTTPConnection(request.host, request.port)
        self.httpconnection.send = functools.partial(self.on_http_request, self)
        self.httpconnection.request(request.method, request.url, request.body, request.headers)
        self.timer = Timer.addTimer(timeout, self.timeout)

    def on_http_request(self, httpconnection, data):
        self.request_data = data
        _logger.debug('connecting to %s', (self.httpconnection.host, self.httpconnection.port))
        if self.request.usessl:
            self.sslconnector = SSLConnector(self.request.certfile, self)
            self.sslconnector.connect((self.httpconnection.host, self.httpconnection.port))
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((self.httpconnection.host, self.httpconnection.port))

    def handle_connect(self):
        if self.request.usessl:
            self.sslconnector.del_channel()
            self.set_socket(self.sslconnector.socket)
        self.push(self.request_data)

    def on_connect_failed(self):
        self.callback(None)
        self.timer.cancel()
        return

    def collect_incoming_data(self, data):
        self.remaining -= len(data)
        if self.remaining < 0:
            _logger.warn('http request %s response exceed max length', str(self.request))
            self.timer.cancel()
            self.close()
            return
        self.received_data.append(data)

    def __str__(self):
        return 'AsyncHTTPResponse %s' % self._replyline

    def timeout(self):
        _logger.warn('http request %s  timeout', str(self.request))
        if self.request.usessl and self.socket is None:
            self.sslconnector.close()
        else:
            self.close()
        self.callback(None)
        return

    def get_content_length(self):
        data = ''.join(self.received_data)
        self.received_data = [
         data, '\r\n\r\n']
        m = _RE_CONTENT_LENGTH.search(data)
        if m is None:
            return
        else:
            start = m.start()
            end = data.find('\n', start)
            pair = data[start:end].split(':')
            if len(pair) != 2:
                return
            return int(pair[1].strip())

    def check_chunked(self):
        data = ''.join(self.received_data)
        m = _RE_TRANSFER_ENCODING.search(data)
        if m is None:
            return False
        else:
            start = m.start()
            end = data.find('\n', start)
            pair = data[start:end].split(':')
            if len(pair) != 2:
                return False
            if pair[1].strip() != 'chunked':
                return False
            return True

    def get_chunk_header_length(self):
        data = ''.join(self.received_data)
        bodyLenStr = data[self.curPos:]
        bodyLen = int(bodyLenStr, 16)
        self.received_data = [
         data, '\r\n']
        return bodyLen

    def found_terminator(self):
        if self.state == STATE_BEGIN:
            contentlen = self.get_content_length()
            if contentlen:
                self.state = STATE_FINISH
                self.set_terminator(contentlen)
            elif self.check_chunked():
                self.state = STATE_CHUNK_HEAD
                data = ''.join(self.received_data)
                self.curPos = len(data)
                self.received_data = [data]
                self.set_terminator('\r\n')
            else:
                self.handle_close()
        elif self.state == STATE_CHUNK_HEAD:
            bodyLen = self.get_chunk_header_length()
            if bodyLen != 0:
                self.state = STATE_CHUNK_BODY
                self.set_terminator(bodyLen)
            else:
                self.state = STATE_CHUNK_END
                self.set_terminator('\r\n')
        elif self.state == STATE_CHUNK_BODY:
            self.state = STATE_CHUNK_BOUND
            self.set_terminator('\r\n')
        elif self.state == STATE_CHUNK_BOUND:
            self.state = STATE_CHUNK_HEAD
            data = ''.join(self.received_data)
            self.received_data = [data, '\r\n']
            self.curPos = len(data) + 2
            self.set_terminator('\r\n')
        elif self.state == STATE_CHUNK_END:
            data = ''.join(self.received_data)
            self.received_data = [data, '\r\n']
            self.state = STATE_FINISH
            self.handle_close()
        else:
            self.handle_close()

    def handle_close(self):
        asynchat.async_chat.handle_close(self)
        if self.state != STATE_FINISH:
            self.callback(None)
            self.timer.cancel()
            return
        else:
            try:
                fp = six_ex.moves.cStringIO.StringIO(''.join(self.received_data))
                response = _HttpResponse(fp)
                response.begin()
                body = response.read()
            except:
                self.callback(None)
                self.timer.cancel()
            else:
                self.callback(HttpReply(response.msg, body))
                self.timer.cancel()

            return

    def handle_expt(self):
        asynchat.async_chat.handle_expt(self)
        self.callback(None)
        self.timer.cancel()
        return

    def handle_error(self):
        asynchat.async_chat.handle_error(self)
        self.callback(None)
        self.timer.cancel()
        return


if __name__ == '__main__':

    def callback(request, reply):
        print('entering http callback')
        if reply != None:
            print(request, reply, reply.body)
        else:
            print('failed to fetch the request', str(request))
        return


    client = SimpleAsyncHTTPClient(10)
    request = HttpRequest('reg.163.com', 'GET', '/services/checkMobToken?userip=10.12.1.2&token=7287c60ead2a841f7c97bfb08bfc2aac&id=9BCE35B69832E767E085421C3D22691AE96E0873A4DD583B9D89DA079D1D7F92', usessl=False)
    client.http_request(request, 5, callback)
    from mobilerpc.IoService import IoService
    print('active http client' + str(len(client.active)))
    IoService().run()