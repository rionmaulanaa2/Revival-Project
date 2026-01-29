# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCharacter.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, GROUP_CHARACTER_INCLUDE, MASK_CHARACTER_ROBOT, GROUP_CHARACTER_ROBOT, GROUP_MECHA_BALL
import math3d
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, ICE_GROUP, TERRAIN_MASK
import collision
from data.acc_config import ACC_RATE, NO_DIR_ACC_RATE, get_acc_rate
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_PLANE, STAGE_NONE, STAGE_PRE_PARACHUTE
import time
from logic.gcommon.const import NEOX_UNIT_SCALE
import common.utils.timer as timer
import logic.gcommon.common_const.ai_const as ai_const
from common.cfg import confmgr
import logic.gcommon.common_const.collision_const as collision_const
from logic.gutils import character_ctrl_utils
from logic.client.const import game_mode_const
from logic.comsys.control_ui.GMHelperUIFactory import GMHelperUIFactory
from logic.gcommon.common_const import machine_const
from logic.gcommon.cdata import jump_physic_config
FORCE_DIRECTION = 1
LIFT_DIRECTION = 2
TRAIN_DIRECTION = 3
NOT_MOVE_DIST_THRESHOLD_SQR = (0.1 * NEOX_UNIT_SCALE) ** 2
NOT_MOVE_MAX_DURATION = 1
CC_COLLISION_SIDES = 1
CC_COLLISION_UP = 2
CC_COLLISION_DOWN = 4
CC_COLLISION_SLIDE = 8
CC_COLLISION_STUCK1 = CC_COLLISION_SIDES | CC_COLLISION_UP | CC_COLLISION_DOWN
CC_COLLISION_STUCK2 = CC_COLLISION_SIDES | CC_COLLISION_DOWN
CC_COLLISION_STUCK3 = CC_COLLISION_SIDES | CC_COLLISION_UP
DETECT_MAX_HEIGHT = 50 * NEOX_UNIT_SCALE
DETECT_DIRECTIONS = [
 math3d.vector(0, DETECT_MAX_HEIGHT, 0),
 math3d.vector(0, 0.5 * -DETECT_MAX_HEIGHT, 0),
 math3d.vector(DETECT_MAX_HEIGHT, 0, 0),
 math3d.vector(-DETECT_MAX_HEIGHT, 0, 0),
 math3d.vector(0, 0, DETECT_MAX_HEIGHT),
 math3d.vector(0, 0, -DETECT_MAX_HEIGHT)]
DETECT_DIRECTIONS_NUM = len(DETECT_DIRECTIONS)
CLOSE_BUILDING_KEY_WORD = []
SHOW_GM_UI_KEEP_TIME = 15
SHOW_GM_UI_CD_TIME = 90
MECHA_ACC_TYPE = '1'
HUMAN_ACC_TYPE = '0'
IGNORE_DIR_PATHS = [
 'model_new\\scene\\items\\common']
for one_path in list(IGNORE_DIR_PATHS):
    one_new_path = one_path.replace('\\', '/')
    IGNORE_DIR_PATHS.append(one_new_path)

class ComCharacter(UnitCom):
    BIND_EVENT = {'E_CHAR_X_OFF': '_set_x_off',
       'G_CHAR_X_OFF': '_get_x_off',
       'E_CHAR_Y_OFF': '_set_y_off',
       'G_CHAR_Y_OFF': '_get_y_off',
       'E_DEATH': '_on_dead',
       'E_DEFEATED': '_on_defeated',
       'E_REVIVE': '_on_revive',
       'E_ON_CONTROL_TARGET_CHANGE': '_on_control_target_change',
       'G_CHAR_WAITING': '_get_char_waiting',
       'G_CHAR_RESUME_COL': 'resume_gravity',
       'E_RECREATE_CHARACTER': 'recreate',
       'E_REWAIT_DETAIL': 'rewait_detail',
       'E_TELEPORT': '_teleport',
       'E_TEST_PHYSY_SIZE': '_test_physy_size',
       'G_CHARACTER_COLLISON_HEIGHT': '_get_collison_height',
       'E_FORCE_ACTIVE': 'try_active_force',
       'E_FORCE_DEACTIVE': 'try_deactive_force',
       'G_HIT_BY_SCENE_COLLISION': 'hit_by_scene_collision',
       'E_CHARACTER_WALK': '_set_walk_direction',
       'E_CHARACTER_WALK_FORCE': '_set_walk_direction_force',
       'E_CHARACTER_WALK_LIFT': '_set_walk_direction_lift',
       'E_CHARACTER_WALK_TRAIN': '_set_walk_direction_train',
       'E_PHY_DIRECTION': '_set_phy_direction',
       'G_CHAR_WALK_DIRECTION': '_get_walk_direction',
       'G_GRAVITY': 'get_gravity',
       'E_GRAVITY': 'set_gravity',
       'G_FALL_SPEED': 'get_fall_speed',
       'E_FALL_SPEED': 'set_fall_speed',
       'E_VERTICAL_SPEED': 'set_vertical_speed',
       'G_VERTICAL_SPEED': 'get_vertical_speed',
       'G_PHY_POSITION': '_get_physical_position',
       'E_ACC_TRIGGER_INFO': '_on_acc_trigger_info_changed',
       'E_NO_DIR_ACC_TRIGGER_INFO': '_on_no_dir_acc_trigger_info_changed',
       'G_JUMP_SPEED': 'getJumpSpeed',
       'E_SET_JUMP_SPEED': 'setJumpSpeed',
       'E_SET_CHAR_GROUP': 'set_group',
       'G_CHAR_GROUP': 'get_group',
       'E_SET_CHAR_MASK': 'set_mask',
       'G_CHAR_MASK': 'get_mask',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_PARACHUTE_STATUS_CHANGED': '_on_parachute_stage_changed',
       'E_CLEAR_ACC_INFO': 'on_clear_acc_info',
       'E_ENABLE_ACC_INFO': 'enable_acc_info',
       'E_GET_ON_LIFT': 'get_on_lift',
       'E_IGNORE_GRAVITY': 'on_ignore_gravity',
       'G_IS_IN_LIFT': 'is_in_lift',
       'G_TEST_CREATE_CHAR': '_test_create_character',
       'G_EASY_STATIC_TEST': 'easy_static_test',
       'G_STATIC_TEST': 'static_test',
       'G_IS_POS_VALID': 'is_pos_valid',
       'G_SWEEP_TEST': 'sweep_test',
       'G_VERTICAL_HEAD_POSITION': 'get_vertical_head_position',
       'E_DEBUG_CLOSE_SPACE': 'debug_close_space',
       'E_SET_IS_ENABLE_TEST_POS': 'set_is_enable_test_pos',
       'E_USE_GM_HLEP': 'use_gm_help',
       'G_IS_CHARACTER_ACTIVE': 'is_character_active',
       'G_CHARACTER_COL_ID': 'get_col_id',
       'E_FOOT_POSITION': 'set_foot_position',
       'E_FOOT_POSITION_BY_SYNC': 'set_foot_position_by_sync',
       'G_FOOT_POSITION': 'get_foot_position',
       'G_COL_HEAD_POSITION': 'get_head_position',
       'E_CHECK_ACTIVE_CHARACTER': 'check_active_character',
       'E_DEBUG_NOT_MOVE': 'debug_not_move',
       'E_ENABLE_TEST_POS': 'set_is_enable_test_pos',
       'E_SET_CHAR_ROTATION_DIR': 'set_character_direction',
       'E_RESET_PHY': 'reset',
       'E_LIMIT_HEIGHT': 'limit_height',
       'E_UNLIMIT_HEIGHT': 'unlimit_Height',
       'G_LIMIT_HEIGHT': 'get_limit_height',
       'G_IS_LIMIT_LOWER_HEIGHT': 'is_limit_lower_height',
       'E_LIMIT_LOWER_HEIGHT': 'limit_lower_height',
       'E_UNLIMIT_LOWER_HEIGHT': 'unlimit_lower_Height',
       'G_LIMIT_LOWER_HEIGHT': 'get_limit_lower_height',
       'G_IS_LIMIT_HEIGHT': 'is_limit_height',
       'E_TRY_ACTIVE_CHARACTER': 'active_char',
       'G_CHARACTER_TOTAL_HEIGHT': '_get_character_total_height',
       'E_ENABLE_Z_CAPSULE': 'set_enable_z_capsule',
       'E_ENABLE_COL_WATE': 'enable_col_wate'
       }

    def __init__(self):
        super(ComCharacter, self).__init__()
        self.sd.ref_character = None
        self._active_waiting = None
        self._collison_height = None
        self.lift = None
        self._walk_direction = math3d.vector(0, 0, 0)
        self._real_walk_direction = math3d.vector(0, 0, 0)
        self._other_walk_direction = {}
        self._is_in_acc = False
        self.sd.ref_is_in_acc = False
        self._is_in_no_dir_acc = False
        self.sd.ref_is_in_no_dir_acc = False
        self._acc_dir = None
        self._acc_key = HUMAN_ACC_TYPE
        self.sd.ref_acc_dir = None
        self._acc_dir_dict = {}
        self._no_dir_acc_dir_dict = {}
        self._is_enable_acc = True
        self._last_foot_position = None
        self._keep_same_pos_start_time = 0
        self._touch_wall = False
        self._test_move_char_ctrl = None
        self._detect_direction = 0
        self._last_close_direction = None
        self._is_debug_log = False
        self._ignore_col_ids = set([])
        self._last_stuck_time = 0
        self._last_show_gm_ui_time = 0
        self.init_collision_parameter()
        self._active_character_timer = None
        self._limit_lower_height = 0
        self._is_limit_lower_height = False
        self._is_limit_height = False
        return

    def init_collision_parameter(self):
        if CLOSE_BUILDING_KEY_WORD:
            return
        close_space_key_word_conf = confmgr.get('scene_args_conf', 'CloseSpaceKeyWord', 'Content', default={})
        for one_config in six.itervalues(close_space_key_word_conf):
            CLOSE_BUILDING_KEY_WORD.append(one_config['key_word'])

        print('test--init_collision_parameter--CLOSE_BUILDING_KEY_WORD =', CLOSE_BUILDING_KEY_WORD)

    def destroy(self):
        self.char_ctrl and self.char_ctrl.setOnSidesCallback(None)
        self.del_character()
        self.lift = None
        super(ComCharacter, self).destroy()
        return

    def _change_character_attr(self, name, *arg):
        if name == 'dump_character':
            print(('test--ComCharacter.dump_character--isActive =', self.char_ctrl.isActive(), '--group =', self.char_ctrl.group, '--mask =', self.char_ctrl.filter, '--is_limit_height =', self.is_limit_height(), '--getLimitHeight =', self.char_ctrl.getLimitHeight(), '--is_limit_lower_height =', self.is_limit_lower_height(), '--getLimitLowerHeight =', self.char_ctrl.getLimitLowerHeight()))

    def _on_parachute_stage_changed(self, stage):
        if self._active_waiting and stage in (STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_PLANE, STAGE_NONE, STAGE_PRE_PARACHUTE):
            self.resume_gravity()

    def get_vertical_head_position(self):
        if not self.char_ctrl:
            return
        foot_position = self.char_ctrl.getFootPosition()
        height = self.char_ctrl.getHeight()
        radius = self.char_ctrl.getRadius()
        head_position = math3d.vector(foot_position)
        head_position.y = foot_position.y + height + radius * 2
        return head_position

    def is_character_active(self):
        return self.char_ctrl and self.char_ctrl.isActive()

    def check_active_character(self, *args, **kwargs):
        if self.ev_g_is_avatar() and self.ev_g_death():
            return
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        if self.char_ctrl.isActive():
            return
        foot_position = self.get_foot_position()
        if not self.scene.check_collision_loaded(foot_position):
            return
        self.active_char(*args, **kwargs)

    def del_character(self):
        self._release_active_character_timer()
        if self.char_ctrl:
            scene = self.scene
            global_data.emgr.scene_remove_lift_user_event.emit(self.char_ctrl.cid)
            scene.scene_col.remove_character(self.char_ctrl)
        self.sd.ref_character = None
        return

    def easy_static_test(self):
        if not self.is_valid():
            return False
        scene = self.scene
        if not scene or not scene.valid:
            return False
        if not self.is_character_active():
            return False
        character = self._get_character()
        group = character.group
        mask = character.filter
        return character.staticTest(group, mask)

    def static_test(self, group=None, mask=None, position=None, ignore_col_id_list=False):
        if not self.is_valid():
            return False
        else:
            scene = self.scene
            if not scene or not scene.valid:
                return False
            if not self.is_character_active():
                return False
            character = self._get_character()
            if group is None:
                group = character.group
            if mask is None:
                mask = character.filter
            is_hit = False
            if position:
                if getattr(character, 'staticTestWithPos1', None):
                    is_hit, col_id_list = character.staticTestWithPos1(group, mask, position)
                    if ignore_col_id_list:
                        return is_hit
                    if is_hit:
                        if not col_id_list:
                            return False
                        col_id_list = set(col_id_list) - self._ignore_col_ids
                        if not col_id_list:
                            return False
                elif getattr(character, 'staticTestWithPos', None):
                    is_hit = character.staticTestWithPos(group, mask, position)
                else:
                    cur_pos = character.physicalPosition
                    character.physicalPosition = position
                    is_hit = character.staticTest(group, mask)
                    character.physicalPosition = cur_pos
            elif getattr(character, 'staticTestWithPos1', None):
                is_hit, col_id_list = character.staticTestWithPos1(group, mask, character.physicalPosition)
                if ignore_col_id_list:
                    return is_hit
                if is_hit:
                    col_id_list = set(col_id_list) - self._ignore_col_ids
                    if not col_id_list:
                        return False
            else:
                is_hit = character.staticTest(group, mask)
            return is_hit

    def is_pos_valid(self, position):
        if not self.is_character_active():
            return True
        old_position = self.char_ctrl.physicalPosition
        self._set_phys_pos_ignore_test(position)
        is_in_collision = self.static_test()
        is_valid = not is_in_collision
        self._set_phys_pos_ignore_test(old_position)
        return is_valid

    def sweep_test(self, direction, position=None):
        if not self.is_character_active():
            return (False,)
        else:
            if position is None:
                position = self.char_ctrl.physicalPosition
            if direction.is_zero:
                return (False,)
            col_result = self.char_ctrl.sweepTest(position, direction)
            return col_result

    def setJumpSpeed(self, jump_speed):
        character = self._get_character()
        if not character:
            return
        character.setJumpSpeed(jump_speed)

    def getJumpSpeed(self):
        character = self._get_character()
        if not character:
            return 0
        return character.getJumpSpeed()

    def set_gravity(self, gravity):
        if not self.char_ctrl:
            return
        self.sd.ref_gravity = gravity
        self.char_ctrl.setGravity(gravity * self.sd.ref_gravity_scale)

    def get_gravity(self):
        if not self.char_ctrl:
            return 0
        return self.char_ctrl.getGravity()

    def set_fall_speed(self, speed):
        if not self.char_ctrl:
            return
        self.char_ctrl.setFallSpeed(speed)

    def get_fall_speed(self):
        if not self.char_ctrl:
            return 0
        return self.char_ctrl.getFallSpeed()

    def get_vertical_speed(self):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        return char_ctrl.verticalVelocity

    def set_vertical_speed(self, speed):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        char_ctrl.verticalVelocity = speed

    def _get_physical_position(self):
        if not self.char_ctrl:
            return
        return self.char_ctrl.physicalPosition

    def init_from_dict(self, unit_obj, bdict):
        super(ComCharacter, self).init_from_dict(unit_obj, bdict)
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        if not self.sd.ref_gravity:
            self.sd.ref_gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        self._init_character(bdict)
        self.char_ctrl.setOnSidesCallback(self.on_sides_callback)
        self.init_col_event()
        if self.ev_g_is_avatar():
            global_data.game_mgr.register_logic_timer(self.check_overlap_tick, 0.2, times=-1, mode=timer.CLOCK)
            global_data.game_mgr.register_logic_timer(self.check_in_close_space_tick, 2, times=-1, mode=timer.CLOCK)

    def init_col_event(self):
        if not self.ev_g_is_avatar():
            return
        emgr = global_data.emgr
        econf = {'add_ignore_col_ids_event': self.add_ignore_col_ids,
           'del_ignore_col_ids_event': self.del_ignore_col_ids
           }
        emgr.bind_events(econf)

    def add_ignore_col_ids(self, cid, *args):
        self._ignore_col_ids.add(cid)

    def del_ignore_col_ids(self, cid, *args):
        if cid in self._ignore_col_ids:
            self._ignore_col_ids.remove(cid)

    def on_sides_callback(self, hit_flags, *args):
        self._touch_wall = hit_flags & CC_COLLISION_SIDES != 0

    def getStaticSweepTest(self):
        cur_physic_postion = self.char_ctrl.physicalPosition
        skin_width = self.char_ctrl.getSkinWidth()
        direction = math3d.vector(self._real_walk_direction)
        direction.y = 0
        distance = skin_width + 3.5
        normalize_direction = math3d.vector(direction)
        if normalize_direction.is_zero:
            return (False, None, 0)
        else:
            normalize_direction.normalize()
            direction = normalize_direction * distance
            col_result = self.char_ctrl.sweepTest(cur_physic_postion, direction)
            is_hit = col_result[0]
            hit_position = col_result[1]
            hit_normal = col_result[2]
            move_len = col_result[3]
            if move_len is not None and move_len >= 0:
                is_hit = False
            return (is_hit, hit_normal, move_len)

    def cannot_inverse_dir_leave(self):
        cur_physic_postion = self.char_ctrl.physicalPosition
        skin_width = self.char_ctrl.getSkinWidth()
        direction = -self._real_walk_direction
        direction.y = 0
        distance = skin_width + 3.5
        if direction.is_zero:
            return (False, None, 0)
        else:
            normalize_direction = math3d.vector(direction)
            normalize_direction.normalize()
            direction = normalize_direction * distance
            col_result = self.char_ctrl.sweepTest(cur_physic_postion, direction)
            is_hit = col_result[0]
            hit_position = col_result[1]
            hit_normal = col_result[2]
            move_len = col_result[3]
            if move_len is not None and move_len >= 0:
                is_hit = False
            return (
             is_hit, hit_normal, move_len)

    def is_move_dir_hit_scene(self):
        chect_begin = self.char_ctrl.physicalPosition
        normalize_move_dir = math3d.vector(self._real_walk_direction)
        normalize_move_dir.y = 0
        if normalize_move_dir.is_zero:
            return False
        normalize_move_dir.normalize()
        distance = (self.char_ctrl.getSkinWidth() + 0.1) * NEOX_UNIT_SCALE
        check_end = chect_begin + normalize_move_dir * distance
        group = GROUP_CAN_SHOOT & ~WATER_GROUP
        mask = GROUP_CAN_SHOOT & ~WATER_MASK
        is_hit = self.hit_by_scene_collision(chect_begin, check_end)
        return is_hit

    def test_no_block(self):
        is_hit = self.is_move_dir_hit_scene()
        if is_hit:
            return True
        col_result = self.cannot_inverse_dir_leave()
        is_hit, hit_normal, move_len = col_result
        if not is_hit:
            return True
        return False

    def is_need_check_build_model(self, one_model):
        filename = one_model.filename
        filename = filename.replace('\\', '/')
        path_list = filename.split('/')
        if not path_list:
            return False
        filename = path_list[-1]
        for one_key_word in CLOSE_BUILDING_KEY_WORD:
            if one_key_word in filename:
                return True

        return False

    def filter_outer_col_obj(self, col_obj_list):
        if not col_obj_list:
            return col_obj_list
        filter_col_obj_list = []
        for col_object in col_obj_list:
            if not col_object:
                continue
            one_model = col_object.model
            if not one_model:
                continue
            if self.ev_g_is_in_model(one_model):
                filter_col_obj_list.append(col_object)

        return filter_col_obj_list

    def debug_close_space(self, is_open_log):
        self._is_debug_log = is_open_log

    def is_ignore_col_model(self, filename):
        if not filename:
            return False
        for one_path in IGNORE_DIR_PATHS:
            if one_path in filename:
                return True

        return False

    def check_direction_in_close_space1(self, direction):
        physicalPosition = self.char_ctrl.physicalPosition
        pos1 = physicalPosition
        pos2 = math3d.vector(pos1)
        pos2 = pos2 + direction
        group = collision_const.GROUP_STATIC_SHOOTUNIT
        mask = self.char_ctrl.mask
        filter_type = collision.INCLUDE_FILTER
        result = self.scene.scene_col.hit_by_ray_multi_side(pos1, pos2, 0, group, mask, filter_type)
        is_hit, hit_point, hit_normal, fraction, color, col_object = result
        if not is_hit:
            return False
        else:
            if not hit_normal:
                return False
            inverse_direction = -direction
            dot_value = inverse_direction.dot(hit_normal)
            is_block = dot_value < 0
            if self._is_debug_log and is_block:
                self._is_debug_log = False
                normal_end_point = hit_point + hit_normal * 2 * NEOX_UNIT_SCALE
                line_list = [(pos1, hit_point, 255), (hit_point, normal_end_point, 16711680)]
                self.send_event('E_DRAW_LINE', line_list)
                filename = ''
                model_name = ''
                position = None
                if col_object.model:
                    filename = col_object.model.filename
                    model_name = col_object.model.name
                    position = col_object.model.position
                if self._detect_direction < DETECT_DIRECTIONS_NUM:
                    direction = DETECT_DIRECTIONS[self._detect_direction]
                    is_ignore = self.is_ignore_col_model(filename)
                    print(('test--check_direction_in_close_space1--step1--pos1 =', pos1, '--hit_point =', hit_point))
                    print(('test--check_direction_in_close_space1--step2--hit_point =', hit_point, '--normal_end_point =', normal_end_point))
                    print(('test--check_direction_in_close_space1--step3--dot_value =', dot_value, '--_detect_direction =', self._detect_direction, '--direction =', direction, '--model_col_name =', col_object.model_col_name, '--filename =', filename, '--model_name =', model_name, '--model.position =', position, '--hit_normal =', hit_normal, '--is_ignore =', is_ignore))
                else:
                    print(('test--check_direction_in_close_space1--_detect_direction =', self._detect_direction, '--DETECT_DIRECTIONS_NUM =', DETECT_DIRECTIONS_NUM))
            if is_block:
                pos2 = math3d.vector(pos1)
                pos2 = pos2 - direction
                result = self.scene.scene_col.hit_by_ray_multi_side(pos1, pos2, 0, group, mask, filter_type)
                is_hit, hit_point, hit_normal, fraction, color, inverse_col_object = result
                if not is_hit or not hit_normal:
                    is_block = False
                else:
                    inverse_direction = direction
                    dot_value = inverse_direction.dot(hit_normal)
                    inverse_is_block = dot_value < 0
                    is_block = inverse_is_block
                    if inverse_col_object != col_object:
                        is_block = False
                filename = ''
                if col_object.model:
                    filename = col_object.model.filename
                is_ignore = self.is_ignore_col_model(filename)
                if is_ignore:
                    is_block = False
            return is_block

    def reset(self):
        character = self.sd.ref_character
        if not character:
            return
        character.reset()

    def set_is_enable_test_pos(self, is_enable):
        character = self.sd.ref_character
        if not character:
            return
        if not hasattr(character, 'setIsEnableTestPos'):
            return
        character.setIsEnableTestPos(is_enable)

    def check_in_close_space(self):
        helper_ui = global_data.ui_mgr.get_ui(GMHelperUIFactory.get_gm_helper_ui_name())
        character = self.sd.ref_character
        is_helper_ui_visible = helper_ui and helper_ui.isPanelVisible()
        if not character or not character.isActive() or not self.ev_g_is_parachute_battle_land():
            GMHelperUIFactory.close_gm_helper_ui()
            return False
        if helper_ui and helper_ui.isPanelVisible() and helper_ui.is_in_close_space():
            if self._last_close_direction:
                is_block = self.check_direction_in_close_space1(self._last_close_direction)
                if not is_block:
                    GMHelperUIFactory.close_gm_helper_ui()
                    return False
            return True
        if not self.scene or not self.scene.scene_col or not hasattr(self.scene.scene_col, 'hit_by_ray_multi_side'):
            return False
        if self._detect_direction < 0 or self._detect_direction >= DETECT_DIRECTIONS_NUM:
            self._detect_direction = 0
        direction = DETECT_DIRECTIONS[self._detect_direction]
        self._detect_direction += 1
        is_block = self.check_direction_in_close_space1(direction)
        if is_block and not helper_ui:
            self._last_close_direction = direction
            self.set_is_enable_test_pos(False)
            GMHelperUIFactory.create_gm_helper_ui(in_close_space=True)
        return is_block

    def check_in_close_space_tick(self, *args):
        if global_data.game_mode and not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SURVIVALS, game_mode_const.GAME_MODE_EXERCISE)):
            return
        if not self.is_valid():
            return timer.RELEASE
        if not self.char_ctrl:
            return timer.RELEASE
        self.check_in_close_space()

    def check_ice_river_tick(self, *args):
        if not self.is_valid():
            return
        if not self.char_ctrl:
            return
        if not self.char_ctrl.isActive():
            return
        now_foot_position = self.ev_g_foot_position()
        if not now_foot_position:
            return
        if not self.ev_g_is_cam_target():
            return
        chect_begin = self.char_ctrl.physicalPosition
        check_end = chect_begin + math3d.vector(0, 1, 0) * 16 * NEOX_UNIT_SCALE
        hit_point_list = []
        is_hit = self.hit_by_scene_collision(chect_begin, check_end, ICE_GROUP, TERRAIN_MASK, filter_type=collision.EQUAL_FILTER, is_multi_select=False, hit_point_list=hit_point_list)
        if not is_hit:
            return
        helper_ui = global_data.ui_mgr.get_ui(GMHelperUIFactory.get_gm_helper_ui_name())
        if helper_ui and helper_ui.isPanelVisible() and helper_ui.is_in_close_space():
            return
        GMHelperUIFactory.create_gm_helper_ui()

    def check_overlap_tick(self, *args):
        self.check_ice_river_tick()
        if global_data.game_mode and not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SURVIVALS, game_mode_const.GAME_MODE_EXERCISE)):
            return
        if not self.is_valid():
            return timer.RELEASE
        if not self.char_ctrl:
            return timer.RELEASE
        if not self.char_ctrl.isActive():
            return
        now_foot_position = self.ev_g_foot_position()
        if not now_foot_position:
            return
        if not self.ev_g_is_cam_target() and self.unit_obj.__class__.__name__ != 'LMotorcycle':
            return
        if self.sd.ref_align_on_ground_enabled:
            return
        helper_ui = global_data.ui_mgr.get_ui(GMHelperUIFactory.get_gm_helper_ui_name())
        if helper_ui and helper_ui.isPanelVisible() and helper_ui.is_in_close_space():
            return
        now_time = time.time()
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            pass_time = now_time - self._last_show_gm_ui_time
            if pass_time < SHOW_GM_UI_CD_TIME:
                return
        if self._real_walk_direction.is_zero or not self._last_foot_position:
            self._last_foot_position = now_foot_position
            self._keep_same_pos_start_time = now_time
            return
        diff_vec = now_foot_position - self._last_foot_position
        diff_vec.y = 0
        diff_dist_sqr = diff_vec.length_sqr
        if diff_dist_sqr > NOT_MOVE_DIST_THRESHOLD_SQR:
            if helper_ui and helper_ui.panel.isVisible():
                GMHelperUIFactory.close_gm_helper_ui()
            self._last_foot_position = now_foot_position
            self._keep_same_pos_start_time = now_time
            self._last_stuck_time = 0
            return
        is_hit = self.static_test(self.char_ctrl.group, self.char_ctrl.mask)
        if is_hit:
            is_not_block = False
        else:
            col_result = self.getStaticSweepTest()
            is_hit, hit_normal, move_len = col_result
            is_not_block = True
            if not is_hit:
                if not self._touch_wall:
                    if helper_ui and helper_ui.panel.isVisible():
                        GMHelperUIFactory.close_gm_helper_ui()
                    self._last_foot_position = now_foot_position
                    self._keep_same_pos_start_time = now_time
                    self._last_stuck_time = 0
                    return
                is_not_block = self.test_no_block()
            else:
                if self._touch_wall:
                    is_not_block = self.test_no_block()
                if is_not_block:
                    if helper_ui and helper_ui.panel.isVisible():
                        GMHelperUIFactory.close_gm_helper_ui()
                    self._last_foot_position = now_foot_position
                    self._keep_same_pos_start_time = now_time
                    self._last_stuck_time = 0
                    return
                if helper_ui and helper_ui.panel.isVisible():
                    return
            pass_time = now_time - self._keep_same_pos_start_time
            if pass_time < NOT_MOVE_MAX_DURATION:
                return
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            if not self._last_stuck_time:
                self._last_stuck_time = now_time
                return
            pass_time = now_time - self._last_stuck_time
            if pass_time < SHOW_GM_UI_KEEP_TIME:
                return
        GMHelperUIFactory.create_gm_helper_ui()

    def use_gm_help(self):
        self._last_show_gm_ui_time = time.time()

    def hit_by_scene_collision(self, chect_begin, check_end, group=None, mask=None, filter_type=collision.INCLUDE_FILTER, filter_col_ids=None, is_multi_select=True, col_model_obj_list=None, hit_point_list=None):
        if filter_col_ids is None:
            filter_col_ids = self.ev_g_human_col_id()
        if group is None:
            group = GROUP_CAN_SHOOT
        if mask is None:
            mask = GROUP_CAN_SHOOT
        return character_ctrl_utils.hit_by_scene_collision(chect_begin, check_end, group, mask, filter_type=filter_type, filter_col_ids=filter_col_ids, is_multi_select=is_multi_select, col_model_obj_list=col_model_obj_list, hit_point_list=hit_point_list)

    def on_init_complete(self):
        from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_NONE, STAGE_PLANE
        parachute_stage = self.sd.ref_parachute_stage
        ignore_prachute_stage = parachute_stage in (STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_PLANE, STAGE_NONE)
        if not ignore_prachute_stage:
            self.init_char_ready()
        self.set_gravity(self.get_gravity())

    def init_char_ready(self):
        from logic.units.LAvatar import LAvatar
        from logic.units.LMecha import LMecha
        from logic.units.LMechaTrans import LMechaTrans
        is_avatar = isinstance(self.unit_obj, LAvatar)
        is_mecha = isinstance(self.unit_obj, LMecha)
        is_mechatrans = isinstance(self.unit_obj, LMechaTrans)
        self._acc_key = MECHA_ACC_TYPE if is_mecha else HUMAN_ACC_TYPE
        if is_avatar or is_mecha or is_mechatrans:
            self.cache_gravity_and_wait_detail()
        else:
            self.cache_gravity_and_wait_detail(False)

    def _teleport(self, position):
        self._set_phys_pos_ignore_test(position)

    def _set_phys_pos_ignore_test(self, position):
        if self.char_ctrl and position:
            if hasattr(self.char_ctrl, 'setPhysicalPositionIgnoreTest'):
                self.char_ctrl.setPhysicalPositionIgnoreTest(position)
            else:
                self.char_ctrl.physicalPosition = position

    def get_foot_position(self):
        if not self.char_ctrl:
            return math3d.vector(0, 0, 0)
        foot_position = self.char_ctrl.getFootPosition()
        return foot_position

    def set_foot_position(self, position):
        self._on_set_position_no_inter(position)

    def get_head_position(self):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return math3d.vector(0, 0, 0)
        else:
            if hasattr(char_ctrl, 'getHeadPosition'):
                return char_ctrl.getHeadPosition()
            cur_phy_pos = char_ctrl.physicalPosition
            diff_vec = cur_phy_pos - char_ctrl.getFootPosition()
            head_pos = cur_phy_pos + diff_vec
            return head_pos

        return math3d.vector(0, 0, 0)

    def set_foot_position_by_sync(self, position):
        self._on_set_position_no_inter(position)
        if self.ev_g_is_avatar() and global_data.battle and global_data.channel:
            if global_data.channel.is_south_east_asia_server() or G_TRUNK_PC:
                global_data.battle.on_chunk_changed()

    def _on_set_position_no_inter(self, pos):
        if self.char_ctrl and pos:
            if getattr(self.char_ctrl, 'setFootPositionIgnoreTest', None):
                self.char_ctrl.setFootPositionIgnoreTest(pos)
            else:
                self._set_phys_pos_ignore_test(pos)
                self.char_ctrl.setFootPosition(pos)
        return

    def _on_control_target_change(self, target_id, position, is_in_mecha=False, by_init=False):
        if self.unit_obj.id == target_id:
            if self.sd.ref_is_agent:
                self.send_event('E_FORCE_CHECK_WATER')
                self.try_active()
            elif self.scene and self.scene.check_collision_loaded(position):
                if not is_in_mecha:
                    self.send_event('E_FORCE_CHECK_WATER')
                if self.unit_obj.__class__.__name__ != 'LMotorcycle' or not by_init:
                    self.try_active()
            else:
                self.send_event('E_START_WAITING_CEHCK')
            self._on_set_position_no_inter(position)
        else:
            self.deactivate()

    def get_col_id(self):
        if not self.char_ctrl:
            return
        return self.char_ctrl.cid

    def try_active(self):
        if self.ev_g_is_avatar() and global_data.player and global_data.player.is_in_global_spectate():
            return
        if self.ev_g_is_avatar() and self.ev_g_death():
            return
        if not self._active_waiting:
            self.active()

    def debug_not_move(self):
        foot_position = self.get_foot_position()
        print(('test--debug_not_move--is_in_global_spectate =', global_data.player.is_in_global_spectate(), '--_active_waiting =', self._active_waiting, '--ev_g_is_pure_mecha =', self.ev_g_is_pure_mecha(), '--is_valid =', self.is_valid(), '--scene.valid =', self.scene.valid, '--char_ctrl =', self.char_ctrl, '--is_character_active =', self.is_character_active(), '--foot_position =', foot_position, '--check_collision_loaded =', self.scene.check_collision_loaded(foot_position)))

    def is_limit_height(self):
        char_ctrl = self.char_ctrl
        if hasattr(char_ctrl, 'isLimitHeight'):
            return char_ctrl.isLimitHeight()
        else:
            return self._is_limit_height

    def limit_height(self, height):
        self._is_limit_height = True
        if self.is_valid() and self.char_ctrl:
            self.char_ctrl.limitHeight(height)

    def unlimit_Height(self):
        self._is_limit_height = False
        if self.is_valid() and self.char_ctrl:
            self.char_ctrl.unlimitHeight()

    def get_limit_height(self):
        if hasattr(self.char_ctrl, 'getLimitHeight'):
            return self.char_ctrl.getLimitHeight()
        return 0

    def is_limit_lower_height(self):
        char_ctrl = self.char_ctrl
        if hasattr(char_ctrl, 'isLimitLowerHeight'):
            return char_ctrl.isLimitLowerHeight()
        else:
            return self._is_limit_lower_height

    def limit_lower_height(self, height):
        self._is_limit_lower_height = True
        if self.is_valid() and self.char_ctrl:
            self.char_ctrl.limitLowerHeight(height)
            self._limit_lower_height = height

    def unlimit_lower_Height(self):
        self._is_limit_lower_height = False
        if self.is_valid() and self.char_ctrl:
            self.char_ctrl.unLimitLowerHeight()

    def get_limit_lower_height(self):
        if hasattr(self.char_ctrl, 'getLimitLowerHeight'):
            return self.char_ctrl.getLimitLowerHeight()
        return self._limit_lower_height

    def try_active_force(self):
        self.active()

    def try_deactive_force(self):
        if not self.char_ctrl:
            return
        self.deactivate()

    def _on_defeated(self, *args, **kwargs):
        if self.is_valid():
            self.deactivate()
            self.on_clear_acc_info()

    def _on_revive(self, *args, **kwargs):
        if self.is_valid():
            self.active()
            self.send_event('E_DISABLE_MOVE', False)

    def _release_active_character_timer(self):
        if self._active_character_timer:
            global_data.game_mgr.unregister_logic_timer(self._active_character_timer)
            self._active_character_timer = None
        return

    def _check_scene_collision_ready(self):
        foot_position = self.get_foot_position()
        if self.sd.ref_is_agent:
            return self.scene.check_landscape_has_load_detail_collision(foot_position)
        if not self.scene.check_collision_loaded(foot_position):
            if global_data.battle and foot_position.y < global_data.battle.force_check_height:
                return False
        return True

    def active_char(self, *args, **kwargs):
        scene = self.scene
        if not scene or not scene.valid:
            return
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        is_detect_scene_loaded = True
        if self.ev_g_is_human():
            parachute_stage = self.sd.ref_parachute_stage
            if parachute_stage <= STAGE_FREE_DROP:
                is_detect_scene_loaded = False
        if is_detect_scene_loaded and not self._check_scene_collision_ready():
            self._release_active_character_timer()
            self._active_character_timer = global_data.game_mgr.register_logic_timer(self.try_active, interval=1, times=-1)
            return
        self._release_active_character_timer()
        char_ctrl.activate(scene.scene_col)
        self.send_event('E_CHARACTER_ACTIVE', *args, **kwargs)

    def active(self):
        if self.ev_g_is_pure_mecha() is True:
            return
        if self.is_valid():
            scene = self.scene
            if not scene or not scene.valid:
                return
            char_ctrl = self.char_ctrl
            if not char_ctrl:
                return
            char_ctrl.activate(scene.scene_col)
            self.send_event('E_CHARACTER_ACTIVE')
        else:
            log_error('ComCharacter active when not valid')

    def deactivate(self):
        if not self.is_valid():
            return
        scene = self.scene
        if not scene or not scene.valid:
            return
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        char_ctrl.deactivate(scene.scene_col)
        self.on_clear_acc_info()

    def _get_char_waiting(self):
        return self._active_waiting

    def _set_x_off(self, offset_x):
        if not self.char_ctrl:
            return
        self.char_ctrl.setXOffset(offset_x)

    def _get_x_off(self):
        if not self.char_ctrl:
            return 0
        return self.char_ctrl.getXOffset()

    def _set_y_off(self, offset_y):
        if not self.char_ctrl:
            return
        self.char_ctrl.setYOffset(offset_y)

    def _get_y_off(self):
        if not self.char_ctrl:
            return 0
        return self.char_ctrl.getYOffset()

    def recreate(self, width, height, stepheight):
        import collision
        self.char_ctrl.setRadius(width)
        character_height = character_ctrl_utils.get_character_logic_height(self.char_ctrl, height)
        self.char_ctrl.setHeight(character_height)
        self._collison_height = height
        if self._active_waiting:
            self.try_deactivate()

    def _test_physy_size--- This code section failed: ---

1255       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'collision'
           9  STORE_FAST            2  'collision'

1256      12  LOAD_CONST            2  0.1
          15  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          18  BINARY_MULTIPLY  
          19  STORE_FAST            3  'x'

1257      22  LOAD_CONST            3  0.9
          25  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          28  BINARY_MULTIPLY  
          29  STORE_FAST            4  'y'

1258      32  LOAD_CONST            4  0.5
          35  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          38  BINARY_MULTIPLY  
          39  STORE_FAST            5  'z'

1259      42  LOAD_GLOBAL           2  'math3d'
          45  LOAD_ATTR             3  'vector'
          48  LOAD_FAST             3  'x'
          51  LOAD_FAST             4  'y'
          54  LOAD_FAST             5  'z'
          57  CALL_FUNCTION_3       3 
          60  STORE_FAST            6  'bounding_box'

1260      63  LOAD_GLOBAL           4  'getattr'
          66  LOAD_GLOBAL           5  'None'
          69  LOAD_CONST            0  ''
          72  CALL_FUNCTION_3       3 
          75  POP_JUMP_IF_FALSE   112  'to 112'

1261      78  LOAD_FAST             0  'self'
          81  LOAD_ATTR             6  'scene'
          84  LOAD_ATTR             7  'scene_col'
          87  LOAD_ATTR             8  'remove_object'
          90  LOAD_FAST             0  'self'
          93  LOAD_ATTR             9  '_col'
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          

1262     100  LOAD_CONST            0  ''
         103  LOAD_FAST             0  'self'
         106  STORE_ATTR            9  '_col'
         109  JUMP_FORWARD          0  'to 112'
       112_0  COME_FROM                '109'

1265     112  LOAD_FAST             2  'collision'
         115  LOAD_ATTR            10  'col_object'
         118  LOAD_FAST             2  'collision'
         121  LOAD_ATTR            11  'CAPSULE'
         124  LOAD_FAST             6  'bounding_box'
         127  CALL_FUNCTION_2       2 
         130  LOAD_FAST             0  'self'
         133  STORE_ATTR            9  '_col'

1266     136  LOAD_FAST             0  'self'
         139  LOAD_ATTR            12  'ev_g_foot_position'
         142  CALL_FUNCTION_0       0 
         145  STORE_FAST            7  'position'

1267     148  LOAD_FAST             7  'position'
         151  DUP_TOP          
         152  LOAD_ATTR            13  'y'
         155  LOAD_FAST             6  'bounding_box'
         158  LOAD_ATTR            14  'x'
         161  LOAD_FAST             6  'bounding_box'
         164  LOAD_ATTR            13  'y'
         167  LOAD_CONST            6  2.0
         170  BINARY_DIVIDE    
         171  BINARY_ADD       
         172  INPLACE_ADD      
         173  ROT_TWO          
         174  STORE_ATTR           13  'y'

1268     177  LOAD_FAST             7  'position'
         180  LOAD_FAST             0  'self'
         183  LOAD_ATTR             9  '_col'
         186  STORE_ATTR           15  'position'

1269     189  LOAD_FAST             0  'self'
         192  LOAD_ATTR             6  'scene'
         195  LOAD_ATTR             7  'scene_col'
         198  LOAD_ATTR            16  'add_object'
         201  LOAD_FAST             0  'self'
         204  LOAD_ATTR             9  '_col'
         207  CALL_FUNCTION_1       1 
         210  POP_TOP          
         211  LOAD_CONST            0  ''
         214  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 72

    def _get_character_total_height(self):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return 0
        return char_ctrl.getHeight() + char_ctrl.getRadius() * 2.0 + char_ctrl.getSkinWidth() * 2.0

    def test_body_slope(self):
        rayDir = math3d.vector(0, -20, 0)
        maxDist = rayDir.length
        rayDir.normalize()
        gridSize = 4
        slopes = [0, 0, 0, 0]
        forwardLen = 8
        sideLen = 2
        yaw = self.ev_g_trans_yaw()
        rot_mat = math3d.matrix.make_rotation_y(yaw)
        model_rot = math3d.matrix_to_rotation(rot_mat)
        chRight = model_rot.get_right()
        chForward = model_rot.get_forward()
        chUp = math3d.vector(0, 1, 0)
        chRight.y = 0
        chForward.y = 0
        chRight.normalize()
        chForward.normalize()
        offVecs = [
         chForward * forwardLen + chRight * sideLen + math3d.vector(0, 2, 0),
         chForward * forwardLen - chRight * sideLen + math3d.vector(0, 2, 0),
         -chForward * forwardLen + chRight * sideLen + math3d.vector(0, 2, 0),
         -chForward * forwardLen - chRight * sideLen + math3d.vector(0, 2, 0)]
        pos_list = []
        char_ctrl = self.sd.ref_character
        cur_phy_pos = char_ctrl.physicalPosition
        for one_pos in offVecs:
            start_pos = cur_phy_pos + one_pos
            end_pos = start_pos + math3d.vector(0, 13 * NEOX_UNIT_SCALE, 0)
            one_draw_info = (start_pos, end_pos, 255)

        if hasattr(char_ctrl, 'getHeadPosition'):
            start_pos = char_ctrl.getHeadPosition()
            end_pos = start_pos + math3d.vector(0, 13 * NEOX_UNIT_SCALE, 0)
            one_draw_info = (start_pos, end_pos, 255)
            pos_list.append(one_draw_info)
        self.send_event('E_DRAW_LINE', pos_list)

    def _test_create_character(self):
        import math
        import logic.gcommon.common_const.collision_const as collision_const
        width = 19.5
        height = 38
        padding = 0.13
        added_margin = 0.026
        stepheight = 7.8
        max_slope = 75.0
        jump_speed = 468
        fall_speed = 1170
        gravity = 56
        character_offset_x = 0
        pos_interpolate = 0.5
        character = collision.Character(width, height, stepheight)
        character.setRadius(width)
        character.setHeight(height)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setSmoothFactor(pos_interpolate)
        character.setSlopeCollisionGroup(collision_const.SLOPE_GROUP)
        character.setStepHeight(stepheight)
        character.setJumpSpeed(jump_speed)
        self.set_fall_speed(fall_speed)
        character.setGravity(gravity * self.sd.ref_gravity_scale)
        character.setXOffset(-character_offset_x)
        character.setSmoothFactor(pos_interpolate)
        mask = GROUP_CHARACTER_INCLUDE | GROUP_MECHA_BALL
        group = GROUP_CHARACTER_INCLUDE
        character.filter = ~group
        character.group = ~mask
        self.scene.scene_col.add_character(character)
        foot_position = self.char_ctrl.getFootPosition()
        character.setFootPosition(foot_position)
        return character

    def _init_character(self, bdict):
        import collision
        import math
        from logic.units.LAvatar import LAvatar
        import logic.gcommon.common_const.collision_const as collision_const
        self.del_character()
        width, height, stepheight = CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, 0.6
        max_slope = 60
        padding = 0.001
        added_margin = 0.02
        pos_interpolate = 0.5
        character = collision.Character(width, height, stepheight)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setSmoothFactor(pos_interpolate)
        character.setSlopeCollisionGroup(collision_const.SLOPE_GROUP)
        if self.unit_obj.id == global_data.player.id:
            character.notify_trigger = True
        elif global_data.mecha and global_data.mecha.id == self.unit_obj.id:
            character.notify_trigger = True
        character.enableForceSync = True
        self.scene.scene_col.add_character(character)
        global_data.emgr.scene_add_lift_user_event.emit(character.cid, self.unit_obj.id)
        character_height = character_ctrl_utils.get_character_logic_height(character, height)
        character.setHeight(character_height)
        character.enableLeaveOverlap(self.ev_g_is_avatar())
        self.sd.ref_character = character
        if hasattr(character, 'scene_group'):
            character.scene_group = GROUP_CHARACTER_INCLUDE
        if hasattr(character, 'scene_mask'):
            character.scene_mask = 65535
        if hasattr(character, 'setMinGroundHeight'):
            character.setMinGroundHeight(ai_const.MOVE_MIN_HEIGHT)
        if hasattr(character, 'setUnderGroundHitDist'):
            character.setUnderGroundHitDist(abs(ai_const.MOVE_MIN_HEIGHT * 1.2))
        if hasattr(character, 'setUnderGroundHitStartY'):
            character.setUnderGroundHitStartY(NEOX_UNIT_SCALE * 10)
        if hasattr(character, 'setMaxHorizonDistPerTime'):
            character.setMaxHorizonDistPerTime(NEOX_UNIT_SCALE * 1.6)
        if hasattr(character, 'setMaxSectionCount'):
            character.setMaxSectionCount(15)
        if hasattr(character, 'setIsEnableTestPos'):
            character.setIsEnableTestPos(False)
        use_phys = bdict.get('use_phys', 0)
        is_use_new_behavior = False
        if self.unit_obj.__class__.__name__ == 'LPuppetRobot':
            self.char_ctrl.filter = MASK_CHARACTER_ROBOT
            self.char_ctrl.group = GROUP_CHARACTER_ROBOT
        else:
            self.char_ctrl.filter = GROUP_CHARACTER_INCLUDE | GROUP_MECHA_BALL
            self.char_ctrl.group = GROUP_CHARACTER_INCLUDE
            is_use_new_behavior = True
        if hasattr(character, 'setBehaviorVersion'):
            character.setBehaviorVersion(is_use_new_behavior, is_use_new_behavior)
        if hasattr(character, 'setTestGroundUpMinY'):
            character.setTestGroundUpMinY(0.5)
        self.try_deactivate()
        self.send_event('E_CHRACTER_INITED', self.char_ctrl)

    @property
    def char_ctrl(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl and char_ctrl.valid:
            return char_ctrl
        else:
            return None

    def set_group(self, group):
        character = self._get_character()
        if not character:
            return
        character.group = group

    def get_group(self):
        character = self._get_character()
        if not character:
            return
        return character.group

    def set_mask(self, filter):
        character = self._get_character()
        if not character:
            return
        character.filter = filter

    def get_mask(self):
        character = self._get_character()
        if not character:
            return
        return character.filter

    def on_detail_finished(self, _):
        global_data.emgr.event_finish_detail -= self.on_detail_finished
        self.resume_gravity()

    def cache_gravity_and_wait_detail(self, enable_rewaiting=True):
        if not self.char_ctrl:
            return
        import world
        scn = world.get_active_scene()
        if not hasattr(scn, 'get_detail_done'):
            return
        if scn.get_detail_done():
            return
        self.rewait_detail(enable_rewaiting)

    def rewait_detail(self, enable_rewaiting=True):
        cam_pos = self.scene.active_camera.position
        if self.scene.check_collision_loaded(cam_pos):
            return
        if self._active_waiting:
            return
        self._active_waiting = True
        self.try_deactivate()
        if enable_rewaiting:
            self.scene.recheck_st_percent()
            global_data.emgr.event_finish_detail += self.on_detail_finished

    def try_deactivate(self):
        self._release_active_character_timer()
        if not self.char_ctrl:
            return
        self.deactivate()
        self.send_event('E_CHARACTER_DEACTIVE')

    def resume_gravity(self):
        if not self._active_waiting:
            return
        self._active_waiting = False
        self.try_active()

    def _get_character(self):
        return self.char_ctrl

    def _on_dead(self, *arg):
        if self.is_valid():
            self.deactivate()
            self.on_clear_acc_info()

    def _get_collison_height(self):
        return self._collison_height

    def set_enable_z_capsule(self, enable_z_capsule):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        char_ctrl.enableZCapsule = enable_z_capsule

    def enable_col_wate(self, enable_col_water):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        if not hasattr(char_ctrl, 'enableColWater'):
            return
        char_ctrl.enableColWater(enable_col_water)

    def set_character_direction(self, model_rot):
        char_ctrl = self.char_ctrl
        if not char_ctrl:
            return
        char_ctrl.setCharacterDirection(model_rot)

    def _set_walk_direction(self, walk_direction):
        try:
            self._walk_direction = walk_direction
            acc_rate = 0
            if self._is_in_acc:
                walk_dir_xz = math3d.vector(walk_direction.x, 0, walk_direction.z)
                walk_dir_xz.is_zero or walk_dir_xz.normalize()
                dot_res = walk_dir_xz.dot(self._acc_dir)
                if dot_res > 0:
                    acc_rate = acc_rate + dot_res * get_acc_rate(self._acc_key) if 1 else acc_rate
            if self._is_in_no_dir_acc:
                acc_rate = NO_DIR_ACC_RATE
            other_dirs = math3d.vector(0, 0, 0)
            if self._is_enable_acc:
                for odir in six.itervalues(self._other_walk_direction):
                    other_dirs += odir

                if acc_rate:
                    other_dirs += walk_direction * acc_rate
            self._real_walk_direction = walk_direction + other_dirs
            self.char_ctrl.setWalkDirection(self._real_walk_direction)
        except Exception as e:
            log_error(' _set_walk_direction in ComCharacter')

    def _set_phy_direction(self, walk_direction):
        self._walk_direction = walk_direction
        self._real_walk_direction = walk_direction
        self.char_ctrl.setWalkDirection(walk_direction)

    def _get_walk_direction(self):
        return self._walk_direction

    def _set_walk_direction_force(self, walk_direction_force):
        if not self.char_ctrl:
            return
        if walk_direction_force.is_zero:
            if FORCE_DIRECTION in self._other_walk_direction:
                del self._other_walk_direction[FORCE_DIRECTION]
        else:
            self._other_walk_direction[FORCE_DIRECTION] = walk_direction_force
        self._set_walk_direction(self._walk_direction)

    def _set_walk_direction_train(self, walk_direction):
        from logic.units.LMecha import LMecha
        from logic.units.LMechaTrans import LMechaTrans
        if not self.char_ctrl:
            return
        if walk_direction.is_zero:
            if TRAIN_DIRECTION in self._other_walk_direction:
                del self._other_walk_direction[TRAIN_DIRECTION]
            is_mecha = isinstance(self.unit_obj, LMecha)
            is_mechatrans = isinstance(self.unit_obj, LMechaTrans)
            if is_mecha or is_mechatrans:
                self._set_walk_direction(self._walk_direction)
            elif not self.char_ctrl.isJumping():
                self._set_walk_direction(self._walk_direction)
        else:
            self._other_walk_direction[TRAIN_DIRECTION] = walk_direction
            self._set_walk_direction(self._walk_direction)

    def _set_walk_direction_lift(self, walk_direction):
        from logic.units.LMecha import LMecha
        from logic.units.LMechaTrans import LMechaTrans
        if not self.char_ctrl:
            return
        if walk_direction.y > 0:
            self.char_ctrl.is_ignore_gravity = True
        else:
            self.char_ctrl.is_ignore_gravity = False
        if walk_direction.is_zero:
            if LIFT_DIRECTION in self._other_walk_direction:
                del self._other_walk_direction[LIFT_DIRECTION]
            is_mecha = isinstance(self.unit_obj, LMecha)
            is_mechatrans = isinstance(self.unit_obj, LMechaTrans)
            if is_mecha or is_mechatrans:
                self._set_walk_direction(self._walk_direction)
            elif not self.char_ctrl.isJumping():
                self._set_walk_direction(self._walk_direction)
        else:
            self._other_walk_direction[LIFT_DIRECTION] = walk_direction
            self._set_walk_direction(self._walk_direction)

    def _on_acc_trigger_info_changed(self, is_in_acc, acc_dir, idx):
        old_acc_dir_count = len(self._acc_dir_dict)
        if is_in_acc:
            self._acc_dir_dict[idx] = acc_dir
        elif idx in self._acc_dir_dict:
            del self._acc_dir_dict[idx]
        new_acc_dir_count = len(self._acc_dir_dict)
        self._is_in_acc = new_acc_dir_count > 0
        if self._is_in_acc:
            acc_dir_sum = math3d.vector(0, 0, 0)
            for acc_dir in six.itervalues(self._acc_dir_dict):
                acc_dir_sum += acc_dir

            acc_dir_sum.normalize()
            self._acc_dir = acc_dir_sum
        else:
            self._acc_dir = math3d.vector(0, 0, 0)
        self.sd.ref_is_in_acc = self._is_in_acc
        self.sd.ref_acc_dir = self._acc_dir
        self._set_walk_direction(self._walk_direction)
        if new_acc_dir_count == 1 and old_acc_dir_count == 0:
            self.send_event('E_CALL_SYNC_METHOD', 'trigger_enter_accelerate_box', (machine_const.MACHINE_TYPE_ACC_ONEWAY,))
        elif new_acc_dir_count == 0 and old_acc_dir_count == 1:
            if not self._is_in_no_dir_acc:
                self.send_event('E_CALL_SYNC_METHOD', 'trigger_leave_accelerate_box', (machine_const.MACHINE_TYPE_ACC_ONEWAY,))

    def _on_no_dir_acc_trigger_info_changed(self, is_in_acc, idx):
        if is_in_acc:
            self._no_dir_acc_dir_dict[idx] = True
        elif idx in self._no_dir_acc_dir_dict:
            del self._no_dir_acc_dir_dict[idx]
        self._is_in_no_dir_acc = len(self._no_dir_acc_dir_dict) > 0
        self.sd.ref_is_in_no_dir_acc = self._is_in_no_dir_acc
        self._set_walk_direction(self._walk_direction)
        if self._is_in_no_dir_acc:
            self.send_event('E_CALL_SYNC_METHOD', 'trigger_enter_accelerate_box', (machine_const.MACHINE_TYPE_ACC_TWOWAY,))
        elif not self._is_in_acc:
            self.send_event('E_CALL_SYNC_METHOD', 'trigger_leave_accelerate_box', (machine_const.MACHINE_TYPE_ACC_TWOWAY,))

    def on_clear_acc_info(self):
        self._is_in_acc = False
        self.sd.ref_is_in_acc = False
        self._is_in_no_dir_acc = False
        self.sd.ref_is_in_no_dir_acc = False
        self._acc_dir_dict = {}
        self._no_dir_acc_dir_dict = {}
        self._other_walk_direction = {}
        char_ctrl = self.char_ctrl
        if char_ctrl:
            char_ctrl.is_ignore_gravity = False
        if self.lift:
            self.lift.send_event('E_UPDATE_LIFT_USER', self.char_ctrl.cid, self.unit_obj, False)

    def enable_acc_info(self, enable):
        self._is_enable_acc = enable

    def get_on_lift(self, lift, get_on):
        self.lift = lift if get_on else None
        return

    def is_in_lift(self):
        return self.lift is not None

    def on_ignore_gravity(self, ignore):
        self.char_ctrl.is_ignore_gravity = ignore