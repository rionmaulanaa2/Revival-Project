# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ShieldBloodUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
ICON_RES = [
 'gui/ui_res_2/battle/attack/shield_blood_prog',
 'gui/ui_res_2/battle/attack/shield_blood_bar',
 'gui/ui_res_2/battle/attack/icon_shield']
CRITICAL_PERCENT = 50
from common.const import uiconst

class ShieldBloodUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_shield'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.init_ui()
        self.init_event()

    def init_ui(self):
        pass

    def init_event(self):
        global_data.emgr.target_dead_event += self.close_ui
        global_data.emgr.target_defeated_event += self.close_ui
        global_data.emgr.auto_aim_pos_update += self.init_ui
        global_data.emgr.on_observer_control_target_changed += self.on_ctrl_target_changed
        global_data.emgr.on_observer_parachute_stage_changed += self.on_parachute_stage_changed

    def close_ui(self, *args):
        global_data.ui_mgr.close_ui('ShieldBloodUI')

    def update_shield_info(self, armor):
        percentage_range = (67.64, 82.33)
        rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
        percent = max(min(100, armor.get_duration_percent() * 100), 0)
        self.update_uires(percent)
        self.prog_blood.setPercentage(percent * rate + percentage_range[0])
        cur_dur = armor.get_cur_dur()
        max_dur = armor.get_max_dur()
        self.panel.lab_hp.SetString(ui_utils.get_ratio_txt(cur_dur, max_dur))
        if cur_dur == max_dur and armor.conf('iDurFullHide'):
            self.close()

    def update_uires(self, percent):
        blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
        self.prog_blood.SetProgressTexture(blood_res)
        bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
        self.prog_bar.SetDisplayFrameByPath('', bar_res)

    def get_uires_by_percent(self, percent, original_res):
        if percent >= CRITICAL_PERCENT:
            return ''.join([original_res, '.png'])
        return ''.join([original_res, '_red', '.png'])

    def on_ctrl_target_changed(self, target):
        self.panel.setVisible(not bool(target))

    def on_parachute_stage_changed(self, stage):
        from logic.gcommon.common_utils.parachute_utils import STAGE_LAND
        self.panel.setVisible(stage == STAGE_LAND)