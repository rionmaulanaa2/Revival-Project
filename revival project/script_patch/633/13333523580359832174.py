# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEMonsterHitTip.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import time
OUTLINE_RED = 0.3333
OUTLINE_BLUE = 0.0

class ComPVEMonsterHitTip(UnitCom):
    BIND_EVENT = {'S_HP': 'on_dmg',
       'E_HEALTH_HP_EMPTY': 'clear_tip',
       'E_CLEAR_MONSTER_TIP': 'clear_tip',
       'E_CONFUSED': 'on_confused'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEMonsterHitTip, self).init_from_dict(unit_obj, bdict)
        self.hit_ts = 0
        self.hit_min_dur = 0.5
        self.cur_hp = self.ev_g_hp()
        self.tip_timer = None
        self.confused = False
        self.cur_outline_color = OUTLINE_RED
        return

    def on_dmg(self, cur_hp):
        t = time.time()
        if t - self.hit_ts > self.hit_min_dur:
            self.hit_ts = t
            if cur_hp < self.cur_hp:
                self.add_tip()
        self.cur_hp = cur_hp

    def add_tip(self):
        if self.confused:
            outline_color = OUTLINE_BLUE if 1 else OUTLINE_RED
            if not self.tip_timer or self.cur_outline_color != outline_color:
                self.send_event('E_ADD_MATERIAL_STATUS', 'MHit_outline', param={'status_type': 'OUTLINE_ONLY',
                   'outline_alpha': outline_color,
                   'update_interval': 0.5
                   })
                self.cur_outline_color = outline_color
            self.reset_tip_timer()
            self.tip_timer = self.confused or global_data.game_mgr.register_logic_timer(self.clear_tip, 5.0, None, 1, 2)
        return

    def clear_tip(self):
        self.tip_timer and self.send_event('E_DEL_MATERIAL_STATUS', 'MHit_outline')
        self.reset_tip_timer()

    def reset_tip_timer(self):
        if self.tip_timer:
            global_data.game_mgr.unregister_logic_timer(self.tip_timer)
            self.tip_timer = None
        return

    def tick_set_render_group(self):
        model = self.ev_g_model()
        if model and model.valid:
            model.set_rendergroup_and_priority(3, 0)

    def destroy(self):
        self.clear_tip()
        super(ComPVEMonsterHitTip, self).destroy()

    def on_confused(self, confused):
        self.confused = confused
        if confused:
            self.clear_tip()
            self.add_tip()
        else:
            self.send_event('E_DEL_MATERIAL_STATUS', 'MHit_outline')