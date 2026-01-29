# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseBeginCountDown.py
from __future__ import absolute_import
from logic.comsys.battle.ffa.FFABeginCountDown import FFABeginCountDown

class ImproviseBeginCountDown(FFABeginCountDown):
    PANEL_CONFIG_NAME = 'battle_3v3/battle_begin_time_3v3'

    def _get_root_node(self):
        return self.panel.temp_count