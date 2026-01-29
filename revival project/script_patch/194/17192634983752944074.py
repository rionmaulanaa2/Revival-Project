# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8028DashUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.common_const.skill_const import SKILL_8028_RABBIT_RUN
from logic.gcommon.cdata.mecha_status_config import MC_DASH
from common.const import uiconst
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
MAX_DASH_ENERGY_PERCENT = 88
MIN_DASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_DASH_ENERGY_PERCENT - MIN_DASH_ENERGY_PERCENT

class Mecha8028DashUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8006_2'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.nd_jet.setVisible(False)
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.energy_changed_event_registered = False
        self._timer_id = None
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_SET_DASH_UI_VISIBLE', self.set_dash_ui_visible)
            self.set_dash_ui_visible(MC_DASH in self.mecha.ev_g_cur_state())

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SET_DASH_UI_VISIBLE', self.set_dash_ui_visible)
            self._register_energy_changed_event(False)
        self.mecha = None
        return

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _register_energy_changed_event(self, flag):
        if self.energy_changed_event_registered ^ flag:
            func = self.mecha.regist_event if flag else self.mecha.unregist_event
            func('E_ENERGY_CHANGE', self.on_energy_changed)
            self.energy_changed_event_registered = flag

    def set_dash_ui_visible(self, visible):
        self._register_energy_changed_event(visible)
        self.panel.nd_jet.setVisible(visible)
        if visible:
            self.panel.prog_jet.setPercentage(MIN_DASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * self.mecha.ev_g_energy(SKILL_8028_RABBIT_RUN))

    def on_energy_changed(self, skill_id, percent):
        if skill_id != SKILL_8028_RABBIT_RUN:
            return
        self.panel.prog_jet.setPercentage(MIN_DASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * percent)