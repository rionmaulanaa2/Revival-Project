# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMeadow.py
from __future__ import absolute_import
import six
import math3d
from . import ScenePart
import math
import random
import version
from logic.vscene.meadow_quality_level import NONE_LEVEL, LOW_LEVEL, MID_LEVEL, HIGH_LEVEL
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from logic.client.const.game_mode_const import GAME_MODE_NIGHT_SURVIVAL
MeadowDistConfig = {LOW_LEVEL: (100, 400, 0),
   MID_LEVEL: (120, 430, 1200),
   HIGH_LEVEL: (120, 480, 1800)
   }
MeadowDensityConfig = {LOW_LEVEL: (4, 4, 0),
   MID_LEVEL: (5, 4, 2),
   HIGH_LEVEL: (5, 5, 5)
   }

class PartMeadow(ScenePart.ScenePart):
    ENTER_EVENT = {'set_meadow_quality': 'on_set_meadow_quality'
       }

    def __init__(self, scene, name):
        super(PartMeadow, self).__init__(scene, name)
        self.wind_param_decide = False
        self.blowing = False
        self.target_wind_dir = 0
        self.wind_start_delay = 0
        self.wind_dir = 0
        self.wind_life_time = 0
        self.wind_elapsed_time = 0
        self.wind_speed = 0
        self.wind_wave = 0
        self.wind_distro = 0

    def on_enter(self):
        if not global_data.feature_mgr.is_support_meadow():
            return
        if not global_data.enable_meadow:
            return
        if global_data.game_mode.is_snow_res():
            return
        fake_val = 0 if CGameModeManager().get_mode_type() == GAME_MODE_NIGHT_SURVIVAL else 0.32
        self.scene().set_meadow_global_param('u_fake_sky_light', (fake_val, fake_val, fake_val, 1.0))
        quality = global_data.game_mgr.gds.get_meadow_quality()
        if quality > NONE_LEVEL:
            self.on_set_meadow_quality(quality)
            self.scene().enable_meadow(True)
            self.need_update = True

    def on_update(self, dt):
        self.update_meadow_param(dt)

    def on_exit(self):
        pass

    def on_set_meadow_quality(self, quality):
        if not global_data.feature_mgr.is_support_meadow():
            return
        if not global_data.enable_meadow:
            return
        if global_data.game_mode.is_snow_res():
            return
        scene = self.scene()
        if not scene:
            return
        if quality == NONE_LEVEL:
            self.need_update = False
            scene.enable_meadow(False)
        else:
            self.need_update = True
            scene.enable_meadow(True)
            scene.set_meadow_lod_density(0, MeadowDensityConfig[quality][0])
            scene.set_meadow_lod_density(1, MeadowDensityConfig[quality][1])
            scene.set_meadow_lod_density(2, MeadowDensityConfig[quality][2])
            scene.set_meadow_lod_dist(0, MeadowDistConfig[quality][0])
            scene.set_meadow_lod_dist(1, MeadowDistConfig[quality][1])
            scene.set_meadow_lod_dist(2, MeadowDistConfig[quality][2])
            scene.reload_meadow()

    def update_meadow_param(self, dt):
        scene = self.scene()
        if not scene:
            return
        if not scene.is_meadow_loaded():
            return
        cam_lplayer = global_data.cam_lplayer
        pos = math3d.vector(0, 0, 0)
        inter_val = 20.0
        if cam_lplayer:
            if cam_lplayer.ev_g_in_mecha():
                inter_val = 60.0 if 1 else 20.0
                pos = cam_lplayer.ev_g_position() or math3d.vector(0, 0, 0)
            self.target_wind_dir = self.wind_param_decide or random.uniform(0, 2) * math.pi * 0.25
            self.wind_life_time = random.randint(40, 50)
            self.wind_elapsed_time = 0
            self.wind_start_delay = random.randint(4, 6)

            def start_wind():
                self.blowing = True
                global_data.emgr.scene_wind_info_update.emit(True, self.wind_dir)

            global_data.game_mgr.delay_exec(self.wind_start_delay, start_wind)
            self.wind_param_decide = True
        if self.blowing:
            self.wind_elapsed_time += dt
            self.get_wind_param(dt)
        elif self.wind_param_decide:
            self.wind_dir += dt / self.wind_start_delay * self.target_wind_dir
        scene.set_meadow_param(-1, (pos.x, pos.y, pos.z, inter_val,
         self.wind_speed, self.wind_wave, self.wind_distro,
         math.cos(self.wind_dir), math.sin(self.wind_dir), 0.0))

    def get_wind_param(self, dt):
        wind_speed = self.wind_speed
        wind_wave = self.wind_wave
        wind_distro = self.wind_distro
        wind_min = 0.2
        wind_max = 0.6
        wind_distro_max = 1.0
        wind_wave_max = 0.5
        if self.wind_elapsed_time < self.wind_life_time - 2.0:
            wind_speed = self.wind_elapsed_time if self.wind_elapsed_time < wind_max else wind_max
            wind_speed = wind_min if wind_speed < wind_min else wind_speed
            wind_distro = self.wind_elapsed_time - 1.0
            wind_distro = 0 if wind_distro < 0 else (wind_distro if wind_distro < wind_distro_max else wind_distro_max)
            wind_wave = self.wind_elapsed_time - 2.0
            wind_wave = 0 if wind_wave < 0 else (wind_wave if wind_wave < wind_wave_max else wind_wave_max)
        elif self.wind_elapsed_time < self.wind_life_time:
            wind_speed -= dt / 2.0
            wind_speed = wind_min if wind_speed < wind_min else wind_speed
            wind_distro -= dt * wind_distro_max / 2.0
            wind_distro = 0 if wind_distro < 0 else wind_distro
            wind_wave -= dt * wind_wave_max / 2.0
            wind_wave = 0 if wind_wave < 0 else wind_wave
        else:
            self.wind_param_decide = False
            self.blowing = False
            wind_speed = wind_min
            wind_wave = 0
            wind_distro = 0
            global_data.emgr.scene_wind_info_update.emit(False)
        self.wind_speed = wind_speed
        self.wind_wave = wind_wave
        self.wind_distro = wind_distro