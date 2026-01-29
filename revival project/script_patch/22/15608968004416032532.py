# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/WeaponBarConst.py
from __future__ import absolute_import
from logic.gcommon.ctypes.WpMelee import WpMelee
from logic.gcommon.ctypes.WpThrowable import WpThrowable
import logic.gcommon.const as const

class WeaponBarConst(object):
    POS_ARR = [
     const.PART_WEAPON_POS_MAIN1,
     const.PART_WEAPON_POS_MAIN2,
     const.PART_WEAPON_POS_MAIN3,
     const.PART_WEAPON_POS_MAIN4,
     const.PART_WEAPON_POS_MAIN5,
     const.PART_WEAPON_POS_MAIN6,
     const.PART_WEAPON_POS_MAIN_DF,
     const.PART_WEAPON_PVE_POS_MAIN,
     const.PART_WEAPON_PVE_POS_SECOND,
     const.PART_WEAPON_PVE_POS_SKILL,
     const.PART_WEAPON_PVE_POS_HITTED]
    if G_IS_CLIENT:
        from logic.gcommon.ctypes.WpGunClient import WpGunClient
        MP_CLS = {const.PART_WEAPON_POS_MAIN1: WpGunClient,
           const.PART_WEAPON_POS_MAIN2: WpGunClient,
           const.PART_WEAPON_POS_MAIN3: WpGunClient,
           const.PART_WEAPON_POS_MAIN4: WpGunClient,
           const.PART_WEAPON_POS_MAIN5: WpGunClient,
           const.PART_WEAPON_POS_MAIN6: WpGunClient,
           const.PART_WEAPON_POS_MAIN7: WpGunClient,
           const.PART_WEAPON_POS_MAIN8: WpGunClient,
           const.PART_WEAPON_POS_MAIN9: WpGunClient,
           const.PART_WEAPON_POS_MAIN_DF: WpGunClient,
           const.PART_WEAPON_POS_COLD: WpMelee,
           const.PART_WEAPON_POS_BOMB: WpThrowable,
           const.PART_WEAPON_POS_SIMU1: WpGunClient,
           const.PART_WEAPON_PVE_POS_MAIN: WpGunClient,
           const.PART_WEAPON_PVE_POS_SECOND: WpGunClient,
           const.PART_WEAPON_PVE_POS_SKILL: WpGunClient,
           const.PART_WEAPON_PVE_POS_HITTED: WpGunClient
           }
    else:
        from logic.gcommon.ctypes.WpGunServer import WpGunServer
        MP_CLS = {const.PART_WEAPON_POS_MAIN1: WpGunServer,
           const.PART_WEAPON_POS_MAIN2: WpGunServer,
           const.PART_WEAPON_POS_MAIN3: WpGunServer,
           const.PART_WEAPON_POS_MAIN4: WpGunServer,
           const.PART_WEAPON_POS_MAIN5: WpGunServer,
           const.PART_WEAPON_POS_MAIN6: WpGunServer,
           const.PART_WEAPON_POS_MAIN7: WpGunServer,
           const.PART_WEAPON_POS_MAIN8: WpGunServer,
           const.PART_WEAPON_POS_MAIN9: WpGunServer,
           const.PART_WEAPON_POS_MAIN_DF: WpGunServer,
           const.PART_WEAPON_POS_COLD: WpMelee,
           const.PART_WEAPON_POS_BOMB: WpThrowable,
           const.PART_WEAPON_POS_SIMU1: WpGunServer,
           const.PART_WEAPON_PVE_POS_MAIN: WpGunServer,
           const.PART_WEAPON_PVE_POS_SECOND: WpGunServer,
           const.PART_WEAPON_PVE_POS_SKILL: WpGunServer,
           const.PART_WEAPON_PVE_POS_HITTED: WpGunServer
           }