# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMotorcycleDriver.py
from __future__ import absolute_import
from __future__ import print_function
from .com_character_ctrl.ComDriver import ComDriver
import logic.gcommon.common_const.animation_const as animation_const
import math
import math3d
import time
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.cdata.mecha_status_config as mecha_status_config

class ComMotorcycleDriver(ComDriver):
    BIND_EVENT = ComDriver.BIND_EVENT.copy()
    BIND_EVENT.update({})
    CHECK_DISTANCE = 3 * NEOX_UNIT_SCALE

    def init_position(self, pos, bdict):
        if pos:
            pos = math3d.vector(*pos)
            pos.y = pos.y + 0.5 * NEOX_UNIT_SCALE
            self.send_event('E_FOOT_POSITION', pos)
        else:
            move_up_pos = bdict.get('move_up_pos', True)
            pos = self.ev_g_position()
            char_ctrl = self.sd.ref_character
            if char_ctrl:
                if move_up_pos:
                    pos.y = pos.y + 0.5 * NEOX_UNIT_SCALE
                char_ctrl.position = pos

    def on_rotate(self, yaw, force_change_spd=True):
        seat_logic = self.sd.ref_avatar_seat_logic
        if seat_logic:
            seat_logic.send_event('E_ACTION_YAW', yaw)
            seat_logic.send_event('E_SYNC_YAW', yaw)

    def on_pitch(self, pitch, *args):
        seat_logic = self.sd.ref_avatar_seat_logic
        if seat_logic:
            seat_logic.send_event('E_ACTION_PITCH', pitch)
            seat_logic.send_event('E_SYNC_PITCH', pitch)

    def set_walk_direction(self, move_dir, reach_target_callback=None, reach_target_pos=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        super(ComMotorcycleDriver, self).set_walk_direction(move_dir, reach_target_callback, reach_target_pos)
        self.on_turn_dir()

    def get_model_yaw_mat(self):
        return self.sd.ref_rotatedata.rotation_mat

    def on_turn_dir(self):
        model_rot_mat = self.get_model_yaw_mat()
        model_rot = math3d.matrix_to_rotation(model_rot_mat)
        self.send_event('E_SET_CHAR_ROTATION_DIR', model_rot)

    def on_move(self, move_dir, target_callback=None, target_pos=None):
        super(ComMotorcycleDriver, self).on_move(move_dir, target_callback, target_pos)
        is_in_water_area = self.ev_g_is_in_water_area()
        if is_in_water_area:
            return
        down_direction = math3d.vector(0, self.CHECK_DISTANCE, 0)
        foot_position = self.ev_g_foot_position()
        head_position = self.ev_g_col_head_position()
        head_col_result = self.ev_g_sweep_test(down_direction, head_position)
        col_obj_ids = set()
        is_in_col = False
        if head_col_result and head_col_result[0]:
            is_in_col = True
            if len(head_col_result) >= 5:
                col_obj_list = head_col_result[4]
                for one_col_obj in col_obj_list:
                    if one_col_obj:
                        col_obj_ids.add(one_col_obj.cid)

        filter_col_ids = self.ev_g_all_exclude_col_id()
        filter_col_ids = set(filter_col_ids)
        foot_col_result = self.ev_g_sweep_test(down_direction, foot_position)
        if foot_col_result and foot_col_result[0]:
            is_in_col = True
            if len(foot_col_result) >= 5:
                col_obj_list = foot_col_result[4]
                for one_col_obj in col_obj_list:
                    if not one_col_obj:
                        continue
                    col_obj_ids.add(one_col_obj.cid)

        if is_in_col:
            if col_obj_ids in filter_col_ids:
                is_in_col = False
        if is_in_col:
            foot_position.y = foot_position.y + 0.02 * NEOX_UNIT_SCALE
            self.send_event('E_FOOT_POSITION', foot_position)

    def on_pos_changed(self, pos, *arg):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        super(ComMotorcycleDriver, self).on_pos_changed(pos, *arg)
        if not self.ev_g_is_character_active():
            return
        animator = self.ev_g_animator()
        if not animator:
            return
        turn_full_body_node = animator.find(animation_const.TURN_X_FULL_BODY_NODE)
        if not turn_full_body_node:
            return
        rot = char_ctrl.calculateGroundAngle(self.CHECK_DISTANCE)
        degree = math.degrees(rot)
        MAX_DEGREE = 70
        if degree > MAX_DEGREE:
            degree = MAX_DEGREE
        elif degree < -MAX_DEGREE:
            degree = -MAX_DEGREE
        turn_full_body_node.twistAngle = degree