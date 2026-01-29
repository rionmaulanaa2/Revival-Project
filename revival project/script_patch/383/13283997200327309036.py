# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/VideoListPlayer.py
from __future__ import absolute_import
from __future__ import print_function
from common.daemon_thread import DaemonThreadPool
from common.framework import Singleton
import os
import game3d
from logic.comsys.video.VideoLoadingUI import VideoLoadingUI
from logic.comsys.video.VideoListCtrlUI import VideoListCtrlUI
from logic.comsys.video.VideoListSkip import VideoListSkip
from logic.comsys.video.VideoSkip import VideoSkip
from logic.manager_agents.manager_decorators import sync_exec
from common.utils import timer
import C_file
import cclive
import gc
STATE_VIDEO_INIT = 0
STATE_VIDEO_LOADING = 1
STATE_VIDEO_LOAED = 2
STATE_VIDEO_PLAYING = 3
STATE_VIDEO_STOP = 4
STATE_VIDEO_PAUSE = 5
import exception_hook
PLATFORM_TIME = {game3d.PLATFORM_ANDROID: 1000.0,
   game3d.PLATFORM_WIN32: 1000000.0,
   game3d.PLATFORM_IOS: 1000.0
   }
DISABLE_SOUND_TYPE_NONE = 0
DISABLE_SOUND_TYPE_BG = 1
DISABLE_SOUND_TYPE_ALL = 2

def calc_string_hash(video_name):
    string_id_int = game3d.calc_filename_hash64(video_name.replace('\\', '/'))
    hashed_video_name = str(abs(string_id_int))
    hashed_video_path = os.path.join(game3d.get_doc_dir(), 'v_tmp', hashed_video_name)
    return hashed_video_path.replace('\\', '/')


class VideoListPlayer(Singleton):
    ALIAS_NAME = 'video_list_player'

    def init(self, *args):
        super(VideoListPlayer, self).init(*args)
        self._init_params()

    def _init_params(self):
        self._time_scale = PLATFORM_TIME.get(game3d.get_platform(), 1)
        self._disable_sound_type = DISABLE_SOUND_TYPE_ALL
        self._proload_hashed_video_path_list = []
        self._reset_params()

    def _reset_params(self):
        self._video_list = []
        self._all_count = 0
        self._load_count = 0
        self._cur_play_index = 0
        self.update_timer = 0
        self._cur_time = 0
        self._ready_count = 0
        self._jump_video_list = []
        self._can_jump_all = False
        self._can_jump_all_time = 0
        self._jump_all_cb = None
        return

    def clear(self):
        for video_data in self._video_list:
            video = video_data
            video.clear_video()

        if self._disable_sound_type == DISABLE_SOUND_TYPE_BG:
            global_data.sound_mgr.resume_music()
            global_data.emgr.lobby_set_models_is_mute_event.emit(False)
        elif self._disable_sound_type == DISABLE_SOUND_TYPE_ALL:
            global_data.sound_mgr.set_mute(False)
            global_data.sound_mgr.set_background(False, 0)
        self._on_unregister_timer()
        self._reset_params()
        global_data.ui_mgr.close_ui('VideoListCtrlUI')
        global_data.ui_mgr.close_ui('VideoListSkip')

    def set_video_list_params(self, count, disable_sound_type=DISABLE_SOUND_TYPE_ALL, can_jump_all=False, can_jump_all_time=0, jump_all_cb=None):
        self._all_count = count
        self._disable_sound_type = disable_sound_type
        self._load_count = 0
        self._cur_play_index = 0
        self._ready_count = 0
        self._jump_video_list = []
        self._can_jump_all = can_jump_all
        self._can_jump_all_time = can_jump_all_time
        self._jump_all_cb = jump_all_cb

    def load_finish_cb(self):
        self._load_count += 1
        print('load_finish_cb', self._load_count, self._all_count)
        if self._load_count >= self._all_count:
            global_data.ui_mgr.close_ui('ScreenLockerUI')
            self._cur_play_index = 0
            for i in range(self._all_count):
                self.get_video(i).do_play_video()

    def _common_video_ready_cb(self, video_index):
        self._ready_count += 1
        print('common_video_ready_cb', self._ready_count, self._all_count)
        if self._ready_count == self._all_count:
            if self._disable_sound_type == DISABLE_SOUND_TYPE_BG:
                global_data.sound_mgr.pause_music()
                global_data.emgr.lobby_set_models_is_mute_event.emit(True)
            elif self._disable_sound_type == DISABLE_SOUND_TYPE_ALL:
                global_data.sound_mgr.set_mute(True)
                global_data.sound_mgr.set_background(True, 0)
            ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
            if not ctrl_ui:
                ctrl_ui = VideoListCtrlUI()
                ctrl_ui.SeFullBgMode()
            self.get_video(0).set_video_tex_sprite()
            self.get_video(1).set_video_tex_sprite()
            self._resume_cur_video()
            ctrl_ui.show_tex_sprite()
            ctrl_ui.show()
            if self._can_jump_all:
                VideoListSkip(time=self._can_jump_all_time, skip_cb=self._skip_all_video)

    def _skip_all_video(self):
        if self._jump_all_cb:
            self._jump_all_cb()
        self.clear()

    def _on_video_loop_timer(self, dt):
        video = self._video_list[self._cur_play_index]
        repeat_time = video.get_repeat_time()
        self._cur_time += dt
        player = video.get_player()
        if repeat_time == 0:
            if self._cur_time >= player.duration / self._time_scale - 0.5:
                player.seek_to(0)
                video.on_loop_cb()
                self._cur_time = 0
        elif repeat_time == 1:
            if self._cur_time >= player.duration / self._time_scale - 0.5:
                video.stop_video()

    def _on_unregister_timer(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer)
        self._cur_time = 0
        self.update_timer = 0

    def _resume_cur_video(self):
        cur_player = self.get_player(self._cur_play_index)
        cur_player.resume()
        self._on_unregister_timer()
        video = self.get_cur_video()
        repeat_time = video.get_repeat_time()
        if repeat_time == 0:
            self.update_timer = global_data.game_mgr.register_logic_timer(self._on_video_loop_timer, 1, timedelta=True)
        video.set_video_interaction_cb()
        video.on_resume_cb()

    def _common_finished_cb(self):
        self._on_unregister_timer()
        if not self._video_list:
            self.clear()
            return
        ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if not ctrl_ui:
            self.clear()
            return
        ctrl_ui.show_tex_sprite()
        video = self._video_list[self._cur_play_index]
        video.clear_video()
        self._cur_play_index += 1
        self._check_next_video_is_jump()
        if len(self._video_list) > self._cur_play_index + 1:
            self.get_video(self._cur_play_index + 1).set_video_tex_sprite()
        if len(self._video_list) > self._cur_play_index:
            self._resume_cur_video()
        else:
            self.clear()

    def add_video(self, video_name, cb=None, dialog_config=None, repeat_time=1, custom_video_target=None, bg_play=False, file_mode=0, complete_cb=None, seek_to_cb=None, can_jump=True, video_ready_cb=None, clip_enable=True, cb_args=None, skip_time=0, skip_callback=None, force_ignore_volume_setting=False, need_remove=True, click_cb=None, drag_begin_cb=None, drag_cb=None, drag_end_cb=None, loop_cb=None, resume_cb=None):

        def on_video_ready_cb(video_index):
            if video_ready_cb:
                video_ready_cb()
            self._common_video_ready_cb(video_index)

        def on_finished_callback(*cb_args):
            if cb:
                cb(*cb_args)
            self._common_finished_cb()

        video = Video()
        self._video_list.append(video)
        dialog_config = dialog_config or {}
        cb_args = cb_args or ()
        video.play_video(video_name, on_finished_callback, dialog_config, repeat_time, custom_video_target, bg_play, file_mode, complete_cb, seek_to_cb, can_jump, on_video_ready_cb, clip_enable, cb_args, skip_time, skip_callback, force_ignore_volume_setting, len(self._video_list) - 1, need_remove, self.load_finish_cb, click_cb, drag_begin_cb, drag_cb, drag_end_cb, loop_cb, resume_cb)

    def get_video(self, index):
        if index < 0 or index >= len(self._video_list):
            return None
        else:
            return self._video_list[index]

    def get_cur_video(self):
        return self.get_video(self._cur_play_index)

    def _check_next_video_is_jump(self):
        if self._cur_play_index in self._jump_video_list:
            self._cur_play_index += 1
            self._check_next_video_is_jump()

    def jump_video(self, jump_index):
        if self._cur_play_index >= jump_index or jump_index > len(self._video_list) or jump_index in self._jump_video_list:
            return
        self._jump_video_list.append(jump_index)
        if self._cur_play_index + 1 == jump_index:
            self.get_video(jump_index + 1).set_video_tex_sprite()

    def get_player(self, index):
        if index < 0 or index >= len(self._video_list):
            return None
        else:
            return self.get_video(index).get_player()

    def preload_video(self, video_name_list):
        dir_name = os.path.join(game3d.get_doc_dir(), 'v_tmp').replace('\\', '/')
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        for video_name in video_name_list:
            hashed_video_path = calc_string_hash(video_name)
            self._proload_hashed_video_path_list.append(hashed_video_path)
            DaemonThreadPool().add_threadpool(self.thread_load_video, None, video_name)

        return

    def thread_load_video(self, video_name):

        def cb(res):
            pass

        if not video_name or not C_file.find_res_file(video_name, ''):
            res = False
        else:
            print('start loading video', video_name)
            video_data = C_file.get_res_file(video_name, '')
            hashed_video_path = calc_string_hash(video_name)
            dir_name = os.path.dirname(hashed_video_path)
            try:
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                with open(hashed_video_path, 'wb') as f:
                    f.write(video_data)
                res = True
            except Exception as e:
                print('[load video] write exception:', str(e))
                res = False

        game3d.delay_exec(1, cb, (res,))

    def remove_all_played_video(self):
        for hashed_video_path in self._proload_hashed_video_path_list:
            if not hashed_video_path:
                continue
            try:
                if os.path.exists(hashed_video_path):
                    print('[remove played video] {}'.format(hashed_video_path))
                    os.remove(hashed_video_path)
            except Exception as e:
                print('[remove played video error] {} hashed path is {}'.format(str(e), hashed_video_path))


class Video(object):

    def __init__(self, *args):
        super(Video, self).__init__(*args)
        self.player = None
        self.load_id = 0
        self.state = STATE_VIDEO_INIT
        self.user_quit = False
        self.video_name = None
        self.hashed_video_path = None
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        self.update_timer = 0
        self.remove_dialog_timer = 0
        self.custom_video_target = None
        self.dialog_index = 1
        self.repeat_time = 1
        self.bg_play = False
        self.dialog_config = {}
        self._clip_enable = False
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        self._load_finish_cb = None
        self._click_cb = None
        self._drag_begin_cb = None
        self._drag_cb = None
        self._drag_end_cb = None
        self._loop_cb = None
        self._resume_cb = None
        self.prev_players = []
        self._skip_time = 0
        self._skip_cb = None
        self.force_ignore_volume_setting = False
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.sound_sys_audio_mute += self.on_sys_audio_mute
        global_data.emgr.app_pause_event += self.on_app_pause
        global_data.emgr.app_background_event += self.on_app_background
        global_data.emgr.app_resume_event += self.on_app_resume

    def remove_event(self):
        global_data.emgr.sound_sys_audio_mute -= self.on_sys_audio_mute
        global_data.emgr.app_pause_event -= self.on_app_pause
        global_data.emgr.app_background_event -= self.on_app_background
        global_data.emgr.app_resume_event -= self.on_app_resume

    def on_app_pause(self):
        cur_video = VideoListPlayer().get_cur_video()
        if self != cur_video:
            return
        if self.state == STATE_VIDEO_PLAYING:
            self.player.pause()
            self.state = STATE_VIDEO_PAUSE

    def on_app_background(self):
        cur_video = VideoListPlayer().get_cur_video()
        if self != cur_video:
            return
        if self.state == STATE_VIDEO_PLAYING:
            self.player.pause()
            self.state = STATE_VIDEO_PAUSE

    def on_app_resume(self):
        cur_video = VideoListPlayer().get_cur_video()
        if self != cur_video:
            return
        if self.state == STATE_VIDEO_PAUSE:
            self.player.resume()

    def on_video_timer(self):
        if not self.dialog_config:
            return
        cur_dialog_info = self.dialog_config.get(str(self.dialog_index), {})
        if not cur_dialog_info:
            return
        ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if not ctrl_ui:
            return
        cur_pos = self.player.current_position
        txt_id = cur_dialog_info['txt_id']
        cur_sec = cur_pos / 1000.0
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            cur_sec = cur_sec / 1000.0
        if cur_sec > cur_dialog_info['dialog_time']:
            ctrl_ui.show_dialog(txt_id)
            self.dialog_index += 1
            global_data.game_mgr.unregister_logic_timer(self.remove_dialog_timer)
            self.remove_dialog_timer = global_data.game_mgr.register_logic_timer(self.on_remove_dialog_timer, cur_dialog_info['dialog_duration'], times=1, mode=timer.CLOCK)

    def on_remove_dialog_timer(self):
        ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if not ctrl_ui:
            return
        ctrl_ui.hide_dialog()

    def reset_event(self):
        self.player.error_callback = self.error_callback
        self.player.video_ready_callback = self.video_ready_callback
        self.player.video_complete_callback = self.video_complete_callback
        self.player.seek_complete_callback = self._seek_to_complete_cb

    def reset_player(self):
        if self.player:
            self.player.stop()
            self.prev_players.append(self.player)
            self.player = None
            self.recyle_players()
        return

    @sync_exec
    def recyle_players(self):
        self.prev_players = []

    def init_player(self):
        if self.player:
            self.reset_player()
        self.player = cclive.player()
        self.reset_event()

    def reset_data(self):
        self.state = STATE_VIDEO_INIT
        self.user_quit = False
        self.video_name = None
        self.hashed_video_path = None
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        self._clip_enable = False
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        self._load_finish_cb = None
        self._click_cb = None
        self._drag_begin_cb = None
        self._drag_cb = None
        self._drag_end_cb = None
        self._loop_cb = None
        self._resume_cb = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer)
        self.update_timer = 0
        global_data.game_mgr.unregister_logic_timer(self.remove_dialog_timer)
        self.remove_dialog_timer = 0
        self.dialog_index = 1
        self.dialog_config = {}
        self.custom_video_target = None
        self.repeat_time = 1
        self.bg_play = False
        self._skip_time = 0
        self._skip_cb = None
        self.force_ignore_volume_setting = False
        return

    def error_callback(self, *args):
        print('erro with args', args)

        def error_cb():
            self.stop_video()

        game3d.delay_exec(1, error_cb)

    def video_ready_callback(self, *args):
        print('on video ready', args)
        self.update_timer = global_data.game_mgr.register_logic_timer(self.on_video_timer, 1)
        if not self.player:
            self.stop_video()
            return
        else:
            self.player.loop_count = self.repeat_time
            provider = self.player.fetch_data_provider()
            if provider is None:
                print('[VideoPlayer] provider is None')
                self.stop_video()
                return
            if self.custom_video_target:
                self.custom_video_target()
            elif self._skip_time > 0:
                VideoSkip(time=self._skip_time, skip_cb=self.on_skip_video)
            print('=====================', self.video_index, self.video_name)
            if self.video_index > 0:
                self.player.pause()
                self.player.seek_to(0)
                self.state = STATE_VIDEO_PAUSE
            if self._on_play_ready_cb:
                self._on_play_ready_cb(self.video_index)
            return

    def set_video_tex_sprite(self, *args):
        ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if ctrl_ui:
            ctrl_ui.set_spr_clip_enable(self._clip_enable)
            ctrl_ui.init_tex_sprite(self.video_index)
            if self.bg_play:
                ctrl_ui.set_zorder_bottom()

    def set_video_interaction_cb(self, *args):
        ctrl_ui = global_data.ui_mgr.get_ui('VideoListCtrlUI')
        if ctrl_ui:
            ctrl_ui.set_interaction_cb(self._click_cb, self._drag_begin_cb, self._drag_cb, self._drag_end_cb)
            if self._can_jump:
                ctrl_ui.set_touch_close_enable(True)

    def video_complete_callback(self, *args):
        if self._on_play_end_cb:
            self._on_play_end_cb()
            return

        def complete_callback():
            self.stop_video()

        if self.repeat_time != 0:
            game3d.delay_exec(1, complete_callback)
        else:
            self.replay()

    def _seek_to_complete_cb(self, *args):
        if self._seek_to_cb:
            self._seek_to_cb()

    def replay(self):
        if self.player:
            self.player.stop()
            if self.hashed_video_path:
                self.player.play_vod(self.hashed_video_path)
                self.on_sys_audio_mute()

    def play_video(self, video_name, cb, dialog_config=None, repeat_time=1, custom_video_target=None, bg_play=False, file_mode=0, complete_cb=None, seek_to_cb=None, can_jump=True, video_ready_cb=None, clip_enable=True, cb_args=None, skip_time=0, skip_callback=None, force_ignore_volume_setting=False, video_index=0, need_remove=True, load_finish_cb=None, click_cb=None, drag_begin_cb=None, drag_cb=None, drag_end_cb=None, loop_cb=None, resume_cb=None):
        if self.state not in (STATE_VIDEO_INIT, STATE_VIDEO_STOP):
            if global_data.is_inner_server:
                print('[VideoPlayer] state:', self.state)
            return
        else:
            self.reset_data()
            self.init_player()
            self.video_name = video_name
            self.on_finished_callback = cb
            self.on_finished_callback_args = cb_args or ()
            self._clip_enable = clip_enable
            self._on_play_ready_cb = video_ready_cb
            self._on_play_end_cb = complete_cb
            self._seek_to_cb = seek_to_cb
            self.dialog_config = dialog_config or {}
            self.repeat_time = repeat_time
            self.custom_video_target = custom_video_target
            self.bg_play = bg_play
            self._can_jump = False if bg_play else can_jump
            self._skip_time = skip_time
            self._skip_cb = skip_callback
            self.force_ignore_volume_setting = force_ignore_volume_setting
            self.video_index = video_index
            self._need_remove = need_remove
            self._load_finish_cb = load_finish_cb
            self._click_cb = click_cb
            self._drag_begin_cb = drag_begin_cb
            self._drag_cb = drag_cb
            self._drag_end_cb = drag_end_cb
            if repeat_time == 0:
                self._loop_cb = loop_cb
            else:
                self._loop_cb = None
            self._resume_cb = resume_cb
            self.load_video(file_mode)
            return

    def play_vod(self, url, cb, bg_play=False, complete_cb=None, custom_video_target=None, seek_to_cb=None):
        if self.state not in (STATE_VIDEO_INIT, STATE_VIDEO_STOP):
            if global_data.is_inner_server:
                print('[VideoPlayer] state:', self.state)
            return
        self.reset_data()
        self.init_player()
        self.on_finished_callback = cb
        self._on_play_end_cb = complete_cb
        self.bg_play = bg_play
        self.custom_video_target = custom_video_target
        self._seek_to_cb = seek_to_cb
        self.hashed_video_path = url
        self.player.stop()
        self.player.play_vod(url)
        self.on_sys_audio_mute()

    def reset_finish_callback(self):
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        return

    def force_stop_video(self):
        self.reset_finish_callback()
        self.stop_video()

    def stop_video(self, remove_video=True, ignore_cb=False, is_click_stop=False):
        if not self.player:
            return
        self.player.stop()
        self.on_stop_video(remove_video, ignore_cb)

    def do_play_video(self):
        global_data.ui_mgr.close_ui('VideoLoadingUI')
        self.state = STATE_VIDEO_PLAYING
        try:
            width, height, depth, windowType, multisample = game3d.get_window_size()
            if global_data.is_inner_server:
                print('play vod ', self.hashed_video_path)
            if not self.player or not self.hashed_video_path:
                return
            self.player.play_vod(self.hashed_video_path)
            self.on_sys_audio_mute()
        except Exception as e:
            try:
                exception_hook.post_error('[play video error] {} hashed path is {}'.format(str(e), self.hashed_video_path))
            except Exception as ee:
                exception_hook.post_error('[play video eee]{}'.format(str(ee)))

            game3d.delay_exec(10, self.on_stop_video)

    def remove_played_video(self):
        if self._need_remove == False:
            return
        try:
            if not self.hashed_video_path:
                return
            if os.path.exists(self.hashed_video_path):
                os.remove(self.hashed_video_path)
        except:
            pass

    def on_video_load_finish(self, is_finish):
        if self.state != STATE_VIDEO_LOADING:
            return
        print('on video load finish:', is_finish)
        if not is_finish:
            VideoListPlayer()._skip_all_video()
            return
        if self._load_finish_cb:
            self._load_finish_cb()

    def thread_load_video(self, load_id):

        def cb(res):
            if load_id != self.load_id:
                return
            self.on_video_load_finish(res)

        if not self.video_name or not C_file.find_res_file(self.video_name, ''):
            res = False
        else:
            print('start loading video', self.video_name)
            video_data = C_file.get_res_file(self.video_name, '')
            self.hashed_video_path = calc_string_hash(self.video_name)
            dir_name = os.path.dirname(self.hashed_video_path)
            try:
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                with open(self.hashed_video_path, 'wb') as f:
                    f.write(video_data)
                res = True
            except Exception as e:
                print('[load video] write exception:', str(e))
                res = False

        game3d.delay_exec(1, cb, (res,))

    def on_stop_video(self, remove_video=True, ignore_cb=False, is_skip=False):
        global_data.ui_mgr.close_ui('VideoLoadingUI')
        global_data.ui_mgr.close_ui('VideoSkip')
        cb = self.on_finished_callback
        cb_args = self.on_finished_callback_args
        if cb and not ignore_cb:
            cb(*cb_args)

    def on_loop_cb(self):
        if self._loop_cb and callable(self._loop_cb):
            self._loop_cb(self)

    def on_resume_cb(self):
        if self._resume_cb and callable(self._resume_cb):
            self._resume_cb(self)

    def clear_video(self):
        self.remove_event()
        self.remove_played_video()
        self.reset_data()
        self.reset_player()

    def load_video(self, file_mode):
        self.state = STATE_VIDEO_LOADING
        self.load_id += 1
        VideoLoadingUI()
        hashed_video_path = calc_string_hash(self.video_name)
        if os.path.exists(hashed_video_path):
            self.hashed_video_path = hashed_video_path
            self.on_video_load_finish(True)
            return
        else:
            if file_mode == 0:
                DaemonThreadPool().add_threadpool(self.thread_load_video, None, self.load_id)
            else:
                self.hashed_video_path = self.video_name
                res = os.path.exists(self.hashed_video_path) or False if 1 else True
                self.on_video_load_finish(res)
            return

    def on_sys_audio_mute(self):
        if self.player:
            if global_data.sound_mgr.is_sys_mute():
                self.player.set_volume(0.0)
            else:
                val = global_data.sound_mgr.get_total_video_volume()
                self.player.set_volume(val / 10000.0)

    def get_player(self):
        return self.player

    def get_repeat_time(self):
        return self.repeat_time

    def get_video_name(self):
        return self.video_name

    def is_in_init_state(self):
        return self.state == STATE_VIDEO_INIT

    def on_skip_video(self):
        if self._skip_cb:
            self._skip_cb()
        else:
            self.stop_video()