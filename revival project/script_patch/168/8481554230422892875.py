# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossShieldTowerLogic.py
from __future__ import absolute_import
from .PVEMonsterSummonLogic import MonsterSummon
from common.cfg import confmgr
import math3d
from math import radians
from logic.gcommon.const import NEOX_UNIT_SCALE

class BossShieldTower(MonsterSummon):

    def init_params(self):
        super(BossShieldTower, self).init_params()
        self.tower_sfx_res = self.custom_param.get('tower_sfx_res', 'effect/fx/monster/pve/pve_fanweijingshi_01.sfx')
        self.tower_sfx_rate = self.custom_param.get('tower_sfx_rate', 1.0)
        self.tower_sfx_scale = self.custom_param.get('tower_sfx_scale', 1.0)
        self.tower_sfx_offset = self.custom_param.get('tower_sfx_offset', 0)
        self.summon_info = confmgr.get('skill_conf', str(self.skill_id), 'ext_info', 'summoninfo')
        self.tower_info = []
        for summon_target in self.summon_info:
            if 'monster_id' in summon_target:
                self.tower_info.append([summon_target['angle'], summon_target['dis']])

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_summon_callbacks()

    def start_pre(self):
        super(BossShieldTower, self).start_pre()

        def cb(sfx):
            sfx.scale = math3d.vector(self.tower_sfx_scale, self.tower_sfx_scale, self.tower_sfx_scale)
            sfx.frame_rate = self.tower_sfx_rate

        for t in self.tower_info:
            angle, dis = t
            m_pos = self.ev_g_position()
            yaw = self.ev_g_yaw()
            forward = math3d.matrix.make_rotation_y(yaw).forward
            forward.y = 0
            new_dire = forward * math3d.matrix.make_rotation_y(radians(angle))
            new_dire.normalize()
            diff_add = new_dire * dis * NEOX_UNIT_SCALE
            t_pos = m_pos + diff_add
            t_pos.y += self.tower_sfx_offset
            global_data.sfx_mgr.create_sfx_in_scene(self.tower_sfx_res, t_pos, 5, cb)

    def update(self, dt):
        super(BossShieldTower, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)