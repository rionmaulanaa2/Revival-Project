# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillWeapon.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillWeapon(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillWeapon, self).__init__(skill_id, unit_obj, data)
        self._equiped = False

    def on_add(self):
        if not self._unit_obj.ev_g_in_mecha():
            self._unit_obj.send_event('E_EQUIP_OUT_ARMOR')
        self._equiped = True

    def on_remove(self):
        self._unit_obj.send_event('E_UNEQUIP_OUT_ARMOR')
        self._equiped = False

    def on_temp_remove(self):
        if self._equiped:
            self._unit_obj.send_event('E_UNEQUIP_OUT_ARMOR')

    def on_recover(self):
        if self._equiped:
            self._unit_obj.send_event('E_EQUIP_OUT_ARMOR')