# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_video.py
from __future__ import absolute_import
from __future__ import print_function
import os
import game
import render
import game3d
import C_file
import cclive
from cocosui import cc, ccs
STATE_VIDEO_INIT = 0
STATE_VIDEO_LOADING = 1
STATE_VIDEO_PLAYING = 2
STATE_VIDEO_STOPPING = 3
PATCH_VIDEO_INSTANCE = None

def get_patch_video_instance():
    global PATCH_VIDEO_INSTANCE
    if not PATCH_VIDEO_INSTANCE:
        PATCH_VIDEO_INSTANCE = PatchVideoPlayer()
    return PATCH_VIDEO_INSTANCE


def destroy_patch_video_instance():
    global PATCH_VIDEO_INSTANCE
    if PATCH_VIDEO_INSTANCE:
        PATCH_VIDEO_INSTANCE.force_stop_video()
    PATCH_VIDEO_INSTANCE = None
    return


class PatchVideoPlayer(object):

    def __init__(self):
        super(PatchVideoPlayer, self).__init__()
        self.player = None
        self.load_id = 0
        self.state = STATE_VIDEO_INIT
        self.video_name = None
        self._spr_cc = None
        self._widget = None
        self.hashed_video_name = None
        self.hashed_video_path = None
        self._on_stop_callback = None
        self._on_stop_callback_args = ()
        self.custom_video_target = None
        self.repeat_time = 1
        self._is_mute = False
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        self._init_game_event()
        return

    def is_playing(self):
        return self.state == STATE_VIDEO_PLAYING

    def set_mute(self, is_mute):
        try:
            if not self.player:
                return
            self._is_mute = is_mute
            if is_mute:
                self.player.set_volume(0.0)
            else:
                self.player.set_volume(1.0)
        except Exception as e:
            print('[patch video] set mute except:', str(e))

    def set_stop_callback(self, in_stop_cb, cb_args=()):
        self._on_stop_callback = in_stop_cb
        self._on_stop_callback_args = cb_args

    def set_complete_cb(self, complete_cb):
        self._on_play_end_cb = complete_cb

    def set_video_ready_cb(self, video_ready_cb):
        self._on_play_ready_cb = video_ready_cb

    def init_player(self):
        if self.player:
            self.reset_player()
        self.player = cclive.player()
        self._reset_player_event()

    def _reset_player_event(self):
        if not self.player:
            return
        self.player.error_callback = self.error_callback
        self.player.video_ready_callback = self.video_ready_callback
        self.player.video_complete_callback = self.video_complete_callback
        self.player.seek_complete_callback = self._seek_to_complete_cb

    def reset_player(self):
        try:
            if not self.player:
                return
            self.player.stop()
            self.player = None
        except Exception as e:
            print('[patch video] reset player except:', str(e))

        return

    def reset_data(self):
        self.state = STATE_VIDEO_INIT
        self.video_name = None
        self.hashed_video_path = None
        self.hashed_video_name = None
        self._on_stop_callback = None
        self._on_stop_callback_args = ()
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        self.custom_video_target = None
        self.repeat_time = 1
        self._is_mute = False
        return

    def error_callback(self, *args):
        print('[patch video] error cb:', args)
        game3d.delay_exec(1, self.stop_video)

    def video_ready_callback(self, *args):
        print('[patch video] ready cb:', args)
        try:
            if not self.player:
                self.stop_video()
                return
            self.player.loop_count = self.repeat_time
            if self._is_mute:
                self.player.set_volume(0.0)
            provider = self.player.fetch_data_provider()
            if provider is None:
                print('[patch video] error: provider is None')
                self.stop_video()
                return
            if self.custom_video_target:
                self.custom_video_target()
            else:
                ret = self._create_video_ui()
                if not ret:
                    self.stop_video()
                    return
            if self._on_play_ready_cb:
                self._on_play_ready_cb()
        except Exception as e:
            print('[patch video] ready cb except:', str(e))

        return

    def video_complete_callback(self, *args):
        if self._on_play_end_cb:
            self._on_play_end_cb()
            return
        if self.repeat_time != 0:
            game3d.delay_exec(1, self.stop_video)
        else:
            self.replay()

    def _seek_to_complete_cb(self, *args):
        if self._seek_to_cb:
            self._seek_to_cb()

    def replay(self):
        try:
            if not self.player:
                return
            self.player.stop()
            if self.hashed_video_path and os.path.exists(self.hashed_video_path):
                self.player.play_vod(self.hashed_video_path)
                if self._is_mute:
                    self.player.set_volume(0.0)
        except Exception as e:
            print('[patch video] replay except:', str(e))

    def play_video(self, video_name, stop_cb, repeat_time=1, custom_video_target=None, file_mode=0, complete_cb=None, seek_to_cb=None, is_mute=False, video_ready_cb=None, cb_args=()):
        if self.state not in (STATE_VIDEO_INIT,):
            print('[patch video] state:', self.state)
            return
        print('[patch video] play video:', video_name)
        self.reset_data()
        self.init_player()
        self.video_name = video_name
        self._on_stop_callback = stop_cb
        self._on_stop_callback_args = cb_args
        self._on_play_ready_cb = video_ready_cb
        self._on_play_end_cb = complete_cb
        self._seek_to_cb = seek_to_cb
        self.repeat_time = repeat_time
        self.custom_video_target = custom_video_target
        self._is_mute = is_mute
        self.load_video(file_mode)

    def load_video(self, file_mode):
        self.state = STATE_VIDEO_LOADING
        self.load_id += 1
        if file_mode == 0:
            import threading
            t = threading.Thread(target=self.thread_load_video, args=(self.load_id,))
            t.setDaemon(True)
            t.start()
        else:
            self.hashed_video_path = self.video_name
            res = os.path.exists(self.hashed_video_path) or False if 1 else True
            self.on_video_load_finish(res)

    def thread_load_video(self, load_id):
        if not self.video_name or not C_file.find_res_file(self.video_name, ''):
            print('[patch video]:{} not exists'.format(self.video_name))
            res = False
        else:
            try:
                video_data = C_file.get_res_file(self.video_name, '')
                string_id_int = game3d.calc_filename_hash64(self.video_name.replace('\\', '/'))
                hashed_video_name = str(abs(string_id_int))
                self.hashed_video_path = os.path.join(game3d.get_doc_dir(), 'v_tmp', hashed_video_name)
                if not os.path.exists(game3d.get_doc_dir()):
                    os.makedirs(game3d.get_doc_dir())
                if game3d.get_platform() == game3d.PLATFORM_IOS:
                    self.hashed_video_name = hashed_video_name if 1 else self.hashed_video_path
                    print('[patch video] hash path:', self.hashed_video_path)
                    dir_name = os.path.dirname(self.hashed_video_path)
                    os.path.exists(dir_name) or os.makedirs(dir_name)
                with open(self.hashed_video_path, 'wb') as tmp_file:
                    tmp_file.write(video_data)
                res = True
            except Exception as e:
                print('[patch video] write exception:', str(e))
                res = False

        def cb(res):
            if load_id != self.load_id:
                return
            self.on_video_load_finish(res)

        game3d.delay_exec(1, cb, (res,))

    def on_video_load_finish(self, is_finish):
        if self.state != STATE_VIDEO_LOADING:
            return
        print('[patch video] load video finish:', is_finish)
        self.do_play_video() if is_finish else self.stop_video()

    def do_play_video(self):
        self.state = STATE_VIDEO_PLAYING
        try:
            if not self.player or not self.hashed_video_path or not os.path.exists(self.hashed_video_path):
                self.stop_video()
                return
            self.player.play_vod(self.hashed_video_path)
            if self._is_mute:
                self.player.set_volume(0.0)
            else:
                self.player.set_volume(1.0)
        except Exception as e:
            print('[patch video] play except:', str(e))
            game3d.delay_exec(1, self.stop_video)

    def reset_all_callback(self):
        game.on_resume = None
        self._on_stop_callback = None
        self._on_stop_callback_args = ()
        self._on_stop_callback = None
        self._on_stop_callback_args = None
        self._on_play_ready_cb = None
        self._on_play_end_cb = None
        self._seek_to_cb = None
        return

    def force_stop_video(self):
        self.stop_video()
        self.reset_all_callback()

    def stop_video(self, remove_video=True, ignore_cb=False):
        print('[patch video] stop video new')
        if self.player:
            self.player.stop()
        game3d.frame_delay_exec(2, self.delay_destroy_player)
        self._destroy_widget()
        if remove_video:
            self._remove_played_video()
        cb = self._on_stop_callback
        cb_args = self._on_stop_callback_args
        self.reset_data()
        self.state = STATE_VIDEO_STOPPING
        if cb and not ignore_cb:
            cb(*cb_args)

    def delay_destroy_player(self):
        self.state = STATE_VIDEO_INIT
        try:
            if not self.player:
                return
            self.player.stop()
            self.player = None
        except Exception as e:
            print('[patch video] reset player except:', str(e))

        return

    def _destroy_widget(self):
        try:
            if self._spr_cc:
                self._spr_cc.removeFromParent()
        except Exception as e:
            print('[patch video] remove sprite except:', str(e))

        try:
            if self._widget:
                self._widget.removeFromParent()
        except Exception as e:
            print('[patch video] remove widget except:', str(e))

        self._spr_cc = None
        self._widget = None
        return

    def _remove_played_video(self):
        if not self.hashed_video_path or not os.path.exists(self.hashed_video_path):
            return

        def remove_played_video(remove_path=self.hashed_video_path):
            try:
                if not remove_path or not os.path.exists(remove_path):
                    return
                os.remove(remove_path)
            except Exception as e:
                print('[patch video] remove error:', str(e))

        game3d.frame_delay_exec(3, remove_played_video)

    def _create_video_ui(self):
        try:
            reader = ccs.GUIReader.getInstance()
            widget = reader.widgetFromJsonFile('gui/patch_ui/patch_video.json')
            from .patch_utils import PATCH_UI_LAYER, normalize_widget
            widget = normalize_widget(widget)
            self._widget = widget
            director = cc.Director.getInstance()
            scene = director.getRunningScene()
            scene.addChild(widget, 0)
            provider = self.player.fetch_data_provider()
            render_tex = render.texture('cclive', data_provider=provider)
            spr_cc = cc.Sprite.createWithTexture(cc.Texture2D.createWithITexture(render_tex))
            self._spr_cc = spr_cc
            widget.addChild(spr_cc, 2)
            self.set_scale_and_pos()
            self.check_spr_shader(spr_cc)
            return True
        except Exception as e:
            print('[patch video] create video ui error:', str(e))
            return False

    def set_scale_and_pos(self):
        if not self._spr_cc:
            return
        try:
            director = cc.Director.getInstance()
            view = director.getOpenGLView()
            v_size = view.getVisibleSize()
            spr_size = self._spr_cc.getContentSize()
            width_ratio = v_size.width / spr_size.width
            height_ratio = v_size.height / spr_size.height
            max_ratio = max(width_ratio, height_ratio)
            self._spr_cc.setScale(max_ratio)
            self._spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
            self._spr_cc.setPosition(cc.Vec2(v_size.width * 0.5, v_size.height * 0.5))
        except Exception as e:
            print('[patch video] set scale and pos except:', str(e))

    def check_spr_shader(self, spr):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():

            def create_shader(vs, ps):
                postfix_vs = 'vs'
                postfix_ps = 'ps'
                format_str = '{0}/{1}.{2}'
                SHADER_PATH = 'shader/ui2'
                vs_path = format_str.format(SHADER_PATH, vs, postfix_vs)
                ps_path = format_str.format(SHADER_PATH, ps, postfix_ps)
                shader = cc.GLProgram.createWithFilenames(vs_path, ps_path)
                return shader

            gl_yuv = create_shader('yuv_texture', 'yuv_texture')
            program_yuv = cc.GLProgramState.getOrCreateWithGLProgram(gl_yuv)
            spr.setGLProgramState(program_yuv)

    def _init_game_event(self):
        game.on_resume = self._on_app_resume

    def _on_app_resume(self):
        if self.state == STATE_VIDEO_PLAYING:
            self.replay()