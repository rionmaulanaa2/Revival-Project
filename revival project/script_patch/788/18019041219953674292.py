# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8004HeatUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.component.client.com_mecha_appearance.ComHeatEnergyClient import MAX_HEAT_STATE
from common.cfg import confmgr
import cc
from common.const import uiconst

class Mecha8004HeatUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech8004_heat'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    MAX_HEAT = 3000

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        return

    def init_parameters(self):
        self.heat_action = None
        self.player = None
        self.mecha = None
        self.last_heat = 0
        self.last_heat_state = 0
        emgr = global_data.emgr
        self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def init_event(self):
        if not self.mecha:
            return
        heat_info = self.mecha.ev_g_heat()
        if heat_info:
            self.nd_heat_disappear()
            self.on_heat_change(*heat_info)

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SET_HEAT', self.on_heat_change)
        self.mecha = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            heat_conf = confmgr.get('mecha_conf', 'HeatEnergyConfig', 'Content').get(str(mecha.share_data.ref_mecha_id))
            if heat_conf:
                self.MAX_HEAT = heat_conf.get('heat_cnt')
            regist_func = mecha.regist_event
            regist_func('E_SET_HEAT', self.on_heat_change)
            self.init_event()

    def on_heat_change(self, heat, heat_state):
        if heat and heat < self.last_heat and not self.panel.nd_heat.isVisible():
            self.panel.PlayAnimation('show_heat')
        elif (heat == 0 or heat and heat > self.last_heat) and self.panel.nd_heat.isVisible():
            self.nd_heat_disappear()
        percent = 100.0 * heat / self.MAX_HEAT
        state_index = 1 if heat_state == MAX_HEAT_STATE else 0
        if self.last_heat_state != heat_state:
            ani_name = [
             'disappear_frenzy', 'show_frenzy']
            self.panel.PlayAnimation(ani_name[state_index])
        if state_index == 1:
            percent += 0.1
        MIN_PERCENT = 47
        MAX_PERCENT = 56
        bar_percent = MIN_PERCENT + (MAX_PERCENT - MIN_PERCENT) * (percent * 1.0 / 100)
        self.panel.progress_heat1.SetPercent(bar_percent)
        self.panel.progress_heat2.SetPercent(bar_percent)
        self.last_heat = heat
        self.last_heat_state = heat_state

    def nd_heat_disappear(self):
        self.panel.PlayAnimation('disappear_heat')

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')