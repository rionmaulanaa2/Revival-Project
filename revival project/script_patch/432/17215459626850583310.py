# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_const.py
from __future__ import absolute_import
import game3d
IS_RELEASE = game3d.is_release_version()
CHUNK_SIZE = 10240
CONNECT_TIMEOUT = 15.0
DOWNLOAD_TIMEOUT = 15.0
ENABLE_ZIP_DOWNLOAD = True
ENABLE_ZIP_RANGE_DOWNLOWD = False
RANGE_ERROR_COUNT = 0
ENABLE_DOWNLOAD_DRPF_UP = True
PACKAGE_DRPF_UP_TIME = 10
ENABLE_A_B_SERVER_CHANGE = False
SUPPORT_BASE_PACKAGE_PLATFORMS = (
 game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS)
ENABLE_CHECK_WEEK_AND_PATCH = True
ENABLE_CHECK_EXT_NAME = True
ENABLE_CHECK_SCRIPT_PKG_CRC = True
ENABLE_CHECK_NPK_FLIST = True
SPACE_UP_TIME = 3
ENABLE_PATCH_NPK = game3d.is_feature_ready('PATCH_NPK_MERGE')
ENABLE_LOCAL_FLIST = ENABLE_PATCH_NPK
ENABLE_VERIFY_PATCH_NPK = True
ENABLE_CHECK_BASE_NPK = True
ENABLE_PATCH_VIDEO = True
ENABLE_PATCH_ANNOUNCE = True
PATCH_VIDEO_NAME = 'video/intro_fight.mp4'