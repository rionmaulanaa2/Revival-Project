# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPveClearTimeTeam.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int, List, Bool

class impPveClearTimeTeam(object):

    def _init_pvecleartimeteam_from_dict(self, bdict):
        self.pve_clear_team_info_dict = bdict.get('pve_clear_team_info_dict', {})

    def request_pve_clear_detail_team(self, rank_type, pve_uid_key, uid_list):
        self.call_server_method('request_pve_clear_detail_team', (rank_type, pve_uid_key, uid_list))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Str('pve_uid_key'), Dict('response_infos')))
    def reply_pve_clear_detail_team(self, rank_type, pve_uid_key, response_infos):
        global_data.message_data.set_team_pve_rank_pass_data(rank_type, pve_uid_key, response_infos)

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Str('pve_uid_key'), Dict('clear_info')))
    def on_pve_clear_team_info_change(self, rank_type, pve_uid_key, clear_info):
        all_clear_info = self.pve_clear_team_info_dict.setdefault(rank_type, {})
        all_clear_info[pve_uid_key] = clear_info

    def request_pve_clear_team_info(self, rank_type, pve_uid_key):
        self.call_server_method('request_pve_clear_team_info', (rank_type, pve_uid_key))

    def get_pve_team_pass_info_dict(self, rank_type, default_data=None):
        return self.pve_clear_team_info_dict.get(rank_type, default_data)