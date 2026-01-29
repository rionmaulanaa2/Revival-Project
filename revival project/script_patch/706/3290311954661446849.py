# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLEDLightEffect.py
from __future__ import absolute_import
from . import ScenePart
RED_HIGHLIGHT = 1
RED_FLASH = 2
YELLOW_HIGHLIGHT = 3
YELLOW_FLASH = 4
GREEN_HIGHLIGHT = 5
GREEN_FLASH = 6
BLUE_HIGHLIGHT = 7

class PartLEDLightEffect(ScenePart.ScenePart):
    INIT_EVENT = {'battle_logic_ready_event': 'on_battle_begin',
       'settle_stage_event': 'on_battle_end',
       'hit_down_enemy': 'on_hit_down_enemy',
       'role_fashion_chagne': 'on_role_fashion_change',
       'i_am_dead': 'on_human_dead'
       }

    def __init__(self, scene, name):
        super(PartLEDLightEffect, self).__init__(scene, name, False)
        import device_compatibility
        if not device_compatibility.can_light_effect():
            self._unbind_event(self.INIT_EVENT)

    def on_battle_begin(self):
        import common.platform.uds_sdk.PerfSdkWrapper as P
        p = P.PerfSdkWrapper()
        p.light_effect(GREEN_FLASH, 10000)

    def on_battle_end(self, battle_tid, alive_fighter_num, settle_dict, *args):
        import common.platform.uds_sdk.PerfSdkWrapper as P
        p = P.PerfSdkWrapper()
        if settle_dict.get('rank', 3) == 1:
            p.light_effect(GREEN_HIGHLIGHT, 10000)
        else:
            p.light_effect(RED_FLASH, 10000)

    def on_hit_down_enemy(self):
        import common.platform.uds_sdk.PerfSdkWrapper as P
        p = P.PerfSdkWrapper()
        p.light_effect(YELLOW_HIGHLIGHT, 6000)

    def on_role_fashion_change(self, *args, **kwargs):
        import common.platform.uds_sdk.PerfSdkWrapper as P
        p = P.PerfSdkWrapper()
        p.light_effect(YELLOW_FLASH, 6000)

    def on_human_dead(self):
        import common.platform.uds_sdk.PerfSdkWrapper as P
        p = P.PerfSdkWrapper()
        p.light_effect(RED_FLASH, 6000)