# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRobotBehavior.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
import math3d
from ...cdata import status_config as st_const
from logic.gcommon.const import NEOX_UNIT_SCALE
import common.utils.timer as timer
import time
import random
import game3d
import logic.gcommon.common_const.water_const as water_const
from logic.gcommon import time_utility as t_util
CHECK_CLIMB_MIN_DISTANCE_SQR = (2.5 * NEOX_UNIT_SCALE) ** 2
CHECK_LAST_CLIMB_POS_DISTANCE_SQE = (0.5 * NEOX_UNIT_SCALE) ** 2
CHECK_INTERVAL = 1.0
_HASH_MaskTex = game3d.calc_string_hash('MaskTex')
_HASH_Tex0 = game3d.calc_string_hash('Tex0')
_HASH_DyeColor = game3d.calc_string_hash('DyeColor')
_HASH_DyePart = game3d.calc_string_hash('DyePart')
_HASH_CHANGE_COLOR = game3d.calc_string_hash('u_change_color')
_HASH_xray_color = game3d.calc_string_hash('xray_color')
FROZEN_JUMP_CNT = 30
DOT_VALUE_TO_JUMP = 0.6

class ComRobotBehavior(UnitCom):
    BIND_EVENT = {'E_ON_MOVE_TO': '_on_move_to',
       'E_ON_TOUCH_GROUND': '_on_ground',
       'E_END_ROLL': '_on_roll_end',
       'E_ON_GROUND_FINISH': ('_on_ground_finish', 999)
       }

    def __init__(self):
        super(ComRobotBehavior, self).__init__(need_update=True)
        self._save_pos = None
        self._diff_pre = None
        self._last_climb_pos = math3d.vector(0, 0, 0)
        self._check_timer = None
        self._frozen_cnt = 0
        self.mp_last_jump_time = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRobotBehavior, self).init_from_dict(unit_obj, bdict)
        self._name = bdict.get('char_name', '')

    def set_color(self):
        import render
        model = self.ev_g_model()
        if not model:
            return
        model.all_materials.set_macro('DYE_ENABLE', 'TRUE')
        model.all_materials.rebuild_tech()
        tex_path = 'character/dye_mask.tga'
        texture = render.texture(tex_path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
        model.all_materials.set_texture(_HASH_MaskTex, 'MaskTex', texture)
        if self._name.find('DM') == -1:
            model.all_materials.set_var(_HASH_DyeColor, 'DyeColor', (0.0, 0.0, 1.0,
                                                                     1.0))
        else:
            model.all_materials.set_var(_HASH_DyeColor, 'DyeColor', (1.0, 0.0, 1.0,
                                                                     1.0))
        model.all_materials.set_var(_HASH_DyePart, 'DyePart', (1.0, 0.0, 0.0, 1.0))

    def destroy(self):
        if self._check_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_timer)
            self._check_timer = None
        super(ComRobotBehavior, self).destroy()
        return

    def tick(self, dt):
        self.check_climb_tick()

    def check_climb_tick(self):
        if self.ev_g_agony():
            return
        else:
            if self.sd.ref_water_status > water_const.WATER_MID_LEVEL:
                return
            if self.ev_g_is_in_any_state((st_const.ST_MOVE, st_const.ST_RUN)):
                cur_pos = self.ev_g_position()
                if self._save_pos and cur_pos:
                    diff = cur_pos - self._save_pos
                    if self._check_dir_to_jump(diff):
                        self.trigger_jump(reason='dir_dot')
                        self._save_pos = cur_pos
                        return
                    length_sqr = diff.length_sqr
                    if self._frozen_cnt >= FROZEN_JUMP_CNT:
                        self.trigger_jump(reason='frozen')
                    if length_sqr < CHECK_CLIMB_MIN_DISTANCE_SQR and (self._last_climb_pos - cur_pos).length_sqr > CHECK_LAST_CLIMB_POS_DISTANCE_SQE:
                        flag = self.check_climb()
                        if flag[0]:
                            self.send_event('E_CLIMB', flag[1], flag[2], flag[3])
                        elif flag[1] < -100:
                            pass
                        self._last_climb_pos = cur_pos
                self._save_pos = cur_pos
            else:
                self._save_pos = None
                self._frozen_cnt = 0
            return

    def _check_dir_to_jump(self, diff):
        pos_dir = math3d.vector(diff.x, 0, diff.z)
        if pos_dir.is_zero:
            self._frozen_cnt += 1
            return False
        if not self._diff_pre:
            self._diff_pre = pos_dir
            return False
        new_pos_dir = self._diff_pre + pos_dir
        self._diff_pre = pos_dir
        pos_dir = new_pos_dir
        if pos_dir.is_zero:
            self._frozen_cnt += 1
            return False
        pos_dir.normalize()
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return False
        cha_dir = char_ctrl.getWalkDirection()
        if cha_dir.is_zero:
            return False
        cha_dir.normalize()
        if cha_dir.dot(pos_dir) < DOT_VALUE_TO_JUMP:
            return True
        return False

    def _clear_jump_check(self):
        self._diff_pre = None
        self._frozen_cnt = 0
        self._save_pos = None
        return

    def _on_move_to(self, pos):
        self._clear_jump_check()

    def _on_ground(self, *args):
        self._clear_jump_check()

    def _on_roll_end(self, *args):
        self._clear_jump_check()

    def trigger_jump(self, reason):
        if t_util.time() - self.mp_last_jump_time.get(reason, 0) < 1.5:
            return
        self._clear_jump_check()
        self.mp_last_jump_time[reason] = t_util.time()
        self.send_event('E_CTRL_JUMP')

    def check_climb(self):
        import logic.gcommon.const as g_const
        import math3d
        from logic.gcommon.common_const import collision_const
        from logic.gcommon.common_const import animation_const
        import collision
        import math
        import world
        player_unit = global_data.player.logic
        if not self.ev_g_status_check_pass(st_const.ST_CLIMB):
            return [False, -2]
        scn = world.get_active_scene()
        player_pos = self.ev_g_foot_position()
        if not player_pos:
            return [False, -11]
        model_yaw = self.ev_g_yaw()
        forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
        chect_begin = player_pos + math3d.vector(0, g_const.CLIMB_MIN_HIGHT, 0)
        check_end = chect_begin + forward_vect * g_const.CLIMB_MAX_DISTANCE
        distance = 0
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK, collision.INCLUDE_FILTER, False)
        if result[0]:
            distance = (result[1] - chect_begin).length
            if abs(result[2].y) > 0.18:
                return [False, -4]
        else:
            return [
             False, -105]
        chect_begin += math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
        check_end += math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK, collision.INCLUDE_FILTER, False)
        if result[0]:
            return [
             False, -101]
        for i in range(2):
            if i == 0:
                offset = g_const.FIRST_FORWARD_OFFSET
            else:
                offset = g_const.SECOND_FORWARD_OFFSET
            forward_pos = player_pos + forward_vect * (distance + offset)
            chect_begin = forward_pos + math3d.vector(0.0, g_const.CLIMB_MAX_HIGHT, 0.0)
            check_end = forward_pos + math3d.vector(0.0, g_const.CLIMB_MIN_HIGHT, 0.0)
            height = 0
            result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK, collision.INCLUDE_FILTER, False)
            if result[0]:
                height = result[1].y
                if abs(result[2].y) < 0.9:
                    return [False, -6]
                climb_height = height - player_pos.y
                if climb_height < g_const.CLIMB_MIN_HIGHT or climb_height > g_const.CLIMB_MAX_HIGHT:
                    return [False, -7]
                break
        else:
            return [
             False, -8]

        forward_pos = player_pos + forward_vect * (distance + g_const.CLIMB_BOARD_MIN_WIDTH)
        chect_begin = forward_pos + math3d.vector(0.0, g_const.CLIMB_MAX_HIGHT, 0.0)
        check_end = forward_pos + math3d.vector(0.0, g_const.CLIMB_MIN_HIGHT + g_const.CLIMB_RAY_CHECK_HEIGHT, 0.0)
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK, collision.INCLUDE_FILTER, False)
        if result[0]:
            offset = height - result[1].y
            if offset < 0.01:
                climb_type = g_const.CLIMB_TO_TOP_STAND
            elif self.ev_g_is_in_any_state((st_const.ST_RUN,)):
                climb_type = g_const.CLIMB_TO_RUN
            else:
                climb_type = g_const.CLIMB_TO_DOWN_STAND
        else:
            climb_type = g_const.CLIMB_TO_DROP
        character = self.sd.ref_character
        if not character:
            return [False, -9]
        if climb_type == g_const.CLIMB_TO_TOP_STAND:
            c_width = collision_const.CHARACTER_STAND_WIDTH
            c_height = collision_const.CHARACTER_STAND_HEIGHT - c_width * 2.0
            check_distance = 1.1
        else:
            c_width = collision_const.CHARACTER_CLIMB_WIDTH
            c_height = collision_const.CHARACTER_CLIMB_HEIGHT - c_width * 2.0
            check_distance = g_const.CLIMB_BOARD_MIN_WIDTH + (collision_const.CHARACTER_STAND_WIDTH - c_width)
        check_pos_y = height + c_height * 0.5 + c_width + 0.4
        check_begin = math3d.vector(player_pos.x, check_pos_y, player_pos.z)
        check_end = check_begin + forward_vect * check_distance
        size = math3d.vector(c_width, c_height, 1)
        col = collision.col_object(collision.CAPSULE, size, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK)
        result = scn.scene_col.sweep_intersect(col, check_begin, check_end, collision_const.GROUP_CLIMB_CHECK, collision_const.GROUP_CLIMB_CHECK, collision.INCLUDE_FILTER)
        if result:
            return [False, -10]
        if climb_height < g_const.CLIMB_RAY_CHECK_HEIGHT:
            climb_type += g_const.CLIMB_SUB_TYPY_COUNT
        climb_pos = math3d.vector(player_pos.x, height, player_pos.z) + forward_vect * (distance + g_const.CLIMB_POINT_OFFSET)
        return [
         True, climb_type, climb_pos, model_yaw]

    def _on_ground_finish(self):
        info = self.ev_g_target_dir()
        if info is None:
            return
        else:
            t_pos, t_dir = info
            c_pos = self.ev_g_position()
            if t_pos and t_dir and c_pos:
                c_dir = c_pos - t_pos
                if c_dir.is_zero:
                    return
                c_dir.normalize()
                if self.same_direction(t_dir, c_dir):
                    return
                self.send_event('E_CTRL_FORCE_MOVE_STOP')
            return

    def same_direction(self, d1, d2):
        if d1.x > 0 and d2.x > 0:
            if d1.x * d2.z * (d1.z * d2.x) > 0:
                return True
        elif d1.x < 0 and d2.x < 0:
            if d1.x * d2.z * (d1.z * d2.x) > 0:
                return True
        return False