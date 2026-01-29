# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/InjureProcess.py
from __future__ import absolute_import
import math
import common.utilities
import game3d
import math3d
import cc
from . import LockProcess
import time
animation_interval = 0.16

class InjureProcess(LockProcess.LockProcess):

    def __init__(self, parent, elem_type, elem_last_time, disappear_last_time, max_elem_count, panel, panel_items, item_min_angle, is_2d=True):
        super(InjureProcess, self).__init__(parent, elem_type, elem_last_time, disappear_last_time, max_elem_count, panel, panel_items, item_min_angle, is_2d)
        self._is_sound_enable = False
        self._animation_start_time = time.time()

    def fix_position(self, panel_item, is_mecha):
        if self._is_2d:
            fix_ui_pos = False
            if global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_in_aim:
                obj_weapon = global_data.cam_lctarget.share_data.ref_wp_bar_cur_weapon
                if obj_weapon:
                    weapon_id = obj_weapon.get_item_id()
                    fix_ui_pos = weapon_id in (10021, 10022, 10023)
            if fix_ui_pos:
                panel_item.injure_mecha.SetContentSize(88, 110)
                panel_item.injure_normal.SetContentSize(88, 110)
            else:
                panel_item.injure_mecha.SetContentSize(88, 150)
                panel_item.injure_normal.SetContentSize(88, 150)
            panel_item.injure_mecha.ChildRecursionRePosition()
            panel_item.injure_normal.ChildRecursionRePosition()

    def on_add_elem(self, entity, pos, damage=0, is_mecha=False):
        if not self.parent.enable_player_or_mecha:
            return
        else:
            player_pos = self.parent.enable_player_or_mecha.ev_g_model_position()
            if not player_pos:
                return
            if entity == None:
                entity = 0
            listener_look_at = self.sound_mgr.get_listener_look_at()
            direction = pos - player_pos
            angle = common.utilities.vect2d_radian(direction, listener_look_at) * LockProcess.R_A_RATE
            look_direction = pos - global_data.game_mgr.scene.active_camera.world_position
            if not self._is_2d:
                heading_pitch = common.utilities.vect2d_vertical_radian_half(look_direction, listener_look_at) * LockProcess.R_A_RATE
                pitch_diff = LockProcess.pitch_mapping(heading_pitch)
            else:
                pitch_diff = 0
            self._temp_math3d_angle_vector.x = pitch_diff
            self._temp_math3d_angle_vector.z = angle
            length_sqr = direction.length_sqr
            if entity not in self._entity_inf_map:
                if len(self._entity_inf_map) == self._elem_max_count:
                    panel_index = self.get_farthest_elem_index_and_del(length_sqr)
                    if panel_index == None:
                        return
                else:
                    panel_index = self.get_empty_elem_inde(angle)
                panel_item = self._panel_items[panel_index]
                panel_item.setOpacity(255)
                panel_item.setVisible(True)
                self.check_pitch_angle()
                panel_item.setRotation3D(self._temp_math3d_angle_vector)
                if self._is_2d:
                    if is_mecha:
                        panel_item.injure_mecha.StopAnimation('disappear')
                        panel_item.injure_mecha.PlayAnimation('show')
                    else:
                        panel_item.injure_normal.StopAnimation('disappear')
                        panel_item.injure_normal.PlayAnimation('show')
                else:
                    panel_item.PlayAnimation('show')
                    panel_item.StopAnimation('disappear')
                    self._animation_start_time = time.time()
                self._entity_inf_map[entity] = {'panel_index': panel_index,'pos': pos,'length_sqr': length_sqr}
            else:
                entity_inf = self._entity_inf_map[entity]
                entity_inf['pos'] = pos
                entity_inf['length_sqr'] = length_sqr
                panel_index = entity_inf['panel_index']
                panel_item = self._panel_items[panel_index]
                self.check_pitch_angle()
                panel_item.setRotation3D(self._temp_math3d_angle_vector)
                panel_item.stopAllActions()
                panel_item.setOpacity(255)
                if not self._is_2d:
                    if time.time() - self._animation_start_time > animation_interval:
                        self._animation_start_time = time.time()
                        panel_item.PlayAnimation('continue')
            color = self.get_color(damage)
            if self._is_2d:
                panel_item.injure_mecha.setVisible(False)
                panel_item.injure_mecha_blue.setVisible(False)
                panel_item.injure_normal.setVisible(False)
                panel_item.injure_normal_blue.setVisible(False)
                if is_mecha:
                    rate = 1.0 * 25 / 250
                    damage = min(350, max(100, damage))
                    scale = ((damage - 100) * rate + 75) / 100.0
                    if color == 'red':
                        nd_hint = panel_item.injure_mecha
                    else:
                        nd_hint = panel_item.injure_mecha_blue
                else:
                    rate = 1.0 * 25 / 120
                    damage = min(150, max(30, damage))
                    scale = ((damage - 30) * rate + 75) / 100.0
                    if color == 'red':
                        nd_hint = panel_item.injure_normal
                    else:
                        nd_hint = panel_item.injure_normal_blue
                nd_hint.setVisible(True)
                nd_hint.img_hurt.setScale(scale)
                self._disappear_last_time = nd_hint.GetAnimationMaxRunTime('disappear')
            else:
                panel_item.setVisible(True)
                rate = 1.0 * 25 / 250
                damage = min(350, max(100, damage))
                scale = ((damage - 100) * rate + 75) / 100.0
                panel_item.nd_scale.setScale(scale)
                if color == 'red':
                    arrow_pic = 'gui/ui_res_2/battle/hurt/3d_hurt.png'
                    trigger_pic = 'gui/ui_res_2/battle/hurt/icon_injure_machine.png' if is_mecha else 'gui/ui_res_2/battle/hurt/icon_injure_people.png'
                else:
                    arrow_pic = 'gui/ui_res_2/battle/hurt/3d_hurt_blue.png'
                    trigger_pic = 'gui/ui_res_2/battle/hurt/icon_injure_machine_blue.png' if is_mecha else 'gui/ui_res_2/battle/hurt/icon_injure_people_blue.png'
                panel_item.img_hurt.SetDisplayFrameByPath('', arrow_pic)
                panel_item.img_mech.setVisible(True)
                panel_item.img_mech.SetDisplayFrameByPath('', trigger_pic)
                self._disappear_last_time = panel_item.GetAnimationMaxRunTime('disappear')
            panel_item.DelayCallWithTag(self._elem_last_time - self._disappear_last_time, self.on_play_end_animtion, panel_index, panel_item, is_mecha)
            panel_item.DelayCallWithTag(self._elem_last_time, self.del_elem, self._elem_max_count + panel_index, entity)
            self.fix_position(panel_item, is_mecha)
            self.check_cover_elem_and_del()
            global_data.emgr.scene_hide_sound_visible.emit(True)
            return

    def on_play_end_animtion(self, panel_item, is_mecha):
        if self._is_2d:
            if is_mecha:
                panel_item.injure_mecha.PlayAnimation('disappear')
            else:
                panel_item.injure_normal.PlayAnimation('disappear')
        else:
            panel_item.PlayAnimation('disappear')

    def del_elem(self, entity):
        super(InjureProcess, self).del_elem(entity)
        if not self._entity_inf_map:
            global_data.emgr.scene_hide_sound_visible.emit(False)

    def get_color(self, damage):
        if damage > 0:
            return 'red'
        my_logic = global_data.cam_lplayer
        if not my_logic:
            return 'red'
        if my_logic:
            my_logic = my_logic.ev_g_control_target().logic
        if not my_logic:
            return 'red'
        if my_logic.sd.ref_raise_shield:
            return 'blue'
        return 'red'