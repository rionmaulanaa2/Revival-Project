# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/aab_listener.py
from __future__ import absolute_import
from __future__ import print_function
import six.moves.builtins
from patch import patch_dctool
from .patch_utils import send_script_error
aab_package = True
try:
    import playassetdelivery
except ImportError:
    aab_package = False

error_codes_upload = []
if aab_package:
    FAILED_DL_STATUS = (playassetdelivery.SDK_DL_INFO_FAILED,
     playassetdelivery.SDK_DL_DOWNLOAD_FAILED)
else:
    FAILED_DL_STATUS = ()
if aab_package:
    NO_NEED_UP_ERRORS = (
     playassetdelivery.SDK_AP_INSUFFICIENT_STORAGE, playassetdelivery.SDK_AP_NETWORK_ERROR)
else:
    NO_NEED_UP_ERRORS = ()

def asset_pack_status_change_cb(name, state, download_status, sdk_error_code):
    try:
        aab_finish = six.moves.builtins.__dict__['aab_finish']
        print('aab st cb:', name, state, download_status, sdk_error_code, aab_finish)
        info_dict = {'aab_info': 'aab st cb:{0},{1},{2},{3},aab_finish:{4}'.format(name, state, download_status, sdk_error_code, aab_finish)}
        patch_dctool.get_dctool_instane().send_aab_stage_info(info_dict)
        if sdk_error_code != playassetdelivery.SDK_AP_NO_ERROR:
            if sdk_error_code not in error_codes_upload:
                error_codes_upload.append(sdk_error_code)
                if sdk_error_code not in NO_NEED_UP_ERRORS:
                    send_script_error('[aab] name:{},error:{},state:{},aab_finish:{}'.format(name, sdk_error_code, download_status, aab_finish))
    except:
        pass


def listen_aab():
    if aab_package:
        try:
            playassetdelivery.set_status_change_callback(asset_pack_status_change_cb)
        except:
            pass