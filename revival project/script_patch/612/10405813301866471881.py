# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGo.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.comsys.activity.widget import widget
from logic.client.const import mall_const
from logic.gutils.task_utils import get_children_task, get_task_conf_by_id
from logic.gutils.jump_to_ui_utils import jump_to_web_charge, jump_to_lottery
from logic.gutils.client_utils import post_ui_method
from logic.gutils.template_utils import quick_init_common_reward_list
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from logic.gutils.activity_utils import is_activity_in_limit_time

@widget('AsyncGoodsTaskListWidget', 'DescribeWidget')
class ActivityGo(ActivityBase):

    def set_show(self, show, is_init=False):
        super(ActivityGo, self).set_show(show, is_init)
        if show and not is_init:
            self.panel.PlayAnimation('show')
            self.panel.PlayAnimation('loop')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self._update_btn_buy
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityGo, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityGo, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self.process_event(True)
        fixed_task_id = conf.get('cTask', '')
        children_task_list = get_children_task(fixed_task_id)
        if not children_task_list:
            log_error('!!!ActivityGo: Invalid task id!!!')
            buy_reward = 0
        else:
            buy_reward = get_task_conf_by_id(str(children_task_list[0])).get('reward', 0)
        quick_init_common_reward_list(self.panel.list_reward_now, buy_reward)
        self._remind_text_id = ui_data.get('remind_text_id', 610076)
        self._remind_timestamp = ui_data.get('remind_timestamp', -1)
        self._game_goods_id = ui_data.get('game_goods_id', '')
        goods_list = getattr(mall_const, ui_data.get('goods_list', ''))
        if not goods_list:
            log_error('!!!!ActivityGo: Goods list name invalid!!!!')
        self._jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
        self.btn_buy = self.panel.btn_buy

        @self.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if not is_activity_in_limit_time(self._activity_type):
                global_data.game_mgr.show_tip(607911)
                return
            has_bought = limite_pay(self._game_goods_id)
            if has_bought:
                return

            def buy():
                if is_pc_global_pay():
                    jump_to_web_charge()
                elif self._jelly_goods_info:
                    global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

            from logic.gcommon.time_utility import get_server_time
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            cur_time = get_server_time()
            if cur_time > self._remind_timestamp > 0:
                sec_confirm_dlg = SecondConfirmDlg2()
                sec_confirm_dlg.confirm(content=self._remind_text_id, confirm_callback=buy)
            else:
                buy()

        self._update_btn_buy()
        self._lucky_house_id = ui_data.get('lucky_house_id', None)
        if self.panel.btn_lucky_house and self._lucky_house_id:

            @self.panel.btn_lucky_house.callback()
            def OnClick(btn, touch):
                jump_to_lottery(self._lucky_house_id)

        return

    @post_ui_method
    def _update_btn_buy(self):
        has_bought = limite_pay(self._game_goods_id)
        if not self._jelly_goods_info:
            self.btn_buy.SetEnable(False)
            self.btn_buy.SetText(12121)
        elif has_bought:
            self.btn_buy.SetEnable(False)
            self.btn_buy.setVisible(False)
            self.panel.img_get.setVisible(True)
            self.btn_buy.SetText(80836)
        else:
            self.btn_buy.SetEnable(True)
            if is_pc_global_pay() or is_steam_pay():
                price_txt = get_pc_charge_price_str(self._jelly_goods_info)
            else:
                price_txt = get_charge_price_str(self._jelly_goods_info['goodsid'])
            adjusted_price = adjust_price(str(price_txt))
            self.btn_buy.SetText(adjusted_price + ' ' + get_text_by_id(609817))
        global_data.emgr.refresh_activity_redpoint.emit()