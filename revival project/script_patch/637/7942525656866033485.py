# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PoisonDamageViewMgr.py
from __future__ import absolute_import
import math3d
import world
import render
import game3d
import common.utils.timer as timer
import logic.gcommon.const as const
from logic.gutils.screen_effect_utils import SCREEN_EFFECT_SCALE
SHAKE_POINT = [
 (0.0, 0.0), (0.15, 0.56), (0.5, 0.9146), (0.6, 0.3411), (0.68, 0.7442), (0.74, 0.15), (0.84, 1.0), (1.5, 0.0)]
SHAKE_MAX_COUNT = 8
CIRCLE_SCALE = 1.0
_HASH_time = game3d.calc_string_hash('time')
_HASH_distortionScale = game3d.calc_string_hash('distortionScale')
_HASH_texture_distort = game3d.calc_string_hash('texture_distort')
_HASH_texture_light = game3d.calc_string_hash('texture_light')

class PoisonDamageViewMgr(object):

    def __init__(self, poison_mgr):
        self._is_inside = None
        self._poison_mgr = poison_mgr
        self._screen_sfx = None
        self._load_screen_sfx_task = None
        self._shake_timer = None
        self._poison_check_timer = None
        self._shake_time = 0
        self._shake_index = 0
        self._scene = world.get_active_scene()
        self.register_event()
        self.enable = True
        global_data.display_agent.set_longtime_post_process_active('screen_shake', False)
        self.poison_circle_stopped = False
        return

    def register_event(self):
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.set_up_posteffect += self.reset_posteffect
        global_data.emgr.scene_stop_poison_circle += self.stop_poison_circle
        global_data.emgr.scene_recover_poison_circle += self.recover_poison_circle
        global_data.emgr.scene_camera_player_setted_event += self.on_scene_cam_player_setted

    def start_check(self):
        if not self._poison_check_timer:
            self._poison_check_timer = global_data.game_mgr.register_logic_timer(self.check_outside, interval=0.5, times=-1, mode=timer.CLOCK)

    def check_outside(self):
        if global_data.is_in_judge_camera:
            if self._is_inside or self._is_inside is None:
                self._is_inside = False
                self.stop_scene_shake()
                return
        if not global_data.cam_lplayer or not global_data.cam_lplayer.is_valid():
            return
        else:
            pos = global_data.cam_lplayer.ev_g_position()
            if pos is None:
                return
            is_inside = self._poison_mgr.is_in_poison()
            if self._is_inside is None or is_inside != self._is_inside:
                self._is_inside = is_inside
                if self._is_inside:
                    self.stop_scene_shake()
                    global_data.cam_lplayer.send_event('E_GUIDE_POISON', False)
                    global_data.cam_lplayer.send_event('E_IN_POISON', False)
                else:
                    self.play_scene_shake()
                    global_data.cam_lplayer.send_event('E_GUIDE_POISON', True)
                    global_data.cam_lplayer.send_event('E_IN_POISON', True)
            return

    def play_scene_shake(self):
        if global_data.game_mode.is_snow_res():
            return
        if self.poison_circle_stopped:
            return
        if self._screen_sfx:
            self._screen_sfx.visible = True
            self._screen_sfx.restart()
        else:
            self.load_scene_sfx()

    def stop_scene_shake(self):
        if self._screen_sfx:
            self._screen_sfx.visible = False
            self._screen_sfx.shutdown()

    def reset_posteffect(self):
        if self._shake_timer:
            self.stop_scene_shake()
            self.play_scene_shake()

    def update_time_callback(self):
        self._shake_time += 0.015
        if self._shake_time > SHAKE_POINT[self._shake_index][0]:
            self._shake_index += 1
            if self._shake_index >= SHAKE_MAX_COUNT:
                self._shake_time -= SHAKE_POINT[SHAKE_MAX_COUNT - 1][0]
                self._shake_index = 1
        rate = (self._shake_time - SHAKE_POINT[self._shake_index - 1][0]) / (SHAKE_POINT[self._shake_index][0] - SHAKE_POINT[self._shake_index - 1][0])
        scale = SHAKE_POINT[self._shake_index - 1][1] + (SHAKE_POINT[self._shake_index][1] - SHAKE_POINT[self._shake_index - 1][1]) * rate
        mat = global_data.display_agent.get_post_effect_pass_mtl('screen_shake', 0)
        mat.set_var(_HASH_time, 'time', scale)
        mat.set_var(_HASH_distortionScale, 'distortionScale', 0.02)

    def load_scene_sfx(self):
        if not self._screen_sfx and not self._load_screen_sfx_task:
            self._load_screen_sfx_task = world.create_sfx_async('effect/fx/duquan/duquanfankui.sfx', self.load_scene_sfx_callback)

    def load_scene_sfx_callback(self, sfx, user_data, current_task):
        if not self._scene.valid:
            sfx.destroy()
            return
        else:
            if not self.enable:
                sfx.destroy()
                return
            self._load_screen_sfx_task = None
            self._screen_sfx = sfx
            self._screen_sfx.scale = SCREEN_EFFECT_SCALE
            self._screen_sfx.visible = not self._is_inside
            self._scene.add_object(sfx)
            return

    def on_login_reconnect(self, *args):
        if self._shake_timer:
            global_data.game_mgr.unregister_logic_timer(self._shake_timer)
            self._shake_timer = global_data.game_mgr.register_logic_timer(self.update_time_callback, interval=1, times=-1, mode=timer.LOGIC)
        if self._poison_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._poison_check_timer)
            self._poison_check_timer = global_data.game_mgr.register_logic_timer(self.check_outside, interval=0.5, times=-1, mode=timer.CLOCK)

    def destroy_scene_sfx(self):
        if self._screen_sfx and self._screen_sfx.valid:
            self._screen_sfx.destroy()
            self._screen_sfx = None
        if self._load_screen_sfx_task:
            self._load_screen_sfx_task.cancel()
            self._load_screen_sfx_task = None
        return

    def destroy(self):
        self.stop_scene_shake()
        self.destroy_scene_sfx()
        if self._poison_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._poison_check_timer)
            self._poison_check_timer = None
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect
        global_data.emgr.set_up_posteffect -= self.reset_posteffect
        global_data.emgr.scene_stop_poison_circle -= self.stop_poison_circle
        global_data.emgr.scene_recover_poison_circle -= self.recover_poison_circle
        global_data.emgr.scene_camera_player_setted_event -= self.on_scene_cam_player_setted
        self.enable = False
        self._poison_mgr = None
        return

    def stop_poison_circle(self):
        self.poison_circle_stopped = True
        self.stop_scene_shake()
        self.destroy_scene_sfx()

    def recover_poison_circle(self):
        self.poison_circle_stopped = False
        self._is_inside = True

    def on_scene_cam_player_setted(self):
        self._is_inside = None
        return