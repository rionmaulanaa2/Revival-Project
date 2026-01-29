# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/armor_utils.py
from __future__ import absolute_import
from common.cfg import confmgr

def get_armor_level(armor_no):
    return confmgr.get('armor_config', str(armor_no), 'iLevel')


def get_armor_max_shield(armor_no):
    return confmgr.get('armor_config', str(armor_no), 'iMaxShield')


def get_armor_shield_speed(armor_no):
    return confmgr.get('armor_config', str(armor_no), 'iShieldSpeed')