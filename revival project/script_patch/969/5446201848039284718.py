# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/buff_utils.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.buff_const import SPEED_UP_TYPE_BASE, SPEED_UP_TYPE_MULTI, SPEED_UP_TYPE_COVER_BASE, SPEED_UP_TYPE_COVER_MULTI
MP_BUFF_SPD_TYPES = {'base': SPEED_UP_TYPE_BASE,
   'multi': SPEED_UP_TYPE_MULTI,
   'cover_base': SPEED_UP_TYPE_COVER_BASE,
   'cover_multi': SPEED_UP_TYPE_COVER_MULTI
   }

def cal_buff_speed(data):
    cover_base = 0
    cover_multi = None
    base = 0
    multi = 1
    for idx, tp in six.iteritems(data):
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
    return spd_scale