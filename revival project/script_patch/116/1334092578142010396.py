# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_hit_hint/ComHitHintExplosive.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const

class ComHitHintExplosive(UnitCom):
    BIND_EVENT = {'G_HIT_HINT_BONE': 'get_hit_hint_bone'
       }

    def get_hit_hint_bone(self):
        return animation_const.BONE_BIPED_NAME