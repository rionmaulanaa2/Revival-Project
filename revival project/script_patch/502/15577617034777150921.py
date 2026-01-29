# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNewbiePass.py
from __future__ import absolute_import
import six
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict, List
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.ctypes.RewardRecord import RewardRecord
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_NEWBIE_BATTLEPASS_H
from logic.gcommon.common_const.battlepass_const import NEWBIE_PASS_TYPE_1, NEWBIE_CARD, BATTLE_CARD_TYPE
from data.newbiepass_data import NEWBIEPASS_LV_CAP, get_lv_reward

class impNewbiePass(object):

    def _init_newbiepass_from_dict(self, bdict):
        self.newbiepass_lv = bdict.get('newbiepass_lv', 1)
        self.newbiepass_point = bdict.get('newbiepass_point', 0)
        self.newbiepass_types = set(bdict.get('newbiepass_types', ()))
        self.newbiepass_reward_record = RewardRecord()
        self.newbiepass_reward_record.init_from_dict(bdict.get('newbiepass_reward_record', {}))

    @rpc_method(CLIENT_STUB, ())
    def reset_newbiepass(self):
        self.newbiepass_lv = 1
        self.newbiepass_point = 0
        self.newbiepass_types = set()
        self.newbiepass_reward_record.clear()

    def activate_newbiepass_type(self, newbiepass_type):
        if newbiepass_type in self.newbiepass_types:
            return
        self.call_server_method('activate_newbiepass_type', (newbiepass_type,))

    @rpc_method(CLIENT_STUB, (List('newbiepass_types'), Str('newbiepass_reward_type')))
    def open_newbiepass_type(self, newbiepass_types, newbiepass_reward_type):
        old_newbiepass_types = self.newbiepass_types
        self.newbiepass_types = set(newbiepass_types)
        self.newbiepass_reward_record.setdefault(newbiepass_reward_type, Record())
        add_newbiepass_types = self.newbiepass_types - old_newbiepass_types
        for newbiepass_type in add_newbiepass_types:
            global_data.emgr.newbiepaas_open_type.emit(newbiepass_type)

        if str(NEWBIE_PASS_TYPE_1) in newbiepass_types:
            Appsflyer().advert_track_event(AF_NEWBIE_BATTLEPASS_H)
        global_data.ui_mgr.close_ui('BuyNewBieCardUI')

    @rpc_method(CLIENT_STUB, (Int('newbiepass_lv'), Int('newbiepass_point')))
    def update_newbiepass_lv(self, newbiepass_lv, newbiepass_point):
        if self.newbiepass_lv != newbiepass_lv:
            ui = global_data.ui_mgr.show_ui('NewBiePassLevelUp', 'logic.comsys.battle_pass')
            ui.set_level(NEWBIE_CARD, self.newbiepass_lv, newbiepass_lv)
        self.newbiepass_lv = newbiepass_lv
        self.newbiepass_point = newbiepass_point
        global_data.emgr.newbiepaas_update_lv.emit(self.newbiepass_lv, self.newbiepass_point)

    def receive_newbiepass_reward(self, newbiepass_reward_type, newbiepass_lv):
        pass

    def receive_all_newbiepass_reward(self):
        pass

    @rpc_method(CLIENT_STUB, (Dict('newbiepass_reward_records'),))
    def update_newbiepass_rewards(self, newbiepass_reward_records):
        for newbiepass_reward_type, record_data in six.iteritems(newbiepass_reward_records):
            reward_record = self.newbiepass_reward_record.setdefault(newbiepass_reward_type, Record())
            reward_record.update(record_data[0], set(record_data[1]))

        global_data.emgr.newbiepaas_update_award.emit()

    def get_newbiepass_info(self):
        return (
         self.newbiepass_lv, self.newbiepass_point)

    def get_newbiepass_reward_record(self):
        return self.newbiepass_reward_record

    def has_buy_newbie_card_type(self, np_type):
        if str(np_type) in self.newbiepass_types:
            return True
        return False

    def has_buy_newbie_card(self):
        if str(NEWBIE_PASS_TYPE_1) in self.newbiepass_types:
            return True
        return False

    def has_received_all_newbiepass_reward(self):
        if self.newbiepass_lv != NEWBIEPASS_LV_CAP:
            return False
        else:
            reward_records = self.get_newbiepass_reward_record()
            for bp_lv in range(1, NEWBIEPASS_LV_CAP + 1):
                for bp_type in BATTLE_CARD_TYPE:
                    reward_at_lv = get_lv_reward(str(bp_type), bp_lv)
                    if not reward_at_lv:
                        continue
                    reward_record = reward_records.get(str(bp_type), None)
                    if reward_record is None:
                        is_received = False if 1 else reward_record.is_record(bp_lv)
                        if not is_received:
                            return False

            return True

    def has_set_hide_newbiepass_ui(self):
        return self.get_hide_newbiepass_ui_setting() == 1 and self.has_received_all_newbiepass_reward()

    def get_hide_newbiepass_ui_setting(self):
        from logic.gcommon.common_const import ui_operation_const
        return global_data.player.get_setting(ui_operation_const.NEWBIE_PASS_HIDE_UI, 0)

    def write_hide_newbiepass_ui_setting(self, option=1):
        from logic.gcommon.common_const import ui_operation_const
        self.write_setting(ui_operation_const.NEWBIE_PASS_HIDE_UI, option, upload=True)
        self.save_settings_to_file()