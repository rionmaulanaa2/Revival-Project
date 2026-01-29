# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/version_utils.py
from __future__ import absolute_import
import version
CHANNEL_PACKAGE_INFO = {'bilibili_sdk': 'https://www.biligame.com/detail/?id=102024',
   'fanyou': 'https://dd.myapp.com/16891/apk/076BF71B8F072784C6F32BCF23B2452E.apk?fsname=com.tencent.tmgp.jddsaef_1.0.17646.apk'
   }

def get_integer_script_version():
    try:
        script_ver = int(version.get_script_version())
        return script_ver
    except Exception as e:
        log_error("Can't convert script version to integer", version.get_script_version())
        return 0


def get_integer_engine_version():
    try:
        engine_ver = int(version.get_engine_svn())
        return engine_ver
    except Exception as e:
        log_error("Can't convert engine version to integer", version.get_engine_svn())
        return 0


def open_package_update_web(channel_name):
    if channel_name not in CHANNEL_PACKAGE_INFO:
        return
    down_url = CHANNEL_PACKAGE_INFO[channel_name]
    import game3d
    game3d.open_url(down_url)