# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleMainCommonInfo.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.gcommon.common_const import battle_const
import cc

class BattleMainCommonInfo(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_tips_main'
    UI_TYPE = UI_TYPE_MESSAGE
    IGNORE_RESIZE_TYPE = set([
     battle_const.ZOMBIEFFA_MECHA_EXTINCTION])
    IGNORE_RESIZE_TYPE.update(BattleInfoMessage.IGNORE_RESIZE_TYPE)

    def process_one_message(self, message, finish_cb):

        def _finish_cb_func():
            global_data.emgr.fight_tips_finish_event.emit(message)
            finish_cb()

        self.main_process_one_message(message, _finish_cb_func)