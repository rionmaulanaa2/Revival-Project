# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GravitySurvivalBattle.py
from __future__ import absolute_import
import six
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gutils import gravity_mode_utils

class GravitySurvivalBattle(SurvivalBattle):

    def __init__(self, entityid):
        super(GravitySurvivalBattle, self).__init__(entityid)
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
        super(GravitySurvivalBattle, self).destroy(clear_cache)
        self.process_event(False)

    def init_from_dict(self, bdict):
        self.reconnect_handle_data(bdict)
        super(GravitySurvivalBattle, self).init_from_dict(bdict)
        self._show_tip_cache = False
        self._timestamp_cache = 0
        self._cache_valid = False

    def load_finish(self):
        super(GravitySurvivalBattle, self).load_finish()
        self.reconnect_handle_gravity_region()
        self.reconnect_handle_region_timestamp()
        self.reconnect_handle_pc()

    def on_resolution_changed(self):
        if self._cache_valid:
            self.update_gravity_region_timestamp(self._timestamp_cache, self._show_tip_cache)

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'), Bool('show_tip')))
    def init_gravity_region_refresh_tips(self, init_timestamp, show_tip):
        self.update_gravity_region_timestamp(init_timestamp, show_tip)

    @rpc_method(CLIENT_STUB, (Tuple('region_pos'), Float('region_r'), Int('region_level')))
    def init_less_gravity_region(self, region_pos, region_r, region_level):
        global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.LESS_GRAVITY, [(region_pos, region_r, region_level)])
        global_data.emgr.init_gravity_region.emit(gravity_mode_utils.LESS_GRAVITY)

    @rpc_method(CLIENT_STUB, (Tuple('region_pos'), Float('region_r'), Int('region_level')))
    def init_over_gravity_region(self, region_pos, region_r, region_level):
        global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.OVER_GRAVITY, [(region_pos, region_r, region_level)])
        global_data.emgr.init_gravity_region.emit(gravity_mode_utils.OVER_GRAVITY)

    @rpc_method(CLIENT_STUB, (Int('region_level'),))
    def remove_gravity_region(self, region_level):
        self.remove_gravity_region_by_type(gravity_mode_utils.LESS_GRAVITY)
        self.remove_gravity_region_by_type(gravity_mode_utils.OVER_GRAVITY)

    def remove_gravity_region_by_type(self, type):
        global_data.gravity_sur_battle_mgr.set_region_param()
        global_data.emgr.remove_gravity_region.emit(type)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        battle_mark = stage_dict.get('mark_dict', {})
        self.update_player_num((player_num,))
        self.on_battle_status_changed(Battle.BATTLE_STATUS_FIGHT)
        global_data.player.logic and global_data.player.logic.send_event('E_START_POSITION_CHECKER')
        self.init_poison_circle(poison_circle)
        global_mark_dict = battle_mark.get('global_mark_dict', {})
        group_mark_dict = battle_mark.get('group_mark_dict', {})
        soul_mark_dict = battle_mark.get('soul_mark_dict', {})
        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(global_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(group_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(soul_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        gravity_region_dict = stage_dict.get('gravity_region_dict')
        self.set_gravity_region_dict(gravity_region_dict)
        timestamp = stage_dict.get('gravity_region_refresh_timestamp')
        show_tip = stage_dict.get('gravity_region_show_tip')
        if timestamp:
            self.update_gravity_region_timestamp(timestamp, show_tip)

    def set_gravity_region_dict(self, gravity_region_dict):
        if not gravity_region_dict:
            return
        less_region_center = gravity_region_dict.get('less_region_center')
        less_region_radius = gravity_region_dict.get('less_region_radius')
        over_region_center = gravity_region_dict.get('over_region_center')
        over_region_radius = gravity_region_dict.get('over_region_radius')
        region_level = gravity_region_dict.get('region_level')
        if less_region_center and less_region_radius and not global_data.gravity_sur_battle_mgr.get_region_param(gravity_mode_utils.LESS_GRAVITY):
            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.LESS_GRAVITY, [(less_region_center, less_region_radius, region_level)])
            global_data.emgr.init_gravity_region.emit(gravity_mode_utils.LESS_GRAVITY)
        if over_region_center and over_region_radius and not global_data.gravity_sur_battle_mgr.get_region_param(gravity_mode_utils.OVER_GRAVITY):
            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.OVER_GRAVITY, [(over_region_center, over_region_radius, region_level)])
            global_data.emgr.init_gravity_region.emit(gravity_mode_utils.OVER_GRAVITY)

    def reconnect_handle_data(self, bdict):
        self.reconnect_data = {'gravity_region_dict': bdict.get('gravity_region_dict'),
           'gravity_region_refresh_timestamp': bdict.get('gravity_region_refresh_timestamp'),
           'gravity_region_show_tip': bdict.get('gravity_region_show_tip')
           }

    def reconnect_handle_gravity_region(self):
        gravity_region_dict = self.reconnect_data.get('gravity_region_dict')
        self.set_gravity_region_dict(gravity_region_dict)

    def reconnect_handle_region_timestamp(self):
        timestamp = self.reconnect_data.get('gravity_region_refresh_timestamp')
        show_tip = self.reconnect_data.get('gravity_region_show_tip')
        if timestamp:
            self.update_gravity_region_timestamp(timestamp, show_tip)

    def reconnect_handle_pc(self):
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def update_gravity_region_timestamp(self, timestamp, show_tip):
        self._cache_valid = True
        self._timestamp_cache = timestamp
        self._show_tip_cache = show_tip
        global_data.emgr.update_gravity_region_timestamp.emit(timestamp, show_tip)

    @rpc_method(CLIENT_STUB, ())
    def notify_gravity_refresh(self):
        from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_REFRESH_TIPS, MAIN_NODE_COMMON_INFO
        message = {'i_type': GRANBELM_PORTAL_REFRESH_TIPS,'content_txt': 19881}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)