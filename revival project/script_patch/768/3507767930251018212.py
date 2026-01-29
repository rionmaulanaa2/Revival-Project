# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleMedCommonInfo.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import UI_TYPE_MESSAGE

class BattleMedCommonInfo(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_recruit/battle_recruit_tips'
    UI_TYPE = UI_TYPE_MESSAGE

    def process_one_message(self, message, finish_cb):
        self.main_process_one_message(message, finish_cb)