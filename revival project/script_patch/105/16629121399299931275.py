# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/HpInfoUIPC.py
from __future__ import absolute_import
from .HpInfoUI import HpInfoBaseUI
from common.framework import Functor
from logic.gcommon.common_const import ui_battle_const as ubc
import world
from logic.gutils import template_utils
from logic.gcommon.common_const.ui_battle_const import HP_TAIL_SLOW_TIME
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from common.utils.timer import CLOCK
from logic.client.const import game_mode_const

class HpInfoUIPC(HpInfoBaseUI):
    PANEL_CONFIG_NAME = 'battle\\hp_mp_pc'

    def leave_screen(self):
        super(HpInfoUIPC, self).leave_screen()
        global_data.ui_mgr.close_ui('HpInfoUIPC')