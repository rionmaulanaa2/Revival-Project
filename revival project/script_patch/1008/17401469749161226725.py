# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/location/country.py
from __future__ import absolute_import

def get_country_code():
    import utilities
    if utilities.is_pc():
        return 'UNKNOW'
    import time
    import datetime
    v = time.strftime('%Z', time.localtime())
    gmt = int(time.timezone / -3600.0)
    return '{0}{1}'.format(v, gmt)


def is_china_area():
    import utilities
    import time
    s_code = get_country_code()
    if utilities.is_pc():
        return time.timezone == -28800
    return s_code == 'CST8'