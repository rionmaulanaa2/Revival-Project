# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPveClearTime.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int, List, Bool
from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
import copy

class impPveClearTime(object):

    def _init_pvecleartime_from_dict(self, bdict):
        pass_info_dict = bdict.get('pve_clear_info_dict', {})
        c_pass_info_dict = self.server_2_client_info(pass_info_dict)
        self.pve_clear_info_dict = c_pass_info_dict
        global_data.message_data.on_update_my_rank_data(copy.deepcopy(c_pass_info_dict))

    def server_2_client_info(self, pass_info_dict):
        new_pass_info_dict = {}
        for server_rank_type, pass_info in six.iteritems(pass_info_dict):
            data_obj = PVERankDataObj(server_rank_type)
            new_pass_info_dict[data_obj.to_client()] = pass_info

        return new_pass_info_dict

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Dict('response_infos')))
    def reply_pve_clear_detail(self, rank_type, response_infos):
        data_obj = PVERankDataObj(rank_type)
        global_data.message_data.set_pve_rank_pass_data(data_obj, response_infos)

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Dict('clear_info')))
    def on_pve_clear_info_change(self, rank_type, clear_info):
        data_obj = PVERankDataObj(rank_type)
        self.pve_clear_info_dict[data_obj.to_client()] = clear_info

    def get_pve_pass_info_dict(self, c_rank_type, default_data=None):
        return self.pve_clear_info_dict.get(c_rank_type, default_data)

    def request_pve_clear_info(self, rank_type):
        self.call_server_method('request_pve_clear_info', (rank_type,))