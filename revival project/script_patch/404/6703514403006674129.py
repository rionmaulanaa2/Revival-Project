# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBattleVideoMgr.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import time
import cclive
import render
import game3d
import os
import C_file
from random import randint
from common.daemon_thread import DaemonThreadPool
import world
from logic.gutils.screen_effect_utils import SCREEN_EFFECT_SCALE
from logic.gcommon import time_utility
import common.utils.timer as timer
from common.framework import Functor
import world
from common.cfg import confmgr
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
s_mv_model = 'model_new\\scene\\aijiangwutai\\item_ajld_pm_a01.gim'
s_tv_info = [
 (
  (1073.88, 811, 2203.88), 43.35, (1.0, 1.0, 1.0))]
s_video_url = 'https://nie.v.netease.com/nie/2022/0118/c2d2a104d0bd58dc23163456fc838c32.mp4'
s_video_last_time = 3283.0
s_mv_wait_pic = 'model_new\\scene\\aijiangwutai\\textures\\mv_wati_bg.png'
s_cc_sound_volume_scale = 2.5

class PartBattleVideoMgr(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartBattleVideoMgr, self).__init__(scene, name, need_update=True)
        self.render_tex = None
        self.cclive_player = cclive.player()
        self.mv_model = None
        self.mv_wait_model = None
        self.is_mv_ready = False
        self.is_bind_mv_model = False
        self.is_wait = True
        self.is_end = False
        self.save_cc_sound_volume = 0.0
        self.video_start = confmgr.get('game_mode/concert/play_data', 'sing_time_conf')[0][0]
        self.concert_start_ts = global_data.battle.get_concert_start_ts()
        if self.concert_start_ts > 0:
            self.all_time = time_utility.get_server_time() - self.concert_start_ts
        else:
            self.all_time = 0
        self.last_time = global_data.game_time
        self.is_check_progress = False
        self.max_check_progress_count = 0
        self.check_progress_downcount = 0
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            self.seek_scale = 1000000.0
        else:
            self.seek_scale = 1000.0
        global_data.emgr.update_battle_stage += self.on_update_battle_stage
        global_data.emgr.cc_sound_volume_change += self.on_sound_volume_change
        return

    def reset_event(self):
        self.cclive_player.video_ready_callback = self.video_ready_callback
        self.cclive_player.video_complete_callback = self.video_complete_callback

    def video_ready_callback(self, *args):
        self.is_mv_ready = True
        self.bind_mv_model_tex()
        self.is_need_seek_to = True
        self.seek_to_downcount = 20

    def video_complete_callback(self, *args):
        self.is_end = True
        self.cclive_player.stop()
        self.reset_pic()

    def bind_mv_model_tex(self):
        if not self.is_bind_mv_model and self.is_mv_ready and self.mv_model and self.mv_model.valid:
            provider = self.cclive_player.fetch_data_provider()
            if provider:
                self.render_tex = render.texture('cclive', data_provider=provider)
                self.mv_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', self.render_tex)
                self.is_bind_mv_model = True

    def on_update_battle_stage(self, *args):
        if self.concert_start_ts != global_data.battle.get_concert_start_ts():
            self.concert_start_ts = global_data.battle.get_concert_start_ts()
            self.all_time = time_utility.get_server_time() - self.concert_start_ts
            self.is_wait = True if self.all_time < self.video_start else False
            self.reset_music()
            self.reset_pic()

    def on_sound_volume_change(self, volume):
        self.save_cc_sound_volume = volume
        if not self.is_check_progress:
            self.cclive_player.set_volume(volume * s_cc_sound_volume_scale)

    def on_enter(self):
        global_data.sound_mgr.reset_volume()
        self.reset_event()
        scn = self.scene()

        def create_cb(model):
            self.mv_model = model
            if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
                model.all_materials.set_technique(1, 'shader/g93shader/effect_g93_cclive.nfx::TShader')
            model.world_rotation_matrix = math3d.matrix.make_rotation_y(s_tv_info[0][1] / 180 * 3.14)
            self.bind_mv_model_tex()
            self.mv_model.visible = not (self.is_wait or self.is_end)

        global_data.model_mgr.create_model_in_scene(s_mv_model, math3d.vector(*s_tv_info[0][0]), on_create_func=create_cb)

        def create_cb_mv_wait(model):
            self.mv_wait_model = model
            model.world_rotation_matrix = math3d.matrix.make_rotation_y(s_tv_info[0][1] / 180 * 3.14)
            tex = render.texture(s_mv_wait_pic)
            model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex)
            self.mv_wait_model.visible = self.is_wait or self.is_end

        global_data.model_mgr.create_model_in_scene(s_mv_model, math3d.vector(*s_tv_info[0][0]), on_create_func=create_cb_mv_wait)
        self.reset_music()
        self.reset_pic()

    def get_video_time(self):
        if self.is_wait or self.is_end:
            return None
        else:
            if self.cclive_player:
                return self.cclive_player.current_position / self.seek_scale
            return None

    def reset_pic(self):
        if self.mv_model:
            self.mv_model.visible = not (self.is_wait or self.is_end)
        if self.mv_wait_model:
            self.mv_wait_model.visible = self.is_wait or self.is_end

    def on_update(self, dt):
        cur_time = global_data.game_time
        cur_dt = cur_time - self.last_time
        self.last_time = cur_time
        self.all_time += cur_dt
        if self.is_wait and self.all_time > self.video_start and self.is_end == False:
            self.is_wait = False
            self.reset_music()
            self.reset_pic()
        if not self.is_wait and not self.is_end:
            self.check_progress_downcount -= cur_dt
            if self.check_progress_downcount <= 0:
                if self.is_check_progress:
                    self.check_progress_downcount = 1.0
                else:
                    self.check_progress_downcount = 5.0
                part_time = self.all_time - self.video_start
                if part_time > s_video_last_time + 2.0:
                    if self.cclive_player:
                        self.cclive_player.stop()
                    self.is_end = True
                    self.reset_pic()
                    return
                interval_time = self.cclive_player.current_position / self.seek_scale - part_time
                if abs(interval_time) < 5.0 and self.max_check_progress_count > 10:
                    if self.is_check_progress:
                        self.is_check_progress = False
                        self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)
                    return
                self.max_check_progress_count += 1
                if interval_time < -2.0 or interval_time > 5.0:
                    self.cclive_seek_to(part_time)
                elif interval_time > 2.0:
                    if self.cclive_player:
                        self.cclive_player.pause()

                        def callback():
                            if self.cclive_player:
                                self.cclive_player.resume()
                                if self.is_check_progress:
                                    self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)

                        global_data.game_mgr.register_logic_timer(callback, interval=interval_time, times=1, mode=timer.CLOCK)
                        self.check_progress_downcount = interval_time + 1.0
                elif self.is_check_progress:
                    self.is_check_progress = False
                    self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)

    def reset_music(self):
        self.cclive_player.stop()
        if not self.is_wait:
            if self.all_time - self.video_start > s_video_last_time:
                self.is_end = True
                return
            self.cclive_player.play_vod(s_video_url)
            if not self.is_wait:
                self.cclive_seek_to(self.all_time - self.video_start)

    def cclive_seek_to(self, time):
        if self.cclive_player:
            self.cclive_player.seek_to(int(time * self.seek_scale))

    def on_exit(self):
        global_data.emgr.update_battle_stage -= self.on_update_battle_stage
        global_data.emgr.cc_sound_volume_change -= self.on_sound_volume_change
        if self.cclive_player:
            self.cclive_player.stop()