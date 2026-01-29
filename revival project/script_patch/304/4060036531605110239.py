# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/device_utils.py
from __future__ import absolute_import
import game3d

def check_vivo_device():
    di = global_data.deviceinfo
    if di:
        tag = di.get_device_manufacturer()
        if tag == 'vivo':
            return True
    return False


def check_ipad():
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        di = global_data.deviceinfo
        if di:
            tag = di.get_device_model_name()
            if isinstance(tag, str) and 'ipad' in tag.lower():
                return True
            device_model = di.get_device_model()
            if isinstance(device_model, str) and 'ipad' in device_model.lower():
                return True
    return False