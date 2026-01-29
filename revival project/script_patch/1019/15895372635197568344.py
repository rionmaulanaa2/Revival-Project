# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterMultiRangeLogic.py
from __future__ import absolute_import
from six.moves import range
import world
import math3d
from logic.gutils.weapon_utils import recheck_pve_fire_dir
from common.utils.timer import CLOCK
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN, WP_TRACK_MISSILE, WP_SWORD_LIGHT
from common.cfg import confmgr
from logic.gutils.pve_utils import get_aim_pos
from .PVEMonsterRangeLogic import MonsterRangeBase
from math import radians

class MonsterMultiRangeBase(MonsterRangeBase):

    def init_params(self):
        super(MonsterMultiRangeBase, self).init_params()
        self.wp_type = 0
        self.fire_timer_dict = {}
        self.fire_seq_dict = {}
        self.sub_idx_dict = {}

    def init_fire(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            if self.sub_state != self.RANGE_ATK:
                return
            cur_fire_seq = self.multi_fire_seq[self.fire_idx]
            for fire_socket in cur_fire_seq:
                mat = model.get_socket_matrix(fire_socket, world.SPACE_TYPE_WORLD)
                start_pos = mat.translation
                target_pos = get_aim_pos(self.target_id, self.target_pos)
                direction = target_pos - start_pos
                direction.normalize()
                self.prepare_fire_multi(start_pos, direction, fire_socket)

            self.fire_delay_id = None
            return

    def prepare_fire_multi(self, start_pos, direction, fire_socket):
        wp_type = self.wp_list[self.socket_list.index(fire_socket)]
        wp_conf = confmgr.get('firearm_config', str(wp_type))
        wp_pellets = wp_conf.get('iPellets')
        wp_kind = wp_conf.get('iKind')
        wp_cus_param = wp_conf.get('cCustomParam', {})
        if type(wp_pellets) == dict:
            self.reset_fire_timer_multi(fire_socket)
            self.fire_seq_dict[fire_socket] = 0
            self.sub_idx_dict[fire_socket] = 0
            self.fire_timer_dict[fire_socket] = global_data.game_mgr.register_logic_timer(lambda s_p=start_pos, d=direction, w_p=wp_pellets, f_s=fire_socket, w_t=wp_type, w_k=wp_kind, w_c_p=wp_cus_param: self.open_fire_seq_multi(s_p, d, w_p, f_s, w_t, w_k, w_c_p), wp_pellets['cd'], None, len(wp_pellets['bullets']), CLOCK)
        else:
            self.sub_idx_dict[fire_socket] = 0
            for i in range(0, wp_pellets):
                self.open_fire_multi(start_pos, direction, fire_socket, wp_type, wp_kind, wp_cus_param)

        return

    def open_fire_seq_multi(self, start_pos, direction, wp_pellets, fire_socket, wp_type, wp_kind, wp_cus_param):
        count = wp_pellets['bullets'][self.fire_seq_dict[fire_socket]]
        for i in range(0, count):
            self.open_fire_multi(start_pos, direction, fire_socket, wp_type, wp_kind, wp_cus_param)

        self.fire_seq_dict[fire_socket] += 1

    def open_fire_multi(self, start_pos, direction, fire_socket, wp_type, wp_kind, wp_cus_param):
        if not self or not self.is_valid():
            return
        else:
            sub_idx = self.sub_idx_dict[fire_socket]
            owner = self.unit_obj.get_owner()
            fix_dir = recheck_pve_fire_dir(wp_cus_param, direction, sub_idx, owner.get_monster_id(), owner.get_pve_monster_level(), self.wp_type)
            throw_item = {'uniq_key': self.get_uniq_key(),
               'item_itype': wp_type,
               'item_kind': wp_kind,
               'position': (
                          start_pos.x, start_pos.y, start_pos.z),
               'dir': (
                     fix_dir.x, fix_dir.y, fix_dir.z),
               'sub_idx': sub_idx
               }
            if wp_kind == WP_NAVIGATE_GUN:
                throw_item.update({'aim_target': self.target_id,
                   'm_position': (
                                start_pos.x, start_pos.y, start_pos.z),
                   'wp_pos': 1,
                   'aim_pos': (
                             self.target_pos.x, self.target_pos.y, self.target_pos.z)
                   })
            elif wp_kind == WP_SWORD_LIGHT:
                throw_item.update({'col_width': wp_cus_param.get('energy_width', 9)
                   })
                roll_angle = wp_cus_param.get('roll_angle', None)
                if roll_angle:
                    rad = radians(roll_angle)
                    rot_mat = math3d.matrix.make_rotation(math3d.vector(0, 0, 1), rad)
                    ret = math3d.vector(0, 1, 0) * rot_mat
                    up = (ret.x, ret.y, ret.z)
                    throw_item.update({'up': up
                       })
            self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
            self.sub_idx_dict[fire_socket] += 1
            return

    def reset_fire_timer_multi(self, fire_socket):
        fire_timer = self.fire_timer_dict.get(fire_socket, None)
        if fire_timer:
            global_data.game_mgr.unregister_logic_timer(fire_timer)
        self.fire_timer_dict[fire_socket] = None
        return

    def reset_fire_timer_multi_all(self):
        for t in self.fire_timer_dict:
            timer = self.fire_timer_dict[t]
            if timer:
                global_data.game_mgr.unregister_logic_timer(timer)

        self.fire_timer_dict = {}

    def exit(self, enter_states):
        self.reset_fire_timer_multi_all()
        super(MonsterMultiRangeBase, self).exit(enter_states)

    def destroy(self):
        self.reset_fire_timer_multi_all()
        super(MonsterMultiRangeBase, self).destroy()


class MonsterMultiRange(MonsterMultiRangeBase):

    def init_params(self):
        super(MonsterMultiRange, self).init_params()
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.socket_list = self.custom_param.get('socket_list', [])
        self.wp_list = self.custom_param.get('wp_list', [])
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
        self.multi_fire_seq = self.custom_param.get('multi_fire_seq', [[]])
        self.fire_delay = self.custom_param.get('fire_delay', 0)
        self.move_start_ts = self.custom_param.get('move_start_ts', 0)
        self.move_end_ts = self.custom_param.get('move_end_ts', 0)
        self.move_anim = self.custom_param.get('move_anim', '')
        self.move_anim_rate = self.custom_param.get('move_anim_rate', 1.0)
        self.move_speed = self.custom_param.get('move_speed', 0)
        self.stand_anim = self.custom_param.get('stand_anim', '')
        self.stand_anim_rate = self.custom_param.get('stand_anim_rate', 1.0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_range_callbacks()