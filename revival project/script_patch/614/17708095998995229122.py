# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/charm_data.py
_reload_all = True
from logic.gcommon.item import lobby_item_type as litem_type
data = {litem_type.L_ITEM_TYPE_MECHA_SKIN: {2: 20,
                                       3: 30,
                                       4: 50,
                                       5: 120,
                                       6: 90,
                                       7: 130
                                       },
   litem_type.L_ITME_TYPE_GUNSKIN: {2: 10,
                                    3: 20,
                                    4: 30
                                    },
   litem_type.L_ITEM_TYPE_WEAPON_SFX: {5: 200,
                                       7: 210
                                       },
   litem_type.L_ITEM_TYPE_PET_SKIN: {3: 30,
                                     4: 50,
                                     5: 120,
                                     6: 90
                                     },
   litem_type.L_ITEM_TYPE_ROLE_SKIN: {2: 20,
                                      3: 30,
                                      4: 50,
                                      5: 120,
                                      6: 90
                                      },
   litem_type.L_ITEM_YTPE_VEHICLE_SKIN: {2: 10,
                                         3: 20,
                                         4: 30,
                                         6: 40
                                         }
   }

def get_charm(item_type, degree):
    return data.get(item_type, {}).get(degree, 0)