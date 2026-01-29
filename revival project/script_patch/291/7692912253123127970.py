# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComDriver.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from ....cdata import jump_physic_config
from logic.gcommon.common_const import collision_const
from ....cdata import state_physic_arg
from common.cfg import confmgr
import math
import game3d
from logic.client.const import game_mode_const
from logic.gcommon.cdata.mecha_status_config import *
from common.utils import timer
import world
import math3d
from logic.gcommon.utility import dummy_cb
from logic.gcommon import editor

@editor.com_exporter('\xe7\x89\xa9\xe7\x90\x86\xe7\xbb\x84\xe4\xbb\xb6', {('cur_speed', 'float'): {'zh_name': '\xe9\x80\x9f\xe5\xba\xa6(m/s)','getter': lambda self: self.sd.ref_cur_speed / NEOX_UNIT_SCALE if self.sd.ref_cur_speed else -1
                            },
   ('vertical_speed', 'float'): {'zh_name': '\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6(m/s)','getter': lambda self: self.ev_g_vertical_speed() / NEOX_UNIT_SCALE if self.ev_g_vertical_speed() else -1
                                 }
   })
class ComDriver(UnitCom):
    BIND_EVENT = {'E_ACTIVE_DRIVER': 'on_active_driver',
       'E_DISABLE_DRIVER': 'on_disable_driver',
       'E_MODEL_LOADED': 'on_model_loaded',
       'E_RESET_CHAR_SIZE': 'reset_char_size',
       'E_SET_WALK_DIRECTION': 'set_walk_direction',
       'G_GET_WALK_DIRECTION': 'get_walk_direction',
       'E_RESET_GRAVITY': 'on_reset_gravity',
       'E_SPEED': 'on_set_speed',
       'G_SPEED': 'on_get_speed',
       'E_ROTATE': 'on_rotate',
       'E_PITCH': 'on_pitch',
       'E_MOVE': 'on_move',
       'G_MOVE_DIR': 'get_move_dir',
       'E_CLEAR_SPEED': 'on_stop',
       'E_CLEAR_SPEED_INTRP': 'on_stop_intrp',
       'E_CHANGE_CHAR_GROUP': 'set_group',
       'G_CHAR_GROUP': 'get_group',
       'E_STEP_HEIGHT': 'set_step_height',
       'E_RESET_STEP_HEIGHT': 'reset_step_height',
       'G_STEP_HEIGHT': 'get_step_height',
       'G_HEIGHT': 'get_height',
       'E_HEIGHT': 'set_height',
       'G_RADIUS': 'get_radius',
       'G_GRAVITY': 'get_gravity',
       'G_ON_GROUND': 'get_on_ground',
       'E_JUMP': 'jump',
       'G_CHAR_GROUP_MASK': 'get_group_mask',
       'E_CHANGE_CHAR_GROUP_MASK': 'set_group_mask',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_DRAW_LINE': 'draw_line',
       'G_INPUT_MOVE_DIR': '_get_move_info_from_rock_or_keyboard',
       'E_CHARACTER_ACTIVE': 'active_character',
       'E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL': 'enable_camera_rotate_sync_to_model',
       'E_ENABLE_CAMERA_REFERENCE_MOVE': 'enable_camera_reference_move',
       'G_ALL_PHYSX_STATE_DESC': 'get_all_state_desc',
       'E_ENABLE_POS_CHANGE_NOTIFY': 'on_enable_pos_change_notify',
       'E_TRANS_CREATE_MECHA_TO_SHARE_NOTIFY': 'on_trans_to_share',
       'E_START_WAITING_CEHCK': 'on_start_waiting_check',
       'E_REFRESH_CHARACTER_Y_OFFSET': 'refresh_character_y_offset',
       'E_JUMP_FACTOR': 'change_jump_factor'
       }

    def __init__(self):
        super(ComDriver, self).__init__()
        self.need_update = False
        self.sd.ref_cur_speed = 0
        self._init_speed = None
        self._draw_obj_list = []
        self.is_share = False
        self._camera_rotate_sync_to_model_enabled = True
        self._camera_reference_move_enabled = False
        self._get_reference_rotation = self._get_model_rotation
        self.stepheight = NEOX_UNIT_SCALE
        self.enable_pos_notify = True
        self.brake_timer = None
        self.waiting_timer = None
        self.jump_factor = 1.0
        return

    def _clear_draw_obj(self):
        if self._draw_obj_list:
            for draw_obj in self._draw_obj_list:
                draw_obj.destroy()

        self._draw_obj_list = []

    def draw_line(self, line_list, is_append=False):
        if not is_append:
            self._clear_draw_obj()
        if not line_list:
            return
        scene = self.scene
        index = 0
        for one_line_info in line_list:
            obj = world.primitives(scene)
            start = one_line_info[0]
            end = one_line_info[1]
            color = 65280
            if len(one_line_info) > 2:
                color = one_line_info[2]
            index += 1
            obj.create_line([((start,), (end,), color)])
            self._draw_obj_list.append(obj)

    def init_from_dict(self, unit_obj, bdict):
        super(ComDriver, self).init_from_dict(unit_obj, bdict)
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        self.sd.ref_on_ground = False
        self.ignore_ongournd_cb = bdict.get('ignore_ongournd_cb', False)
        self.char_size = bdict.get('char_size', None)
        self.is_share = bdict.get('share')
        self.init_character()
        self.init_position(bdict.get('position', None), bdict)
        model = self.ev_g_model()
        if model:
            self.on_model_loaded(model)
        self._init_speed = bdict.get('init_speed', None)
        return

    def destroy(self):
        self.clear_brake_timer()
        self.clear_waiting_timer()
        self.uninit_character()
        self._clear_draw_obj()
        self._get_reference_rotation = dummy_cb
        super(ComDriver, self).destroy()

    def on_init_complete(self):
        if self._init_speed:
            speed_value = self._init_speed.length
            if speed_value > 0:
                max_run_speed = self.ev_g_max_run_speed() or 0
                max_walk_speed = self.ev_g_max_walk_speed() or 0
                can_move = False
                if speed_value > max_walk_speed:
                    if speed_value > max_run_speed:
                        speed_value = max_run_speed
                        self._init_speed.normalize()
                        self._init_speed = self._init_speed * speed_value
                    if self.ev_g_status_check_pass(MC_RUN):
                        can_move = True
                        self.send_event('E_ACTIVE_STATE', MC_RUN)
                elif self.ev_g_status_check_pass(MC_MOVE):
                    can_move = True
                    self.send_event('E_ACTIVE_STATE', MC_MOVE)
                if can_move:
                    self.sd.ref_cur_speed = speed_value
                    self.send_event('E_CHARACTER_WALK', self._init_speed)
        self._init_speed = None
        return

    def on_active_driver(self):
        scene = self.scene
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.activate(scene.scene_col)
        self.send_event('E_GRAVITY', jump_physic_config.gravity * NEOX_UNIT_SCALE)

    def on_disable_driver(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        char_ctrl.deactivate(self.scene.scene_col)

    def on_model_loaded(self, model):
        if self.ev_g_death():
            return
        passenger = self.ev_g_passenger_info() or {}
        char_ctrl = self.sd.ref_character
        if char_ctrl and (len(passenger) <= 0 or self.sd.ref_is_robot) and not self.is_share:
            self.on_active_driver()

    def on_rotate(self, yaw, force_change_spd=True):
        self.sd.ref_logic_trans.yaw_target += yaw

    def on_pitch(self, pitch, *args):
        self.send_event('E_ACTION_PITCH', pitch)
        self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)

    def _get_model_rotation(self):
        return self.ev_g_rotation()

    def _get_camera_rotation(self):
        if self.sd.ref_effective_camera_rot:
            return self.sd.ref_effective_camera_rot
        return math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)

    def enable_camera_rotate_sync_to_model(self, flag):
        if flag == self._camera_rotate_sync_to_model_enabled:
            return
        func = self.regist_event if flag else self.unregist_event
        func('E_ROTATE', self.on_rotate)
        self._camera_rotate_sync_to_model_enabled = flag

    def enable_camera_reference_move(self, flag):
        if self._camera_reference_move_enabled == flag:
            return
        if flag:
            self._get_reference_rotation = self._get_camera_rotation
        else:
            self._get_reference_rotation = self._get_model_rotation
        self.enable_camera_rotate_sync_to_model(not flag)
        self._camera_reference_move_enabled = flag

    def on_move(self, move_dir, target_callback=None, target_pos=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        self.send_event('E_CHECK_ACTIVE_CHARACTER')
        if not move_dir or move_dir.is_zero:
            walk_direction = char_ctrl.getWalkDirection()
            if not walk_direction.is_zero:
                walk_direction.normalize()
        else:
            rotation = self._get_reference_rotation()
            walk_direction = rotation.rotate_vector(move_dir)
            walk_direction.y = 0
            if not walk_direction.is_zero:
                walk_direction.normalize()
        walk_direction = walk_direction * self.sd.ref_cur_speed
        self.set_walk_direction(walk_direction, target_callback, target_pos)

    def on_stop(self):
        self.clear_brake_timer()
        self.sd.ref_cur_speed = 0
        self.set_walk_direction(math3d.vector(0, 0, 0))

    def on_stop_intrp(self, lerp_time):
        cur_walk_dir = self.get_walk_direction()
        if cur_walk_dir.is_zero:
            return
        start_speed = self.sd.ref_cur_speed
        cur_walk_dir.normalize()
        self.brake_time = 0

        def brake(dt):
            self.brake_time += dt
            self.sd.ref_cur_speed = start_speed * (1 - self.brake_time / lerp_time)
            if self.sd.ref_cur_speed < 0:
                self.sd.ref_cur_speed = 0
            self.set_walk_direction(cur_walk_dir * self.sd.ref_cur_speed)
            if self.brake_time >= lerp_time or self.sd.ref_cur_speed == 0:
                self.sd.ref_cur_speed = 0
                self.set_walk_direction(math3d.vector(0, 0, 0))
                return timer.RELEASE

        self.brake_timer = global_data.game_mgr.register_logic_timer(brake, 1, timedelta=True)

    def clear_brake_timer(self):
        if self.brake_timer:
            global_data.game_mgr.unregister_logic_timer(self.brake_timer)
            self.brake_timer = None
        return

    def on_enable_pos_change_notify(self, enable):
        self.enable_pos_notify = enable
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            self.on_pos_changed(char_ctrl.position)

    def on_pos_changed(self, pos, *arg):
        if math.isinf(pos.x) or math.isinf(pos.y) or math.isinf(pos.y) or math.isnan(pos.x) or math.isnan(pos.y) or math.isnan(pos.y):
            return
        if not self.enable_pos_notify:
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)

    def on_fall(self):
        if not self.is_valid():
            return
        self.sd.ref_on_ground = False
        self.send_event('E_FALL')

    def uninit_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setPositionChangedCallback(None)
            char_ctrl.setRotationChangedCallback(None)
            char_ctrl.setOnTouchGroundCallback(None)
            char_ctrl.setOnFallCallback(None, 0.0)
        return

    def reset_phys_attr(self, physic_conf=None):
        if physic_conf is None:
            physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
            mecha_id = self.sd.ref_mecha_id or 8001
            physic_conf = physic_conf[str(mecha_id)]
        self.stepheight = physic_conf['step_height'] * NEOX_UNIT_SCALE
        max_slope = physic_conf['max_slope']
        if global_data.game_mode.is_mode_type(game_mode_const.TDM_MaxSlop):
            max_slope = physic_conf['max_slope_death']
        enable_z_capsule = physic_conf.get('enable_z_capsule', 0)
        enable_z_capsule = bool(enable_z_capsule)
        self.send_event('E_ENABLE_Z_CAPSULE', enable_z_capsule)
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        added_margin = state_physic_arg.added_margin * NEOX_UNIT_SCALE
        pos_interpolate = state_physic_arg.pos_interpolate
        jump_speed = physic_conf['jump_speed'] * NEOX_UNIT_SCALE
        gravity = physic_conf['gravity'] * NEOX_UNIT_SCALE
        fall_speed = physic_conf['max_fall_speed'] * NEOX_UNIT_SCALE
        self.character_offset_x = collision_const.STAND_MODEL_OFFSET_X
        character = self.sd.ref_character
        character.setStepHeight(self.stepheight)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setJumpSpeed(jump_speed)
        character.setFallSpeed(fall_speed)
        character.setGravity(gravity * self.sd.ref_gravity_scale)
        character.setXOffset(-self.character_offset_x)
        character.setSmoothFactor(pos_interpolate)
        character.enableFollow = False
        width = self.char_size or physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2 if 1 else self.char_size[0]
        height = self.char_size or physic_conf['character_size'][1] * NEOX_UNIT_SCALE if 1 else self.char_size[1]
        model_offset_y = self.ev_g_model_offset_y() or 0
        if enable_z_capsule:
            self.character_down_height = width / 2 + model_offset_y
        else:
            self.character_down_height = height / 2 + model_offset_y
        character.setYOffset(-self.character_down_height)
        self.send_event('E_RECREATE_CHARACTER', width, height, 0.6)
        if self.is_share:
            character.group = 65520
        if getattr(character, 'setMaxPushDist', None):
            character.setMaxPushDist(0.5 * NEOX_UNIT_SCALE)
        return

    def refresh_character_y_offset(self, force_offset=0):
        character = self.sd.ref_character
        if not character:
            return
        mecha_id = self.sd.ref_mecha_id or 8001
        physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content', str(mecha_id))
        width = self.char_size or physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2 if 1 else self.char_size[0]
        height = self.char_size or physic_conf['character_size'][1] * NEOX_UNIT_SCALE if 1 else self.char_size[1]
        model_offset_y = self.ev_g_model_offset_y() or 0
        if character.enableZCapsule:
            self.character_down_height = width / 2 + model_offset_y + force_offset
        else:
            self.character_down_height = height / 2 + model_offset_y + force_offset
        character.setYOffset(-self.character_down_height)

    def reset_char_size(self, width, height, y_off):
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        model_offset_y = self.ev_g_model_offset_y() or 0
        self.character_down_height = y_off + padding + model_offset_y
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setYOffset(-self.character_down_height)
        self.send_event('E_RECREATE_CHARACTER', width, height, 0.6)

    def init_character(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setPositionChangedCallback(self.on_pos_changed)
        if not self.ignore_ongournd_cb:
            char_ctrl.setOnFallCallback(lambda : global_data.game_mgr.next_exec(self.on_fall), jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE)
            char_ctrl.setOnTouchGroundCallback(lambda *args: global_data.game_mgr.next_exec(self.on_ground_callback, *args))
        self.reset_phys_attr()

    def init_position(self, pos, bdict):
        if pos:
            pos = math3d.vector(*pos)
        else:
            pos = self.ev_g_position()
        if pos:
            pos.y = pos.y + 0.5 * NEOX_UNIT_SCALE
            self.send_event('E_FOOT_POSITION', pos)

    def active_character(self, *args, **kwargs):
        if kwargs.get('not_update_pos', False):
            return
        foot_position = self.ev_g_foot_position()
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if not foot_position:
            return
        col_result = char_ctrl.getStaticSweepTest()
        is_hit, hit_normal, move_len = col_result
        if is_hit:
            chect_begin = foot_position
            move_len *= 0.7
            incr_dist = hit_normal * move_len
            check_end = chect_begin + incr_dist
            if hit_normal.y >= 0 and incr_dist.length <= 5 * NEOX_UNIT_SCALE:
                self.send_event('E_FOOT_POSITION', check_end)
                return
            cur_physic_postion = char_ctrl.physicalPosition
            direction = math3d.vector(0, -1 * NEOX_UNIT_SCALE, 0)
            col_result = char_ctrl.sweepTest(cur_physic_postion, direction)
            is_hit = col_result[0]
            hit_position = col_result[1]
            hit_normal = col_result[2]
            move_len = col_result[3]
            if is_hit:
                if foot_position.y < hit_position.y:
                    diff_height = hit_position.y - foot_position.y
                    foot_position.y = foot_position.y + diff_height
                    self.send_event('E_FOOT_POSITION', foot_position)

    def set_walk_direction(self, move_dir, reach_target_callback=None, reach_target_pos=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_immobilized():
            move_dir = math3d.vector(0, 0, 0)
        if move_dir and move_dir.is_zero:
            self.send_event('E_ACTION_SYNC_STOP')
        self.send_event('E_CHARACTER_WALK', move_dir)
        if reach_target_pos:
            char_ctrl.setOnReachTargetCallback(reach_target_pos, reach_target_callback)
        else:
            char_ctrl.clearReachTargetCallback()

    def get_walk_direction(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return math3d.vector(0, 0, 0)
        return char_ctrl.getWalkDirection()

    def get_gravity(self):
        mechainfo = self.ev_g_mecha_config('PhysicConfig')
        if mechainfo:
            gravity = mechainfo['gravity'] * NEOX_UNIT_SCALE
        else:
            gravity = 40 * NEOX_UNIT_SCALE
        return gravity

    def on_reset_gravity(self):
        gravity = self.get_gravity()
        self.send_event('E_GRAVITY', gravity)

    def set_group(self, group):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.group = group

    def get_group(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.group

    def set_group_mask(self, group, mask):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.group = group
        char_ctrl.filter = mask

    def get_group_mask(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return (
         char_ctrl.group, char_ctrl.filter)

    def get_step_height(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.getStepHeight()

    def set_step_height(self, step_height):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setStepHeight(step_height)

    def reset_step_height(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setStepHeight(self.stepheight)

    def get_height(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.getHeight()

    def set_height(self, height):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setHeight(height)

    def get_radius(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.getRadius()

    def on_set_speed(self, speed):
        log_error('\xe4\xb8\xba\xe4\xbb\x80\xe4\xb9\x88\xe8\xa6\x81\xe7\x94\xa8E_SPEED\xef\xbc\x8cshare_data\xe4\xb8\x8d\xe9\xa6\x99\xe5\x90\x97')
        self.sd.ref_cur_speed = speed

    def on_get_speed(self):
        log_error('\xe4\xb8\xba\xe4\xbb\x80\xe4\xb9\x88\xe8\xa6\x81\xe7\x94\xa8G_SPEED\xef\xbc\x8cshare_data\xe4\xb8\x8d\xe9\xa6\x99\xe5\x90\x97')
        return self.sd.ref_cur_speed

    def change_jump_factor(self, flag, factor):
        if flag:
            self.jump_factor += factor
        else:
            self.jump_factor = 1.0

    def jump(self, jump_speed=None):
        jump_speed *= self.jump_factor
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        else:
            if jump_speed is not None:
                char_ctrl.setJumpSpeed(jump_speed)
            char_ctrl.jump()
            self.sd.ref_on_ground = False
            return

    def on_ground_callback(self, *args):
        if not self.is_valid():
            return
        self.sd.ref_on_ground = True
        self.send_event('E_ON_TOUCH_GROUND', *args)
        self.send_event('E_JUMP_STAGE', 0)

    def get_on_ground(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if not self.is_valid():
            return
        return char_ctrl.onGround()

    def get_move_dir(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        try:
            walk_dir = char_ctrl.getWalkDirection()
            if not walk_dir.is_zero:
                walk_dir.normalize()
            return walk_dir
        except:
            log_error('char_ctrl=%s is valid:%s', char_ctrl, char_ctrl.valid)

    def _get_move_info_from_rock_or_keyboard(self):
        rocker_ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if rocker_ui:
            rocker_ui.check_run_lock()
        ctrl_part = global_data.moveKeyboardMgr
        move_dir = None
        move_state = None
        if rocker_ui and (rocker_ui.is_run_lock or rocker_ui.is_rocker_enable):
            move_dir = rocker_ui.last_move_dir
            move_state = rocker_ui.last_move_state
        if game3d.get_platform() == game3d.PLATFORM_WIN32 and ctrl_part and ctrl_part.last_move_dir:
            if not move_dir or move_dir.length == 0:
                return (ctrl_part.last_move_dir, ctrl_part.last_move_state)
        return (move_dir, move_state)

    def get_all_state_desc(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return ''
        last_frame_time = 0
        if hasattr(char_ctrl, 'getLastFrameTime'):
            last_frame_time = char_ctrl.getLastFrameTime()
        seperate_direction = math3d.vector(0, 0, 0)
        if hasattr(char_ctrl, 'getLastFrameTime'):
            seperate_direction = char_ctrl.getSeperateDirection()
        scene_debug_info = ''
        scene_col = global_data.game_mgr.scene.scene_col
        if hasattr(scene_col, 'get_debug_info'):
            scene_debug_info = scene_col.get_debug_info()
        scene_debug_info = ''
        walk_direction = char_ctrl.getWalkDirection()
        model = self.ev_g_model()
        if model:
            world_yaw = model.world_rotation_matrix.yaw
            local_yaw = model.rotation_matrix.yaw
            state_desc = 'test--ComDriver.dump_character--isActive =' + str(char_ctrl.isActive()) + '--enableZCapsule =' + str(char_ctrl.enableZCapsule) + '--footPosition =' + str(char_ctrl.getFootPosition()) + '--physicalPosition =' + str(char_ctrl.physicalPosition) + '--model.position =' + str(model.position) + '--model.world_position =' + str(model.world_position) + '--position =' + str(char_ctrl.position) + '--walk_direction.length =' + str(walk_direction.length / NEOX_UNIT_SCALE) + '--last_frame_time =' + str(last_frame_time) + '--seperate_direction.length =' + str(seperate_direction.length) + '--walk_direction =' + str(walk_direction) + '--jumpSpeed =' + str(char_ctrl.getJumpSpeed() / NEOX_UNIT_SCALE) + '--verticalVelocity =' + str(char_ctrl.verticalVelocity / NEOX_UNIT_SCALE) + '--gravity =' + str(char_ctrl.getGravity() / NEOX_UNIT_SCALE) + '--getFallSpeed =' + str(char_ctrl.getFallSpeed() / NEOX_UNIT_SCALE) + '--onGround =' + str(char_ctrl.onGround()) + '--world_yaw =' + str(world_yaw) + '--local_yaw =' + str(local_yaw) + '--canJump =' + str(char_ctrl.canJump()) + '--speed =' + str(self.sd.ref_cur_speed / NEOX_UNIT_SCALE) + '--stepHeight =' + str(char_ctrl.getStepHeight()) + '--getXOffset =' + str(char_ctrl.getXOffset()) + '--getYOffset =' + str(char_ctrl.getYOffset()) + '--getRadius =' + str(char_ctrl.getRadius()) + '--max_slope =' + str(math.degrees(char_ctrl.getMaxSlope())) + '--speed_scale =' + str(self.ev_g_get_speed_scale()) + '--skin_width =' + str(char_ctrl.getSkinWidth()) + '---padding =' + str(char_ctrl.getPadding())
            return state_desc
        else:
            return ''

    def _change_character_attr(self, name, *arg):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        value = arg[0]
        char_ctrl = self.sd.ref_character
        if name == 'stepheight':
            value *= NEOX_UNIT_SCALE
            char_ctrl.setStepHeight(value)
        elif name == 'max_slope':
            char_ctrl.setMaxSlope(math.radians(value))
        elif name == 'padding':
            value *= NEOX_UNIT_SCALE
            char_ctrl.setPadding(value)
            self.character_down_height = collision_const.STAND_MODEL_OFFSET_Y + value
            char_ctrl.setYOffset(-self.character_down_height)
        elif name == 'added_margin':
            value *= NEOX_UNIT_SCALE
            char_ctrl.setAddedMargin(value)
        elif name == 'jump_speed':
            value *= NEOX_UNIT_SCALE
            char_ctrl.setJumpSpeed(value)
        elif name == 'max_fall_speed':
            value *= NEOX_UNIT_SCALE
            self.send_event('E_FALL_SPEED', value)
        elif name == 'gravity':
            value *= NEOX_UNIT_SCALE
            char_ctrl.setGravity(value * self.sd.ref_gravity_scale)
        elif name == 'reset_phys_attr':
            self.reset_phys_attr()
        elif name == 'debug_phys':
            scene = self.scene
            is_drawing = bool(value)
            scene.scene_col.drawing = is_drawing
            if is_drawing:
                scene.scene_col.drawing_center = self.ev_g_position()
                scene.scene_col.drawing_radius = 1000
        elif name == 'enable_log':
            char_ctrl.setIsLog(bool(value))
        elif name == 'gm_cmd':
            global_data.player.wiz_command(value, True)
        elif name == 'dump_character':
            print(self.get_all_state_desc())
            char_ctrl = self.sd.ref_character
            if char_ctrl and hasattr(char_ctrl, 'dump_info'):
                char_ctrl.dump_info()
        elif name == 'enable_pvd':
            import collision
            collision.set_pvd_enable(bool(value))
        elif name == 'open_debug_log':
            is_log = bool(value)
            print('test--open_debug_log--is_log =', is_log)
            char_ctrl.setIsOpenDebugLog(is_log)

    def on_trans_to_share(self):
        self.is_share = True

    def on_start_waiting_check(self):
        self.waiting_timer = global_data.game_mgr.register_logic_timer(self.waiting_process, 1)

    def waiting_process(self):
        cam_pos = self.scene.active_camera.position
        if self.scene.check_collision_loaded(cam_pos):
            self.send_event('E_FORCE_ACTIVE')
            self.clear_waiting_timer()

    def clear_waiting_timer(self):
        if self.waiting_timer:
            global_data.game_mgr.unregister_logic_timer(self.waiting_timer)
            self.waiting_timer = None
        return