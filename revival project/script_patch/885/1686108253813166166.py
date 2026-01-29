# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/game_voice_utils.py
from __future__ import absolute_import
import six_ex

def is_use_skin(player, skin):
    if player.logic:
        if type(skin) not in (tuple, list):
            skin = [
             skin]
        fashion = six_ex.values(player.logic.ev_g_fashion())
        for s in skin:
            if int(s) in fashion:
                return True

    return False