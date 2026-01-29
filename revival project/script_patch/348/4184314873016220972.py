# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryVideoController.py
from common.framework import Singleton
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cinematic.VideoListPlayer import VideoListPlayer, DISABLE_SOUND_TYPE_BG
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gutils.item_utils import REWARD_RARE_COLOR, get_item_need_show, get_lobby_item_type, is_default_skin
from logic.gutils.mall_utils import get_lottery_table_to_mode_map
from logic.gcommon.item.item_const import RARE_DEGREE_1, ITEM_SHOW_TYPE_MODEL, ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE
from .LotteryResultUI import LotteryResultUI
from .LotteryVideoBeforeUI import LotteryVideoBeforeUI
from logic.gcommon.item.lobby_item_type import L_ITEM_MECHA_SFX
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex
MODEL_SHOW_TYPE = 0
WEAPON_SHOW_TYPE = 1
CAN_CLICK_TIME = 5.5
VIDEO_NAME_TO_SOUND_EVENT_NAME_MAP = {'video/lottery_start.mp4': 'Play_ui_gift_start',
   'video/lottery_loop_01.mp4': 'Play_ui_gift_lp_01',
   'video/lottery_activate.mp4': 'Play_ui_gift_activate',
   'video/lottery_loop_02.mp4': 'Play_ui_gift_lp_02',
   'video/lottery_effect_blue.mp4': 'Play_ui_gift_prize_blue',
   'video/lottery_effect_green.mp4': 'Play_ui_gift_prize_green',
   'video/lottery_effect_purple.mp4': 'Play_ui_gift_prize_purple',
   'video/lottery_effect_orange.mp4': 'Play_ui_gift_prize_golden',
   'video/lottery_effect_red.mp4': 'Play_ui_gift_prize_red',
   'video/lottery_effect_color.mp4': 'Play_ui_gift_prize_colours'
   }

class LotteryVideoController(object):

    def __init__(self, parent):
        self.parent = parent
        self.init_params()
        self._init_lottery_video()
        self.process_event(True)

    def init_params(self):
        self._video_list_timer = 0
        self._video_time = 0
        self._mode_to_table_map = get_lottery_table_to_mode_map(reverse=True)
        self.reset_params()

    def reset_params(self):
        self._reward_list = []
        self._need_show_reward_item_list = set()
        self._chips_data = {}
        self._lottery_id = None
        self._video_item_id_dict = {}
        self._video_sound_list = []
        self._loop_video_sound_list = []
        self._show_index = 0
        self._release_video_list_timer()
        self._has_show_tips = False
        return

    def _init_lottery_video(self):
        video_list_player = VideoListPlayer()
        video_list = [
         'video/lottery_start.mp4',
         'video/lottery_loop_01.mp4',
         'video/lottery_activate.mp4',
         'video/lottery_loop_02.mp4',
         'video/lottery_effect_green.mp4',
         'video/lottery_effect_blue.mp4',
         'video/lottery_effect_purple.mp4',
         'video/lottery_effect_gold.mp4',
         'video/lottery_effect_red.mp4']
        video_list_player.preload_video(video_list)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_test_lottery_video': self.test_lottery_video_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _stop_cur_video(self, *args):
        video = global_data.video_list_player.get_cur_video()
        video and video.stop_video()

    def _play_video_sound(self, video):
        self._stop_loop_video_sound()
        video_name = video.get_video_name()
        sound_event_name = VIDEO_NAME_TO_SOUND_EVENT_NAME_MAP.get(video_name)
        if sound_event_name:
            sound = global_data.sound_mgr.play_sound_2d(sound_event_name)
            if video.get_repeat_time() == 0:
                self._loop_video_sound_list.append(sound)
            else:
                self._video_sound_list.append(sound)

    def _stop_loop_video_sound(self, *args):
        for sound in self._loop_video_sound_list:
            global_data.sound_mgr.stop_playing_id(sound)

        self._loop_video_sound_list = []

    def _stop_all_video_sound(self, *args):
        self._stop_loop_video_sound()
        for sound in self._video_sound_list:
            global_data.sound_mgr.stop_playing_id(sound)

        self._video_sound_list = []

    def _on_video_list_timer(self, dt):
        self._video_time += dt
        if self._video_time >= CAN_CLICK_TIME and not self._has_show_tips:
            self._set_lottery_tips_visible(True)
            self._has_show_tips = True
            global_data.ui_mgr.close_ui('VideoListSkip')

    def _release_video_list_timer(self):
        if self._video_list_timer:
            global_data.game_mgr.unregister_logic_timer(self._video_list_timer)
            self._video_list_timer = 0
            self._video_time = 0

    def _set_lottery_tips_visible(self, visible):
        ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if not ui:
            return
        if visible:
            ui.play_animation('show')
            ui.play_animation('loop')
        else:
            ui.play_animation('out')

    def play_lottery_video(self, item_list, origin_list, extra_info, lottery_id):
        print (
         '============item_list', item_list)
        print ('============origin_list', origin_list)
        lottery_result_ui = global_data.ui_mgr.get_ui('LotteryResultUI')
        if not lottery_result_ui:
            lottery_result_ui = LotteryResultUI()
        lottery_result_ui.hide()
        self._set_reward_data(item_list, origin_list, extra_info, lottery_id)
        self._show_index = 0
        if not self._reward_list:
            return
        transition_ui = global_data.ui_mgr.get_ui('LotteryVideoBeforeUI')
        if not transition_ui:
            transition_ui = LotteryVideoBeforeUI()
        transition_ui.show_transition()
        video_list_player = VideoListPlayer()

        def on_first_resume(video):
            self._release_video_list_timer()
            self._video_list_timer = global_data.game_mgr.register_logic_timer(self._on_video_list_timer, interval=0.5, mode=CLOCK, timedelta=True)
            self._play_video_sound(video)
            global_data.emgr.on_lottery_ended_event.emit()
            item_id_list = []
            for item_info in item_list:
                item_id = item_info[0]
                item_id_list.append(item_id)

            global_data.emgr.lottery_open_box_result.emit(item_id_list)

        def on_drag_begin_cb():
            if self._video_time >= CAN_CLICK_TIME:
                video_list_player.jump_video(1)
                self._stop_cur_video()
                self._set_lottery_tips_visible(False)

        def video_list_end_cb():
            self._release_video_list_timer()
            self._stop_all_video_sound()
            global_data.ui_mgr.close_ui('ScreenLockerUI')
            transition_ui = global_data.ui_mgr.get_ui('LotteryVideoBeforeUI')
            transition_ui and transition_ui.hide()
            self._show_next_award()

        def jump_loop_02_and_push_video():
            video_list_player.jump_video(3)
            global_data.game_mgr.register_logic_timer(self._stop_cur_video, times=1, interval=0.2, mode=CLOCK)
            self._set_lottery_tips_visible(False)

        first_reward_video_path = self._check_need_show_video()
        if first_reward_video_path:
            video_list_player.set_video_list_params(6, disable_sound_type=DISABLE_SOUND_TYPE_BG, can_jump_all=True, jump_all_cb=video_list_end_cb)
        else:
            video_list_player.set_video_list_params(5, disable_sound_type=DISABLE_SOUND_TYPE_BG, can_jump_all=True, jump_all_cb=video_list_end_cb)
        video_list_player.add_video('video/lottery_start.mp4', can_jump=False, need_remove=False, drag_begin_cb=on_drag_begin_cb, resume_cb=on_first_resume)
        video_list_player.add_video('video/lottery_loop_01.mp4', can_jump=False, need_remove=False, repeat_time=0, drag_begin_cb=self._stop_cur_video, resume_cb=self._play_video_sound)
        video_list_player.add_video('video/lottery_activate.mp4', can_jump=False, need_remove=False, drag_end_cb=jump_loop_02_and_push_video, resume_cb=self._play_video_sound)
        video_list_player.add_video('video/lottery_loop_02.mp4', can_jump=False, need_remove=False, repeat_time=0, drag_end_cb=self._stop_cur_video, resume_cb=self._play_video_sound)
        max_rare_degree = extra_info.get('max_rare_degree', RARE_DEGREE_1)
        color = REWARD_RARE_COLOR.get(max_rare_degree)
        lottery_effect_path = 'video/lottery_effect_{}.mp4'.format(color)
        if first_reward_video_path:
            video_list_player.add_video(lottery_effect_path, can_jump=False, need_remove=False, resume_cb=self._play_video_sound)
            video_list_player.add_video(first_reward_video_path, video_list_end_cb)
        else:
            video_list_player.add_video(lottery_effect_path, video_list_end_cb, can_jump=False, need_remove=False, resume_cb=self._stop_loop_video_sound)

    def _set_reward_data(self, item_list, origin_list, extra_info, lottery_id):
        self._need_show_reward_item_list = set()
        reward_list = []
        chips_data = {}
        cur_index = 0
        for origin_item_info in origin_list:
            if origin_item_info:
                reward_list.append(origin_item_info)
                chips_data[cur_index] = item_list[cur_index]
            else:
                reward_list.append(item_list[cur_index])
                item_no, _ = reward_list[-1]
                need_show = get_item_need_show(item_no)
                item_type = get_lobby_item_type(item_no)
                if need_show == ITEM_SHOW_TYPE_MODEL and not is_default_skin(item_no):
                    self._need_show_reward_item_list.add((item_no, MODEL_SHOW_TYPE))
                elif need_show == ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE:
                    self._need_show_reward_item_list.add((item_no, WEAPON_SHOW_TYPE))
                elif item_type == L_ITEM_MECHA_SFX:
                    self._need_show_reward_item_list.add((item_no, MODEL_SHOW_TYPE))
            cur_index += 1

        if not reward_list:
            return
        self._reward_list = reward_list
        self._chips_data = chips_data
        self._extra_info = extra_info
        self._lottery_id = lottery_id
        self._need_show_reward_item_list = list(self._need_show_reward_item_list)

    def _show_next_award(self):
        if self._show_index > len(self._need_show_reward_item_list) - 1:
            self._show_item_finished()
            return
        item_no, show_type = self._need_show_reward_item_list[self._show_index]

        def show_model_display():
            self._show_index += 1
            transition_ui = global_data.ui_mgr.get_ui('LotteryVideoBeforeUI')
            transition_ui and transition_ui.hide()
            if show_type == MODEL_SHOW_TYPE:
                if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                    global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                global_data.emgr.show_new_model_item.emit(item_no, self._show_next_award)
                global_data.emgr.hide_item_desc_ui_event.emit()
            elif show_type == WEAPON_SHOW_TYPE:
                if not global_data.ui_mgr.get_ui('GetWeaponDisplayUI'):
                    global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
                global_data.emgr.show_new_weapon_skin.emit(item_no, self._show_next_award)
                global_data.emgr.hide_item_desc_ui_event.emit()
            else:
                self._show_next_award()

        if self._show_index == 0:
            show_model_display()
        else:
            transition_ui = global_data.ui_mgr.get_ui('LotteryVideoBeforeUI')
            transition_ui and transition_ui.show()
            video_path = self._get_reward_video_path(item_no)
            if video_path:
                VideoPlayer().play_video(video_path, show_model_display)
            else:
                import game3d
                game3d.delay_exec(10, show_model_display)

    def _show_item_finished(self):
        global_data.ui_mgr.close_ui('LotteryVideoBeforeUI')
        global_data.emgr.on_lottery_ended_event.emit()
        lottery_result_ui = global_data.ui_mgr.get_ui('LotteryResultUI')
        lottery_result_ui.set_box_items(self._reward_list, self._chips_data, self._extra_info, self._lottery_id)
        self.reset_params()

    def _check_need_show_video(self):
        if self._need_show_reward_item_list:
            item_no = self._need_show_reward_item_list[0][0]
            video_path = self._get_reward_video_path(item_no)
            return video_path
        else:
            return None
            return None

    def _get_reward_video_path(self, item_no):
        if not self._video_item_id_dict:
            lottery_list_id = self._mode_to_table_map.get(self._lottery_id, None)
            if lottery_list_id is None:
                log_error('Lottery mode {} match preview_table failed!!!'.format(self._lottery_id))
            else:
                conf = confmgr.get('preview_%d' % lottery_list_id, default=None)
                if conf is None:
                    log_error('preview_%d' % lottery_list_id + ' not found!!!')
                else:
                    self._video_item_id_dict = conf.get('video_item_id_dict')
        if not self._video_item_id_dict:
            return ''
        else:
            video_name = self._video_item_id_dict.get(str(item_no))
            if video_name is None:
                print 'video_name not found!!!' + 'item_no %d' % item_no
                return ''
            return 'video/%s.mp4' % video_name

    def destroy(self):
        self.process_event(False)
        global_data.video_list_player.remove_all_played_video()

    def test_lottery_video_list(self, degree=None):
        if not degree:
            return
        video_list_player = VideoListPlayer()

        def video_list_end_cb():
            transition_ui = global_data.ui_mgr.get_ui('LotteryVideoBeforeUI')
            transition_ui and transition_ui.hide()
            self._show_next_award()

        def jump_loop_02_and_push_video():
            video_list_player.jump_video(3)
            global_data.game_mgr.register_logic_timer(self._stop_cur_video, times=1, interval=0.2, mode=CLOCK)

        video_list_player.set_video_list_params(5, disable_sound_type=DISABLE_SOUND_TYPE_BG)
        video_list_player.add_video('video/lottery_start.mp4', can_jump=False, need_remove=False, resume_cb=self._play_video_sound)
        video_list_player.add_video('video/lottery_loop_01.mp4', can_jump=False, need_remove=False, repeat_time=0, drag_begin_cb=self._stop_cur_video, resume_cb=self._play_video_sound)
        video_list_player.add_video('video/lottery_activate.mp4', can_jump=False, need_remove=False, drag_end_cb=jump_loop_02_and_push_video, resume_cb=self._play_video_sound)
        video_list_player.add_video('video/lottery_loop_02.mp4', can_jump=False, need_remove=False, repeat_time=0, drag_end_cb=self._stop_cur_video, resume_cb=self._play_video_sound)
        color = REWARD_RARE_COLOR.get(degree)
        lottery_effect_path = 'video/lottery_effect_{}.mp4'.format(color)
        video_list_player.add_video(lottery_effect_path, can_jump=False, need_remove=False, resume_cb=self._play_video_sound)