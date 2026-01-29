# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterEvadeMissileLogic.py
from __future__ import absolute_import
from math import pi
from .PVEMonsterEvadeLogic import MonsterEvadeBase
from common.cfg import confmgr
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gutils.weapon_utils import recheck_pve_launcher_dir
import world
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN

class MonsterEvadeMissileBase(MonsterEvadeBase):

    def init_params(self):
        super(MonsterEvadeMissileBase, self).init_params()
        self.fire_idx = 0
        self.sub_idx = 0

    def start_pre(self):
        super(MonsterEvadeMissileBase, self).start_pre()
        self.fire_idx = 0
        self.sub_idx = 0
        for fire_ts in self.fire_ts_seq:
            self.delay_call(fire_ts, self.prepare_fire)

    def prepare_fire(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        start_pos = model.get_socket_matrix(self.fire_socket, world.SPACE_TYPE_WORLD).translation
        direction = self.ev_g_forward()
        direction.y = 0
        direction.normalize()
        self.sub_idx = 0
        for i in range(0, self.wp_pellets):
            self.open_fire(start_pos, direction)

        self.fire_idx += 1

    def open_fire(self, start_pos, direction):
        fix_dir = recheck_pve_launcher_dir(self.wp_cus_param, direction, self.fire_idx)
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
               'wp_pos': 1,
               'aim_pos': (
                         self.target_pos.x, self.target_pos.y, self.target_pos.z)
               })
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.sub_idx += 1

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class MonsterEvadeMissile(MonsterEvadeMissileBase):

    def init_params(self):
        super(MonsterEvadeMissile, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9011355)
        self.evd_speed = self.custom_param.get('evd_speed', 800)
        self.max_evd_time = self.custom_param.get('max_evd_time', 0.5)
        self.gravity = self.custom_param.get('gravity', 1000)
        self.pre_anim = self.custom_param.get('pre_anim', 'jump_02')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0.667)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 2.0)
        self.evd_anim = self.custom_param.get('evd_anim', 'jump_04')
        self.evd_anim_rate = self.custom_param.get('evd_anim_rate', 1.0)
        self.land_anim = self.custom_param.get('land_anim', None)
        self.land_anim_dur = self.custom_param.get('land_anim_dur', 0)
        self.land_anim_rate = self.custom_param.get('land_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', 'jump_05')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.9)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.turn_start_ts = self.custom_param.get('turn_start_ts', 0.5)
        self.turn_speed = self.custom_param.get('turn_speed', 3 * pi)
        self.fire_ts_seq = self.custom_param.get('fire_ts_seq', [])
        self.fire_socket = self.custom_param.get('fire_socket', 'fx_vice_kaihuo')
        self.wp_type = self.custom_param.get('wp_type', None)
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_pellets = self.wp_conf.get('iPellets')
        self.wp_kind = self.wp_conf.get('iKind')
        self.main_angle = self.custom_param.get('main_angle')
        self.offset_angle = self.custom_param.get('offset_angle')
        self.spin_seq = self.custom_param.get('spin_seq')
        self.wp_cus_param = {'main_angle': self.main_angle,'offset_angle': self.offset_angle,'spin_seq': self.spin_seq}
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_evade_callbacks()