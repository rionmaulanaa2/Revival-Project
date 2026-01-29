# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/game_mode_utils.py
from __future__ import absolute_import

def get_custom_param_by_mode(conf=None, conf_key=None):
    if not conf:
        return 0
    if not global_data.game_mode:
        return conf.get(conf_key, 0)
    custom_param = conf.get('cCustomParam', {})
    mode_type = global_data.game_mode.get_mode_type()
    return custom_param.get(mode_type, {}).get(conf_key, conf.get(conf_key, 0))