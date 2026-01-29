# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaWeaponBarClient.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gcommon.const import PART_WEAPON_POS_NONE, PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from logic.gcommon.ctypes.WeaponBarConst import WeaponBarConst

class ComMechaWeaponBarClient(UnitCom, WeaponBarConst):
    BIND_EVENT = {'G_WEAPON_DATA': '_get_weapon_data',
       'G_WPBAR_GET_BY_POS': 'get_weapon_by_pos',
       'G_WPBAR_CUR_WEAPON': '_get_cur_weapon',
       'G_WPBAR_ALL_WEAPON': '_get_all_weapons_in_bar',
       'G_BULLET_NUM': '_get_bullet_num',
       'E_SWITCHING': ('_switch_cur_weapon', 10),
       'G_WPBAR_CUR_WEAPON_POS': '_get_cur_weapon_pos',
       'G_ATTACHMENT_ATTR': '_get_attachment_attr',
       'E_WEAPON_BULLET_CHG': 'weapon_bullet_change',
       'E_WEAPON_BULLET_MAX_CHG': 'weapon_bullet_max_change',
       'E_PICK_UP_WEAPON': 'pick_up_weapon',
       'G_BIND_WEAPON_CUR_POS': '_get_bind_weapon_cur_pos',
       'E_SWITCH_BIND_WEAPON_CUR_POS': '_switch_bind_weapon_cur_pos'
       }

    def __init__(self):
        super(ComMechaWeaponBarClient, self).__init__()
        self._cur_pos = PART_WEAPON_POS_MAIN1
        self.sd.ref_wp_bar_cur_weapon = None
        self._weapons = {}
        self._shared_magazine_dict = None
        self.mp_weapons = {}
        self.sd.ref_wp_bar_mp_weapons = self.mp_weapons
        self._bind_weapon_cur_pos_dict = None
        return

    @property
    def cur_pos(self):
        return self._cur_pos

    @cur_pos.setter
    def cur_pos(self, value):
        self._cur_pos = value
        self.sd.ref_wp_bar_cur_pos = value
        self.sd.ref_wp_bar_cur_weapon = self.mp_weapons.get(value)

    def destroy(self):
        self.sd.ref_wp_bar_cur_pos = None
        for wp in six.itervalues(self.mp_weapons):
            wp and wp.destroy()

        self.mp_weapons = {}
        self.sd.ref_wp_bar_mp_weapons = {}
        self._weapons = {}
        self._shared_magazine_dict = None
        self._bind_weapon_cur_pos_dict = None
        super(ComMechaWeaponBarClient, self).destroy()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaWeaponBarClient, self).init_from_dict(unit_obj, bdict)
        self.cur_pos = bdict.get('wp_bar_cur_pos', PART_WEAPON_POS_MAIN1)
        self._weapons = bdict.get('weapons', {})
        self._shared_magazine_dict = bdict.get('shared_magazine_dict', None)
        self._bind_weapon_cur_pos_dict = bdict.get('bind_weapon_cur_pos_dict', None)
        self.sd.ref_wp_bar_mp_weapons = self.mp_weapons
        return

    def on_init_complete(self):
        self.init_obj()
        self.send_event('E_WPBAR_INIT')

    def init_obj(self):
        for wp_pos, wp_data in six.iteritems(self._weapons):
            self.load_weapon_obj(wp_pos, wp_data)

        if self._shared_magazine_dict:
            for magazine_idx, shared_magazine in six.iteritems(self._shared_magazine_dict):
                for pos in shared_magazine.get('related_pos', ()):
                    wp = self.mp_weapons[pos]
                    wp.set_magazine(shared_magazine)

    def load_weapon_obj(self, wp_pos, wp_data):
        from logic.gcommon.ctypes.WpGunClient import WpGunClient
        if not wp_data:
            return
        else:
            clss = self.MP_CLS.get(wp_pos, WpGunClient)
            if not clss:
                return
            wp_obj = clss(wp_data)
            wp_obj.set_pos(wp_pos)
            wp_obj.set_host_player(self)
            original_wp_obj = self.mp_weapons.get(wp_pos, None)
            if original_wp_obj:
                wp_obj.transfer_weapon(original_wp_obj)
                original_wp_obj.destroy()
            self.mp_weapons[wp_pos] = wp_obj
            self.sd.ref_wp_bar_cur_weapon = self.mp_weapons.get(self.cur_pos)
            return

    def _get_cur_weapon(self):
        return self.get_weapon_by_pos(self.cur_pos)

    def _get_bullet_num(self):
        if self.cur_pos in [PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3]:
            weapon = self._get_cur_weapon()
            if weapon:
                return weapon.get_bullet_num()
        return 0

    def _get_cur_weapon_pos(self):
        return self.cur_pos

    def get_weapon_by_pos(self, wp_pos):
        return self.mp_weapons.get(wp_pos, None)

    def _get_all_weapons_in_bar(self):
        return self.mp_weapons

    def _get_weapon_data(self, weapon_pos):
        return self._weapons.get(weapon_pos, None)

    def _get_attachment_attr(self, pos):
        if self.cur_pos in self.mp_weapons:
            weapon = self._get_cur_weapon()
            if weapon:
                return weapon.get_attachment_attr(pos)
        return None

    def _switch_cur_weapon(self, pos):
        self.cur_pos = pos

    def pick_up_weapon(self, item_data, wp_pos, switch=True):
        if wp_pos <= 0:
            return
        else:
            old_wp_data = self._weapons.get(wp_pos, None)
            if old_wp_data and old_wp_data.get('item_id', 0) == item_data.get('item_id', 0):
                return
            change_weapon = True if old_wp_data else False
            self._weapons[wp_pos] = item_data
            self.load_weapon_obj(wp_pos, item_data)
            self.send_event('E_WEAPON_DATA_CHANGED_SUCCESS', wp_pos)
            self.send_event('E_WEAPON_DATA_CHANGED', wp_pos)
            if change_weapon:
                self.send_event('E_WEAPON_CHANGED', wp_pos)
            return

    def weapon_bullet_max_change(self, weapon_pos, cur_bullet_max_cnt):
        wp = self.mp_weapons.get(weapon_pos)
        if not wp:
            return
        wp.set_bullet_cap(cur_bullet_max_cnt)
        pos_list = wp.get_related_weapon_pos() or (weapon_pos,)
        for pos in pos_list:
            self.send_event('E_WEAPON_DATA_CHANGED', pos)

    def weapon_bullet_change(self, weapon_pos, cur_bullet_cnt):
        wp = self.mp_weapons.get(weapon_pos)
        if not wp:
            return
        wp.set_bullet_num(cur_bullet_cnt)
        pos_list = wp.get_related_weapon_pos() or (weapon_pos,)
        for pos in pos_list:
            self.send_event('E_WEAPON_DATA_CHANGED', pos)

        self.send_event('E_CUR_BULLET_NUM_CHG', pos_list)

    def _get_bind_weapon_cur_pos(self, magazine_idx):
        if not self._shared_magazine_dict:
            return None
        else:
            return self._bind_weapon_cur_pos_dict.get(magazine_idx)

    def _switch_bind_weapon_cur_pos(self, magazine_idx, pos):
        if not self._shared_magazine_dict or magazine_idx not in self._shared_magazine_dict:
            return
        if magazine_idx not in self._bind_weapon_cur_pos_dict:
            return
        if pos not in self.mp_weapons:
            return
        cur_pos = self._bind_weapon_cur_pos_dict[magazine_idx]
        if cur_pos != pos:
            self._bind_weapon_cur_pos_dict[magazine_idx] = pos
            self.send_event('E_CALL_SYNC_METHOD', 'switch_bind_weapon_cur_pos', (magazine_idx, pos), True)