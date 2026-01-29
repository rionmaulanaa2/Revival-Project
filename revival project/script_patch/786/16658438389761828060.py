# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSpeedUp.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from logic.gcommon.common_const.buff_const import SPEED_UP_TYPE_BASE, SPEED_UP_TYPE_MULTI, SPEED_UP_TYPE_COVER_BASE, SPEED_UP_TYPE_COVER_MULTI
from logic.gcommon.common_const import attr_const
MP_BUFF_SPD_TYPES = {'base': SPEED_UP_TYPE_BASE,
   'multi': SPEED_UP_TYPE_MULTI,
   'cover_base': SPEED_UP_TYPE_COVER_BASE,
   'cover_multi': SPEED_UP_TYPE_COVER_MULTI
   }

class ComSpeedUp(UnitCom):
    BIND_EVENT = {'E_SPD_RATE_CHANGE': '_on_spd_rate_change',
       'E_SPD_ENABLE_BUFF_SCALE': '_set_enable_buff_spd',
       'E_BUFF_SPD_ADD': '_on_buff_speed_add',
       'E_BUFF_SPD_DEL': '_on_buff_speed_del',
       'E_NOTIFY_SPD_ATTR_CHANGE': '_on_notify_spd_attr_change',
       'E_BUFF_SPD_ADD_STANDALONE': '_on_buff_speed_add_standalone',
       'E_BUFF_SPD_DEL_STANDALONE': '_on_buff_speed_del_standalone',
       'G_SPEEDUP_SCALE': '_get_speed_scale',
       'E_BOARD_SKATE': 'on_board_skate',
       'E_LEAVE_SKATE': 'on_leave_skate',
       'G_SPEEDUP_SKILL_SCALE': '_get_skill_scale',
       'E_CHARACTER_ATTR': '_change_character_attr'
       }
    BIND_ATTR_CHANGE = {attr_const.ATTR_SPEED_UP_FACTOR: '_on_add_attr_changed'
       }

    def __init__(self):
        super(ComSpeedUp, self).__init__()
        self._attr_spped_up = 0
        self._buff_spd_scale = 0
        self._skill_scale = 1
        self._enable_buff_speed_up = True
        self._mp_speed_pool = {}
        self._mp_skill_scale_pool = {}
        self._spd_rate = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpeedUp, self).init_from_dict(unit_obj, bdict)
        self._attr_spped_up = 0
        self._spd_rate = 0
        self._buff_spd_scale = 0

    def on_post_init_complete(self, bdict):
        self._attr_spped_up += self.ev_g_add_attr(attr_const.ATTR_SPEED_UP_FACTOR)
        self._do_change_speed_up()

    def _change_character_attr(self, name, *arg):
        if name == 'dump_character':
            _speed_up = self._get_speed_scale()
            print('test--ComSpeedUp.dump_character--_speed_up =', _speed_up, '--_buff_spd_scale =', self._buff_spd_scale, '--_enable_buff_speed_up =', self._enable_buff_speed_up, '--_attr_spped_up =', self._attr_spped_up)

    def _set_enable_buff_spd(self, enable):
        if enable:
            self._enable_buff_speed_up = True
        else:
            self._enable_buff_speed_up = False
        self._do_change_speed_up()

    def _on_spd_rate_change(self, speed_up):
        self._spd_rate = speed_up
        self._do_change_speed_up()

    def _on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        self._attr_spped_up += cur_value - pre_value
        self._do_change_speed_up()

    def _on_notify_spd_attr_change(self, val):
        self._attr_spped_up += val

    def _get_speed_scale(self):
        return 1.0 + (self._buff_spd_scale if self._enable_buff_speed_up else 0) + self._attr_spped_up + self._spd_rate

    def _do_change_speed_up(self):
        _speed_up = self._get_speed_scale()
        self.send_event('E_SET_SPEED_SCALE', _speed_up)

    def _get_skill_scale(self):
        return self._skill_scale

    def _on_buff_speed_add(self, buff_id, buff_idx, spd_type, spd_val, data=None):
        if spd_type not in MP_BUFF_SPD_TYPES:
            log_error('[ComSpeedUp] adding speed error. spd_type not found: %s', spd_type)
            return
        self._mp_speed_pool[buff_idx] = (
         MP_BUFF_SPD_TYPES[spd_type], float(spd_val))
        if data and 'skill_scale' in data:
            self._add_skill_scale(buff_id, buff_idx, data['skill_scale'])
        self._cal_buff_speed()
        self._do_change_speed_up()

    def _on_buff_speed_del(self, buff_id, buff_idx):
        if buff_idx in self._mp_speed_pool:
            self._mp_speed_pool.pop(buff_idx)
        if buff_id in self._mp_skill_scale_pool:
            self._del_skill_scale(buff_id)
        self._cal_buff_speed()
        self._do_change_speed_up()

    def _cal_buff_speed(self):
        cover_base = 0
        cover_multi = None
        base = 0
        multi = 1
        for idx, tp in six.iteritems(self._mp_speed_pool):
            spd_type, spd_val = tp
            if spd_type == SPEED_UP_TYPE_BASE:
                base += spd_val
            elif spd_type == SPEED_UP_TYPE_MULTI:
                multi *= spd_val
            elif spd_type == SPEED_UP_TYPE_COVER_BASE:
                if not cover_base or spd_val < cover_base:
                    cover_base = spd_val
            elif spd_type == SPEED_UP_TYPE_COVER_MULTI:
                if cover_multi is None or spd_val < cover_multi:
                    cover_multi = spd_val

        spd_scale = (1 + base + cover_base) * multi * (1 if cover_multi is None else cover_multi) - 1
        spd_scale = min(spd_scale, 4)
        self._buff_spd_scale = spd_scale
        return

    def _on_buff_speed_add_standalone(self, buff_id, buff_data=None):
        if buff_data:
            extra_info = buff_data
        else:
            from common.cfg import confmgr
            conf = confmgr.get('c_buff_data', str(buff_id))
            if not conf:
                log_error('_on_buff_speed_add_standalone error 1 - invalid buff_id:%s', buff_id)
                return
            extra_info = conf.get('ExtInfo', {})
            if not extra_info or 'spd_type' not in extra_info or 'spd_val' not in extra_info:
                log_error('_on_buff_speed_add_standalone error 2 - invalid buff_id:%s', buff_id)
                return
        spd_type = extra_info['spd_type']
        spd_val = extra_info['spd_val']
        self._on_buff_speed_add(buff_id, 0, spd_type, spd_val)

    def _on_buff_speed_del_standalone(self, buff_id):
        self._on_buff_speed_del(buff_id, 0)

    def on_board_skate(self):
        self._set_enable_buff_spd(False)

    def on_leave_skate(self):
        self._set_enable_buff_spd(True)

    def _add_skill_scale(self, buff_id, buff_idx, skill_scale):
        if abs(skill_scale) > 1:
            log_error('_add_skill_scale error 1 - invalid buff_id:%s, skill_scale=%s', buff_id, skill_scale)
            return
        self._mp_skill_scale_pool[buff_id] = skill_scale
        self._cal_skill_scale()

    def _del_skill_scale(self, buff_id):
        if buff_id in self._mp_skill_scale_pool:
            self._mp_skill_scale_pool.pop(buff_id)
            self._cal_skill_scale()

    def _cal_skill_scale(self):
        base = 1
        for buff_id, val in six.iteritems(self._mp_skill_scale_pool):
            base += val

        base = max(0, base)
        self._skill_scale = base
        self.send_event('E_SPD_ON_SKILL_SCALE_CHANGE', self._skill_scale)