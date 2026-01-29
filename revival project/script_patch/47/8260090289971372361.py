# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaAutoAimWidget8030.py
from __future__ import absolute_import
from .MechaAutoAimWidget import MechaAutoAimWidget, empty_func, default_play_lock_sound_func
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.common_const.weapon_const import AUTO_AIM_KIND_UNIQUE
from math import atan, tan, radians, pi
import world
import cc
from logic.gcommon.component.client.ComMechaAimHelper import AIM_TARGET_VALID, AIM_TARGET_INVALID

class MechaAutoAimWidget8030(MechaAutoAimWidget):

    def __init__(self, panel, auto_aim_fov_map=None, show_anim_name='sample_visable_auto', hide_anim_name='', target_refreshed_anim_map=None, miss_target_anim=None, lock_count_refreshed_anim_map=None, play_lock_sound_func=default_play_lock_sound_func, need_play_lock_sound_map=None, lock_node_map=None, reset_node_map=None, lock_node_parent_map=None, update_callback=empty_func):
        super(MechaAutoAimWidget8030, self).__init__(panel, auto_aim_fov_map, show_anim_name, hide_anim_name, target_refreshed_anim_map, miss_target_anim, lock_count_refreshed_anim_map, play_lock_sound_func, need_play_lock_sound_map, lock_node_map, reset_node_map, lock_node_parent_map, update_callback)
        self.panel_showed = False
        self.target_valid = AIM_TARGET_INVALID

    def show(self):
        self.panel_showed = True
        super(MechaAutoAimWidget8030, self).show()

    def hide(self):
        self.panel_showed = False
        super(MechaAutoAimWidget8030, self).hide()

    def refresh_auto_aim_range_appearance(self, weapon_pos):
        if not self.auto_aim_node:
            return False
        weapon = self.lmecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        conf = weapon.conf
        auto_aim_yaw = conf('fAutoAimYaw', 0.0)
        auto_aim_pitch = conf('fAutoAimPitch', 0.0)
        if not (auto_aim_yaw and auto_aim_pitch):
            return False
        width, height = self.panel.GetContentSize()
        x_fov = self.auto_aim_fov_map.get(weapon_pos, self.default_fov)
        d = width / 2.0 / tan(radians(x_fov / 2.0))
        cell = 30
        y_fov = atan(cell / 2.0 / d) * 180 / pi * 2.0
        scale_value = cell / y_fov * 2.0
        center = self.auto_aim_node.frame.center
        center.SetContentSize(auto_aim_yaw * scale_value, auto_aim_pitch * scale_value)
        center.RecursionReConfPosition()
        return True

    def update_aim_target(self, target, weapon_pos, **kwargs):
        if weapon_pos != self.cur_weapon_pos:
            return
        else:
            invalid_target = kwargs.get('invalid_target')
            invalid_type = AIM_TARGET_INVALID
            if target is None and invalid_target is not None:
                invalid_target, invalid_type = invalid_target
                target = invalid_target
            target_valid = AIM_TARGET_VALID if target is not invalid_target else invalid_type
            if target != self.aim_target_compared or self.target_valid != target_valid:
                self.target_valid = target_valid
                self.aim_target_compared = target
                self.aim_target_validating = target
                if self.auto_aim_kind == AUTO_AIM_KIND_UNIQUE:
                    if self._validate_aim_target_uniquely():
                        self._register_check_timer_uniquely()
                elif self._validate_aim_target_multiply():
                    self._register_check_timer_multiply()
            return

    def _update_aim_node_position_uniquely(self):
        if self.aim_target and self.aim_target.is_valid():
            scn = global_data.game_mgr.scene
            if not scn:
                return
            camera = scn.active_camera
            if not camera:
                return
            model = self.aim_target.ev_g_model()
            if not model:
                return
            matrix = model.get_bone_matrix(BONE_BIPED_NAME, world.SPACE_TYPE_WORLD)
            if matrix:
                aim_pos = matrix.translation
            else:
                matrix = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
                if matrix:
                    aim_pos = matrix.translation
                else:
                    aim_pos = model.ev_g_position()
            x, y = camera.world_to_screen(aim_pos)
            pos = cc.Vec2(*neox_pos_to_cocos(x, y))
            pos = self.cur_lock_node_parent.convertToNodeSpace(pos)
            for lock_node in self.cur_lock_node:
                lock_node.setPosition(pos)

            self.update_callback(aim_pos, self.target_valid)