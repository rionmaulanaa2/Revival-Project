# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSunEffect.py
from __future__ import absolute_import
from six.moves import range
from . import ScenePart
import math3d
import world
import game3d
import collision
import logic.gcommon.common_const.battle_const as battle_const
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from logic.gcommon.common_const import collision_const
from common.utils.timer import CLOCK
from common.cfg import confmgr
REAL_SUN_DIST = 40000

class PartSunEffect(ScenePart.ScenePart):
    INIT_EVENT = {'update_suneffect_state': 'update_suneffect_state'
       }

    def __init__(self, scene, name):
        super(PartSunEffect, self).__init__(scene, name)
        self._timer1 = None
        self._timer3 = None
        self._ray_idx = 0
        self._ray_res = [0] * 9
        self._ray_list = [(0.0, 0.0)] * 9
        self._sun_flare = None
        self._sun = None
        self._last_total = 0
        self.total = 0
        self._offset = 0.0
        return

    def on_enter(self):
        self.clear()
        if self.scene().realtime_shadow_light is None:
            return
        else:
            sun = self.scene().get_model('sun')
            if sun:
                sun.destroy()
            sun_light = self.scene().get_model('sun_flare')
            if sun_light:
                sun_light.destroy()
            env = CGameModeManager().get_enviroment()
            if env in ('night', 'snow_night', 'ajld_night'):
                model_path = confmgr.get('script_gim_ref')['sky_moon']
                light_path = confmgr.get('script_gim_ref')['sky_moon_light']
            elif env == 'granbelm':
                model_path = confmgr.get('script_gim_ref')['sky_granbelm_moon']
                light_path = confmgr.get('script_gim_ref')['sky_moon_light']
            else:
                model_path = confmgr.get('script_gim_ref')['sky_sun']
                light_path = confmgr.get('script_gim_ref')['sky_sun_light']
            sun_offset = battle_const.ENV_SUN_OFFSET_DICT.get(env, 0)
            sun_light_offset = battle_const.ENV_SUN_LIGHT_OFFSET_DICT.get(env, 0)
            self._offset = abs(sun_light_offset) / 100

            def create_cb(model, *args):
                model.scale = math3d.vector(5000, 5000, 5000)
                self._sun = model
                self._sun.render_level = 3
                self.enable_flare(sun_offset, sun_light_offset)

            global_data.model_mgr.create_model_in_scene(model_path, on_create_func=create_cb)

            def create_cb(model, *args):
                model.scale = math3d.vector(5000, 5000, 5000)
                self._sun_flare = model
                self._sun_flare.render_level = 3
                self.enable_flare(sun_offset, sun_light_offset)

            global_data.model_mgr.create_model_in_scene(light_path, on_create_func=create_cb)
            return

    def enable_flare(self, sun_offset=0.0, light_offset=0.0):
        HASH_DIST = game3d.calc_string_hash('u_dist')
        HASH_WIDTH = game3d.calc_string_hash('u_width')
        self.HASH_FADE = game3d.calc_string_hash('u_fade')
        if self._sun_flare and self._sun:
            self._sun.scale *= 10000
            self._sun_flare.scale *= 10000
            self._timer1 = global_data.game_mgr.get_logic_timer().register(func=self.on_update, interval=0.03, mode=CLOCK)
            self._timer3 = global_data.game_mgr.get_logic_timer().register(func=self.on_calc_ray, interval=0.1, mode=CLOCK)
            self._ray_idx = 0
            sun_dist = self._sun.get_sub_material(0).get_var(HASH_DIST, 'u_dist')
            width = self._sun.get_sub_material(0).get_var(HASH_WIDTH, 'u_width')
            self._sun.get_sub_material(0).set_var('u_sun_offset', sun_offset)
            self._sun_flare.get_sub_material(0).set_var('u_sun_light_offset', light_offset)
            real_dist = REAL_SUN_DIST
            real_width = real_dist / sun_dist * width
            fix_width = real_width * 0.5 * 0.7
            sun_width = math3d.vector(0, 0, 0)
            camera = self.scene().active_camera
            camera_pos = camera.position
            far_ofs = camera.transformation.forward * sun_dist + sun_width
            range_w, range_h = camera.world_to_screen(camera_pos + far_ofs)
            size = game3d.get_window_size()
            for i in range(3):
                for j in range(3):
                    x, y = i / 2.0 - 0.5, j / 2.0 - 0.5
                    self._ray_list[j * 3 + i] = (x * fix_width, y * fix_width)

            self.init_suneffect()

    def on_calc_ray(self):
        scn = self.scene()
        cam = scn.active_camera
        direction = -scn.realtime_shadow_light.direction
        right = direction.cross(math3d.vector(0, 1, 0))
        up = direction.cross(right)
        direction = -scn.realtime_shadow_light.direction * REAL_SUN_DIST
        direction.y -= REAL_SUN_DIST * self._offset
        scn_col = scn.scene_col
        for i in range(3):
            self._ray_idx = (self._ray_idx + 1) % 9
            ray_ofs = self._ray_list[self._ray_idx]
            start = cam.position
            end = start + direction + up * ray_ofs[0] + right * ray_ofs[1]
            result = scn_col.hit_by_ray(start, end, 0, collision_const.REGION_BOUNDARY_SCENE_GROUP, 0, collision.INEQUAL_FILTER)
            hit = result[0]
            if hit:
                self._ray_res[self._ray_idx] = 0 if 1 else 1

        total = 0
        for v in self._ray_res:
            total += v

        self.total = total / 9.0

    def init_suneffect(self):
        part_privilige_lobby = self.scene().get_com('PartPrivilegeLobby')
        if part_privilige_lobby:
            is_show = part_privilige_lobby.get_suneffect_state()
            self._sun.visible = is_show
            self._sun_flare.visible = is_show

    def update_suneffect_state(self, state):
        if not self._sun or not self._sun_flare:
            return
        if not self._sun_flare.valid:
            return
        self._sun_flare.visible = state
        self._sun.visible = state

    def on_update(self):
        if not self._sun_flare.valid:
            self.clear()
            return
        self._last_total = self._last_total * 0.8 + self.total * 0.2
        self._sun_flare.all_materials.set_var(self.HASH_FADE, 'u_fade', self._last_total)

    def clear(self):
        if self._timer1 is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer1)
            self._timer1 = None
        if self._timer3 is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer3)
            self._timer3 = None
        self._sun_flare = None
        self._sun = None
        return

    def on_exit(self):
        self.clear()