# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8015.py
from __future__ import absolute_import
from logic.gcommon.cdata.mecha_status_config import *
from .ShootLogic import WeaponFire
from .BoostLogic import OxRushNew
from .StateBase import StateBase
from common.utils import timer
from common.utils.timer import CLOCK
import math3d
import world
import math
from logic.gutils import scene_utils
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_7
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.const as g_const
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils.mecha_utils import do_hit_phantom

class WeaponFire8015(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CHANGE_ENHANCE_WEAPON_FIRE_8015': '_on_change_enhance_weapon_fire'
       })
    ENHANCE_MAX_TIMES = 1

    def read_data_from_custom_param(self):
        super(WeaponFire8015, self).read_data_from_custom_param()
        self.is_play_anim_beforehand = self.custom_param.get('is_play_anim_beforehand', False)
        self.default_weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.enhance_weapon_pos = self.custom_param.get('enhance_weapon_pos', g_const.PART_WEAPON_POS_MAIN3)
        self.enhance_weapon_pos1 = self.custom_param.get('enhance_weapon_pos1', g_const.PART_WEAPON_POS_MAIN4)
        self.send_event('E_ADD_BIND_GUNS', 1, self.default_weapon_pos, self.enhance_weapon_pos1)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8015, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.continue_atk_timer = None
        self.enhance_weapon_times = 0
        self.is_switch = False
        return

    def _on_change_enhance_weapon_fire(self, is_switch):
        self.do_on_change_enhance_weapon_fire(is_switch)

    def do_on_change_enhance_weapon_fire(self, is_switch):
        if self.is_switch == is_switch:
            return
        self.is_switch = is_switch
        self.enhance_weapon_times = 0
        if is_switch:
            self.weapon_pos = self.enhance_weapon_pos
            sub_weapon_pos = self.enhance_weapon_pos1
        else:
            self.weapon_pos = self.default_weapon_pos
            sub_weapon_pos = self.default_weapon_pos
        self.send_event('E_SWITCH_BIND_WEAPON', 0, self.weapon_pos)
        self.send_event('E_SWITCH_BIND_WEAPON', 1, sub_weapon_pos, is_sync=sub_weapon_pos == self.enhance_weapon_pos1)

    def try_weapon_attack_begin(self):
        enable = self.ev_g_try_bind_weapon_attack_begin(0)
        if self.enhance_weapon_pos == self.weapon_pos:
            self.ev_g_try_bind_weapon_attack_begin(1)
        return enable

    def try_weapon_attack_end(self, is_cancel=False):
        enable = self.ev_g_try_bind_weapon_attack_end(0)
        if self.enhance_weapon_pos == self.weapon_pos:
            self.ev_g_try_bind_weapon_attack_end(1)
        return enable

    def release_continue_atk_timer(self):
        if self.continue_atk_timer:
            global_data.game_mgr.unregister_logic_timer(self.continue_atk_timer)
            self.continue_atk_timer = None
        return

    def action_btn_up(self):
        self.release_continue_atk_timer()
        return super(WeaponFire8015, self).action_btn_up()

    def can_fire_attack(self):
        self.try_play_anim_beforehand()

    def can_not_fire_attack(self):
        self.release_continue_atk_timer()

    def try_play_anim_beforehand(self):
        if self.is_play_anim_beforehand:
            self.release_continue_atk_timer()
            fire_cd = self.ev_g_weapon_fire_cd(self.weapon_pos)
            if fire_cd:

                def fire():
                    self.play_fire_anim(self.ev_g_socket_index(self.weapon_pos))

                self.continue_atk_timer = global_data.game_mgr.register_logic_timer(fire, interval=fire_cd, times=-1, mode=CLOCK)
                fire()

    def try_play_fire_anim(self, fired_socket_index):
        self.enhance_weapon_times += 1
        if self.weapon_pos == self.enhance_weapon_pos and self.enhance_weapon_times >= self.ENHANCE_MAX_TIMES:
            self.send_event('E_CHANGE_ENHANCE_WEAPON_FIRE_8015', False)
        if not self.is_play_anim_beforehand:
            self.play_fire_anim(fired_socket_index)

    def refresh_action_param(self, action_param, custom_param):
        self.release_continue_atk_timer()
        super(WeaponFire8015, self).refresh_action_param(action_param, custom_param)

    def destroy(self):
        self.release_continue_atk_timer()
        super(WeaponFire8015, self).destroy()

    def exit(self, enter_states):
        self.release_continue_atk_timer()
        super(WeaponFire8015, self).exit(enter_states)


class OxRushNew8015(OxRushNew):
    BIND_EVENT = {'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start'
       }
    IS_AUTO_OX_RUSH_COL_CHECK = False
    CAN_CANCEL_RUSH = False

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OxRushNew8015, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.is_hit_play_skill = False
        self.hit_mecha_id = set()
        self.check_hit_timer = None
        self._dash_dis = 0
        self._old_pos = None
        self.is_enhanced_1 = False
        self.is_enhanced_2 = False
        self.enable_param_changed_by_buff()
        self.hit_phantom = []
        return

    def refresh_param_changed(self):
        self.check_col_info = self.enhanced_col_info if self.is_enhanced_2 else self.col_info

    def destroy(self):
        self.clear_check_hit_timer()
        super(OxRushNew8015, self).destroy()

    def read_data_from_custom_param(self):
        self.range_pitch_angle = self.custom_param.get('range_pitch_angle', [-60, -30])
        self.range_pitch_speed_ratio = self.custom_param.get('range_pitch_speed_ratio', [1.0, 0.3])
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.col_info = self.custom_param.get('col_info', (30, 50))
        self.enhanced_col_info = self.custom_param.get('enhanced_col_info', (30, 50))
        self.check_col_info = self.col_info
        super(OxRushNew8015, self).read_data_from_custom_param()
        min_angle, max_angle = self.range_pitch_angle
        min_ratio, max_ratio = self.range_pitch_speed_ratio
        self.one_angle_ratio = (max_ratio - min_ratio) / (max_angle - min_angle)

    def action_btn_down(self):
        return StateBase.action_btn_down(self)

    def action_btn_up(self):
        super(OxRushNew8015, self).action_btn_up()
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        self.sound_custom_start()

    def enter(self, leave_states):
        super(OxRushNew8015, self).enter(leave_states)
        self.send_event('E_DO_OXRUSH_8015', True)
        self.hit_phantom = []
        self.start_check_hit()
        self._start_cal_dash_dist()

    def exit(self, enter_states):
        super(OxRushNew8015, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_8015', False)
        self.stop_check_hit()
        self._finish_cal_dash_dist()

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8015', MECHA_MEMORY_LEVEL_7, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def update(self, dt):
        StateBase.update(self, dt)
        if self.is_accelerating:
            self.cur_speed += self.acc_speed * dt
            if self.cur_speed > self.max_rush_speed:
                self.cur_speed = self.max_rush_speed
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.is_moving:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            if self.ev_g_is_agent():
                cam_forward = self.ev_g_forward()
                cam_pitch = self.ev_g_cam_pitch()
                if not cam_forward.y:
                    up = math3d.vector(0, 1, 0)
                    right = cam_forward.cross(up) * -1
                    right.normalize()
                    mat = math3d.matrix.make_rotation(right, -cam_pitch)
                    cam_forward = cam_forward * mat
            else:
                cam_forward = scn.active_camera.rotation_matrix.forward
                cam_pitch = scn.active_camera.rotation_matrix.pitch
            angle = math.degrees(cam_pitch)
            min_angle, max_angle = self.range_pitch_angle
            min_ratio, max_ratio = self.range_pitch_speed_ratio
            if angle > min_angle and angle < max_angle:
                cur_ratio = (angle - min_angle) * self.one_angle_ratio + min_ratio
            elif angle <= min_angle:
                cur_ratio = min_ratio
            else:
                cur_ratio = max_ratio
            walk_direction = self.get_walk_direction(cam_forward, cur_ratio)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)

    def get_hit_unit_id_list(self):
        height, radius = self.check_col_info
        if global_data.player and global_data.player.logic:
            pos = self.ev_g_position() + math3d.vector(0, height, 0)
            if self.is_draw_col:
                global_data.emgr.scene_draw_wireframe_event.emit(pos, math3d.matrix(), 10, length=(radius * 2, radius * 2, radius * 2))
            unit_datas = global_data.emgr.scene_get_hit_enemy_mecha_unit.emit(self.unit_obj, pos, radius)
            hit_unit_id_list = []
            if unit_datas and unit_datas[0]:
                for unit in unit_datas[0]:
                    unit_id = unit.id
                    if unit_id not in self.hit_mecha_id:
                        if scene_utils.dash_filtrate_hit(self.unit_obj, unit):
                            continue
                        self.hit_mecha_id.add(unit_id)
                        hit_unit_id_list.append(unit_id)

            hit_phantom = global_data.emgr.scene_get_hit_all_phantom_unit.emit(pos, radius)
            if hit_phantom:
                for phantom_list in hit_phantom:
                    for phantom in phantom_list:
                        if phantom not in self.hit_phantom:
                            do_hit_phantom(self, phantom)
                            self.hit_phantom.append(phantom)

                return hit_unit_id_list

    def start_check_hit(self):
        self.clear_check_hit_timer()
        self.check_hit_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_hit, mode=timer.CLOCK, interval=0.1)

    def _check_hit(self):
        hit_unit_id_list = self.get_hit_unit_id_list()
        if hit_unit_id_list:
            self.send_skill_hit(hit_unit_id_list)

    def send_skill_hit(self, info):
        self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, info), False, True)
        if self.is_enhanced_2:
            self.send_event('E_OXRUSH_8015_LOCK_TARGET', info)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_OXRUSH_8015_LOCK_TARGET, (info,)])

    def clear_check_hit_timer(self):
        self.check_hit_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
        self.check_hit_timer = None
        return

    def stop_check_hit(self):
        self.clear_check_hit_timer()
        self.hit_mecha_id = set()

    def on_cam_rotate(self, *args):
        if self.is_active and self.is_moving and not self.ev_g_is_agent():
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            cam_pitch = scn.active_camera.rotation_matrix.pitch
            angle = abs(math.degrees(cam_pitch))
            min_angle, max_angle = self.range_pitch_angle
            min_ratio, max_ratio = self.range_pitch_speed_ratio
            if angle > min_angle and angle < max_angle:
                cur_ratio = (angle - min_angle) * self.one_angle_ratio + min_ratio
            elif angle <= min_angle:
                cur_ratio = min_ratio
            else:
                cur_ratio = max_ratio
            walk_direction = cam_forward * (self.cur_speed * cur_ratio)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)