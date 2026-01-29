# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NeutralShopBattle/BattleAceCoinUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER_1
from logic.gcommon.cdata import driver_lv_data
from logic.gcommon.common_const import battle_const
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.const import uiconst

class BattleAceCoinUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_s4_shop/fight_ace_coin'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'update_shop_entity_ace_coins_event': 'on_update_shop_entity_ace_coins'
       }

    def on_init_panel(self, *args, **kwargs):
        self.update_ace_coin()
        self.init_custom_com()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def update_ace_coin(self):
        self.panel.lab_coin.SetString(str(self.get_coin()))

    def get_coin(self):
        if not global_data.neutral_shop_battle_data:
            return 0
        if not global_data.cam_lplayer:
            return 0
        return global_data.neutral_shop_battle_data.get_entity_ace_coins(global_data.cam_lplayer.id)

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')

    def on_update_shop_entity_ace_coins(self, entity_id, money):
        if not global_data.cam_lplayer:
            return
        if entity_id == global_data.cam_lplayer.id:
            self.update_ace_coin()