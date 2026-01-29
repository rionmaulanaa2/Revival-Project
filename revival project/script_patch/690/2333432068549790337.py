# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Magic/MagicRuneConfUIPC.py
from __future__ import absolute_import
from .MagicRuneConfUI import MagicRuneConfUI

class MagicRuneConfUIPC(MagicRuneConfUI):
    PANEL_CONFIG_NAME = 'battle_hunter/battle_hunter_choose_button_pc'
    HOT_KEY_FUNC_MAP_SHOW = {'toggle_moon_rune_list': {'node': 'nd_adjust_custom.temp_pc'}}