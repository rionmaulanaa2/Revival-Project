# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComMechaBindGun.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom

class ComMechaBindGun(UnitCom):
    BIND_EVENT = {'G_TRY_BIND_WEAPON_ATTACK_BEGIN': 'weapon_attack_begin',
       'G_TRY_BIND_WEAPON_ATTACK_END': 'weapon_attack_end',
       'E_SWITCH_BIND_WEAPON': 'switch_fire_pos',
       'E_ADD_BIND_GUNS': 'add_bind_guns'
       }

    def __init__(self):
        super(ComMechaBindGun, self).__init__()
        self.bind_guns_dict = {}
        self.last_fire_pos_dict = {}
        self.firing = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaBindGun, self).init_from_dict(unit_obj, bdict)
        shared_magazine_dict = bdict.get('shared_magazine_dict', {})
        if shared_magazine_dict:
            for magazine_idx, shared_magazine in six.iteritems(shared_magazine_dict):
                self.bind_guns_dict[magazine_idx] = shared_magazine.get('related_pos', {})

    def add_bind_guns(self, magazine_idx, bind_weapon_pos, weapon_pos):
        if magazine_idx in self.bind_guns_dict:
            if self.bind_guns_dict[magazine_idx]:
                if self.bind_guns_dict[magazine_idx][0] != bind_weapon_pos:
                    self.bind_guns_dict[magazine_idx][0] = bind_weapon_pos
            else:
                self.bind_guns_dict[magazine_idx] = [
                 bind_weapon_pos]
            if weapon_pos not in self.bind_guns_dict[magazine_idx]:
                self.bind_guns_dict[magazine_idx].append(weapon_pos)
        else:
            self.bind_guns_dict[magazine_idx] = [
             bind_weapon_pos, weapon_pos]

    def weapon_attack_begin(self, magazine_idx):
        if not self.bind_guns_dict or magazine_idx not in self.bind_guns_dict:
            return
        else:
            if not self.bind_guns_dict[magazine_idx]:
                return
            if self.last_fire_pos_dict.get(magazine_idx) is None:
                self.last_fire_pos_dict[magazine_idx] = self.bind_guns_dict[magazine_idx][0]
            self.firing = self.ev_g_try_weapon_attack_begin(self.last_fire_pos_dict[magazine_idx])
            return self.firing

    def weapon_attack_end(self, magazine_idx):
        end_result = False
        if self.last_fire_pos_dict.get(magazine_idx) is not None:
            end_result = self.ev_g_try_weapon_attack_end(self.last_fire_pos_dict[magazine_idx])
        self.firing = False
        return end_result

    def switch_fire_pos(self, magazine_idx, weapon_pos, is_sync=True):
        if magazine_idx not in self.bind_guns_dict:
            return
        if weapon_pos not in self.bind_guns_dict[magazine_idx]:
            return
        last_fire_pos = self.last_fire_pos_dict.get(magazine_idx)
        if last_fire_pos:
            if last_fire_pos == weapon_pos:
                return
            self.ev_g_try_weapon_attack_end(last_fire_pos)
            if is_sync:
                self.send_event('E_SYNC_WEAPON_TO_WEPAON', last_fire_pos, weapon_pos)
            self.last_fire_pos_dict[magazine_idx] = weapon_pos
            if self.firing:
                self.firing = self.ev_g_try_weapon_attack_begin(weapon_pos)
        else:
            self.last_fire_pos_dict[magazine_idx] = weapon_pos