# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/Weapon.py
from __future__ import absolute_import
from .BaseDataType import BaseDataType
from .RefBool import RefTrue

class Weapon(BaseDataType):

    def __init__(self, data):
        super(Weapon, self).__init__()
        self.iAtkMode = 0
        self.iPos = 0
        self._ext_set_default_skin(data)
        self._data = data
        self._conf = {}
        self._effective_conf = {}
        self._enable = RefTrue()
        self._equip_check_func = None
        self._open_shield_check_func = None
        return

    def _ext_set_default_skin(self, data):
        if not G_IS_CLIENT:
            return
        from ext_package.ext_decorator import has_skin_ext
        if not has_skin_ext() and 'fashion' in data and 'item_id':
            from logic.gutils.dress_utils import get_weapon_default_fashion
            default_fashion = get_weapon_default_fashion(data['item_id'])
            if default_fashion:
                data['fashion'] = {0: default_fashion}

    def init_equip_func(self):
        from logic.gcommon.common_utils import weapon_utils
        equip_cond = self.conf('iEquipCondition', 0)
        if equip_cond:
            self._equip_check_func = weapon_utils.get_equip_check_func(equip_cond)
        if self.check_shield_owned():
            self._open_shield_check_func = weapon_utils.check_can_open_shield

    def switch_wp_mode(self, *args):
        return False

    def set_player_attr(self, player_attr):
        pass

    def reload(self, ammo_num):
        pass

    def get_attachment_attr(self, pos):
        pass

    def get_config(self, *args):
        return {}

    def get_effective_config(self):
        return self._effective_conf

    def reset_config(self):
        self._conf = {}

    def get_key_config_value(self, key, default=None, weapon_id=None):
        if weapon_id is not None:
            conf = self.get_config(weapon_id)
        else:
            conf = self.get_config()
        if not conf:
            return default
        else:
            return conf.get(key, default)

    def set_key_config_value(self, key, value):
        conf = self.get_config()
        if not conf:
            return
        conf[key] = value

    def conf(self, key, default=None):
        return self.get_key_config_value(key, default)

    def set_enable(self, enable):
        self._enable.enable(enable)

    def is_enable(self):
        return bool(self._enable)

    def get_effective_value(self, key, default=None):
        if key in self._effective_conf:
            return self._effective_conf[key]
        value = self.get_key_config_value(key, default)
        self._effective_conf[key] = value
        return value

    def set_multi_mode(self, enable):
        if self.get_multi_kind():
            self._data['is_multi_mode'] = enable
            return True
        return False

    def is_multi_mode(self):
        return self._data.get('is_multi_mode', False)

    def get_kind(self):
        return 0

    def is_multi_wp(self):
        if self.conf('multiMode', None):
            return True
        else:
            return False

    def get_multi_kind(self):
        multiMode = self.conf('multiMode', None)
        if multiMode:
            return multiMode[0]
        else:
            return 0

    def get_multi_item_id(self):
        multiMode = self.conf('multiMode', None)
        if multiMode:
            return multiMode[1]
        else:
            return

    def get_item_id(self):
        return self._data.get('item_id', -1)

    def get_fashion(self):
        return self._data.get('fashion', {})

    def get_atk_mode(self):
        return self.iAtkMode

    def set_pos(self, iPos):
        self.iPos = iPos
        self._data['wp_pos'] = iPos

    def get_pos(self):
        return self.iPos

    def get_data(self):
        return self._data

    def get_entity_id(self):
        return self._data.get('entity_id')

    def check_kind(self, *i_kind):
        if self.get_effective_value('iKind') in i_kind:
            return True
        else:
            multiMode = self.get_effective_value('multiMode', None)
            if multiMode:
                return multiMode[0] in i_kind
            return False

    def check_shield_owned(self):
        return bool(self.get_effective_value('iShieldOpenCondition'))

    def check_can_equip(self):
        if self._equip_check_func:
            return self._equip_check_func(self)
        return True

    def check_can_open_shield(self):
        if self._open_shield_check_func:
            return self._open_shield_check_func(self)
        return True

    def destroy(self):
        self._equip_check_func = None
        self._open_shield_check_func = None
        return