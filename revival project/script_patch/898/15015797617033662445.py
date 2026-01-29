# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombBattleDefines.py
from __future__ import absolute_import
POWER_CORE = 0
SPACE_CORE = 1
SPEED_CORE = 2
SPEED_CORE_ID = 6078
POWER_CORE_ID = 6076
SPACE_CORE_ID = 6077
POWER_CORE_ID_LST = [SPEED_CORE_ID, POWER_CORE_ID, SPACE_CORE_ID]
COLLECT_BTN_ICON = {POWER_CORE_ID: {'normal': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_2.png',
                   'disable': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_2_3.png'
                   },
   SPEED_CORE_ID: {'normal': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_1.png',
                   'disable': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_1_3.png'
                   },
   SPACE_CORE_ID: {'normal': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_3.png',
                   'disable': 'gui/ui_res_2/battle_bomb/icon_battle_bomb_core_3_3.png'
                   }
   }
CORE_CIRCLE_MAP_FRAME = {POWER_CORE_ID: 'gui/ui_res_2/battle/map/img_map_light_yellow.png',
   SPEED_CORE_ID: 'gui/ui_res_2/battle/map/img_map_light_green.png',
   SPACE_CORE_ID: 'gui/ui_res_2/battle/map/img_map_light_purple.png'
   }
GROUP_IDX_2_ICON = [
 'gui/ui_res_2/battle/icon/icon_teammate_num_blue.png',
 'gui/ui_res_2/battle/icon/icon_teammate_num_green.png',
 'gui/ui_res_2/battle/icon/icon_teammate_num_yellow.png']
NBOMB_NEWBIE_GUIDE_KEY = 'nbomb_newbie_guide'
NBOMB_CORE_LEN = 3
NBOMB_INSTALL_TOTAL_TIME = 5
CORE_ID_2_ICON = {SPEED_CORE_ID: 'gui/ui_res_2/battle/map/icon_map_bomb_1.png',
   POWER_CORE_ID: 'gui/ui_res_2/battle/map/icon_map_bomb_2.png',
   SPACE_CORE_ID: 'gui/ui_res_2/battle/map/icon_map_bomb_3.png'
   }
NBOMB_DEVICE_BLOOD_BLUE = 0
NBOMB_DEVICE_BLOOD_RED = 1