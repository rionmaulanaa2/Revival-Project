# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/TrainBattle.py
from __future__ import absolute_import
from six.moves import range
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility
import math3d
from logic.entities.DeathBattle import DeathBattle
from collections import defaultdict
from logic.comsys.battle.Train.TrainBattleMgr import TrainBattleMgr
from logic.gutils.scene_utils import is_in_lobby
INTERVAL_HIDE_UI_LIST = [
 'MechaUI',
 'FireRockerUI',
 'PostureControlUI',
 'MoveRockerUI',
 'MoveRockerTouchUI',
 'BulletReloadUI',
 'FightLeftShotUI',
 'HpInfoUI']

class TrainBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        self.show_to_next_station_tips = {}
        self._atk_group_id = bdict.get('atk_group_id')
        self._def_group_id = bdict.get('def_group_id')
        self._skill_power = bdict.get('power_dic')
        self._old_atk_group_id = bdict.get('old_atk_group_id')
        self._old_def_group_id = bdict.get('old_def_group_id')
        self._my_group_id = bdict.get('my_group_id')
        self._round = bdict.get('cur_round')
        self._round_timestamp = bdict.get('round_settle_timestamp', 0)
        self._last_round_dis = -1
        self._last_round_left_time = -1
        self._round_train_dis = bdict.get('round_train_dis', {})
        self._round_settle_res_time = bdict.get('round_settle_res_time', {})
        self._round_status = bdict.get('round_status')
        self._enable_in_train_check = bdict.get('enable_in_train_check', False)
        self._last_cache_range_player = []
        super(TrainBattle, self).init_from_dict(bdict)
        if not global_data.train_battle_mgr:
            TrainBattleMgr()
        self.play_data = global_data.game_mode.get_cfg_data('play_data')
        global_data.emgr.update_train_small_map_icon.emit()
        if global_data.game_mgr.scene and not is_in_lobby(global_data.game_mgr.scene.scene_type):
            global_data.train_battle_mgr.create_extra_model_in_scene()

    def load_finish(self):
        super(TrainBattle, self).load_finish()
        if global_data.train_battle_mgr:
            global_data.train_battle_mgr.create_extra_model_in_scene()
        global_data.death_battle_data.check_pos()

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.death_battle_data.set_settle_timestamp(self.settle_timestamp)
        if self._round_timestamp:
            global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_timestamp)

    @rpc_method(CLIENT_STUB, (List('players'),))
    def update_valid_range_player(self, players):
        if not players:
            players = []
        self._last_cache_range_player = players
        num_atk, num_def = self.update_range_player(players)
        global_data.train_battle_mgr.update_train_skill_screen_sfx(players)
        global_data.train_battle_mgr.update_train_range_sfx_state(num_atk, num_def)
        global_data.emgr.update_train_around_state.emit(num_atk, num_def)

    @rpc_method(CLIENT_STUB, (Float('round_timestamp'),))
    def update_round_settle_timestamp(self, round_timestamp):
        self._round_timestamp = round_timestamp
        global_data.emgr.crystal_round_settle_timestamp_event.emit(round_timestamp)

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    @rpc_method(CLIENT_STUB, (Dict('round_end_data'),))
    def train_round_end(self, round_end_data):
        self._old_atk_group_id = round_end_data.get('old_atk_group_id')
        self._old_def_group_id = round_end_data.get('old_def_group_id')
        self._last_round_dis = round_end_data.get('last_round_dis')
        self._last_round_left_time = round_end_data.get('last_round_left_time')
        self.show_round_end_tip()

    @rpc_method(CLIENT_STUB, (Dict('clean_up_data'),))
    def start_clean_up_all_soul(self, clean_up_data):
        self.exit_interval_view()

    @rpc_method(CLIENT_STUB, (Dict('round_interval_data'),))
    def train_round_interval(self, round_interval_data):
        self.enter_interval_view()
        global_data.game_mgr.get_logic_timer().register(func=lambda : global_data.ui_mgr.show_ui('TrainTransitionUI', 'logic.comsys.battle.Train'), interval=1.0, mode=2, times=1)
        self._round = round_interval_data.get('cur_round')
        self._round_timestamp = round_interval_data.get('round_timestamp')
        self._round_status = round_interval_data.get('round_status')
        global_data.ui_mgr.close_ui('TrainSkillUI')
        global_data.ui_mgr.close_ui('TrainSkillSelectUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('MechaSummonUI')
        global_data.ui_mgr.close_ui('MechaSummonAndChooseSkinUI')
        if global_data.ui_mgr.get_ui('StateChangeUI'):
            global_data.ui_mgr.close_ui('StateChangeUI')

    @rpc_method(CLIENT_STUB, (Bool('enable_out_base_rogue'),))
    def clear_rogue(self, enable_out_base_rogue):
        battle_data = global_data.death_battle_data
        battle_data.rogue_gift_candidates = {}
        battle_data.selected_rogue_gifts = defaultdict(dict)
        battle_data.enable_out_base_rogue = enable_out_base_rogue
        battle_data.rogue_refresh_times = defaultdict(int)
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        ui = global_data.ui_mgr.get_ui('TrainRogueChooseBtnUI')
        ui and ui.hide()

    @rpc_method(CLIENT_STUB, (Dict('update_data'),))
    def new_round(self, update_data):
        self.clear_limit_height_tip()
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_PHY_DIRECTION', math3d.vector(0, 0, 0))
        global_data.game_mgr.get_logic_timer().register(func=lambda : self.show_round_start_tip(), interval=1.0, mode=2, times=1)
        self._atk_group_id = update_data.get('atk_group_id')
        self._def_group_id = update_data.get('def_group_id')
        self._round_timestamp = update_data.get('round_settle_timestamp')
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_timestamp)
        global_data.emgr.death_in_base_part_change.emit()
        global_data.emgr.show_last_round_info_event.emit()
        global_data.ui_mgr.close_ui('TrainTransitionUI')
        global_data.ui_mgr.close_ui('TrainTopProgUI')
        global_data.ui_mgr.show_ui('TrainTopProgUI', 'logic.comsys.battle.Train')
        global_data.ui_mgr.show_ui('TrainSkillUI', 'logic.comsys.battle.Train')
        self.show_to_next_station_tips = {}
        self.force_lookat_train()

    def get_atk_group_id(self):
        return self._atk_group_id

    def get_def_group_id(self):
        return self._def_group_id

    def get_old_atk_group_id(self):
        return self._old_atk_group_id

    def get_old_def_group_id(self):
        return self._old_def_group_id

    def get_my_group_id(self):
        return self._my_group_id

    def _on_scene_cam_observe_player_setted(self):
        super(TrainBattle, self)._on_scene_cam_observe_player_setted()
        if not global_data.cam_lplayer:
            return
        if not global_data.player:
            return
        if not global_data.player.logic:
            return
        from logic.gutils import judge_utils
        if judge_utils.is_ob() or global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate():
            old_group_id = self._my_group_id
            self._my_group_id = global_data.cam_lplayer.ev_g_group_id()
            print ('_on_scene_cam_observe_player_setted: old_group_id', old_group_id, 'new_group_id', self._my_group_id)
            if old_group_id != self._my_group_id:
                players = self._last_cache_range_player
                num_atk, num_def = self.update_range_player(players)
                global_data.train_battle_mgr.update_train_skill_screen_sfx(players)
                global_data.train_battle_mgr.update_train_range_sfx_state(num_atk, num_def)
                global_data.emgr.update_train_around_state.emit(num_atk, num_def)

    def get_last_round_dis(self):
        if self._last_round_dis == -1 and len(self._round_train_dis) == 1:
            return self._last_round_dis
        return self._round_train_dis.get(0, self._last_round_dis)

    def get_last_round_left_time(self):
        if self._last_round_left_time == -1 and len(self._round_settle_res_time) == 1:
            return self._last_round_left_time
        return self._round_settle_res_time.get(0, self._last_round_left_time)

    def get_round(self):
        return self._round

    def get_round_time(self):
        return self._round_timestamp

    def get_skill_power(self):
        if global_data.cam_lplayer:
            return self._skill_power.get(global_data.cam_lplayer.id, 0)
        return 0

    def get_is_show_next_station_tips(self, station):
        if not self.show_to_next_station_tips.get(station):
            self.show_to_next_station_tips[station] = True
            return False
        return self.show_to_next_station_tips[station]

    def update_range_player(self, players):
        num = 0
        for player in players:
            entity = self.get_entity(player)
            if entity and entity.logic:
                if entity.logic.ev_g_group_id() == self._my_group_id:
                    add = 1 if 1 else 10
                else:
                    add = 10
                num += add

        num_atk = num % 10 if self._my_group_id == self._atk_group_id else int(num / 10)
        num_def = num % 10 if self._my_group_id == self._def_group_id else int(num / 10)
        return (
         num_atk, num_def)

    def enter_interval_view(self):
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_PLAY_VICTORY_CAMERA')
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_PLAY_VICTORY_CAMERA')
        global_data.ui_mgr.hide_all_ui_by_key('trainbattle', INTERVAL_HIDE_UI_LIST)

    def exit_interval_view(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_EXIT_FOCUS_CAMERA')
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_EXIT_FOCUS_CAMERA')
        global_data.ui_mgr.revert_hide_all_ui_by_key_action('trainbattle', INTERVAL_HIDE_UI_LIST)

    def clear_limit_height_tip(self):
        try:
            BattlePrepare = global_data.game_mgr.scene.get_com('PartCompetitionBattlePrepare')
            if not (BattlePrepare and BattlePrepare.battle_prepare):
                return
            if not hasattr(BattlePrepare.battle_prepare, 'range_mgr'):
                return
            range_mgr = BattlePrepare.battle_prepare.range_mgr
            if not range_mgr:
                return
            range_mgr.clear_timer()
        except:
            pass

    def on_receive_report_dict(self, report_dict):
        if not global_data.cam_lplayer:
            return
        else:
            msg = None
            killer_id, injured_id, _ = battle_utils.parse_battle_report_death(report_dict)
            is_mecha = False
            show_points = 0
            if killer_id:
                is_my_side = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(killer_id)
                if killer_id == global_data.cam_lplayer.id:
                    msg = {'i_type': battle_const.MAIN_KOTH_KILL_POINT,'icon_path': 'gui/ui_res_2/battle/notice/icon_msg_kill.png'
                       }
                    msg['show_num'] = self.play_data.get('kill_human_power', 0)
                if is_my_side:
                    show_points = self.play_data.get('kill_human_power', 0)
            mecha_killer_id, mecha_injured_id = battle_utils.parse_battle_report_mecha_death(report_dict)
            if mecha_killer_id:
                is_my_side = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(mecha_killer_id)
                if mecha_killer_id == global_data.cam_lplayer.id:
                    msg = {'i_type': battle_const.MAIN_KOTH_KILL_MECHA_POINT}
                    msg['show_num'] = self.play_data.get('kill_mecha_power')
                if is_my_side:
                    show_points = self.play_data.get('kill_mecha_power')
                    is_mecha = True
            if msg:
                global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_POINT)
            if show_points:
                global_data.emgr.show_battle_points.emit(is_mecha, show_points)
            return

    def show_round_end_tip(self):
        max_length = global_data.train_battle_mgr.get_mode_max_length()
        if self._last_round_left_time == 0 or max_length > self._last_round_dis:
            message_data = {'i_type': battle_const.TRAIN_USE_ALL_TIME,'content_txt': get_text_by_id(17591).format('{}%'.format(int(float(max_length - self._last_round_dis) / float(max_length) * 100.0)))}
            global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
        elif self._my_group_id == self._old_atk_group_id:
            left_time = time_utility.get_delta_time_str(self._last_round_left_time)
            message_data = {'i_type': battle_const.TRAIN_ARRIVE_END,'content_txt': get_text_by_id(17593).format(left_time)}
            global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)

    def show_round_start_tip(self):
        round_no = self._round + 2
        if self._my_group_id == self._atk_group_id:
            tip_type = battle_const.TRAIN_TIP_ATK_START
            text = get_text_by_id(17832).format(round_no)
        else:
            text = get_text_by_id(17833).format(round_no)
            tip_type = battle_const.TRAIN_TIP_DEF_START
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
        global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)

    def clear_limit_height_tip(self):
        try:
            BattlePrepare = global_data.game_mgr.scene.get_com('PartCompetitionBattlePrepare')
            if not (BattlePrepare and BattlePrepare.battle_prepare):
                return
            if not hasattr(BattlePrepare.battle_prepare, 'range_mgr'):
                return
            range_mgr = BattlePrepare.battle_prepare.range_mgr
            if not range_mgr:
                return
            range_mgr.clear_timer()
        except:
            pass

    @rpc_method(CLIENT_STUB, (List('born_point_list'), Dict('group_born_dict')))
    def update_born_point(self, born_point_list, group_born_dict):
        return
        global_data.death_battle_data and global_data.death_battle_data.update_born_point(group_born_dict, born_point_list)

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        TIPS_THRE = battle_const.TDM_FIRST_POINTS_TIPS_THRE
        if not global_data.cam_lplayer:
            return
        else:
            msg = None
            data = group_points_dict
            first_team_over_thre = None
            for g_id in six.iterkeys(data):
                if data[g_id] >= TIPS_THRE and old_group_points_dict.get(g_id, 0) < TIPS_THRE:
                    if first_team_over_thre is None:
                        first_team_over_thre = g_id
                    else:
                        first_team_over_thre = None
                        break

            if not (global_data.player and global_data.player.logic):
                return
            my_group_id = None
            from logic.gutils import judge_utils
            if judge_utils.is_ob():
                from logic.gutils import judge_utils
                ob_unit = judge_utils.get_ob_target_unit()
                if ob_unit:
                    my_group_id = ob_unit.ev_g_group_id()
            else:
                my_group_id = global_data.player.logic.ev_g_group_id()
            return

    def force_lookat_train(self):
        player_unit = global_data.cam_lplayer
        if not player_unit:
            return
        lpos = player_unit.ev_g_position()
        target_pos = global_data.train_battle_mgr.get_look_at_nearlist_station(player_unit.ev_g_position())
        target_pos = math3d.vector(*target_pos)
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = player_unit.ev_g_yaw() or 0
                global_data.emgr.fireEvent('camera_set_yaw_event', target_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)
                player_unit.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def get_move_range(self):
        polygon_pos_data = global_data.game_mode.get_cfg_data('polygon_check')
        if not polygon_pos_data:
            return super(TrainBattle, self).get_move_range()
        pos_list = []
        born_data = global_data.game_mode.get_born_data()
        polygon_check_list = born_data.get('polygon_check', [])
        for idx in range(len(polygon_check_list)):
            pos_list.append(polygon_pos_data.get(idx, {}).get('corner_pos', [0, 0, 0]))

        return pos_list

    def get_enable_in_train_check(self):
        return self._enable_in_train_check

    def destroy(self, clear_cache=True):
        _last_cache_range_player = []
        super(TrainBattle, self).destroy(clear_cache)
        if global_data.train_battle_mgr:
            global_data.train_battle_mgr.clear_all_sfx_and_extra_model()
            global_data.train_battle_mgr.finalize()