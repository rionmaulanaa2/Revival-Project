# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothCampShopEntryUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.setting_ui.SimpleLabelUIBase import SimpleLabelUIBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.client.const.koth_shop_const import GOLD_PIC, DIAMOND_PIC
from common.const import uiconst

class KothCampShopEntryUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/mall_entry'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_mall.OnClick': 'on_click_btn_mall'}

    def on_init_panel(self):
        self._is_in_camp = False
        self.panel.RecordAnimationNodeState('tips')
        self.start_tick()

    def on_finalize_panel(self):
        pass

    def on_click_btn_mall(self, btn, touch):
        global_data.ui_mgr.show_ui('KothCampShopUI', 'logic.comsys.battle.King')
        from logic.comsys.battle.King.KothCampShopUI import KothCampShopUI
        KothCampShopUI()

    def start_tick(self):
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.in_camp_tick),
         cc.DelayTime.create(1)])))

    def in_camp_tick(self):
        if global_data.player and global_data.player.logic:
            pos = global_data.player.logic.ev_g_position()
            if global_data.king_battle_data:
                if global_data.king_battle_data.is_in_camp(pos, global_data.king_battle_data.my_camp_id):
                    self.on_enter_camp()
                    return
        self.on_leave_camp()

    def on_enter_camp(self):
        if self._is_in_camp:
            return
        self._is_in_camp = True
        self.panel.PlayAnimation('tips')

    def on_leave_camp(self):
        if not self._is_in_camp:
            return
        self._is_in_camp = False
        self.panel.StopAnimation('tips')
        self.panel.RecoverAnimationNodeState('tips')
        global_data.ui_mgr.close_ui('KothCampShopUI')