# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BpLevelUpBaseUI.py
from __future__ import absolute_import
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
EXCEPT_HIDE_UI_LIST = []

class BpLevelUpBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    GLOBAL_EVENT = {'receive_award_succ_event': 'on_receive_award_event',
       'leave_get_model_display_ui': 'show_level_up',
       'receive_award_end_event': 'show_level_up',
       'close_season_buy_card_success': 'show_level_up'
       }
    UI_ACTION_EVENT = {'temp_btn_close.btn_common_big.OnClick': 'on_click_back_btn',
       'temp_btn_go.btn_common_big.OnClick': 'on_click_receive_btn'
       }

    def set_level(self, battle_pass_type, old_lv, new_lv):
        self.panel.nd_level.lab_level_before.SetString(str(old_lv))
        self.panel.nd_level.lab_level_now.SetString(str(new_lv))
        self.show_level_up()

    def on_init_panel(self):
        self.disappearing = False
        self.hide()
        self.panel.RecordAnimationNodeState('appear')

    def show_level_up(self):
        ui_receive = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        ui_display = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        ui_buy_card_success = global_data.ui_mgr.get_ui('BuyLoopCardSuccess')
        cond_1 = ui_receive and ui_receive.isPanelVisible()
        cond_2 = ui_receive and ui_receive.is_showing()
        cond_3 = ui_display and ui_display.is_showing_model_item()
        cond_4 = ui_buy_card_success
        if cond_1 or cond_2 or cond_3 or cond_4:
            self.hide()
            return
        self.clear_show_count_dict()
        self.panel.StopTimerAction()
        self.panel.StopAnimation('appear')
        self.panel.RecoverAnimationNodeState('appear')
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('appear')

    def on_receive_award_event(self, *args):
        self.hide()

    def on_click_receive_btn(self, *args):
        pass

    def on_click_back_btn(self, *args):
        self.close()