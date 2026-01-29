# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/BattleStartMechaInfo.py
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

class BattleFallWarnUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/i_fight_newmap_backtips2'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.hide_main_ui()
        self.panel.PlayAnimation('break')
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def disappear(self):
        self.panel.DelayCall(2.0, lambda *args: self.panel.PlayAnimation('break_out') and 0)
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)