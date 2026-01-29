# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartRayTestEyeAdapt.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import game
import common.const.common_const as const
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_COLL
import collision
import math3d

def vdc(n, base=2):
    vdc, denom = (0, 1)
    while n:
        denom *= base
        n, remainder = divmod(n, base)
        vdc += remainder / denom

    return vdc


def hammersley(n, base=2):
    result = []
    for i in range(n):
        x = i / n
        result.append((x, vdc(i, base)))

    return result


RAY_COUNT = 60
RAY_DIST = 1500.0
MASK_VISIBLE = 32768

def screen_pos_to_world_pos(scene, x, y):
    start_pt, dir = scene.active_camera.screen_to_world(x, y)
    end_pt = start_pt + dir * RAY_DIST
    result = scene.scene_col.hit_by_ray(start_pt, end_pt, 0, GROUP_CAMERA_COLL, MASK_VISIBLE, collision.INCLUDE_FILTER)
    if result is None or not result[0]:
        return
    else:
        pos = math3d.vector(result[1].x, result[1].y, result[1].z)
        return pos
        return


def world_pos_to_sun(scene, pos):
    direction = -scene.realtime_shadow_light.direction
    result = scene.scene_col.hit_by_ray(pos, pos + direction * RAY_DIST, 0, GROUP_CAMERA_COLL, MASK_VISIBLE, collision.INCLUDE_FILTER)
    if result is None or not result[0]:
        return 1
    else:
        return 0
        return


def remap(val, min_val, max_val, new_min_val, new_max_val):
    return new_min_val + max(0, val - min_val) / (max_val - min_val) * (new_max_val - new_min_val)


class PartRayTestEyeAdapt(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartRayTestEyeAdapt, self).__init__(scene, name, True)
        self._hammersley_sequence = hammersley(RAY_COUNT)
        self._query_index = 0
        self._results = [1] * RAY_COUNT
        self._avg_result = 1
        self._debug_models = []
        self._debug_view = False
        self._enable = global_data.enable_ray_test_eye_adapt
        self._timer_handler = None
        self._key_registed = False
        return

    def on_enter(self):
        import common.utils.timer as t
        self._query_index = 0
        if self._enable:
            self.register_keys()
            self._timer_handler = global_data.game_mgr.get_fix_logic_timer().register(func=self._update_tick, interval=1 / 60, mode=t.CLOCK, strict=True)
            self.scene().set_light_config_finetune(0.6, 1.0, False)

    def _update_tick(self):
        if self._enable:
            i = self._query_index
            self._query_index = i + 1
            if self._query_index == RAY_COUNT:
                self._query_index = 0
            cur_start_point = self._hammersley_sequence[i]
            self._results[i] = self._test_camera_ray(cur_start_point[0], cur_start_point[1])
            self._avg_result = sum(self._results) / RAY_COUNT

    def on_exit(self):
        self.unregister_keys()
        if self._timer_handler:
            global_data.game_mgr.get_fix_logic_timer().unregister(self._timer_handler)

    def register_keys(self):
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_L, game.VK_K), self._key_handler)
        self._key_registed = True

    def unregister_keys(self):
        if self._key_registed:
            game.remove_key_handler(game.MSG_KEY_DOWN, (
             game.VK_L, game.VK_K), self._key_handler)

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def _key_handler(self, msg, keycode):
        if keycode == game.VK_L:
            self._toggle_debug_view()
        if keycode == game.VK_K:
            self._toggle_enable()

    def _toggle_enable(self):
        if not __debug__:
            return
        self._enable = not self._enable
        if self._enable:
            self.scene().set_light_config_finetune(0.6, 1.0, False)
        else:
            self.scene().set_light_config_finetune(1.0, 1.0, True)
        self.scene().set_adapt_factor(1.0)

    def _toggle_debug_view(self):
        if not __debug__:
            return
        else:
            import world
            self._debug_view = not self._debug_view
            if self._debug_view and not self._debug_models:
                cam = self.scene().active_camera
                w, h = const.WINDOW_WIDTH, const.WINDOW_HEIGHT
                for i in range(RAY_COUNT):
                    mod = world.model('model_new/test/bone_sphere.gim', None)
                    mod.set_parent(cam)
                    x, y = self._hammersley_sequence[i]
                    p0, dir = cam.screen_to_world(x * w, y * h)
                    dir.normalize()
                    cam_pos = cam.world_to_camera(p0 + dir * 35)
                    mod.position = cam_pos
                    self._debug_models.append(mod)

            for m in self._debug_models:
                m.visible = self._debug_view

            return

    def on_update(self, dt):
        if self._enable:
            if self._debug_view:
                import game3d
                _HASH_CHANGE_COLOR = game3d.calc_string_hash('u_change_color')
                color_success = (0.0, 1.0, 0.0, 1.0)
                color_failed = (1.0, 0.0, 0.0, 1.0)
                for i in range(RAY_COUNT):
                    mod = self._debug_models[i]
                    mod.all_materials.set_var(_HASH_CHANGE_COLOR, 'u_change_color', color_success if self._results[i] == 1 else color_failed)

            avg_min, avg_max = (0.0, 1.0)
            adapt_min, adapt_max = (1.5, 1.0)
            value = remap(self._avg_result, avg_min, avg_max, adapt_min, adapt_max)
            self.scene().set_adapt_factor(value)
            if self._debug_view:
                print('avg {}, adaptive {}'.format(self._avg_result, value))

    def _test_camera_ray(self, x, y):
        scene = self.scene()
        if not scene:
            return
        else:
            rt_x = x * const.WINDOW_WIDTH
            rt_y = y * const.WINDOW_HEIGHT
            pos = screen_pos_to_world_pos(scene, rt_x, rt_y)
            if pos is not None:
                return world_pos_to_sun(scene, pos)
            return 1
            return