# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAddFactorClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.cdata import human_attr_config
from logic.gcommon.cdata import mecha_attr_config
from logic.gutils.client_unit_tag_utils import preregistered_tags

class ComAddFactorClient(UnitCom):
    BIND_EVENT = {'G_ADD_ATTR': '_get_add_attr',
       'G_ADDITION_EFFECT': '_get_addition_effect',
       'E_MOD_ADD_ATTR': '_mod_add_attr',
       'E_CLEAR_ADD_FACTOR': '_clear_add_factor'
       }

    def __init__(self):
        super(ComAddFactorClient, self).__init__()
        self._mp_add_attr = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComAddFactorClient, self).init_from_dict(unit_obj, bdict)
        self._mp_add_attr = bdict.get('mp_add_attr', {})
        owner = self.unit_obj.get_owner()
        self._is_human = bool(owner.logic.MASK & preregistered_tags.HUMAN_TAG_VALUE)

    def _clear_add_factor(self):
        self._mp_add_attr = {}

    def _get_add_attr(self, attr, item_id=None, item_eid=None):
        result = self._mp_add_attr.get(attr, 0)
        if item_id is not None:
            result += self._mp_add_attr.get(item_id, {}).get(attr, 0)
        if item_eid is not None:
            result += self._mp_add_attr.get(item_eid, {}).get(attr, 0)
        if self._is_human:
            extremum = human_attr_config.get_attr_extremum(attr)
        else:
            extremum = mecha_attr_config.get_attr_extremum(attr)
        if extremum and abs(result) > abs(extremum):
            log_error('[%s-%s-%s] The absolute value of attr is larger than extremum, attr_name=%s, item_id=%s, value=%s, extrenum=%s]', self.unit_obj.get_owner().__class__.__name__, self.unit_obj.id, self.unit_obj.get_battle().id, attr, item_id, result, extremum)
            result = result / abs(result) * extremum
        return result

    def _get_addition_effect(self, init, item_id=None, key=None, add_attrs=None, factor_attrs=None):
        add_attrs = [] if add_attrs is None else add_attrs
        factor_attrs = [] if factor_attrs is None else factor_attrs
        add_value = 0
        if item_id and key is not None:
            default_factor_name = 'mul_{}'.format(key)
            default_add_name = 'add_{}'.format(key)
            if default_factor_name not in factor_attrs:
                factor_attrs.append(default_factor_name)
            if default_add_name not in add_attrs:
                add_attrs.append(default_add_name)
        for add_attr in add_attrs:
            add_value += self._get_add_attr(add_attr, item_id)

        add_factor = 0
        for factor_attr in factor_attrs:
            add_factor += self._get_add_attr(factor_attr, item_id)

        return init * (1 + add_factor) + add_value

    def _mod_add_attr(self, attr, mod, item_id=None, source_info=None, force_set=False):
        if item_id:
            self._mp_add_attr.setdefault(item_id, {})
            self._mp_add_attr[item_id].setdefault(attr, 0)
            pre_value = self._mp_add_attr[item_id][attr]
            if not force_set:
                self._mp_add_attr[item_id][attr] += mod
            else:
                self._mp_add_attr[item_id][attr] = mod
            cur_value = self._mp_add_attr[item_id][attr]
        else:
            self._mp_add_attr.setdefault(attr, 0)
            pre_value = self._mp_add_attr[attr]
            if not force_set:
                self._mp_add_attr[attr] += mod
            else:
                self._mp_add_attr[attr] = mod
            cur_value = self._mp_add_attr[attr]
        self.send_event('E_ADD_ATTR_CHANGED_%s' % attr, attr, item_id, pre_value, cur_value, source_info)