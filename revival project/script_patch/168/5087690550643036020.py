# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartAmbSound.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import common.utils.timer as timer
from logic.gcommon.common_const.battle_const import BATTLE_SCENE_KONGDAO

class PartAmbSound(ScenePart.ScenePart):
    INIT_EVENT = {'scene_camera_target_setted_event': 'on_cam_target_setted',
       'camera_transformation_change': 'on_camera_change',
       'battle_music_enable': 'on_battle_music_enable'
       }

    def __init__(self, scene, name):
        super(PartAmbSound, self).__init__(scene, name)
        self.sound_mgr = global_data.sound_mgr
        self._sound_id = self.sound_mgr.register_game_obj('amb')
        self._sound_player_id = None
        self._cam_target = None
        self._is_diving = False
        self._camera_pos = math3d.vector(0, 100, 0)
        self._is_camera_underwater = False
        self._reset_timer = None
        return

    def on_cam_target_setted(self):
        target = global_data.cam_lctarget
        if self._cam_target:
            target.unregist_event('E_MECHA_ENTER_DIVING', self.on_enter_diving)
            target.unregist_event('E_MECHA_LEAVE_DIVING', self.on_leave_diving)
        self._cam_target = target
        target.regist_event('E_MECHA_ENTER_DIVING', self.on_enter_diving)
        target.regist_event('E_MECHA_LEAVE_DIVING', self.on_leave_diving)
        self._is_diving = target.ev_g_is_diving()
        self.check_underwater()

    def on_enter_diving(self, *args):
        self._is_diving = True
        self.check_underwater()

    def on_leave_diving(self, *args):
        self._is_diving = False
        self.check_underwater()

    def on_camera_change(self, camera_pos):
        self._camera_pos = camera_pos
        self.check_underwater()

    def check_underwater(self):
        if self._is_diving:
            if self._cam_target.ev_g_water_height() is not None and self._camera_pos.y < self._cam_target.ev_g_water_height():
                if not self._is_camera_underwater:
                    global_data.sound_mgr.set_underwater_percent(80)
                    self.sound_mgr.set_switch('in_outdoor', 'underwater', self._sound_id)
                    self._is_camera_underwater = True
                    self.reset_sound()
            elif self._is_camera_underwater:
                global_data.sound_mgr.set_underwater_percent(0)
                self.sound_mgr.set_switch('in_outdoor', 'outdoor', self._sound_id)
                self._is_camera_underwater = False
                self.stop_reset_timer()
        elif self._is_camera_underwater:
            global_data.sound_mgr.set_underwater_percent(0)
            self.sound_mgr.set_switch('in_outdoor', 'outdoor', self._sound_id)
            self._is_camera_underwater = False
            self.stop_reset_timer()
        return

    def on_enter(self):
        scene_name = global_data.battle.get_scene_name()
        if scene_name == BATTLE_SCENE_KONGDAO:
            return
        if global_data.game_mode.is_pve():
            return
        self.sound_mgr.set_switch('in_outdoor', 'outdoor', self._sound_id)
        self._sound_player_id = self.sound_mgr.post_event('Play_amb_wind', self._sound_id)

    def on_exit(self):
        if self._sound_player_id:
            self.sound_mgr.stop_playing_id(self._sound_player_id)
            self._sound_player_id = None
        if self._sound_id:
            self.sound_mgr.unregister_game_obj(self._sound_id)
            self._sound_id = None
        if self._cam_target:
            self._cam_target.unregist_event('E_MECHA_ENTER_DIVING', self.on_enter_diving)
            self._cam_target.unregist_event('E_MECHA_LEAVE_DIVING', self.on_leave_diving)
            self._cam_target = False
        self._is_camera_underwater = False
        global_data.sound_mgr.set_underwater_percent(0)
        self.stop_reset_timer()
        return

    def on_battle_music_enable(self, enable):
        if not self._sound_id:
            return
        else:
            if enable and self._sound_player_id:
                if self._sound_player_id:
                    self.sound_mgr.stop_playing_id(self._sound_player_id)
                    self._sound_player_id = None
            elif not enable and self._sound_player_id is None:
                self.sound_mgr.set_switch('in_outdoor', 'outdoor', self._sound_id)
                self._sound_player_id = self.sound_mgr.post_event('Play_amb_wind', self._sound_id)
            return

    def reset_sound(self):
        if not self._reset_timer:
            self._reset_timer = global_data.game_mgr.register_logic_timer(self.reset_timer, interval=7, times=-1, mode=timer.CLOCK)

    def reset_timer(self):
        self.sound_mgr.set_switch('in_outdoor', 'underwater', self._sound_id)
        self.sound_mgr.set_switch('in_outdoor', 'outdoor', self._sound_id)
        self.sound_mgr.set_switch('in_outdoor', 'underwater', self._sound_id)

    def stop_reset_timer(self):
        if self._reset_timer:
            global_data.game_mgr.unregister_logic_timer(self._reset_timer)
            self._reset_timer = None
        return