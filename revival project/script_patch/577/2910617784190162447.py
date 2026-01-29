# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComArmorClient.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from ...item import item_const as iconst
from logic.gcommon.item import item_utility as iutils
import logic.gcommon.const as const

class ComArmorClient(UnitCom):
    BIND_EVENT = {'E_CLOTHING_CHANGED': '_on_change',
       'E_WEAPON_SHIELD_GUN_LOAD': '_on_shield_gun_load',
       'E_WEAPON_SHIELD_GUN_UNLOAD': '_on_shield_gun_unload',
       'E_ARMOR_DO_DAMAGE': ('_do_armor_damage', -10),
       'E_SHIELD_RECOVER': '_on_armor_recover',
       'G_AMROR_BY_POS': '_get_armor_data',
       'G_COMPARE_ARMOR_LEVEL': '_compare_armor_level'
       }

    def __init__(self):
        super(ComArmorClient, self).__init__()
        self.mp_armors = {}

    def on_post_init_complete(self, bdict):
        super(ComArmorClient, self).on_post_init_complete(bdict)
        for key in bdict.get('armors', ()):
            if key not in self.mp_armors:
                self._on_change(key)

    def _on_shield_gun_load(self, wp_pos):
        wp_obj = self.ev_g_wpbar_get_by_pos(wp_pos)
        if not wp_obj:
            return
        self.do_change_armor(iconst.DRESS_POS_SHIELD, wp_obj.get_data())

    def _get_armor_data(self, pos=None):
        if not pos:
            return self.mp_armors
        else:
            return self.mp_armors.get(pos, None)

    def _on_shield_gun_unload(self, wp_pos):
        self.do_change_armor(iconst.DRESS_POS_SHIELD)

    def _on_change(self, put_pos):
        dict_data = self.ev_g_clothing_data_by_pos(put_pos)
        self.do_change_armor(put_pos, dict_data)

    def do_change_armor(self, put_pos, dict_data=None):
        if not dict_data:
            self.unload_armor(put_pos)
        elif iutils.is_armor(dict_data['item_id']):
            self.load_armor(put_pos, dict_data)
        else:
            return
        self.on_armor_data_changed(put_pos)

    def load_armor(self, pos, data):
        from logic.gcommon.ctypes.Armor import Armor
        obj_armor = Armor(data)
        self.mp_armors[pos] = obj_armor
        return obj_armor

    def unload_armor(self, pos):
        if pos in self.mp_armors:
            self.mp_armors.pop(pos)

    def _compare_armor_level(self, item_no):
        put_pos = iutils.get_clothing_dress_pos(item_no)
        armor = self.mp_armors.get(put_pos, None)
        if not armor:
            return True
        else:
            from common.cfg import confmgr
            conf = confmgr.get('item')
            old_level = conf.get(str(armor.get_item_id()), {}).get('level', 0)
            new_level = conf.get(str(item_no), {}).get('level', 0)
            return new_level > old_level

    def _do_armor_damage(self, pos, damage):
        if pos not in self.mp_armors:
            return
        obj_armor = self.mp_armors[pos]
        left = obj_armor.sub_dur(damage)
        if left <= 0:
            self.on_broken(pos, obj_armor)
        self.on_armor_data_changed(pos)

    def on_broken(self, pos, obj_armor):
        if pos == iconst.DRESS_POS_SHIELD:
            self.send_event('E_WEAPON_SHIELD_GUN_BROKEN')
        else:
            self.send_event('E_THROW_ITEM', const.BACKPACK_PART_CLOTHING, obj_armor.get_pos())

    def _on_armor_recover(self, info_dict):
        all_weapon = self.ev_g_wpbar_all_weapon()
        for pos, data in six.iteritems(info_dict):
            weapon = all_weapon.get(pos)
            if weapon:
                weapon.get_data().update(data)

        if global_data.cam_lplayer is self.unit_obj:
            ui = global_data.ui_mgr.get_ui('WeaponBarSelectUI')
            ui and ui.tick_armor_hp()

    def on_armor_data_changed(self, pos):
        armor = self._get_armor_data(pos)
        self.send_event('E_ARMOR_DATA_CHANGED', pos, armor)