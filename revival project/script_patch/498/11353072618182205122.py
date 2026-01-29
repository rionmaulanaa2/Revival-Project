# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaFuelUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
ASSOCIATE_UI_LIST = []
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_red.png',
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png']
from common.const import uiconst

class MechaFuelUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/i_mech_power'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.mecha = None
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.panel.nd_power.setVisible(False)
        self.process_lack_fuel_event(True)
        return

    def on_finalize_panel(self):
        self.unbind_ui_event()
        self.show_main_ui()
        self.process_lack_fuel_event(False)

    def enter_screen(self):
        super(MechaFuelUI, self).enter_screen()
        emgr = global_data.emgr
        self.on_player_setted(global_data.cam_lplayer)
        econf = {'scene_camera_player_setted_event': self.on_cam_lplayer_setted,
           'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        self.init_parameters()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def leave_screen(self):
        super(MechaFuelUI, self).leave_screen()
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_lplayer_setted,
           'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.unbind_events(econf)
        self.unbind_ui_event()

    def init_parameters(self):
        self.mecha = None
        self.last_val_percent = 100
        return

    def init_event(self):
        cur_fuel = self.mecha.ev_g_fuel()
        max_fuel = self.mecha.ev_g_max_fuel()
        self.last_val_percent = cur_fuel
        self.progress_pic = 0 if self.last_val_percent <= 25 else 1
        self.panel.prog_power.SetProgressTexture(PROGRESS_PIC[self.progress_pic])
        self.on_fuel_energy_changed(cur_fuel * 1.0 / max_fuel)
        self.panel.nd_power.setVisible(cur_fuel < max_fuel)

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())
        if not player:
            self.leave_screen()

    def unbind_ui_event(self, *args):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_FUEL_CHANGE', self.on_fuel_energy_changed)
        self.mecha = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event()
        if not mecha:
            return
        self.mecha = mecha
        regist_func = mecha.regist_event
        regist_func('E_FUEL_CHANGE', self.on_fuel_energy_changed)
        self.init_event()

    def on_fuel_energy_changed(self, percent):
        if not self.is_valid():
            return
        percent *= 100
        percentage_range = (62, 88)
        rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
        if self.last_val_percent < percent == 100:
            self.panel.nd_power.setVisible(False)
        elif self.last_val_percent == 100 > percent:
            self.panel.nd_power.setVisible(True)
            self.panel.PlayAnimation('showing')
        progress_pic = 0 if self.last_val_percent <= 25 else 1
        if self.progress_pic != progress_pic:
            self.progress_pic = progress_pic
            self.panel.prog_power.SetProgressTexture(PROGRESS_PIC[progress_pic])
            self.panel.prog_power.setPercentage((percent + 0.01) * rate + percentage_range[0])
        self.panel.prog_power.setPercentage(percent * rate + percentage_range[0])
        self.last_val_percent = percent
        if self.panel.nd_power.isVisible():
            global_data.player.logic.send_event('E_GUIDE_MECHA_FUEL', True)
        else:
            global_data.player.logic.send_event('E_GUIDE_MECHA_FUEL', False)

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def process_lack_fuel_event(self, is_bind):
        if is_bind:
            global_data.emgr.mecha_skill_lack_fuel_event += self.show_lack_fuel_anim
        else:
            global_data.emgr.mecha_skill_lack_fuel_event -= self.show_lack_fuel_anim

    def show_lack_fuel_anim(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.PlayAnimation('low_power')