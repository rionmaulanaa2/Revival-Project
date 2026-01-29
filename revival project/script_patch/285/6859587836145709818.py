# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/TVMissileAimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
import logic.gcommon.const as g_const
from common.cfg import confmgr
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
from common.const import uiconst
import cc
import math
ASSOCIATE_UI_LIST = [
 'TVMissileLauncherUI', 'MechaControlMain', 'TeammateUI']

class TVMissileAimUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_tv_missile'
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True
    AUTO_AIM_SIZE = 60.0

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.hide_main_ui(exceptions=ASSOCIATE_UI_LIST)
        self.missile_unit = None
        self.update_missile_left_fuel_timer = None
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        self.missile_unit = None
        if self.update_missile_left_fuel_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_missile_left_fuel_timer)
            self.update_missile_left_fuel_timer = None
        return

    def update_missile_left_fuel(self):
        if self.missile_unit and self.missile_unit.is_valid():
            percent = self.missile_unit.sd.ref_left_duration_percent * 100
            self.panel.nd_prog.prog.SetPercentage(percent)
            self.panel.nd_prog.lab_prog.SetString('%d%%' % percent)

    def hide_fuel_info(self):
        self.panel.nd_prog.setVisible(False)

    def set_missile_unit(self, missile_unit):
        if missile_unit is None:
            self.hide_fuel_info()
            return
        else:
            self.missile_unit = missile_unit
            self.update_missile_left_fuel()
            self.update_missile_left_fuel_timer = global_data.game_mgr.register_logic_timer(self.update_missile_left_fuel, interval=1, times=-1)
            return