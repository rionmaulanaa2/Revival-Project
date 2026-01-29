# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEMonsterPosChecker.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from random import uniform
from logic.gcommon.cdata.pve_monster_status_config import MC_MOVE, MC_RUN
import collision

class ComPVEMonsterPosChecker(UnitCom):
    RAD = 0.45
    SEQ = [
     [
      0, 0],
     [
      -RAD, 0],
     [
      RAD, 0],
     [
      0, RAD],
     [
      0, -RAD]]
    BIND_EVENT = {'E_BEGIN_AGENT_AI': 'init_check',
       'E_HEALTH_HP_EMPTY': 'on_hp_empty'
       }

    def __init__(self):
        super(ComPVEMonsterPosChecker, self).__init__()
        self.need_update = False
        self.ts = 0
        self.last_pos = math3d.vector(0, 0, 0)
        self._col_ids = []
        self.check_cnt = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEMonsterPosChecker, self).init_from_dict(unit_obj, bdict)

    def init_check(self, *args):
        if self.ev_g_need_pos_check():
            self.last_pos = self.ev_g_position()
            self.need_update = True

    def tick(self, dt):
        self.ts += dt
        if self.ts > uniform(1, 3):
            pos = self.ev_g_position()
            if (pos - self.last_pos).length < 0.5 * NEOX_UNIT_SCALE:
                if self.ev_g_cur_state() & {MC_MOVE, MC_RUN}:
                    self.check_cnt = 0
                    self.start_ray_check(pos)
            self.last_pos = pos
            self.ts = 0

    def start_ray_check(self, pos):
        self.check_cnt += 1
        if self.check_cnt > 10:
            return
        self._col_ids = self.ev_g_human_col_id()
        c_size = self.ev_g_character_size()
        if not c_size:
            return
        width, height = c_size
        safe_tag = True
        for i in range(0, len(self.SEQ)):
            start_pos = math3d.vector(pos.x + width * self.SEQ[i][0] * NEOX_UNIT_SCALE, pos.y, pos.z + width * self.SEQ[i][1] * NEOX_UNIT_SCALE)
            end_pos = math3d.vector(start_pos)
            end_pos.y += height * NEOX_UNIT_SCALE
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
            if result[0]:
                for t in result[1]:
                    if t[4].cid in self._col_ids:
                        continue
                    else:
                        safe_tag = False
                        break

                if not safe_tag:
                    break
            else:
                continue

        ret_pos = pos + math3d.vector(0, height * NEOX_UNIT_SCALE + 1, 0)
        if safe_tag:
            self.send_event('E_FOOT_POSITION', pos)
        else:
            self.start_ray_check(ret_pos)

    def on_hp_empty(self, *args):
        self.need_update = False

    def destroy(self):
        super(ComPVEMonsterPosChecker, self).destroy()