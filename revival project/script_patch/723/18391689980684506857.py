# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossDashRocketLogic.py
from __future__ import absolute_import
from six.moves import range
from .BoostLogic import OxRushNew
from .PVEMonsterDashAtkLogic import MonsterDashAtkBase
import math3d
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
from logic.gutils.weapon_utils import recheck_pve_launcher_dir
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gcommon.behavior.StateBase import StateBase
from logic.gutils.pve_utils import get_aim_pos

class BossDashRocketBase(MonsterDashAtkBase):
    BIND_EVENT = OxRushNew.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       })
    econf = {}

    def init_parameters(self):
        super(BossDashRocketBase, self).init_parameters()
        self.fire_idx = 0
        self.sub_idx = 0

    def on_begin_pre(self):
        super(BossDashRocketBase, self).on_begin_pre()
        self.fire_idx = 0
        self.sub_idx = 0
        self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        if self.begin_aoe_skill_id_2_delay:
            self.delay_call(self.begin_aoe_skill_id_2_delay, self.release_shockwave)

    def on_begin_rush(self):
        super(MonsterDashAtkBase, self).on_begin_rush()
        self.start_check_hit()
        self.send_event('E_FORWARD', self.rush_direction, True)
        if self.begin_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.begin_aoe_skill_id)

    def release_shockwave(self):
        if self.begin_aoe_skill_id_2:
            self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.begin_aoe_skill_id_2, self.post_data()), False, True)

    def post_data(self):
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.begin_aoe_skill_socket, 1)
        pos = mat.translation
        data = ((pos.x, pos.y, pos.z),)
        return data

    def update(self, dt):
        StateBase.update(self, dt)
        if self.is_accelerating:
            pass
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.rush_direction is not None and self.is_moving:
            walk_direction = self.get_walk_direction(self.rush_direction)
            self.air_walk_direction_setter.execute(walk_direction)
        if self.sub_state == self.STATE_RUSH:
            if self.fire_idx < len(self.fire_ts_seq) and self.elapsed_time > self.fire_ts_seq[self.fire_idx]:
                self.prepare_fire()
        pos = self.ev_g_position()
        dis = (pos - self.center_pos).length
        if dis > self.dash_radius * NEOX_UNIT_SCALE and self.elapsed_time > self.min_valid_ts:
            self.sub_state = self.STATE_MISS
        return

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
        fix_dir = recheck_pve_launcher_dir(self.wp_cus_param, direction, self.sub_idx)
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
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.sub_idx += 1

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class BossDashRocket(BossDashRocketBase):

    def read_data_from_custom_param(self):
        super(BossDashRocket, self).read_data_from_custom_param()
        self.max_rush_duration = self.custom_param.get('max_rush_duration', 3.0)
        self.max_rush_speed = self.custom_param.get('max_rush_speed', 180)
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 3.0)
        self.pre_anim = self.custom_param.get('pre_anim', 'attack_04')
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 1.0)
        self.start_acc_time = self.custom_param.get('start_acc_time', self.pre_anim_duration)
        self.rush_anim = self.custom_param.get('rush_anim', 'run')
        self.rush_anim_rate = self.custom_param.get('rush_anim_rate', 2.0)
        self.miss_anim = self.custom_param.get('miss_anim', 'hit')
        self.miss_anim_rate = self.custom_param.get('miss_anim_rate', 1.0)
        self.miss_anim_duration = self.custom_param.get('miss_anim_duration', 1.0)
        self.end_brake_time = self.custom_param.get('end_brake_time', 0.1)
        self.air_dash_end_speed = self.custom_param.get('air_dash_end_speed', 30)
        self.skill_id = self.custom_param.get('skill_id', 9010153)
        self.tick_interval = self.custom_param.get('tick_interval', 0.03)
        self.is_draw_col = self.custom_param.get('is_draw_col', True)
        self.col_info = self.custom_param.get('col_info', (30, 100))
        self.begin_aoe_skill_id = self.custom_param.get('begin_aoe_skill_id', None)
        self.begin_aoe_skill_id_2 = self.custom_param.get('begin_aoe_skill_id_2', None)
        self.begin_aoe_skill_id_2_delay = self.custom_param.get('begin_aoe_skill_id_2_delay', 0)
        self.begin_aoe_skill_socket = self.custom_param.get('begin_aoe_skill_socket', 'fx_root')
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.calc_dir_stage = self.STAGE_ENTER
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
        self.center_point = self.custom_param.get('center_point', (0, 0, 0))
        self.center_pos = math3d.vector(*self.center_point)
        self.dash_radius = self.custom_param.get('dash_radius', 50)
        self.min_valid_ts = self.custom_param.get('min_valid_ts', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.read_data_from_custom_param()
            self.reset_sub_states_callback()
            self._register_sub_state_callbacks()