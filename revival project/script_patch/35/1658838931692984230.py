# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/RpcChannelManager.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from .RpcChannel import MobileRpcChannel
from ..common import mobilecommon

class RpcChannelCreator(object):

    def __init__(self, rpc_service, channel_handler, max_data_len=0):
        super(RpcChannelCreator, self).__init__()
        self.logger = LogManager.get_logger('mobilerpc.RpcChannelCreator')
        self.rpc_service = rpc_service
        self.channel_handler = channel_handler
        self.max_data_len = max_data_len

    def set_max_data(self, size):
        self.max_data_len = size

    def handle_new_connection(self, con):
        if mobilecommon.replace_async:
            pass
        rpc_channel = MobileRpcChannel(self.rpc_service, con)
        if self.max_data_len > 0:
            rpc_channel.set_max_data(self.max_data_len)
        self.channel_handler.handle_new_channel(rpc_channel)

    def handle_connection_failed(self, con):
        pass


class RpcChannelHolder(object):

    def __init__(self):
        super(RpcChannelHolder, self).__init__()
        self.logger = LogManager.get_logger('mobilerpc.RpcChannelHolder')
        self.rpc_channel = None
        return

    def handle_new_channel(self, rpc_channel):
        self.rpc_channel = rpc_channel
        rpc_channel.reg_listener(self)

    def on_channel_disconnected(self, _rpc_channel):
        self.rpc_channel = None
        return

    def get_rpc_channel(self):
        return self.rpc_channel


class RpcChannelManager(object):

    def __init__(self):
        super(RpcChannelManager, self).__init__()
        self.logger = LogManager.get_logger('mobilerpc.RpcChannelManager')
        self.rpc_channels = {}

    def handle_new_channel(self, rpc_channel):
        self.rpc_channels[rpc_channel.getpeername()] = rpc_channel
        rpc_channel.reg_listener(self)

    def on_channel_disconnected(self, rpc_channel):
        peername = rpc_channel.conn.getpeername()
        if peername in self.rpc_channels:
            del self.rpc_channels[peername]

    def get_rpc_channel(self, peername):
        return self.rpc_channels.get(peername, None)

    def rpc_channel_num(self):
        return len(self.rpc_channels)