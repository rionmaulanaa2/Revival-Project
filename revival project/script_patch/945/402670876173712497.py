# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/button_custom_key_func.py
from __future__ import absolute_import

def convert_left_fire_custom_key(set_val):
    from logic.gcommon.common_const.ui_operation_const import LEFT_FIRE_ALWAYS_CLOSE
    main_sel, sub_sel = set_val
    if main_sel == LEFT_FIRE_ALWAYS_CLOSE:
        return str(main_sel)
    else:
        return str(main_sel) + '_' + str(sub_sel)