# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8004.py
from __future__ import absolute_import
from .BoostLogic import OxRushNew
from common.cfg import confmgr
import logic.gcommon.const as g_const
import common.utils.timer as timer
import world
from data import camera_state_const
import math3d
from math import pi
from .ShootLogic import WeaponFire

class OxRush8004(OxRushNew):
    BIND_EVENT = {'E_RUSH_HIT_TARGET': 'on_hit_target',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_ENABLE_ALL_DIR_DASH_DMG': 'on_enable_all_dir_dash_dmg',
       'G_ENABLE_ALL_DIR_DASH_DMG': 'get_enable_all_dir_dash_dmg'
       }
    BIND_ATTR_CHANGE = {'8004_rush_extra_duration_factor': 'on_rush_duration_changed'
       }

    def read_data_from_custom_param(self):
        super(OxRush8004, self).read_data_from_custom_param()
        self.all_dir_dash_dmg = False
        if global_data.game_mode.is_pve():
            mecha_id = self.ev_g_mecha_id()
            if mecha_id == 8004:
                self.max_rush_duration = confmgr.get('mecha_init_data', default={}).get('8004', {}).get('pve_diff_param', {}).get('pve_rush_max_duration', 1.2)

    def on_rush_duration_changed(self, attr, item_id, pre_value, cur_value, source_info):
        self.max_rush_duration = self.init_max_rush_duration * (1 + self.ev_g_add_attr('8004_rush_extra_duration_factor'))
        self.reset_sub_state_callback(self.STATE_RUSH)
        self.register_substate_callback(self.STATE_RUSH, 0.0, self.on_begin_rush)
        self.register_substate_callback(self.STATE_RUSH, self.max_rush_duration, self.on_end_rush)

    def on_hit_target(self, target):
        if self.sub_state != self.STATE_RUSH:
            return
        else:
            if self.target_hitted:
                return
            super(OxRushNew, self).sound_custom_end()
            if target and target.MASK & self.RUSH_DAMAGE_TARGET_TAG_VALUE:
                from logic.gcommon.skill.client.SkillOxRush import STAGE_DMG
                self.send_event('E_DO_SKILL', self.hit_skill_id, [target.id], self.ev_g_position(), None, STAGE_DMG)
                return
            self.target_hitted = target
            self.send_event('E_FORBID_ROTATION', False)
            self.send_event('E_RESET_ROTATION')
            self.send_event('E_CLEAR_SPEED')
            self.send_event('E_VERTICAL_SPEED', 0)
            if self.IS_AUTO_OX_RUSH_COL_CHECK:
                self.send_event('E_OX_END_RUSH')
            self.sub_state = self.STATE_HIT
            if not self.ev_g_is_agent():
                global_data.player.logic.send_event('E_MECHA_CAMERA', camera_state_const.MECHA_MODE_FOUR)
                global_data.emgr.enable_camera_yaw.emit(False)
            scn = world.get_active_scene()
            camera = scn.active_camera
            fire_forward = camera.rotation_matrix.forward
            if self.all_dir_dash_dmg:
                fire_position = self.ev_g_position()
                if self.is_hit_play_skill:
                    self.send_event('E_DO_SKILL', self.attack_skill_id, 0, fire_position, fire_forward)
                pos = (
                 fire_position.x, fire_position.y, fire_position.z)
                camera_yaw = camera.world_rotation_matrix.yaw
                for i in range(3):
                    r = camera_yaw + (1 + i) * pi * 0.5
                    rot_matrix = math3d.matrix.make_rotation_y(r)
                    rotation = math3d.matrix_to_rotation(rot_matrix)
                    rot = (rotation.x, rotation.y, rotation.z, rotation.w)
                    self.send_event('E_CREATE_ALL_DIR_DASH_DMG_EFFECT', pos, rot)

            else:
                fire_position = camera.position
                if self.is_hit_play_skill:
                    self.send_event('E_DO_SKILL', self.attack_skill_id, 0, fire_position, fire_forward)
            return

    def enter(self, leave_states):
        super(OxRushNew, self).enter(leave_states)
        self.init_parameters()
        self.air_walk_direction_setter.reset()
        self.start_rush()
        if global_data.game_mode.is_pve():
            ex_sec_skill_cast_time = self.ev_g_add_attr('8004_dash_ex_sec_skill_time')
            if ex_sec_skill_cast_time > 0:
                self.on_ex_sec_skill()

    def on_ex_sec_skill(self):
        scn = world.get_active_scene()
        camera = scn.active_camera
        fire_forward = camera.rotation_matrix.forward
        fire_position = self.ev_g_position()
        pos = (fire_position.x, fire_position.y, fire_position.z)
        camera_yaw = camera.world_rotation_matrix.yaw
        if self.all_dir_dash_dmg:
            for i in range(4):
                r = camera_yaw + i * pi * 0.5
                rot_matrix = math3d.matrix.make_rotation_y(r)
                rotation = math3d.matrix_to_rotation(rot_matrix)
                rot = (rotation.x, rotation.y, rotation.z, rotation.w)
                self.send_event('E_CREATE_ALL_DIR_DASH_DMG_EFFECT', pos, rot)

        else:
            r = camera_yaw
            rot_matrix = math3d.matrix.make_rotation_y(r)
            rotation = math3d.matrix_to_rotation(rot_matrix)
            rot = (rotation.x, rotation.y, rotation.z, rotation.w)
            self.send_event('E_CREATE_ALL_DIR_DASH_DMG_EFFECT', pos, rot)
        self.send_event('E_DO_SKILL', self.attack_skill_id, 0, fire_position, fire_forward)

    def destroy(self):
        super(OxRush8004, self).destroy()

    def on_end_rush(self):
        super(OxRush8004, self).on_end_rush()

    def exit(self, enter_states):
        super(OxRush8004, self).exit(enter_states)
        self.send_event('E_CALL_SYNC_METHOD', 'exit_dash_8004', (), True)

    def on_enable_all_dir_dash_dmg(self, enable):
        self.all_dir_dash_dmg = enable

    def get_enable_all_dir_dash_dmg(self):
        return not self.all_dir_dash_dmg


class WeaponFire8004(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_BREAKTHROUGH_8004_TRACK_WP': 'on_enable_breakthrough_8004_track_wp',
       'E_ENHANCE_BREAKTHROUGH_8004_TRACK_WP': 'on_enhance_breakthrough_8004_track_wp'
       })
    TRACK_BULLETS_ANGLE = [
     (0.1, 10), (11.2, 5), (-11.2, 5), (11.2, -5), (-11.2, -5)]

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8004, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.breakthrough_8004_track_wp_pos = 0
        self.enhance_8004_track_wp = False

    def on_enable_breakthrough_8004_track_wp(self, wp_pos):
        self.breakthrough_8004_track_wp_pos = wp_pos

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        super(WeaponFire8004, self).on_fire(f_cdtime, weapon_pos, fired_socket_index=fired_socket_index)
        pos = self.enhance_8004_track_wp or self.breakthrough_8004_track_wp_pos if 1 else self.check_enhance_wp_pos()
        if pos and weapon_pos in (1, 2):
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, pos)
            self.send_event('E_SET_MULTIPLE_AIM_TARGET_MAX_COUNT', pos, 5, force_update=True)
            if len(self.sd.ref_aim_targets.get(pos, -1)) > 0:
                for index in range(len(self.sd.ref_aim_targets[pos])):
                    self.ev_g_try_weapon_attack_begin(pos, aim_target_index=index)
                    self.ev_g_try_weapon_attack_end(pos, weapon_state_info={'sub_idx': index})

            else:
                for index in range(5):
                    force_pitch = self.TRACK_BULLETS_ANGLE[index][0]
                    force_yaw = self.TRACK_BULLETS_ANGLE[index][1]
                    self.ev_g_try_weapon_attack_begin(pos, aim_target_index=-1)
                    self.ev_g_try_weapon_attack_end(pos, weapon_state_info={'forced_pitch': force_pitch,'forced_yaw': force_yaw})

            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, pos)

    def on_enhance_breakthrough_8004_track_wp(self):
        self.enhance_8004_track_wp = True

    def check_enhance_wp_pos(self):
        wp = self.ev_g_wpbar_get_by_pos(1)
        if wp:
            cur_bullet_num = wp.get_bullet_num()
            if cur_bullet_num <= 0:
                return 5
            return 4
        else:
            return 4