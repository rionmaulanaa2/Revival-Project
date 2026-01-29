# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaRecoil.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import random
from math import radians, tan, pi
import math3d
import world
import time
from logic.gcommon.common_const import weapon_const
from logic.units.LAvatar import LAvatar
from ..UnitCom import UnitCom
import logic.gcommon.const as g_const
from collections import defaultdict
from logic.gcommon.cdata import mecha_status_config
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const import attr_const
from math import isnan
from logic.gutils.frame_data_utils import filter_duplicated_execution, filter_duplicated_execution_with_arg_key
from logic.gcommon.const import NEOX_UNIT_SCALE
SEQUENCE_RECOVER_MIN_INTERVAL = 0.3
SEQUENCE_RECOVER_SPEED = 1.0 / 0.16666665
MAX_RECOVER_TIME = 0.2
UP_VECTOR = math3d.vector(0, 1, 0)
DOWN_VECTOR = math3d.vector(0, -1, 0)

class ComMechaRecoil(UnitCom):
    BIND_EVENT = {'E_DELTA_YAW': '_on_yaw',
       'E_DELTA_PITCH': '_on_pitch',
       'E_FIRE': '_on_fire',
       'G_MECHA_FIRE_RAY': '_on_fire_ray',
       'G_MECHA_FIRE_RAY_WITHOUT_SPREAD': '_on_fire_ray_without_spread',
       'G_SPREAD_VALUES': 'get_spread_values',
       'G_SPREAD_INCREASE': 'get_spreadinc',
       'E_SIMULATE_FIRE': '_simulate_fire',
       'E_MECHA_AIM_TARGET': '_set_target',
       'E_PUPPET_ATTACK_START': '_puppet_attack_start',
       'E_PUPPET_ATTACK_END': '_puppet_attack_end',
       'G_SEQUENCE_NUM': 'get_sequence_num',
       'G_MECHA_WEAPON': 'get_weapon',
       'E_OVERRIDE_SPREAD_BASE': 'on_override_spread_base',
       'E_CLEAR_SPREAD_OVERRIDE': 'on_clear_spread_override',
       'E_SET_SPREAD_RECOVER_OFF_TIME': 'set_spread_recover_off_time'
       }
    BIND_ATTR_CHANGE = {attr_const.ATTR_HIP_JUMP_FACTOR: 'on_add_attr_changed',
       attr_const.ATTR_HIP_STAND_STOP_FACTOR: 'on_add_attr_changed',
       attr_const.ATTR_HIP_STAND_MOVE_FACTOR: 'on_add_attr_changed'
       }

    def __init__(self):
        super(ComMechaRecoil, self).__init__(True)
        self._last_weapon_pos = None
        self._camera_delta_yaw = 0
        self._camera_delta_pitch = 0
        self._recoil_yaw_v = 0
        self._recoil_pitch_v = 0
        self._recoil_yaw_total = 0
        self._recoil_pitch_total = 0
        self._camera_pitch = None
        self._recoil_time = 0
        self._recoil_recover_v = 0
        self._recoil_last_fire_time = 0
        self._override_spread_base = None
        self._last_sequence_time = defaultdict(float)
        self._sequence_num = defaultdict(float)
        self._spreads = defaultdict(float)
        self._spreads_recover_time = defaultdict(float)
        self._spread_recover_off_time = 0
        self._is_auto_fire = False
        self._is_first_dire = True
        self._aim_targets = {}
        self._needed_camera_event = True
        self.matrix = None
        self.sim_count = 0
        self.sim_dist = 1
        self._is_avatar = False
        self._last_cam_trans = None
        self._jump_status = {
         mecha_status_config.MC_JUMP_1, mecha_status_config.MC_JUMP_2,
         mecha_status_config.MC_DASH_JUMP_1, mecha_status_config.MC_DASH_JUMP_2,
         mecha_status_config.MC_OTHER_JUMP_1, mecha_status_config.MC_OTHER_JUMP_2,
         mecha_status_config.MC_SUPER_JUMP, mecha_status_config.MC_OTHER_SUPER_JUMP}
        self._ai_camera_pitch = 1.0
        self._ai_camera_direction = 5
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaRecoil, self).init_from_dict(unit_obj, bdict)
        self._is_avatar = isinstance(self.unit_obj, LAvatar)
        self._last_weapon_pos = g_const.PART_WEAPON_POS_MAIN1

    def destroy(self):
        self._aim_targets.clear()
        super(ComMechaRecoil, self).destroy()

    def on_init_complete(self):
        mecha_id = self.sd.ref_mecah_id
        if mecha_id == 8005:
            self._ai_camera_pitch = 0.75
        elif mecha_id == 8009:
            self._ai_camera_direction = 30

    def get_weapon(self, weapon_pos):
        return self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)

    def on_override_spread_base(self, state, spread_base):
        self._override_spread_base = (
         state, spread_base)

    def on_clear_spread_override(self):
        self._override_spread_base = None
        return

    @filter_duplicated_execution_with_arg_key(1)
    def get_spread_base(self, weapon_pos, weapon):
        cur_state = self.ev_g_get_all_state() or set()
        spread_scale = 1.0
        if self.sd.ref_in_aim:
            spread_base = weapon.get_config().get('fADSStop' if self.ev_g_is_move() else 'fADSMove', 0)
        else:
            overlay_state = weapon.get_data_by_key('cHIPOverlayState')
            if overlay_state:
                for str_state, scale in six.iteritems(overlay_state):
                    state = mecha_status_config.desc_2_num[str_state]
                    if state in cur_state:
                        spread_scale *= scale

            custom_state = weapon.get_data_by_key('cHIPCustomState')
            if custom_state:
                for str_state, value in six.iteritems(custom_state):
                    state = mecha_status_config.desc_2_num[str_state]
                    if state in cur_state:
                        return spread_scale * value

            if mecha_status_config.MC_MOVE in cur_state:
                spread_base = weapon.get_config().get('fHIPStandMove', 0)
                spread_base *= 1 + self.ev_g_add_attr(attr_const.ATTR_HIP_STAND_MOVE_FACTOR, weapon.get_item_id())
            elif mecha_status_config.MC_RUN in cur_state or mecha_status_config.MC_VEHICLE in cur_state and self.sd.ref_cur_speed > 0:
                spread_base = weapon.get_data_by_key('fHIPRun')
                if spread_base == 0.0:
                    spread_base = weapon.get_data_by_key('fHIPStandMove')
                    spread_base *= 1 + self.ev_g_add_attr(attr_const.ATTR_HIP_STAND_MOVE_FACTOR, weapon.get_item_id())
            elif self._jump_status & cur_state:
                spread_base = weapon.get_config().get('fHIPJump', 0)
                spread_base *= 1 + self.ev_g_add_attr(attr_const.ATTR_HIP_JUMP_FACTOR, weapon.get_item_id())
            else:
                spread_base = weapon.get_config().get('fHIPStandStop', 0)
                spread_base *= 1 + self.ev_g_add_attr(attr_const.ATTR_HIP_STAND_STOP_FACTOR, weapon.get_item_id())
            if self._override_spread_base:
                override_state, override_spread_base = self._override_spread_base
                if override_state in cur_state:
                    spread_base = override_spread_base
        spread_base *= spread_scale
        return self.ev_g_addition_effect(spread_base, weapon.get_item_id(), factor_attrs=[attr_const.ATTR_SPREAD_FACTOR])

    def get_spread_value(self, weapon, weapon_pos):
        delta = time.time() - self._spreads_recover_time[weapon_pos]
        if delta > 0:
            self._spreads[weapon_pos] -= weapon.get_data_by_key('fSpreadDec') * delta
            if self._spreads[weapon_pos] < 0.0:
                self._spreads[weapon_pos] = 0.0
            self._spreads_recover_time[weapon_pos] += delta
        return self._spreads[weapon_pos]

    def get_spread_values(self, weapon=None, weapon_pos=None):
        if not weapon_pos:
            weapon_pos = g_const.PART_WEAPON_POS_MAIN1
            weapon = self.get_weapon(weapon_pos)
        else:
            if not weapon:
                weapon = self.get_weapon(weapon_pos)
            if weapon and weapon.is_accumulate_gun():
                last_accumulate_duration = self.ev_g_accumulate_duration(weapon_pos)
                accumulate_level = weapon.get_accumulate_level(last_accumulate_duration)
                new_weapon_pos = weapon_pos + accumulate_level
                if new_weapon_pos != weapon_pos:
                    new_weapon = self.get_weapon(new_weapon_pos)
                    if new_weapon:
                        weapon = new_weapon
                        weapon_pos = new_weapon_pos
            if not weapon:
                print(('test--ComMechaRecoil.get_spread_values--step1--weapon_pos =', weapon_pos, '--weapon =', weapon, '--unit_obj =', self.unit_obj))
                import traceback
                traceback.print_stack()
                return (0, 0, 0)
        spread_base = self.get_spread_base(weapon_pos, weapon)
        spread_value = self.get_spread_value(weapon, weapon_pos)
        recover_time = 0.1
        spread_dec = weapon.get_data_by_key('fSpreadDec')
        if spread_dec > 0:
            recover_time = spread_value / spread_dec
        return (spread_base, spread_base + spread_value, recover_time)

    def _set_target(self, target, weapon_pos, **kwargs):
        self._aim_targets[weapon_pos] = target

    def _fire_sequence(self, weapon, weapon_pos):
        max_sequence = weapon.get_data_by_key('iMaxSequence')
        if max_sequence == 0:
            return
        self._last_sequence_time[weapon_pos] = time.time()
        self._sequence_num[weapon_pos] += 1
        if self._sequence_num[weapon_pos] > max_sequence:
            self._sequence_num[weapon_pos] = max_sequence

    def get_sequence_num(self, weapon_pos=g_const.PART_WEAPON_POS_MAIN1):
        weapon = self.get_weapon(weapon_pos)
        if not weapon:
            return
        delta = time.time() - self._last_sequence_time[weapon_pos] - SEQUENCE_RECOVER_MIN_INTERVAL
        if delta > 0:
            recover_speed = self.get_sequence_recover_speed(weapon)
            self._sequence_num[weapon_pos] -= recover_speed * delta
            if self._sequence_num[weapon_pos] < 0:
                self._sequence_num[weapon_pos] = 0
            self._last_sequence_time[weapon_pos] = time.time() - SEQUENCE_RECOVER_MIN_INTERVAL
        return int(self._sequence_num[weapon_pos])

    def get_sequence_recover_speed(self, weapon):
        return weapon.get_sequence_recover_speed() or SEQUENCE_RECOVER_SPEED

    def get_target_direction(self, start_pos, weapon, weapon_pos, aim_target_index, ignore_fire_pos, camera_direction):
        auto_aim_distance = weapon.get_data_by_key('fAutoAimDistance')
        if auto_aim_distance is None:
            return
        else:
            custom_param = weapon.conf('cCustomParam', {})
            follow_aim_weapon_pos = custom_param.get('follow_aim_weapon_pos', None)
            if follow_aim_weapon_pos:
                weapon_pos = follow_aim_weapon_pos
            if not self._aim_targets.get(weapon_pos):
                return
            if aim_target_index > -1:
                aim_target = self._aim_targets[weapon_pos][aim_target_index]
            else:
                aim_target = self._aim_targets[weapon_pos]
            if custom_param.get('apply_aim_helper_if_miss', False):
                if aim_target.ev_g_model_hit_ray(start_pos, camera_direction * weapon.get_data_by_key('iShootRange') * NEOX_UNIT_SCALE) is not None:
                    return
            model = aim_target.ev_g_model()
            if not model:
                return
            matrix = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
            if not matrix:
                return
            aim_pos = matrix.translation
            if ignore_fire_pos == weapon_const.SHOOT_FROM_MUZZLE:
                _, fire_pos = self.ev_g_fire_pos(weapon_pos, keep_socket_index=True)
                if fire_pos:
                    start_pos = fire_pos
            direction = aim_pos - start_pos
            if direction.is_zero:
                return
            direction.normalize()
            return direction

    def _get_cam_trans(self):
        partcamera = self.scene.get_com('PartCamera')
        camera = partcamera.cam
        from logic.client.const import camera_const
        cameradata = partcamera.cam_manager.last_camera_state_setting
        matrix = None
        if cameradata:
            if partcamera.get_cur_camera_state_type() == camera_const.FREE_MODEL:
                matrix = cameradata['trans']
                self._last_cam_trans = matrix
            elif partcamera.is_out_cam_state_slerp(camera_const.FREE_MODEL):
                matrix = self._last_cam_trans
        if matrix is None:
            matrix = camera.world_rotation_matrix
        return matrix

    @filter_duplicated_execution
    def _on_get_camera_param(self):
        if self.sd.ref_is_agent:
            model = self.ev_g_model()
            if not model:
                return (None, None, None)
            m_height = model.bounding_box.y * self._ai_camera_pitch
            m_pos = model.position
            if not m_pos:
                return (None, None, None)
            camera_pos = math3d.vector(m_pos.x, m_pos.y + m_height, m_pos.z)
            attack_pos = self.ev_g_attack_pos()
            if not attack_pos:
                return (None, None, None)
            camera_direction = attack_pos - camera_pos
            if camera_direction.is_zero:
                return (None, None, None)
            camera_direction.normalize()
            if camera_direction == UP_VECTOR or camera_direction == DOWN_VECTOR:
                return (None, None, None)
            camera_pos = camera_pos + camera_direction * self._ai_camera_direction
            right = camera_direction.cross(math3d.vector(0, 1, 0))
            up = right.cross(camera_direction)
            return (
             camera_pos, camera_direction, up)
        else:
            camera = self.scene.get_com('PartCamera').cam
            if not camera:
                return (None, None, None)
            matrix = self._get_cam_trans()
            camera_pos = camera.world_position
            return (
             camera_pos, matrix.forward, matrix.up)
            return None

    def _on_fire_ray(self, weapon_pos=g_const.PART_WEAPON_POS_MAIN1, aim_target_index=-1, check_aim_target=True, ignore_fire_pos=weapon_const.SHOOT_FROM_CAMERA):
        weapon = self.get_weapon(weapon_pos)
        if weapon and weapon.is_accumulate_gun():
            last_accumulate_duration = self.ev_g_accumulate_duration(weapon_pos)
            accumulate_level = weapon.get_accumulate_level(last_accumulate_duration)
            new_weapon_pos = weapon_pos + accumulate_level
            if new_weapon_pos != weapon_pos:
                new_weapon = self.get_weapon(new_weapon_pos)
                if new_weapon:
                    weapon = new_weapon
                    weapon_pos = new_weapon_pos
        if not weapon:
            return
        else:
            camera_pos, camera_direction, camera_up = self._on_get_camera_param()
            if not camera_pos:
                return
            if isnan(camera_pos.x) or isnan(camera_pos.y) or isnan(camera_pos.z):
                return
            if not camera_pos or not camera_direction:
                return
            direction = None
            if check_aim_target:
                direction = self.get_target_direction(camera_pos, weapon, weapon_pos, aim_target_index, ignore_fire_pos, camera_direction)
            if direction is None:
                direction = camera_direction
                camera_direction = None
            spread_value = self.get_spread_base(weapon_pos, weapon) + self.get_spread_value(weapon, weapon_pos)
            spread_range = random.uniform(0, tan(radians(spread_value)))
            rotation_matrix = math3d.matrix.make_rotation(direction, random.uniform(-pi, pi))
            direction += camera_up * rotation_matrix * spread_range
            direction.normalize()
            return (
             camera_pos, direction, camera_direction)

    def _on_fire_ray_without_spread(self, weapon_pos=g_const.PART_WEAPON_POS_MAIN1, aim_target_index=-1, check_aim_target=True, ignore_fire_pos=weapon_const.SHOOT_FROM_CAMERA):
        weapon = self.get_weapon(weapon_pos)
        if not weapon:
            return
        else:
            camera_pos, camera_direction, camera_up = self._on_get_camera_param()
            if not camera_pos or not camera_direction:
                return
            direction = None
            if check_aim_target:
                direction = self.get_target_direction(camera_pos, weapon, weapon_pos, aim_target_index, ignore_fire_pos, camera_direction)
            if direction is None:
                direction = camera_direction
                camera_direction = None
            return (
             camera_pos, direction, camera_direction)

    def _on_yaw(self, dx, *args):
        if self._needed_camera_event and self.need_update:
            self._camera_delta_yaw = dx

    def _on_pitch(self, dy):
        if self._needed_camera_event and self.need_update and self._camera_pitch is not None:
            self._camera_delta_pitch = -dy
            if dy < 0:
                com_camera = self.scene.get_com('PartCamera')
                if com_camera:
                    self._camera_pitch = max(com_camera.get_pitch(), self._camera_pitch)
        return

    def _fire_recoil(self, weapon):
        self._recoil_last_fire_time = time.time()
        self._recoil_recover_v = 0
        if self._recoil_pitch_total >= radians(weapon.get_data_by_key('fMaxUp')):
            self._recoil_pitch_v = 0
        else:
            self._recoil_pitch_v = weapon.get_data_by_key('fRecoilUp')
        self._recoil_time = weapon.get_data_by_key('fRecoilTime')
        self._recoil_yaw_v = random.uniform(-weapon.get_data_by_key('fRecoilLeft'), weapon.get_data_by_key('fRecoilRight'))
        if weapon:
            if not weapon.is_accumulate_gun() and self.ev_g_need_play_each_fire_camera_trk(weapon.iType):
                self.send_event('E_PLAY_WEAPON_FIRE_CAMERA_TRK', weapon.iType)
        if abs(self._recoil_yaw_total) >= abs(radians(weapon.get_data_by_key('fMaxYaw'))):
            if self._recoil_yaw_v * self._recoil_yaw_total > 0:
                self._recoil_yaw_v = -self._recoil_yaw_v
        if self.sd.ref_in_aim:
            aim_mod = weapon.get_data_by_key('fAimMod') or 1
            self._recoil_pitch_v *= aim_mod
            self._recoil_yaw_v *= aim_mod
        weapon_recoil_sub_factor = self.ev_g_add_attr(attr_const.MECHA_RECOIL_UP_SUB_FACTOR, weapon.get_item_id())
        if weapon_recoil_sub_factor:
            self._recoil_pitch_v *= 1 - weapon_recoil_sub_factor
            self._recoil_yaw_v *= 1 - weapon_recoil_sub_factor
        self.need_update = True
        if self._is_first_dire:
            self._is_first_dire = False
            mul = weapon.get_data_by_key('fFirstShotMul')
            self._recoil_pitch_v *= mul
            self._recoil_yaw_v *= mul
            com_camera = self.scene.get_com('PartCamera')
            if com_camera:
                self._camera_pitch = com_camera.get_pitch()

    def set_spread_recover_off_time(self, off_time):
        self._spread_recover_off_time = off_time

    def _fire_spread(self, weapon, weapon_pos):
        if self.sd.ref_in_aim:
            spread_inc = weapon.get_data_by_key('fAimSpreadInc')
        else:
            spread_inc = self.get_spreadinc(weapon, weapon_pos)
        spread_inc *= 1 + self.ev_g_add_attr(attr_const.ATTR_SPREAD_FACTOR, weapon.get_item_id()) + self.ev_g_add_attr(attr_const.ATTR_SPREAD_INC_FACTOR, weapon.get_item_id()) + (weapon.heat_magazine.get_fire_spread_ratio() if weapon.heat_magazine else 0)
        self._spreads[weapon_pos] += spread_inc
        max_spread = weapon.get_config().get('fMaxSpread', 0)
        max_spread *= 1 + self.ev_g_add_attr(attr_const.ATTR_SPREAD_FACTOR, weapon.get_item_id()) + self.ev_g_add_attr(attr_const.ATTR_SPREAD_MAX_FACTOR, weapon.get_item_id()) + self.ev_g_add_attr('spread_factor_pos_%s' % weapon_pos)
        if max_spread and max_spread < self._spreads[weapon_pos]:
            self._spreads[weapon_pos] = max_spread
        min_spread = weapon.get_data_by_key('fMinSpread')
        if max_spread and min_spread and self._spreads[weapon_pos] < min_spread < max_spread:
            self._spreads[weapon_pos] = min_spread
        if self._spreads[weapon_pos] < 0:
            self._spreads[weapon_pos] = 0
        now = time.time()
        if self._spreads_recover_time[weapon_pos] <= now:
            self._spreads_recover_time[weapon_pos] = now + weapon.get_fire_cd() + self._spread_recover_off_time
        else:
            self._spreads_recover_time[weapon_pos] += weapon.get_fire_cd() + self._spread_recover_off_time

    def get_spreadinc(self, weapon, weapon_pos):
        spreadinc = weapon.get_data_by_key('fSpreadInc')
        if isinstance(spreadinc, list):
            area = spreadinc[0]
            data = spreadinc[1]
            all_spread = 0
            for index in range(len(area)):
                all_spread += area[index] * data[index]
                if self._spreads[weapon_pos] < all_spread:
                    return data[index]
                return data[-1]

        else:
            return spreadinc

    def _on_fire(self, cd_time, weapon_pos, *args):
        weapon = self.get_weapon(weapon_pos)
        if not weapon:
            return None
        else:
            self._last_weapon_pos = weapon_pos
            self._fire_recoil(weapon)
            self._fire_sequence(weapon, weapon_pos)
            self._fire_spread(weapon, weapon_pos)
            if self.unit_obj and global_data.player and self.unit_obj.id == global_data.player.id:
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SIMULATE_FIRE,
                 (
                  self._recoil_pitch_v, self._recoil_yaw_v, self._camera_pitch, weapon_pos)], True)
            spread_base, spread_value, recover_time = self.get_spread_values(weapon, weapon_pos)
            self.send_event('E_AIM_SPREAD', spread_base, spread_value, weapon.get_fire_cd(), recover_time, weapon_pos)
            return None

    def _simulate_fire(self, pitch_v, yaw_v, camera_pitch, weapon_pos):
        if global_data.cam_lplayer is global_data.player.logic:
            return None
        else:
            weapon = self.get_weapon(weapon_pos)
            if not weapon:
                return None
            self._recoil_last_fire_time = time.time()
            self._recoil_pitch_v = pitch_v
            self._recoil_yaw_v = yaw_v
            self._camera_pitch = camera_pitch
            self._spreads[weapon_pos] += self.get_spreadinc(weapon, weapon_pos)
            max_spread = weapon.get_data_by_key('fMaxSpread')
            if max_spread and max_spread < self._spreads[weapon_pos]:
                self._spreads[weapon_pos] = max_spread
            min_spread = weapon.get_data_by_key('fMinSpread')
            if min_spread and max_spread:
                if self._spreads[weapon_pos] < min_spread < max_spread:
                    self._spreads[weapon_pos] = min_spread
                spread_base, spread_value, recover_time = self.get_spread_values(weapon, weapon_pos)
                self.send_event('E_AIM_SPREAD', spread_base, spread_value, weapon.get_fire_cd(), recover_time, weapon_pos)
                self.need_update = self.need_update or True
            return None

    def _cal_recoil_v(self, delta, weapon):
        if delta >= self._recoil_time:
            self._recoil_time = 0
            delta = self._recoil_time
            if self._recoil_recover_v < weapon.get_data_by_key('fRecoverV'):
                self._recoil_recover_v = weapon.get_data_by_key('fRecoverV')
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
        com_camera = self.scene.get_com('PartCamera')
        ctrl = self.scene.get_com('PartCtrl')
        if not com_camera or not ctrl or not global_data.player:
            return
        self._needed_camera_event = False
        player_id = global_data.player.id
        if self.unit_obj and self.unit_obj.id == player_id or self.sd.ref_driver_id == player_id:
            rotate_func = lambda yaw, pitch: ctrl.rotate_camera(yaw, pitch, False)
        elif self.is_spectate_target():
            rotate_func = ctrl.puppet_rotate_camera
        else:
            self._recoil_pitch_total = 0
            return
        rotate_func(yaw, pitch / com_camera.camera_y_slide_dir)
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

    def _cal_recoil_total(self, delta, weapon):
        delta_pitch = 0
        delta_yaw = 0
        if self._recoil_pitch_total < radians(weapon.get_data_by_key('fMaxUp')):
            delta_pitch = radians(self._recoil_pitch_v * delta)
        if abs(self._recoil_yaw_total) >= radians(weapon.get_data_by_key('fMaxYaw')):
            if self._recoil_yaw_total * self._recoil_yaw_v < 0:
                delta_yaw += radians(self._recoil_yaw_v * delta)
        else:
            delta_yaw = radians(self._recoil_yaw_v * delta)
        self._recoil_pitch_total += delta_pitch
        self._recoil_yaw_total += delta_yaw
        if delta_yaw != 0 or delta_pitch != 0:
            self._rotate_camera(delta_yaw, delta_pitch)

    def _cal_recoil_recover(self, now_time, delta, weapon):
        delay_time = weapon.get_data_by_key('fDelayRecover')
        if delay_time == -1.0:
            delay_time = min(weapon.get_fire_cd(), MAX_RECOVER_TIME)
        if weapon.get_data_by_key('iMode') != weapon_const.MANUAL_MODE and now_time - self._recoil_last_fire_time <= delay_time:
            return
        if self._recoil_pitch_total > 0:
            cot = abs(self._recoil_yaw_total / self._recoil_pitch_total)
        else:
            cot = 1
        self._recoil_recover_v += weapon.get_data_by_key('fRecoilDec') * delta
        recover_value = radians(self._recoil_recover_v) * delta
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
        if self._recoil_yaw_total != 0:
            if self._recoil_yaw_total > 0:
                if recover_value >= self._recoil_yaw_total:
                    self._recoil_yaw_total = 0
                    recover_yaw = -self._recoil_yaw_total
                else:
                    self._recoil_yaw_total -= recover_value
                    recover_yaw = -recover_value
            elif -recover_value <= self._recoil_yaw_total:
                self._recoil_yaw_total = 0
                recover_yaw = -self._recoil_yaw_total
            else:
                self._recoil_yaw_total += recover_value
                recover_yaw = recover_value
        else:
            recover_yaw = 0
        self._rotate_camera(recover_yaw, recover_pitch)

    def tick(self, delta):
        weapon = self.get_weapon(self._last_weapon_pos)
        if not weapon:
            self.need_update = False
            self._camera_pitch = None
            self._is_first_dire = True
            return
        else:
            now_time = time.time()
            self._camera_recoil_recover()
            recoil_delta = self._cal_recoil_v(delta, weapon)
            if recoil_delta <= 0:
                self._cal_recoil_recover(now_time, delta, weapon)
            else:
                self._cal_recoil_total(recoil_delta, weapon)
            if self._recoil_pitch_total <= 0 and self._recoil_yaw_total == 0:
                self.need_update = False
                self._camera_pitch = None
                self._is_first_dire = True
            return

    def on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        if attr in [attr_const.ATTR_HIP_JUMP_FACTOR, attr_const.ATTR_HIP_STAND_STOP_FACTOR, attr_const.ATTR_HIP_STAND_MOVE_FACTOR]:
            weapon_pos = g_const.PART_WEAPON_POS_MAIN1
            weapon = self.get_weapon(weapon_pos)
            if not weapon:
                return
            spread_base, spread_value, recover_time = self.get_spread_values(weapon, weapon_pos)
            self.send_event('E_AIM_SPREAD', spread_base, spread_value, weapon.get_fire_cd(), recover_time, weapon_pos)