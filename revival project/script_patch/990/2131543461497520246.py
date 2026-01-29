# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAtkContinuousLaser.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from ...cdata.status_config import ST_SHOOT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.skill.client.SkillSecWeapon8016 import get_hit_target, get_fire_end
from logic.gcommon.const import NEOX_UNIT_SCALE, HIT_PART_BODY
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp, tp_to_v3d
from logic.gutils.firearm_sfx_mapping_utils import encode_sfx_info
from logic.vscene.parts import PartCtrl
from common.cfg import confmgr
from math import radians, isnan
from random import randint
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import world
from logic.gcommon.common_const.sync_const import ID_ATTACK_START
from logic.gutils.mecha_utils import do_hit_phantom
SYNC_INTERVAL = 0.05
LASER_END_APPEAR_TIME = 0.1

class ComAtkContinuousLaser(UnitCom):
    BIND_EVENT = {'E_START_AUTO_FIRE': 'start_auto_fire',
       'E_STOP_AUTO_FIRE': 'stop_auto_fire',
       'E_GUN_ATTACK': 'on_attack_start',
       'E_ATTACK_END': 'on_attack_end',
       'E_END_ROLL': 'on_roll_end',
       'E_END_RUSH_EVENT': 'on_roll_end',
       'E_END_PUT_ON_BULLET': 'on_roll_end',
       'E_SUCCESS_RIGHT_AIM': 'enter_right_aim',
       'E_QUIT_RIGHT_AIM': 'quit_right_aim',
       'E_SYNC_CREATE_VICE_EFFECT': 'sync_start_laser',
       'E_SYNC_UPDATE_VICE_EFFECT': 'sync_update_laser',
       'E_CREATE_VICE_END_EFFECT': 'sync_end_laser'
       }

    def __init__(self):
        super(ComAtkContinuousLaser, self).__init__(False)
        self.atk_radius = 2 * NEOX_UNIT_SCALE
        self.cost_bullet_interval = 0.5
        self.max_laser_length = 300 * NEOX_UNIT_SCALE
        self.laser_speed = 50 * NEOX_UNIT_SCALE
        self.laser_start_sfx_path = ''
        self.laser_sfx_path = ''
        self.laser_hit_sfx_path = ''
        self.laser_hit_sfx_scale = 1.0
        self.enemy_laser_start_sfx_path = ''
        self.enemy_laser_sfx_path = ''
        self.enemy_laser_hit_sfx_path = ''
        self.max_delta_value = 0.01
        self.yaw_spread_speed = 0.1
        self.same_yaw_area_max_stay_time = 0.2
        self.pitch_spread_speed = 0.1
        self.same_pitch_area_max_stay_time = 0.2
        self.right_aim_max_delta_value = 0.01
        self.right_aim_yaw_spread_speed = 0.1
        self.right_aim_same_yaw_area_max_stay_time = 0.2
        self.right_aim_pitch_spread_speed = 0.1
        self.right_aim_same_pitch_area_max_stay_time = 0.2
        self.weapon = None
        self.weapon_id = None
        self.is_avatar = False
        self.camp_id = None
        self.can_fire = False
        self.can_continue = False
        self.cur_yaw_offset = 0.0
        self.cur_pitch_offset = 0.0
        self.yaw_spread_dir = 1
        self.pitch_spread_dir = 1
        self.cur_yaw_dir_area_stay_time = 0
        self.cur_pitch_dir_area_stay_time = 0
        self.last_cost_bullet_time = 0
        self.interval_threshold = 0
        self.last_hit_time_map = {}
        self.cur_laser_length = 0
        self.laser_hit_sfx_code = 0
        self.cur_laser_start_sfx_path = ''
        self.cur_laser_sfx_path = ''
        self.cur_laser_hit_sfx_path = ''
        self.laser_start_sfx_id = None
        self.laser_sfx = None
        self.laser_sfx_id = None
        self.laser_end_sfx = None
        self.laser_end_sfx_id = None
        self.laser_end_pos = None
        self.laser_start_time = 0
        self.last_sync_time = 0
        self.tick_func = None
        self.hit_phantom = {}
        self.last_start_auto_fire_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAtkContinuousLaser, self).init_from_dict(unit_obj, bdict)
        self.is_avatar = unit_obj.__class__.__name__ == 'LAvatar' or unit_obj.ev_g_is_agent()
        self.is_agent = unit_obj.ev_g_is_agent()
        self.tick_func = self.avatar_tick if self.is_avatar else self.puppet_tick
        if self.is_avatar:
            if G_POS_CHANGE_MGR:
                self.regist_pos_change(self.refresh_appearance)
            self.regist_event('E_ROTATE', self.refresh_appearance)

    def destroy(self):
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.refresh_appearance)
        self.unregist_event('E_ROTATE', self.refresh_appearance)
        super(ComAtkContinuousLaser, self).destroy()
        if self.is_avatar:
            PartCtrl.enable_clamp_cam_rotation(False)
        self.tick_func = None
        self.on_clear_sfx()
        return

    def set_weapon(self, wp_obj):
        self.weapon = wp_obj
        if wp_obj:
            weapon_id = wp_obj.get_item_id()
            self.weapon_id = weapon_id
            conf = confmgr.get('firearm_config', str(weapon_id))
            self.cost_bullet_interval = conf.get('fCDTime')
            self.interval_threshold = self.cost_bullet_interval + 0.1
            self.atk_radius = conf.get('cRayWeaponRadius', 2) * NEOX_UNIT_SCALE
            self.max_laser_length = conf.get('iShootRange', 500) * NEOX_UNIT_SCALE
            custom_param = conf.get('cCustomParam', {})
            self.max_delta_value = custom_param.get('max_delta_value', 0.01)
            self.yaw_spread_speed = radians(custom_param.get('yaw_spread_speed', 3))
            self.same_yaw_area_max_stay_time = custom_param.get('same_yaw_area_max_stay_time', 0.2)
            self.pitch_spread_speed = radians(custom_param.get('pitch_spread_speed', 3))
            self.same_pitch_area_max_stay_time = custom_param.get('same_pitch_area_max_stay_time', 0.2)
            self.right_aim_max_delta_value = custom_param.get('right_aim_max_delta_value', 0.01)
            self.right_aim_yaw_spread_speed = radians(custom_param.get('right_aim_yaw_spread_speed', 3))
            self.right_aim_same_yaw_area_max_stay_time = custom_param.get('right_aim_same_yaw_area_max_stay_time', 0.2)
            self.right_aim_pitch_spread_speed = radians(custom_param.get('right_aim_pitch_spread_speed', 3))
            self.right_aim_same_pitch_area_max_stay_time = custom_param.get('right_aim_same_pitch_area_max_stay_time', 0.2)
            res_conf = confmgr.get('firearm_res_config', str(weapon_id))
            self.laser_sfx_path = res_conf.get('cSfxBulletFlying', '')
            self.laser_hit_sfx_path = res_conf.get('cSfxHit', '')
            self.laser_hit_sfx_scale = res_conf.get('cSfxHitScale', 1.0)
            self.laser_hit_sfx_code = encode_sfx_info(self.laser_hit_sfx_path, self.laser_hit_sfx_scale)
            self.laser_speed = res_conf.get('cSfxBulletSpeed', 100) * NEOX_UNIT_SCALE
            self.laser_start_sfx_path = res_conf['cCustomParam'][0]['laser_start_sfx_path']
            self.enemy_laser_start_sfx_path = res_conf['cCustomParam'][0]['enemy_laser_start_sfx_path']
            self.enemy_laser_sfx_path = res_conf['cCustomParam'][0]['enemy_laser_sfx_path']
            self.enemy_laser_hit_sfx_path = res_conf['cExtraParam']['camp_diff']
        else:
            self.weapon = None
        return

    def _determine_laser_sfx_path(self):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != self.ev_g_camp_id():
            self.cur_laser_start_sfx_path = self.enemy_laser_start_sfx_path
            self.cur_laser_sfx_path = self.enemy_laser_sfx_path
            self.cur_laser_hit_sfx_path = self.enemy_laser_hit_sfx_path
        else:
            self.cur_laser_start_sfx_path = self.laser_start_sfx_path
            self.cur_laser_sfx_path = self.laser_sfx_path
            self.cur_laser_hit_sfx_path = self.laser_hit_sfx_path

    def start_auto_fire(self, *args, **kwargs):
        now = global_data.game_time
        if now - self.last_start_auto_fire_time <= self.cost_bullet_interval + 0.1:
            return
        else:
            self.last_start_auto_fire_time = now
            if self.weapon is None:
                self.send_event('E_SHOW_MESSAGE', get_text_by_id(18001))
                return
            wp = self.weapon
            if not self.is_agent and wp.get_bullet_num() < wp.get_cost_ratio():
                self.send_event('E_TRY_RELOAD')
                self.can_fire = False
                self.can_continue = False
                self.need_update = True
                return
            if not self.ev_g_status_try_trans(ST_SHOOT):
                return
            self._determine_laser_sfx_path()
            self.send_event('E_GUN_ATTACK')
            self.send_event('E_ATTACK_START')
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_START, (), None, True, ID_ATTACK_START, 'E_ATTACK_END'], True)
            self.need_update = True
            return

    def continue_auto_fire(self):
        self._determine_laser_sfx_path()
        self.send_event('E_GUN_ATTACK')
        self.send_event('E_ATTACK_START')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_START, (), None, True, ID_ATTACK_START, 'E_ATTACK_END'], True)
        return

    def stop_auto_fire(self, *args, **kwargs):
        wp = self.weapon
        if wp.get_bullet_num() < wp.get_cost_ratio():
            self.send_event('E_TRY_RELOAD')
        self.unit_obj.send_event('E_ATTACK_END')
        self.need_update = False
        self.on_attack_end()

    def on_attack_start(self):
        if not self.is_avatar:
            return
        if self.is_agent:
            self._determine_laser_sfx_path()
        self.camp_id = self.ev_g_camp_id()
        if not self.is_agent:
            PartCtrl.enable_clamp_cam_rotation(True, self.right_aim_max_delta_value if self.sd.ref_in_right_aim else self.max_delta_value)
        self.can_fire = True
        self.cur_yaw_offset = 0
        self.cur_pitch_offset = 0
        self.cur_yaw_dir_area_stay_time = 0
        self.cur_pitch_dir_area_stay_time = 0
        self.yaw_spread_dir = -self.pitch_spread_dir
        self.last_cost_bullet_time = 0
        self.cur_laser_length = 0
        self.tick(0.01)
        if self.laser_end_pos:
            end_pos_tuple = (
             self.laser_end_pos.x, self.laser_end_pos.y, self.laser_end_pos.z)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_CREATE_VICE_EFFECT, (end_pos_tuple,)], True)

    def on_attack_end(self):
        if not self.is_avatar:
            return
        self.can_fire = False
        self.can_continue = False
        PartCtrl.enable_clamp_cam_rotation(False)
        self.on_clear_sfx()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_VICE_END_EFFECT, ()], True)

    def on_roll_end(self, *args):
        self.can_continue = True
        self.cur_yaw_offset = 0
        self.cur_pitch_offset = 0

    def _update_aim_offset(self, dt):
        if self.sd.ref_in_right_aim:
            yaw_spread_speed = self.right_aim_yaw_spread_speed
            same_yaw_area_max_stay_time = self.right_aim_same_yaw_area_max_stay_time
            pitch_spread_speed = self.right_aim_pitch_spread_speed
            same_pitch_area_max_stay_time = self.right_aim_same_pitch_area_max_stay_time
        else:
            yaw_spread_speed = self.yaw_spread_speed
            same_yaw_area_max_stay_time = self.same_yaw_area_max_stay_time
            pitch_spread_speed = self.pitch_spread_speed
            same_pitch_area_max_stay_time = self.same_pitch_area_max_stay_time
        old_yaw_offset = self.cur_yaw_offset
        self.cur_yaw_offset += yaw_spread_speed * dt * self.yaw_spread_dir
        if old_yaw_offset * self.cur_yaw_offset < 0:
            self.cur_yaw_dir_area_stay_time = 0
        else:
            self.cur_yaw_dir_area_stay_time += dt
        if self.cur_yaw_dir_area_stay_time > same_yaw_area_max_stay_time:
            if self.yaw_spread_dir * self.cur_yaw_offset > 0:
                self.yaw_spread_dir = -1 if self.cur_yaw_offset > 0 else 1
        elif randint(1, 4) == 1:
            self.yaw_spread_dir *= -1
        old_pitch_offset = self.cur_pitch_offset
        self.cur_pitch_offset += pitch_spread_speed * dt * self.pitch_spread_dir
        if old_pitch_offset * self.cur_pitch_offset < 0:
            self.cur_pitch_dir_area_stay_time = 0
        else:
            self.cur_pitch_dir_area_stay_time += dt
        if self.cur_pitch_dir_area_stay_time > same_pitch_area_max_stay_time:
            if self.pitch_spread_dir * self.cur_pitch_offset > 0:
                self.pitch_spread_dir = -1 if self.cur_pitch_offset > 0 else 1
        elif randint(1, 4) == 1:
            self.pitch_spread_dir *= -1

    def _update_laser_end_pos(self, dt, start_pos, end_pos):
        forward = end_pos - start_pos
        if forward.is_zero:
            return (end_pos, True)
        if self.is_agent:
            return (end_pos, False)
        dist = forward.length
        forward.normalize()
        reach_end = False
        self.cur_laser_length += self.laser_speed * dt
        if self.cur_laser_length >= dist:
            self.cur_laser_length = dist
            reach_end = True
        end_pos = start_pos + forward * self.cur_laser_length
        return (
         end_pos, reach_end)

    def on_create_laser_sfx_callback(self, sfx):
        self.laser_sfx = sfx
        if self.laser_end_pos:
            sfx.end_pos = self.laser_end_pos

    def on_create_laser_end_sfx_callback(self, sfx):
        self.laser_end_sfx = sfx
        if self.laser_end_pos:
            sfx.position = self.laser_end_pos

    def on_remove_laser_end_sfx_callback(self, sfx):
        self.laser_end_sfx_id = None
        self.laser_end_sfx = None
        return

    def tick(self, dt):
        self.tick_func(dt)

    def avatar_tick(self, dt):
        if not self.can_fire:
            if self.can_continue and self.ev_g_status_try_trans(ST_SHOOT):
                self.continue_auto_fire()
            if not self.can_fire:
                return
        wp = self.weapon
        if wp.dirty:
            return
        else:
            if self.is_avatar and not self.is_agent and wp.get_bullet_num() < wp.get_cost_ratio():
                self.unit_obj.send_event('E_ATTACK_END')
                self.send_event('E_TRY_RELOAD')
                return
            wp_model = self.sd.ref_hand_weapon_model
            if self.is_agent:
                weapon_pos = wp.get_pos() if 1 else None
                if wp_model:
                    start_pos = wp_model.get_socket_matrix('kaihuo', world.SPACE_TYPE_WORLD).translation
                    camera = global_data.game_mgr.scene.active_camera
                    cam_pos = camera.position
                    mat = camera.rotation_matrix
                    forward = mat.forward
                    up = mat.up
                    right = mat.right
                    if dt:
                        self._update_aim_offset(dt)
                    if self.cur_yaw_offset:
                        yaw_rotation = math3d.rotation(0, 0, 0, 1)
                        yaw_rotation.set_axis_angle(up, self.cur_yaw_offset)
                        forward = yaw_rotation.rotate_vector(forward)
                        right = yaw_rotation.rotate_vector(right)
                    if self.cur_pitch_offset:
                        pitch_rotation = math3d.rotation(0, 0, 0, 1)
                        pitch_rotation.set_axis_angle(right, self.cur_pitch_offset)
                        forward = pitch_rotation.rotate_vector(forward)
                    if self.is_agent:
                        attack_pos = self.ev_g_attack_pos()
                        if not attack_pos or isnan(attack_pos.x) or isnan(attack_pos.y) or isnan(attack_pos.z):
                            return
                        cam_pos = start_pos
                        forward = attack_pos - cam_pos
                        forward.normalize()
                        if not forward or isnan(forward.x) or isnan(forward.y) or isnan(forward.z):
                            return
                    end_pos = get_fire_end(self.camp_id, cam_pos, cam_pos + forward * self.max_laser_length, self.ev_g_position(), start_pos, forward, directly_use_start_pos=True)
                    end_pos, reach_end = self._update_laser_end_pos(dt, start_pos, end_pos)
                    self.laser_end_pos = end_pos
                    lst_pos = v3d_to_tp(start_pos)
                    cur_time = global_data.game_time
                    if cur_time - self.last_cost_bullet_time > self.cost_bullet_interval:
                        wp.cost_bullet(1)
                        t_use = self.weapon.get_fire_use_time()
                        self.send_event('E_WEAPON_DATA_CHANGED', wp.get_pos())
                        self.send_event('E_CUR_BULLET_NUM_CHG', wp.get_pos())
                        if self.last_cost_bullet_time == 0:
                            self.last_cost_bullet_time = cur_time
                        else:
                            self.last_cost_bullet_time = self.last_cost_bullet_time + self.cost_bullet_interval
                        args = (
                         lst_pos, v3d_to_tp(end_pos), None, 0, {}, {}, 0, None, weapon_pos, t_use)
                        self.send_event('E_CALL_SYNC_METHOD', 'do_shoot', args, True)
                    if cur_time - self.last_sync_time > SYNC_INTERVAL:
                        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_UPDATE_VICE_EFFECT, (v3d_to_tp(end_pos),)], True)
                        self.last_sync_time = cur_time
                    if not self.laser_start_sfx_id:
                        self.laser_start_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.cur_laser_start_sfx_path, wp_model, 'kaihuo')
                    self.laser_sfx_id = self.laser_sfx_id or global_data.sfx_mgr.create_sfx_on_model(self.cur_laser_sfx_path, wp_model, 'kaihuo', on_create_func=self.on_create_laser_sfx_callback)
                else:
                    if self.laser_sfx and self.laser_sfx.valid:
                        self.laser_sfx.end_pos = end_pos
                    if dt == 0:
                        return
                if reach_end:
                    if not self.laser_end_sfx_id:
                        self.laser_end_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.cur_laser_hit_sfx_path, on_create_func=self.on_create_laser_end_sfx_callback, on_remove_func=self.on_remove_laser_end_sfx_callback)
                    elif self.laser_end_sfx and self.laser_end_sfx.valid:
                        self.laser_end_sfx.position = self.laser_end_pos
                else:
                    if self.laser_end_sfx_id:
                        global_data.sfx_mgr.remove_sfx_by_id(self.laser_end_sfx_id)
                        self.laser_end_sfx_id = None
                        self.laser_end_sfx = None
                    if (end_pos - start_pos).is_zero:
                        return
                hit_target_list, hit_phantom, atk_range, pos, t_forward, up = get_hit_target(self.unit_obj.id, self.camp_id, start_pos, end_pos, sputtering_coe=0, radius=self.atk_radius)
                if hit_phantom:
                    for phantom in hit_phantom:
                        if phantom not in self.hit_phantom or cur_time - self.hit_phantom[phantom.id] >= self.cost_bullet_interval:
                            self.hit_phantom[phantom.id] = cur_time
                            do_hit_phantom(self, phantom)

                if hit_target_list:
                    target_dict = {}
                    for eid, _ in hit_target_list:
                        if eid not in self.last_hit_time_map:
                            self.last_hit_time_map[eid] = cur_time
                        elif cur_time - self.last_hit_time_map[eid] >= self.cost_bullet_interval:
                            if cur_time - self.last_hit_time_map[eid] > self.interval_threshold:
                                self.last_hit_time_map[eid] = cur_time
                            else:
                                self.last_hit_time_map[eid] += self.cost_bullet_interval
                        else:
                            continue
                        if eid not in target_dict:
                            target_dict[eid] = {}
                        target_dict[eid] = {'parts': {HIT_PART_BODY: 1}}

                    if target_dict:
                        ext_dict = {'hit_sfx_code': self.laser_hit_sfx_code}
                        hor_start_pos = math3d.vector(start_pos.x, 0, start_pos.z)
                        hor_end_pos = math3d.vector(end_pos.x, 0, end_pos.z)
                        hor_fire_forward = hor_end_pos - hor_start_pos
                        fire_forward = end_pos - start_pos
                        if hor_fire_forward.is_zero:
                            return
                        fire_forward.normalize()
                        hor_fire_forward.normalize()
                        cos_value = fire_forward.dot(hor_fire_forward)
                        for eid in target_dict:
                            entity = global_data.battle.get_entity(eid)
                            if not (entity and entity.logic):
                                continue
                            pos = entity.logic.ev_g_position()
                            hor_pos = math3d.vector(pos.x, 0, pos.z)
                            tmp_dir = hor_pos - hor_start_pos
                            if tmp_dir.is_zero:
                                continue
                            tmp_dist = tmp_dir.length
                            tmp_dir.normalize()
                            tmp_cos_value = hor_fire_forward.dot(tmp_dir)
                            hor_projection_forward_dist = tmp_dist * tmp_cos_value
                            real_dist = hor_projection_forward_dist / cos_value
                            target_forward = fire_forward * real_dist
                            target_pos = start_pos + target_forward
                            entity.logic.send_event('E_HIT_BLOOD_SFX', start_pos, target_pos, self.weapon_id, is_self=True, dmg_parts={}, triger_is_mecha=False, ext_dict=ext_dict)
                            entity.logic.send_event('E_HIT_SHIELD_SFX', start_pos, target_pos, self.weapon_id)
                            entity.logic.send_event('E_HIT_FIELD_SHIELD', start_pos, target_pos)
                            entity.logic.send_event('E_SHOW_PART_HIGHLIGHT', (HIT_PART_BODY,))
                            args = (
                             lst_pos, v3d_to_tp(target_pos), None, 0, {eid: target_dict[eid]}, {}, 0, ext_dict, weapon_pos, 0)
                            self.send_event('E_CALL_SYNC_METHOD', 'do_shoot', args, True)

            return

    def puppet_tick(self, dt):
        wp_model = self.sd.ref_hand_weapon_model
        if wp_model and self.laser_end_pos:
            cur_time = global_data.game_time
            if not self.laser_start_sfx_id:
                self.laser_start_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.cur_laser_start_sfx_path, wp_model, 'kaihuo')
            if not self.laser_sfx_id:
                self.laser_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.cur_laser_sfx_path, wp_model, 'kaihuo', on_create_func=self.on_create_laser_sfx_callback)
                self.laser_start_time = cur_time
            elif self.laser_sfx and self.laser_sfx.valid:
                self.laser_sfx.end_pos = self.laser_end_pos
            if cur_time - self.laser_start_time > LASER_END_APPEAR_TIME:
                if not self.laser_end_sfx_id:
                    self.laser_end_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.cur_laser_hit_sfx_path, on_create_func=self.on_create_laser_end_sfx_callback, on_remove_func=self.on_remove_laser_end_sfx_callback)
                elif self.laser_end_sfx and self.laser_end_sfx.valid:
                    self.laser_end_sfx.position = self.laser_end_pos

    def on_clear_sfx(self):
        if self.laser_start_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.laser_start_sfx_id)
            self.laser_start_sfx_id = None
        if self.laser_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.laser_sfx_id)
            self.laser_sfx_id = None
            self.laser_sfx = None
        if self.laser_end_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.laser_end_sfx_id)
            self.laser_end_sfx_id = None
            self.laser_end_sfx = None
        return

    def enter_right_aim(self):
        if not self.is_avatar or not self.can_fire:
            return
        PartCtrl.MAX_DELTA_VAL = self.right_aim_max_delta_value

    def quit_right_aim(self):
        if not self.is_avatar or not self.can_fire:
            return
        PartCtrl.MAX_DELTA_VAL = self.max_delta_value

    def sync_start_laser(self, end_pos_tuple):
        self._determine_laser_sfx_path()
        self.need_update = True
        self.laser_end_pos = math3d.vector(*end_pos_tuple)
        self.tick(0.01)

    def sync_update_laser(self, end_pos_tuple):
        if not self.need_update:
            self.sync_start_laser(end_pos_tuple)
        else:
            self.laser_end_pos = tp_to_v3d(end_pos_tuple)

    def sync_end_laser(self):
        self.need_update = False
        self.on_clear_sfx()

    def refresh_appearance(self, *args):
        if self.is_avatar and self.need_update:
            self.avatar_tick(0)