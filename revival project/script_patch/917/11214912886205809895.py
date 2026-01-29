# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/TVMissileLauncherAimUI.py
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
 'FrontSightUI']

class TVMissileLauncherAimUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_tv_missile_launcher'
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        from logic.comsys.battle.AimColorWidget import AimColorWidget
        self._aimColorWidget = AimColorWidget(self, self.panel)
        self._aimColorWidget.calculate_aim_node()
        self._aimColorWidget.setup_color()

    def on_finalize_panel(self):
        self.destroy_widget('_aimColorWidget')
        self.show_main_ui()