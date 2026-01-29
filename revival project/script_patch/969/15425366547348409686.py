# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEResWidget.py
from __future__ import absolute_import
from math import ceil

class PVEResWidget(object):
    TEMPLATE = 'battle_tips/pve/i_pve_tips_res_window'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.init_ui_nds()
        self.process_events(True)
        self.init_crystal()
        self.init_coin()

    def init_params(self):
        self.widget = None
        self.crystal_num = 0
        self.coin_num = 0
        self.nd_crystal = None
        self.nd_coin = None
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)

    def init_ui_nds(self):
        if not self.widget:
            return
        self.widget.nd_res_tips.setVisible(False)
        self.widget.list_money.SetInitCount(2)
        self.nd_crystal = self.widget.list_money.GetItem(0)
        self.nd_coin = self.widget.list_money.GetItem(1)

    def process_events(self, is_bind):
        econf = {'scene_player_setted_event': self.on_player_setted,
           'pve_update_crystal_num': self.update_crystal,
           'pve_cost_crystal_stone': self.on_cost_crystal,
           'pve_update_coin_num': self.update_coin
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.widget and self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def on_player_setted(self, *args):
        self.init_crystal()
        self.init_coin()

    def update_crystal(self, num, add):
        if not self.widget:
            return
        self.nd_crystal.num_2.SetString(str(self.crystal_num))
        self.nd_crystal.num_1.SetString(str(ceil((self.crystal_num + num) * 0.5)))
        self.nd_crystal.num.SetString(str(num))
        if add > 0:
            self.nd_crystal.lab_num_add.SetString(('%.2f' % add).strip('0').strip('.'))
        self.nd_crystal.StopAnimation('appear')
        self.nd_crystal.PlayAnimation('appear')
        self.crystal_num = num

    def update_coin(self, num):
        if not self.widget:
            return
        self.nd_coin.num_2.SetString(str(self.coin_num))
        self.nd_coin.num_1.SetString(str(ceil((self.coin_num + num) * 0.5)))
        self.nd_coin.num.SetString(str(num))
        self.nd_coin.lab_num_add.SetString(str(num - self.coin_num))
        self.nd_coin.PlayAnimation('appear')
        self.coin_num = num

    def on_cost_crystal(self):
        if not global_data.player or not global_data.player.logic:
            return
        if not self.widget:
            return
        num = global_data.player.logic.ev_g_crystal_stone()
        self.nd_crystal.num.SetString(str(num))

    def init_crystal(self):
        if not global_data.player or not global_data.player.logic:
            return
        if not self.widget:
            return
        num = global_data.player.logic.ev_g_crystal_stone()
        self.update_crystal(num, 0)

    def init_coin(self):
        if not global_data.player or not global_data.player.logic:
            return
        if not self.widget:
            return
        num = global_data.player.logic.ev_g_pve_coin_num()
        self.update_coin(num)