# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/region_utils.py
from __future__ import absolute_import
import os
import game3d
REGION_SETTING_FILENAME = 'region_data'
REGION_SETTING_PATH = os.path.join(game3d.get_doc_dir(), REGION_SETTING_FILENAME)

def get_selected_region_code():
    try:
        f = open(REGION_SETTING_PATH, 'r')
        s = f.read()
        f.close()
        return int(s)
    except:
        return None

    return None


def save_selected_region_code(region_id):
    try:
        f = open(REGION_SETTING_PATH, 'w+')
        f.write(str(region_id))
        f.close()
    except:
        pass