# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComShockWaveCore.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr
import math3d
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComShockWaveCore(UnitCom):
    BIND_EVENT = {'E_SFX_INIT': 'on_sfx_init'
       }

    def init_from_dict(self, unit, bdict):
        super(ComShockWaveCore, self).init_from_dict(unit, bdict)
        self.init_params(bdict)
        self.process_event(True)

    def init_params(self, bdict):
        self.item_id = bdict.get('item_id')
        self.conf = confmgr.get('grenade_res_config', str(self.item_id))
        self.params = global_data.pve_shockwave_dict or self.conf.get('cCustomParam') if 1 else global_data.pve_shockwave_dict
        self.center = math3d.vector(*bdict.get('position'))
        self.r_inner = 0
        self.r_outer = 1.0 * NEOX_UNIT_SCALE
        self.height = self.params['height']
        self.dur = self.params['dur']
        self.rate = self.params['rate']
        self.sfx_range = self.params['sfx_range'] * NEOX_UNIT_SCALE
        self.valid_range = self.params['valid_range'] * NEOX_UNIT_SCALE
        self.scale = self.params['scale']
        self.r_adder = self.sfx_range * self.scale / (self.dur / self.rate)
        self.ts = 0
        self.hit_set = set([])

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_sfx_init(self):
        self.need_update = True

    def destroy(self):
        super(ComShockWaveCore, self).destroy()

    def tick(self, dt):
        self.check_hit()
        self.ts += dt
        if self.ts > self.dur / self.rate * (self.valid_range / self.sfx_range):
            self.need_update = False

    def check_hit(self):
        if not global_data.mecha or not global_data.mecha.logic:
            return
        tar_pos = global_data.mecha.logic.ev_g_position()
        tar_pos.y = self.center.y
        tar_dire = tar_pos - self.center
        tar_dire.normalize()
        start_pos = self.center + tar_dire * (self.r_inner + self.ts * self.r_adder)
        start_pos.y += self.height
        end_pos = self.center + tar_dire * (self.r_outer + self.ts * self.r_adder)
        end_pos.y += self.height
        if global_data.is_inner_server:
            global_data.emgr.scene_draw_line_event.emit([start_pos, end_pos])
        hit_set = set([])
        result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
        if result[0]:
            for t in result[1]:
                hit_target = global_data.emgr.scene_find_unit_event.emit(t[4].cid)[0]
                if not hit_target:
                    continue
                elif not hit_target.sd.ref_monster_id:
                    hit_set.add(hit_target.id)
                else:
                    continue

        if hit_set and hit_set != self.hit_set:
            self.hit_set = hit_set
            self.upload_hit()

    def upload_hit(self):
        self.send_event('E_CALL_SYNC_METHOD', 'shockwave_hit_target', (list(self.hit_set),), True)