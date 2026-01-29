# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GranbelmSurvivalBattle.py
from __future__ import absolute_import
import six
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_FIRST_TELEPORT, GRANBELM_PORTAL_SECOND_TELEPORT, GRANBELM_PORTAL_REFRESH_TIPS, MAIN_NODE_COMMON_INFO, GRANBELM_TELE_CALLBACK_STATE_FAIL
from logic.gutils import granbelm_utils
import math3d

class GranbelmSurvivalBattle(SurvivalBattle):

    def __init__(self, entityid):
        super(GranbelmSurvivalBattle, self).__init__(entityid)
        global_data.emgr.resolution_changed += self.on_resolution_changed

    def init_from_dict(self, bdict):
        self.reconnect_handle_data(bdict)
        super(GranbelmSurvivalBattle, self).init_from_dict(bdict)
        self._show_tip_cache = False
        self._timestamp_cache = 0
        self._cache_valid = False

    def load_finish(self):
        super(GranbelmSurvivalBattle, self).load_finish()
        self.reconnect_handle_below_col()
        self.reconnect_handle_rune_region()
        self.reconnect_handle_ui_visible()
        self.reconnect_handle_region_timestamp()
        self.reconnect_handle_pc()

    def on_resolution_changed(self):
        if self._cache_valid:
            self.update_rune_region_timestamp(self._timestamp_cache, self._show_tip_cache)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('portal_type'), Str('tele_role'), Int('tele_stage'), Tuple('below_pos'), Bool('tele_tag')))
    def granbelm_teleport_single(self, entity_id, portal_type, tele_role, tele_stage, below_pos, tele_tag):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.is_valid():
            return
        if global_data.cam_lplayer.id == entity_id:
            if tele_stage == GRANBELM_PORTAL_FIRST_TELEPORT:
                global_data.ui_mgr.set_all_ui_visible(False)
                global_data.gran_sur_battle_mgr.create_tele_screen_sfx(portal_type)
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', granbelm_utils.get_tele_sound_map(portal_type, 0)))
                global_data.emgr.scene_stop_poison_circle.emit()
                global_data.gran_sur_battle_mgr.set_tele_tag(tele_tag)
                if granbelm_utils.check_switch_model_visible():
                    global_data.cam_lplayer.ev_g_control_target().logic.send_event('E_HIDE_MODEL')
                global_data.gran_sur_battle_mgr.create_below_col(below_pos)
                if global_data.pc_ctrl_mgr:
                    global_data.pc_ctrl_mgr.enable_keyboard_control(False)
            elif tele_stage == GRANBELM_PORTAL_SECOND_TELEPORT:
                global_data.ui_mgr.set_all_ui_visible(True)
                global_data.emgr.scene_recover_poison_circle.emit()
                global_data.gran_sur_battle_mgr.set_tele_tag(tele_tag)
                if granbelm_utils.check_switch_model_visible():
                    global_data.cam_lplayer.ev_g_control_target().logic.send_event('E_SHOW_MODEL')
                global_data.gran_sur_battle_mgr.destroy_below_col()
                if global_data.pc_ctrl_mgr:
                    global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    @rpc_method(CLIENT_STUB, (Int('portal_type'), Str('tele_role'), Int('tele_stage'), Tuple('tele_pos')))
    def granbelm_teleport_all(self, portal_type, tele_role, tele_stage, tele_pos):
        global_data.gran_sur_battle_mgr.create_tele_sfx(portal_type, tele_role, tele_stage, tele_pos)
        if tele_stage == GRANBELM_PORTAL_SECOND_TELEPORT:
            global_data.sound_mgr.play_sound('Play_ui_notice', math3d.vector(tele_pos[0], tele_pos[1], tele_pos[2]), ('ui_notice', granbelm_utils.get_tele_sound_map(portal_type, 1)))

    @rpc_method(CLIENT_STUB, (Int('portal_type'),))
    def granbelm_refresh_portal(self, portal_type):
        message = {'i_type': GRANBELM_PORTAL_REFRESH_TIPS}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'), Bool('show_tip')))
    def init_rune_region_refresh_tips(self, init_timestamp, show_tip):
        self.update_rune_region_timestamp(init_timestamp, show_tip)

    @rpc_method(CLIENT_STUB, (Tuple('region_pos'), Float('region_r'), Int('region_level')))
    def init_rune_region(self, region_pos, region_r, region_level):
        global_data.gran_sur_battle_mgr.set_region_param(region_pos, region_r, region_level)
        global_data.emgr.init_granbelm_rune_region.emit(region_pos, region_r, region_level)

    @rpc_method(CLIENT_STUB, (Int('region_level'),))
    def remove_rune_region(self, region_level):
        param_list = global_data.gran_sur_battle_mgr.get_region_param()
        if param_list:
            level = param_list[2]
            if region_level == level:
                global_data.gran_sur_battle_mgr.set_region_param(None, None, None)
        global_data.emgr.remove_granbelm_rune_region.emit(region_level)
        return

    @rpc_method(CLIENT_STUB, (Int('tele_callback_state'),))
    def update_tele_state(self, tele_callback_state):
        if tele_callback_state == GRANBELM_TELE_CALLBACK_STATE_FAIL:
            global_data.gran_sur_battle_mgr.set_tele_tag(False)

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

        rune_region_dict = stage_dict.get('rune_region_dict')
        region_wpos = rune_region_dict.get('region_center')
        region_radius = rune_region_dict.get('region_radius')
        if region_wpos and region_radius and not global_data.gran_sur_battle_mgr.get_region_param():
            region_level = rune_region_dict.get('region_level')
            global_data.gran_sur_battle_mgr.set_region_param(region_wpos, region_radius, region_level)
            global_data.emgr.init_granbelm_rune_region.emit(region_wpos, region_radius, region_level)
        timestamp = stage_dict.get('rune_region_timestamp')
        show_tip = stage_dict.get('rune_region_show_tip')
        if timestamp:
            self.update_rune_region_timestamp(timestamp, show_tip)

    def reconnect_handle_data(self, bdict):
        self.reconnect_data = {'tele_dict': bdict.get('tele_dict'),
           'rune_region_dict': bdict.get('rune_region_dict'),
           'rune_region_timestamp': bdict.get('rune_region_refresh_timestamp'),
           'rune_region_show_tip': bdict.get('rune_region_show_tip')
           }

    def reconnect_handle_below_col(self):
        tele_dict = self.reconnect_data.get('tele_dict')
        tele_tag = tele_dict.get('tele_tag')
        global_data.gran_sur_battle_mgr.set_tele_tag(tele_tag)
        if tele_tag:
            below_pos = tele_dict.get('below_pos')
            global_data.gran_sur_battle_mgr.create_below_col(below_pos)
        else:
            global_data.gran_sur_battle_mgr.destroy_below_col()

    def reconnect_handle_rune_region(self):
        rune_region_dict = self.reconnect_data.get('rune_region_dict')
        region_wpos = rune_region_dict.get('region_center')
        region_radius = rune_region_dict.get('region_radius')
        if region_wpos and region_radius:
            region_level = rune_region_dict.get('region_level')
            global_data.gran_sur_battle_mgr.set_region_param(region_wpos, region_radius, region_level)
            global_data.emgr.init_granbelm_rune_region.emit(region_wpos, region_radius, region_level)

    def reconnect_handle_ui_visible(self):
        tele_dict = self.reconnect_data.get('tele_dict')
        tele_tag = tele_dict.get('tele_tag')
        if tele_tag:
            global_data.ui_mgr.set_all_ui_visible(False)

    def reconnect_handle_region_timestamp(self):
        timestamp = self.reconnect_data.get('rune_region_timestamp')
        show_tip = self.reconnect_data.get('rune_region_show_tip')
        if timestamp:
            self.update_rune_region_timestamp(timestamp, show_tip)

    def reconnect_handle_pc(self):
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def update_rune_region_timestamp(self, timestamp, show_tip):
        self._cache_valid = True
        self._timestamp_cache = timestamp
        self._show_tip_cache = show_tip
        global_data.emgr.update_rune_region_timestamp.emit(timestamp, show_tip)