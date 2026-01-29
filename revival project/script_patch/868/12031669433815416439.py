# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingBattleUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import battle_const
OCCUPY_ICON = [
 'gui/ui_res_2/battle/koth/icon_koth_blue.png',
 'gui/ui_res_2/battle/koth/icon_koth_red.png',
 'gui/ui_res_2/battle/koth/icon_koth_purple.png']
OCCUPY_BG = [
 'gui/ui_res_2/battle/notice/img_mech_upgrade_bg.png',
 'gui/ui_res_2/battle/notice/img_mech_upgrade2_bg.png',
 'gui/ui_res_2/battle/notice/img_mech_upgrade3_bg.png']
OCCUPY_TXT_ID = [
 8002, 8003, 8004]
from common.const import uiconst

class KingBattleUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/koth_point'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_hide_panel',
       'btn_check_stat.OnBegin': 'on_show_check_state',
       'btn_check_stat.OnEnd': 'on_hide_check_state'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.panel.bar_time.StopTimerAction()

    def init_parameters(self):
        self.is_warning = False
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.camp_template = ['temp_blue', 'temp_red', 'temp_orange']
        self.last_occupy_side = -1
        self.camp_point = {}
        self.show_left_time_msg = []
        self.get_state_timer = None
        self.last_round = None
        self.last_second = None
        return

    def init_panel(self):
        for temp_name in self.camp_template:
            node = getattr(self.panel, temp_name)
            node.progress_occupy.SetPercent(0)
            node.lab_point.SetString('0')
            node.lab_occupy.SetString('0')

        camps = global_data.king_battle_data.get_camp()
        for id in six.iterkeys(camps):
            self.update_camp_point(id)

        self.update_occupy_info()
        self.panel.RecordAnimationNodeState('increasing')
        self.panel.RecordAnimationNodeState('alarm')

    def init_event(self):
        emgr = global_data.emgr
        econf = {'update_camp_point': self.update_camp_point,
           'update_camp_occupy_info': self.update_occupy_info,
           'show_battle_report_event': self.show_battle_report
           }
        emgr.bind_events(econf)

    def update_camp_point(self, faction_id):
        total_point = self.cfg_data.get('settle_point')
        if not total_point:
            return
        camp_data = global_data.king_battle_data.get_camp()[faction_id]
        temp_name = self.camp_template[camp_data.side]
        temp_node = getattr(self.panel, temp_name)
        node = temp_node.progress_occupy
        self.set_progress(node, 100.0 * camp_data.point / total_point)
        self.show_ten_points_ani(temp_node, faction_id, camp_data.point)
        self.camp_point[faction_id] = camp_data.point
        node = temp_node.lab_point

        def _set_point(node, faction_id):
            point = self.camp_point.get(faction_id, 0)
            node.SetString(str(point))

        if not temp_node.IsPlayingAnimation('lab_add_point'):
            temp_node.PlayAnimation('lab_add_point')
            node.DelayCall(0.264, _set_point, node, faction_id)

    def update_occupy_info(self):
        camps = global_data.king_battle_data.get_camp()
        for faction_id, camp_data in six.iteritems(camps):
            temp_name = self.camp_template[camp_data.side]
            node = getattr(self.panel, temp_name).lab_occupy
            node.SetString(str(camp_data.occupy_num))

    def show_ten_points_ani(self, temp_node, faction_id, point):
        camps = global_data.king_battle_data.get_camp()
        camp_data = camps.get(faction_id)
        i_types = [battle_const.MAIN_KOTH_B_SIDE_TEN_POINTS,
         battle_const.MAIN_KOTH_R_SIDE_TEN_POINTS,
         battle_const.MAIN_KOTH_O_SIDE_TEN_POINTS]
        last_point = self.camp_point.get(faction_id, 0)
        if last_point != point and point > 0 and point % 10 == 0:
            temp_node.PlayAnimation('add_point2')
            msg = {'i_type': i_types[camp_data.side],'show_num': point
               }
            if faction_id == global_data.king_battle_data.my_camp_id:
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            elif point == 80:
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def show_occupy_ani(self, control_camp_id, occupy_id):
        from logic.gcommon.common_const import battle_const
        show_control_camp_id = global_data.king_battle_data.get_side_by_faction_id(control_camp_id)
        cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        show_text_id = ''
        if cfg:
            show_text_id = cfg.get(str(occupy_id), {}).get('show_text_id', '')
        msg = {'i_type': battle_const.MAIN_KOTH_OCCUPY,'icon_path': OCCUPY_ICON[show_control_camp_id],'content_txt': get_text_by_id(8001).format(camp=get_text_by_id(OCCUPY_TXT_ID[show_control_camp_id]), point=get_text_by_id(show_text_id)),
           'set_attr_dict': {'node_name': 'glow','func_name': 'SetDisplayFrameByPath',
                             'args': (
                                    '', OCCUPY_BG[show_control_camp_id])
                             }
           }
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
        if global_data.player and global_data.player.logic:
            my_faction_id = global_data.player.logic.ev_g_camp_id()
            if my_faction_id == control_camp_id:
                global_data.sound_mgr.play_ui_sound('get_instructions')
            else:
                global_data.sound_mgr.play_ui_sound('get_instructions')

    def set_progress(self, node, progress):
        cur_progress = node.getPercent()
        ani_time = abs(progress - cur_progress) / 50
        node.SetPercent(progress, time=ani_time)

    def on_count_down(self, settle_timestamp, overtime=None):
        revive_time = settle_timestamp - tutil.get_server_time()
        if revive_time <= 0 and overtime:
            self.on_count_down(overtime)
            return

        def refresh_time(pass_time):
            left_time = int(revive_time - pass_time)
            if left_time == 180 and 3 not in self.show_left_time_msg:
                msg = {'i_type': battle_const.MAIN_KOTH_LEFT_TIME,'set_num_func': 'set_show_minute_num','show_num': 3
                   }
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
                self.show_left_time_msg.append(3)
            elif left_time == 60 and 1 not in self.show_left_time_msg:
                msg = {'i_type': battle_const.MAIN_KOTH_LEFT_TIME,'set_num_func': 'set_show_minute_num','show_num': 1
                   }
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
                self.show_left_time_msg.append(1)
            if left_time <= 10 and not self.is_warning:
                self.panel.bar_time.lab_time.SetColor('#DR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif left_time > 10 and self.is_warning:
                self.panel.bar_time.lab_time.SetColor('#DW')
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.bar_time.lab_time.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)
            if overtime:
                self.on_count_down(overtime)

        self.panel.bar_time.lab_time.SetColor('#DW')
        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.bar_time.StopTimerAction()
        self.panel.bar_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)

    def on_turns_count_down(self, settle_timestamp, overtime):
        reward_interval = global_data.game_mode.get_cfg_data('play_data').get('reward_interval', 0)
        play_duration = global_data.game_mode.get_cfg_data('play_data').get('play_duration', 0)
        revive_time = settle_timestamp - tutil.get_server_time()
        count_down_info = (play_duration, revive_time, reward_interval)
        play_duration = global_data.game_mode.get_cfg_data('play_data').get('play_overtime', 0)
        revive_time = overtime - tutil.get_server_time() - revive_time
        over_count_down_info = (play_duration, revive_time, reward_interval)
        self.delay_turns_count_down(1, count_down_info, over_count_down_info)

    def delay_turns_count_down(self, delay_time, count_down_info, over_count_down_info):
        play_duration, revive_time, reward_interval = count_down_info
        if revive_time + delay_time <= 0 and over_count_down_info:
            play_duration, revive_time, reward_interval = over_count_down_info
        cur_round = int((play_duration - revive_time) / reward_interval) + 1
        cur_left_time = reward_interval - (play_duration - revive_time) % reward_interval

        def refresh_time(pass_time):
            turn_txt = get_text_by_id(18218).format(num=str(cur_round))
            self.panel.bar_round_time.lab_round.SetString(turn_txt)
            left_time = cur_left_time + (delay_time - pass_time)
            left_time_str = tutil.get_delta_time_str(left_time)[3:]
            self.panel.bar_round_time.lab_time.SetString(left_time_str)

        def refresh_time_finsh():
            self._on_turns_count_down(count_down_info, over_count_down_info)

        self.panel.bar_round_time.StopTimerAction()
        self.panel.bar_round_time.TimerAction(refresh_time, delay_time, callback=refresh_time_finsh)

    def _on_turns_count_down(self, count_down_info, over_count_down_info=None):
        play_duration, revive_time, reward_interval = count_down_info
        if revive_time <= 0 and over_count_down_info:
            self._on_turns_count_down(over_count_down_info)
            return

        def refresh_time(pass_time):
            cur_round = int((play_duration - revive_time + pass_time) / reward_interval) + 1
            turn_txt = get_text_by_id(18218).format(num=str(cur_round))
            self.panel.bar_round_time.lab_round.SetString(turn_txt)
            left_time = reward_interval - (play_duration - revive_time + pass_time) % reward_interval
            left_time_str = tutil.get_delta_time_str(left_time)[3:]
            self.panel.bar_round_time.lab_time.SetString(left_time_str)
            if left_time <= 11:
                left_time_second = int(left_time)
                if self.last_second is None or self.last_second != left_time_second:
                    self.last_second = left_time_second
                    if cur_round <= 4:
                        global_data.sound_mgr.play_ui_sound('resurrection_countdown')
                    else:
                        global_data.sound_mgr.play_ui_sound('resurrection_countdown')
            if self.last_round is None:
                self.last_round = cur_round
            if self.last_round != cur_round:
                self.last_round = cur_round
                global_data.sound_mgr.play_ui_sound('achievement')
            return

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.bar_round_time.lab_time.SetString(left_time)
            if over_count_down_info:
                self._on_turns_count_down(over_count_down_info)

        self.panel.bar_round_time.StopTimerAction()
        self.panel.bar_round_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)

    def on_show_check_state(self, *args):

        def get_time_state():
            if not global_data.player:
                return
            bat = global_data.player.get_battle()
            if not bat:
                return
            bat.call_soul_method('request_rank_data', (global_data.player,))

        from common.utils.timer import CLOCK
        if self.get_state_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_state_timer)
        self.get_state_timer = global_data.game_mgr.register_logic_timer(get_time_state, times=-1, interval=1, mode=CLOCK)
        get_time_state()
        global_data.ui_mgr.show_ui('KingCheckStateUI', 'logic.comsys.battle.King')

    def on_hide_check_state(self, *args):
        global_data.ui_mgr.close_ui('KingCheckStateUI')
        if self.get_state_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_state_timer)
            self.get_state_timer = None
        return

    def show_battle_report(self, report_dict):
        event_type = report_dict['event_type']
        from logic.gcommon.common_const import battle_const as bconst
        if event_type == bconst.FIGHT_EVENT_KING_CONTROL:
            control_faction_id = report_dict.get('control_faction_id')
            king_point_id = report_dict.get('king_point_id')
            if control_faction_id is not None and king_point_id is not None:
                self.show_occupy_ani(control_faction_id, king_point_id)
        return