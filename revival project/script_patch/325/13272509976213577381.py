# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/NetService.py
from __future__ import absolute_import
from ..common import mobilecommon
if mobilecommon.replace_async:
    from ..client.CachedServerProxy import AsioCachedServerProxy as CachedServerProxy
    from ..client.AsioGateClient import AsioGateClient as GateClient
else:
    from ..client.CachedServerProxy import CachedServerProxy
    from ..client.GateClient import GateClient
from ..mobilerpc.IoService import IoService
from logic.gcommon.common_utils.local_text import get_text_by_id

class NetService(object):
    ST_CONNECTING = 0
    ST_CONNECTED = 1
    ST_DISCONNECTED = 2
    DEFAULT_DISCONNECT_MSG = 80550
    CONNECT_TIMEOUT = 5

    def __init__(self, gate_client_config, traceback_handler):
        self._connect_status = NetService.ST_DISCONNECTED
        self._disconnect_msg = NetService.DEFAULT_DISCONNECT_MSG
        self._user_cb_dict = {}
        self._default_cb_dict = {}
        self._io_service = IoService()
        self._gate_client = None
        self.__init_gate_client(gate_client_config, traceback_handler)
        return

    def _set_connected_status(self, flag):
        self._connect_status = flag

    def disconnected(self):
        return self._connect_status == NetService.ST_DISCONNECTED

    def connected(self):
        return self._connect_status == NetService.ST_CONNECTED

    def connecting(self):
        return self._connect_status == NetService.ST_CONNECTING

    def get_connect_status(self):
        return self._connect_status

    def get_received_srv_msg_seq(self):
        if self._gate_client is None:
            return 0
        else:
            return self._gate_client.received_seq

    def get_send_srv_msg_seq_range(self):
        return CachedServerProxy.seq_range()

    def get_gate_client(self):
        return self._gate_client

    def __init_gate_client(self, gate_client_config, traceback_handler):
        if self._gate_client is not None:
            return
        else:
            gate_client = GateClient(None, None, gate_client_config)
            gate_client.enable_message_cache()
            gate_client.set_traceback_handler(traceback_handler)
            gate_client.set_session_padding_length(1, 4)
            gate_client.register_on_event_callback(GateClient.CB_ON_CONNECT_FAILED, self._on_connect_failed)
            gate_client.register_on_event_callback(GateClient.CB_ON_CONNECT_SUCCESSED, self._on_connect_successed)
            gate_client.register_on_event_callback(GateClient.CB_ON_DISCONNECTED, self._on_disconnected)
            gate_client.register_on_event_callback(GateClient.CB_ON_CONNECT_REPLY, self._on_connect_reply)
            gate_client.register_on_event_callback(GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT, self._on_reliable_message_cannot_sent)
            self._gate_client = gate_client
            return

    def tick(self):
        if self._connect_status in (NetService.ST_CONNECTING, NetService.ST_CONNECTED):
            self._io_service.loop(True)

    def _call_cb(self, type, *arg):
        ucb = self._user_cb_dict.get(type)
        if ucb is not None:
            ucb(*arg)
            return
        else:
            dcb = self._default_cb_dict.get(type)
            if dcb is not None:
                dcb(*arg)
                return
            return

    def _on_connect_failed(self):
        if self._connect_status == NetService.ST_DISCONNECTED:
            return
        self._set_connected_status(NetService.ST_DISCONNECTED)
        self._call_cb(GateClient.CB_ON_CONNECT_FAILED)

    def _on_connect_successed(self):
        self._set_connected_status(NetService.ST_CONNECTED)
        self._call_cb(GateClient.CB_ON_CONNECT_SUCCESSED)

    def _on_disconnected(self):
        self._set_connected_status(NetService.ST_DISCONNECTED)
        self._call_cb(GateClient.CB_ON_DISCONNECTED)

    def _on_connect_reply(self, type):
        self._call_cb(GateClient.CB_ON_CONNECT_REPLY, type)

    def _on_reliable_message_cannot_sent(self, op_code):
        self._call_cb(GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT, op_code)

    def set_default_callback(self, event_type, new_dcb):
        self._default_cb_dict[event_type] = new_dcb

    def set_user_callback(self, event_type, new_ucb):
        self._user_cb_dict[event_type] = new_ucb

    def unset_user_callback(self, event_type, cb):
        ucb = self._user_cb_dict.get(event_type)
        if ucb is not None and ucb == cb:
            del self._user_cb_dict[event_type]
        return

    def clean_all_user_callback(self):
        self._user_cb_dict = {}

    def clean_cache(self, reset_seq=True):
        CachedServerProxy.clear_cache(reset_seq)

    def connect(self, ip, port, authmsg=None):
        self._set_connected_status(NetService.ST_CONNECTING)
        CachedServerProxy.clear_cache()
        self._gate_client.reset(ip, port)
        self._gate_client.start_game(NetService.CONNECT_TIMEOUT, authmsg)

    def reconnect(self, ip, port, entityid, authmsg):
        self._set_connected_status(NetService.ST_CONNECTING)
        self._gate_client.reset(ip, port)
        self._gate_client.resume_game(NetService.CONNECT_TIMEOUT, entityid, authmsg)

    def disconnect(self):
        if self._gate_client is None:
            return
        else:
            self._gate_client.disconnect()
            return

    def set_disconnect_msg(self, err):
        self._disconnect_msg = err

    def pop_disconnect_msg(self):
        msg = self._disconnect_msg
        self.set_disconnect_msg(get_text_by_id(NetService.DEFAULT_DISCONNECT_MSG))
        return msg

    def get_disconnect_msg(self):
        return self._disconnect_msg