# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComSpd.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const
from ...cdata import status_config
import logic.gcommon.const as const
from logic.gcommon.common_const import attr_const

class ComSpd(UnitCom):
    NON_FILTER = {'have_gun_shoot': 26,
       'squat_shoot': 18.72,
       'crawl_shoot': 18.72,
       'crawl_walk': 31.2
       }
    BIND_EVENT = {'G_FILTER_SPD': '_get_cur_spd_by_key',
       'E_WEAPON_DATA_CHANGED': '_on_weapon_changed',
       'E_WPBAR_INIT': '_on_weapon_init',
       'E_WPBAR_SWITCH_CUR': '_on_weapon_switch',
       'E_THROW_ITEM': '_on_throw_item',
       'E_START_SUPER_JUMP': '_on_super_jump',
       'E_LEAVE_STATE': '_on_leave_states',
       'E_WATER_EVENT': '_on_swim'
       }

    def __init__(self):
        super(ComSpd, self).__init__()
        self._debuff = 0
        self._super_jump_spd = 0
        self._in_super_jump = False
        self.init()

    def init(self):
        pass

    def reset(self):
        self._debuff = 0

    def _get_cur_spd_by_key(self, spd_key, origin):
        from ...cdata import speed_physic_arg
        spd = 0
        if self._in_super_jump and self.ev_g_is_jump():
            spd = self._super_jump_spd
        else:
            old_origin = getattr(speed_physic_arg, spd_key, 20)
            if not origin:
                origin = old_origin
            debuf = self._debuff
            if self.ev_g_get_state(status_config.ST_SHOOT):
                obj_wp = self.ev_g_wpbar_cur_weapon()
                debuf += self.get_debuff_by_wp(obj_wp)
            spd = (1.0 - debuf) * origin
        return spd

    def _on_throw_item(self, part, key):
        if part != const.BACKPACK_PART_WEAPON:
            return
        self._on_weapon_changed(0)

    def _on_weapon_init(self, _=None):
        self._on_weapon_changed(0)

    def _on_weapon_switch(self, _=None):
        self._on_weapon_changed(0)

    def _on_weapon_changed(self, _):
        self._debuff = 0

    def get_debuff_by_wp(self, obj_wp):
        if not obj_wp:
            return 0
        fSpdDebuff = obj_wp.get_effective_value('fSpdDebuff')
        fSpdDebuff *= 1 - self.ev_g_add_attr(attr_const.MECHA_ATTR_FIRE_SPD_DEBUFF_REDUCE_FACTOR)
        if not fSpdDebuff:
            return 0
        return fSpdDebuff

    def _on_super_jump(self, spd):
        self._super_jump_spd = spd
        self._in_super_jump = True

    def _on_leave_states(self, leave_state, new_state=None):
        if not self._in_super_jump:
            return
        if leave_state == status_config.ST_JUMP_3:
            self._super_jump_spd = 0
            self._in_super_jump = False

    def _on_swim(self, water_status, water_height=None):
        import logic.gcommon.common_const.water_const as water_const
        if water_status != water_const.WATER_NONE and self._in_super_jump:
            self._super_jump_spd = 0
            self._in_super_jump = False

    def destroy(self):
        super(ComSpd, self).destroy()