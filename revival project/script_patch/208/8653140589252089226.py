# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComAimIK.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import math
from common.utils import timer
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const.character_anim_const import UP_BODY
UNIT_Y = math3d.vector(0, 1, 0)
BAN_AIM_IK_STATE = [
 status_config.ST_RELOAD, status_config.ST_SWITCH]

class ComAimIK(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'G_SUPPORT_AIM_IK_BLEND_RATE': 'on_get_support_blend_rate',
       'E_CHARACTER_ATTR': 'change_character_attr'
       }

    def __init__(self):
        super(ComAimIK, self).__init__()
        self._support_ik = True
        self._aim_ik_enabled = False
        self._aim_ik_solver = None
        self._cur_aim_pos = None
        self._new_aim_pos = None
        self._clear_lerp_timer = 0
        self._lerp_time = 0.05
        self._lerp_thresh = 0
        self._aim_socket = None
        self._pitch_limit = 70
        self._support_blend_rate = False
        self._max_blend_rate = 0.9
        self._cur_blend_rate = 0.0
        self._support_exit_aim_ik_lerp = False
        self._exit_lerp_timer = None
        self._exit_lerp_time = 0.0
        self._exit_lerp_thresh = 0.2
        self._soft_exit_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAimIK, self).init_from_dict(unit_obj, bdict)

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            print(('test--ComAimIK.animator_info--_aim_ik_enabled =', self._aim_ik_enabled, '--unit_obj =', self.unit_obj))

    def destroy(self):
        super(ComAimIK, self).destroy()
        self.unregist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
        self.unregist_event('E_AIM_IK_PARAM', self.init_aim_ik)
        self.unregist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
        self.unregist_event('E_ENTER_STATE', self.on_enter_states)
        self.unregist_event('E_LEAVE_STATE', self.on_leave_states)
        self._release_exit_lerp_timer()

    def on_load_animator_complete(self, *args):
        self._model = self.ev_g_model()
        if not self._model:
            return
        if self.ev_g_is_avatar():
            if not self.sd.ref_is_refreshing_whole_model:
                self.regist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
                self.regist_event('E_AIM_IK_PARAM', self.init_aim_ik)
                self.regist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
                self.regist_event('E_ENTER_STATE', self.on_enter_states)
                self.regist_event('E_LEAVE_STATE', self.on_leave_states)
            if not self._aim_ik_solver:
                self._aim_ik_solver = world.aimik()
                self._model.set_custom_ik_solver(self._aim_ik_solver, 2)
                self._support_blend_rate = hasattr(self._aim_ik_solver, 'set_aim_blend_rate')
        else:
            self.unregist_event('E_ENABLE_AIM_IK', self.enable_aim_ik)
            self.unregist_event('E_AIM_IK_PARAM', self.init_aim_ik)
            self.unregist_event('E_AIM_LERP_TIME', self.on_set_lerp_time)
            self.unregist_event('E_ENTER_STATE', self.on_enter_states)
            self.unregist_event('E_LEAVE_STATE', self.on_leave_states)
            self._release_exit_lerp_timer()

    def on_enter_states(self, new_state):
        if new_state in BAN_AIM_IK_STATE:
            if self._aim_ik_enabled:
                self._model.set_aimik_enable(False)

    def on_leave_states(self, leave_state, new_state=None):
        if leave_state in BAN_AIM_IK_STATE:
            if self._aim_ik_enabled:
                self._model.set_aimik_enable(True)

    def on_set_lerp_time(self, time, exit_time=0.2):
        self._lerp_thresh = time
        self._exit_lerp_thresh = exit_time
        if self._support_blend_rate:
            self._lerp_time = 0
            self.need_update = True
        else:

            def clear_lerp():
                if not self or not self.is_valid():
                    return
                self._lerp_thresh = 0.01
                self._clear_lerp_timer = 0
                return timer.RELEASE

            if self._clear_lerp_timer:
                global_data.game_mgr.unregister_logic_timer(self._clear_lerp_timer)
            self._clear_lerp_timer = global_data.game_mgr.register_logic_timer(clear_lerp, interval=self._lerp_thresh, times=1, mode=timer.CLOCK)

    def on_get_support_blend_rate(self):
        return self._support_blend_rate

    def init_aim_ik(self, aim_param, support_exit_aim_ik_lerp=False):
        aim_socket, bone_list = aim_param
        if not self._aim_ik_solver:
            self._aim_ik_solver = world.aimik()
            self._model.set_custom_ik_solver(self._aim_ik_solver, 2)
        self._aim_socket = aim_socket
        self._aim_ik_solver.set_aim_param(bone_list, self._aim_socket)
        self._support_exit_aim_ik_lerp = support_exit_aim_ik_lerp

    def _handle_event_bound(self, bound):
        func = self.unit_obj.regist_event if bound else self.unit_obj.unregist_event
        func('E_ACTION_YAW', self.update_aim_position)
        func('E_ACTION_PITCH', self.update_aim_position)
        func('E_MOVE', self.update_aim_position)

    def _enter_aim_ik(self, pitch_limit=80, max_blend_rate=0.9):
        self._cur_blend_rate = 0
        self._lerp_time = 0
        self.init_aim_position()
        self.update_aim_position()
        if self._exit_lerp_timer:
            self._release_exit_lerp_timer()
            self.unit_obj.unregist_event('E_POST_ACTION', self.on_post_action)
        else:
            self._handle_event_bound(True)
            if not self.ev_g_is_in_any_state(BAN_AIM_IK_STATE):
                self._model.set_aimik_enable(True)
        self._pitch_limit = pitch_limit
        self._max_blend_rate = max_blend_rate

    def _quit_aim_ik(self):
        self.need_update = False
        self._cur_aim_pos = None
        self._new_aim_pos = None
        if self._support_blend_rate and self._support_exit_aim_ik_lerp:
            self.activate_exit_lerp()
        else:
            self._handle_event_bound(False)
            self._model.set_aimik_enable(False)
        return

    def enable_aim_ik(self, enable, pitch_limit=80, max_blend_rate=0.9):
        if self._aim_ik_enabled == enable:
            return
        if enable:
            self._enter_aim_ik(pitch_limit, max_blend_rate)
            self.need_update = True
        else:
            self._quit_aim_ik()
        self._aim_ik_enabled = enable

    def init_aim_position(self):
        mat = self._model.get_socket_matrix(self._aim_socket, world.SPACE_TYPE_WORLD)
        pos = mat.translation + mat.rotation.forward * NEOX_UNIT_SCALE
        self._cur_aim_pos = pos
        self._new_aim_pos = pos
        self._aim_ik_solver.set_aim_target(pos)
        if self._support_blend_rate:
            self._aim_ik_solver.set_aim_blend_rate(0)

    def get_state_look_at_pos(self):
        from logic.gcommon.common_const.collision_const import GROUP_CAMERA_INCLUDE
        CHECK_DIST = 400 * NEOX_UNIT_SCALE
        scn = global_data.game_mgr.scene
        cam = scn.active_camera
        start_pos = cam.world_position
        forward_dir = cam.world_rotation_matrix.forward
        PartCamera = global_data.game_mgr.scene.get_com('PartCamera')
        if PartCamera:
            if PartCamera.cam_manager:
                default_pos = PartCamera.cam_manager.default_pos or math3d.vector(0, 0, 0)
                start_pos += forward_dir * (abs(default_pos.z) + NEOX_UNIT_SCALE * 10)
        if forward_dir.length < 0.0001:
            forward_dir = FORWARD_VECTOR
            log_error('error direction!!!!')
        end_pos = start_pos + forward_dir * CHECK_DIST
        hit, point, normal, fraction, color, obj = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_CAMERA_INCLUDE, 0)
        if hit:
            look_at_pos = point
        else:
            look_at_pos = end_pos
        return look_at_pos

    def draw_aim_line(self, end_pos):
        model = self.ev_g_model()
        if model:
            aim_socket = self._aim_socket if self._aim_socket else 'aim'
            chect_begin = model.get_socket_matrix(aim_socket, world.SPACE_TYPE_WORLD).translation
            check_end = end_pos
            line_list = [(chect_begin, check_end, 255)]
            self.send_event('E_DRAW_LINE', line_list)

    def get_aim_ik_forward(self):
        from logic.gcommon.const import SEX_MALE
        camera = world.get_active_scene().active_camera
        forward = self.clap_forward(camera.rotation_matrix.forward)
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return forward
        weapon_id = obj_weapon.get_item_id()
        if SEX_MALE == self.get_value('G_SEX') and weapon_id == 10414 and not self.get_value('G_APPEARANCE_IN_SKATE'):
            up = camera.rotation_matrix.up
            right = camera.rotation_matrix.right
            up_factor = -0.1
            right_factor = -0.2
            forward = forward + math3d.vector(right_factor, right_factor, right_factor) * right + math3d.vector(up_factor, up_factor, up_factor) * up
            forward.normalize()
        return forward

    def update_aim_position(self, *args, **kwargs):
        import game3d
        camera = world.get_active_scene().active_camera
        forward = self.get_aim_ik_forward()
        end_pos = camera.position + forward * NEOX_UNIT_SCALE * 200
        if self._support_blend_rate:
            self._aim_ik_solver.set_aim_target(end_pos)
            self._aim_ik_solver.set_aim_blend_rate(self._cur_blend_rate)
        else:
            self._lerp_time = 0
            self._new_aim_pos = end_pos
            self.need_update = True

    def tick(self, delta):
        if self._support_blend_rate:
            if self._lerp_thresh <= 0:
                self.need_update = False
                return self._aim_ik_solver.set_aim_blend_rate(self._max_blend_rate)
            self._lerp_time += delta
            if self._lerp_time >= self._lerp_thresh:
                self.need_update = False
                rate = 1
            else:
                rate = self._lerp_time / self._lerp_thresh
            self._cur_blend_rate = rate * self._max_blend_rate
            rate = self._cur_blend_rate
            self._aim_ik_solver.set_aim_blend_rate(rate)
        else:
            if not self._cur_aim_pos or not self._new_aim_pos:
                self.need_update = False
                return
            self._lerp_time += delta
            if self._lerp_time >= self._lerp_thresh:
                self.need_update = False
                self._cur_aim_pos = self._new_aim_pos
            else:
                self._cur_aim_pos.intrp(self._cur_aim_pos, self._new_aim_pos, self._lerp_time / self._lerp_thresh)
            self._aim_ik_solver.set_aim_target(self._cur_aim_pos)

    def clap_forward(self, forward):
        if math.degrees(forward.pitch) > self._pitch_limit:
            y = -math.tan(math.radians(self._pitch_limit)) * math.sqrt(forward.x ** 2 + forward.z ** 2)
            forward = math3d.vector(forward.x, y, forward.z)
            forward.normalize()
            return forward
        return forward

    def _release_exit_lerp_timer(self):
        if self._exit_lerp_timer:
            global_data.game_mgr.unregister_logic_timer(self._exit_lerp_timer)
            self._exit_lerp_timer = None
        return

    def _exit_lerp_done(self):
        self.unit_obj.unregist_event('E_POST_ACTION', self.on_post_action)
        self._handle_event_bound(False)
        self._model.set_aimik_enable(False)

    def _execute_exit_lerp(self, dt):
        self._exit_lerp_time += dt
        if self._exit_lerp_time > self._exit_lerp_thresh:
            self._exit_lerp_time = self._exit_lerp_thresh
        rate = 1.0 - self._exit_lerp_time / self._exit_lerp_thresh
        self._aim_ik_solver.set_aim_blend_rate(self._cur_blend_rate * rate)
        if self._exit_lerp_time == self._exit_lerp_thresh:
            self._exit_lerp_done()
            self._exit_lerp_timer = None
            return timer.RELEASE
        else:
            return

    def activate_exit_lerp(self):
        self.unit_obj.regist_event('E_POST_ACTION', self.on_post_action)
        self._release_exit_lerp_timer()
        self._exit_lerp_time = 0
        self._exit_lerp_timer = global_data.game_mgr.register_logic_timer(self._execute_exit_lerp, interval=1, times=-1, timedelta=True)

    def on_post_action(self, anim_name, part, *args, **kwargs):
        if part == UP_BODY:
            self._exit_lerp_done()
            self._release_exit_lerp_timer()