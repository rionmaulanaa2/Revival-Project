# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/ISkillBase.py
from __future__ import absolute_import
import cython

class ISkillBase(object):

    def destroy(self):
        pass

    def update_skill(self, data, trigger_update_event=True):
        pass

    def mod_skill(self, data, trigger_update_event=True):
        pass

    def get_skill_data(self, keys):
        pass

    def on_add(self):
        pass

    def on_remove(self):
        pass

    def check_cost_energy(self):
        pass

    def check_skill(self):
        pass

    def set_mp(self, mp):
        pass

    def get_mp(self):
        pass

    def on_temp_remove(self):
        pass

    def on_recover(self):
        pass

    def on_interrupt(self):
        pass

    def cal_dmg(self, entity, info):
        pass

    def mod_attr(self, key, mod):
        pass

    def get_attr_by_key(self, key, default=None):
        pass

    def hit_on_target(self):
        pass

    def tick(self, delta):
        pass

    def get_cost_fuel(self):
        pass

    def get_cost_fuel_pre(self):
        pass

    def get_cost_fuel_type(self):
        pass

    def mod_left_cnt(self, delta_times):
        pass

    def set_left_cnt(self, cnt):
        pass

    def mod_mp(self, mod):
        pass

    def has_spec_fuel(self):
        pass

    def on_add_attr_changed(self, attr, pre_value, cur_value):
        pass