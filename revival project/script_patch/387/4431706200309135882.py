# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRatRobotDriver.py
from __future__ import absolute_import
import world
import math
import math3d
import weakref
import game3d
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from ..UnitCom import UnitCom
from ...cdata import jump_physic_config
import common.utils.timer as timer
from mobile.common.EntityManager import EntityManager
import random
import logic.gcommon.common_utils.bcast_utils as bcast
import world
from logic.entities import Avatar, Puppet
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp
from logic.gcommon.common_const import collision_const
import collision
from logic.gcommon.utility import dummy_cb
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
EXPLOSIVE_ROBOT_STATE_APPEAR = 0
EXPLOSIVE_ROBOT_STATE_MOVE = 1
EXPLOSIVE_ROBOT_STATE_JMUP = 2
EXPLOSIVE_ROBOT_STATE_DISABLE = 3
APPEAR_LAST_TIME = 1.3
SEARCH_RADIUS = 40 * NEOX_UNIT_SCALE
DOT_VALUE_TO_JUMP = 0.6
ROBOT_AIM_SOCKET_NAME = 'aim_start'
CHECK_JUMP_DISTANCE = 1.5

class ComRatRobotDriver(UnitCom):
    CHECK_JUMP_MIN_DISTANCE_SQR = (2.5 * NEOX_UNIT_SCALE) ** 2
    CHECK_LAST_JUMP_POS_DISTANCE_SQE = (0.5 * NEOX_UNIT_SCALE) ** 2
    CHECK_INTERVAL = 0.5
    SLOW_MODEL_POS_SCALE = 0.8
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_EXPLOSIVE_ROBOT_LOCK_TARGET': 'on_lock_target',
       'E_EXPLOSIVE_ROBOT_TIMEOUT': 'on_explosive',
       'G_IS_ENEMY': 'is_enemy'
       }

    def __init__(self):
        super(ComRatRobotDriver, self).__init__()
        self.sd.ref_is_robot = True
        self._pos_cache = None
        self._tick_func = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRatRobotDriver, self).init_from_dict(unit_obj, bdict)
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        master_id = bdict.get('master_id', None)
        if master_id:
            self._master = EntityManager.getentity(master_id)
            if self._master:
                self._master = self._master.logic
        else:
            self._master = None
        self.model = None
        self.need_update = True
        self._save_pos = None
        self._last_jump_pos = math3d.vector(0, 0, 0)
        self._check_jump_end = 0
        move_dir = bdict.get('forward_dir', None)
        if not move_dir:
            move_dir = [
             1, 0, 1]
        self._move_direction = math3d.vector(*move_dir)
        self.state = EXPLOSIVE_ROBOT_STATE_APPEAR
        robot_id = bdict.get('robot_no', 105611)
        self.robot_data = confmgr.get('explosive_robot_conf', str(robot_id))
        self.cur_speed = self.robot_data['walk'] * NEOX_UNIT_SCALE
        self.init_character()
        self.model = self.ev_g_model()
        if self.model:
            self.on_model_loaded(self.model)
        self._tick_func = self.tick_appear
        self.jump_check_countdown = 0.0
        self.explosion_countdown = bdict.get('life_time', 7)
        self.appear_countdown = 0.0
        self.cur_animate = None
        self._diff_pre = None
        self.upload_tick = 0.0
        self.old_upload_pos = None
        return

    def on_model_loaded(self, model):
        self.model = model
        self.set_physx_sync_lod(model)
        self.play_animation('transform')
        self.model.register_on_end_event(self.animate_callback, False)
        passenger = self.ev_g_passenger_info()
        scene = self.scene
        char_ctrl = self.sd.ref_character
        if char_ctrl and scene:
            scene = self.scene
            char_ctrl.activate(scene.scene_col)
            char_ctrl.group = char_ctrl.group | collision_const.GROUP_GRENADE
            self.send_event('E_FOOT_POSITION', model.position)
        mat = math3d.matrix.make_rotation_y(random.random() * 6.414)
        self.send_event('E_ROTATION', mat)

    def animate_callback(self, *args):
        self.play_animation('run', loop=1)

    def set_physx_sync_lod(self, model):
        from logic.gcommon.const import PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES
        char_ctrl = self.sd.ref_character
        if model and char_ctrl:
            char_ctrl.setRefModel(model)
            char_ctrl.setSyncLodDist(PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES)

    def on_pos_changed(self, pos, *arg):
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)

    def on_rotation_changed(self):
        char_ctrl = self.sd.ref_character
        self.send_event('E_SYNC_MODEL_ROTATION_TO_COL', char_ctrl.getSlope())

    def init_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl is None:
            return
        else:
            char_ctrl.setPositionChangedCallback(self._on_pos_changed)
            char_ctrl.setRotationChangedCallback(self._on_rotation_changed)
            char_ctrl.setOnFallCallback(self._on_fall, jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE)
            self.reset_phys_attr()
            return

    def uninit_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setPositionChangedCallback(None)
            char_ctrl.setRotationChangedCallback(None)
            char_ctrl.setOnFallCallback(None, 0.0)
        return

    def reset_phys_attr(self):
        from ...cdata import state_physic_arg
        stepheight = 0.3 * NEOX_UNIT_SCALE
        max_slope = 75
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        added_margin = state_physic_arg.added_margin * NEOX_UNIT_SCALE
        pos_interpolate = state_physic_arg.pos_interpolate
        self._jump_speed = self.robot_data['jump_speed'] * NEOX_UNIT_SCALE
        gravity = self.robot_data['gravity'] * NEOX_UNIT_SCALE
        fall_speed = 50 * NEOX_UNIT_SCALE
        self.y_off = 0.8 * NEOX_UNIT_SCALE
        self.x_off = 0
        character = self.sd.ref_character
        character.setStepHeight(stepheight)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setJumpSpeed(self._jump_speed)
        character.setFallSpeed(fall_speed)
        character.setGravity(gravity * self.sd.ref_gravity_scale)
        character.setXOffset(-self.x_off)
        character.setYOffset(-self.y_off)
        character.setSmoothFactor(pos_interpolate)
        character.enableFollow = False
        character.mask = character.mask & ~collision_const.GROUP_MECHA_BALL
        self.char_size = (
         0.5 * NEOX_UNIT_SCALE, 1.6 * NEOX_UNIT_SCALE)
        self.send_event('E_RECREATE_CHARACTER', self.char_size[0], self.char_size[1], 0.6)

    def on_rotate_by_dir(self, forward):
        forward = math3d.vector(forward)
        forward.y = 0
        rot = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
        self.model.rotation_matrix = rot
        model_rot = math3d.matrix_to_rotation(rot)
        char_ctrl = self.sd.ref_character
        char_ctrl.setCharacterDirection(model_rot)
        self.send_event('E_ACTION_SYNC_FORCE_YAW', rot.yaw)

    def recreate(self, width, height):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        pos = char_ctrl.getFootPosition()
        stepheight = char_ctrl.getStepHeight()
        self.send_event('E_RECREATE_CHARACTER', width, height, stepheight)
        self.init_character()
        char_ctrl.setXOffset(-self.x_off)
        char_ctrl.setYOffset(-self.y_off)

    def _on_fall(self):
        pass

    def _on_pos_changed(self, pos, *arg):
        old_model_position = self._pos_cache
        char_ctrl = self.sd.ref_character
        if char_ctrl.verticalVelocity < 0 and old_model_position:
            pos_y = old_model_position.y + self.SLOW_MODEL_POS_SCALE * (pos.y - old_model_position.y)
            pos.y = pos_y
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)
        self._pos_cache = pos

    def _on_rotation_changed(self):
        pass

    def _move_toward(self, move_dir, force_update=False):
        self._move_direction = move_dir
        self.send_event('E_ACTION_MOVE', move_dir)
        speed = self.cur_speed
        move_dir *= speed
        self.send_event('E_ACTION_SYNC_DIR', move_dir)
        self.set_walk_direction(move_dir)
        mat = math3d.matrix.make_rotation_between(math3d.vector(0, 0, 1), math3d.vector(move_dir.x, 0, move_dir.z))
        self.send_event('E_ROTATION', mat)

    def set_walk_direction(self, move_dir):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        self.send_event('E_CHARACTER_WALK', move_dir)

    def tick(self, dt):
        self.explosion_countdown -= dt
        if self.explosion_countdown <= 0.0:
            self_pos = self._pos_cache
            self.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_explode', ((self_pos.x, self_pos.y, self_pos.z),), True)
            self.on_explosive(False)
            self.state = EXPLOSIVE_ROBOT_STATE_DISABLE
            self._tick_func = self.tick_none
            return
        if self._tick_func:
            self._tick_func(dt)
        self.upload_pos(dt)

    def tick_appear(self, dt):
        self.appear_countdown += dt
        if self.appear_countdown > APPEAR_LAST_TIME:
            self._on_ground()

    def tick_move(self, dt):
        self._move_toward(self._move_direction)
        if not self.model:
            return
        mat = self.model.get_socket_matrix(ROBOT_AIM_SOCKET_NAME, world.SPACE_TYPE_WORLD)
        pos = mat.translation
        self._move_direction.y = 0.0
        self._move_direction.normalize()
        result = self.scene.scene_col.hit_by_ray(pos, pos + self._move_direction * CHECK_JUMP_DISTANCE * NEOX_UNIT_SCALE, 0, collision_const.GROUP_STATIC_SHOOTUNIT, collision_const.GROUP_STATIC_SHOOTUNIT, collision.INCLUDE_FILTER, False)
        if result[0]:
            self.set_jump()
            return
        self.jump_check_countdown += dt
        if self.jump_check_countdown > self.CHECK_INTERVAL:
            self.jump_check_countdown -= self.CHECK_INTERVAL
            char_ctrl = self.sd.ref_character
            cur_pos = char_ctrl.position
            if self._save_pos and cur_pos:
                if (self._save_pos - cur_pos).length_sqr < self.CHECK_JUMP_MIN_DISTANCE_SQR and (self._last_jump_pos - cur_pos).length_sqr > self.CHECK_LAST_JUMP_POS_DISTANCE_SQE or self._check_dir_to_jump(cur_pos - self._save_pos):
                    self._last_jump_pos = cur_pos
                    self.set_jump()
            self._save_pos = cur_pos

    def tick_jump(self, dt):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            if char_ctrl.verticalVelocity == 0.0:
                self._check_jump_end += 1
                if self._check_jump_end > 4:
                    self._on_ground()
            else:
                self._check_jump_end = 0

    def tick_none(self, dt):
        pass

    def set_jump(self):
        self.state = EXPLOSIVE_ROBOT_STATE_JMUP
        self._vert_zero_speed_time = 0.0
        self._tick_func = self.tick_jump
        char_ctrl = self.sd.ref_character
        char_ctrl.verticalVelocity = self._jump_speed
        char_ctrl.setOnTouchGroundCallback(self._on_ground)
        self.play_animation('attack')

    def _check_dir_to_jump(self, diff):
        pos_dir = math3d.vector(diff.x, 0, diff.z)
        if pos_dir.is_zero:
            return False
        if not self._diff_pre:
            self._diff_pre = pos_dir
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

    def _on_ground(self, *args):
        self.state = EXPLOSIVE_ROBOT_STATE_MOVE
        self._tick_func = self.tick_move
        self.play_animation('run', loop=1)

    def explosion(self):
        self._explosion_timer = None
        return

    def _move_stop(self, force_stop=False):
        self.send_event('E_ACTION_SYNC_STOP')
        self.send_event('E_ACTION_MOVE_STOP')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_MOVE_STOP, ()], False)
        self.set_walk_direction(math3d.vector(0, 0, 0))

    def play_animation(self, anim, transit_time=-1.0, transit_type=0, init_time=0, loop=2):
        if self.cur_animate == anim:
            return
        if self.model and self.model.valid:
            self.model.play_animation(anim, transit_time, transit_type, init_time, loop)
            self.cur_animate = anim

    def on_explosive(self, is_time_out=True):
        if self.state != EXPLOSIVE_ROBOT_STATE_DISABLE and self.model and self.model.valid:
            self.state = EXPLOSIVE_ROBOT_STATE_DISABLE
            if is_time_out:
                sfx = self.robot_data['sfx']
                scale = self.robot_data['sfx_scale']
            else:
                sfx = self.robot_data['death_sfx']
                scale = self.robot_data['death_sfx_scale']
            scale = math3d.vector(scale, scale, scale)

            def create_cb(sfx):
                sfx.scale = scale

            global_data.sfx_mgr.create_sfx_in_scene(sfx, self.model.position, duration=0.5, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            global_data.sound_mgr.play_sound_optimize('Play_grenade', self.unit_obj, self.model.position, ('grenade', self.robot_data['explosive_sound']))
            self.model.visible = False

    def upload_pos(self, dt):
        if self._master == global_data.cam_lctarget:
            self.upload_tick -= dt
            if self.upload_tick < 0.0:
                self.upload_tick = 0.2
                model_position = self._pos_cache
                if model_position and model_position != self.old_upload_pos:
                    self.old_upload_pos = model_position
                    self.send_event('E_CALL_SYNC_METHOD', 'update_explosive_robot_position', (global_data.player.id, v3d_to_tp(model_position)), True)

    def is_enemy(self):
        if self._master and global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_campmate(self._master.ev_g_camp_id()):
            return True
        return False

    def destroy(self):
        self.uninit_character()
        self._tick_func = dummy_cb
        super(ComRatRobotDriver, self).destroy()