# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAttributeClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.cdata import human_attr_config
from logic.gcommon.cdata import mecha_attr_config
from logic.gcommon.cdata import bond_gift_config
import logic.gcommon.common_const.animation_const as animation_const

class ComAttributeClient(UnitCom):
    BIND_EVENT = {'G_ATTR_GET': '_get_attr_by_key',
       'S_ATTR_SET': '_set_attr_by_key',
       'G_WEAPON_ATTR_GET': '_get_weapon_attr_by_key',
       'E_CLEAR_ATTR': '_clear_attr',
       'G_BASE_ATK_POWER': '_get_base_atk_power'
       }

    def __init__(self):
        super(ComAttributeClient, self).__init__()
        self.mp_attr = {}
        self._mp_tick_func = {}
        self._atk_power = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComAttributeClient, self).init_from_dict(unit_obj, bdict)
        self.mp_attr = bdict.get('mp_attr', {})
        self.mp_attr['item_num'] = bdict.get('item_num', 0)
        self.mp_attr['mileage'] = bdict.get('mileage', 0) / 10
        self._atk_power = bdict.get('atk_power', 0)

    def _clear_attr(self):
        self.mp_attr = {}

    def _get_attr_by_key(self, key, default=None):
        if key not in self.mp_attr:
            if self.sd.ref_is_mecha:
                init_val = mecha_attr_config.get_init_attr_val(key, default=default)
            else:
                init_val = human_attr_config.get_init_attr_val(key, default=default)
            return init_val
        return self.mp_attr[key]

    def _get_weapon_attr_by_key(self, itype, key, src_val):
        weapon_attr = self._get_attr_by_key('weapon_attr_{}'.format(itype), {})
        if not weapon_attr:
            return src_val
        if type(src_val) in [int, float]:
            return src_val * weapon_attr.get('mul_{}'.format(key), 1.0) + weapon_attr.get('add_{}'.format(key), 0.0)
        if key == 'firearm_res_custom':
            custom_res = weapon_attr.get(key, '')
            if custom_res:
                str_type, cId = custom_res.split('_')
                if str_type == 'gift':
                    gift_conf = bond_gift_config.GetBondGiftDataConfig().get(int(cId), {})
                    gift_extra_params = gift_conf.get('gift_extra_params', [])
                    if gift_extra_params:
                        return gift_extra_params
            return src_val
        return weapon_attr.get(key, src_val)

    def _set_attr_by_key(self, key, value, source_info=None):
        self.mp_attr[key] = value

    def _get_base_atk_power(self):
        return self._atk_power