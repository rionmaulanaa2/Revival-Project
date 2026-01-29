# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGrenadeCollision.py
from __future__ import absolute_import
from . import ComWeaponCollisionBase
import math3d
import math
import time
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.weapon_const import THROWABLE_TRIGGER_COLLISION, THROWABLE_TRIGGER_ENTITY, WP_SUMMON_GRENADES_GUN, THROWABLE_TRIGGER_TIME
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, GROUP_CHARACTER_INCLUDE, GROUP_AUTO_AIM, GROUP_SHIELD, GROUP_GRENADE, GROUP_DYNAMIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT, GROUP_SHOOTUNIT
from logic.gutils.scene_utils import is_break_obj
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from logic.gcommon.common_const import mecha_const
from math import pi, cos, sin
from logic.gcommon.common_const.attr_const import ATTR_COL_RADIUS, WEAPON_PIERCE_CNT, MECHA_WEAPON_TOTAL_ANGLE_SUB_RATE, ATTR_SUB_WP_PELLET_NUM, ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR
from logic.gutils import team_utils
from logic.gcommon.common_const import weapon_const
from .ComObjCollision import ignore_lod_collisions
import collision
from logic.gcommon.common_const import collision_const
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon.common_const import buff_const as bconst
UP_VECTOR = math3d.vector(0, 1, 0)

class ComGrenadeCollision(ComWeaponCollisionBase.ComWeaponCollisionBase):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'G_POSITION': 'get_position',
       'G_COL_RADIUS_RATE': 'get_col_radius_rate',
       'E_POSITION': '_on_position_changed',
       'S_DIRECTION': '_on_direction_changed',
       'E_ON_ATTACH_EXPLOSIVE': ('attach_mecha', 99),
       'G_CHECK_PIERCE': '_check_pierce'
       }
    MIN_DELTA_DIST = 0.5
    DELAY_UPDATE_FRAME_COUNT = 30
    DYNAMIC_CHECK_FRAME = 1
    COLLIDE_SOUND_INTERVAL = 0.2
    COLLIDE_SOUND_SPEED_LIMIT = 100
    SIDE_LEFT = -1
    SIDE_RIGHT = 1

    def init_from_dict(self, unit_obj, bdict):
        self.throw_info = {}
        self.throw_info.update(bdict)
        self.item_type = self.throw_info['item_itype']
        self.item_kind = self.throw_info.get('item_kind', None)
        self.count_down_frame_cnt = -1
        self._left_time = 1000
        self._trigger_type = None
        self._max_distance = 0.0
        self._max_height = 0
        self._sink_speed = 0
        self._restitution = 1
        self._gravity = None
        self._distance_for_gravity = 0
        self._target_logic = None
        self._impulse_power = 0
        self._impulse_range = 0
        self._owner_id = bdict['owner_id']
        self._original_pos = None
        self._ignore_fire_pos = False
        self._contact_other_col_times = 0
        self._max_contact_other_col_times = confmgr.get('grenade_config', str(self.item_type), 'iBoundCount', default=0)
        self._hit_sfx_use_dir_normal = confmgr.get('grenade_res_config', str(self.item_type), 'iSfxUseDirAsNormal', default=0)
        self.init_main_weapon_func = {weapon_const.WP_ARROWS_GUN: self.init_main_arrow_phy
           }
        self.init_sub_weapon_func = {weapon_const.WP_GRENADES_GROUP_GUN: self.init_sub_grenade_phy,
           weapon_const.WP_ARROWS_GROUP_GUN: self.init_sub_arrow_group_phy,
           weapon_const.WP_ARROWS_GUN: self.init_sub_arrow_phy,
           weapon_const.WP_GRENADES_CROWD_GUN: self.init_child_grenade_phy
           }
        self.tick_sub_weapon_func = {weapon_const.WP_GRENADES_GROUP_GUN: self.tick_sub_grenade,
           weapon_const.WP_ARROWS_GROUP_GUN: self.tick_sub_arrow,
           weapon_const.WP_ARROWS_GUN: self.tick_sub_arrow,
           weapon_const.WP_GRENADES_CROWD_GUN: self.tick_child_grenade
           }
        self._is_sub_weapon = False
        self.check_model_col_same_dir_count = 2
        self.pure_last_pos = None
        self.change_forward_dist_threshold = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={}).get('change_forward_dist_threshold', 0) * NEOX_UNIT_SCALE
        self.last_update_time = 0
        self.last_pos = math3d.vector(0, 0, 0)
        self._col_objs = []
        self.post_contact_timer = None
        conf = self.throw_info
        if conf.get('trigger_id', None):
            trigger_id = conf['trigger_id']
            target = EntityManager.getentity(trigger_id)
            self._target_logic = target.logic
            self._col_ids = self._target_logic.ev_g_human_col_id()
            shield_id = self._target_logic.share_data.ref_mecha_shield_col_id
            if shield_id:
                self._col_ids.append(shield_id)
            relative_ids = target.logic.share_data.ref_mecha_relative_cols
            if relative_ids:
                self._col_ids.extend(relative_ids)
        else:
            self._col_ids = []
        self._save_collision_time = time.time()
        self._gernade_id = global_data.sound_mgr.register_game_obj('gernade')
        self._gernade_player_id = None
        self._is_collision_enable = True
        self._collision_enable_downcount = 0
        self.tm = global_data.game_mgr.get_logic_timer()
        self._collide_sound = confmgr.get('grenade_res_config', str(self.item_type), 'cCollideSound', default=None)
        self._ignore_unit_tag = None
        super(ComGrenadeCollision, self).init_from_dict(unit_obj, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_position_changed)
        self.qte_info = {}
        self.iKind = 0
        self.sd.ref_col_obj = None
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        if info.get('ignore_faction'):
            self.faction_id = None
        self._auto_intrp_rot = info.get('need_update_rotation', False)
        return

    def set_group_and_mask(self, obj):
        super(ComGrenadeCollision, self).set_group_and_mask(obj)
        if str(self.item_type) == weapon_const.SNATCHEGG_THROW_ITEM:
            obj.group = collision_const.GROUP_MECHA_BALL
            obj.mask = collision_const.GROUP_CAN_SHOOT | collision_const.GROUP_SHIELD | collision_const.WATER_GROUP | collision_const.GROUP_MECHA_BALL | collision_const.GROUP_CAMERA_COLL

    def cache(self):
        self._stop_sound()
        self.stop_post_contact_timer()
        self._is_collision_enable = False
        super(ComGrenadeCollision, self).cache()

    def init_sub_grenade_phy(self, direction, conf):
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        self._spread_time = info.get('time') or 0.5
        self._spread_radius = (info.get('radius') or 3) * NEOX_UNIT_SCALE
        self._angular_speed = (info.get('angle_speed') or 1) * pi
        self._radius_speed = (info.get('radius_speed') or 1) * NEOX_UNIT_SCALE * (1 + conf.get('radius_speed_add_rate', 0))
        self._raidus = 0.5 * NEOX_UNIT_SCALE
        self._forward = direction
        self._right = UP_VECTOR.cross(direction)
        self._up = self._forward.cross(self._right)
        self._right.normalize()
        self._up.normalize()
        self._fly_time = 0
        angle_para = 2.0
        owner = EntityManager.getentity(self._owner_id)
        if owner and owner.logic:
            wp_pos = conf.get('wp_pos')
            wp = owner.logic.ev_g_wpbar_get_by_pos(wp_pos)
            if wp:
                pellet = wp.get_bullet_pellets()
                angle_para = (pellet - 1) / 2.0
        self._rad = conf['sub_idx'] / angle_para * pi
        self._col_obj.position = self._col_obj.position + (self._right * cos(self._rad) + self._up * sin(self._rad)) * self._raidus
        self._product_radius_angle = self._raidus * self._angular_speed

    def init_child_grenade_phy(self, direction, conf):
        self._side = self.SIDE_LEFT if conf['sub_idx'] % 2 else self.SIDE_RIGHT
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        self._min_gap = info.get('min_gap', 0) * NEOX_UNIT_SCALE
        self._max_gap = info.get('max_gap', 0) * NEOX_UNIT_SCALE
        self._spread_time = info.get('time') or 0.5
        self._spread_speed = info.get('speed', 0) * NEOX_UNIT_SCALE
        self._forward = direction
        self._right = UP_VECTOR.cross(direction)
        self._up = self._forward.cross(self._right)
        self._right.normalize()
        self._up.normalize()
        self._fly_time = 0
        self._col_obj.position = self._col_obj.position + self._right * self._side * self._min_gap

    def init_main_arrow_phy(self, direction, conf):
        weapon_state_info = conf.get('weapon_state_info', {})
        if not weapon_state_info:
            return
        else:
            info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
            rate = info.get('rate', 1.0)
            sub_state = weapon_state_info.get('sub_state', 0)
            right = UP_VECTOR.cross(direction)
            up = direction.cross(right)
            right_dir = None
            if sub_state == 1:
                right_dir = 1
            elif sub_state == 2:
                right_dir = -1
            elif sub_state == 3:
                right_dir = 1
            if self.model and self._col_obj:
                rotation = math3d.matrix_to_rotation(math3d.matrix.make_rotation(direction, -1 * right_dir * math.atan(rate / 1)))
                up = rotation.rotate_vector(up)
                self.model.rotation_matrix = math3d.matrix.make_orient(direction, up)
                self._col_obj.rotation_matrix = self.model.rotation_matrix
            return

    def init_sub_arrow_group_phy(self, direction, conf):
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        item_type = self.throw_info['item_itype']
        trigger_id = self.throw_info.get('trigger_id', None)
        trigger = self.battle.get_entity(trigger_id)
        angle_sub_rate = 0
        if trigger and trigger.logic:
            angle_sub_rate = trigger.logic.ev_g_add_attr(MECHA_WEAPON_TOTAL_ANGLE_SUB_RATE, item_type)
        if angle_sub_rate is None:
            angle_sub_rate = 0
        total_angle = info.get('total_angle', 1.57) * (1 - angle_sub_rate)
        custom_pellet = None
        if trigger and trigger.logic:
            custom_pellet = trigger.logic.ev_g_add_attr(ATTR_SUB_WP_PELLET_NUM, item_type)
        pellets = custom_pellet or conf['pellets'] - 1
        sub_idx = conf['sub_idx']
        sub_angle = total_angle / pellets
        pellets /= 2.0
        right = UP_VECTOR.cross(direction)
        up = direction.cross(right)
        offset = 1 if pellets >= sub_idx else 0
        sub_angle *= pellets - sub_idx + offset
        rotation = math3d.matrix_to_rotation(math3d.matrix.make_rotation(up, sub_angle))
        new_direction = rotation.rotate_vector(direction)
        direction.x, direction.y, direction.z = new_direction.x, new_direction.y, new_direction.z
        return

    def init_sub_arrow_phy(self, direction, conf):
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        total_angle = info.get('total_angle', 1.57)
        rate = info.get('rate', 1.0)
        weapon_state_info = conf.get('weapon_state_info', {})
        sub_state = weapon_state_info.get('sub_state', 0)
        pellets = conf['pellets'] - 1
        sub_idx = conf['sub_idx']
        pellets /= 2
        sub_angle = total_angle / pellets
        offset = 1 if pellets >= sub_idx else 0
        right = UP_VECTOR.cross(direction)
        up = direction.cross(right)
        if sub_state == 3:
            sub_angle *= (pellets - sub_idx) / 2 + offset
        else:
            sub_angle *= pellets - sub_idx + offset
        right_dir = None
        if sub_state == 1:
            right_dir = 1
        elif sub_state == 2:
            right_dir = -1
        elif sub_state == 3:
            right_dir = 1 if sub_idx % 2 == 0 else -1
        rotation = math3d.matrix_to_rotation(math3d.matrix.make_rotation(up, sub_angle))
        new_direction = rotation.rotate_vector(direction)
        if right_dir:
            rotation = math3d.matrix_to_rotation(math3d.matrix.make_rotation(right * right_dir, sub_angle * rate))
            new_direction = rotation.rotate_vector(new_direction)
            if self.model and self._col_obj:
                rotation = math3d.matrix_to_rotation(math3d.matrix.make_rotation(new_direction, -1 * right_dir * math.atan(rate / 1)))
                up = rotation.rotate_vector(up)
                self.model.rotation_matrix = math3d.matrix.make_orient(new_direction, up)
                self._col_obj.rotation_matrix = self.model.rotation_matrix
        direction.x, direction.y, direction.z = new_direction.x, new_direction.y, new_direction.z
        return

    def init_physical_parameters(self):
        conf = self.throw_info
        cobj = self._col_obj
        m = self._model()
        item_conf = confmgr.get('grenade_config', str(self.item_type))
        self._trigger_type = item_conf['iTriggerType']
        self._sink_speed = item_conf['fSinkSpeed']
        self._max_distance = item_conf['fMaxDistance']
        trigger_id = self.throw_info.get('trigger_id', None)
        trigger = self.battle.get_entity(trigger_id)
        if trigger and trigger.logic:
            self._max_distance *= 1.0 + trigger.logic.ev_g_add_attr(ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR, self.item_type)
        self._max_height = item_conf.get('bMaxHeight', 0)
        harm_config = confmgr.get('break_data', str(self.item_type), default={})
        self._impulse_power = harm_config.get('cBreakPower', 0) if harm_config else 0
        self._impulse_range = harm_config.get('fBreakRange', 0) * NEOX_UNIT_SCALE
        dir_data = conf.get('dir', (0, 0, 1))
        direction = math3d.vector(*dir_data)
        if 'sub_idx' not in conf and self.item_kind in self.init_main_weapon_func:
            self.init_main_weapon_func[self.item_kind](direction, conf)
        if 'sub_idx' in conf and self.item_kind in self.init_sub_weapon_func:
            self._is_sub_weapon = True
            self.init_sub_weapon_func[self.item_kind](direction, conf)
        throw_speed_add_rate = conf.get('throw_speed_add_rate', 0)
        throw_speed_add_rate = throw_speed_add_rate if throw_speed_add_rate else 0
        speed_factor = 1 + throw_speed_add_rate
        speed = direction * conf['speed'] * speed_factor
        cobj.mass = conf['mass']
        gravity = conf['gravity']
        cobj.disable_gravity(True)
        if gravity <= 0:
            cobj.disable_gravity(True)
        else:
            self._gravity = math3d.vector(0, -gravity * conf['mass'] * 1.8, 0)
            self._distance_for_gravity = item_conf['DistanceForGravity']
            if self._distance_for_gravity == 0:
                cobj.apply_force(self._gravity)
        cobj.static_friction = item_conf['fStaticFriction']
        cobj.dynamic_friction = item_conf['fDynamicFriction']
        cobj.restitution = 1
        cobj.enable_ccd = True
        self._restitution = item_conf['fRestitution']
        custom_param = item_conf.get('cCustomParam', {})
        self.is_pierced = custom_param.get('pierced', 0)
        cobj.set_damping(item_conf['fLinearDamp'], item_conf['fLangularDamp'])
        self.left_pierce_cnt = 9999 if self.is_pierced else 0
        limited_pierce_cnt = self.get_limited_pierce_cnt()
        if limited_pierce_cnt > 0:
            self.left_pierce_cnt += limited_pierce_cnt
        elif limited_pierce_cnt < 0:
            self.left_pierce_cnt = 0
        self._col_obj.set_damping(item_conf['fLinearDamp'], item_conf['fLangularDamp'])
        cobj.set_linear_velocity(speed)
        bullet_type = self.item_type
        if bullet_type:
            special_sfx_path_list = confmgr.get('break_data', str(bullet_type), default={}).get('cBreakBulletHit')
            if special_sfx_path_list:
                cobj.enable_ccd = True
        ignore_unit_tag = custom_param.get('ignore_unit_tag', None)
        if ignore_unit_tag:
            self._ignore_unit_tag = register_unit_tag(ignore_unit_tag)
        if self._trigger_type == THROWABLE_TRIGGER_TIME:
            self._col_obj.group = collision_const.REGION_BOUNDARY_SCENE_GROUP
            self._col_obj.mask = collision_const.REGION_BOUNDARY_SCENE_MASK
        return

    def _create_col_obj(self):
        if not self.is_enable():
            return
        else:
            iType = self.throw_info.get('iType', 1)
            if iType == mecha_const.SELF_DESTRUCT:
                return
            if self._model:
                m = self._model() if 1 else None
                return m or None
            collision_type = collision.SPHERE
            item_type = self.throw_info['item_itype']
            item_conf = confmgr.get('grenade_config', str(item_type))
            if item_conf:
                ini_radius = item_conf['fCollisionRadius']
                if type(ini_radius) == list:
                    if self.throw_info.get('in_aim', False):
                        ini_radius = float(ini_radius[1]) if 1 else float(ini_radius[0])
                    radius_add_rate = self.get_col_radius_rate()
                    radius = ini_radius * (1 + radius_add_rate)
                    if 'accumulate_rate' in self.throw_info:
                        add_rate = item_conf.get('cCustomParam', {}).get('max_acc_add_radius_rate', 0.0) * self.throw_info['accumulate_rate']
                        radius *= 1.0 + add_rate
                    self._radius = radius
                    bounding_box = math3d.vector(radius, radius, radius)
                else:
                    bounding_box = math3d.vector(3, 3, 3)
                self._ignore_fire_pos = confmgr.get('firearm_config', str(item_type), 'iIgnoreFirePos')
                position = self.throw_info['position']
                self.collision_type_mask = item_conf['iCollisionTypeMask']
                self._col_obj = collision.col_object(collision_type, bounding_box, 0, 0, 1)
                self.sd.ref_col_obj = self._col_obj
                self.set_group_and_mask(self._col_obj)
                self._col_obj.position = position
                self._original_pos = self._col_obj.position
                self._last_check_pos = self._original_pos
                self.pure_last_pos = self._col_obj.position
                if not self._ignore_fire_pos and self._target_logic and self._target_logic.sd.ref_is_mecha:
                    direction = self.throw_info['dir']
                    direction = math3d.vector(direction[0], direction[1], direction[2])
                    direction.is_zero or direction.normalize()
                    self._last_check_pos = self._original_pos - direction * 4.0 * NEOX_UNIT_SCALE
            self._col_obj.rotation_matrix = m.rotation_matrix
            self._col_obj.is_explodable = True
            self.scene.scene_col.add_object(self._col_obj)
            return

    def get_col_radius_rate(self):
        item_type = self.throw_info['item_itype']
        trigger_id = self.throw_info.get('trigger_id', None)
        trigger = self.battle.get_entity(trigger_id)
        radius_add_rate = 0
        if trigger and trigger.logic:
            radius_add_rate = trigger.logic.ev_g_add_attr(ATTR_COL_RADIUS, item_type)
        if radius_add_rate is None:
            radius_add_rate = 0
        return radius_add_rate

    def on_model_load_complete(self, com_unit):
        super(ComGrenadeCollision, self).on_model_load_complete(com_unit)
        if not self._col_obj or not self.is_enable():
            return
        cobj = self._col_obj
        self.need_update = True
        cobj.set_notify_contact(True)
        if global_data.feature_mgr.is_support_collision_bind_model():
            sync_type = collision.INTRP_SYNC if self._ignore_fire_pos else collision.DIRECTLY_SYNC
            cobj.bind_sync_visible_obj(self._model(), sync_type, 1, False)
        self.last_pos = cobj.position
        self.last_check_pos = self.last_pos
        self.last_update_time = time.time()
        self.play_fly_sound(cobj)
        firearm_config = confmgr.get('firearm_config', str(self.throw_info['item_itype']))
        if firearm_config:
            self.iKind = firearm_config.get('iKind')

    def play_fly_sound(self, cobj):
        item_conf = confmgr.get('grenade_res_config', str(self.throw_info['item_itype']))
        if item_conf and item_conf['cFlySound']:
            fly_sound = item_conf['cFlySound']
            if isinstance(fly_sound, str):
                global_data.sound_mgr.set_switch('bullet_fly', fly_sound, self._gernade_id)
                self._gernade_player_id = global_data.sound_mgr.post_event('Play_bullet_fly2', self._gernade_id, cobj.position)
            elif isinstance(fly_sound, list):
                if fly_sound[1] == 'nf':
                    self._gernade_player_id = global_data.sound_mgr.post_event(fly_sound[0], self._gernade_id, cobj.position)

    def _get_left_time(self, position, speed, fly_time):
        result = self.scene.scene_col.hit_by_ray(position + speed * 0.5, position + speed * fly_time, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
        if not result[0]:
            return fly_time
        hit_objs = result[1]
        first_hit_obj = hit_objs[0]
        for info in hit_objs:
            if info[2] < first_hit_obj[2]:
                first_hit_obj = info

        hit_pos = first_hit_obj[0]
        return (position - hit_pos).length / self.throw_info['speed']

    def _on_position_changed--- This code section failed: ---

 508       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  '_col_obj'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    27  'to 27'

 509      12  LOAD_FAST             1  'position'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  '_col_obj'
          21  STORE_ATTR            2  'position'
          24  JUMP_FORWARD          0  'to 27'
        27_0  COME_FROM                '24'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def _on_direction_changed--- This code section failed: ---

 512       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_FAST             1  'direction'
           6  LOAD_GLOBAL           1  'math3d'
           9  LOAD_ATTR             2  'matrix'
          12  CALL_FUNCTION_2       2 
          15  POP_JUMP_IF_TRUE     22  'to 22'

 514      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 515      22  LOAD_GLOBAL           3  'getattr'
          25  LOAD_GLOBAL           1  'math3d'
          28  CALL_FUNCTION_2       2 
          31  POP_JUMP_IF_FALSE    49  'to 49'

 516      34  LOAD_FAST             1  'direction'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             4  '_col_obj'
          43  STORE_ATTR            5  'rotation_matrix'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 28

    def qte_break_speed(self):
        if self.qte_info:
            return
        if self._col_obj:
            self.qte_info[self._col_obj] = self._col_obj.linear_velocity
        for col in self._col_objs:
            self.qte_info[col] = col.linear_velocity

        for col in self.qte_info:
            col.set_linear_velocity(col.linear_velocity * 0.0)

    def qte_resume_speed(self):
        if not self.qte_info:
            return
        for col in self.qte_info:
            col.set_linear_velocity(self.qte_info[col])

        self.qte_info = {}

    def play_collisions_sound(self, position):
        cur_time = time.time()
        if cur_time - self._save_collision_time > self.COLLIDE_SOUND_INTERVAL:
            self._save_collision_time = cur_time
            if isinstance(self._collide_sound, str):
                if self._collide_sound != '':
                    global_data.sound_mgr.set_switch('grenade', self._collide_sound, self._gernade_id)
                else:
                    global_data.sound_mgr.set_switch('grenade', 'grenade_ground', self._gernade_id)
                global_data.sound_mgr.post_event('Play_grenade', self._gernade_id, position)
            elif isinstance(self._collide_sound, list):
                if self._collide_sound[1] == 'nf':
                    global_data.sound_mgr.post_event(self._collide_sound[0], self._gernade_id, position)

    def is_trigger(self, cobj):
        if cobj is None:
            return True
        else:
            if cobj.group == GROUP_AUTO_AIM:
                return False
            if self._trigger_type == THROWABLE_TRIGGER_COLLISION:
                return True
            if self._trigger_type == THROWABLE_TRIGGER_ENTITY:
                units = global_data.emgr.scene_find_unit_event.emit(cobj.cid)
                if units and units[0]:
                    return True
            if cobj.group == WATER_GROUP and cobj.mask == WATER_MASK:
                position = self._col_obj.position
                if position.y < 0:
                    position.y = 0
                result = self.scene.scene_col.hit_by_ray(position + math3d.vector(0, 5, 0), position + math3d.vector(0, -3, 0), 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
                hit_objs = result[1]
                if result[0]:
                    first_hit_obj = None
                    for info in hit_objs:
                        hit_cobj = info[4]
                        if hit_cobj.cid == self._col_obj.cid or hit_cobj.group == WATER_GROUP and hit_cobj.mask == WATER_MASK:
                            continue
                        if first_hit_obj is None or info[2] < first_hit_obj[2]:
                            first_hit_obj = hit_cobj

                    if first_hit_obj:
                        return
                self._col_obj.disable_gravity(True)
                self._col_obj.group = 0
                self._col_obj.mask = 0
                self._col_obj.set_linear_velocity(math3d.vector(0, -NEOX_UNIT_SCALE * self._sink_speed, 0))
                self._gravity = None
            else:
                global_data.game_mgr.post_exec(self.restitution)
            return False

    def restitution(self):
        if self._col_obj:
            self._col_obj.set_linear_velocity(self._col_obj.linear_velocity * self._restitution)

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            if not self._is_collision_enable:
                return
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            is_ignore, cobj, point, normal = self.collision_check(cobj, point, normal, **kwargs)
            if is_ignore:
                return
            if self._hit_sfx_use_dir_normal:
                normal = self._last_check_pos - self._col_obj.position
                if normal.is_zero:
                    normal = UP_VECTOR
                else:
                    normal.normalize()
            if self.iKind == WP_SUMMON_GRENADES_GUN:
                point = point + normal * 0.4 * NEOX_UNIT_SCALE
            if cobj:
                if cobj.cid in self._col_ids:
                    return
            is_trigger = self.is_trigger(cobj)
            if not is_trigger and not is_break_obj(cobj.model_col_name):
                self._contact_other_col_times += 1
                if not (self._max_contact_other_col_times > 0 and self._contact_other_col_times >= self._max_contact_other_col_times):
                    if self._col_obj.linear_velocity.length > self.COLLIDE_SOUND_SPEED_LIMIT:
                        self.play_collisions_sound(point)
                    return
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                contact_info = {}
                target_id = None
                if cobj:
                    unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                    if unit:
                        target_id = unit.id
                        if unit.ev_g_is_campmate(self.faction_id):
                            start_pos = self._col_obj.position - self._col_obj.rotation_matrix.forward * 3 * NEOX_UNIT_SCALE
                            end_pos = self._col_obj.position + self._col_obj.rotation_matrix.forward * 2 * NEOX_UNIT_SCALE
                            result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
                            overlapped_col = False
                            if result[0]:
                                for col_info in result[1]:
                                    if col_info[4] == self._col_obj:
                                        continue
                                    hit_unit = global_data.emgr.scene_find_unit_event.emit(col_info[4].cid)[0]
                                    if not hit_unit or hit_unit == unit:
                                        continue
                                    if hit_unit.ev_g_is_shield() or not hit_unit.ev_g_is_campmate(self.faction_id):
                                        target_id = hit_unit.id
                                        overlapped_col = True
                                        break

                            if not overlapped_col:
                                return
                        if self._ignore_unit_tag:
                            is_through_unit = unit.MASK & self._ignore_unit_tag
                            can_through = is_through_unit and unit.ev_g_can_through(self.faction_id)
                            if can_through:
                                overlapped_col = False
                                start_pos = self._col_obj.position - self._col_obj.rotation_matrix.forward * 3 * NEOX_UNIT_SCALE
                                end_pos = self._col_obj.position + self._col_obj.rotation_matrix.forward * 2 * NEOX_UNIT_SCALE
                                result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
                                if result[0]:
                                    for col_info in result[1]:
                                        if col_info[4] == self._col_obj:
                                            continue
                                        hit_unit = global_data.emgr.scene_find_unit_event.emit(col_info[4].cid)[0]
                                        if not hit_unit or hit_unit == unit:
                                            continue
                                        if hit_unit.ev_g_is_shield() or not hit_unit.ev_g_is_campmate(self.faction_id):
                                            target_id = hit_unit.id
                                            point = col_info[0]
                                            overlapped_col = True
                                            break

                                return overlapped_col or None
                    if is_trigger:
                        if team_utils.ignore_expolosion(self._owner_id, target_id):
                            return
                    elif unit.ev_g_is_campmate(self.faction_id):
                        return
                    target_type = global_data.emgr.scene_find_unit_type_event.emit(cobj.cid)[0]
                    if self._check_pierce(unit, cobj.cid, point):
                        return
                    contact_info['target_type'] = target_type
            if self._intrp_time < self._intrp_duration:
                initial_position = math3d.vector(*self.throw_info['position'])
                self.set_model_end_pos(point)
                if (point - initial_position).length < self._col_obj.linear_velocity.length * 0.015:
                    self.hide_model()
            if self._col_obj:
                self.need_update = False
                self._col_obj.set_notify_contact(False)
                self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
            self.stop_post_contact_timer()
            explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            return

    def _check_pierce(self, unit, cid, point):
        col_is_pierced = unit.ev_g_is_pierced()
        if unit.id in self.pierced_targets:
            return True
        else:
            if self.dynamic_pierce_check(unit):
                self.send_harm_info(unit, cid, point)
                self.complete_model_pos_interpolation()
                return True
            if self.left_pierce_cnt > 0 and (col_is_pierced is None or col_is_pierced is True):
                do_pierce = self.send_harm_info(unit, cid, point)
                self.complete_model_pos_interpolation()
                if do_pierce:
                    self.left_pierce_cnt -= 1
                return True
            return False

    def post_on_contact(self):
        if global_data.feature_mgr.is_support_collision_bind_model() and self._col_obj:
            self._col_obj.unbind_sync_visible_obj()
        if not self._col_objs:
            return

        def get_target_type(elem):
            return elem.get('target_type', -1)

        self._col_objs.sort(key=get_target_type, reverse=True)
        self.update_explosive_info(*self._col_objs[0]['explosive_info'])
        self._col_objs = []

    def stop_post_contact_timer(self):
        if self.post_contact_timer:
            self.tm.unregister(self.post_contact_timer)
            self.post_contact_timer = None
        return

    def tick_sub_grenade(self, dt, col_obj):
        self._fly_time += dt
        if self._fly_time >= self._spread_time:
            center_pos = col_obj.position - (self._right * cos(self._rad) + self._up * sin(self._rad)) * self._raidus
            self._raidus += dt * self._radius_speed
            if self._raidus > self._spread_radius:
                self._raidus = self._spread_radius
            self._angular_speed = self._product_radius_angle / self._raidus
            self._rad += dt * self._angular_speed
            pos = center_pos + (self._right * cos(self._rad) + self._up * sin(self._rad)) * self._raidus
            col_obj.position = pos

    def tick_child_grenade(self, dt, col_obj):
        self._fly_time += dt
        if self._fly_time >= self._spread_time:
            spread_dis = self._spread_speed * (self._fly_time - self._spread_time)
            if spread_dis > self._max_gap:
                return
            col_obj.position = col_obj.position + self._right * self._side * self._spread_speed * dt

    def tick_sub_arrow(self, dt, col_obj):
        pass

    def check_max_height(self, m, col_obj):
        if self._max_height and self.pure_last_pos.y > col_obj.position.y:
            self.on_contact(None, m.position, UP_VECTOR)
        return

    def update_left_time(self, dt):
        self._left_time -= dt

    def tick(self, dt):
        col_obj = self._col_obj
        if not col_obj:
            self.need_update = False
            return
        else:
            if not col_obj.valid:
                return
            if self._gravity:
                if self._distance_for_gravity == 0 or self._distance_for_gravity <= (col_obj.position - self._original_pos).length:
                    col_obj.apply_force(self._gravity)
            if self._model:
                m = self._model() if 1 else None
                if not m or not m.valid:
                    self.need_update = False
                    return
                self.update_left_time(dt)
                if self._left_time <= 0:
                    self.on_contact(None, col_obj.position, UP_VECTOR)
                if self._max_distance and self._max_distance <= (col_obj.position - self._original_pos).length:
                    self.on_contact(None, col_obj.position, UP_VECTOR)
                self.check_max_height(m, col_obj)
                if self._is_sub_weapon and self.item_kind in self.tick_sub_weapon_func:
                    self.tick_sub_weapon_func[self.item_kind](dt, col_obj)
                cpos = col_obj.position
                if self._need_ray_check:
                    self.ray_check(cpos)
                else:
                    self._last_check_pos = cpos
                if global_data.feature_mgr.is_support_collision_bind_model() or self._ignore_fire_pos:
                    self.intrp_model_pos(dt, auto_intrp_rot=self._auto_intrp_rot)
                else:
                    self.directly_set_model_pos()
            if self.change_forward_dist_threshold:
                forward = cpos - self.pure_last_pos
                forward.y = 0
                if forward.length < self.change_forward_dist_threshold:
                    return
                forward.normalize()
                mat = math3d.matrix.make_orient(forward, UP_VECTOR)
                m = self._model_cache
                if m and m.valid:
                    m.rotation_matrix = mat
            self.pure_last_pos = cpos
            if self._gernade_player_id:
                global_data.sound_mgr.set_position(self._gernade_id, cpos)
            return

    def _stop_sound(self):
        if self._gernade_player_id:
            global_data.sound_mgr.stop_playing_id(self._gernade_player_id)
            self._gernade_player_id = None
        if self._gernade_id:
            global_data.sound_mgr.unregister_game_obj(self._gernade_id)
            self._gernade_id = None
        return

    def attach_mecha(self, *args):
        self._on_grenade_attached()

    def destroy_col(self):
        if self.sd.ref_col_obj:
            self.sd.ref_col_obj = None
        super(ComGrenadeCollision, self).destroy_col()
        return

    def destroy(self):
        if not self._is_valid:
            return
        self._stop_sound()
        self.stop_post_contact_timer()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_position_changed)
        super(ComGrenadeCollision, self).destroy()

    def get_position(self):
        if self._col_obj and self._col_obj.valid:
            return self._col_obj.position

    def get_col_obj(self):
        return self._col_obj

    def get_limited_pierce_cnt(self):
        if self.throw_info.get('limited_pierce_cnt', 0) != 0:
            return self.throw_info.get('limited_pierce_cnt', 0) != 0
        else:
            item_type = self.throw_info['item_itype']
            trigger_id = self.throw_info.get('trigger_id', None)
            trigger = self.battle.get_entity(trigger_id)
            limited_pierce_cnt = 0
            if trigger and trigger.logic:
                limited_pierce_cnt = trigger.logic.ev_g_add_attr(WEAPON_PIERCE_CNT, item_type)
            return limited_pierce_cnt

    def dynamic_pierce_check(self, unit_obj):
        if self.item_type == 8000012 and (unit_obj.ev_g_has_buff_by_id(50300079) or unit_obj.ev_g_has_buff_by_id(bconst.BUFF_ID_ELEMENT_WIND)):
            return True
        return False