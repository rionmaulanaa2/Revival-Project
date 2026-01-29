# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8502AimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
import logic.gcommon.const as g_const
from common.cfg import confmgr
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
import cc
import math
from logic.comsys.mecha_ui.Mecha8501AimUI import Mecha8501AimUI
ASSOCIATE_UI_LIST = [
 'FrontSightUI']

class Mecha8502AimUI(Mecha8501AimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_chicken2'

    def on_init_panel(self):
        super(Mecha8502AimUI, self).on_init_panel()