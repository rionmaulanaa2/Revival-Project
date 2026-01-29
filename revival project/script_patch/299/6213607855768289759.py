# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/third_party_sdk_utils.py
from __future__ import absolute_import
import game3d

def check_need_show_naver_cafe():
    return False
    from logic.gcommon.common_const.lang_data import LANG_KO
    from logic.gcommon.common_utils.local_text import get_cur_text_lang
    if not global_data.feature_mgr.is_support_naver_cafe() or not global_data.enable_naver_cafe:
        return False
    if get_cur_text_lang() == LANG_KO and game3d.get_app_name() in ('com.netease.g93na',
                                                                    'com.163.itest.g93',
                                                                    'com.163.itest.dm87',
                                                                    'com.163.itest.dm87lxy'):
        return True
    return False