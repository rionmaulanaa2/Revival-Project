# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterLauncherLogic.py
from __future__ import absolute_import
from .PVEMonsterRangeLogic import MonsterRangeBase
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN, WP_SWORD_LIGHT
from logic.gutils.weapon_utils import recheck_pve_launcher_dir
from common.cfg import confmgr
from math import radians
import math3d

class MonsterLauncherBase(MonsterRangeBase):

    def check_wp(self):
        super(MonsterLauncherBase, self).check_wp()
        self.wp_cus_param.update({'main_angle': self.main_angle,'offset_angle': self.offset_angle,'spin_seq': self.spin_seq})

    def init_params(self):
        super(MonsterLauncherBase, self).init_params()
        self.end_aoe_skill_id_list = self.custom_param.get('end_aoe_skill_id_list', [])
        self.end_aoe_skill_id_2_list = self.custom_param.get('end_aoe_skill_id_2_list', [])

    def open_fire(self, start_pos, direction):
        fix_dir = recheck_pve_launcher_dir(self.wp_cus_param, direction, self.sub_idx)
        if not self or not self.is_valid():
            return
        else:
            throw_item = {'uniq_key': self.get_uniq_key(),
               'item_itype': self.wp_type,
               'item_kind': self.wp_kind,
               'position': (
                          start_pos.x, start_pos.y, start_pos.z),
               'dir': (
                     fix_dir.x, fix_dir.y, fix_dir.z),
               'sub_idx': self.sub_idx
               }
            if self.wp_kind == WP_NAVIGATE_GUN:
                throw_item.update({'aim_target': self.target_id,
                   'm_position': (
                                start_pos.x, start_pos.y, start_pos.z),
                   'wp_pos': self.wp_pos,
                   'aim_pos': (
                             self.target_pos.x, self.target_pos.y, self.target_pos.z)
                   })
            elif self.wp_kind == WP_SWORD_LIGHT:
                throw_item.update({'col_width': self.wp_cus_param.get('energy_width', 9)
                   })
                roll_angle = self.wp_cus_param.get('roll_angle', None)
                if roll_angle:
                    rad = radians(roll_angle)
                    rot_mat = math3d.matrix.make_rotation(math3d.vector(0, 0, 1), rad)
                    ret = math3d.vector(0, 1, 0) * rot_mat
                    up = (ret.x, ret.y, ret.z)
                    throw_item.update({'up': up
                       })
            self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
            self.sub_idx += 1
            return

    def end_pre(self):
        super(MonsterLauncherBase, self).end_pre()
        if self.fire_idx < len(self.end_aoe_skill_id_list):
            end_aoe_skill_id = self.end_aoe_skill_id_list[self.fire_idx]
            self.send_event('E_DO_SKILL', end_aoe_skill_id)
        if self.fire_idx < len(self.end_aoe_skill_id_2_list):
            end_aoe_skill_id_2 = self.end_aoe_skill_id_2_list[self.fire_idx]
            self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (end_aoe_skill_id_2, self.post_data()), False, True)

    def post_data(self):
        if self.fire_idx < len(self.end_aoe_skill_socket_list):
            end_aoe_skill_socket = self.end_aoe_skill_socket_list[self.fire_idx]
        else:
            end_aoe_skill_socket = 'fx_root'
        model = self.ev_g_model()
        mat = model.get_socket_matrix(end_aoe_skill_socket, 1)
        pos = mat.translation
        data = ((pos.x, pos.y, pos.z),)
        return data


class MonsterLauncher(MonsterLauncherBase):

    def init_params(self):
        super(MonsterLauncher, self).init_params()
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.wp_list = self.custom_param.get('wp_list', (808012, ))
        self.wp_pos = self.custom_param.get('wp_pos', 1)
        self.wp_type = self.wp_list[self.wp_pos - 1]
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_pellets = self.wp_conf.get('iPellets')
        self.wp_kind = self.wp_conf.get('iKind')
        self.wp_cus_param = self.wp_conf.get('cCustomParam', {})
        self.main_angle = self.custom_param.get('main_angle')
        self.offset_angle = self.custom_param.get('offset_angle')
        self.spin_seq = self.custom_param.get('spin_seq')
        self.skill_id = self.custom_param.get('skill_id', 9010251)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.pre_anim_name_list = self.custom_param.get('pre_anim_name_list', ('', ))
        self.pre_anim_name = self.pre_anim_name_list[self.fire_idx]
        self.pre_anim_rate_list = self.custom_param.get('pre_anim_rate_list', (1.0, ))
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.pre_anim_dur_list = self.custom_param.get('pre_anim_dur_list', (0, ))
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.atk_anim_name_list = self.custom_param.get('atk_anim_name_list', ('attack01', ))
        self.atk_anim_name = self.atk_anim_name_list[self.fire_idx]
        self.atk_anim_rate_list = self.custom_param.get('atk_anim_rate_list', (1.0, ))
        self.atk_anim_rate = self.atk_anim_rate_list[self.fire_idx]
        self.atk_anim_dur_list = self.custom_param.get('atk_anim_dur_list', (1.0, ))
        self.atk_anim_dur = self.atk_anim_dur_list[self.fire_idx]
        self.bac_anim_name_list = self.custom_param.get('bac_anim_name_list', ('', ))
        self.bac_anim_name = self.bac_anim_name_list[self.fire_idx]
        self.bac_anim_rate_list = self.custom_param.get('bac_anim_rate_list', (1.0, ))
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.bac_anim_dur_list = self.custom_param.get('bac_anim_dur_list', (0, ))
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.fire_socket_list = self.custom_param.get('fire_socket_list', ('fx_kaihuo', ))
        self.fire_socket = self.fire_socket_list[self.fire_idx]
        self.fire_delay = self.custom_param.get('fire_delay', 0)
        self.move_start_ts = self.custom_param.get('move_start_ts', 0)
        self.move_end_ts = self.custom_param.get('move_end_ts', 0)
        self.move_anim = self.custom_param.get('move_anim', '')
        self.move_anim_rate = self.custom_param.get('move_anim_rate', 1.0)
        self.move_speed = self.custom_param.get('move_speed', 0)
        self.stand_anim = self.custom_param.get('stand_anim', '')
        self.stand_anim_rate = self.custom_param.get('stand_anim_rate', 1.0)
        self.end_aoe_skill_id_list = self.custom_param.get('end_aoe_skill_id_list', [])
        self.end_aoe_skill_id_2_list = self.custom_param.get('end_aoe_skill_id_2_list', [])
        self.end_aoe_skill_socket_list = self.custom_param.get('end_aoe_skill_socket_list', [])
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_range_callbacks()