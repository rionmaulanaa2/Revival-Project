# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComPhantomCtrl.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.utils.timer import RELEASE, CLOCK
import world
import math3d
import math
import time
import random
import collision
import game3d
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_EXCLUDE, SLOPE_GROUP, CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, GROUP_CHARACTER_INCLUDE, MASK_CHARACTER_ROBOT, GROUP_CHARACTER_ROBOT, GROUP_MECHA_BALL, GROUP_DEFAULT_VISIBLE
from logic.gcommon.const import NEOX_UNIT_SCALE, CHARACTER_LERP_DIR_YAWS
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, MECHA_FASHION_KEY
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from logic.gutils.character_ctrl_utils import get_character_logic_height
from logic.gcommon.common_const.ai_const import MOVE_MIN_HEIGHT
from logic.client.const import game_mode_const
from logic.gcommon.common_const.collision_const import MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y, STAND_MODEL_OFFSET_X
from ....cdata import state_physic_arg
from common.cfg import confmgr
from logic.gutils.dress_utils import get_mecha_model_offset_y, battle_id_to_mecha_lobby_id
from logic.gcommon.component.client.ComCharacter import CC_COLLISION_SIDES
from logic.gcommon.common_utils.bcast_utils import E_UPDATE_PHANTOM_STATE
MIN_DIS = 1.0 * NEOX_UNIT_SCALE
STATE_NONE = 0
STATE_RUN = 1
STATE_IDLE = 2

class ComPhantomCtrl(UnitCom):
    BIND_EVENT = {'G_IS_AVATAR': 'get_is_avatar',
       'G_IS_CAMPMATE': 'get_is_same_team',
       'G_IS_HUMAN': 'get_is_human',
       'E_8029_PHANTOM_START_DESTROY': 'on_destroy_start',
       'G_CHARACTER_CID': 'get_character_cid',
       'G_PHANTOM_YAW': 'get_yaw',
       'E_SET_PHANTOM_POS': '_set_phantom_pos'
       }

    def __init__(self):
        super(ComPhantomCtrl, self).__init__(need_update=False)
        self._phantom_char_ctrl = None
        self._last_position = None
        self._timer = None
        self._model = None
        self._state = STATE_NONE
        self._yaw = None
        self._agent_id = None
        self._touch_wall = False
        self._last_foot_pos = math3d.vector(0, 0, 0)
        self._last_check_time = None
        self._speed = 0
        self._extra_info = {}
        self._entity_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPhantomCtrl, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_is_mecha = True
        self.sd.ref_owner_id = bdict.get('owner_eid', None)
        self._extra_info = bdict.get('extra_info', {})
        self._speed = self._extra_info.get('speed', 100)
        self._slope_add = self._extra_info.get('slope_add', 0.0)
        self._stepheight_add = self._extra_info.get('stepheight_add', 0.0)
        self._yaw = bdict.get('yaw', 0)
        self._state = bdict.get('state', STATE_RUN)
        self._entity_id = unit_obj.id
        pos = bdict.get('position', None)
        self._last_foot_pos = math3d.vector(*pos)
        if bdict.get('mecha_id') != 8023:
            self._init_screen_mark()
        self._init_extra_coms()
        self._init_phantom_character()
        self._init_position(pos)
        return

    def _init_screen_mark(self):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == self.sd.ref_owner_id:
            global_data.emgr.add_entity_screen_mark.emit(self._entity_id, 'battle_mech/fight_hit_mech8029_mark', True)

    def _init_extra_coms(self):
        if global_data.cam_lplayer and global_data.cam_lplayer.id != self.sd.ref_owner_id:
            add_coms = ('ComMoveSyncReceiver2', 'ComInterpolater')
        else:
            add_coms = ('ComMoveSyncSender2', )
        for add_com in add_coms:
            if not self.unit_obj.get_com(add_com):
                com = self.unit_obj.add_com(add_com, 'client')
                com.init_from_dict(self.unit_obj, {})
                com.on_init_complete()
                com.on_post_init_complete({})

        self.send_event('E_ENABLE_SYNC', True)

    def _init_phantom_character(self):
        if not global_data.cam_lplayer or global_data.cam_lplayer.id != self.sd.ref_owner_id:
            return
        else:
            if not self.sd.ref_character:
                return
            character = self.sd.ref_character
            physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
            mecha_id = self.sd.ref_mecha_id
            physic_conf = physic_conf[str(mecha_id)]
            stepheight = (physic_conf['step_height'] + self._stepheight_add) * NEOX_UNIT_SCALE
            max_slope = physic_conf['max_slope'] + self._slope_add
            if global_data.game_mode.is_mode_type(game_mode_const.TDM_MaxSlop):
                max_slope = physic_conf['max_slope_death']
            enable_z_capsule = physic_conf.get('enable_z_capsule', 0)
            enable_z_capsule = bool(enable_z_capsule)
            padding = state_physic_arg.padding * NEOX_UNIT_SCALE
            added_margin = state_physic_arg.added_margin * NEOX_UNIT_SCALE
            pos_interpolate = state_physic_arg.pos_interpolate
            jump_speed = physic_conf['jump_speed'] * NEOX_UNIT_SCALE
            gravity = physic_conf['gravity'] * NEOX_UNIT_SCALE
            fall_speed = physic_conf['max_fall_speed'] * NEOX_UNIT_SCALE
            character_offset_x = STAND_MODEL_OFFSET_X
            width = physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2
            height = physic_conf['character_size'][1] * NEOX_UNIT_SCALE
            self.send_event('E_RECREATE_CHARACTER', width, height, 0.6)
            character.setPadding(padding)
            character.setAddedMargin(added_margin)
            character.setMaxSlope(math.radians(max_slope))
            character.setSmoothFactor(pos_interpolate)
            character.setSlopeCollisionGroup(SLOPE_GROUP)
            character.setStepHeight(stepheight)
            character.setJumpSpeed(jump_speed)
            character.setFallSpeed(fall_speed)
            character.setGravity(gravity)
            character.setXOffset(-character_offset_x)
            character.enableFollow = False
            model_offset_y = self.get_model_offset_y() or 0
            if enable_z_capsule:
                self.character_down_height = width / 2 + model_offset_y
            else:
                self.character_down_height = height / 2 + model_offset_y
            character.setYOffset(-self.character_down_height)
            character.enableForceSync = True
            character_height = get_character_logic_height(character, height)
            character.setHeight(character_height)
            character.filter = GROUP_CHARACTER_EXCLUDE
            character.group = GROUP_CHARACTER_INCLUDE
            if hasattr(character, 'scene_group'):
                character.scene_group = GROUP_CHARACTER_INCLUDE
            if hasattr(character, 'scene_mask'):
                character.scene_mask = 65535
            if hasattr(character, 'setMinGroundHeight'):
                character.setMinGroundHeight(MOVE_MIN_HEIGHT)
            if hasattr(character, 'setUnderGroundHitDist'):
                character.setUnderGroundHitDist(abs(MOVE_MIN_HEIGHT * 1.2))
            if hasattr(character, 'setUnderGroundHitStartY'):
                character.setUnderGroundHitStartY(NEOX_UNIT_SCALE * 10)
            if hasattr(character, 'setMaxHorizonDistPerTime'):
                character.setMaxHorizonDistPerTime(NEOX_UNIT_SCALE * 1.6)
            if hasattr(character, 'setMaxSectionCount'):
                character.setMaxSectionCount(15)
            if hasattr(character, 'setIsEnableTestPos'):
                character.setIsEnableTestPos(False)
            if getattr(character, 'setMaxPushDist', None):
                character.setMaxPushDist(0.5 * NEOX_UNIT_SCALE)
            if hasattr(character, 'setBehaviorVersion'):
                character.setBehaviorVersion(True, True)
            if hasattr(character, 'setTestGroundUpMinY'):
                character.setTestGroundUpMinY(0.5)
            self._phantom_char_ctrl = character
            self.scene.scene_col.add_character(character)
            global_data.emgr.scene_add_lift_user_event.emit(character.cid, self.unit_obj.id)
            self._on_agent()
            return

    def _init_position(self, pos):
        if pos:
            pos = math3d.vector(*pos)
        else:
            pos = self.ev_g_position()
        if pos:
            pos.y = pos.y + 0.5 * NEOX_UNIT_SCALE
            self.send_event('E_FOOT_POSITION', pos)

    def get_model_offset_y(self):
        return -get_mecha_model_offset_y(self.ev_g_mecha_fashion_id())

    def update_character_pos(self, pos, *args):
        self._last_foot_pos = pos

    def on_pos_changed(self, pos, *args):
        if math.isinf(pos.x) or math.isinf(pos.y) or math.isinf(pos.y) or math.isnan(pos.x) or math.isnan(pos.y) or math.isnan(pos.y):
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)

    def _update_phantom_state(self, state):
        self._state = state
        if self._state == STATE_RUN:
            walk_dir = math3d.matrix.make_rotation_y(self._yaw).forward
            walk_dir_xz = math3d.vector(walk_dir.x, 0, walk_dir.z)
            if not walk_dir_xz.is_zero:
                walk_dir_xz.normalize()
            self._phantom_char_ctrl.setWalkDirection(walk_dir_xz * self._speed)
        elif self._state == STATE_IDLE:
            self._phantom_char_ctrl.setWalkDirection(math3d.vector(0, 0, 0))
        self.send_event('E_UPDATE_PHANTOM_STATE', self._state)

    def on_sides_callback(self, hit_flags, *args):
        self._touch_wall = hit_flags & CC_COLLISION_SIDES != 0

    def _check_stop(self):
        if self._state == STATE_IDLE:
            return
        if not self._phantom_char_ctrl:
            return
        if not self._last_foot_pos:
            self._last_foot_pos = self._phantom_char_ctrl.getFootPosition()
            return
        d_pos = self._phantom_char_ctrl.getFootPosition() - self._last_foot_pos
        if d_pos.length < self._speed * 0.2 and self._touch_wall:
            self.set_phantom_state(STATE_IDLE)
        self._last_foot_pos = self._phantom_char_ctrl.getFootPosition()

    def set_phantom_state(self, state):
        self._state = state
        self._update_phantom_state(self._state)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_UPDATE_PHANTOM_STATE, (self._state,)], True)

    def destroy(self):
        self.clear_timer()
        global_data.emgr.del_entity_screen_mark.emit(self._entity_id)
        super(ComPhantomCtrl, self).destroy()

    def get_is_avatar(self):
        return False

    def get_character_cid(self):
        if self._phantom_char_ctrl:
            return self._phantom_char_ctrl.cid
        else:
            return None

    def get_is_same_team(self, *args):
        return True

    def get_is_human(self):
        return False

    def get_yaw(self):
        return self._yaw

    def active_character(self):
        if not self._phantom_char_ctrl:
            return
        self._phantom_char_ctrl.setOnSidesCallback(self.on_sides_callback)
        self._phantom_char_ctrl.setPositionChangedCallback(self.on_pos_changed)
        self.send_event('E_FORCE_ACTIVE')
        self.send_event('E_FOOT_POSITION', self._last_foot_pos)

    def inactive_character(self):
        if not self._phantom_char_ctrl:
            return
        else:
            self.regist_pos_change(self.update_character_pos)
            self._phantom_char_ctrl.setOnSidesCallback(None)
            self._phantom_char_ctrl.setPositionChangedCallback(None)
            self._phantom_char_ctrl.setWalkDirection(math3d.vector(0, 0, 0))
            self.send_event('E_FORCE_DEACTIVE')
            return

    def _on_agent(self, *args):
        self._update_phantom_state(self._state)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_UPDATE_PHANTOM_STATE, (self._state,)], True)
        self.clear_timer()
        self.active_character()
        self._timer = global_data.game_mgr.register_logic_timer(self._check_stop, interval=0.2, times=-1, mode=CLOCK)

    def _on_cancel_agent(self, *args):
        self.inactive_character()
        self.clear_timer()

    def clear_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def _on_set_agent_from_server(self, agent_id):
        self._agent_id = agent_id
        if not self._agent_id and self._phantom_char_ctrl:
            self._phantom_char_ctrl.setWalkDirection(math3d.vector(0, 0, 0))
            self.send_event('E_FOOT_POSITION', self._last_foot_pos)

    def _set_phantom_pos(self, pos):
        if not global_data.cam_lplayer or global_data.cam_lplayer.id != self.sd.ref_owner_id:
            return
        if not self._phantom_char_ctrl:
            return
        self.set_phantom_state(STATE_IDLE)
        self.send_event('E_FOOT_POSITION', math3d.vector(pos[0], pos[1], pos[2]))

    def on_destroy_start(self):
        if self._phantom_char_ctrl:
            self._phantom_char_ctrl.setWalkDirection(math3d.vector(0, 0, 0))