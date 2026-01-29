# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/magic_mode_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
LESS_GRAVITY = 'less'
OVER_GRAVITY = 'over'

def get_region_model_path(type, region_level):
    region_model_dict = confmgr.get('script_gim_ref')['gravity_region_range']
    if type in region_model_dict:
        return region_model_dict[type].get(str(region_level))