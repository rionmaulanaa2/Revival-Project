# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/SnatchEggBattle.py
from __future__ import absolute_import
import six_ex
from collections import defaultdict
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon import time_utility as tutil
from logic.entities.Battle import Battle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Uuid, Dict, Float, Str, List
import math
import math3d
from logic.gcommon.common_const import scene_const
from logic.gutils.CameraHelper import get_adaptive_camera_fov
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility
from logic.gcommon.common_const import battle_const as bconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gcommon import time_utility as t_util
INTERVAL_HIDE_UI_LIST = [
 'MechaUI',
 'FireRockerUI',
 'PostureControlUI',
 'MoveRockerUI',
 'MoveRockerTouchUI',
 'BulletReloadUI',
 'FightLeftShotUI',
 'HpInfoUI']

class SnatchEggBattle(DeathBattle):

    def __init__(self, entityid):
        super(SnatchEggBattle, self).__init__(entityid)
        self.our_group_egg_cnt = 0
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, bdict):
        self._round_settle_timestamp = bdict.get('round_settle_timestamp', 0)
        self._round_prepare_timestamp = bdict.get('round_prepare_timestamp')
        self._round_status = bdict.get('round_status')
        self.battle_bdict = bdict
        self.map_id = bdict.get('map_id')
        self.area_id = bdict.get('area_id')
        self.egg_list = bdict.get('egg_list')
        self._all_group_ids = bdict.get('all_group_ids')
        self.show_group_list = []
        super(SnatchEggBattle, self).init_from_dict(bdict)

    @rpc_method(CLIENT_STUB, (Dict('round_interval_data'),))
    def snatchegg_round_interval(self, round_interval_data):
        self._group_left_time_dict = round_interval_data.get('group_left_time_dict', {})
        self._crystal_round = round_interval_data.get('cur_round')
        self._round_prepare_timestamp = round_interval_data.get('round_prepare_timestamp')
        self._round_status = round_interval_data.get('round_status')
        self._moneybox_position = round_interval_data.get('moneybox_position')
        self.egg_list = round_interval_data.get('egg_list')
        self.enter_interval_view()
        global_data.emgr.snatchegg_round_interval_event.emit()
        global_data.ui_mgr.close_ui('MechaSummonUI')
        global_data.ui_mgr.close_ui('MechaSummonAndChooseSkinUI')
        global_data.emgr.death_in_base_part_change.emit()

    def enter_interval_view(self):
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_PLAY_VICTORY_CAMERA')
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_PLAY_VICTORY_CAMERA')
        global_data.ui_mgr.hide_all_ui_by_key('snatcheggbattle', INTERVAL_HIDE_UI_LIST)

    def exit_interval_view(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_EXIT_FOCUS_CAMERA')
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_EXIT_FOCUS_CAMERA')
        global_data.ui_mgr.revert_hide_all_ui_by_key_action('snatcheggbattle', INTERVAL_HIDE_UI_LIST)

    @rpc_method(CLIENT_STUB, (Dict('round_begin_data'),))
    def snatchegg_round_begin(self, round_begin_data):
        self._round_settle_timestamp = round_begin_data.get('round_settle_timestamp')
        self._snatchegg_round = round_begin_data.get('cur_round')
        self._round_status = round_begin_data.get('round_status')
        self.show_round_begin_tip()
        global_data.death_battle_data.is_ready_state = False
        global_data.emgr.death_in_base_part_change.emit()
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)
        global_data.emgr.snatchegg_round_begin_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('settle_info'),))
    def settle_round(self, settle_info):
        knock_out_group = settle_info.get('knock_out_group', [])
        for gid in knock_out_group:
            if gid in self._all_group_ids:
                self._all_group_ids.remove(gid)

        self.on_settle_round(knock_out_group)

    def on_settle_round(self, knock_out_group):
        if not (global_data.player and global_data.player.logic):
            return
        is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()

        def show_round():

            def cb():
                from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
                stop_self_fire_and_movement()
                from logic.comsys.battle.SnatchEgg.SnatchEggEndUI import SnatchEggPromoteUI
                SnatchEggPromoteUI(None, {}, None, 5)
                return

            import game3d
            game3d.delay_exec(1200, lambda : cb())

        if is_in_spectate:
            if not global_data.cam_lplayer:
                return
            g_id = global_data.cam_lplayer.ev_g_group_id()
            is_win = g_id not in knock_out_group and g_id in self._all_group_ids
            if is_win:
                show_round()
            return
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        g_id = global_data.player.logic.ev_g_group_id()
        is_win = g_id not in knock_out_group and g_id in self._all_group_ids
        if is_win:
            show_round()

    @rpc_method(CLIENT_STUB, (List('egg_list'),))
    def create_goldeneggs(self, egg_list):
        self.egg_list = egg_list
        tip_type = bconst.SNATCHEGG_CREATE_EGG_TIP
        message = {'i_type': tip_type,'in_anim': 'appear','out_anim': 'disappear'}
        global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
        global_data.emgr.update_battle_data.emit()

    def show_round_begin_tip(self):
        if self._snatchegg_round is None:
            return
        else:
            round_no = self._snatchegg_round + 1
            text = get_text_by_id(17945, [round_no])
            tip_type = bconst.SNATCHEGG_ROUND_TIP
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            return

    def get_snatchegg_round(self):
        return self._snatchegg_round

    @rpc_method(CLIENT_STUB, (Dict('round_end_data'),))
    def snatchegg_round_stop(self, round_end_data):
        global_data.death_battle_data.set_egg_picker_dict({})
        self.our_group_egg_cnt = 0
        self._round_settle_timestamp = round_end_data.get('round_settle_timestamp')
        self._snatchegg_round = round_end_data.get('cur_round')
        self.show_round_end_tip()
        global_data.emgr.snatchegg_round_stop_event.emit()

    def show_round_end_tip(self):
        if self._snatchegg_round is None:
            return
        else:
            round_no = self._snatchegg_round + 1
            text = get_text_by_id(17930, [round_no])
            tip_type = bconst.SNATCHEGG_ROUND_TIP
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            return

    @rpc_method(CLIENT_STUB, (Dict('clean_up_data'),))
    def start_clean_up_all_soul(self, clean_up_data):
        self.exit_interval_view()

    @rpc_method(CLIENT_STUB, ())
    def start_set_out_all_soul(self):
        global_data.death_battle_data.is_ready_state = True
        global_data.game_mode.mode and global_data.game_mode.mode.init_player_rotation()
        if not self.is_knocked_out() or self.is_in_spectate():
            self.show_interval_count_down()

    def show_interval_count_down(self):
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_prepare_timestamp)
        if self._round_status != bconst.ROUND_STATUS_INTERVAL:
            return
        else:
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            revive_time = self._round_prepare_timestamp - t_util.time()
            ui.on_delay_close(revive_time, None)
            return

    def get_prepare_left_time(self):
        return self._round_prepare_timestamp

    def get_round_left_time(self):
        return int(math.ceil(self._round_settle_timestamp - tutil.time()))

    def get_round_status(self):
        return self._round_status

    def is_knocked_out(self):
        if not (global_data.player and global_data.player.logic):
            return True
        return global_data.player.logic.ev_g_group_id() not in self._all_group_ids

    def is_in_spectate(self):
        if not (global_data.player and global_data.player.logic):
            return False
        return global_data.player.logic.ev_g_is_in_spectate()

    def destroy(self, clear_cache=True):
        self.process_event(False)
        super(SnatchEggBattle, self).destroy(clear_cache)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.death_battle_data.set_settle_timestamp(settle_timestamp)
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), List('born_point_list'), Dict('group_born_dict'), Dict('group_points_dict'), Dict('selected_combat_weapons'), Dict('extra_data')))
    def update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons, extra_data):
        self._update_snatchegg_data(extra_data)
        self._update_battle_data(settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons)

    def _update_snatchegg_data(self, extra_data):
        self._round_settle_timestamp = extra_data.get('round_settle_timestamp')
        self.temp_mecha_info = extra_data.get('picker_mecha_info')
        self.egg_list = extra_data.get('egg_list', [])
        self._all_group_ids = extra_data.get('all_group_ids', [])
        global_data.death_battle_data.set_egg_picker_dict(extra_data.get('egg_picker_dict', {}))
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)
        global_data.emgr.update_battle_data.emit()

    def on_player_setted(self, player):
        self.show_group_list = self.get_show_group_list()

    def get_show_group_list(self):
        if self.show_group_list:
            return self.show_group_list
        else:
            group_dict = self.group_loading_dict
            group_list = sorted(six_ex.keys(group_dict))
            a_group_id = None
            if global_data.player:
                for gid, g_info in six_ex.items(group_dict):
                    if global_data.player.id in g_info:
                        a_group_id = gid
                        break

            if a_group_id in group_list:
                group_list.remove(a_group_id)
                group_list.insert(0, a_group_id)
            self.show_group_list = group_list
            return group_list
            return

    def get_all_group_ids(self):
        return self._all_group_ids or []

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        pass