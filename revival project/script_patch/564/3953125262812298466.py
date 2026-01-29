# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/BattleStartHumanInfo.py
from __future__ import absolute_import
from logic.comsys.effect import ui_effect
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, DIALOG_LAYER_BAN_ZORDER
from logic.gcommon.item import item_const
from logic.gcommon.common_const.buff_const import COMMON_BUFF, BUFF_SET_FIRE, BUFF_ID_ZOMBIEFFA_MECHA_BLOOD, BUFF_ID_ZOMBIEFFA_MECHA_TUFF
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gcommon.common_utils import text_utils
from logic.gcommon.common_const.buff_const import SFX_TARGET_TYPE_TO_STR, SFX_VIS_SKATEBOARD, BUFF_ID_BOND_GIFT_HP_DOWN_SHIELD_CD
from common.const import uiconst
import cc

class BattleStartHumanInfo(BasePanel):
    PANEL_CONFIG_NAME = 'battle_hunting/battle_hunting_start_tips'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.PlayAnimation('break')
        self.panel.SetTimeOut(1.0, self.disappear)
        self.panel.SetTimeOut(3.0, lambda : self.panel.PlayAnimation('break_out'))
        self.panel.SetTimeOut(4.0, self.close)

    def disappear(self):
        pass

    def on_finalize_panel(self):
        pass


class BattleStartMechaInfo(BattleStartHumanInfo):
    PANEL_CONFIG_NAME = 'battle_hunting/battle_hunting_start_tips2'