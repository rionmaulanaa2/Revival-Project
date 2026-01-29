# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPVEMechaDevelopment.py
from __future__ import absolute_import
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict
from common.cfg import confmgr
from copy import deepcopy
import six_ex

class impPVEMechaDevelopment(object):

    def _init_pvemechadevelopment_from_dict(self, bdict):
        self.pve_mecha_level_dict = bdict.get('pve_mecha_level_dict', {})
        self.mecha_upgrade_cost_conf = confmgr.get('mecha_upgrade_cost_data', default={})
        self.mecha_debris_conf = confmgr.get('mecha_debris_data', default={})
        self.get_mecha_sp_effect_list()

    def get_mecha_level_by_id(self, mecha_id):
        mecha_id = str(mecha_id)
        return self.pve_mecha_level_dict.get(mecha_id, 0)

    def get_upgrade_mecha_cost_list(self, mecha_id, upgrade_level):
        level = self.get_mecha_level_by_id(mecha_id)
        ex_cost, common_cost = (0, 0)
        for i in range(level, level + upgrade_level):
            i = str(i + 1)
            if i in self.mecha_upgrade_cost_conf:
                ex_cost += self.mecha_upgrade_cost_conf.get(i, {}).get('ex_cost', 0)
                common_cost += self.mecha_upgrade_cost_conf.get(i, {}).get('common_cost', 0)

        mecha_debris_conf = self.mecha_debris_conf.get(str(mecha_id))
        ex_cost_item_no = mecha_debris_conf.get('ex_cost')
        common_cost_item_no = mecha_debris_conf.get('common_cost')
        return {'ex_cost': (ex_cost_item_no, ex_cost),'common_cost': (common_cost_item_no, common_cost)}

    def get_max_upgrade_mecha_level(self, mecha_id):
        level = self.get_mecha_level_by_id(mecha_id)
        max_level = len(self.get_mecha_all_effect(mecha_id))
        ex_cost, common_cost = (0, 0)
        upgrade_level = 0
        mecha_debris_conf = self.mecha_debris_conf.get(str(mecha_id))
        ex_cost_item_no = mecha_debris_conf.get('ex_cost')
        common_cost_item_no = mecha_debris_conf.get('common_cost')
        ex_cost_item_count = global_data.player.get_item_num_by_no(int(ex_cost_item_no))
        common_cost_item_count = global_data.player.get_item_num_by_no(int(common_cost_item_no))
        while ex_cost <= ex_cost_item_count and common_cost <= common_cost_item_count and upgrade_level + level < max_level:
            i = str(upgrade_level + level + 1)
            if i in self.mecha_upgrade_cost_conf:
                ex_cost += self.mecha_upgrade_cost_conf.get(i, {}).get('ex_cost', 0)
                common_cost += self.mecha_upgrade_cost_conf.get(i, {}).get('common_cost', 0)
            if ex_cost_item_count >= ex_cost and common_cost_item_count >= common_cost:
                upgrade_level += 1

        return upgrade_level

    def get_mecha_sp_effect_list(self):
        self.mecha_add_effect_dict = {}
        self.mecha_all_effect_dict = {}
        mecha_upgrade_conf = deepcopy(confmgr.get('mecha_upgrade_data', default={}))
        for mecha_id, mecha_dict in six_ex.items(mecha_upgrade_conf):
            effect_dict = {}
            mecha_effect_dict = {}
            mecha_all_effect_dict = {}
            effect_list = []
            for mecha_level, effect_info in six_ex.items(mecha_dict):
                effect_id = effect_info.get('upgrade_add_effect')[0]
                effect_list.append(effect_id)
                effect_level = 1
                if 'upgrade_del_effect' in effect_info:
                    del_effect_id = effect_info['upgrade_del_effect'][0]
                    effect_level = effect_dict[del_effect_id] + 1
                    if del_effect_id in effect_list:
                        effect_list.remove(del_effect_id)
                effect_dict[effect_id] = effect_level
                mecha_effect_dict[int(mecha_level)] = {'effect_id': effect_id,'effect_level': effect_level}
                if not mecha_all_effect_dict.get(int(mecha_level)):
                    mecha_all_effect_dict[int(mecha_level)] = []
                mecha_all_effect_dict[int(mecha_level)] = deepcopy(effect_list)

            self.mecha_add_effect_dict[mecha_id] = mecha_effect_dict
            self.mecha_all_effect_dict[mecha_id] = mecha_all_effect_dict

    def get_mecha_all_effect(self, mecha_id):
        return self.mecha_add_effect_dict.get(str(mecha_id), {})

    def get_mecha_effect(self, mecha_id, level):
        return self.mecha_all_effect_dict.get(str(mecha_id), {}).get(level, [])

    def get_add_upgrade_mecha_effect(self, mecha_id, level):
        return self.get_mecha_all_effect(mecha_id).get(int(level), [0, 0])

    @rpc_method(CLIENT_STUB, (Int('mecha_id'), Int('new_level'), Int('add_cnt')))
    def on_pve_mecha_upgrade(self, mecha_id, new_level, add_cnt):
        self.pve_mecha_level_dict[str(mecha_id)] = new_level
        global_data.emgr.on_pve_mecha_upgrade.emit(mecha_id)
        ui = global_data.ui_mgr.get_ui('PVEMechaUpgradePanel')
        if not ui:
            from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVEMechaUpgradePanel import PVEMechaUpgradePanel
            PVEMechaUpgradePanel(mecha_id=mecha_id, new_level=new_level, add_cnt=add_cnt)

    def do_pve_mecha_upgrade(self, mecha_id, add_cnt):
        self.call_server_method('do_pve_mecha_upgrade', (mecha_id, add_cnt))