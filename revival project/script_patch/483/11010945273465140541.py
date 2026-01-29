# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataAimIK.py
from __future__ import absolute_import
from ..share.ComDataBase import ComDataBase
import world
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const.character_anim_const import UP_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
BAN_AIM_IK_STATE = [
 status_config.ST_RELOAD, status_config.ST_SWITCH]

class ComDataAimIK(ComDataBase):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete'
       }

    def get_share_data_name(self):
        return 'ref_aimik'

    def __init__(self):
        super(ComDataAimIK, self).__init__(False)
        self.is_blending = False
        self.lerp_time = 0.05
        self.lerp_thresh = 0
        self.max_blend_rate = 1
        self.cur_blend_rate = 0
        self.force_update_this_frame = False
        self.support_ik = True
        self._aim_ik_enabled = False
        self.aim_ik_solver = None
        self._aim_socket = None
        self.pitch_limit = 70
        self._support_exit_aim_ik_lerp = False
        self.exit_lerp = False
        self.exit_lerp_time = 0.0
        self.exit_lerp_thresh = 0.2
        self.exit_blend_rate = 0
        self._model = None
        self.need_modify_forward = False
        return

    def _do_cache(self):
        self._model = None
        self.unregist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
        self.unregist_event('E_AIM_IK_PARAM', self.init_aim_ik)
        self.unregist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
        self.unregist_event('E_ENTER_STATE', self.on_enter_states)
        self.unregist_event('E_LEAVE_STATE', self.on_leave_states)
        self.unregist_event('E_MOVE', self.update_aim_position)
        self.unregist_event('E_POST_ACTION', self.on_post_action)
        return

    def _do_destroy(self):
        self._model = None
        self.unregist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
        self.unregist_event('E_AIM_IK_PARAM', self.init_aim_ik)
        self.unregist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
        self.unregist_event('E_ENTER_STATE', self.on_enter_states)
        self.unregist_event('E_LEAVE_STATE', self.on_leave_states)
        self.unregist_event('E_MOVE', self.update_aim_position)
        self.unregist_event('E_POST_ACTION', self.on_post_action)
        return

    def on_load_animator_complete(self, *args):
        self._model = self.ev_g_model()
        if not self._model:
            return
        if self.ev_g_is_avatar():
            if not self.sd.ref_is_refreshing_whole_model:
                self.activate_ecs()
                self.regist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
                self.regist_event('E_AIM_IK_PARAM', self.init_aim_ik)
                self.regist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
                self.regist_event('E_ENTER_STATE', self.on_enter_states)
                self.regist_event('E_LEAVE_STATE', self.on_leave_states)
                self.regist_event('E_MOVE', self.update_aim_position)
            if not self.aim_ik_solver:
                self.aim_ik_solver = world.aimik()
                self._model.set_custom_ik_solver(self.aim_ik_solver, 2)
        else:
            self.deactivate_ecs()
            self.unregist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
            self.unregist_event('E_AIM_IK_PARAM', self.init_aim_ik)
            self.unregist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
            self.unregist_event('E_MOVE', self.update_aim_position)

    def on_enter_states(self, new_state):
        if new_state in BAN_AIM_IK_STATE:
            if self._aim_ik_enabled:
                self._model.set_aimik_enable(False)

    def on_leave_states(self, leave_state, new_state=None):
        if leave_state in BAN_AIM_IK_STATE:
            if self._aim_ik_enabled:
                self._model.set_aimik_enable(True)

    def on_set_lerp_time(self, time, exit_time=0.2):
        self.lerp_thresh = time
        self.exit_lerp_thresh = exit_time
        self.lerp_time = 0
        self.is_blending = True

    def init_aim_ik(self, aim_param, support_exit_aim_ik_lerp=False):
        aim_socket, bone_list = aim_param
        if not self.aim_ik_solver:
            self.aim_ik_solver = world.aimik()
            self._model.set_custom_ik_solver(self.aim_ik_solver, 2)
        self._aim_socket = aim_socket
        self.aim_ik_solver.set_aim_param(bone_list, self._aim_socket)
        self._support_exit_aim_ik_lerp = support_exit_aim_ik_lerp

    def _enter_aim_ik(self, pitch_limit=80, max_blend_rate=0.9):
        self.cur_blend_rate = 0
        self.lerp_time = 0
        self.init_aim_position()
        if self.exit_lerp:
            self.exit_lerp = False
            self.unit_obj.unregist_event('E_POST_ACTION', self.on_post_action)
        else:
            self.activate_ecs()
            if not self.ev_g_is_in_any_state(BAN_AIM_IK_STATE):
                self._model.set_aimik_enable(True)
        self.pitch_limit = pitch_limit
        self.max_blend_rate = max_blend_rate

    def _quit_aim_ik(self):
        if self._support_exit_aim_ik_lerp:
            self.activate_exit_lerp()
        else:
            self.deactivate_ecs()
            self._model.set_aimik_enable(False)

    def enable_aim_ik(self, enable, pitch_limit=80, max_blend_rate=0.9):
        if self._aim_ik_enabled == enable:
            return
        if enable:
            self._enter_aim_ik(pitch_limit, max_blend_rate)
        else:
            self._quit_aim_ik()
        self._aim_ik_enabled = enable

    def init_aim_position(self):
        from logic.gcommon.const import SEX_MALE
        mat = self._model.get_socket_matrix(self._aim_socket, world.SPACE_TYPE_WORLD)
        pos = mat.translation + mat.rotation.forward * NEOX_UNIT_SCALE
        self.aim_ik_solver.set_aim_target(pos)
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            self.need_modify_forward = False
        else:
            weapon_id = obj_weapon.get_item_id()
            self.need_modify_forward = self.get_value('G_SEX') == SEX_MALE and weapon_id == 10414 and not self.get_value('G_APPEARANCE_IN_SKATE')

    def activate_exit_lerp(self):
        self.unit_obj.regist_event('E_POST_ACTION', self.on_post_action)
        self.is_blending = True
        self.exit_lerp = True
        self.exit_lerp_time = 0
        self.exit_blend_rate = self.cur_blend_rate

    def on_post_action(self, anim_name, part, *args, **kwargs):
        if part == UP_BODY:
            self.deactivate_ecs()

    def deactivate_ecs(self):
        if self._model:
            self._model.set_aimik_enable(False)
        if self.exit_lerp:
            self.unit_obj.unregist_event('E_POST_ACTION', self.on_post_action)
            self.exit_lerp = False
        super(ComDataAimIK, self).deactivate_ecs()

    def update_aim_position(self, move_dir):
        self.force_update_this_frame = True

    def draw_aim_line(self, end_pos):
        model = self.ev_g_model()
        if model:
            aim_socket = self._aim_socket if self._aim_socket else 'aim'
            chect_begin = model.get_socket_matrix(aim_socket, world.SPACE_TYPE_WORLD).translation
            check_end = end_pos
            line_list = [(chect_begin, check_end, 255)]
            self.send_event('E_DRAW_LINE', line_list)