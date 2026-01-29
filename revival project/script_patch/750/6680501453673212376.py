# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPveTalent.py
from __future__ import absolute_import
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict
from common.cfg import confmgr

class impPveTalent(object):

    def _init_pvetalent_from_dict(self, bdict):
        self.talent_data = bdict.get('talent_data', {})

    def get_talent_level_by_id(self, talent_id):
        talent_id = int(talent_id)
        return self.talent_data.get(talent_id, 0)

    def get_talent_cost(self, talent_id):
        talent_total_level = 0
        for talent_level in six_ex.values(self.talent_data):
            talent_total_level += talent_level

        init_cost = confmgr.get('talent_data', str(talent_id), 'init_cost')
        cost = init_cost + talent_total_level * 10
        return cost

    @rpc_method(CLIENT_STUB, (Int('talent_id'), Int('lv')))
    def up_talent_level_sec(self, talent_id, lv):
        self.talent_data[talent_id] = lv
        talent_id = str(talent_id)
        global_data.emgr.refresh_pve_talent_event.emit(talent_id)

    def up_talent_level(self, talent_id):
        self.call_server_method('up_talent_level', (talent_id,))