# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBond.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict, List
from common.cfg import confmgr
from logic.gcommon.ctypes.Record import Record
import logic.gcommon.time_utility as tutil
from logic.gutils import role_utils

class impBond(object):
    BOND_LEVEL = 'lv'
    BOND_STRENGTH = 'st'
    BOND_KEEPSAKE_OPER_EQUIP = 'equip_keepsake'
    BOND_KEEPSAKE_OPER_UNLOAD = 'unload_keepsake'
    BOND_KEEPSAKE_OPER_UPDATE = 'update_keepsake'

    def _init_bond_from_dict(self, bdict):
        self.bond_data = bdict.get('bond_data', {})
        bond_reward_data = bdict.get('bond_reward_data', {})
        self.bond_reward_data = {role_id:Record(record_dict) for role_id, record_dict in six.iteritems(bond_reward_data)}
        self.bond_gifts = bdict.get('bond_gifts', {})
        self.bond_keepsakes = bdict.get('bond_keepsakes', {})
        self.bond_driver_gifts = bdict.get('bond_driver_gifts', {})
        self.bond_human_gifts = bdict.get('bond_human_gifts', {})
        self.bond_gift_last_reset_time = bdict.get('bond_gift_last_reset_time', {})
        self._bond_upgrade_sequence = []

    def get_bond_role_num(self):
        return len(self.bond_gifts)

    def get_bond_data(self, role_id):
        bond_dict = self.bond_data.get(role_id, {})
        level = bond_dict.get(impBond.BOND_LEVEL, 1)
        strength = bond_dict.get(impBond.BOND_STRENGTH, 0)
        return (
         level, strength)

    def get_role_bond_gifts(self, role_id):
        return self.bond_gifts.get(role_id, [])

    def has_keepsake(self, gift_id):
        from logic.gutils import bond_utils
        from logic.gcommon.cdata import bond_gift_config
        gift_base_conf = bond_gift_config.GetBondGiftBaseDataConfig().get(gift_id, None)
        if not gift_base_conf or gift_base_conf['gift_type'] != bond_gift_config.BOND_GIFT_TYPE_KEEPSAKE_GIFT:
            return False
        else:
            if not self.has_item_by_no(gift_base_conf['activate_item_no']):
                return False
            return True

    def has_equiped_keepsake(self, role_id, gift_id):
        cur_gift_id = self.get_equip_keepsake(role_id)
        return cur_gift_id == gift_id

    def get_equip_keepsake(self, role_id):
        from logic.gutils import bond_utils
        ret_gift_id = 0
        role_keepsake_info = self.bond_keepsakes.get(role_id, {})
        if not role_keepsake_info:
            return ret_gift_id
        for item_no, flag in six.iteritems(role_keepsake_info):
            if flag:
                ret_gift_id = bond_utils.get_gift_id_by_itemno(item_no)
                break

        return ret_gift_id

    def get_equip_driver_gift(self, role_id):
        from logic.gutils import bond_utils
        ret_gift_id = 0
        role_driver_gifts_info = self.bond_driver_gifts.get(role_id, {})
        if not role_driver_gifts_info:
            return ret_gift_id
        for gift_id, flag in six.iteritems(role_driver_gifts_info):
            if flag:
                ret_gift_id = gift_id
                break

        return ret_gift_id

    def get_equip_human_gift(self, role_id):
        from logic.gutils import bond_utils
        ret_gift_id = 0
        role_human_gifts_info = self.bond_human_gifts.get(role_id, {})
        if not role_human_gifts_info:
            return ret_gift_id
        for gift_id, flag in six.iteritems(role_human_gifts_info):
            if flag:
                ret_gift_id = gift_id
                break

        return ret_gift_id

    def get_crossover_equip_driver_gift(self, role_id, gift_type):
        from logic.gutils import role_utils
        from logic.gcommon.cdata.bond_gift_config import get_bond_gift_type
        if not role_utils.is_crossover_role(role_id):
            return
        role_gifts_info = self.bond_gifts.get(role_id, [])
        for gift_id in role_gifts_info:
            if get_bond_gift_type(gift_id) == gift_type:
                return gift_id

    def get_equip_gift(self, role_id, gift_type):
        from logic.gcommon.cdata import bond_gift_config
        from logic.gcommon.cdata.bond_gift_config import get_bond_gift_type
        if gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
            return self.get_equip_human_gift(role_id)
        if gift_type == bond_gift_config.BOND_GIFT_TYPE_DRIVER_GIFT:
            return self.get_equip_driver_gift(role_id)

    def get_role_keepsake(self, role_id):
        return self.bond_keepsakes.get(role_id, {})

    def get_bond_gift_last_reset_time(self, base_gift_id):
        base_gift_id = int(base_gift_id)
        return self.bond_gift_last_reset_time.get(base_gift_id)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Int('level'), Int('strength'), Str('reason'), Int('dialog_id')))
    def update_bond_level(self, role_id, level, strength, reason, dialog_id):
        from logic.comsys.lobby.RoleBondTipsUI import RoleBondTipsUI
        self.bond_data.setdefault(role_id, {})
        old_lv, old_exp = self.get_bond_data(role_id)
        event_info = {impBond.BOND_LEVEL: [
                              old_lv, level],
           impBond.BOND_STRENGTH: [
                                 old_exp, strength]
           }
        self.bond_data[role_id].update({impBond.BOND_LEVEL: level,
           impBond.BOND_STRENGTH: strength
           })
        global_data.emgr.bond_update_role_level.emit(role_id, event_info)
        if not global_data.ui_mgr.get_ui('LotteryMainUI'):
            self.show_bond_level_up(old_lv, old_exp, role_id, level, strength, reason, dialog_id)
        else:
            self._bond_upgrade_sequence.append([old_lv, old_exp, role_id, level, strength, reason, dialog_id])
        if reason.startswith('ADD_BOND_ON_GOT_ITEM'):
            ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            if not ui:
                tips_ui = global_data.ui_mgr.get_ui('RoleBondTipsUI')
                if tips_ui:
                    tips_ui.init_widget(role_id, event_info)
                else:
                    RoleBondTipsUI(None, role_id, event_info)
        return

    def show_bond_level_up(self, old_lv, old_exp, role_id, level, strength, reason, dialog_id):
        import game3d
        from logic.comsys.battle.Settle import EndExpUI
        if old_lv != level:
            ui = global_data.ui_mgr.get_ui('EndExpUI')
            if not ui:
                ui = global_data.ui_mgr.get_ui('BRV2EndExpUI')
            if not ui and not reason.startswith('BATTLE_REWARD') and not reason.startswith('gm_revert') and not reason.startswith('ADD_BOND_OF_EXISTING_ROLE'):
                game3d.delay_exec(500, lambda : global_data.emgr.show_bond_level_up.emit([role_id, old_lv, level]))

    def receive_bond_reward(self, role_id, lv):
        cur_lv, _ = self.get_bond_data(role_id)
        if cur_lv < lv:
            return
        if not self.is_bond_reward_received(role_id, lv):
            self.call_server_method('receive_bond_reward', (role_id, lv))

    def is_bond_reward_received(self, role_id, lv):
        reward_record = self.bond_reward_data.setdefault(role_id, Record())
        if not reward_record:
            return False
        return reward_record.is_record(lv)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Int('lv'), Bool('ret')))
    def receive_bond_reward_ret(self, role_id, lv, ret):
        if ret:
            self.bond_reward_data.setdefault(role_id, Record())
            self.bond_reward_data[role_id].record(lv)
            global_data.emgr.bond_role_reward.emit(role_id)

    def request_upgrade_role_bond_gift(self, role_id, gift_id):
        global_data.player.call_server_method('request_upgrade_role_bond_gift', (role_id, gift_id))

    @rpc_method(CLIENT_STUB, (Int('role_id'), Int('gift_id')))
    def on_role_add_bond_gift(self, role_id, gift_id):
        if role_id not in self.bond_gifts:
            self.bond_gifts[role_id] = [
             gift_id]
        elif gift_id not in self.bond_gifts[role_id]:
            self.bond_gifts[role_id].append(gift_id)
        global_data.emgr.bond_role_gift.emit(role_id)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Int('old_gift_id'), Int('new_gift_id')))
    def on_role_upgrade_bond_gift(self, role_id, old_gift_id, new_gift_id):
        self.bond_gifts[role_id].remove(old_gift_id)
        self.bond_gifts[role_id].append(new_gift_id)
        global_data.emgr.bond_role_gift.emit(role_id)

    @rpc_method(CLIENT_STUB, (Int('role_id'), List('gifts')))
    def on_role_set_bond_gift(self, role_id, gifts):
        if role_id in self.bond_gifts:
            self.bond_gifts[role_id] = gifts
            global_data.emgr.bond_role_gift.emit(role_id)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Dict('reward_data')))
    def reset_received_role_bond_reward(self, role_id, reward_data):
        self.bond_reward_data[role_id] = Record(reward_data)
        global_data.emgr.bond_role_reward.emit(role_id)

    @rpc_method(CLIENT_STUB, (Str('oper_type'), Int('role_id'), Dict('role_keepsakes')))
    def ret_bond_keepsake_oper(self, oper_type, role_id, role_keepsakes):
        self.bond_keepsakes[role_id] = role_keepsakes
        global_data.emgr.ret_bond_keepsake_oper.emit(oper_type, role_id, role_keepsakes)

    def equip_bond_keepsake(self, role_id, item_no):
        if not role_id or not item_no:
            return
        if not self.has_role(int(role_id)) or not self.has_item_by_no(item_no):
            return
        self.call_server_method('equip_bond_keepsake', (role_id, item_no))

    def unload_bond_keepsake(self, role_id, item_no):
        if not role_id or not item_no:
            return
        if not self.has_role(int(role_id)) or not self.has_item_by_no(item_no):
            return
        self.call_server_method('unload_bond_keepsake', (role_id, item_no))

    def update_bond_keepsake(self, role_id, old_item_no, new_item_no):
        if not role_id or not old_item_no or not new_item_no:
            return
        if not self.has_role(int(role_id)) or not self.has_item_by_no(old_item_no) or not self.has_item_by_no(new_item_no):
            return
        self.call_server_method('update_bond_keepsake', (role_id, old_item_no, new_item_no))

    def replace_bond_driver_gift(self, to_role_id, new_gift_id):
        from logic.gcommon.cdata import bond_gift_config
        new_gift_type = bond_gift_config.get_bond_gift_type(new_gift_id)
        if role_utils.is_crossover_role(to_role_id):
            old_gift_id = self.get_crossover_equip_driver_gift(to_role_id, new_gift_type)
        else:
            old_gift_id = self.get_equip_gift(to_role_id, new_gift_type)
        if old_gift_id == new_gift_id:
            return
        self._replace_bond_driver_gift(to_role_id, old_gift_id, new_gift_id)

    def _replace_bond_driver_gift(self, role_id, old_gift_id, new_gift_id):
        if not role_id or not old_gift_id or not new_gift_id:
            return
        if role_utils.is_crossover_role(role_id):
            driver_gifts = self.bond_gifts.get(role_id, [])
        else:
            driver_gifts = set(self.bond_driver_gifts.get(role_id, {})).union(set(self.bond_human_gifts.get(role_id, {})))
        if old_gift_id not in driver_gifts or new_gift_id in driver_gifts:
            return
        self.call_server_method('replace_bond_driver_gift', (role_id, old_gift_id, new_gift_id))

    @rpc_method(CLIENT_STUB, (Int('role_id'), Dict('driver_gifts')))
    def ret_bond_replace_driver_gift(self, role_id, driver_gifts):
        self.bond_driver_gifts[role_id] = driver_gifts
        global_data.emgr.ret_bond_replace_driver_gift.emit(role_id, driver_gifts)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Dict('human_gifts')))
    def ret_bond_replace_human_gift(self, role_id, human_gifts):
        self.bond_human_gifts[role_id] = human_gifts
        global_data.emgr.ret_bond_replace_driver_gift.emit(role_id, human_gifts)

    @rpc_method(CLIENT_STUB, (Dict('bond_driver_gifts'),))
    def update_bond_driver_gift(self, bond_driver_gifts):
        self.bond_driver_gifts = bond_driver_gifts
        global_data.emgr.ret_bond_refresh_driver_gifts.emit()

    @rpc_method(CLIENT_STUB, (Dict('bond_human_gifts'),))
    def update_bond_human_gift(self, bond_human_gifts):
        self.bond_human_gifts = bond_human_gifts
        global_data.emgr.ret_bond_refresh_driver_gifts.emit()

    def reset_bond_gift(self, gift_id):
        from logic.gcommon.cdata import bond_gift_config
        if not gift_id:
            return
        if bond_gift_config.get_gift_level(gift_id) <= 1:
            return
        self.call_server_method('reset_bond_gift', (gift_id,))

    @rpc_method(CLIENT_STUB, (Int('role_id'), Int('reset_gift_id')))
    def on_role_reset_bond_gift(self, role_id, reset_gift_id):
        if role_id not in self.bond_gifts:
            return
        from logic.gcommon.cdata import bond_gift_config
        base_gift_id = bond_gift_config.get_base_gift_id(reset_gift_id)
        role_gift = self.bond_gifts[role_id]
        self.bond_gifts[role_id] = [ base_gift_id if 1 else gift for gift in role_gift if gift == reset_gift_id ]
        global_data.emgr.bond_role_gift.emit(role_id)
        global_data.emgr.player_money_info_update_event.emit()
        self.bond_gift_last_reset_time[base_gift_id] = tutil.get_time()

    def check_waiting_bond_upgrade_sequences(self):
        if self._bond_upgrade_sequence:
            info = self._bond_upgrade_sequence.pop(0)
            import game3d
            game3d.delay_exec(1, lambda : self.show_bond_level_up(*info))

    @rpc_method(CLIENT_STUB, (Int('role_id'), List('gifts')))
    def ret_replace_bond_cross_role_gift(self, role_id, gifts):
        self.bond_gifts[role_id] = gifts
        global_data.emgr.bond_role_gift.emit(role_id)