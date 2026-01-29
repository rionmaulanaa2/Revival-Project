# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTestShow.py
from __future__ import absolute_import
from ..UnitCom import UnitCom

def get_test_list():
    test_list = [
     'E_HEALTH_INIT',
     'E_HEALTH_HP_CHANGE',
     'E_AIR_SHOOT',
     'E_WPBAR_INIT']
    return test_list


class ComTestShow(UnitCom):
    BIND_EVENT = {'E_TEST_SHOW_TXT': 'show_text'
       }

    def __init__(self):
        super(ComTestShow, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComTestShow, self).init_from_dict(unit_obj, bdict)
        arr = get_test_list()

        def get_cb(e_name):
            return lambda *args, **argv: self.on_show(e_name, *args, **argv)

        for s_evt in arr:
            self.regist_event(s_evt, get_cb(s_evt))

    def destroy(self):
        super(ComTestShow, self).destroy()

    def on_show(self, e_name, *args, **argv):
        if not e_name:
            return
        func = getattr(self, e_name.lower())
        if func:
            func(*args, **argv)

    def show_text(self, s_text, fade=0):
        global_data.emgr.battle_show_message_event.emit(s_text, fade)

    def e_health_init(self, *args, **argv):
        if self.unit_obj.id != global_data.player.logic.id:
            return
        hp = self.ev_g_hp()
        self.show_text('Your Health: hp={}'.format(hp))

    def e_air_shoot(self, start_pos, end_pos, *args):
        import math3d
        global_data.emgr.scene_bullet_event.emit(start_pos, end_pos)
        self.show_text('\xe5\xad\x90\xe5\xbc\xb9\xe5\x87\xbb\xe4\xb8\xad\xe5\x9c\xba\xe6\x99\xaf:{}'.format([ int(v) for v in end_pos ]))

    def e_health_hp_change(self, hp, mod):
        if self.unit_obj.id == global_data.player.logic.id:
            self.show_text('\xe4\xbd\xa0\xe7\x9a\x84HP={}, MOD={}'.format(hp, mod))
            return
        self.show_text('\xe7\x8e\xa9\xe5\xae\xb6ID\xe5\xb0\xbe\xe5\x8f\xb7{}\xe7\x9a\x84: Hp = {}, mod = {}'.format(str(self.unit_obj.id)[-4:], hp, mod))

    def e_wpbar_init(self):
        cur_wp = self.ev_g_wpbar_cur_weapon()
        all_wp = self.ev_g_all_weapons_in_bar()
        self.show_text('\xe6\xad\xa6\xe5\x99\xa8\xe6\xa0\x8f\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe5\xae\x8c\xe6\x88\x90\xef\xbc\x8c\xe5\xbd\x93\xe5\x89\x8d\xe6\xad\xa6\xe5\x99\xa8:{}'.format(cur_wp))
        self.show_text('\xe6\xad\xa6\xe5\x99\xa8\xe6\xa0\x8f\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe5\xae\x8c\xe6\x88\x90\xef\xbc\x8c\xe6\x89\x80\xe6\x9c\x89\xe6\xad\xa6\xe5\x99\xa8:{}'.format(all_wp))