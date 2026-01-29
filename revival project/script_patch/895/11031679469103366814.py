# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRedPacket.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import json
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.time_utility import time
from logic.gcommon.common_const.red_packet_const import RED_PACKET_MESSAGE_CLAIM

class impRedPacket(object):

    def _init_redpacket_from_dict(self, bdict):
        self._red_packet_info = {}
        self._red_packet_day_create_cnt = bdict.get('red_packet_day_create_cnt', 0)
        self._red_packet_day_recv_cnt = bdict.get('red_packet_day_recv_cnt', 0)
        self._red_packet_day_luck_recv_cnt = bdict.get('red_packet_day_luck_recv_cnt', 0)
        self._red_packet_day_create_limit = bdict.get('red_packet_day_create_limit', 0)

    def _destroy_redpacket(self):
        self._red_packet_info = {}

    @rpc_method(CLIENT_STUB, (Int('pid'), Int('uid'), Str('name')))
    def claim_host_red_packet_succeed(self, pid, uid, name):
        if not global_data.message_data:
            return
        data = {}
        data['msg'] = ''
        data['chnl'] = 0
        data['time'] = time()
        sender_info = {}
        sender_info['uid'] = uid
        sender_info['char_name'] = name
        sender_info['red_packet_flag'] = RED_PACKET_MESSAGE_CLAIM
        sender_info['red_packet_claim_info'] = {'pid': pid
           }
        data['sender_info'] = sender_info
        self.search_red_packet_info([pid])
        global_data.message_data.add_msg(data)

    @rpc_method(CLIENT_STUB, (Int('create_cnt'), Int('create_limit')))
    def update_red_packet_day_create_cnt(self, create_cnt, create_limit):
        self._red_packet_day_create_cnt = create_cnt
        self._red_packet_day_create_limit = create_limit

    @rpc_method(CLIENT_STUB, (Int('create_limit'),))
    def clear_red_packet_day_cnt(self, create_limit):
        self._red_packet_day_recv_cnt = 0
        self._red_packet_day_create_cnt = 0
        self._red_packet_day_luck_recv_cnt = 0
        self._red_packet_day_create_limit = create_limit

    @rpc_method(CLIENT_STUB, (Int('recv_cnt'),))
    def update_red_packet_day_recv_cnt(self, recv_cnt):
        self._red_packet_day_recv_cnt = recv_cnt

    @rpc_method(CLIENT_STUB, (Int('recv_cnt'),))
    def update_red_packet_day_luck_recv_cnt(self, recv_cnt):
        self._red_packet_day_luck_recv_cnt = recv_cnt

    @rpc_method(CLIENT_STUB, (Int('flag'), Int('pid'), Int('count'), Int('item_no'), Dict('avt_info')))
    def respond_packet_claim(self, flag, pid, count, item_no, avt_info):
        packet_info = self._red_packet_info.get(pid, {})
        packet_info.update({'avt_info_dict': avt_info})
        avt_uid_list = packet_info.get('avt_uid_list', [])
        new_avt_uid_list = six_ex.keys(avt_info)
        packet_info['avt_uid_list'] = list(set(avt_uid_list + new_avt_uid_list))
        self._red_packet_info[pid] = packet_info
        global_data.emgr.claim_red_packet_succeed.emit(flag, pid, count, item_no, packet_info)

    @rpc_method(CLIENT_STUB, (List('infos'),))
    def respond_packets_search(self, infos):
        red_packet_infos = {}
        for i in range(len(infos)):
            info = json.loads(infos[i])
            if 'is_valid' in info:
                continue
            pid = info.get('pid', None)
            if not pid:
                continue
            red_packet_infos[pid] = info
            self._red_packet_info.update({pid: info})

        global_data.emgr.on_refresh_red_packet_info.emit(red_packet_infos)
        return

    def claim_red_packet(self, channel, pid, stub_id):
        self.call_server_method('try_claim_red_packet', (channel, pid, stub_id))

    def gen_red_packet(self, channel, coin_type, coin_num, spilt_count, skin_id, text_id):
        self.call_server_method('try_gen_red_packet', (channel, coin_type, coin_num, int(spilt_count), skin_id, text_id))

    def search_red_packet_info(self, packet_ids):
        self.call_server_method('search_red_packet_info', (packet_ids,))

    def get_red_packet_day_create_count(self):
        return self._red_packet_day_create_cnt

    def get_red_packet_day_recv_count(self):
        return self._red_packet_day_recv_cnt

    def get_red_packet_day_luck_recv_count(self):
        return self._red_packet_day_luck_recv_cnt

    def get_red_packet_day_create_limit_count(self):
        return self._red_packet_day_create_limit

    def send_red_packet_chat(self, channel, pid, text_idx, text_type):
        self.call_server_method('red_packet_chat', (channel, pid, text_idx, text_type))

    def update_new_red_packet_info(self, pid):
        if pid in self._red_packet_info or pid == -1:
            return
        self._red_packet_info[pid] = {}

    def get_red_packet_info(self, pid):
        if pid not in self._red_packet_info:
            return None
        else:
            return self._red_packet_info[pid]

    def gen_concert_red_packet(self, coin_type, coin_num, spilt_count, skin_id, text_id):
        self.call_server_method('try_gen_concert_red_packet', (coin_type, coin_num, int(spilt_count), skin_id, text_id))