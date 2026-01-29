# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileHttpClient.py
from __future__ import absolute_import
from __future__ import print_function
from .NileTimer import NileTimer
import time
import six
if six.PY2:
    from six.moves.urllib.parse import urlparse
else:
    from urllib.parse import urlparse
import urllib3
import common.daemon_thread

class NileHttpClient(object):

    def __init__(self, maxCount=10):
        super(NileHttpClient, self).__init__()
        self._maxCount = maxCount
        self._pendingRequests = list()
        self._clients = set()
        print('NileHttpClient init: maxClient %d' % self._maxCount)

    def Request(self, request, timeoutInSecond, callback):
        if not callable(callback):
            print('callback is not callable')
            return
        if self._GetActiveCount() >= self._maxCount:
            print('maxCount: %d limit reached' % self._maxCount)
            self._pendingRequests.append((request, timeoutInSecond, callback))
            return
        client = NileHttpImpl(self, request, timeoutInSecond, callback)
        self._clients.add(client)
        print('NileHttpClient start, url: %s' % request.url)
        client.Start()
        return client

    def _GetActiveCount(self):
        return len(self._clients)

    def ExecutePendingRequest(self):
        if len(self._pendingRequests) > 0:
            request, timeoutInSecond, callback = self._pendingRequests.pop(0)
            self.Request(request, timeoutInSecond, callback)

    def Remove(self, client):
        self._clients.discard(client)


class NileHttpImpl(object):

    def __init__(self, handler, request, timeoutInSecond, callback):
        self.handler = handler
        self.request = request
        self.timeout = timeoutInSecond * 1000
        self.callback = callback

    def Start(self):

        def DoRequest(url, request):
            try:
                http = urllib3.PoolManager(cert_reqs='CERT_NONE')
                print('%s send request: %s' % (time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()), request.url))
                response = http.request(request.method, request.url, timeout=self.timeout, headers=request.header, body=request.body, preload_content=False)
                return NileHttpReply(response.getheaders(), response.data, response.status, response.reason)
            except BaseException as e:
                print('http request error, url: %s, message: %s' % (url, str(e)))
                return NileHttpReply(request.header, None, 500, str(e))

            return None

        def DoResponse(request, reply):
            print('%s receive response: url: %s reply: %s' % (time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()), request.args[0], reply))
            self._Destroy()
            self.handler.ExecutePendingRequest()
            self.callback(request, reply)

        common.daemon_thread.DaemonThreadPool.get_instance().add_threadpool(DoRequest, DoResponse, self.request.url, self.request)

    def _Destroy(self):
        self.handler.Remove(self)


class NileHttpRequest(object):

    def __init__(self, url, port, method, header=None, body=''):
        result = urlparse(url)
        self.url = url.replace(result.netloc, '%s:%s' % (result.hostname, port))
        self.method = method
        self.header = header
        self.body = body

    def __str__(self):
        return self.method + ' ' + self.url


class NileHttpReply(object):

    def __init__(self, header, body, status, reason):
        self.header = header
        self.body = body
        self.status = status
        self.error = 0
        if self.status != 200:
            self.error = self.status
        self.reason = reason

    def __str__(self):
        return 'status: %s body length: %s' % (self.status, len(self.body or ''))