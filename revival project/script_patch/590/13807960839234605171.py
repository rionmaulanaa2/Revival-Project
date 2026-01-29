# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impPvePlay.py
from __future__ import absolute_import
from __future__ import print_function
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, List, Dict, Bool, Float, Uuid
from logic.gutils.granbelm_utils import check_switch_model_visible

class impPvePlay(object):

    def _init_pveplay_from_dict(self, bdict):
        self._fight_state = bdict.get('fight_state', False)
        self._win_pve = bdict.get('win_pve', False)
        self._pve_player_size_mode = bdict.get('pve_player_size_mode', 0)
        self._dead_id_list = bdict.get('dead_id_list', [])
        self._pve_boss_eid = None
        return

    def _init_pveplay_completed(self, bdict):
        self.mission_data = bdict.get('target_data', {})
        self.guide_data = bdict.get('guide_data', {})
        if self.mission_data:
            self.show_level_mission_imp(self.mission_data)
        for guide_id, guide_pos in six.iteritems(self.guide_data):
            self.show_dest_guide_imp(guide_pos, guide_id)

    def get_pve_player_size_mode(self):
        return self._pve_player_size_mode

    def _tick_pveplay(self, delta):
        pass

    def _destroy_pveplay(self, clear_cache):
        pass

    @rpc_method(CLIENT_STUB, (Int('tip_type'), Int('text_id'), Int('text_id_2')))
    def show_level_tip(self, tip_type, text_id, text_id_2):
        global_data.emgr.pve_level_tips.emit(tip_type, text_id, text_id_2)

    @rpc_method(CLIENT_STUB, (Dict('mission_data'),))
    def show_level_mission(self, mission_data):
        self.mission_data = mission_data
        self.show_level_mission_imp(mission_data)

    def show_level_mission_imp(self, mission_data):
        print('show_level_mission', mission_data)
        ui = global_data.ui_mgr.get_ui('PVETipsUI')
        ui and ui.set_mission(mission_data)

    @rpc_method(CLIENT_STUB, (List('guide_pos'), Int('guide_id')))
    def show_dest_guide(self, guide_pos, guide_id):
        self.show_dest_guide_imp(guide_pos, guide_id)

    def clear_all_tips(self):
        self.guide_data = {}
        self.mission_data = {}

    def show_dest_guide_imp(self, guide_pos, guide_id):
        print('show_dest_guide', guide_id, guide_pos, end=' ')
        self.guide_data[guide_id] = guide_pos
        ui = global_data.ui_mgr.get_ui('PVETipsUI')
        ui and ui.set_guide_pos(guide_id, guide_pos)
        ui = global_data.ui_mgr.get_ui('PVERadarMapUI')
        ui and ui.set_guide_pos(guide_id, guide_pos)

    @rpc_method(CLIENT_STUB, (Int('guide_id'),))
    def clear_dest_guide(self, guide_id):
        print('clear_dest_guide', guide_id)
        ui = global_data.ui_mgr.get_ui('PVETipsUI')
        ui and ui.clear_guide_pos(guide_id)
        ui = global_data.ui_mgr.get_ui('PVERadarMapUI')
        ui and ui.clear_guide_pos(guide_id)
        self.guide_data.pop(guide_id, None)
        return

    @rpc_method(CLIENT_STUB, (Bool('fight_state'),))
    def change_fight_state(self, fight_state):
        print('change_fight_state', fight_state)
        if fight_state != self._fight_state:
            is_boss = True if self._pve_boss_eid else False
            global_data.emgr.pve_fight_state_changed.emit(fight_state, is_boss)
        self._fight_state = fight_state

    def get_fight_state(self):
        return self._fight_state

    def wait_choose_bless(self, node_id, bless_list, extra_data):
        ui = global_data.ui_mgr.show_ui('PVEBlessConfUI', 'logic.comsys.battle.pve')
        ui.init_bless(node_id, bless_list, extra_data)

    def wait_choose_break(self, node_id, break_list, extra_data):
        ui = global_data.ui_mgr.show_ui('PVEBreakConfUI', 'logic.comsys.battle.pve')
        ui.init_break(node_id, break_list, extra_data)

    def open_shop(self, shop_eid, goods_data, refresh_price):
        ui = global_data.ui_mgr.get_ui('PVEShopUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('PVEShopUI', 'logic.comsys.battle.pve')
        ui.init_goods(shop_eid, goods_data, refresh_price)

    def request_pve_battle_info(self):
        self.call_soul_method('request_pve_battle_info')

    @rpc_method(CLIENT_STUB, (Dict('battle_info'),))
    def reply_pve_battle_info(self, battle_info):
        global_data.emgr.pve_battle_info_event.emit(battle_info)

    @rpc_method(CLIENT_STUB, (Str('sfx_path'), List('pos'), Float('scale'), Float('rate')))
    def play_sfx_in_scene(self, sfx_path, pos, scale=1.0, rate=1.0):
        import math3d
        v3d_pos = math3d.vector(*pos)

        def cb(sfx):
            sfx.scale = math3d.vector(scale, scale, scale)
            sfx.frame_rate = rate

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, v3d_pos, on_create_func=cb)

    @rpc_method(CLIENT_STUB, ())
    def on_pve_win(self):
        self._win_pve = True

    def get_pve_win_ret(self):
        return self._win_pve

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('alive_mecha_cnt')))
    def on_mecha_destroyed(self, soul_id, alive_mecha_cnt):
        if soul_id not in self._dead_id_list:
            self._dead_id_list.append(soul_id)
        if not global_data.player or not global_data.player.logic:
            return
        if soul_id == global_data.player.id and alive_mecha_cnt > 0:
            global_data.emgr.pve_team_defeat_event.emit()
            global_data.player.logic.send_event('E_REQ_SPECTATE', 1.3, True)

    @rpc_method(CLIENT_STUB, (Str('rescuer_name'),))
    def on_pve_mecha_revive(self, rescuer_name):
        global_data.emgr.pve_team_revive_event.emit(rescuer_name)

    @rpc_method(CLIENT_STUB, ())
    def on_pve_mecha_revive_end(self):
        global_data.emgr.pve_team_revive_end_event.emit()

    @rpc_method(CLIENT_STUB, (Int('chapter'),))
    def play_pve_boss_video(self, chapter):
        from logic.gcommon.common_const.pve_const import VIDEO_RES
        res_path = VIDEO_RES.get(chapter, None)
        if res_path:
            from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
            stop_self_fire_and_movement(True)

            def cb(*args):
                pass

            from common.cinematic.VideoPlayer import VideoPlayer
            VideoPlayer().play_video(res_path, cb, repeat_time=1, can_jump=False)
        return

    def set_pve_boss_eid(self, eid):
        self._pve_boss_eid = eid

    def get_pve_boss_eid(self):
        return self._pve_boss_eid

    @rpc_method(CLIENT_STUB, ())
    def on_pve_roll_back(self):
        from logic.gutils.screen_effect_utils import create_screen_effect_directly
        from logic.gcommon.common_const.pve_const import PVE_RB_SFX
        import game3d

        def cb(sfx):
            sfx.frame_rate = 2.0

        global_data.ui_mgr.set_all_ui_visible(False)
        create_screen_effect_directly(PVE_RB_SFX, on_create_func=cb, on_remove_func=self.rb_callback)
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'portal2_process'))
        global_data.cam_lctarget and global_data.cam_lctarget.send_event('E_HIDE_MODEL')
        game3d.delay_exec(2100, self.rb_callback)

    def rb_callback(self, *args):
        global_data.ui_mgr.set_all_ui_visible(True)
        global_data.cam_lctarget and global_data.cam_lctarget.send_event('E_SHOW_MODEL')