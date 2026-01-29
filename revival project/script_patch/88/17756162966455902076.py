# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/uds_sdk/UDSMgr.py
from __future__ import absolute_import
import socket
from common.framework import Singleton

class UDSDKBase(object):
    UDS_ADDR = ''

    def __init__(self):
        self._udsock = None
        return

    def setup(self):
        self._udsock = UDSMgr().get_or_create(self.UDS_ADDR)
        return self._udsock is not None


class UDSocket(object):

    def __init__(self, sock_id):
        self._sock_id = sock_id
        self._send_list = []

    def send(self, msg):
        self._send_list.append(msg)
        UDSMgr().notify_sync()

    def query(self, msg, callback=None):
        raise NotImplementedError('')


class UDSMgr(Singleton):
    ALIAS_NAME = 'uds_mgr'

    def init(self):
        self._uds_list = []
        self._uds_map = {}
        self._do_sync = False

    def get_or_create(self, address):
        if address in self._uds_map:
            return self._uds_map[address]
        else:
            try:
                import nxapp
                sock_id = nxapp.create_localsocket(address)
                if sock_id == -1:
                    sock = None
                else:
                    sock = UDSocket(sock_id)
                    self._uds_list.append(sock)
            except AttributeError as msg:
                log_error('UDS not support', msg)
                sock = None
            except ImportError as msg:
                log_error('UDS not support', msg)
                sock = None

            self._uds_map[address] = sock
            return sock

    def notify_sync(self):
        if self._do_sync:
            return
        self._do_sync = True
        global_data.game_mgr.post_exec(self.sync)

    def sync(self):
        try:
            import nxapp
            for sock in self._uds_list:
                for msg in sock._send_list:
                    nxapp.localsocket_send(sock._sock_id, msg)

            self._do_sync = False
        except ImportError as msg:
            log_error('UDS not support', msg)
            self._do_sync = False
        except AttributeError as msg:
            log_error('UDS not support', msg)
            self._do_sync = False