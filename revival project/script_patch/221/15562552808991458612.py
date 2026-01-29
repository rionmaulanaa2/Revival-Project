# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEMonsterShake.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d

class ComPVEMonsterShake(UnitCom):
    BIND_EVENT = {'S_HP': 'on_dmg'
       }
    off = 0.75
    off_list = [
     [
      off, off, off],
     [
      off, off, -off],
     [
      off, -off, off],
     [
      off, -off, -off],
     [
      -off, off, off],
     [
      -off, off, -off],
     [
      -off, -off, off],
     [
      -off, -off, -off]]
    s_states = {
     101,
     217,
     223,
     224,
     226,
     235,
     237,
     240,
     241,
     242,
     243,
     244,
     247}

    def __init__(self):
        super(ComPVEMonsterShake, self).__init__()
        self.shake_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEMonsterShake, self).init_from_dict(unit_obj, bdict)
        self.shake_idx = 0
        self.tick_count = 0
        self.is_boss = None
        return

    def on_dmg(self, *args):
        if self.shake_timer:
            return
        self.init_shake()

    def init_shake(self):
        self.reset_shake_timer()
        self.tick_count = 0
        if self.check_state():
            self.shake_timer = global_data.game_mgr.register_logic_timer(self.tick_shake, 1, None, len(self.off_list))
        return

    def tick_shake(self, *args):
        off = self.off_list[self.shake_idx % len(self.off_list)]
        self.shake_idx += 1
        self.tick_count += 1
        model = self.ev_g_model()
        if not model or not model.valid:
            self.reset_shake_timer()
            return
        model.position += math3d.vector(*off)
        if self.tick_count >= len(self.off_list):
            self.reset_shake_timer()

    def reset_shake_timer(self):
        if self.shake_timer:
            global_data.game_mgr.unregister_logic_timer(self.shake_timer)
            self.shake_timer = None
        return

    def check_state(self):
        states = self.ev_g_cur_state()
        if states & self.s_states:
            return False
        return True

    def destroy(self):
        self.reset_shake_timer()
        super(ComPVEMonsterShake, self).destroy()