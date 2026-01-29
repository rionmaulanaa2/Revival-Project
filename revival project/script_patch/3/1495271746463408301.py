# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/HttpBase.py
from __future__ import absolute_import
import six.moves.collections_abc
import collections
import functools
from ..mobilelog.LogManager import LogManager
import six.moves.http_client

class HttpRequest(object):

    def __init__(self, host, method, url, headers=None, usessl=False, keyfile=None, certfile=None, port=None, body=None):
        self.host = host
        self.port = port
        if usessl and self.port == None:
            self.port = 443
        self.method = method
        self.url = url
        self.headers = headers and headers or {}
        self.usessl = usessl
        self.keyfile = keyfile
        self.certfile = certfile
        self.body = body
        return

    def __str__(self):
        return self.method + ' ' + self.host + ' ' + self.url


class HttpReply(object):

    def __init__(self, header, body):
        super(HttpReply, self).__init__()
        self.header = header
        self.body = body

    def __str__(self):
        return str(self.header)