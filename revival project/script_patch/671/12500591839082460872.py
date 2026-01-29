# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8031DashUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.cdata.mecha_status_config import MC_OTHER_SHAPE
from common.const import uiconst
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
MAX_DASH_ENERGY_PERCENT = 88
MIN_DASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_DASH_ENERGY_PERCENT - MIN_DASH_ENERGY_PERCENT

class Mecha8031DashUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8031_2'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.nd_jet.setVisible(False)
        self.panel.nd_hp.setVisible(False)
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def _unregister_reaper_shape_timer(self):
        if self.reaper_shape_timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self.reaper_shape_timer_id)
            self.reaper_shape_timer_id = None
        return

    def on_finalize_panel(self):
        self._unregister_reaper_shape_timer()
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        self.beacon_unit = None
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.reaper_shape_timer_id = None
        self.beacon_eid = None
        self.beacon_unit = None
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
            regist_func('E_TRANS_TO_REAPER', self.on_trans_to_reaper, 99)
            self.on_trans_to_reaper(MC_OTHER_SHAPE in self.mecha.ev_g_cur_state())

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_TRANS_TO_REAPER', self.on_trans_to_reaper)
        self.mecha = None
        return

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def update_reaper_shape_info(self):
        if self.mecha and self.mecha.is_valid():
            percent = self.mecha.sd.ref_reaper_shape_left_time_percent
            self.panel.nd_jet.prog_jet.setPercentage(MIN_DASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * percent)
            if not self.beacon_unit:
                beacon_entity = global_data.battle.get_entity(self.beacon_eid)
                if beacon_entity and beacon_entity.logic:
                    self.beacon_unit = beacon_entity.logic
            if self.beacon_unit and self.beacon_unit.is_valid():
                hp_percent = self.beacon_unit.ev_g_health_percent() * 100
                self.panel.nd_hp.prog_jet.setPercentage(hp_percent)

    def on_trans_to_reaper(self, left_time, beacon_eid=None):
        if left_time > 0:
            if self.reaper_shape_timer_id is None:
                self.panel.nd_jet.setVisible(True)
                self.panel.nd_hp.setVisible(True)
                self.beacon_eid = beacon_eid
                self.update_reaper_shape_info()
                self.reaper_shape_timer_id = global_data.game_mgr.register_logic_timer(self.update_reaper_shape_info, interval=1, times=-1)
        else:
            self.beacon_eid = None
            self.beacon_unit = None
            self.panel.nd_jet.setVisible(False)
            self.panel.nd_hp.setVisible(False)
            self._unregister_reaper_shape_timer()
        return