# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComBuffData.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from collections import defaultdict

class ComBuffData(UnitCom):
    BIND_EVENT = {'E_BUFF_ADD_DATA': 'add_data',
       'E_BUFF_ACT_DATA': 'act_data',
       'E_BUFF_DEL_DATA': 'del_data',
       'G_GET_BUFF_DATA': 'get_data',
       'G_GET_BUFF_VAL_BY_FIELD': 'get_buff_val_by_field',
       'G_GET_BUFF': 'get_buff',
       'G_GET_BUFF_CNT': 'get_buff_cnt',
       'G_GET_BUFF_INFO': 'get_buff_info',
       'G_HAS_BUFF': 'has_buff',
       'E_INC_BUFF_EFFECT': 'inc_buff_effect',
       'E_DEC_BUFF_EFFECT': 'dec_buff_effect',
       'G_HAS_BUFF_EFFECT': 'has_buff_effect'
       }

    def __init__(self):
        super(ComBuffData, self).__init__()
        self._data = None
        self.effect_execution = None
        self.effect_immune = defaultdict(int)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBuffData, self).init_from_dict(unit_obj, bdict)
        self._data = bdict.get('buff_data', {})

    def get_client_dict(self):
        if self._data:
            return {'buff_data': self._data}

    def add_data(self, buff_key, buff_id, buff_idx, data):
        self._data.setdefault(buff_key, {})
        self._data[buff_key].setdefault(buff_id, {})
        self._data[buff_key][buff_id][buff_idx] = data

    def act_data(self, buff_key, buff_id, buff_idx, data):
        buff_data = self.get_buff_info(buff_key, buff_id, buff_idx)
        if buff_data:
            buff_data.update(data)

    def del_data(self, buff_key, buff_id, buff_idx):
        try:
            del self._data[buff_key][buff_id][buff_idx]
        except:
            pass

    def get_data(self):
        return self._data

    def get_buff_val_by_field(self, _buff_id, field):
        ret_val = 0
        for buff_key, buff_info in six.iteritems(self._data):
            for buff_id, buff_data in six.iteritems(buff_info):
                if _buff_id != buff_id:
                    continue
                for buff_idx, data in six.iteritems(buff_data):
                    ret_val += data.get(field, 0)

        if ret_val is None:
            ret_val = 0
        return ret_val

    def get_buff(self, buff_key, buff_id):
        return self._data.get(buff_key, {}).get(buff_id, {})

    def get_buff_cnt(self, buff_key, buff_id):
        return len(self.get_buff(buff_key, buff_id))

    def get_buff_info(self, buff_key, buff_id, buff_idx):
        return self._data.get(buff_key, {}).get(buff_id, {}).get(buff_idx, None)

    def has_buff(self, buff_key, buff_id, buff_idx):
        return buff_idx in self._data.get(buff_key, {}).get(buff_id, {})

    def clear_data(self, *arg):
        if self._data:
            self._data.clear()

    def add_buff_effect(self, effect_name, effect_value):
        setattr(self, effect_name, effect_value)

    def del_buff_effect(self, effect_name):
        setattr(self, effect_name, None)
        return

    def get_buff_effect(self, effect_name):
        return getattr(self, effect_name, None)

    def inc_buff_effect(self, effect_name, effect_value):
        effect = getattr(self, effect_name, None)
        if effect is None:
            return
        else:
            for value in effect_value:
                effect[value] += 1

            return

    def dec_buff_effect(self, effect_name, effect_value):
        effect = getattr(self, effect_name, None)
        if not effect:
            return
        else:
            for value in effect_value:
                effect[value] -= 1

            return

    def has_buff_effect(self, effect_name, effect_value):
        effect = getattr(self, effect_name, None)
        return effect and effect.get(effect_value) > 0

    def destroy(self):
        self.clear_data()
        super(ComBuffData, self).destroy()