# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/movie_controller.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.framework import Singleton
from time import time
import math3d
import render

class MovieController(Singleton):

    def init(self, *args):
        self.movie_play_id = 0
        self.effect_ids = []
        self.screen_effects = []
        self.reset()
        self.init_event()
        self.init_handler()

    def init_event(self):
        global_data.emgr.app_background_event += self.on_app_background
        global_data.emgr.app_resume_event += self.on_app_resume
        global_data.emgr.net_login_reconnect_before_destroy_event += self.on_disconnect

    def on_app_background(self):
        if self.playing:
            self.background_time = time()

    def on_disconnect(self, *args):
        self.stop(None, False)
        return

    def init_handler(self):
        self.handle_dict = {'CAMERA_PREPARE': self.camera_prepare,
           'END': self.movie_end,
           'MODEL_SET': self.model_set,
           'MODEL_ANIM': self.model_anim,
           'MODEL_HIDDEN': self.model_hidden,
           'MODEL_SHOWED': self.model_showed,
           'MODEL_SET_VAR': self.model_set_var,
           'SFX_RESTART': self.sfx_restart,
           'SFX_SHUTDOWN': self.sfx_shutdown,
           'SP_LOBBY_MECHA_CAM': self.sp_lobby_mecha_cam,
           'MODEL_MOVE': self.model_move,
           'SCREEN_EFFECT': self.screen_effect,
           'SP_JET_SCENE_EFFECT': self.sp_jet_scene_effect,
           'SET_GLOBAL_UNIFORM': self.set_global_uniform
           }

    def movie_update(self):
        if not self.movie_data or self.movie_idx not in self.movie_data:
            self.movie_end()
            return
        while self.movie_idx in self.movie_data:
            cnt_data = self.movie_data[self.movie_idx]
            if not self.check_movie_time(cnt_data):
                return
            self.movie_idx += 1
            parameter = cnt_data.get('parameter', {})
            handler_key = cnt_data['action_name']
            self.handle_dict[handler_key](parameter, self.start_time)
            if not self.movie_data:
                break

    def check_movie_time(self, parameter):
        interval = parameter['action_time']
        cnt_time = time()
        gap = cnt_time - self.start_time - self.background_time
        return gap >= interval

    def on_app_resume(self):
        if self.playing:
            self.background_duration += time() - self.background_time
            self.background_time = 0

    def reset(self):
        self.background_time = 0
        self.start_time = 0
        self.background_duration = 0
        self.playing = False
        global_data.game_mgr.unregister_logic_timer(self.movie_play_id)
        self.movie_data = None
        self.movie_play_id = 0
        self.movie_idx = 0
        self.movie_end_callback = None
        return

    def parse_movie_data(self, movie_data):
        self.movie_data = movie_data
        self.movie_idx = 1

    def start(self, movie_data, movie_end_callback=None):
        if self.playing:
            return False
        self.reset()
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.movie_end_callback = movie_end_callback
        self.parse_movie_data(movie_data)
        self.playing = True
        self.start_time = time()
        self.movie_play_id = global_data.game_mgr.register_logic_timer(self.movie_update, 1)
        global_data.emgr.movie_start.emit()
        self.movie_update()
        return True

    def camera_prepare(self, parameter, start_time, *args):
        global_data.emgr.movie_camera_prepare.emit(parameter, start_time)
        print('movie prepare ok')

    def model_set(self, parameter, *args):
        global_data.emgr.movie_model_set.emit(parameter)
        print('movie model set')

    def model_anim(self, parameter, *args):
        global_data.emgr.movie_model_anim.emit(parameter)
        print('movie model anim')

    def model_hidden(self, parameter, *args):
        global_data.emgr.movie_model_hidden.emit(parameter)
        print('movie_model hidden')

    def model_showed(self, parameter, *args):
        global_data.emgr.movie_model_showed.emit(parameter)
        print('movie_model showed')

    def model_set_var(self, parameter, *args):
        global_data.emgr.movie_model_set_var.emit(parameter)
        print('model_set_var')

    def sfx_restart(self, parameter, *args):
        global_data.emgr.movie_sfx_restart.emit(parameter)
        print('sfx_restart')

    def sfx_shutdown(self, parameter, *args):
        global_data.emgr.movie_sfx_shutdown.emit(parameter)
        print('sfx_shutdown')

    def sp_lobby_mecha_cam(self, parameter, *args):
        global_data.emgr.movie_sp_lobby_mecha_cam.emit(parameter)

    def model_move(self, parameter, start_time, *args):
        global_data.emgr.movie_model_move.emit(parameter, start_time)

    def stop(self, parameter, with_callback=True):
        global_data.ui_mgr.close_ui('MovieUI')
        if not self.playing:
            return
        global_data.emgr.movie_end.emit(parameter)
        callback = self.movie_end_callback
        if with_callback and callback:
            callback()
        self.reset()

    def movie_end(self, parameter=None, *args):
        self.stop(parameter)

    def screen_effect(self, parameter, *args):
        position = math3d.vector(*parameter['position']) if 'position' in parameter else None
        global_data.emgr.show_screen_effect.emit(parameter['name'], {'position': position})
        return

    def sp_jet_scene_effect(self, parameter, *args):
        global_data.emgr.movie_sp_jet_scene_effect.emit(parameter)

    def set_global_uniform(self, parameter, *args):
        import world
        scn = world.get_active_scene()
        if not scn:
            return
        for k, v in six.iteritems(parameter):
            if global_data.is_ue_model:
                if k == 'FogDensity':
                    continue
            scn.set_global_uniform(k, v)