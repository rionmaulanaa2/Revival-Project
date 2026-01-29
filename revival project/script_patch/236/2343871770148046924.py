# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterPounceBombLogic.py
from __future__ import absolute_import
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_POUNCE_WARN_SFX, E_PVE_BOSS_BOMB_WARN_SFX
from .PVEMonsterPounceLogic import MonsterPounceBase
from random import uniform
from math import pi, cos, sin
from logic.gcommon.common_const.idx_const import ExploderID
from common.cfg import confmgr

class MonsterPounceBombBase(MonsterPounceBase):
    BIND_EVENT = MonsterPounceBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PVE_BOSS_BOMB_WARN_SFX': 'create_bomb_warn_sfx'
       })
    R_COUNT = 3

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.focus_pos = None
        self.focus_tag = False
        self.use_bias = False
        self.bias_dur = 0
        self.dash_time = 0
        self.fire_ts = 0
        self.fire_idx = 0
        self.sub_idx = 0
        self.fire_timer = None
        self.bomb_pos = []
        return

    def start_dash_pre(self):
        super(MonsterPounceBombBase, self).start_dash_pre()

    def end_dash_pre(self):
        super(MonsterPounceBombBase, self).end_dash_pre()

    def start_dash(self):
        super(MonsterPounceBombBase, self).start_dash()

    def end_dash(self):
        super(MonsterPounceBombBase, self).end_dash()

    def start_land(self):
        super(MonsterPounceBombBase, self).start_land()

    def start_dash_bac(self):
        super(MonsterPounceBombBase, self).start_dash_bac()
        self.init_fire()

    def end_dash_bac(self):
        super(MonsterPounceBombBase, self).end_dash_bac()

    def enter(self, leave_states):
        super(MonsterPounceBombBase, self).enter(leave_states)

    def update(self, dt):
        super(MonsterPounceBombBase, self).update(dt)

    def exit(self, enter_states):
        super(MonsterPounceBombBase, self).exit(enter_states)

    def destroy(self):
        self.reset_fire_timer()
        super(MonsterPounceBombBase, self).destroy()

    def init_fire(self):
        self.fire_ts = 0
        self.fire_idx = 0
        self.sub_idx = 0
        self.bomb_pos = []
        self.reset_fire_timer()
        self.fire_timer = global_data.game_mgr.register_logic_timer(self.tick_fire, 1, timedelta=True)

    def tick_fire(self, dt):
        if self.fire_idx >= len(self.fire_seq):
            self.reset_fire_timer()
            return
        ts, radius, count = self.fire_seq[self.fire_idx]
        if self.fire_ts >= ts:
            for i in range(int(count)):
                self.open_fire(radius)

            self.fire_idx += 1
        self.fire_ts += dt

    def open_fire(self, radius):
        center_pos = self.ev_g_position()
        if not center_pos:
            return
        self.random_pos(radius)
        fix_pos = self.bomb_pos[self.sub_idx]
        fix_x, fix_z = fix_pos.x, fix_pos.y
        pos = (
         center_pos.x + fix_x, self.ammo_height * NEOX_UNIT_SCALE, center_pos.z + fix_z)
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': pos,
           'dir': (0, -1, 0),
           'sub_idx': 0
           }
        self.sub_idx += 1
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.create_bomb_warn_sfx(self.sid, pos)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_BOMB_WARN_SFX, (self.sid, pos)], True)

    def random_pos(self, radius):
        r_count = 0
        while 1:
            if r_count < self.R_COUNT:
                pos = self.generate_random_pos(radius)
                for i in range(self.sub_idx):
                    if (pos - self.bomb_pos[i]).length < self.min_gap:
                        r_count += 1
                        break
                else:
                    self.bomb_pos.append(pos)
                    break

        else:
            self.bomb_pos.append(self.generate_random_pos(radius))

    def generate_random_pos(self, radius):
        theta = uniform(0, 2 * pi)
        r = radius * uniform(0, 1)
        pos = math3d.vector2(r * cos(theta), r * sin(theta))
        return pos

    def reset_fire_timer(self):
        if self.fire_timer:
            global_data.game_mgr.unregister_logic_timer(self.fire_timer)
            self.fire_timer = None
        return

    def create_bomb_warn_sfx(self, sid, pos):
        if sid != self.sid:
            return
        pos = math3d.vector(*pos)

        def cb(sfx):
            sfx.scale = math3d.vector(self.bomb_warn_sfx_scale, self.bomb_warn_sfx_scale, self.bomb_warn_sfx_scale)
            sfx.frame_rate = self.bomb_warn_sfx_rate
            sfx.world_position += math3d.vector(0, self.bomb_warn_sfx_offset, 0)

        pos.y = self.get_surface_h(pos)
        global_data.sfx_mgr.create_sfx_in_scene(self.bomb_warn_sfx, pos, on_create_func=cb)

    def get_surface_h(self, pos):
        return self.ev_g_position().y

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class MonsterPounceBomb(MonsterPounceBombBase):

    def init_params(self):
        super(MonsterPounceBomb, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015154)
        self.focus_time = self.custom_param.get('focus_time', 0.6)
        self.focus_dis = self.custom_param.get('focus_dis', 7.0) * NEOX_UNIT_SCALE
        self.use_bias = self.custom_param.get('use_bias', False)
        self.dash_speed = self.custom_param.get('dash_speed', 2000)
        self.max_dash_time = self.custom_param.get('max_dash_time', 2.0)
        self.gravity = self.custom_param.get('gravity', 1000)
        self.pre_dash_anim = self.custom_param.get('pre_dash_anim', 'attack_04')
        self.pre_dash_anim_dur = self.custom_param.get('pre_dash_anim_dur', 1.2)
        self.pre_dash_anim_rate = self.custom_param.get('pre_dash_anim_rate', 1.0)
        self.dash_anim = self.custom_param.get('dash_anim', 'run')
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.land_anim = self.custom_param.get('land_anim', None)
        self.land_anim_dur = self.custom_param.get('land_anim_dur', 0)
        self.land_anim_rate = self.custom_param.get('land_anim_rate', 1.0)
        self.bac_dash_anim = self.custom_param.get('bac_dash_anim', 'hit')
        self.bac_dash_anim_dur = self.custom_param.get('bac_dash_anim_dur', 0.7)
        self.bac_dash_anim_rate = self.custom_param.get('bac_dash_anim_rate', 1.0)
        self.warn_sfx = self.custom_param.get('warn_sfx', None)
        self.warn_sfx_scale = self.custom_param.get('warn_sfx_scale', 1.0)
        self.warn_sfx_rate = self.custom_param.get('warn_sfx_rate', 1.0)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.end_aoe_skill_id_2 = self.custom_param.get('end_aoe_skill_id_2', None)
        self.end_aoe_skill_socket = self.custom_param.get('end_aoe_skill_socket', 'fx_root')
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.wp_type = self.custom_param.get('wp_type', 0)
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_kind = self.wp_conf.get('iKind')
        self.ammo_height = self.custom_param.get('ammo_height', 0)
        self.fire_seq = self.custom_param.get('fire_seq', 0)
        self.min_gap = self.custom_param.get('min_gap', 0)
        self.bomb_warn_sfx = self.custom_param.get('bomb_warn_sfx', '')
        self.bomb_warn_sfx_rate = self.custom_param.get('bomb_warn_sfx_rate', 1.0)
        self.bomb_warn_sfx_scale = self.custom_param.get('bomb_warn_sfx_scale', 1.0)
        self.bomb_warn_sfx_offset = self.custom_param.get('bomb_warn_sfx_offset', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.ev_g_bias_dur()
            self.reset_sub_states_callback()
            self.register_pounce_callbacks()