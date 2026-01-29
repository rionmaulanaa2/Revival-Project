# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillRush.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillRush(SkillBase):

    def on_add(self):
        self._unit_obj.send_event('E_EQUIP_RUSH_BONE')

    def on_remove(self):
        self._unit_obj.send_event('E_UNEQUIP_RUSH_BONE')