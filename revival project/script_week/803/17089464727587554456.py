# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/VideoPlayer.py
from __future__ import absolute_import
from __future__ import print_function
from common.daemon_thread import DaemonThreadPool
from common.framework import Singleton
import os
import game3d
from logic.comsys.video.VideoLoadingUI import VideoLoadingUI
from logic.comsys.video.VideoCtrlUI import VideoCtrlUI
from logic.comsys.video.VideoSkip import VideoSkip
from logic.manager_agents.manager_decorators import sync_exec
from common.utils import timer
import C_file
import cclive
STATE_VIDEO_INIT = 0
STATE_VIDEO_LOADING = 1
STATE_VIDEO_LOAED = 2
STATE_VIDEO_PLAYING = 3
STATE_VIDEO_STOP = 4
import exception_hook

class VideoPlayer(Singleton):
    ALIAS_NAME = 'video_player'

    def init(self, *args):
        super(VideoPlayer, self).init(*args)
        self.player = None
        self.load_id = 0
        self.state = STATE_VIDEO_INIT
        self.user_quit = False
        self.video_name = None
        self.hashed_video_path = None
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        self.hashed_video_name = None
        self.update_timer = 0
        self.remove_dialog_timer = 0
        self.custom_video_target = None
        self.dialog_index = 1
        self.repeat_time = 1
        self.bg_play = False
        self._disable_sound_mgr = True
        self.dialog_config = {}
        self._clip_enable = False
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        self.prev_players = []
        self._skip_time = 0
        self._skip_cb = None
        self.force_ignore_volume_setting = False
        self._is_mute = False
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.sound_sys_audio_mute += self.on_sys_audio_mute
        global_data.emgr.app_resume_event += self.on_app_resume

    def on_app_resume(self):
        if self.state == STATE_VIDEO_PLAYING:
            self.replay()

    def on_video_timer(self):
        if not self.dialog_config:
            return
        cur_dialog_info = self.dialog_config.get(str(self.dialog_index), {})
        if not cur_dialog_info:
            return
        ctrl_ui = global_data.ui_mgr.get_ui('VideoCtrlUI')
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
        ctrl_ui = global_data.ui_mgr.get_ui('VideoCtrlUI')
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
        self.hashed_video_name = None
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        self._clip_enable = False
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer)
        self.update_timer = 0
        global_data.game_mgr.unregister_logic_timer(self.remove_dialog_timer)
        self.remove_dialog_timer = 0
        self.dialog_index = 1
        self.dialog_config = {}
        self.custom_video_target = None
        self.repeat_time = 1
        self.bg_play = False
        self._disable_sound_mgr = True
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
            if self._disable_sound_mgr and not self._is_mute:
                global_data.sound_mgr.set_mute(True)
                global_data.sound_mgr.set_background(True, 0)
                self._is_mute = True
            provider = self.player.fetch_data_provider()
            if provider is None:
                print('[VideoPlayer] provider is None')
                self.stop_video()
                return
            if self.custom_video_target:
                self.custom_video_target()
            else:
                ui = VideoCtrlUI(clip_enable=self._clip_enable)
                ui.SeFullBgMode()
                ui.set_touch_close_enable(self._can_jump)
                if self.bg_play:
                    ui.set_zorder_bottom()
                if self._skip_time > 0:
                    VideoSkip(time=self._skip_time, skip_cb=self.on_skip_video)
            if self._on_play_ready_cb:
                self._on_play_ready_cb()
            return

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

    def play_video(self, video_name, cb, dialog_config={}, repeat_time=1, custom_video_target=None, bg_play=False, file_mode=0, complete_cb=None, seek_to_cb=None, disable_sound_mgr=True, can_jump=True, video_ready_cb=None, clip_enable=True, cb_args=(), skip_time=0, skip_callback=None, force_ignore_volume_setting=False):
        if self.state not in (STATE_VIDEO_INIT, STATE_VIDEO_STOP):
            if global_data.is_inner_server:
                print('[VideoPlayer] state:', self.state)
            return
        self.reset_data()
        self.init_player()
        self.video_name = video_name
        self.on_finished_callback = cb
        self.on_finished_callback_args = cb_args
        self._clip_enable = clip_enable
        self._on_play_ready_cb = video_ready_cb
        self._on_play_end_cb = complete_cb
        self._seek_to_cb = seek_to_cb
        self.dialog_config = dialog_config
        self.repeat_time = repeat_time
        self.custom_video_target = custom_video_target
        self.bg_play = bg_play
        self._disable_sound_mgr = disable_sound_mgr
        self._can_jump = False if bg_play else can_jump
        self._skip_time = skip_time
        self._skip_cb = skip_callback
        self.force_ignore_volume_setting = force_ignore_volume_setting
        self.load_video(file_mode)

    def play_vod(self, url, cb, bg_play=False, complete_cb=None, disable_sound_mgr=True, custom_video_target=None, seek_to_cb=None):
        if self.state not in (STATE_VIDEO_INIT, STATE_VIDEO_STOP):
            if global_data.is_inner_server:
                print('[VideoPlayer] state:', self.state)
            return
        self.reset_data()
        self.init_player()
        self.on_finished_callback = cb
        self._on_play_end_cb = complete_cb
        self.bg_play = bg_play
        self._disable_sound_mgr = disable_sound_mgr
        self.custom_video_target = custom_video_target
        self._seek_to_cb = seek_to_cb
        self.hashed_video_path = url
        self.player.stop()
        self.player.play_vod(url)

    def reset_finish_callback(self):
        self.on_finished_callback = None
        self.on_finished_callback_args = ()
        return

    def force_stop_video(self):
        self.reset_finish_callback()
        self.stop_video()

    def stop_video(self, remove_video=True, ignore_cb=False):
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
            if not self.force_ignore_volume_setting:
                if global_data.sound_mgr.is_sys_mute():
                    self.player.set_volume(0.0)
                else:
                    val = global_data.sound_mgr.get_total_video_volume()
                    self.player.set_volume(val / 10000.0)
        except Exception as e:
            try:
                exception_hook.post_error('[play video error] {} hashed path is {}'.format(str(e), self.hashed_video_path))
            except Exception as ee:
                exception_hook.post_error('[play video eee]{}'.format(str(ee)))

            game3d.delay_exec(10, self.on_stop_video)

    def remove_played_video(self):
        try:
            if not self.hashed_video_path:
                return
            if os.path.exists(self.hashed_video_path):
                os.remove(self.hashed_video_path)
        except Exception as e:
            print('[remove played video] error:', str(e))

    def on_video_load_finish(self, is_finish):
        if self.state != STATE_VIDEO_LOADING:
            return
        print('on video load finish:', is_finish)
        self.do_play_video() if is_finish else self.on_stop_video()

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
            string_id_int = game3d.calc_filename_hash64(self.video_name.replace('\\', '/'))
            hashed_video_name = str(abs(string_id_int))
            self.hashed_video_path = os.path.join(game3d.get_doc_dir(), 'v_tmp', hashed_video_name)
            dir_name = os.path.dirname(self.hashed_video_path)
            try:
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                self.hashed_video_name = hashed_video_name if game3d.get_platform() == game3d.PLATFORM_IOS else self.hashed_video_path
                with open(self.hashed_video_path, 'wb') as f:
                    f.write(video_data)
                res = True
            except Exception as e:
                print('[load video] write exception:', str(e))
                res = False

        game3d.delay_exec(1, cb, (res,))

    def on_stop_video(self, remove_video=True, ignore_cb=False, is_skip=False):
        global_data.ui_mgr.close_ui('VideoLoadingUI')
        global_data.ui_mgr.close_ui('VideoCtrlUI')
        global_data.ui_mgr.close_ui('VideoSkip')
        if remove_video:
            self.remove_played_video()
        self.reset_player()
        if self._disable_sound_mgr and self._is_mute:
            global_data.sound_mgr.set_mute(False)
            global_data.sound_mgr.set_background(False, 0)
            self._is_mute = False
        global_data.sound_mgr.Wakeup_bg_app_music()
        cb = self.on_finished_callback
        cb_args = self.on_finished_callback_args
        self.reset_data()
        if cb and not ignore_cb:
            cb(*cb_args)

    def load_video(self, file_mode):
        self.state = STATE_VIDEO_LOADING
        self.load_id += 1
        VideoLoadingUI()
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

    def is_in_init_state(self):
        return self.state == STATE_VIDEO_INIT

    def on_skip_video(self):
        if self._skip_cb:
            self._skip_cb()
        else:
            self.stop_video()