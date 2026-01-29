# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/privilege/PrivilegeWeekRewardUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL
from logic.gutils.template_utils import init_tempate_mall_i_item
from common.cfg import confmgr

class PrivilegeWeekRewardUI(BasePanel):
    PANEL_CONFIG_NAME = 'charge/bg_charge_weekly_rewards'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        super(PrivilegeWeekRewardUI, self).on_init_panel()
        self.init_btns()

    def init_privilege_week_reward(self, priv_lv, reward_id):
        frame_pic = PRIVILEGE_BAR_BADGE_FRAME[int(priv_lv)]
        level_pic = PRIVILEGE_BAR_BADGE_LEVEL[priv_lv]
        self.panel.bar_level.SetDisplayFrameByPath('', frame_pic)
        self.panel.img_num_level.SetDisplayFrameByPath('', level_pic)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        self.panel.list_rewards.SetInitCount(0)
        self.panel.list_rewards.SetInitCount(len(reward_list))
        for idx, item_info in enumerate(reward_list):
            ui_item = self.panel.list_rewards.GetItem(idx)
            item_no, item_num = item_info
            init_tempate_mall_i_item(ui_item.temp_item, item_no, item_num, show_tips=True, force_extra_ani=False)

    def init_btns(self):

        @self.panel.temp_btn.btn_common_big.unique_callback()
        def OnClick(*args):
            self.on_click_get_reward()

        @self.panel.btn_question.unique_callback()
        def OnClick(*args):
            self.on_click_question()

        self.panel.temp_btn.btn_common_big.SetText(860243)
        self.panel.lab_tips.SetString(610280)

    def on_click_get_reward(self, *args):
        if global_data.player:
            global_data.player.call_server_method('receive_privilege_week_reward')
        self.close()

    def on_click_question(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        title, content = (607171, 610281)
        dlg.set_show_rule(title, content)

    def close(self, *args):
        super(PrivilegeWeekRewardUI, self).close(*args)