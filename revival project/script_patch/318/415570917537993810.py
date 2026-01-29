# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanDriver.py
from __future__ import absolute_import
from __future__ import print_function
from ..UnitCom import UnitCom
import math3d
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_utils.parachute_utils import is_flying
import logic.gcommon.common_const.collision_const as collision_const
import time
from ..component_const import MAX_ITVL_TICK_SYNC
import math
from logic.gcommon.cdata import status_config
import world
import game3d
import collision
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE, STAGE_LAUNCH_PREPARE
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.const import MOVE_TO_MODE_NONE, MOVE_TO_MODE_ALWAYS_FORWARD, MOVE_TO_MODE_ALWAYS_FORWARD_WITH_CAM
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.units.LAvatar import LAvatar
from logic.client.const import game_mode_const
import common.utils.timer as timer
import logic.gcommon.common_const.water_const as water_const
from ...cdata import speed_physic_arg
from ...cdata import jump_physic_config
from logic.gutils import character_action_utils
from logic.gcommon import editor

@editor.com_exporter('\xe7\x89\xa9\xe7\x90\x86\xe7\xbb\x84\xe4\xbb\xb6', {('cur_speed', 'float'): {'zh_name': '\xe9\x80\x9f\xe5\xba\xa6(m/s)','getter': lambda self: self.sd.ref_character and self.sd.ref_character.getWalkDirection().length / NEOX_UNIT_SCALE
                            },
   ('vertical_speed', 'float'): {'zh_name': '\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6(m/s)','getter': lambda self: self.sd.ref_character and self.sd.ref_character.verticalVelocity / NEOX_UNIT_SCALE
                                 }
   })
class ComHumanDriver(UnitCom):
    SLOW_MODEL_POS_SCALE = 0.8
    POSITION_DIS_EPSILON = 1.0
    MASK_COLLISION = 0
    SLOPE_WALK = 1.0
    IK_CHANGE_STATE = (
     status_config.ST_SKATE_MOVE, status_config.ST_SKATE_BRAKE)
    YAW_INTERPOLATION = 0.15
    BIND_EVENT = {'E_ACTIVE_DRIVER': 'on_active_driver',
       'E_DISABLE_DRIVER': 'on_disable_driver',
       'E_MOVE': 'on_move',
       'G_MOVE_DIR': 'get_move_dir',
       'E_STEP_HEIGHT': 'set_step_height',
       'G_STEP_HEIGHT': 'get_step_height',
       'G_PHYSIC_SPEED': '_get_speed_value',
       'E_MOVE_TO': '_move_to',
       'E_AI_MOVE_TO': '_ai_move_to',
       'E_STOP_MOVE_TO': '_clear_move',
       'E_CLEAR_SPEED': 'on_stop',
       'E_MOVE_STOP': 'on_stop',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_START_PARACHUTE': ('_start_parachute_stage', -1),
       'E_CTRL_PARACHUTE_END': '_end_parachute_free_drop',
       'E_PLANE': '_start_fly_stage',
       'G_CAN_DOWN': 'can_down',
       'G_CAN_STAND': 'can_stand',
       'E_CTRL_USE_DRUG': '_on_ctrl_use_drug',
       'E_STAND': 'on_change_posture_stand',
       'E_SQUAT': 'on_change_posture_squat',
       'E_SWIM': 'on_change_posture_swim',
       'E_GROUND': 'on_change_posture_crawl',
       'E_DEATH': '_on_dead',
       'E_DEFEATED': '_on_defeated',
       'E_REVIVE': ('_on_revive', -1),
       'E_JUMP': 'jump',
       'E_ON_CONTROL_TARGET_CHANGE': '_on_control_target_change',
       'G_GROUND_SLOPE': '_get_ground_slope',
       'G_TARGET_POS': '_get_target_pos',
       'G_TARGET_DIR': '_get_target_dir',
       'E_HUMAN_MODEL_LOADED': '_on_model_loaded',
       'E_DRAW_LINE': 'draw_line',
       'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_OPEN_PARACHUTE': '_open_parachute',
       'G_CAM_YAW': '_get_cam_yaw',
       'E_MOVE_ENABLE': '_enable_move',
       'E_WATER_EVENT': '_handle_water_event',
       'G_MODEL_HEIGHT': '_get_model_height',
       'E_HIT_BY_FORCE': '_hit_by_force',
       'E_END_PARACHUTING': '_on_parachuting_finish',
       'E_AGONY': 'on_agony',
       'E_RESIZE_DRIVER_CHARACTER': 'recreate',
       'E_SET_WALK_DIRECTION': 'set_walk_direction',
       'G_GET_WALK_DIRECTION': 'get_walk_direction',
       'E_SPEED': 'on_set_speed',
       'G_SPEED': 'on_get_speed',
       'E_ROTATE': 'on_rotate',
       'E_PITCH': 'on_pitch',
       'G_SPEED_METER_PER_SECOND': '_get_speed_meter_per_second',
       'E_SWITCH_CAMERA_STATE': 'on_camera_state_switched',
       'E_RESET_GRAVITY': 'on_reset_gravity',
       'E_MOVE_TO_WATER_SURFACE': 'move_to_water_surface',
       'E_DISABLE_MOVE': 'disable_rocker_move',
       'E_SET_MAX_SLOPE': 'set_max_slope',
       'E_IGNORE_CHECK_GRAVITY': 'set_ignore_check_gravity',
       'E_SUCCESS_SAVED': 'reset_fall_speed',
       'G_ALL_PHYSX_STATE_DESC': 'get_all_state_desc',
       'E_SET_YAW': '_on_set_yaw',
       'G_ON_GROUND': 'get_on_ground',
       'E_JUMP_ON_TOP': 'set_jump_on_top_callback',
       'E_DEBUG_SPEED': '_debug_speed',
       'E_SET_FALL_CALLBACK': 'initFallCallback',
       'E_TEST_AIM_POS': 'test_aim_pos'
       }

    def __init__(self):
        super(ComHumanDriver, self).__init__(need_update=False)
        self.sd.ref_cur_speed = 0.0
        self._smooth_pos = None
        self._to_pos = None
        self._to_pos_dir = None
        self._can_move = True
        self._always_forward = 0
        self._is_die = False
        self._follow_speed = 0
        self._cur_slope = 0
        self._t_change_slope = 0
        self._draw_obj_list = []
        self._parachuting = False
        self._shape_type = collision_const.SHAPE_TYPE_STAND
        self.is_avatar = False
        self.last_water_status = water_const.WATER_NONE
        self._hited_timer = None
        self._disable_rocker_move = False
        self._to_yaw = None
        self._skate_water_timer_id = None
        self._ignore_check_gravity = False
        self._yaw_cache = 0
        self._yaw_mat = math3d.matrix()
        self.character_offset_x = 0
        self.character_down_height = 0
        return

    def destroy(self):
        self._clear_draw_obj()
        self._uninit_character()
        self._clear_move()
        if self._hited_timer:
            global_data.game_mgr.unregister_logic_timer(self._hited_timer)
            self._hited_timer = None
        super(ComHumanDriver, self).destroy()
        return

    def _debug_speed(self):
        walk_direction = self.get_walk_direction()
        yaw = abs(walk_direction.yaw)
        print(('test--_debug_speed--yaw = ', math.degrees(abs(walk_direction.yaw)), '--speed =',
         self._get_speed_meter_per_second()))

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanDriver, self).init_from_dict(unit_obj, bdict)
        self._init_character()
        self._init_phys(bdict)
        self._init_event()
        self._init_position(bdict)

    def on_init_complete(self):
        is_avatar = isinstance(self.unit_obj, LAvatar)
        if is_avatar:
            self.is_avatar = True
        else:
            self.is_avatar = False
        self.refresh_col_state()

    def on_active_driver(self):
        scene = self.scene
        if not scene:
            return
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.activate(scene.scene_col)
        self.send_event('E_GRAVITY', jump_physic_config.gravity * NEOX_UNIT_SCALE)
        pos = self.ev_g_position()
        char_ctrl.teleport(pos)

    def on_disable_driver(self):
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.deactivate(self.scene.scene_col)

    def refresh_col_state(self):
        st = self.ev_g_attr_get('human_state')
        if st in animation_const.MP_STATUS_2_EVENT:
            self.send_event(animation_const.MP_STATUS_2_EVENT[st])

    def _on_model_loaded(self, *args):
        self.refresh_col_state()
        self._set_physx_sync_lod()

    def _init_phys(self, *args):
        self.reset_phys_attr()
        self._set_physx_sync_lod()

    def _set_physx_sync_lod(self):
        from logic.gcommon.const import PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES
        model = self.ev_g_model()
        char_ctrl = self.sd.ref_character
        if model and char_ctrl:
            char_ctrl.setRefModel(model)
            char_ctrl.setSyncLodDist(PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES)

    def _init_position(self, bdict):
        if 'parachute_position' in bdict:
            pos = bdict.get('parachute_position', (0, 0, 0))
        elif 'position' in bdict:
            pos = bdict.get('position', (0, 0, 0))
        else:
            pos = (0, 0, 0)
        if 'parachute_stage' in bdict and bdict['parachute_stage'] == STAGE_LAUNCH_PREPARE:
            pos = bdict['launch_data'][0]
        new_pos = math3d.vector(pos[0], pos[1], pos[2])
        self.send_event('E_FOOT_POSITION', new_pos)

    def reset(self):
        self._to_pos = None
        self._to_pos_dir = None
        self.on_stop()
        if self.is_avatar:
            global_data.emgr.avatar_reset_state_event.emit()
        return

    def reset_phys_attr(self):
        parachute_stage = self.sd.ref_parachute_stage
        if is_flying(parachute_stage):
            self._start_fly_stage()
            return
        self.init_phys_attr()

    def init_phys_attr(self):
        from ...cdata import state_physic_arg
        stepheight = state_physic_arg.stepheight * NEOX_UNIT_SCALE
        max_slope = state_physic_arg.max_slope
        if global_data.game_mode.is_mode_type(game_mode_const.TDM_MaxSlop):
            max_slope = state_physic_arg.max_slope_death
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        pos_interpolate = state_physic_arg.pos_interpolate
        jump_speed = jump_physic_config.jump_speed * NEOX_UNIT_SCALE
        gravity = self._get_gravity()
        fall_speed = jump_physic_config.max_fall_speed * NEOX_UNIT_SCALE
        st = self.ev_g_attr_get('human_state')
        y_off = animation_const.get_y_offset(st, self.ev_g_role_id())
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
        character = self.sd.ref_character
        character.setStepHeight(stepheight)
        character.setPadding(-padding * 10)
        character.setAddedMargin(-padding * 10)
        character.setMaxSlope(math.radians(max_slope))
        character.setJumpSpeed(jump_speed)
        self.send_event('E_FALL_SPEED', fall_speed)
        self.send_event('E_GRAVITY', gravity)
        character.setXOffset(-self.character_offset_x)
        character.setYOffset(-self.character_down_height)
        character.setSmoothFactor(pos_interpolate)
        character.enableFollow = False
        if getattr(character, 'setMaxPushDist', None):
            character.setMaxPushDist(1.3 * NEOX_UNIT_SCALE)
        return

    def _get_gravity(self):
        water_status = self.sd.ref_water_status
        gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        if water_status != water_const.WATER_NONE:
            if self.ev_g_get_state(status_config.ST_SKATE):
                gravity = 0
            elif water_status == water_const.WATER_DEEP_LEVEL:
                gravity = 0
            if self.ev_g_get_state(status_config.ST_DOWN):
                gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        return gravity

    def on_reset_gravity(self, ignore_water=False):
        character = self.sd.ref_character
        if not character:
            return
        gravity = 0
        if ignore_water:
            gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        else:
            gravity = self._get_gravity()
        self.send_event('E_GRAVITY', gravity)

    def _on_control_target_change(self, target_id, position, *args):
        if self.unit_obj.id == target_id:
            self._init_character()
        else:
            self._uninit_character()

    def _uninit_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setPositionChangedCallback(None)
            char_ctrl.setRotationChangedCallback(None)
            char_ctrl.setOnTouchGroundCallback(None)
            char_ctrl.setOnFallCallback(None, 0.0)
        return

    def _init_character(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setPositionChangedCallback(self.on_pos_changed)
        self.initFallCallback()
        char_ctrl.setOnTouchGroundCallback(lambda *args: global_data.game_mgr.next_exec(self.on_ground_callback, *args))
        self.reset_phys_attr()

    def initFallCallback(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        fall_speed_to_jump = self.ev_g_fall_speed_to_jump()
        char_ctrl.setOnFallCallback(lambda : global_data.game_mgr.next_exec(self._on_fall), fall_speed_to_jump)

    def _get_model_height(self):
        model = self.ev_g_model()
        return model.bounding_box.y * 2

    def _init_event(self):
        emgr = global_data.emgr
        events = {}
        emgr.bind_events(events)

    def _start_parachute_stage(self, start_pos, end_pos, *args):
        self._parachuting = True
        pos = math3d.vector(*start_pos)
        self.send_event('E_FOOT_POSITION', pos)
        self.send_event('E_SET_JUMP_SPEED', 0)
        self.notify_pos_change(pos)

    def _open_parachute(self, *args):
        self._parachuting = True

    def _start_fly_stage(self, *args):
        char_ctrl = self.sd.ref_character
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_SET_JUMP_SPEED', 0)
        self.send_event('E_FALL_SPEED', 0)

    def _end_parachute_free_drop(self):
        if not self._parachuting:
            return
        self._parachuting = False
        self.reset_phys_attr()

    def _on_revive(self, *arg):
        self._is_die = False
        self.set_walk_direction(math3d.vector(0, 0, 0))
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.verticalVelocity = 0
        self.init_phys_attr()

    def _on_defeated(self, *arg):
        self._is_die = True

    def _on_dead(self, *arg):
        self._is_die = True
        self.on_change_posture_stand()

    def _handle_water_event(self, water_status, water_height=None):
        if self.ev_g_get_state(status_config.ST_ROLL):
            self.send_event('E_WAIT_FINISH_ROLL_EVENT', ('E_WATER_EVENT', (water_status, water_height)))
            return
        else:
            if self.ev_g_get_state(status_config.ST_RUSH):
                return
            char_ctrl = self.sd.ref_character
            if not char_ctrl:
                return
            self.send_event('E_CHANGE_WATER_INFO', water_height, water_status)
            fall_speed = char_ctrl.verticalVelocity
            if self.ev_g_get_state(status_config.ST_JUMP_3):
                fall_speed = char_ctrl.getTouchGroundVelocity()
            if water_status != water_const.WATER_NONE:
                if self.ev_g_is_avatar() and self.ev_g_get_state(status_config.ST_SKATE) and not self._skate_water_timer_id:
                    self._skate_water_timer_id = global_data.game_mgr.register_logic_timer(self.check_skate_on_water_tick, 1, times=-1, mode=timer.CLOCK)
            elif not self.ev_g_is_in_water_area():
                if self._skate_water_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self._skate_water_timer_id)
                    self._skate_water_timer_id = None
            if water_status != water_const.WATER_NONE:
                if self.ev_g_is_jump():
                    if fall_speed <= speed_physic_arg.fall_speed_threshold:
                        res_path = 'effect/fx/water/luoshui.sfx'
                        self.send_event('E_PLAY_WATER_EFFECT_BY_PATH', res_path)
            if water_status != self.last_water_status:
                if self.last_water_status == water_const.WATER_NONE:
                    if self.ev_g_get_state(status_config.ST_SKATE):
                        current_posture_state = self.ev_g_anim_state()
                        if current_posture_state != animation_const.STATE_SKATE:
                            self.send_event('E_SWITCH_STATUS', animation_const.STATE_SKATE)
                        self.move_to_water_surface()
                elif water_status == water_const.WATER_NONE:
                    if self.ev_g_get_state(status_config.ST_SKATE) and not self.ev_g_is_in_water_area() and not self.ev_g_is_jump():
                        self.on_reset_gravity()
                        self.send_event('E_UNLIMIT_LOWER_HEIGHT')
            if water_status == water_const.WATER_DEEP_LEVEL:
                self.send_event('E_START_SWIM', water_height)
            elif self.last_water_status == water_const.WATER_DEEP_LEVEL:
                self.send_event('E_STOP_SWIM')
            if water_status >= water_const.WATER_MID_LEVEL:
                if self.ev_g_get_state(status_config.ST_CROUCH):
                    self.send_event('E_CTRL_STAND')
            self.last_water_status = water_status
            self.send_event('E_CHANGE_SPEED')
            self.send_event('E_ACTION_CHECK_POS', True)
            return

    def move_to_water_surface(self, *args):
        water_height = self.ev_g_cur_water_height()
        water_status = self.sd.ref_water_status
        if water_status == water_const.WATER_NONE:
            return
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        is_jump = self.ev_g_is_jump()
        self.send_event('E_CANCEL_JUMP')
        position = char_ctrl.position
        is_up_water = position.y > water_height
        old_height = position.y
        position.y = water_height
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_GRAVITY', 0)
        low_height = water_height - char_ctrl.getYOffset()
        if not is_jump:
            self.send_event('E_TELEPORT', position)
            if char_ctrl.isFalling():
                char_ctrl.reset()
        self.send_event('E_LIMIT_LOWER_HEIGHT', low_height)
        if old_height < water_height:
            new_position = math3d.vector(position.x, water_height, position.z)
            self.send_event('E_TELEPORT', new_position)
        if global_data.player:
            global_data.player.logic.send_event('E_GUIDE_MOVE_TO_WATER_SURFACE')

    def check_skate_on_water_tick(self):
        if not self.is_valid():
            self._skate_water_timer_id = None
            return timer.RELEASE
        else:
            if not self.ev_g_get_state(status_config.ST_SKATE):
                self._skate_water_timer_id = None
                return timer.RELEASE
            if not self.ev_g_is_in_water_area():
                self._skate_water_timer_id = None
                return timer.RELEASE
            character = self.sd.ref_character
            if not character or not character.isActive():
                return
            if self.ev_g_is_jump():
                return
            physicalPosition = character.physicalPosition
            water_height = self.ev_g_cur_water_height()
            diff_offset_y = abs(physicalPosition.y - water_height)
            threshold_value = 2 + abs(character.getYOffset())
            char_ctrl = self.sd.ref_character
            if diff_offset_y > threshold_value:
                physicalPosition.y = water_height
                col_model_obj_list = []
                chect_begin = character.physicalPosition
                check_end = physicalPosition
                group = collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.WATER_GROUP
                mask = char_ctrl.mask
                self.ev_g_hit_by_scene_collision(chect_begin, check_end, group, mask, is_multi_select=False, col_model_obj_list=col_model_obj_list)
                col_object = None
                if col_model_obj_list:
                    col_object = col_model_obj_list[0]
                is_water = False
                if col_object:
                    is_water = col_object.group == collision_const.WATER_GROUP and col_object.mask == collision_const.WATER_MASK
                if not is_water:
                    return
                is_pos_valid = self.ev_g_is_pos_valid(physicalPosition)
                if is_pos_valid:
                    self.send_event('E_TELEPORT', physicalPosition)
            return

    def on_agony(self):
        gravity = self.ev_g_gravity()
        if gravity == 0:
            self.on_reset_gravity()

    def recreate(self, width, height, align_type=collision_const.ALIGN_TYPE_NONE):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        pos = char_ctrl.getFootPosition()
        old_collison_height = self.ev_g_character_collison_height()
        stepheight = char_ctrl.getStepHeight()
        self.send_event('E_RECREATE_CHARACTER', width, height, stepheight)
        self._init_character()
        if self.character_offset_x:
            char_ctrl.setXOffset(-self.character_offset_x)
        if not self.ev_g_get_state(status_config.ST_ROLL):
            yaw = self.ev_g_yaw()
            self._on_set_yaw(yaw)
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
        if self.ev_g_get_state(status_config.ST_SKATE):
            character_offset_x = collision_const.STAND_MODEL_OFFSET_X
            character_down_height = collision_const.STAND_MODEL_OFFSET_Y + char_ctrl.getPadding()
            char_ctrl.setXOffset(-character_offset_x)
            char_ctrl.setYOffset(-character_down_height)

    def _on_set_yaw(self, yaw, force_change_spd=True):
        if yaw is None:
            return
        else:
            self.send_event('E_ACTION_SET_YAW', yaw)
            return

    def set_jump_on_top_callback(self, callback):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setOnJumpOnTopCallback(callback)

    def get_on_ground(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.onGround()

    def jump(self, jump_speed=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        else:
            if jump_speed is not None:
                self.send_event('E_SET_JUMP_SPEED', jump_speed)
            char_ctrl.jump()
            self.on_change_posture_stand()
            return

    def on_change_posture_stand(self, *args):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_death():
            return
        if self._shape_type == collision_const.SHAPE_TYPE_STAND:
            return
        width = collision_const.CHARACTER_STAND_WIDTH
        height = collision_const.CHARACTER_STAND_HEIGHT
        self._shape_type = collision_const.SHAPE_TYPE_STAND
        self.character_down_height = collision_const.STAND_MODEL_OFFSET_Y + char_ctrl.getPadding()
        self.character_offset_x = collision_const.STAND_MODEL_OFFSET_X
        self.recreate(width, height)
        char_ctrl.enableZCapsule = False

    def on_change_posture_squat(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_death():
            return
        if self._shape_type == collision_const.SHAPE_TYPE_SQUAT:
            return
        width = collision_const.CHARACTER_SQUAT_WIDTH
        height = collision_const.CHARACTER_SQUAT_HEIGHT
        self._shape_type = collision_const.SHAPE_TYPE_SQUAT
        self.character_down_height = collision_const.SQUAT_MODEL_OFFSET_Y + char_ctrl.getPadding()
        self.character_offset_x = collision_const.SQUAT_MODEL_OFFSET_X
        self.recreate(width, height)
        char_ctrl.enableZCapsule = False

    def on_change_posture_swim(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_death():
            return
        if self._shape_type == collision_const.SHAPE_TYPE_SWIM:
            return
        width = collision_const.CHARACTER_STAND_WIDTH
        height = collision_const.CHARACTER_STAND_HEIGHT
        self._shape_type = collision_const.SHAPE_TYPE_SWIM
        anim_state = self.ev_g_anim_state()
        y_off = animation_const.get_y_offset(anim_state, self.ev_g_role_id())
        self.character_down_height = y_off + char_ctrl.getPadding()
        self.character_offset_x = collision_const.STAND_MODEL_OFFSET_X
        self.recreate(width, height)
        char_ctrl.enableZCapsule = False

    def on_change_posture_crawl(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_death():
            return
        if self._shape_type == collision_const.SHAPE_TYPE_CRAWL:
            return
        width, height = collision_const.CHARACTER_DOWN_WIDTH, collision_const.CHARACTER_DOWN_HEIGHT
        self._shape_type = collision_const.SHAPE_TYPE_CRAWL
        self.character_down_height = collision_const.DOWN_MODEL_OFFSET_Y + char_ctrl.getPadding()
        self.character_offset_x = collision_const.DOWN_MODEL_OFFSET_X
        self.recreate(width, height)
        char_ctrl.enableZCapsule = True

    def can_down(self):
        forward_dir = self.ev_g_model_forward()
        if not forward_dir or forward_dir.is_zero:
            return False
        scene = self.scene
        start = self._get_pos()
        start.y += collision_const.CHARACTER_STAND_HEIGHT * 0.5
        forward_len = collision_const.CHARACTER_STAND_HEIGHT * 0.5
        forward_dir.normalize()
        forward_dir_dist = forward_dir * forward_len
        end = start + forward_dir_dist
        mask = collision_const.GROUP_CHARACTER_INCLUDE
        group = collision_const.GROUP_CHARACTER_INCLUDE
        hit, point, normal, fraction, color, obj = scene.scene_col.hit_by_ray(start, end, 0, mask, group, collision.INCLUDE_FILTER)
        if hit:
            return False
        forward_dir = self.ev_g_model_forward()
        if not forward_dir:
            return False
        forward_dir = -forward_dir
        forward_dir.normalize()
        forward_dir_dist = forward_dir * forward_len
        end = forward_dir_dist + start
        mask = collision_const.GROUP_CHARACTER_INCLUDE
        group = collision_const.GROUP_CHARACTER_INCLUDE
        hit, point, normal, fraction, color, obj = scene.scene_col.hit_by_ray(start, end, 0, mask, group, collision.INCLUDE_FILTER)
        if hit:
            return False
        return True

    def _get_character_logic_height(self, radius, actual_height):
        char_ctrl = self.sd.ref_character
        return actual_height - radius * 2.0 - char_ctrl.getSkinWidth() * 2.0

    def can_stand(self):
        scene = self.scene
        foot_position = self.ev_g_foot_position()
        character = self.sd.ref_character
        if not character:
            return
        old_radius = character.getRadius()
        old_height = character.getHeight()
        if character and hasattr(character, 'setIsEnableTestPos'):
            character.setIsEnableTestPos(False)
        stepheight = character.getStepHeight()
        width = collision_const.CHARACTER_STAND_WIDTH
        height = collision_const.CHARACTER_STAND_HEIGHT
        self.send_event('E_RECREATE_CHARACTER', width, height, stepheight)
        self.send_event('E_FOOT_POSITION', foot_position)
        is_hit = self.ev_g_static_test(character.group, character.mask)
        character.setRadius(old_radius)
        character.setHeight(old_height)
        self.send_event('E_FOOT_POSITION', foot_position)
        physicalPosition = character.physicalPosition
        if character and hasattr(character, 'setIsEnableTestPos'):
            character.setIsEnableTestPos(True)
        if is_hit:
            return False
        return True

    def get_all_state_desc(self):
        char_ctrl = self.sd.ref_character
        walk_direction = char_ctrl.getWalkDirection()
        model = self.ev_g_model()
        world_yaw = model.world_rotation_matrix.yaw
        local_yaw = model.rotation_matrix.yaw
        state_desc = 'test--ComHumanDriver.dump_character--isActive =' + str(char_ctrl.isActive())
        normalize_walk_direction = math3d.vector(walk_direction)
        if not normalize_walk_direction.is_zero:
            normalize_walk_direction.normalize()
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
        state_desc += '--scene_debug_info =' + str(scene_debug_info) + '--walk_direction.length =' + str(walk_direction.length / NEOX_UNIT_SCALE) + '--last_frame_time =' + str(last_frame_time) + '--seperate_direction.length =' + str(seperate_direction.length) + '--normalize_walk_direction =' + str(normalize_walk_direction) + '--footPosition =' + str(char_ctrl.getFootPosition()) + '--onGround =' + str(char_ctrl.onGround()) + '--physicalPosition =' + str(char_ctrl.physicalPosition) + '--verticalVelocity =' + str(char_ctrl.verticalVelocity / NEOX_UNIT_SCALE) + '--gravity =' + str(self.ev_g_gravity() / NEOX_UNIT_SCALE) + '--walk_direction =' + str(walk_direction) + '--world_yaw =' + str(world_yaw) + '--local_yaw =' + str(local_yaw) + '--canJump =' + str(char_ctrl.canJump()) + '--jumpSpeed =' + str(char_ctrl.getJumpSpeed() / NEOX_UNIT_SCALE) + '--model.position =' + str(model.position) + '--model.world_position =' + str(model.world_position) + '--position =' + str(char_ctrl.position) + '--speed =' + str(self._get_speed_value()) + '--max_slope' + str(math.degrees(char_ctrl.getMaxSlope())) + '--stepHeight =' + str(char_ctrl.getStepHeight()) + '--getFallSpeed =' + str(self.ev_g_fall_speed() / NEOX_UNIT_SCALE) + '--getXOffset =' + str(char_ctrl.getXOffset()) + '--getYOffset =' + str(char_ctrl.getYOffset()) + '--getRadius =' + str(char_ctrl.getRadius()) + '--max_slope =' + str(math.degrees(char_ctrl.getMaxSlope()))
        return state_desc

    def _change_character_attr(self, name, *arg):
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
            self.send_event('E_SET_JUMP_SPEED', value)
        elif name == 'max_fall_speed':
            value *= NEOX_UNIT_SCALE
            self.send_event('E_FALL_SPEED', value)
        elif name == 'gravity':
            value *= NEOX_UNIT_SCALE
            self.send_event('E_GRAVITY', value)
        elif name == 'reset_phys_attr':
            self.reset_phys_attr()
        elif name == 'debug_phys':
            scene = self.scene
            is_drawing = bool(value)
            scene.scene_col.drawing = is_drawing
            if is_drawing:
                scene.scene_col.drawing_center = self._get_pos()
                scene.scene_col.drawing_radius = 1000
        elif name == 'stand_args':
            collision_const.STAND_MODEL_OFFSET_X = arg[0] * NEOX_UNIT_SCALE
            collision_const.STAND_MODEL_OFFSET_Y = arg[1] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_STAND_WIDTH = arg[2] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_STAND_HEIGHT = arg[3] * NEOX_UNIT_SCALE
            self.on_change_posture_stand()
        elif name == 'squat_args':
            collision_const.SQUAT_MODEL_OFFSET_X = arg[0] * NEOX_UNIT_SCALE
            collision_const.SQUAT_MODEL_OFFSET_Y = arg[1] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_SQUAT_WIDTH = arg[2] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_SQUAT_HEIGHT = arg[3] * NEOX_UNIT_SCALE
            self.on_change_posture_squat()
        elif name == 'crawl_args':
            collision_const.DOWN_MODEL_OFFSET_X = arg[0] * NEOX_UNIT_SCALE
            collision_const.DOWN_MODEL_OFFSET_Y = arg[1] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_DOWN_WIDTH = arg[2] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_DOWN_HEIGHT = arg[3] * NEOX_UNIT_SCALE
            collision_const.CHARACTER_DOWN_LENGTH = arg[4] * NEOX_UNIT_SCALE
            self.on_change_posture_crawl()
        elif name == 'enable_log':
            char_ctrl.setIsLog(bool(value))
        elif name == 'gm_cmd':
            global_data.player.wiz_command(value, True)
        elif name == 'dump_character':
            print(self.get_all_state_desc())
        elif name == 'enable_pvd':
            collision.set_pvd_enable(bool(value))
        elif name == 'human_yaw':
            com_camera = self.scene.get_com('PartCamera')
            real_camera_yaw = com_camera.cam.world_rotation_matrix.yaw
            logic_camera_yaw = com_camera.get_yaw()
            walk_direction = char_ctrl.getWalkDirection()
            circle_yaw = math.pi * 2
            human_yaw = self._yaw
            human_yaw = human_yaw - math.floor(human_yaw % circle_yaw) * circle_yaw
            model_yaw = self.ev_g_yaw()
            model_yaw = model_yaw - math.floor(model_yaw % circle_yaw) * circle_yaw
            model = self.ev_g_model()
            real_model_yaw = model.rotation_matrix.yaw
            real_model_yaw = real_model_yaw - math.floor(real_model_yaw % circle_yaw) * circle_yaw
            print('test--human_yaw--human_yaw =', human_yaw, '--model_yaw =', model_yaw, '--real_model_yaw =', real_model_yaw, '--real_camera_yaw =', real_camera_yaw, '--logic_camera_yaw =', logic_camera_yaw, '--walk_direction.yaw =', walk_direction.yaw)

    def set_ignore_check_gravity(self, is_ignore):
        import game3d
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return
        self._ignore_check_gravity = bool(is_ignore)

    def _check_gravity(self, move_dir):
        if self._ignore_check_gravity:
            return
        if move_dir.is_zero:
            return
        if self.ev_g_char_waiting():
            return
        if self.ev_g_get_state(status_config.ST_SWIM):
            return
        if self.ev_g_get_state(status_config.ST_SKATE) and self.ev_g_is_in_water_area():
            return
        gravity = self.ev_g_gravity()
        if gravity == 0:
            self.on_reset_gravity()
        fall_speed = self.ev_g_fall_speed()
        if fall_speed <= 0:
            self.reset_fall_speed()

    def reset_fall_speed(self, *args):
        fall_speed = jump_physic_config.max_fall_speed * NEOX_UNIT_SCALE
        self.send_event('E_FALL_SPEED', fall_speed)

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

    def _enter_states(self, new_state):
        if new_state in self.IK_CHANGE_STATE:
            self.send_event('E_SET_HAND_IK')

    def _leave_states(self, leave_state, new_state=None):
        if leave_state == status_config.ST_SKATE:
            self.send_event('E_UNLIMIT_LOWER_HEIGHT')
        elif leave_state == status_config.ST_RIGHT_AIM:
            self.send_event('E_QUIT_RIGHT_AIM')
        elif character_action_utils.is_jump(leave_state):
            if not self.ev_g_is_jump():
                self.send_event('E_LEAVE_JUMP')
        elif leave_state == status_config.ST_ROLL:
            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            if weapon_obj and weapon_obj.is_bullet_empty():
                self.send_event('E_TRY_RELOAD')
        if leave_state in self.IK_CHANGE_STATE:
            self.send_event('E_SET_HAND_IK')
        if new_state is None:
            return
        else:
            if not self.is_avatar:
                return
            if leave_state != new_state:
                state_events = {status_config.ST_SWITCH: ('E_ACTION_END_SWITCH', new_state),status_config.ST_HELP: ('E_CANCEL_RESCUE', ),
                   status_config.ST_USE_ITEM: (
                                             'E_ITEMUSE_CANCEL', None, True, new_state)
                   }
                if leave_state in state_events:
                    self.send_event(*state_events[leave_state])
                elif leave_state == status_config.ST_FLY:
                    if self._hited_timer:
                        global_data.game_mgr.unregister_logic_timer(self._hited_timer)
                        self._hited_timer = None
                    self.set_walk_direction(math3d.vector(0, 0, 0))
            return

    def _get_speed_value(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return 0
        speed_dir = char_ctrl.getWalkDirection() + math3d.vector(0, char_ctrl.verticalVelocity, 0)
        return speed_dir.length

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

    def _get_speed_meter_per_second(self):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        return char_ctrl.getWalkDirection().length / NEOX_UNIT_SCALE

    def set_max_slope(self, slope):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setMaxSlope(math.radians(slope))

    def get_model_yaw_mat(self):
        yaw = self.sd.ref_rotatedata.yaw_body + self.sd.ref_rotatedata.yaw_offset
        return math3d.matrix.make_rotation_y(yaw)

    def on_turn_dir(self):
        model_rot_mat = self.get_model_yaw_mat()
        model_rot = math3d.matrix_to_rotation(model_rot_mat)
        self.send_event('E_SET_CHAR_ROTATION_DIR', model_rot)

    def set_walk_direction(self, move_dir, reach_target_callback=None, reach_target_pos=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.sd.ref_parachute_stage == STAGE_FREE_DROP:
            return
        if self.ev_g_get_state(status_config.ST_FLY):
            return
        if move_dir and move_dir.is_zero:
            self.send_event('E_ACTION_SYNC_STOP')
        self.on_turn_dir()
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

    def on_set_speed(self, speed):
        log_error('\xe4\xb8\xba\xe4\xbb\x80\xe4\xb9\x88\xe8\xa6\x81\xe7\x94\xa8E_SPEED\xef\xbc\x8cshare_data\xe4\xb8\x8d\xe9\xa6\x99\xe5\x90\x97')
        if speed == self.sd.ref_cur_speed:
            return
        self.sd.ref_cur_speed = speed

    def on_get_speed(self):
        log_error('\xe4\xb8\xba\xe4\xbb\x80\xe4\xb9\x88\xe8\xa6\x81\xe7\x94\xa8G_SPEED\xef\xbc\x8cshare_data\xe4\xb8\x8d\xe9\xa6\x99\xe5\x90\x97')
        return self.sd.ref_cur_speed

    def on_rotate(self, yaw, force_change_spd=True):
        self.sd.ref_logic_trans.yaw_target += yaw

    def on_pitch(self, pitch, *args):
        self.send_event('E_ACTION_PITCH', pitch)
        self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)

    def on_move(self, move_dir, target_callback=None, target_pos=None):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if not move_dir or move_dir.is_zero:
            walk_direction = char_ctrl.getWalkDirection()
            if not walk_direction.is_zero:
                walk_direction.normalize()
        else:
            cur_yaw = self.sd.ref_rotatedata.yaw_body
            if self._yaw_cache != cur_yaw:
                self._yaw_cache = cur_yaw
                self._yaw_mat = math3d.matrix.make_rotation_y(cur_yaw)
            walk_direction = move_dir * self._yaw_mat
        speed = self.sd.ref_cur_speed
        if self._follow_speed and speed < self._follow_speed:
            speed = self._follow_speed
        self.send_event('E_CHECK_ACTIVE_CHARACTER')
        walk_direction = walk_direction * speed
        self.set_walk_direction(walk_direction, target_callback, target_pos)
        self._check_gravity(walk_direction)

    def on_stop(self, force_stop=False):
        if self.ev_g_get_state(status_config.ST_ROLL):
            return
        if not force_stop and self.ev_g_get_state(status_config.ST_SKATE):
            self.send_event('E_ACTION_SKATE_MOVE_STOP')
            return
        self.sd.ref_cur_speed = 0
        self._follow_speed = 0
        self.set_walk_direction(math3d.vector(0, 0, 0))

    def on_pos_changed(self, pos, *arg):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        if self.ev_g_is_in_water_area() and self.ev_g_get_state(status_config.ST_SKATE):
            water_height = self.ev_g_cur_water_height()
            pos.y = max(water_height, pos.y)
        if math.isinf(pos.x) or math.isinf(pos.y) or math.isinf(pos.y) or math.isnan(pos.x) or math.isnan(pos.y) or math.isnan(pos.y):
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)

    def _get_cam_yaw(self):
        if global_data.cam_data:
            return global_data.cam_data.yaw
        return 0

    def _on_parachuting_finish(self):
        jump_speed = jump_physic_config.jump_speed * NEOX_UNIT_SCALE
        self.send_event('E_SET_JUMP_SPEED', jump_speed)

    def on_camera_state_switched(self, new_state, old_state, is_finish):
        if new_state == old_state:
            return
        if not is_finish:
            return
        from data.camera_state_const import PARACHUTE_MODE, VEHICLE_MODE, MECHA_MODE_TWO
        com_camera = self.scene.get_com('PartCamera')
        if com_camera.is_free_type_camera(old_state) and new_state not in [PARACHUTE_MODE, VEHICLE_MODE,
         MECHA_MODE_TWO]:
            camera_yaw = com_camera.get_yaw()
            self.send_event('E_ACTION_SET_YAW', camera_yaw)
            self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR', True)

    def _on_fall(self):
        if self.sd.ref_parachute_stage in (STAGE_NONE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE):
            return
        if self.ev_g_ctrl_mecha():
            return
        self.send_event('E_FALL')

    def on_ground_callback(self, *args):
        self.send_event('E_ON_TOUCH_GROUND', *args)
        self.send_event('E_JUMP_STAGE', 0)

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

    def test_aim_pos(self):
        model = self.ev_g_model()
        if not model:
            return
        look_at_pos = self.get_state_look_at_pos()
        chect_begin = model.get_socket_matrix('aim', world.SPACE_TYPE_WORLD).translation
        check_end = look_at_pos
        line_list = [(chect_begin, check_end, 255)]
        print(('test--test_aim_pos--check_end =', check_end))
        self.draw_line(line_list)

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
            if not start or not end:
                continue
            color = 65280
            if len(one_line_info) > 2:
                color = one_line_info[2]
            index += 1
            obj.create_line([((start,), (end,), color)])
            self._draw_obj_list.append(obj)

    def _end_hit_by_force(self):
        self._hited_timer = None
        self.ev_g_cancel_state(status_config.ST_FLY)
        v3d_vel = math3d.vector(0, 0, 0)
        self.set_walk_direction(v3d_vel)
        self.send_event('E_ACTION_SYNC_VEL', v3d_vel)
        return

    def _hit_by_force(self, velocity, duration):
        if isinstance(velocity, (tuple, list)):
            velocity = math3d.vector(*velocity)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_HIT_BY_FORCE, ((velocity.x, velocity.y, velocity.z), duration)], True)
        self.send_event('E_ACTION_HITED_BY_VEHICLE')
        if self._hited_timer:
            global_data.game_mgr.unregister_logic_timer(self._hited_timer)
            self._hited_timer = None
        self.set_walk_direction(velocity)
        self._hited_timer = global_data.game_mgr.register_logic_timer(self._end_hit_by_force, max(duration, 0.1), times=1, mode=timer.CLOCK)
        self.ev_g_status_try_trans(status_config.ST_FLY)
        return

    def _clear_draw_obj(self):
        if self._draw_obj_list:
            for draw_obj in self._draw_obj_list:
                draw_obj.destroy()

        self._draw_obj_list = []

    def disable_rocker_move(self, enable):
        self._disable_rocker_move = enable

    def _enable_move(self, enable):
        self._can_move = enable

    def tick(self, dt):
        self.tick_move_to(dt)

    def _clear_move(self):
        self.reset()

    def tick_move_to(self, dt):
        char_ctrl = self.sd.ref_character
        if not self._to_pos:
            return
        else:
            if not self._can_move:
                return
            if not char_ctrl:
                return
            if self.ev_g_is_in_any_state((status_config.ST_ROLL, status_config.ST_RUSH)):
                return
            dt_pos = self._to_pos - char_ctrl.position
            dt_pos.y = 0
            if dt_pos.is_zero or dt_pos.length < 4.0:
                self._to_pos = None
                self._to_pos_dir = None
                if not self.ev_g_check_sync_dir_list():
                    self.send_event('E_MOVE_STOP', True)
                return
            dt_pos.normalize()
            yaw = self.ev_g_yaw()
            if not self._always_forward:
                move_dir = dt_pos * math3d.matrix.make_rotation_y(-yaw)
                if math.isnan(move_dir.length):
                    move_dir = math3d.vector(0, 0, 0)
            else:
                f_yaw = dt_pos.yaw
                self._to_yaw = f_yaw
                diff_yaw = f_yaw - yaw
                fix_dt = 2 * math.pi * diff_yaw / abs(diff_yaw) if abs(diff_yaw) > math.pi else 0
                if fix_dt:
                    yaw += fix_dt
                    diff_yaw = f_yaw - yaw
                if abs(diff_yaw) > 0.1:
                    diff_yaw *= self.YAW_INTERPOLATION
                    f_yaw = yaw + diff_yaw
                else:
                    diff_yaw = 0
                self.sd.ref_logic_trans.yaw_target += diff_yaw
                self.send_event('E_ACTION_SET_YAW', f_yaw)
                if diff_yaw == 0:
                    move_dir = math3d.vector(0, 0, 1)
                else:
                    move_dir = dt_pos * math3d.matrix.make_rotation_y(-yaw)
                if self._always_forward == MOVE_TO_MODE_ALWAYS_FORWARD_WITH_CAM:
                    com_camera = self.scene.get_com('PartCamera')
                    if com_camera:
                        com_camera.set_yaw(f_yaw)
            self.send_event('E_MOVE', move_dir)
            if not self.ev_g_is_in_any_state((status_config.ST_MOVE, status_config.ST_RUN)):
                self.send_event('E_ACTIVE_STATE', status_config.ST_MOVE)
            return

    def _ai_move_to(self, pos, f_spd, always_forward, pos_dir):
        self._to_pos_dir = pos_dir
        self._move_to(pos, f_spd, always_forward)

    def _move_to(self, pos, f_spd, always_forward=MOVE_TO_MODE_NONE):
        self._to_pos = pos
        self._follow_speed = f_spd
        self._always_forward = always_forward
        if self._always_forward == MOVE_TO_MODE_ALWAYS_FORWARD_WITH_CAM:
            if not self.unit_obj or not global_data.player or self.unit_obj.id != global_data.player.id:
                self._always_forward = MOVE_TO_MODE_ALWAYS_FORWARD
        self.send_event('E_ON_MOVE_TO', pos)
        self.need_update = True

    def _get_target_pos(self):
        return self._to_pos

    def _get_target_dir(self):
        return (
         self._to_pos, self._to_pos_dir)

    def _get_ground_slope(self):
        char_ctrl = self.sd.ref_character
        return char_ctrl.getSlope()

    def _get_pos(self):
        char_ctrl = self.sd.ref_character
        return char_ctrl.position

    def _get_physical_pos(self):
        char_ctrl = self.sd.ref_character
        pos = char_ctrl.position
        y_off = char_ctrl.getYOffset()
        return math3d.vector(pos.x, pos.y + y_off, pos.z)

    def _on_ctrl_use_drug(self, *args):
        return None