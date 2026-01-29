# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/__init__.py
from __future__ import absolute_import
import game3d

def is_win32():
    return game3d.get_platform() == game3d.PLATFORM_WIN32


def is_ios():
    return game3d.get_platform() == game3d.PLATFORM_IOS


def is_android():
    return game3d.get_platform() == game3d.PLATFORM_ANDROID