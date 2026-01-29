# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHitFlag.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from common.cfg import confmgr

class ComHitFlag(UnitCom):
    BIND_EVENT = {'E_HIT_FLAG_VALUE': '_set_hit_flag_value',
       'G_HIT_FLAG_VALUE': '_get_hit_flag_value',
       'G_HIT_FLAG_LEVEL': '_get_hit_flag_level',
       'G_HIT_FLAG_LEVEL_NUM': '_get_hit_flag_level_num'
       }

    def __init__(self):
        super(ComHitFlag, self).__init__(need_update=False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComHitFlag, self).init_from_dict(unit_obj, bdict)
        self._cur_value = bdict.get('hit_flag_value', {})
        self._cur_level = {}
        for flag_id in six.iterkeys(self._cur_value):
            self._check_hit_flag_level(flag_id, True)

    def destroy(self):
        super(ComHitFlag, self).destroy()

    def _set_hit_flag_value(self, flag_id, new_value):
        self._cur_value[flag_id] = new_value
        self._check_hit_flag_level(flag_id)

    def _get_hit_flag_value(self, flag_id):
        return self._cur_value.get(flag_id, 0)

    def _check_hit_flag_level(self, flag_id, is_init=False):
        level_list = confmgr.get('mecha_conf', 'HitFlagConfig', 'Content').get(str(flag_id), {}).get('level_list', [])
        for idx, value in enumerate(level_list):
            if self._cur_value.get(flag_id, 0) < value:
                new_level = idx
                if self._cur_level.get(flag_id, 0) != new_level:
                    self._cur_level[flag_id] = new_level
                    if not is_init:
                        self.send_event('E_HIT_FLAG_LEVEL_CHANGED', flag_id, new_level)
                break

    def _get_hit_flag_level(self, flag_id):
        return self._cur_level.get(flag_id, 0)

    def _get_hit_flag_level_num(self, flag_id):
        level_list = confmgr.get('mecha_conf', 'HitFlagConfig', 'Content').get(str(flag_id), {}).get('level_list', [])
        return len(level_list)