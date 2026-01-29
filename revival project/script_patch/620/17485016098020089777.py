# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComCharacterBase.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const import collision_const
import math3d
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
from logic.gcommon.cdata import state_physic_arg
from logic.gcommon.cdata import jump_physic_config

class ComCharacterBase(UnitCom):
    BIND_EVENT = {'E_TELEPORT': '_teleport',
       'E_CHARACTER_WALK': '_set_walk_direction',
       'E_MOVE': '_character_move',
       'E_MOVE_STOP': '_character_move_stop',
       'G_ROTATION_MATRIX': '_get_rotation_matrix',
       'E_SET_YAW': '_set_yaw',
       'G_YAW': '_get_yaw',
       'G_IS_MOVE': '_is_move',
       'G_CTRL_DIR': '_get_ctrl_direction',
       'E_SET_POSITION': '_set_position',
       'E_ENABLE_FREE_CAMERA': 'on_enable_free_cam_mode',
       'G_IS_FREE_CAMERA': '_get_is_free_cam_mode',
       'G_CTRL_POSITION': '_get_ctrl_position',
       'G_IS_POS_INITED': '_is_pos_inited',
       'E_FOOT_POSITION': '_set_foot_position',
       'G_FOOT_POSITION': '_get_foot_position',
       'E_SET_JUMP_SPEED': '_set_jump_speed',
       'E_SET_GRAVITY': '_set_gravity',
       'E_RESET_GRAVITY': '_reset_gravity',
       'G_HUMAN_MOVE_DIR': '_get_human_dir',
       'G_ROCK_MOVE_DIR': '_get_rock_dir',
       'E_CHECK_CONTINUE_MOVE': '_check_continue_move',
       'G_CHARACTER_COLLISON_HEIGHT': '_get_collison_height',
       'E_RESIZE_DRIVER_CHARACTER': 'recreate',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'G_EASY_STATIC_TEST': 'easy_static_test'
       }

    def __init__(self):
        super(ComCharacterBase, self).__init__(False)
        self.post_timer = 0
        self.init_data()
        self.sd.ref_character = None
        self.init_tick_logic()
        return

    def _is_move(self):
        return self._ctrl_input_dir is not None

    def _get_ctrl_direction(self):
        return self._ctrl_input_dir

    def _get_ctrl_position(self):
        char_ctrl = self._get_character()
        if char_ctrl:
            return char_ctrl.position
        return math3d.vector(0, 0, 0)

    def _is_pos_inited(self):
        return bool(self.sd.ref_character)

    def init_tick_logic(self):
        tm = global_data.game_mgr.get_post_logic_timer()
        tm.unregister(self.post_timer)
        self.post_timer = tm.register(func=self.post_tick, interval=1, strict=True)

    def post_tick(self):
        dt = global_data.post_logic_real_dt or 0.033
        self.tick(dt)

    def init_data(self):
        self._spd = 5.0 * NEOX_UNIT_SCALE
        self._walk_direction = math3d.vector(0, 0, 0)
        self._pos_dirty = False
        self._rotation_dirty = False
        self._yaw = 0
        self._ctrl_input_dir = None
        self._ctrl_dir = None
        self._is_free_cam_mode = False
        global_data.emgr.net_reconnect_event += self.on_reconnect
        global_data.emgr.net_login_reconnect_event += self.on_reconnect
        return

    def destroy(self):
        tm = global_data.game_mgr.get_post_logic_timer()
        tm.unregister(self.post_timer)
        self.del_character()
        super(ComCharacterBase, self).destroy()

    def on_reconnect(self):
        self.init_tick_logic()

    def del_character(self):
        char_ctrl = self._get_character()
        if char_ctrl:
            self.reset_character_callabck()
            scene = self.scene
            scene.scene_col.remove_character(char_ctrl)
            self.sd.ref_character = None
        return

    def reset_character_callabck(self):
        char_ctrl = self.sd.ref_character
        char_ctrl.setPositionChangedCallback(None)
        return

    def init_character_callback(self):
        char_ctrl = self.sd.ref_character
        char_ctrl.setPositionChangedCallback(self.on_pos_change)
        char_ctrl.setOnFallCallback(self._on_fall, jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE)

    def on_pos_change(self, *args):
        self._pos_dirty = True

    def _set_position(self, position):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        position = math3d.vector(position)
        position.y -= char_ctrl.getYOffset()
        char_ctrl.physicalPosition = position
        self.on_pos_change()

    def tick_position(self):
        if self._pos_dirty:
            char_ctrl = self.sd.ref_character
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(char_ctrl.position)
            else:
                self.send_event('E_POSITION', char_ctrl.position)
            self._pos_dirty = False

    def tick_rotation(self):
        if self._rotation_dirty and not self.ev_g_is_celebrate():
            self._rotation_dirty = False
            if global_data.lobby_model_rotation:
                global_data.lobby_model_rotation = None
            rotation_matrix = math3d.matrix.make_rotation_y(self._yaw)
            self.send_event('E_SET_ROTATION_MATRIX', rotation_matrix)
        return

    def tick_filter(self):
        raise NotImplementedError

    def tick(self, dt):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        if not self.tick_filter():
            return
        self.tick_position()
        self.tick_rotation()

    def init_from_dict(self, unit_obj, bdict):
        super(ComCharacterBase, self).init_from_dict(unit_obj, bdict)
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        self._init_character(bdict)

    def on_init_complete(self):
        raise NotImplementedError

    def _get_speed_value(self):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return 0
        speed_dir = char_ctrl.getWalkDirection() + math3d.vector(0, char_ctrl.verticalVelocity, 0)
        return speed_dir.length

    def get_all_state_desc(self):
        char_ctrl = self.sd.ref_character
        walk_direction = char_ctrl.getWalkDirection()
        model = self.ev_g_model()
        world_yaw = model.world_rotation_matrix.yaw
        local_yaw = model.rotation_matrix.yaw
        state_desc = 'test--ComCharacterBase.dump_character--isActive =' + str(char_ctrl.isActive())
        normalize_walk_direction = math3d.vector(walk_direction)
        if not normalize_walk_direction.is_zero:
            normalize_walk_direction.normalize()
        state_desc += '--normalize_walk_direction =' + str(normalize_walk_direction) + '--footPosition =' + str(char_ctrl.getFootPosition()) + '--walk_direction.length =' + str(walk_direction.length / NEOX_UNIT_SCALE) + '--onGround =' + str(char_ctrl.onGround()) + '--physicalPosition =' + str(char_ctrl.physicalPosition) + '--verticalVelocity =' + str(char_ctrl.verticalVelocity / NEOX_UNIT_SCALE) + '--gravity =' + str(char_ctrl.getGravity() / NEOX_UNIT_SCALE) + '--walk_direction =' + str(walk_direction) + '--world_yaw =' + str(world_yaw) + '--local_yaw =' + str(local_yaw) + '--canJump =' + str(char_ctrl.canJump()) + '--jumpSpeed =' + str(char_ctrl.getJumpSpeed() / NEOX_UNIT_SCALE) + '--model.position =' + str(model.position) + '--model.world_position =' + str(model.world_position) + '--position =' + str(char_ctrl.position) + '--speed =' + str(self._get_speed_value()) + '--max_slope' + str(math.degrees(char_ctrl.getMaxSlope())) + '--stepHeight =' + str(char_ctrl.getStepHeight()) + '--getFallSpeed =' + str(self.get_fall_speed() / NEOX_UNIT_SCALE) + '--getXOffset =' + str(char_ctrl.getXOffset()) + '--getYOffset =' + str(char_ctrl.getYOffset()) + '--getRadius =' + str(char_ctrl.getRadius()) + '--max_slope =' + str(math.degrees(char_ctrl.getMaxSlope()))
        return state_desc

    def _change_character_attr(self, name, *arg):
        value = arg[0]
        char_ctrl = self.sd.ref_character
        if name == 'dump_character':
            print(self.get_all_state_desc())

    def _teleport(self, position):
        char_ctrl = self._get_character()
        if char_ctrl and position:
            char_ctrl.teleport(position)

    def get_fall_speed(self):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return 0
        return char_ctrl.getFallSpeed()

    def _get_character_logic_height(self, character, actual_height):
        return actual_height - character.getRadius() * 2.0 - character.getSkinWidth() * 2.0

    def init_prs(self):
        raise NotImplementedError(' error')

    def _init_character(self, bdict):
        self.del_character()
        width, height = CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT - 0.1
        stepheight = state_physic_arg.lobby_stepheight * NEOX_UNIT_SCALE
        max_slope = 70
        padding = 0.001
        added_margin = 0.02
        pos_interpolate = 0.5
        character = collision.Character(width, height, stepheight)
        self._collison_height = height
        character.setYOffset(-height * 0.5)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setSmoothFactor(pos_interpolate)
        character.enableLeaveOverlap(True)
        self.scene.scene_col.add_character(character)
        character_height = self._get_character_logic_height(character, height)
        character.setHeight(character_height)
        self.sd.ref_character = character
        character.filter = GROUP_CHARACTER_INCLUDE
        character.group = GROUP_CHARACTER_INCLUDE
        self.init_prs()
        self.init_character_callback()
        self.reset_phys_attr()
        self._rotation_dirty = True

    def _get_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl and char_ctrl.valid:
            return char_ctrl

    def easy_static_test(self):
        if not self.is_valid():
            return False
        scene = self.scene
        if not scene or not scene.valid:
            return False
        character = self._get_character()
        if not character:
            return False
        group = character.group
        mask = character.filter
        return character.staticTest(group, mask)

    def _on_fall(self):
        self.send_event('E_FALL')

    def _set_walk_direction(self, walk_direction):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        self._walk_direction = walk_direction
        char_ctrl.setWalkDirection(walk_direction)

    def _get_walk_direction(self):
        return math3d.vector(self._walk_direction)

    def _get_rotation_matrix(self):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return math3d.matrix()
        if self._is_free_cam_mode and not self.ev_g_is_celebrate():
            scene = self.scene
            cam = scene.active_camera
            return math3d.matrix.make_rotation_y(cam.world_rotation_matrix.yaw)
        return math3d.matrix.make_rotation_y(self._yaw)

    def _character_move(self, v):
        self._ctrl_input_dir = v
        if self.ev_g_is_jump():
            self.send_event('E_JUMP_MOVE', v)
            return
        if self.ev_g_is_climb():
            return
        if self.ev_g_is_camera_slerp():
            return
        v_dir = v * self._get_rotation_matrix()
        if self._is_free_cam_mode and not self.ev_g_is_celebrate():
            if self._yaw != v_dir.yaw:
                self._rotation_dirty = True
                self._yaw = v_dir.yaw
        self._ctrl_dir = v
        self._set_walk_direction(v_dir * self._spd)

    def _character_move_stop(self):
        self._ctrl_input_dir = None
        if self.ev_g_is_jump():
            return
        else:
            if self.ev_g_is_climb():
                return
            self._ctrl_dir = None
            self._set_walk_direction(math3d.vector(0, 0, 0))
            return

    def _check_continue_move(self):
        if self._ctrl_input_dir is not None:
            self._character_move(self._ctrl_input_dir)
        else:
            self._character_move_stop()
        return

    def _set_yaw(self, yaw):
        if not self._is_free_cam_mode:
            if self._yaw != yaw:
                self._rotation_dirty = True
            self._yaw = yaw
        if self._is_move():
            self._character_move(self._ctrl_input_dir)

    def _get_yaw(self):
        return self._yaw

    def on_enable_free_cam_mode(self, enable):
        self._rotation_dirty = True
        self._is_free_cam_mode = enable

    def _get_is_free_cam_mode(self):
        return self._is_free_cam_mode

    def _set_foot_position(self, pos):
        char_ctrl = self._get_character()
        if char_ctrl and pos:
            if getattr(char_ctrl, 'setFootPositionIgnoreTest', None):
                char_ctrl.setFootPositionIgnoreTest(pos)
            else:
                self._set_phys_pos_ignore_test(pos)
                char_ctrl.setFootPosition(pos)
        return

    def _set_phys_pos_ignore_test(self, position):
        char_ctrl = self._get_character()
        if char_ctrl and position:
            if hasattr(char_ctrl, 'setPhysicalPositionIgnoreTest'):
                char_ctrl.setPhysicalPositionIgnoreTest(position)
            else:
                char_ctrl.teleport(position)

    def _get_foot_position(self):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return math3d.vector(0, 0, 0)
        foot_position = char_ctrl.getFootPosition()
        return foot_position

    def _set_jump_speed(self, jump_speed):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        char_ctrl.setJumpSpeed(jump_speed)

    def _set_gravity(self, gravity):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        char_ctrl.setGravity(gravity * self.sd.ref_gravity_scale)

    def _reset_gravity(self, ignore_water=False):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        gravity = 0
        if ignore_water:
            from logic.gcommon.cdata import jump_physic_config
            gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        else:
            gravity = self._get_gravity()
        self.send_event('E_SET_GRAVITY', gravity)

    def _get_gravity(self):
        from logic.gcommon.cdata import jump_physic_config
        gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        return gravity

    def _get_human_dir(self):
        return math3d.vector(self._walk_direction)

    def _get_rock_dir(self):
        ctrl_dir = self._ctrl_dir if self._ctrl_dir is not None else math3d.vector(0, 0, 0)
        return ctrl_dir * self._spd

    def _get_collison_height(self):
        return self._collison_height

    def _recreate(self, width, height):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        import collision
        char_ctrl.setRadius(width)
        character_height = self._get_character_logic_height(char_ctrl, height)
        char_ctrl.setHeight(character_height)
        self._collison_height = height

    def recreate(self, width, height, align_type=collision_const.ALIGN_TYPE_NONE):
        char_ctrl = self._get_character()
        if not char_ctrl:
            return
        pos = char_ctrl.getFootPosition()
        old_collison_height = self._get_collison_height()
        self._recreate(width, height)
        self.reset_phys_attr()
        if align_type == collision_const.ALIGN_TYPE_DOWN:
            y_offset_ex = (collision_const.CHARACTER_STAND_HEIGHT - height) * 0.5
            char_ctrl.setYOffset(-self.character_down_height + y_offset_ex)
            self.send_event('E_FOOT_POSITION', pos)
        elif align_type == collision_const.ALIGN_TYPE_TOP:
            y_offset_ex = (collision_const.CHARACTER_STAND_HEIGHT - height) * 0.5
            char_ctrl.setYOffset(-self.character_down_height - y_offset_ex)
            if old_collison_height:
                pos = pos + math3d.vector(0, old_collison_height - height, 0)
                self.send_event('E_FOOT_POSITION', pos)
        else:
            char_ctrl.setYOffset(-self.character_down_height)
            self.send_event('E_FOOT_POSITION', pos)

    def reset_phys_attr(self):
        from logic.gcommon.cdata import state_physic_arg
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        from logic.gcommon.common_const import animation_const
        st = animation_const.STATE_STAND
        y_off = animation_const.get_y_offset(st, self.ev_g_role_id())
        self._shape_type = collision_const.SHAPE_TYPE_STAND
        self.character_down_height = y_off + padding
        if self._shape_type == collision_const.SHAPE_TYPE_STAND:
            self.character_offset_x = collision_const.STAND_MODEL_OFFSET_X
            self.character_down_height = collision_const.STAND_MODEL_OFFSET_Y
        elif self._shape_type == collision_const.SHAPE_TYPE_SQUAT:
            self.character_offset_x = collision_const.SQUAT_MODEL_OFFSET_X
            self.character_down_height = collision_const.SQUAT_MODEL_OFFSET_Y
        elif self._shape_type == collision_const.SHAPE_TYPE_CRAWL:
            self.character_offset_x = collision_const.DOWN_MODEL_OFFSET_X
            self.character_down_height = collision_const.DOWN_MODEL_OFFSET_Y
        self.character_down_height += padding
        char_ctrl = self._get_character()
        if char_ctrl:
            char_ctrl.setXOffset(-self.character_offset_x)
            char_ctrl.setYOffset(-self.character_down_height)