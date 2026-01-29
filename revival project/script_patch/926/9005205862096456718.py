# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComBallons.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const

class ComBallons(UnitCom):
    BIND_EVENT = {'G_DAMAGE': '_on_damage',
       'E_BALLON_HP': '_set_ballon_hp',
       'G_BALLON_COUNT': '_get_ballon_count',
       'G_BALLON': '_get_ballon'
       }

    def __init__(self):
        super(ComBallons, self).__init__()
        self._ballon_num = 0
        self._ballon_hp = 0
        self._ballon_dict = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBallons, self).init_from_dict(unit_obj, bdict)
        self._ballon_num = bdict.get('ballon_num', 0)
        self._ballon_hp = bdict.get('ballon_hp', 0)
        ballon_dict = bdict.get('ballon_dict', None)
        if ballon_dict is None:
            self._ballon_dict = {}
            for i in range(self._ballon_num):
                self._ballon_dict[i + 1] = self._ballon_hp

        else:
            self._ballon_dict = ballon_dict
        return

    def get_client_dict(self):
        return {'ballon_num': self._ballon_num,
           'ballon_hp': self._ballon_hp,
           'ballon_dict': self._ballon_dict
           }

    def _get_ballon_count(self):
        return len(self._ballon_dict)

    def _get_ballon(self):
        return self._ballon_dict

    def _on_damage(self, damage, ballon_idx):
        ret = 0
        if ballon_idx <= 0:
            for ballon_idx in six_ex.keys(self._ballon_dict):
                ret += self._do_damage(damage, ballon_idx)

        else:
            ret += self._do_damage(damage, ballon_idx)
        return ret

    def _do_damage(self, damage, ballon_idx):
        pre_ballon_hp = self._ballon_dict.get(ballon_idx, None)
        if pre_ballon_hp is None:
            return 0
        else:
            ballon_hp = max(0, pre_ballon_hp - damage)
            ret = pre_ballon_hp - ballon_hp
            self._set_ballon_hp(ballon_idx, ballon_hp)
            self.send_event('E_CALL_SYNC_METHOD', 'ballon_hp', (ballon_idx, ballon_hp))
            return ret

    def _set_ballon_hp(self, ballon_idx, hp):
        ballon_hp = self._ballon_dict.get(ballon_idx, None)
        if not ballon_hp:
            return
        else:
            if ballon_hp == hp:
                return
            ballon_hp = hp
            if ballon_hp > 0:
                self._ballon_dict[ballon_idx] = ballon_hp
            else:
                del self._ballon_dict[ballon_idx]
                self.send_event('E_BALLON_EXPLODE', ballon_idx, self._get_ballon_count())
            return