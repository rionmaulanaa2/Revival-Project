# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterTossLogic.py
from __future__ import absolute_import
from .PVEMonsterRangeLogic import MonsterRangeBase
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN
from logic.gutils.weapon_utils import recheck_pve_toss_dir
from common.cfg import confmgr
from logic.gutils.pve_utils import get_aim_pos
from logic.gcommon.const import NEOX_UNIT_SCALE

class MonsterTossBase(MonsterRangeBase):

    def open_fire(self, start_pos, direction):
        diff = get_aim_pos(self.target_id, self.target_pos) - self.ev_g_position()
        diff.y = 0
        dis = diff.length / NEOX_UNIT_SCALE
        fix_dir = recheck_pve_toss_dir(self.wp_cus_param, direction, dis, self.sub_idx)
        if not self or not self.is_valid():
            return
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
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.sub_idx += 1


class MonsterToss(MonsterTossBase):

    def init_params(self):
        super(MonsterToss, self).init_params()
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.wp_list = self.custom_param.get('wp_list', (808012, ))
        self.wp_pos = self.custom_param.get('wp_pos', 1)
        self.wp_type = self.wp_list[self.wp_pos - 1]
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_pellets = self.wp_conf.get('iPellets')
        self.wp_kind = self.wp_conf.get('iKind')
        self.yaw_seq = self.custom_param.get('yaw_seq')
        self.max_angle = self.custom_param.get('max_angle')
        self.min_angle = self.custom_param.get('min_angle')
        self.max_dis = self.custom_param.get('max_dis')
        self.wp_cus_param = {'yaw_seq': self.yaw_seq,'max_angle': self.max_angle,'min_angle': self.min_angle,'max_dis': self.max_dis}
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
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_range_callbacks()