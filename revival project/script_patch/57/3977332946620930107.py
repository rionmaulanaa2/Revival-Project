# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8006RushUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
import common.utils.timer as timer
import time
from common.cfg import confmgr
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
from common.const import uiconst
MAX_DASH_ENERGY_PERCENT = 88
MIN_DASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_DASH_ENERGY_PERCENT - MIN_DASH_ENERGY_PERCENT

class Mecha8006RushUI(BasePanel):
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
        if self._update_dash_action:
            self.panel.stopAction(self._update_dash_action)
            self._update_dash_action = None
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self._update_dash_action = None
        self._timer_id = None
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        self._max_buff_duration = 4.5
        self._max_buff_duration_locked = False
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
            regist_func('E_START_ALL_AROUND_SPEED_BUFF', self._show_dash_progress)
            regist_func('E_STOP_ALL_AROUND_SPEED_BUFF', self._clsoe_dash_progress)
            regist_func('E_REPLACE_DASH_ICON', self._replace_dash_icon)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_START_ALL_AROUND_SPEED_BUFF', self._show_dash_progress)
            unregist_func('E_STOP_ALL_AROUND_SPEED_BUFF', self._clsoe_dash_progress)
            unregist_func('E_REPLACE_DASH_ICON', self._replace_dash_icon)
        self.mecha = None
        return

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _show_dash_progress(self, buff_id, data, left_time):
        if buff_id:
            duration = data.get('duration', 4.5)
            if not self._max_buff_duration_locked:
                self._max_buff_duration_locked = True
                self._max_buff_duration = duration
        else:
            self._max_buff_duration = left_time
        self.dash_full_time = left_time
        self.dash_start_time = time.time()
        self.panel.nd_jet.setVisible(True)
        self._timer_id = global_data.game_mgr.register_logic_timer(self._update_dash_progress, interval=0.03, times=-1, mode=timer.CLOCK)

    def _clsoe_dash_progress(self):
        self._max_buff_duration_locked = False
        self.panel.nd_jet.setVisible(False)
        if self._update_dash_action:
            self.panel.stopAction(self._update_dash_action)
            self._update_dash_action = None
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def _replace_dash_icon(self, icon_path):
        self.panel.icon_skill.SetDisplayFrameByPath('', icon_path)

    def _update_dash_progress(self):
        cur_left_time = self.dash_full_time - (time.time() - self.dash_start_time)
        if cur_left_time <= 0:
            cur_left_time = 0
        if self.panel is not None:
            self.panel.prog_jet.setPercentage(MIN_DASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * cur_left_time / self._max_buff_duration)
        return