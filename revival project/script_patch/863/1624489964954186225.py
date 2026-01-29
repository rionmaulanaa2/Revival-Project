# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEResUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_0
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_NO_EFFECT
from math import ceil
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import game3d
import common.utils.timer as timer

class PVEResUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/pve/i_pve_tips_res_window'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args):
        super(PVEResUI, self).on_init_panel(*args)
        self.init_params()
        self.init_ui_nds()
        self.process_events(True)
        self.init_crystal()
        self.init_coin()
        self.init_custom_com()

    def init_params(self):
        self.crystal_num = 0
        self.coin_num = 0
        self.cache_crystal_add = 0
        self.cache_coin_add = 0
        self.nd_crystal = None
        self.nd_coin = None
        self.show_add_crystal_timer = None
        self.show_add_coin_timer = None
        return

    def init_ui_nds(self):
        self.panel.nd_res_tips.setVisible(False)
        self.panel.list_money.SetInitCount(2)
        self.nd_crystal = self.panel.list_money.GetItem(0)
        self.nd_coin = self.panel.list_money.GetItem(1)

    def process_events(self, is_bind):
        econf = {'scene_camera_player_setted_event': self.on_cam_lplayer_setted,
           'pve_update_crystal_num': self.update_crystal,
           'pve_cost_crystal_stone': self.on_cost_crystal,
           'pve_update_coin_num': self.update_coin
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def on_finalize_panel(self):
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        self.cancel_show_add_crystal_timer()
        self.cancel_show_add_coin_timer()
        self.process_events(False)
        super(PVEResUI, self).on_finalize_panel()
        return

    def on_cam_lplayer_setted(self, *args):
        self.init_crystal()
        self.init_coin()

    def cancel_show_add_crystal_timer(self):
        if self.show_add_crystal_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_add_crystal_timer)
            self.show_add_crystal_timer = None
        return

    def update_crystal(self, num, add):
        self.nd_crystal.num_2.SetString(str(self.crystal_num))
        self.nd_crystal.num_1.SetString(str(ceil((self.crystal_num + num) * 0.5)))
        self.nd_crystal.num.SetString(str(num))
        if add > 0:
            self.cancel_show_add_crystal_timer()
            self.cache_crystal_add += add
            self.show_add_crystal_timer = global_data.game_mgr.register_logic_timer(self._update_add_crystal, interval=0.3, times=1, mode=timer.CLOCK)
        self.crystal_num = num

    def _update_add_crystal(self):
        self.show_add_crystal_timer = None
        self.nd_crystal.lab_num_add.SetString(('%.2f' % self.cache_crystal_add).strip('0').strip('.'))
        self.nd_crystal.StopAnimation('appear')
        self.nd_crystal.PlayAnimation('appear')
        self.cache_crystal_add = 0
        return

    def cancel_show_add_coin_timer(self):
        if self.show_add_coin_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_add_coin_timer)
            self.show_add_coin_timer = None
        return

    def update_coin(self, num):
        self.nd_coin.num_2.SetString(str(self.coin_num))
        self.nd_coin.num_1.SetString(str(ceil((self.coin_num + num) * 0.5)))
        self.nd_coin.num.SetString(str(num))
        self.nd_coin.lab_num_add.SetString(str(num - self.coin_num))
        add = num - self.coin_num
        if add > 0:
            self.cancel_show_add_coin_timer()
            self.show_add_coin_timer = global_data.game_mgr.register_logic_timer(self._update_add_coin, interval=0.3, times=1, mode=timer.CLOCK)
            self.cache_coin_add += add
        self.coin_num = num

    def _update_add_coin(self):
        self.show_add_coin_timer = None
        self.nd_coin.lab_num_add.SetString(('%.2f' % self.cache_coin_add).strip('0').strip('.'))
        self.nd_coin.StopAnimation('appear')
        self.nd_coin.PlayAnimation('appear')
        self.cache_coin_add = 0
        return

    def on_cost_crystal(self):
        if not global_data.cam_lplayer:
            return
        num = global_data.cam_lplayer.ev_g_crystal_stone()
        self.nd_crystal.num.SetString(str(num))

    def init_crystal(self):
        if not global_data.cam_lplayer:
            return
        num = global_data.cam_lplayer.ev_g_crystal_stone()
        self.update_crystal(num, 0)

    def init_coin(self):
        if not global_data.cam_lplayer:
            return
        num = global_data.cam_lplayer.ev_g_pve_coin_num()
        self.update_coin(num)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})