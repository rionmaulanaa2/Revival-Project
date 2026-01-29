# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaHitCallUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
from logic.client.const.camera_const import POSTURE_STAND, POSTURE_SQUAT, POSTURE_GROUND, POSTURE_JUMP
import cc
from logic.gcommon import time_utility as tutil
import time
import game
import world
from logic.client.const import pc_const
from logic.gutils import pc_utils
from logic.gcommon.common_const.skill_const import SKILL_ROLL, SKILL_AIR_JUMP
from logic.gcommon.common_const import battle_const
from .KizunaHitCallHelper import KizunaHitCallGenerator
from logic.gutils.concert_utils import get_song_action_sync_start, get_song_len, get_song_show_time
from logic.comsys.common_ui.CommonInfoUtils import create_ui, destroy_ui
from logic.gutils.hot_key_utils import hot_key_func_to_hot_key, is_down_msg, is_up_msg
SINGLE_BEAT = 1
MULTIPLE_BEAT = 2
LONG_BEAT = 3
BEAT_NONE = 0
BEAT_BAD = 1
BEAT_GOOD = 2
BEAT_GREAT = 3
BEAT_PERFECT = 4
SINGLE_BEAT_TIME = 1
SINGLE_HEART_TIME = 1.0
EXTRA_SHOW_TIME = 5.0
UNIT_LEN_OF_ONE_SEC = 36
STAMINA_MAP = {2: 'battle/i_fight_roll_3',
   3: 'battle/i_fight_roll_1',
   4: 'battle/i_fight_roll_2'
   }
score_dict = {BEAT_BAD: [
            'Miss', 6736056],
   BEAT_GOOD: [
             'Good', 15437662],
   BEAT_GREAT: [
              'Great', 4048639],
   BEAT_PERFECT: [
                'Perfect', 16730367]
   }
score_sp_dict = {BEAT_BAD: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/txt_bad.png',
   BEAT_GOOD: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/txt_good.png',
   BEAT_GREAT: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/txt_great.png',
   BEAT_PERFECT: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/txt_perfect.png'
   }
song_sp_bar_dict = {BEAT_PERFECT: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/bar_perfect.png',
   BEAT_GREAT: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/bar_great.png',
   BEAT_GOOD: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/bar_good.png',
   BEAT_BAD: 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/showtime_and_tips/bar_bad.png'
   }
BEAT_TEMPLATE_CONST = {SINGLE_BEAT: battle_const.CONCERT_SINGLE_BEAT,
   MULTIPLE_BEAT: battle_const.CONCERT_MULTIPLE_BEAT,
   LONG_BEAT: battle_const.CONCERT_LONG_BEAT
   }

def check_in_range(t, range, range_extend=0.0):
    return range[0] - range_extend <= t <= range[1] + range_extend


def check_in_range_ex(t, range, range_extend=(0, 0)):
    return range[0] - range_extend[0] <= t <= range[1] + range_extend[1]


BeatFactory = {}

def regBeatType(cls):
    global BeatFactory
    BeatFactory[cls.BeatType] = cls
    return cls


class BeatBase(object):
    BeatType = -1
    ADVANCE_SHOW_T = EXTRA_SHOW_TIME
    EDGE_TIME = 0.5
    TIME_OF_HEART = SINGLE_HEART_TIME

    def __init__(self, node):
        self.node = node
        self._pos_song_time = 0
        self.unit_len_of_one_sec = UNIT_LEN_OF_ONE_SEC
        self.event_data = {}

    def set_uni_len_of_one_sec(self, val):
        self.unit_len_of_one_sec = val

    def destroy(self):
        self.node = None
        self.event_data = {}
        return

    def get_node(self):
        return self.node

    def set_data(self, event_data):
        self.event_data = event_data

    def get_data(self):
        return self.event_data

    def on_touch_begin(self, song_time):
        pass

    def on_touch_end(self, song_time):
        pass

    def update(self, song_time):
        self.update_pos(song_time)

    def on_show(self, song_time):
        self.update(song_time)

    def on_hide(self):
        pass

    def check_finish(self, song_time, force_extend_time=0):
        start_time, end_time = self.event_data['time_range']
        extend = force_extend_time or self.ADVANCE_SHOW_T if 1 else force_extend_time
        if song_time > end_time + extend:
            return True
        else:
            return False

    def get_default_finish_time(self, force_extend_time=0):
        start_time, end_time = self.event_data['time_range']
        extend = force_extend_time or self.ADVANCE_SHOW_T if 1 else force_extend_time
        return end_time + extend

    def check_in_range(self, t, range, range_extend=0.0):
        return check_in_range(t, range, range_extend)

    def get_score(self, song_time):
        pass

    def get_score_for_one_beat(self, song_time, start_time, end_time, is_hitted, hit_timed, time_required=(0.2, 0.4, 0.5)):
        if not is_hitted:
            if song_time > end_time:
                return BEAT_BAD
            return BEAT_NONE
        else:
            mid_time = (start_time + end_time) / 2.0
            if self.check_in_range(hit_timed, (mid_time, mid_time), time_required[0]):
                return BEAT_PERFECT
            if self.check_in_range(hit_timed, (mid_time, mid_time), time_required[1]):
                return BEAT_GREAT
            if self.check_in_range(hit_timed, (mid_time, mid_time), time_required[2]):
                return BEAT_GOOD
            return BEAT_BAD

    def get_time_center(self):
        start_time, end_time = self.event_data['time_range']
        return (start_time + end_time) / 2.0

    def update_pos(self, song_time):
        pos = self.get_pos_by_time(song_time)
        self.node.setPosition(pos)

    def get_pos_by_time(self, song_time):
        len_of_one_sec = self.unit_len_of_one_sec
        time_of_center = self.get_time_center()
        time_gap = song_time - time_of_center
        pos_x = len_of_one_sec * time_gap / SINGLE_BEAT_TIME
        old_pos = self.node.getPosition()
        self._pos_song_time = song_time
        return cc.Vec2(pos_x, old_pos.y)

    def on_resolution_changed(self):
        pass


@regBeatType
class SingleBeat(BeatBase):
    BeatType = SINGLE_BEAT

    def __init__(self, node):
        super(SingleBeat, self).__init__(node)
        self.is_hitted = False
        self.has_hitted = False
        self.hit_timed = 0

    def on_touch_begin(self, song_time):
        start_time, end_time = self.event_data['time_range']
        if not self.check_in_range(song_time, (start_time, end_time), self.EDGE_TIME):
            return
        if not self.has_hitted:
            if start_time <= song_time <= end_time:
                self.is_hitted = True
                self.node.nd_game_1.temp_game_1.PlayAnimation('click')
            else:
                self.is_hitted = True
            self.has_hitted = True
            self.hit_timed = song_time

    def update(self, song_time):
        super(SingleBeat, self).update(song_time)
        start_time, end_time = self.event_data['time_range']
        if not self.is_hitted:
            if song_time > end_time:
                pass
        elif song_time > end_time:
            self.node.nd_game_1.temp_game_1.btn_heart_0.SetShowEnable(False)

    def on_show(self, song_time):
        super(SingleBeat, self).on_show(song_time)
        self.is_hitted = False
        self.has_hitted = False
        self.node.nd_game_1.setVisible(True)
        self.node.nd_game_1.temp_game_1.btn_heart_0.EnableCustomState(True)
        self.node.nd_game_1.temp_game_1.btn_heart_0.SetSelect(False)
        self.node.nd_game_1.temp_game_1.vx_di.setVisible(False)

    def on_hide(self):
        super(SingleBeat, self).on_hide()
        self.node.nd_game_1.setVisible(False)

    def get_score(self, song_time):
        start_time, end_time = self.event_data['time_range']
        return self.get_score_for_one_beat(song_time, start_time, end_time, self.has_hitted, self.hit_timed)

    def on_resolution_changed(self):
        pass


@regBeatType
class MultipleBeat(BeatBase):
    BeatType = MULTIPLE_BEAT
    EDGE_TIME = 0.2

    def __init__(self, node):
        super(MultipleBeat, self).__init__(node)
        self.is_hitted_dict = {}
        self.hitted_time_dict = {}
        self.has_hitted_dict = {}
        self.half_heart_time = self.TIME_OF_HEART / 2.0

    def on_touch_begin(self, song_time):
        start_time, end_time = self.event_data['time_range']
        if not self.check_in_range(song_time, (start_time, end_time), self.EDGE_TIME + self.half_heart_time):
            return
        before_sel = six_ex.keys(self.is_hitted_dict)
        sec_time = (start_time + end_time) / 2.0
        first_time = start_time
        third_time = end_time

        def set_index_sel(idx):
            self.node.nd_game_2.list_game_2.GetItem(idx).PlayAnimation('click')
            self.is_hitted_dict.update({idx: True})
            self.hitted_time_dict.update({idx: song_time})

        def check_idx(t, idx):
            if self.check_in_range(song_time, (t, t), self.EDGE_TIME + self.half_heart_time):
                if not self.has_hitted_dict.get(idx):
                    if self.check_in_range(song_time, (t, t), self.half_heart_time):
                        set_index_sel(idx)
                    self.has_hitted_dict.update({idx: True})

        check_idx(first_time, 0)
        check_idx(sec_time, 1)
        check_idx(third_time, 2)
        after_sel = six_ex.keys(self.is_hitted_dict)
        if len(after_sel) - len(before_sel) > 1:
            log_error('One touch Trigger Multiple Selection!!!!')

    def update(self, song_time):
        super(MultipleBeat, self).update(song_time)
        start_time, end_time = self.event_data['time_range']
        sec_time = (start_time + end_time) / 2.0
        first_time = start_time
        third_time = end_time

        def on_update_idx(idx, s_t, e_t):
            if not self.is_hitted_dict.get(idx):
                if song_time > e_t:
                    pass
            elif song_time > e_t:
                self.node.nd_game_2.list_game_2.GetItem(idx).btn_heart_0.SetShowEnable(False)

        on_update_idx(0, first_time - self.half_heart_time, first_time + self.half_heart_time)
        on_update_idx(1, sec_time - self.half_heart_time, sec_time + self.half_heart_time)
        on_update_idx(2, third_time - self.half_heart_time, third_time + self.half_heart_time)

    def on_show(self, song_time):
        super(MultipleBeat, self).on_show(song_time)
        self.is_hitted_dict = {}
        self.hitted_time_dict = {}
        self.has_hitted_dict = {}
        self.node.nd_game_2.setVisible(True)
        self.node.nd_game_2.list_game_2.SetInitCount(3)
        for ui_item in self.node.nd_game_2.list_game_2.GetAllItem():
            ui_item.btn_heart_0.EnableCustomState(True)
            ui_item.btn_heart_0.SetSelect(False)
            ui_item.vx_di.setVisible(False)

        start_time, end_time = self.event_data['time_range']
        unit_width = self.unit_len_of_one_sec
        heart_empty_gap_time = (end_time - start_time) / 2.0 - self.half_heart_time * 2
        heart_gap_width = heart_empty_gap_time / self.TIME_OF_HEART * unit_width
        self.node.nd_game_2.list_game_2.SetHorzIndent(heart_gap_width)

    def on_hide(self):
        super(MultipleBeat, self).on_hide()
        self.node.nd_game_2.setVisible(False)

    def check_finish(self, song_time, force_extend_time=0):
        start_time, end_time = self.event_data['time_range']
        extend = force_extend_time or self.ADVANCE_SHOW_T + self.half_heart_time if 1 else force_extend_time
        if song_time > end_time + extend:
            return True
        else:
            return False

    def get_default_finish_time(self, force_extend_time=0):
        start_time, end_time = self.event_data['time_range']
        extend = force_extend_time or self.ADVANCE_SHOW_T + self.half_heart_time if 1 else force_extend_time
        return end_time + extend

    def get_score(self, song_time):
        start_time, end_time = self.event_data['time_range']
        sec_time = (start_time + end_time) / 2.0
        first_time = start_time
        third_time = end_time
        t_list = [first_time, sec_time, third_time]
        ret_list = []
        for idx, t in enumerate(t_list):
            has_hitted = self.has_hitted_dict.get(idx, False)
            hit_time = self.hitted_time_dict.get(idx, 0)
            sub_s_t = t - self.half_heart_time
            sub_e_t = t + self.half_heart_time
            ret_list.append(self.get_score_for_one_beat(song_time, sub_s_t, sub_e_t, has_hitted, hit_time))

        return ret_list

    def get_time_center(self):
        start_time, end_time = self.event_data['time_range']
        return (start_time + end_time) / 2.0


@regBeatType
class LongBeat(BeatBase):
    BeatType = LONG_BEAT
    ADVANCE_SHOW_T = 5

    def __init__(self, node):
        super(LongBeat, self).__init__(node)
        self.is_hitted = False
        self.has_hitted = False
        self.hitted_start_time = 0
        self.hitted_last_time = 0

    def __str__(self):
        return 'event_data %s %s ' % (str(self.BeatType), str(self.event_data))

    def on_touch_begin(self, song_time):
        start_time, end_time = self.event_data['time_range']
        if not self.check_in_range(song_time, (start_time, end_time), self.EDGE_TIME):
            return
        if not self.has_hitted:
            if start_time <= song_time <= end_time and not self.is_hitted:

                def run_progress_action(progress):
                    start_p = max(int((song_time - start_time) / (end_time - start_time) * 100), self.min_percentage)
                    progress.SetPercentage(start_p)

                progress = self.node.nd_game_3.progress_game_3
                run_progress_action(progress)
                self.hitted_start_time = song_time
                self.is_hitted = True
            self.has_hitted = True

    def on_touch_end(self, song_time):
        if self.hitted_start_time > 0 and self.hitted_last_time <= 0:
            self.hitted_last_time = song_time - self.hitted_start_time
            if self.hitted_last_time >= 0.4:
                self.node.nd_game_3.temp_game_3.PlayAnimation('click')
        progress = self.node.nd_game_3.progress_game_3
        progress.stopAllActions()

    def update(self, song_time):
        super(LongBeat, self).update(song_time)
        if self.is_hitted and self.hitted_last_time <= 0:
            start_time, end_time = self.event_data['time_range']

            def run_progress_action(progress):
                start_p = int((song_time - start_time) / (end_time - start_time) * 100)
                p = max(min(start_p, 100), self.min_percentage)
                progress.setVisible(True)
                progress.SetPercentage(p)

            progress = self.node.nd_game_3.progress_game_3
            run_progress_action(progress)

    def on_show(self, song_time):
        super(LongBeat, self).on_show(song_time)
        self.is_hitted = False
        self.hitted_start_time = 0
        self.hitted_last_time = 0
        self.min_percentage = 0
        self.node.nd_game_3.setVisible(True)
        self.refresh_pos_and_size_by_data()
        self.node.nd_game_3.temp_game_3.btn_heart_0.EnableCustomState(True)
        self.node.nd_game_3.temp_game_3.btn_heart_0.SetSelect(False)
        self.node.nd_game_3.temp_game_3.vx_di.setVisible(False)
        progress = self.node.nd_game_3.progress_game_3
        progress.SetPercentage(0)
        progress.stopAllActions()
        progress.setVisible(False)

    def refresh_pos_and_size_by_data(self):
        start_time, end_time = self.event_data['time_range']
        node_len = UNIT_LEN_OF_ONE_SEC * (end_time - start_time)
        self.node.nd_game_3.SetContentSize(node_len, 82)
        self.node.nd_game_3.ChildResizeAndPosition()

    def on_hide(self):
        super(LongBeat, self).on_hide()
        self.node.nd_game_3.setVisible(False)

    def get_score(self, song_time):
        start_time, end_time = self.event_data['time_range']
        if self.has_hitted:
            if self.is_hitted:
                if self.hitted_last_time == 0:
                    return BEAT_NONE
                else:
                    if self.hitted_last_time < 0.4:
                        return BEAT_BAD
                    return self.get_score_for_one_beat(song_time, start_time, end_time, self.has_hitted, self.hitted_start_time)

            else:
                return BEAT_BAD
        else:
            if song_time > end_time:
                return BEAT_BAD
            return BEAT_NONE

    def on_resolution_change(self):
        self.refresh_pos_and_size_by_data()

    def update_pos(self, song_time):
        if not self.is_hitted:
            super(LongBeat, self).update_pos(song_time)
        elif self.hitted_last_time > 0:
            super(LongBeat, self).update_pos(song_time - self.hitted_last_time)


class KizunaHitCallUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_dacall_button'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_icon_dacall.OnClick': 'on_click_btn_icon_dacall',
       'btn_icon_dacall.OnBegin': 'on_begin_btn_icon_dacall',
       'btn_icon_dacall.OnEnd': 'on_end_btn_icon_dacall',
       'btn_jump.OnBegin': 'on_begin_jump_btn',
       'btn_jump.OnEnd': 'on_end_jump_btn'
       }
    ENABLE_HOT_KEY_SUPPORT = True
    HOT_KEY_CHECK_VISIBLE = False
    HOT_KEY_FUNC_MAP_SHOW = {'human_jump': {'node': 'btn_jump.temp_pc'}}
    HOT_KEY_FUNC_MAP = {'concert_hit_call.DOWN_UP': 'on_keyboard_hit_call'
       }
    GLOBAL_EVENT = {'on_player_air_jump_stamina_changed': 'on_air_jump_stamina_changed',
       'on_player_add_jump_max_stage_event': 'check_jump_btn_appearance',
       'on_skill_init_complete_event': 'reset_air_jump_cost',
       'scene_player_setted_event': 'on_player_setted',
       'change_concert_song_data_event': 'on_update_concert_song_data',
       'concert_offer_do_call_reward': 'on_received_call_reward'
       }
    TIMER_TAG = 210911
    TIMER_TAG_2 = 210924

    def on_init_panel(self, *args, **kwargs):
        super(KizunaHitCallUI, self).on_init_panel()
        self._hit_call_generator = None
        self._hit_call_timeline = self.get_hit_call_record()
        self._timeline_play_idx = 0
        self._timeline_playing_idx = -1
        self._cur_show_da_call_beat = None
        self._cur_show_beat_score = BEAT_NONE
        self._history_beat_score = []
        self._song_start_ts = 0
        self._song_idx = -1
        self._song_show_time = None
        self._show_beats_dict = {}
        self._show_beat_play_idx = 0
        self.panel.lab_game_tips.SetString('')
        self.panel.nd_game.setVisible(False)
        self.panel.lab_mark.setVisible(False)
        self.panel.nd_button.setVisible(not global_data.is_pc_mode)
        self.panel.RecordAnimationNodeState('show_01')
        self.panel.RecordAnimationNodeState('disappear')
        self.panel.progress_game.setTouchEnabled(False)
        self._progress_time_len = EXTRA_SHOW_TIME * 2 + SINGLE_BEAT_TIME
        self.panel.progress_game.setPercent(70)
        percent = self.panel.progress_game.getPercent() / 100.0
        self._beat_time_extend = (self._progress_time_len * percent, self._progress_time_len * (1.0 - percent))
        self.init_progress(self._progress_time_len)
        sz = self.panel.progress_game.getContentSize()
        self.panel.nd_heart_list.SetPosition(sz.width * percent, '50%2')
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        self.init_song_info()
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        if player:
            self.on_player_setted(player)
        self.register_timer()
        self.refresh_time()
        self.panel.btn_icon_dacall.set_sound_enable(False)
        self.panel.btn_jump.set_sound_enable(False)
        return

    def on_finalize_panel(self):
        super(KizunaHitCallUI, self).on_finalize_panel()
        self.clear_show_beats()
        self.unregister_timer()
        self.player = None
        self.destroy_widget('_hit_call_generator')
        return

    def clear_show_beats(self):
        for beat in six.itervalues(self._show_beats_dict):
            node = beat.get_node()
            destroy_ui(node)
            beat.destroy()

        self._show_beats_dict = {}
        if self._cur_show_da_call_beat:
            self._cur_show_da_call_beat = None
        return

    def into_generate_system(self):
        if not self._hit_call_generator:
            self._hit_call_generator = KizunaHitCallGenerator()
        self._hit_call_generator.init_keyboard_ctrl()
        self.panel.txt_generate_tip.setVisible(True)
        self._hit_call_generator.init_record()

    def end_generate_system(self):
        if self._hit_call_generator:
            self._hit_call_generator.process_key_note()
            self._hit_call_generator.recover_keyboard_ctrl()
        self.panel.txt_generate_tip.setVisible(False)

    def start_test(self):
        self._song_start_ts = tutil.get_server_time()
        self._timeline_play_idx = 0
        self._hit_call_timeline = self.get_hit_call_record(-1)
        self._song_idx = 0

    def get_hit_call_record(self, song_idx=None):
        if song_idx is None:
            return []
        else:
            if song_idx == -1:
                return [{'type': 3,'time_range': [6, 7]}, {'type': 1,'time_range': [10.35, 11.35]}]
            song_da_call_conf = global_data.game_mode.get_cfg_data('play_data').get('song_da_call_conf', [])
            if 0 <= song_idx < len(song_da_call_conf):
                table_conf = song_da_call_conf[song_idx]
                converted_conf = []
                for beat_conf in table_conf:
                    if len(beat_conf) != 3:
                        log_error('invalid song da call conf', song_idx, table_conf)
                        continue
                    else:
                        ty = beat_conf[0]
                        if ty == SINGLE_BEAT:
                            half_length = beat_conf[2] / 2.0
                            converted_conf.append({'type': ty,'time_range': [
                                            beat_conf[1] - half_length, beat_conf[1] + half_length]
                               })
                        elif ty == MULTIPLE_BEAT:
                            converted_conf.append({'type': ty,'time_range': [
                                            beat_conf[1], beat_conf[1] + beat_conf[2]]
                               })
                        elif ty == LONG_BEAT:
                            half_length = beat_conf[2] / 2.0
                            converted_conf.append({'type': ty,'time_range': [beat_conf[1] - half_length, beat_conf[1] + half_length]})

                return converted_conf
            return []

    def init_progress(self, whole_time, passed_time=0):
        progress_sz = self.panel.progress_game.getContentSize()
        new_width = UNIT_LEN_OF_ONE_SEC * whole_time / SINGLE_BEAT_TIME
        self.panel.progress_game.SetContentSize(new_width, progress_sz.height)
        self.panel.nd_cut.SetContentSize(new_width, self.panel.nd_cut.getContentSize().height)
        progress = self.panel.progress_game
        progress.stopAllActions()

    def init_song_info(self):
        if global_data.battle:
            bat = global_data.battle
            self.on_update_concert_song_data(bat.concert_stage, bat.song_idx, bat.song_end_ts)

    def on_update_concert_song_data(self, stage, song_idx, song_end_ts):
        from logic.gcommon.common_const import battle_const
        if stage == battle_const.CONCERT_SING_STAGE:
            if song_idx != -1 and song_idx is not None:
                self._song_start_ts = song_end_ts - get_song_len(song_idx)
                if song_idx != self._song_idx:
                    self._timeline_play_idx = 0
                    self._hit_call_timeline = self.get_hit_call_record(song_idx)
                    self._song_idx = song_idx
                    self._history_beat_score = []
                    self._song_show_time = get_song_show_time(song_idx)
                    self.on_finish_call_event()
                    self.clear_show_beats()
                    self._show_beat_play_idx = 0
                    self.panel.lab_game_tips.SetString('')
                    self.panel.nd_game.setVisible(False)
        else:
            self._timeline_play_idx = 0
            self._song_show_time = 0
            self._song_start_ts = -1
            self._song_idx = -1
            self._history_beat_score = []
            self.clear_show_beats()
            self._show_beat_play_idx = 0
            self.panel.lab_game_tips.SetString('')
            self.panel.nd_game.setVisible(False)
        return

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.25),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act2 = cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.refresh_time_fast)]))
        self.panel.runAction(act2)
        act.setTag(self.TIMER_TAG)
        act2.setTag(self.TIMER_TAG_2)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)
        self.panel.stopActionByTag(self.TIMER_TAG_2)

    def on_click_btn_icon_dacall(self, btn, touch):
        if self._timeline_playing_idx != -1:
            pass
        else:
            from logic.gcommon.cdata import status_config
            if not (global_data.player and global_data.player.logic):
                return
            plogic = global_data.player.logic
            if plogic.ev_g_is_in_any_state(status_config.ST_CONTINUE_ACTION):
                act_name = plogic.ev_g_continue_action_name()
                if act_name == 'da_call_mid':
                    plogic.send_event('E_PERFORM_CONTINUE_ACTION_EXTEND', 'da_call_mid', 0.5)
                elif act_name == 'da_call':
                    if plogic.ev_g_continue_action_last_time() > 2:
                        t_acts = [
                         (
                          0, {'anim_info': ['mid_call', 1, 1, {'loop': True}]})]
                        plogic.send_event('E_PERFORM_CONTINUE_ACTION_CHANGE', 'da_call_mid', 1.0, t_acts, {'need_cache_anim': True,'blend_time': 0})
                    else:
                        plogic.send_event('E_PERFORM_CONTINUE_ACTION_EXTEND', 'da_call', 0.5)
            else:
                if not plogic.ev_g_status_check_pass(status_config.ST_CONTINUE_ACTION):
                    return False
                t_acts = [
                 (
                  0, {'anim_info': ['low_call', 1, 1, {'loop': True}]})]
                plogic.send_event('E_PERFORM_CONTINUE_ACTION_START', 'da_call', 1.0, t_acts)

    def on_begin_btn_icon_dacall(self, btn, touch):
        if self._cur_show_da_call_beat:
            song_time = tutil.get_server_time() - self._song_start_ts
            self._cur_show_beat_score = self._cur_show_da_call_beat.get_score(song_time)
            self._cur_show_da_call_beat.on_touch_begin(song_time)
        self.panel.StopAnimation('return')
        self.panel.PlayAnimation('click')
        return True

    def on_end_btn_icon_dacall(self, btn, touch):
        if self._cur_show_da_call_beat:
            song_time = tutil.get_server_time() - self._song_start_ts
            self._cur_show_da_call_beat.on_touch_end(song_time)
            da_call_beat_score = self._cur_show_da_call_beat.get_score(song_time)
            self.check_action_with_score(da_call_beat_score)
            self.update_score(da_call_beat_score)
        self.panel.StopAnimation('click')
        self.panel.PlayAnimation('return')

    def check_action_with_score(self, da_call_beat_score):
        if global_data.player and global_data.player.logic:
            if type(da_call_beat_score) in (tuple, list):
                score = BEAT_NONE
                for _tmp_score in da_call_beat_score:
                    if _tmp_score > score:
                        score = _tmp_score
                        if score != BEAT_BAD:
                            break

            else:
                score = da_call_beat_score

            def start_dance():
                if global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_START_CONCERT_DANCE')

            if score is not None and score is not BEAT_NONE:
                if score != BEAT_BAD:
                    sync_start_time = get_song_action_sync_start(self._song_idx)
                    song_time = tutil.get_server_time() - self._song_start_ts
                    if song_time > sync_start_time:
                        start_dance()
                    else:
                        self.panel.SetTimeOut(sync_start_time - song_time + 0.01, lambda : start_dance())
                else:
                    global_data.player.logic.send_event('E_STOP_CONCERT_DANCE', 'miss_call_01')
        return

    def get_new_score_compare_with_cur(self, da_call_beat_score):
        if self._cur_show_beat_score != da_call_beat_score:
            if type(da_call_beat_score) in (tuple, list):
                for idx, score in enumerate(da_call_beat_score):
                    if score != self._cur_show_beat_score[idx] and score != BEAT_NONE:
                        return (idx, score)

            elif da_call_beat_score != BEAT_NONE:
                return (-1, da_call_beat_score)
        return (-1, None)

    def report_score_to_server(self, hit_idx, score):
        if self._song_idx >= 0 and global_data.battle and score > BEAT_BAD:
            global_data.battle.do_dance_call(self._song_idx, hit_idx)

    def update_score(self, da_call_beat_score):
        inside_idx, score = self.get_new_score_compare_with_cur(da_call_beat_score)
        cur_idx = self._timeline_playing_idx
        hit_idx = 0
        for i in range(0, cur_idx):
            event_data = self._hit_call_timeline[i]
            show_type = event_data['type']
            if show_type == MULTIPLE_BEAT:
                hit_idx += 3
            else:
                hit_idx += 1

        if inside_idx and inside_idx >= 0:
            hit_idx += inside_idx
        self.report_score_to_server(hit_idx, score)
        if score is not None and score != BEAT_NONE:
            self.show_beat_score(score)
            self._cur_show_beat_score = da_call_beat_score
        if score is not None:
            self._history_beat_score.append(score)
            combo_count = 0
            for idx, sc in enumerate(reversed(self._history_beat_score)):
                if sc not in [BEAT_NONE, BEAT_BAD, None]:
                    combo_count += 1
                else:
                    break

        return

    def show_beat_score(self, score):
        if score != BEAT_NONE:
            self.panel.lab_mark.setVisible(True)
            score_str, color = score_dict.get(score, ('', 16777215))
            self.panel.lab_mark.SetString(score_str)
            self.panel.lab_mark.SetColor(color)
            self.panel.PlayAnimation('feed_back')
            self.panel.lab_mark.SetTimeOut(1, lambda : self.panel.lab_mark.setVisible(False), tag=210926)
            score_sound_dict = {BEAT_BAD: 'Play_activity_Airlab_musicgame_miss',
               BEAT_GOOD: 'Play_activity_Airlab_musicgame_good',
               BEAT_GREAT: 'Play_activity_Airlab_musicgame_great',
               BEAT_PERFECT: 'Play_activity_Airlab_musicgame_perfect'
               }
            event_name = score_sound_dict.get(score, None)
            if event_name:
                global_data.sound_mgr.play_sound_2d(event_name)
        return

    def show_whole_beat_score(self, score):
        score_anim_dict = {BEAT_BAD: 'show_02',
           BEAT_GOOD: 'show_03',
           BEAT_GREAT: 'show_04',
           BEAT_PERFECT: 'show_01'
           }
        if score != BEAT_NONE:
            self.panel.nd_tips.setVisible(True)
            anim = score_anim_dict.get(score, 'show_01')
            self.panel.nd_tips.PlayAnimation(anim)
            self.panel.nd_tips.nd_mark.setVisible(True)
            self.panel.nd_tips.nd_showtime.setVisible(False)
            sp = score_sp_dict.get(score, '')
            sp_bar = song_sp_bar_dict.get(score, '')
            self.panel.nd_tips.txt_mark.SetDisplayFrameByPath('', sp)
            self.panel.nd_tips.bar_mark.SetDisplayFrameByPath('', sp_bar)
            self.panel.nd_tips.txt_mark.SetTimeOut(self.panel.nd_tips.GetAnimationMaxRunTime(anim) + 1, lambda : self.panel.nd_tips.nd_mark.setVisible(False), tag=210913)

    def show_show_time(self):
        self.panel.nd_tips.setVisible(True)
        self.panel.nd_tips.PlayAnimation('show')

    def on_show_call_event(self, idx, show_type, show_data, song_time):
        if self._cur_show_da_call_beat:
            self._cur_show_da_call_beat = None
        beat_ins = self._show_beats_dict.get(idx, None)
        if beat_ins:
            self._cur_show_da_call_beat = beat_ins
            self._cur_show_beat_score = self._cur_show_da_call_beat.get_score(song_time)
            ty = beat_ins.BeatType
            if ty == SINGLE_BEAT:
                self.panel.lab_game_tips.SetString(82344)
            elif ty == MULTIPLE_BEAT:
                self.panel.lab_game_tips.SetString(82345)
            elif ty == LONG_BEAT:
                self.panel.lab_game_tips.SetString(82346)
        return

    def on_finish_call_event(self):
        self._timeline_playing_idx = -1
        self.panel.lab_game_tips.SetString('')
        if self._cur_show_da_call_beat:
            self._cur_show_da_call_beat = None
        return

    def cal_showtime_score(self):
        for idx in range(0, len(self._hit_call_timeline)):
            pass

    def refresh_time_fast(self):
        if not self._song_start_ts > 0:
            return
        song_time = tutil.get_server_time() - self._song_start_ts
        self.update_beat_show(song_time)

    def refresh_time(self):
        if not self._song_start_ts > 0:
            return
        else:
            song_time = tutil.get_server_time() - self._song_start_ts
            if self._song_show_time:
                if song_time < self._song_show_time[0] < song_time + 6.5:
                    self.show_show_time()
                    self._song_show_time = None
                    global_data.emgr.concert_showtime_start_event.emit()
                self.update_beat_show(song_time)
                if self._timeline_play_idx >= len(self._hit_call_timeline):
                    return
                if self._cur_show_da_call_beat:
                    da_call_beat_score = self._cur_show_da_call_beat.get_score(song_time)
                    self.check_action_with_score(da_call_beat_score)
                    self.update_score(da_call_beat_score)
                    MAX_ABSENCE_TIME = 10
                    is_finished = self._cur_show_da_call_beat.check_finish(song_time, MAX_ABSENCE_TIME)
                    if not is_finished:
                        if self._timeline_playing_idx + 1 >= len(self._hit_call_timeline):
                            return
                        event_data = self._hit_call_timeline[self._timeline_playing_idx]
                        time_range = event_data['time_range']
                        next_event_data = self._hit_call_timeline[self._timeline_playing_idx + 1]
                        next_time_range = next_event_data['time_range']
                        diff = next_time_range[0] - time_range[1]
                        extend = min(diff / 2.0, self._beat_time_extend[1])
                        is_can_finish = self._cur_show_da_call_beat.check_finish(song_time, force_extend_time=extend)
                        if is_can_finish:
                            has_found, break_idx = self.find_next_show_event(self._timeline_playing_idx + 1, song_time)
                            if has_found:
                                self.play_by_idx(break_idx, song_time)
                        return
                    self.on_finish_call_event()
                has_found, idx = self._cur_show_da_call_beat or self.find_next_show_event(self._timeline_play_idx, song_time)
                if has_found:
                    self.play_by_idx(idx, song_time)
            return

    def update_beat_show(self, song_time):
        finish_idxs = []
        for idx, beat in six.iteritems(self._show_beats_dict):
            beat.update(song_time)
            if beat != self._cur_show_da_call_beat:
                is_finish = beat.check_finish(song_time, self._beat_time_extend[1])
                if is_finish:
                    finish_idxs.append(idx)

        for idx in finish_idxs:
            self.hide_by_idx(idx)

        has_found = True
        while has_found:
            has_found, idx = self.find_next_show_event(self._show_beat_play_idx, song_time)
            if has_found:
                self.show_by_idx(idx, song_time)

        if self._show_beats_dict:
            if not self.panel.nd_game.isVisible():
                self.panel.RecoverAnimationNodeState('disappear')
                self.panel.nd_game.setVisible(True)
                self.panel.PlayAnimation('show_01')
        elif self.panel.nd_game.isVisible() and not self.panel.IsPlayingAnimation('disappear'):
            self.panel.PlayAnimation('disappear')
            self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('disappear'), lambda : self.panel.nd_game.setVisible(False))

    def show_by_idx(self, idx, song_time):
        if idx >= len(self._hit_call_timeline):
            return
        else:
            self._show_beat_play_idx = idx + 1
            event_data = self._hit_call_timeline[idx]
            show_type = event_data.get('type')
            beat_cls = BeatFactory.get(show_type, None)
            if beat_cls:
                temp_const = BEAT_TEMPLATE_CONST.get(show_type, None)
                ui_item = create_ui(temp_const, parent=self.panel.nd_heart_list)
                _da_call_beat = beat_cls(ui_item)
                _da_call_beat.set_data(event_data)
                _da_call_beat.set_uni_len_of_one_sec(UNIT_LEN_OF_ONE_SEC)
                _da_call_beat.on_show(song_time)
                _da_call_beat.update_pos(song_time)
                self._show_beats_dict[idx] = _da_call_beat
            return

    def hide_by_idx(self, idx):
        if idx in self._show_beats_dict:
            beat = self._show_beats_dict[idx]
            node = beat.get_node()
            destroy_ui(node)
            beat.destroy()
            del self._show_beats_dict[idx]

    def play_by_idx(self, idx, song_time):
        if idx >= len(self._hit_call_timeline):
            return
        if self._cur_show_da_call_beat:
            self.on_finish_call_event()
        self._timeline_play_idx = idx
        event_data = self._hit_call_timeline[idx]
        show_type = event_data.get('type')
        self._timeline_playing_idx = self._timeline_play_idx
        self.on_show_call_event(idx, show_type, event_data, song_time)

    def find_next_show_event(self, idx, song_time):
        should_end = False
        has_found = False
        while not should_end:
            if idx >= len(self._hit_call_timeline):
                return (False, idx)
            target_event = self._hit_call_timeline[idx]
            event_data = target_event
            time_range = event_data['time_range']
            if check_in_range_ex(song_time, time_range, self._beat_time_extend):
                has_found = True
                should_end = True
            elif song_time >= time_range[1] + self._beat_time_extend[1]:
                idx += 1
            else:
                should_end = True

        return (has_found, idx)

    def on_received_call_reward(self, song_idx, hit_rate, item_count_dict):
        score = BEAT_NONE
        if hit_rate < 10:
            score = BEAT_BAD
        elif 10 <= hit_rate < 50:
            score = BEAT_GOOD
        elif 50 <= hit_rate < 100:
            score = BEAT_GREAT
        else:
            score = BEAT_PERFECT
        self.show_whole_beat_score(score)

    def show_item_fly_to_drug_ani(self, item_count_dict):
        for item_id, item_count in item_count_dict:
            self.show_item_fly_to_drug_ani_helper(item_id)

    def show_item_fly_to_drug_ani_helper(self, item_no):
        from logic.gcommon.common_const import battle_const
        from logic.gutils import template_utils, action_utils
        from logic.gutils import item_utils
        i_type = battle_const.MAIN_MED_GET_ITEM_INFO

        def ani_func(node):
            ui_inst = global_data.ui_mgr.get_ui('DrugUI')
            if ui_inst:
                end_pos = ui_inst.panel.left.ConvertToWorldSpacePercentage(50, 10)
            else:
                return
            l_end_pos = node.icon.getParent().convertToNodeSpace(end_pos)
            l_start_pos = node.icon.getPosition()
            dis = l_start_pos.distance(l_end_pos)
            speed = global_data.ui_mgr.design_screen_size.width
            time = dis / speed
            act = action_utils.bezier_action_helper(time, l_start_pos, l_end_pos, normalized_p1=(0.04,
                                                                                                 0.38), normalized_p2=(0.52,
                                                                                                                       0.94))
            real_act = cc.Spawn.create([
             act,
             cc.Sequence.create([
              cc.FadeIn.create(0.06),
              cc.DelayTime.create(max(time - 0.06, 0.01)),
              cc.FadeOut.create(0.01)])])
            node.icon.runAction(real_act)

        msg = {'i_type': i_type,
           'content_txt': item_utils.get_item_name(item_no),
           'extra_disappear_time': 1,
           'extra_disappear_func': lambda node: ani_func(node),
           'item_id': item_no
           }
        global_data.emgr.show_battle_med_message.emit((msg,), battle_const.MED_NODE_COMMON_INFO)

    def on_resolution_changed(self):
        self.panel.progress_game.setPercent(50)
        percent = self.panel.progress_game.getPercent() / 100.0
        self._beat_time_extend = (self._progress_time_len * percent, self._progress_time_len * (1.0 - percent))
        self.init_progress(self._progress_time_len)
        sz = self.panel.progress_game.getContentSize()
        self.panel.nd_heart_list.SetPosition(sz.width * percent, '50%2')
        for beat in six.itervalues(self._show_beats_dict):
            beat.on_resolution_changed()

    def on_player_setted(self, player):
        self.player = player
        if self.player:
            self.reset_air_jump_cost()
            self.check_jump_btn_appearance()

    def on_begin_jump_btn(self, btn, *args):
        self.play_touch_effect(global_data.is_key_mocking_ui_event or 'jump_click' if 1 else None, 'click', self.panel.nd_jump.getPosition(), self.panel.nd_jump.getScale())
        self._set_posture_btn_sel(POSTURE_JUMP, True)
        from logic.gutils.climb_utils import on_begin_jump_btn_exc
        on_begin_jump_btn_exc()
        return True

    def on_end_jump_btn(self, *args):
        self._set_posture_btn_sel(POSTURE_JUMP, False)

    def _set_posture_btn_sel(self, posture, is_sel):
        if posture == POSTURE_JUMP:
            self.panel.btn_jump.SetSelect(is_sel)
            self.panel.btn_icon_jump.SetSelect(is_sel)

    def check_jump_btn_appearance(self, *args):
        if not self.player:
            return
        else:
            from logic.gcommon.const import BONE_JUMP_PATHS
            max_stage = self.player.ev_g_jump_max_stage()
            if max_stage not in BONE_JUMP_PATHS:
                max_stage = 1
            path_list = BONE_JUMP_PATHS.get(max_stage, [])
            if path_list:
                self.panel.btn_icon_jump.SetFrames('', path_list, False, None)
            self.reset_air_jump_cost()
            return

    def on_air_jump_stamina_changed(self, stamina):
        self.panel.nd_jump_roll.progress.SetPercentage(stamina)
        jump_stamina_count = self._stamina_count[SKILL_AIR_JUMP]
        valid_roll_num = int(stamina / 100.0 * jump_stamina_count)
        for i in range(jump_stamina_count):
            index = i + 1
            stamina_pointer = getattr(self.panel.nd_jump_roll, 'img_use%d' % index, None)
            stamina_pointer and stamina_pointer.setVisible(index <= valid_roll_num)

        return

    def reset_air_jump_cost(self, *args):
        if not self.player:
            return
        if self.player.ev_g_jump_max_stage() == 1:
            self.panel.nd_jump_roll.setVisible(False)
            self.panel.btn_icon_jump.setScale(1)
            return
        self.panel.nd_jump_roll.setVisible(True)
        need_change = self.reset_skill_stamina(self.panel.nd_jump_roll, SKILL_AIR_JUMP)
        if need_change:
            self.on_air_jump_stamina_changed(self.player.ev_g_energy(SKILL_AIR_JUMP) * 100)

    def reset_skill_stamina(self, skill_nd, skill_id):
        if not self.player:
            return
        stamina_count = self.player.ev_g_energy_segment(skill_id)
        if stamina_count > 0:
            self._stamina_count[skill_id] = stamina_count
            template_path = STAMINA_MAP.get(stamina_count, 'battle/i_fight_roll_1')
            cur_template_path = skill_nd.GetTemplatePath()
            if cur_template_path != template_path:
                widget_name = skill_nd.GetName()
                p = skill_nd.GetParent()
                skill_nd.Destroy()
                ret = global_data.uisystem.load_template_create(template_path, parent=p, root=self.panel, name=widget_name)
            return True
        return False

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    PC_KEY_HINT_RELEATED_UI_NAMES = ('btn_jump', )

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        if not self.PC_KEY_HINT_RELEATED_UI_NAMES:
            return
        show = pc_utils.should_pc_key_hint_related_uis_show(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON, hint_switch, display_option, pc_op_mode)
        for ui_name in self.PC_KEY_HINT_RELEATED_UI_NAMES:
            if not hasattr(self.panel, ui_name):
                continue
            ui = getattr(self.panel, ui_name)
            if not ui or not ui.isValid():
                continue
            ui.setVisible(show)

    def on_keyboard_hit_call(self, msg, keycode):
        if not self.panel.isVisible():
            return False
        else:
            if not global_data.battle:
                return False
            if global_data.battle.duel_stage == battle_const.CONCERT_FIGHT_STAGE and global_data.battle.is_king_or_defier_player():
                return False
            if is_down_msg(msg):
                self.on_begin_btn_icon_dacall(None, None)
            elif is_up_msg:
                if self._timeline_playing_idx == -1:
                    self.on_click_btn_icon_dacall(None, None)
                else:
                    self.on_end_btn_icon_dacall(None, None)
            return True