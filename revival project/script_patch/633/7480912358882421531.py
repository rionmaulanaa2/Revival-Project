# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/FireSurvivalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple

class FireSurvivalBattle(SurvivalBattle):

    def __init__(self, entityid):
        super(FireSurvivalBattle, self).__init__(entityid)
        self._cur_fire_num = 0
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'resolution_changed': self.on_resolution_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self, clear_cache=True):
        super(FireSurvivalBattle, self).destroy(clear_cache)
        self.process_event(False)

    def init_from_dict(self, bdict):
        self.reconnect_handle_data(bdict)
        super(FireSurvivalBattle, self).init_from_dict(bdict)
        self._show_tip_cache = False
        self._timestamp_cache = 0
        self._cache_valid = False

    def load_finish(self):
        super(FireSurvivalBattle, self).load_finish()
        self.reconnect_handle_fire_region()
        self.reconnect_handle_fire_num()
        self.reconnect_handle_region_timestamp()
        self.reconnect_handle_pc()

    def on_resolution_changed(self):
        if self._cache_valid:
            self.update_fire_region_timestamp(self._timestamp_cache, self._show_tip_cache)

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'), Bool('show_tip')))
    def init_fire_region_refresh_tips(self, init_timestamp, show_tip):
        self.update_fire_region_timestamp(init_timestamp, show_tip)

    @rpc_method(CLIENT_STUB, (Dict('region_dict'),))
    def init_fire_region(self, region_dict):
        self.on_init_fire_region({'fire_region': region_dict})

    def on_init_fire_region(self, region_dict):
        global_data.fire_sur_battle_mgr.update_fire_regions(region_dict)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        super(FireSurvivalBattle, self).fight_stage((stage_dict,))
        fire_region_dict = stage_dict.get('fire_region_dict')
        self.on_init_fire_region(fire_region_dict)
        timestamp = stage_dict.get('fire_region_refresh_timestamp')
        show_tip = stage_dict.get('fire_region_show_tip')
        if timestamp:
            self.update_fire_region_timestamp(timestamp, show_tip)

    def reconnect_handle_data(self, bdict):
        self.reconnect_data = {'fire_region_dict': bdict.get('fire_region_dict', {}),
           'fire_region_refresh_timestamp': bdict.get('fire_region_refresh_timestamp'),
           'fire_region_show_tip': bdict.get('fire_region_show_tip'),
           'put_fire_num': bdict.get('put_fire_num', 0)
           }

    def reconnect_handle_fire_region(self):
        fire_region_dict = self.reconnect_data.get('fire_region_dict', {})
        global_data.fire_sur_battle_mgr.update_fire_regions(fire_region_dict)

    def reconnect_handle_fire_num(self):
        put_fire_num = self.reconnect_data.get('put_fire_num', 0)
        self.on_update_fire_num(put_fire_num)

    def reconnect_handle_region_timestamp(self):
        timestamp = self.reconnect_data.get('fire_region_refresh_timestamp')
        show_tip = self.reconnect_data.get('fire_region_show_tip')
        if timestamp:
            self.update_fire_region_timestamp(timestamp, show_tip)

    def reconnect_handle_pc(self):
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def update_fire_region_timestamp(self, timestamp, show_tip):
        self._cache_valid = True
        self._timestamp_cache = timestamp
        self._show_tip_cache = show_tip
        global_data.emgr.update_fire_region_timestamp.emit(timestamp, show_tip)

    @rpc_method(CLIENT_STUB, ())
    def notify_fire_region_refresh(self):
        from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_REFRESH_TIPS, MAIN_NODE_COMMON_INFO
        message = {'i_type': GRANBELM_PORTAL_REFRESH_TIPS,'content_txt': 17316}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, (Int('fire_num'),))
    def put_fire_num(self, fire_num):
        self.on_update_fire_num(fire_num)

    def on_update_fire_num(self, fire_num):
        self._cur_fire_num = fire_num
        global_data.emgr.update_fire_count.emit(fire_num)

    def get_fire_num(self):
        return self._cur_fire_num

    @rpc_method(CLIENT_STUB, (Int('fire_num'),))
    def region_fire_num_tip(self, fire_num):
        self.on_region_fire_num_tip(fire_num)

    def on_region_fire_num_tip(self, fire_num):
        from logic.gcommon.common_const.battle_const import FIRE_BATTLE_FIRE_STATE_TIPS, MAIN_NODE_COMMON_INFO
        if fire_num > 0:
            message = {'i_type': FIRE_BATTLE_FIRE_STATE_TIPS,'content_txt': get_text_by_id(17313, {'num': fire_num})}
        else:
            message = {'i_type': FIRE_BATTLE_FIRE_STATE_TIPS,'content_txt': get_text_by_id(17319)}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, ())
    def fire_immune_tip(self):
        self.on_fire_immune_tips()

    def on_fire_immune_tips(self):
        from logic.gcommon.common_const.battle_const import FIRE_BATTLE_IMMUNE_TIPS, MAIN_NODE_COMMON_INFO
        message = {'i_type': FIRE_BATTLE_IMMUNE_TIPS,'content_txt': ''}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, ())
    def notify_fire_reward_tip(self):
        self.on_notify_fire_reward_tip()

    def on_notify_fire_reward_tip(self):
        from logic.gcommon.common_const.battle_const import FIRE_BATTLE_HAVE_AWARD_TIPS, MAIN_NODE_COMMON_INFO
        message = {'i_type': FIRE_BATTLE_HAVE_AWARD_TIPS,'content_txt': ''}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)