# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRecoilNew.py
from __future__ import absolute_import
from six.moves import range
import cython_flag
import time
import world
import math3d
import random
import common.utils.timer as timer
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.gcommon.common_const.animation_const as animation_const
from logic.units.LAvatar import LAvatar
from mobile.common.IdManager import IdManager
from common.cfg import confmgr
from ..UnitCom import UnitCom
from ...cdata import status_config as st_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_utils import parachute_utils
from logic.gutils.weapon_utils import is_in_fast_aim_and_fire_mode, is_auto_fast_aim_and_fire_mode
from math import tan, sin, cos, sqrt, atan, isnan
from logic.gcommon.common_const import attr_const
_SEQUENCE_RECOVER_MIN_INTERVAL = 0.3
_SEQUENCE_RECOVER_SPEED = 1.0 / 0.16666665
_MAX_RECOVER_TIME = 0.2
_AGENT_TRACK_SET = frozenset([weapon_const.WP_GRENADES_GUN, weapon_const.WP_SUMMON_GRENADES_GUN])
_PI = 3.141592653589793
_RADIANS_FACTOR = _PI / 180.0001
_CTRL_TYPE_OHTER = 0
_CTRL_TYPE_AVATAR = 1
_CTRL_TYPE_SPECTATOR = 2

class ComRecoilNew(UnitCom):
    BIND_EVENT = {'E_DELTA_YAW': '_on_yaw',
       'E_DELTA_PITCH': '_on_pitch',
       'E_FIRE': '_on_fire',
       'G_FIRE_RAY': '_on_fire_ray',
       'G_FIRE_RAY_BY_CUSTOM_DIRECTION': '_on_fire_ray_by_custom_direction',
       'G_SPREAD_VALUES': 'get_spread_values',
       'E_WEAPON_DATA_CHANGED_SUCCESS': '_weapon_data_changed',
       'E_DEATH': '_die',
       'E_SIMULATE_FIRE': '_simulate_fire',
       'E_AIM_TARGET': '_set_target',
       'E_PUPPET_ATTACK_START': '_puppet_attack_start',
       'E_PUPPET_ATTACK_END': '_puppet_attack_end',
       'G_SEQUENCE_NUM': 'get_sequence_num',
       'E_END_PUT_ON_BULLET': '_on_reloaded',
       'E_LEAVE_STATE': 'on_leave_state',
       'E_WEAPON_DATA_UPDATE_TO_ATTACKING': '_on_update_to_attack_weapon',
       'E_CTRL_ACCUMULATE_END': '_pullet_accumulate_end',
       'E_PARACHUTE_STATUS_CHANGED': ('_on_parachute_status_changed', -1),
       'G_IS_AUTO_FIRE': '_get_is_auto_fire',
       'G_IS_WEAPON_IN_AUTO_MODE': '_is_weapon_in_auto_mode',
       'E_GUN_ATTACK_ADSORB': 'gun_attack_adsorb'
       }

    def __init__(self):
        super(ComRecoilNew, self).__init__(True)
        self._weapon = None
        self._fire_cd = 99999
        self._fire_maxup = 0
        self._fire_maxyaw = 0
        self._camera_delta_yaw = 0
        self._camera_delta_pitch = 0
        self._recoil_yaw_v = 0
        self._recoil_pitch_v = 0
        self._recoil_yaw_total = 0
        self._recoil_pitch_total = 0
        self._camera_pitch = None
        self._recoil_time = 0
        self._recoil_recover_v = 0
        self._spread = 0
        self._fire_time = 0
        self._sequence_time = 0
        self._is_auto_fire = False
        self._is_first_dire = True
        self._is_fire_end = True
        self._aim_target = None
        self._aim_target_time = 0
        self._needed_camera_event = True
        self._ctrl_type = _CTRL_TYPE_OHTER
        self._cur_sequence_num = 0.0
        self._weapon_accumulate_time = 0
        self._is_can_accumulate_fire = False
        self._last_cam_trans = None
        self._auto_fire_right_mode = False
        return

    def init_from_dict--- This code section failed: ---

 125       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'ComRecoilNew'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'init_from_dict'
          15  LOAD_FAST             1  'unit_obj'
          18  LOAD_FAST             2  'bdict'
          21  CALL_FUNCTION_2       2 
          24  POP_TOP          

 126      25  LOAD_GLOBAL           3  'hasattr'
          28  LOAD_GLOBAL           1  'ComRecoilNew'
          31  CALL_FUNCTION_2       2 
          34  POP_JUMP_IF_FALSE    78  'to 78'

 127      37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             4  'regist_event'
          43  LOAD_CONST            2  'E_START_AUTO_FIRE'
          46  LOAD_FAST             0  'self'
          49  LOAD_ATTR             5  '_start_auto_fire'
          52  CALL_FUNCTION_2       2 
          55  POP_TOP          

 128      56  LOAD_FAST             0  'self'
          59  LOAD_ATTR             4  'regist_event'
          62  LOAD_CONST            3  'E_STOP_AUTO_FIRE'
          65  LOAD_FAST             0  'self'
          68  LOAD_ATTR             6  '_stop_auto_fire'
          71  CALL_FUNCTION_2       2 
          74  POP_TOP          
          75  JUMP_FORWARD          0  'to 78'
        78_0  COME_FROM                '75'

 130      78  LOAD_FAST             0  'self'
          81  LOAD_ATTR             7  'on_init_complete'
          84  CALL_FUNCTION_0       0 
          87  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 31

    def destroy--- This code section failed: ---

 133       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'unregist_event'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    53  'to 53'

 134      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'unregist_event'
          18  LOAD_CONST            2  'E_START_AUTO_FIRE'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  '_start_auto_fire'
          27  CALL_FUNCTION_2       2 
          30  POP_TOP          

 135      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             1  'unregist_event'
          37  LOAD_CONST            3  'E_STOP_AUTO_FIRE'
          40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             3  '_stop_auto_fire'
          46  CALL_FUNCTION_2       2 
          49  POP_TOP          
          50  JUMP_FORWARD          0  'to 53'
        53_0  COME_FROM                '50'

 137      53  LOAD_GLOBAL           4  'super'
          56  LOAD_GLOBAL           5  'ComRecoilNew'
          59  LOAD_FAST             0  'self'
          62  CALL_FUNCTION_2       2 
          65  LOAD_ATTR             6  'destroy'
          68  CALL_FUNCTION_0       0 
          71  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_init_complete(self):
        self.set_weapon(self.sd.ref_wp_bar_cur_weapon)
        player = global_data.player
        if not player:
            return
        player_id = player.id
        if self.unit_obj.id == player_id or self.sd.ref_driver_id == player_id:
            self._ctrl_type = _CTRL_TYPE_AVATAR
        elif player.logic:
            spectate_target = player.logic.ev_g_spectate_target()
            if spectate_target and spectate_target.id == self.unit_obj.id:
                self._ctrl_type = _CTRL_TYPE_SPECTATOR

    def _switched_data(self, obj_weapon):
        self.set_weapon(obj_weapon)

    def _on_update_to_attack_weapon(self, obj_weapon):
        self.set_weapon(obj_weapon)

    def _weapon_data_changed(self, pos):
        if self._weapon is None:
            return
        else:
            if pos is None or pos == self._weapon.iPos:
                self.set_weapon(self.sd.ref_wp_bar_cur_weapon)
            return

    def _die(self, *args):
        self.set_weapon(None)
        return

    def set_weapon(self, obj_weapon):
        self._weapon = obj_weapon
        if obj_weapon:
            conf = self._weapon.conf
            self._fire_cd = self._weapon.get_fire_cd()
            self._fire_maxup = conf('fMaxUp') * _RADIANS_FACTOR
            self._fire_maxyaw = conf('fMaxYaw') * _RADIANS_FACTOR

    def _set_target(self, target):
        self._aim_target = target
        self._aim_target_time = time.time()

    def get_spread_values(self):
        if self._weapon:
            spread_base = self.get_spread_base()
            spread_value = self.get_spread_value()
            recover_time = 0.1
            spread_dec = self._weapon.get_effective_value('fSpreadDec')
            if spread_dec > 0:
                recover_time = spread_value / spread_dec
            spread_base *= 1 + self.ev_g_add_attr(attr_const.ATTR_HUMAN_COMMON_WEAPON_SPREAD_FACTOR)
            spread_value *= 1 + self.ev_g_add_attr(attr_const.ATTR_HUMAN_COMMON_WEAPON_SPREAD_FACTOR)
            return (
             spread_base, spread_base + spread_value, recover_time)
        else:
            return (0, 0, 0)

    def get_spread_base(self):
        right_aim_mod = 1
        if not self._weapon:
            return 0
        conf = self._weapon.conf
        sd = self.sd
        get_value = self.get_value
        if not get_value('G_IS_AIM_TRANSFERRING'):
            if sd.ref_in_aim:
                if get_value('G_IS_MOVE'):
                    return conf('fADSMove')
                return conf('fADSStop')
            if get_value('G_IN_RIGHT_AIM'):
                right_aim_mod = conf('fRAim')
        is_in_jump = get_value('G_ACTION_IS_JUMP')
        if is_in_jump:
            return conf('fHIPJump') * right_aim_mod
        if get_value('G_APPEARANCE_IN_STAND') or get_value('G_APPEARANCE_IN_SKATE'):
            if get_value('G_IS_MOVE'):
                return conf('fHIPStandMove') * right_aim_mod
            return conf('fHIPStandStop') * right_aim_mod
        if get_value('G_APPEARANCE_IN_SQUAT'):
            if get_value('G_IS_MOVE'):
                return conf('fHIPCrouchMove') * right_aim_mod
            return conf('fHIPCrouchStop') * right_aim_mod
        return conf('fHIPStandStop', 0) * right_aim_mod

    def get_spread_value(self):
        if not self._weapon:
            return 0
        if self._is_auto_fire:
            return self._spread
        delta = time.time() - self._fire_time - self._fire_cd
        if delta > 0:
            self._spread -= self._weapon.get_effective_value('fSpreadDec') * delta
            max_spread = self._weapon.get_effective_value('fMaxSpread')
            if (self.sd.ref_in_aim or self.sd.ref_in_right_aim) and not self.get_value('G_IS_AIM_TRANSFERRING'):
                max_spread = self._weapon.get_effective_value('fAimMaxSpread', default=max_spread)
                min_spread = self._weapon.get_effective_value('fAimMinSpread', default=0)
            else:
                min_spread = self._weapon.get_effective_value('fMinSpread', default=0)
            if max_spread < self._spread:
                self._spread = max_spread
            if self._spread < min_spread:
                self._spread = min_spread
        return self._spread

    def get_sequence_num(self, *args):
        if not self._weapon:
            return 0
        delta = time.time() - self._sequence_time - _SEQUENCE_RECOVER_MIN_INTERVAL
        if delta > 0:
            self._cur_sequence_num -= _SEQUENCE_RECOVER_SPEED * delta
            if self._cur_sequence_num < 0:
                self._cur_sequence_num = 0
            self._sequence_time = time.time() - _SEQUENCE_RECOVER_MIN_INTERVAL
        return int(self._cur_sequence_num)

    def get_target_direction(self, pos, camera_direction):
        if self._aim_target is None or self._weapon is None:
            return
        else:
            conf = self._weapon.conf
            if self._weapon.get_kind() != weapon_const.WP_NAVIGATE_GUN and conf('fAutoAimDistance') and self._aim_target.ev_g_model_hit_ray(pos, camera_direction * conf('fAutoAimDistance') * NEOX_UNIT_SCALE):
                return
            model = self._aim_target.ev_g_model()
            if not model:
                return
            matrix = model.get_bone_matrix(animation_const.BONE_SPINE2_NAME, world.SPACE_TYPE_WORLD)
            if not matrix:
                return
            aim_pos = matrix.translation
            direction = aim_pos - pos
            if direction.is_zero:
                return
            return direction

    def _get_cam_trans(self):
        scn = world.get_active_scene()
        partcamera = scn.get_com('PartCamera')
        camera = partcamera.cam
        from logic.client.const import camera_const
        cameradata = partcamera.cam_manager.last_camera_state_setting
        matrix = None
        if cameradata:
            cameradata['type']
            if partcamera.get_cur_camera_state_type() == camera_const.FREE_MODEL:
                matrix = cameradata['trans']
                self._last_cam_trans = matrix
            elif partcamera.is_out_cam_state_slerp(camera_const.FREE_MODEL):
                matrix = self._last_cam_trans
        if matrix is None:
            matrix = camera.world_rotation_matrix
        return matrix

    def _get_agent_camera_direction(self, start_pos, end_pos):
        if not self._weapon:
            return
        else:
            if self._weapon.get_kind() not in _AGENT_TRACK_SET:
                return
            str_type = str(self._weapon.iType)
            conf = confmgr.get('grenade_config', str_type)
            v = conf['fSpeed']
            v_2 = v * v
            g = confmgr.get('grenade_config', str_type, 'fGravity', default=98)
            up_angle = confmgr.get('grenade_config', str_type, 'fUpAngle', default=0)
            camera_direction = end_pos - start_pos
            h = camera_direction.y
            cdx = camera_direction.x
            cdz = camera_direction.z
            x_2 = cdx * cdx + cdz * cdz
            x = sqrt(x_2)
            a = -0.5 * g * x_2 / v_2
            b = x
            c = a - h
            value = b * b - 4 * a * c
            if value < 0 or a == 0:
                return
            value = sqrt(value)
            value_1 = (-b + value) * 0.5 / a
            value_2 = (-b - value) * 0.5 / a
            angle_y = min(value_1, value_2)
            angle_y = atan(angle_y)
            angle_y -= up_angle * _RADIANS_FACTOR
            camera_direction.normalize()
            camera_direction.y = 0
            yaw = camera_direction.yaw
            ai_level = self.battle.get_ai_level()
            if ai_level:
                cfg = confmgr.get('ai_data', 'WeaponToAtkCfg', 'Content', str_type, 'OffsetAngle', default=None)
                if cfg:
                    offset_angle = 0
                    for _, info in enumerate(cfg):
                        if info[0] >= ai_level:
                            offset_angle = info[1]

                    if offset_angle != 0:
                        offset_x = random.uniform(-offset_angle, offset_angle)
                        offset_x *= _RADIANS_FACTOR
                        offset_y = random.uniform(-offset_angle, offset_angle)
                        offset_y *= _RADIANS_FACTOR
                        yaw += offset_x
                        angle_y += offset_y
            camera_direction.x = sin(yaw)
            camera_direction.z = cos(yaw)
            camera_direction.y = sin(angle_y)
            return camera_direction

    def _on_get_camera_param(self):
        if self.sd.ref_is_agent:
            model = self.ev_g_model()
            if not model:
                return (None, None, None)
            m_height = model.bounding_box.y * 0.75
            m_pos = model.position
            if not m_pos:
                return (None, None, None)
            camera_pos = math3d.vector(m_pos.x, m_pos.y + m_height, m_pos.z)
            attack_pos = self.ev_g_attack_pos()
            if not attack_pos:
                return (None, None, None)
            camera_direction = self._get_agent_camera_direction(camera_pos, attack_pos)
            if camera_direction is None:
                camera_direction = attack_pos - camera_pos
                if camera_direction.is_zero:
                    return (None, None, None)
                camera_direction.normalize()
            right = camera_direction.cross(math3d.vector(0, 1, 0))
            up = right.cross(camera_direction)
            return (
             camera_pos, camera_direction, up)
        else:
            scn = world.get_active_scene()
            partcamera = scn.get_com('PartCamera')
            if partcamera:
                camera = partcamera.cam if 1 else None
                return camera or (None, None, None)
            matrix = self._get_cam_trans()
            camera_pos = camera.world_position
            camera_direction = matrix.forward
            return (
             camera_pos, camera_direction, matrix.up)
            return

    def _on_fire_ray(self, one_shoot_bullet_num):
        if not self._weapon:
            return
        else:
            camera_pos, camera_direction, camera_up = self._on_get_camera_param()
            if not camera_pos or not camera_direction:
                return
            if self._weapon.get_kind() == weapon_const.WP_NAVIGATE_GUN:
                direction = camera_direction
                camera_direction = None
            else:
                direction = self.get_target_direction(camera_pos, camera_direction)
                if direction is None:
                    direction = camera_direction
                    camera_direction = None
                if direction and isnan(direction.x):
                    return
                original_direction = direction
                spread_value = self.get_spread_base() + self.get_spread_value()
                spread_value *= 1 + self.ev_g_add_attr(attr_const.ATTR_HUMAN_COMMON_WEAPON_SPREAD_FACTOR)
                tan_spread_value = tan(spread_value * _RADIANS_FACTOR)
                if one_shoot_bullet_num == 1:
                    spread_range = random.uniform(0, tan_spread_value)
                    rotation_matrix = math3d.matrix.make_rotation(direction, random.uniform(-_PI, _PI))
                    direction += camera_up * rotation_matrix * spread_range
                    direction.normalize()
                    if self.sd.ref_in_aim:
                        start_pos = camera_pos + direction * 2.5
                        new_target_pos = self.ev_g_sighting_target_pos(start_pos, direction)
                        if new_target_pos:
                            direction = new_target_pos - start_pos
                            direction.normalize()
                        return (camera_pos + direction * 2.5, direction, camera_direction, original_direction)
                else:
                    all_dirs = []
                    for index in range(one_shoot_bullet_num):
                        spread_range = random.uniform(0, tan_spread_value)
                        rotation_matrix = math3d.matrix.make_rotation(direction, random.uniform(-_PI, _PI))
                        temp_dir = direction + camera_up * rotation_matrix * spread_range
                        temp_dir.normalize()
                        all_dirs.append(temp_dir)

                    direction = all_dirs
                player_pos = self.ev_g_position()
                if not player_pos:
                    return
            return (
             camera_pos, direction, camera_direction, original_direction)

    def _on_fire_ray_by_custom_direction(self, custom_direction):
        if not self._weapon:
            return
        else:
            scn = world.get_active_scene()
            part_cam = scn.get_com('PartCamera')
            if not part_cam:
                return
            camera = part_cam.cam
            if not camera:
                return
            matrix = self._get_cam_trans()
            camera_pos = camera.world_position
            camera_direction = matrix.forward
            if self._weapon.get_kind() == weapon_const.WP_NAVIGATE_GUN:
                direction = camera_direction
                camera_direction = None
            else:
                direction = self.get_target_direction(camera_pos, camera_direction)
                if direction is None:
                    direction = camera_direction
                    camera_direction = None
            original_direction = direction
            all_dirs = []
            for data in custom_direction:
                offset = data[0]
                radian = data[1]
                rotation_matrix = math3d.matrix.make_rotation(direction, radian)
                temp_dir = direction + matrix.up * rotation_matrix * tan(offset * _RADIANS_FACTOR)
                temp_dir.normalize()
                all_dirs.append(temp_dir)

            direction = all_dirs
            return (
             camera_pos, direction, camera_direction, original_direction)

    def _on_yaw(self, dx, *args):
        if self._needed_camera_event and self.need_update:
            self._camera_delta_yaw = dx

    def _on_pitch(self, dy):
        if self._needed_camera_event and self.need_update and self._camera_pitch is not None:
            self._camera_delta_pitch = -dy
            if dy < 0:
                scn = world.get_active_scene()
                com_camera = scn.get_com('PartCamera')
                if com_camera:
                    self._camera_pitch = max(com_camera.get_pitch(), self._camera_pitch)
        return

    def gun_attack_adsorb(self, *args):
        if not self.sd.ref_in_aim:
            return
        if self._recoil_yaw_v == 0:
            return
        diff_target_yaw = self.ev_g_adsorb_diff_target_yaw() or 0
        if diff_target_yaw != 0 and diff_target_yaw * self._recoil_yaw_v < 0:
            self._recoil_yaw_v = 0
            self._recoil_time = 0
            self._recoil_yaw_total = 0

    def _fire_recoil(self):
        if not self._weapon:
            return
        conf = self._weapon.conf
        self._fire_time = time.time()
        self._is_fire_end = False
        self._recoil_recover_v = 0
        if self._recoil_pitch_total >= self._fire_maxup:
            self._recoil_pitch_v = 0
        else:
            self._recoil_pitch_v = conf('fRecoilUp')
        self._recoil_time = conf('fRecoilTime')
        self._recoil_yaw_v = random.uniform(-conf('fRecoilLeft'), conf('fRecoilRight'))
        init_recoil_yaw_v = self._recoil_yaw_v
        if self.is_unit_obj_type('LMecha'):
            self.send_event('E_PLAY_CAMERA_STATE_TRK', 'C_FIRE')
        elif self._weapon:
            if not self._weapon.is_accumulate_gun() and self.ev_g_need_play_each_fire_camera_trk(self._weapon.iType):
                self.send_event('E_PLAY_WEAPON_FIRE_CAMERA_TRK', self._weapon.iType)
        if abs(self._recoil_yaw_total) >= abs(self._fire_maxyaw):
            if self._recoil_yaw_v * self._recoil_yaw_total > 0:
                self._recoil_yaw_v = -self._recoil_yaw_v
        if self.sd.ref_in_aim:
            aim_mod = conf('fAimMod', default=1)
            self._recoil_pitch_v *= aim_mod
            self._recoil_yaw_v *= aim_mod
            diff_target_yaw = self.ev_g_adsorb_diff_target_yaw() or 0
            if diff_target_yaw != 0 and diff_target_yaw * self._recoil_yaw_v < 0:
                self._recoil_yaw_v = -self._recoil_yaw_v
        if not self.need_update:
            self.need_update = True
        if self._is_first_dire:
            self._is_first_dire = False
            mul = conf('fFirstShotMul')
            self._recoil_pitch_v *= mul
            self._recoil_yaw_v *= mul
            scn = world.get_active_scene()
            com_camera = scn.get_com('PartCamera')
            if com_camera:
                self._camera_pitch = com_camera.get_pitch()

    def _fire_sequence(self):
        if not self._weapon:
            return
        max_sequence = self._weapon.get_data_by_key('iMaxSequence')
        if max_sequence == 0:
            return
        self._sequence_time = time.time()
        self._cur_sequence_num += 1
        if self._cur_sequence_num > max_sequence:
            self._cur_sequence_num = max_sequence

    def _get_is_auto_fire(self):
        return self._is_auto_fire

    def _is_weapon_in_auto_mode(self):
        if self._weapon is None:
            return False
        else:
            return self._weapon.get_effective_value('iMode') == weapon_const.AUTO_MODE

    def _start_auto_fire(self, *args, **kwargs):
        if self._weapon is None:
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18001))
            return
        else:
            if self._weapon.get_effective_value('iMode') in [weapon_const.AUTO_MODE]:
                self.get_spread_value()
                self._is_auto_fire = True
                self.need_update = True
            else:
                self._is_auto_fire = False
            if self._weapon.is_accumulate_gun():
                bullet_num = self._weapon.get_bullet_num()
                if bullet_num <= 0:
                    self.send_event('E_TRY_RELOAD')
                    return
                if not self.ev_g_get_state(st_const.ST_WEAPON_ACCUMULATE) and self.ev_g_status_try_trans(st_const.ST_WEAPON_ACCUMULATE):
                    self._weapon_accumulate_time = time.time()
                    self._is_can_accumulate_fire = True
                    self.send_event('E_CTRL_ACCUMULATE', True)
                    self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_CTRL_ACCUMULATE, (True,), None, True, IdManager.genid(), 'E_CTRL_ACCUMULATE_END'), True, False, True)
            right_mode = kwargs.get('right_mode', False)
            control_mode = self._weapon.get_shot_type(custom_dict=kwargs)
            in_fast_aim_and_fire = is_in_fast_aim_and_fire_mode(self._weapon)
            self._auto_fire_right_mode = right_mode
            if control_mode == weapon_const.CONTROL_MODEL_BEGIN:
                self.send_event('E_TRY_FIRE')
                bullet_num = self._weapon.get_bullet_num()
                if bullet_num > 0:
                    self.send_event('E_START_SIM_FIRE')
                if in_fast_aim_and_fire and right_mode:
                    self.send_event('E_TRY_AIM')
            elif control_mode == weapon_const.CONTROL_MODEL_END:
                self.send_event('E_ACTION_IS_SHOOT', 1)
                if in_fast_aim_and_fire:
                    self.send_event('E_TRY_AIM')
            return

    def on_leave_state(self, leave_state, new_st=None):
        if st_const.ST_WEAPON_ACCUMULATE == leave_state:
            self._is_can_accumulate_fire = False
        elif leave_state == st_const.ST_RELOAD:
            if self._weapon and self._auto_fire_right_mode and is_in_fast_aim_and_fire_mode(self._weapon):
                self.send_event('E_TRY_AIM')

    def _stop_auto_fire(self, *args, **kwargs):
        if not self._weapon:
            return
        force = kwargs.get('force', False)
        fire = kwargs.get('fire', True)
        right_mode = kwargs.get('right_mode', False)
        self._auto_fire_right_mode = False
        control_mode = self._weapon.get_shot_type(kwargs)
        if not force and control_mode == weapon_const.CONTROL_MODEL_END:
            if self._weapon.is_accumulate_gun():
                if self._is_can_accumulate_fire:
                    if fire:
                        self.send_event('E_TRY_FIRE', time.time() - self._weapon_accumulate_time)
                    self._is_can_accumulate_fire = False
                    self.ev_g_cancel_state(st_const.ST_WEAPON_ACCUMULATE)
                    self.send_event('E_CTRL_ACCUMULATE', False)
                    self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_CTRL_ACCUMULATE, (False,)), True, False, True)
            elif fire:
                self.send_event('E_TRY_FIRE')
            bullet_num = self._weapon.get_bullet_num()
            if bullet_num > 0:
                self.send_event('E_START_SIM_FIRE')
        if not self._is_fire_end:
            self._is_fire_end = True
            if control_mode == weapon_const.CONTROL_MODEL_END:
                delay_time = self._fire_cd
                global_data.game_mgr.register_logic_timer(self.real_end_attack, delay_time, times=1, mode=timer.CLOCK)
            else:
                self.real_end_attack()
            spread_base, spread_value, recover_time = self.get_spread_values()
            self.send_event('E_AIM_SPREAD', spread_base, spread_value, self._fire_cd, recover_time)
            bullet_num = self._weapon.get_bullet_num()
            if 0 < bullet_num < self._weapon.get_effective_value('iMagSize') * 0.3:
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(18010))
        self._is_auto_fire = False
        self.send_event('E_STOP_SIM_FIRE')
        if right_mode and (self.sd.ref_in_aim or self.sd.ref_in_right_aim) and is_auto_fast_aim_and_fire_mode(self._weapon):
            self.send_event('E_QUIT_AIM')

    def real_end_attack(self):
        self.ev_g_cancel_state(st_const.ST_SHOOT)
        self.send_event('E_ATTACK_END')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_END, ()], True)

    def _on_fire(self, *args):
        if not self._weapon:
            return
        self._do_on_fire()

    def _do_on_fire(self):
        conf = self._weapon.conf
        self._fire_recoil()
        self._fire_sequence()
        if self.unit_obj and self.unit_obj.id == global_data.player.id:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SIMULATE_FIRE,
             (
              self._recoil_pitch_v, self._recoil_yaw_v, self._camera_pitch)], True)
        max_spread = conf('fMaxSpread')
        if (self.sd.ref_in_aim or self.sd.ref_in_right_aim) and not self.get_value('G_IS_AIM_TRANSFERRING'):
            self._spread += conf('fAimSpreadInc', default=0)
            max_spread = self._weapon.get_effective_value('fAimMaxSpread', default=max_spread)
            min_spread = self._weapon.get_effective_value('fAimMinSpread', default=0)
        else:
            self._spread += self.get_spreadinc(conf)
            min_spread = self._weapon.get_effective_value('fMinSpread', default=0)
        if max_spread and max_spread < self._spread:
            self._spread = max_spread
        if self._spread < min_spread:
            self._spread = min_spread
        spread_base, spread_value, recover_time = self.get_spread_values()
        delay_time = 3600
        if not self._is_auto_fire:
            delay_time = conf('fCDTime')
        self.send_event('E_AIM_SPREAD', spread_base, spread_value, conf('fCDTime'), recover_time)

    def _simulate_fire(self, pitch_v, yaw_v, camera_pitch):
        if not global_data.player:
            return
        if global_data.cam_lplayer is global_data.player.logic:
            return
        if not self._weapon:
            return
        self.get_spread_value()
        conf = self._weapon.conf
        self._fire_time = time.time()
        self._recoil_pitch_v = pitch_v
        self._recoil_yaw_v = yaw_v
        self._camera_pitch = camera_pitch
        max_spread = conf('fMaxSpread')
        if (self.sd.ref_in_aim or self.sd.ref_in_right_aim) and not self.get_value('G_IS_AIM_TRANSFERRING'):
            self._spread += conf('fAimSpreadInc', default=0)
            max_spread = self._weapon.get_effective_value('fAimMaxSpread', default=max_spread)
            min_spread = self._weapon.get_effective_value('fAimMinSpread', default=0)
        else:
            self._spread += self.get_spreadinc(conf)
            min_spread = self._weapon.get_effective_value('fMinSpread', default=0)
        if max_spread and max_spread < self._spread:
            self._spread = max_spread
        if self._spread < min_spread:
            self._spread = min_spread
        spread_base, spread_value, recover_time = self.get_spread_values()
        delay_time = 3600
        if not self._is_auto_fire:
            delay_time = conf('fCDTime')
        self.send_event('E_AIM_SPREAD', spread_base, spread_value, conf('fCDTime'), recover_time)
        if not self.need_update:
            self.need_update = True

    def _cal_recoil_v(self, delta):
        if delta >= self._recoil_time:
            self._recoil_time = 0
            delta = self._recoil_time
            wp_recover_v = self._weapon.get_effective_value('fRecoverV')
            if self._recoil_recover_v < wp_recover_v:
                self._recoil_recover_v = wp_recover_v
        else:
            self._recoil_time -= delta
            self._recoil_recover_v = 0
        return delta

    def is_spectate_target(self):
        spectate_target = None
        if global_data.player and global_data.player.logic and self.unit_obj:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
            return spectate_target and spectate_target.id == self.unit_obj.id
        else:
            return False

    def _rotate_camera(self, yaw, pitch):
        scn = world.get_active_scene()
        if not scn:
            return
        com_camera = scn.get_com('PartCamera')
        ctrl = scn.get_com('PartCtrl')
        if not com_camera or not ctrl or not global_data.player:
            return
        self._needed_camera_event = False
        player_id = global_data.player.id
        pitch = pitch / com_camera.camera_y_slide_dir
        if self._ctrl_type == _CTRL_TYPE_AVATAR:
            ctrl.rotate_camera(yaw, pitch, False, ignore_aim_ratio=True)
        elif self._ctrl_type == _CTRL_TYPE_SPECTATOR:
            ctrl.puppet_rotate_camera(yaw, pitch)
        else:
            self._recoil_pitch_total = 0
            return
        camera_pitch = com_camera.get_pitch()
        if self._camera_pitch and camera_pitch >= self._camera_pitch:
            self._recoil_pitch_total = 0
        self._needed_camera_event = True

    def _camera_recoil_recover(self):
        if self._camera_delta_pitch < 0:
            self._recoil_pitch_total += self._camera_delta_pitch
        if self._recoil_yaw_total * self._camera_delta_yaw < 0:
            if self._recoil_yaw_total < 0:
                self._recoil_yaw_total = min(self._recoil_yaw_total + self._camera_delta_yaw, 0)
            else:
                self._recoil_yaw_total = max(self._recoil_yaw_total + self._camera_delta_yaw, 0)
        self._camera_delta_pitch = 0
        self._camera_delta_yaw = 0

    def _cal_recoil_total(self, delta):
        conf = self._weapon.conf
        delta_pitch = 0
        delta_yaw = 0
        if self._recoil_pitch_total < self._fire_maxup:
            delta_pitch = self._recoil_pitch_v * delta * _RADIANS_FACTOR
        if abs(self._recoil_yaw_total) >= self._fire_maxyaw:
            if self._recoil_yaw_total * self._recoil_yaw_v < 0:
                delta_yaw += self._recoil_yaw_v * delta * _RADIANS_FACTOR
        else:
            delta_yaw = self._recoil_yaw_v * delta * _RADIANS_FACTOR
        self._recoil_pitch_total += delta_pitch
        self._recoil_yaw_total += delta_yaw
        if delta_yaw != 0 or delta_pitch != 0:
            self._rotate_camera(delta_yaw, delta_pitch)

    def _cal_recoil_recover(self, now_time, delta):
        delay_time = self._weapon.get_data_by_key('fDelayRecover')
        if delay_time == -1.0:
            delay_time = min(self._fire_cd, _MAX_RECOVER_TIME)
        if self._weapon.get_effective_value('iMode') != weapon_const.MANUAL_MODE and now_time - self._fire_time <= delay_time:
            return
        init_recoil_pitch_total = self._recoil_pitch_total
        init_recoil_yaw_total = self._recoil_yaw_total
        if self._recoil_pitch_total > 0:
            cot = abs(self._recoil_yaw_total / self._recoil_pitch_total)
        else:
            cot = 1
        self._recoil_recover_v += self._weapon.get_effective_value('fRecoilDec') * delta
        recover_value = self._recoil_recover_v * delta * _RADIANS_FACTOR
        if self._recoil_pitch_total > 0:
            if recover_value >= self._recoil_pitch_total:
                recover_pitch = -self._recoil_pitch_total
                self._recoil_pitch_total = 0
            else:
                self._recoil_pitch_total -= recover_value
                recover_pitch = -recover_value
        else:
            recover_pitch = 0
        recover_value *= cot
        if self._recoil_yaw_total > 0:
            if recover_value >= self._recoil_yaw_total:
                recover_yaw = -self._recoil_yaw_total
                self._recoil_yaw_total = 0
            else:
                self._recoil_yaw_total -= recover_value
                recover_yaw = -recover_value
        elif self._recoil_yaw_total < 0:
            if -recover_value <= self._recoil_yaw_total:
                recover_yaw = -self._recoil_yaw_total
                self._recoil_yaw_total = 0
            else:
                self._recoil_yaw_total += recover_value
                recover_yaw = recover_value
        else:
            recover_yaw = 0
        self._rotate_camera(recover_yaw, recover_pitch)

    def tick(self, delta):
        if not self._weapon:
            self.need_update = False
            self._camera_pitch = None
            self._is_first_dire = True
            return
        else:
            parachute_stage = self.unit_obj.share_data.ref_parachute_stage
            ban_recoil_stage = parachute_utils.BAN_RECOIL_STAGE
            if parachute_stage & ban_recoil_stage:
                return
            now_time = time.time()
            self._camera_recoil_recover()
            recoil_delta = self._cal_recoil_v(delta)
            if recoil_delta <= 0:
                self._cal_recoil_recover(now_time, delta)
            else:
                self._cal_recoil_total(recoil_delta)
            if self._is_auto_fire:
                if now_time - self._fire_time > self._fire_cd:
                    self.send_event('E_TRY_FIRE')
            elif self._recoil_pitch_total <= 0 and self._recoil_yaw_total == 0:
                if self._is_fire_end:
                    self.need_update = False
                    self._camera_pitch = None
                    self._is_first_dire = True
                elif now_time - self._fire_time > self._fire_cd:
                    self._is_fire_end = True
                    self.ev_g_cancel_state(st_const.ST_SHOOT)
                    self.send_event('E_ATTACK_END')
                    self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_END, ()], True)
            return

    def get_spreadinc(self, conf):
        spreadinc = conf('fSpreadInc')
        if isinstance(spreadinc, list):
            area = spreadinc[0]
            data = spreadinc[1]
            all_spread = 0
            for index in range(len(area)):
                all_spread += area[index] * data[index]
                if self._spread < all_spread:
                    return data[index]
                return data[-1]

        else:
            return spreadinc

    def _on_reloaded(self, *args):
        self._cur_sequence_num = 0.0
        if self._weapon:
            zhunxin_key = confmgr.get('firearm_res_config', str(self._weapon.iType), 'cAimIcon')
            if zhunxin_key == 'lmg':
                conf = self._weapon.conf
                if self.sd.ref_in_aim or self.sd.ref_in_right_aim:
                    self._spread = self._weapon.get_effective_value('fAimMaxSpread', default=0)
                else:
                    self._spread = self._weapon.get_effective_value('fMaxSpread', default=0)

    def _on_parachute_status_changed(self, stage):
        self._stop_auto_fire(force=False, fire=False)

    def _puppet_attack_start(self, *args):
        if self._weapon is None:
            return
        else:
            if self._weapon.get_effective_value('iMode') in [weapon_const.AUTO_MODE]:
                self.get_spread_value()
                self._is_auto_fire = True
            else:
                self._is_auto_fire = False
            return

    def _puppet_attack_end(self, *args):
        self._is_auto_fire = False

    def _pullet_accumulate_end(self, *args):
        self.send_event('E_CTRL_ACCUMULATE', False)