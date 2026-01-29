# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHealthCrystalClient.py
from ..share.ComHealth import ComHealth
CRYSTAL_DAMAGED_HP_RATE = 0.2

class ComHealthCrystalClient(ComHealth):

    def init_from_dict(self, unit_obj, bdict):
        super(ComHealthCrystalClient, self).init_from_dict(unit_obj, bdict)
        self.faction_id = bdict.get('faction_id')
        self.process_global_event(True)

    def on_post_init_complete(self, bdict):
        super(ComHealthCrystalClient, self).on_post_init_complete(bdict)
        self.do_update_crystal_hp()

    def destroy(self):
        super(ComHealthCrystalClient, self).destroy()
        self.process_global_event(False)

    def process_global_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'ask_update_crystal_hp': self.do_update_crystal_hp
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_hp(self, hp):
        super(ComHealthCrystalClient, self).set_hp(hp)
        self.do_update_crystal_hp()
        cur_hp_percent = self.get_hp_percent()
        self.send_event('E_CRYSTAL_HP_CHANGE', hp, cur_hp_percent)
        if cur_hp_percent < CRYSTAL_DAMAGED_HP_RATE:
            self.send_event('E_CRYSTAL_LOW_HP')

    def do_update_crystal_hp(self):
        global_data.emgr.do_update_crystal_hp.emit(self.faction_id, self.get_hp_percent())