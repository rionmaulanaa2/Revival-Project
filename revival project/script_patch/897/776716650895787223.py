# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/DailyRewardMainlandUI.py
from __future__ import absolute_import
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1

class DailyRewardMainlandUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/daily_reward_get'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'panel.OnClick': '_on_click_back_btn',
       'btn_get.OnClick': '_on_click_receive_btn',
       'btn_buy.OnClick': '_on_click_buy_month_card'
       }
    GLOBAL_EVENT = {'update_month_card_info': '_update_display'
       }

    def on_init_panel(self):
        self.disappearing = False
        self._show_list()
        self._init_reward()

    def _update_display(self):
        has_buy_yueka = global_data.player or False if 1 else global_data.player.has_yueka()
        if has_buy_yueka:
            self.panel.btn_buy.SetEnable(False)
            self.panel.btn_buy.SetText(12014)
            self.panel.temp_item.nd_daily.lab_num.SetString(str(16))

    def _on_click_buy_month_card(self, *args):
        from logic.gutils import jump_to_ui_utils
        from logic.gcommon.common_const.activity_const import ACTIVITY_YUEKA_NEW
        jump_to_ui_utils.jump_to_charge(ACTIVITY_YUEKA_NEW)
        self.close()

    def _on_click_receive_btn(self, *args):
        if global_data.player:
            global_data.player.try_get_battlepass_daily_reward()
            self.disappearing = True
            self.close()

    def _on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()

    def _init_reward(self):
        pass

    def _show_list(self):
        items = [{'text': 607404,'desc': 607423,'template': 'charge/i_month_item_9','init_func': self._init_yuan_bao_item}, {'text': 607413,'desc': 607420,'template': 'charge/i_month_item_1','loop': 'month_loop'}, {'text': 607471,'desc': 607473,'template': 'charge/i_month_item_8'}, {'text': 607414,'desc': 607422,'template': 'charge/i_month_item_3','loop': 'loop'}, {'text': 607415,'desc': 607424,'template': 'charge/i_month_item_5','tips': 607450}, {'text': 607416,'desc': 607425,'template': 'charge/i_month_item_6'}, {'text': 607417,'desc': 607438,'template': 'charge/i_month_item_7'}, {'text': 607419,'desc': 607423,'template': 'charge/i_month_item_4'}]

        def on_create_callback(lv, idx, item_widget):
            info = items[idx]
            reward_item = global_data.uisystem.load_template_create(info['template'], item_widget.temp_item)
            if 'loop' in info:
                reward_item.PlayAnimation(info['loop'])
            item_widget.PlayAnimation('show')
            item_widget.PlayAnimation('loop')
            item_widget.lab_common.SetString(info['text'])
            init_func = info.get('init_func', None)
            if init_func and callable(init_func):
                init_func(item_widget=reward_item)
            return

        self.panel.list_item.BindMethod('OnCreateItem', on_create_callback)
        self.panel.list_item.DeleteAllSubItem()
        self.panel.list_item.SetInitCount(len(items))

    def _init_yuan_bao_item(self, item_widget=None):
        from common.cfg import confmgr
        from logic.gcommon.common_const.activity_const import MONTHCARD_FIRST_BUY_REWARD, MONTHCARD_NOT_FIRST_BUY_REWARD
        buy_count = global_data.player.get_yueka_buy_count()
        if buy_count < 1:
            buy_reward_key = str(MONTHCARD_FIRST_BUY_REWARD)
        else:
            buy_reward_key = str(MONTHCARD_NOT_FIRST_BUY_REWARD)
        buy_reward_list = confmgr.get('common_reward_data', buy_reward_key, 'reward_list', default=[])
        reward_item_no, reward_num = buy_reward_list[0]
        reward_num = 300 + reward_num
        item_widget.lab_num.SetString(str(reward_num))

    def do_show_panel(self):
        super(DailyRewardMainlandUI, self).do_show_panel()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self._update_display()