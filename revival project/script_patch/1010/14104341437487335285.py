# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerBuy.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils.activity_utils import get_left_time, is_activity_in_limit_time
from logic.gutils.template_utils import show_left_time, init_common_reward_list
from logic.gutils.mall_utils import is_pc_global_pay, get_goods_item_no, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from common.cfg import confmgr
from logic.gutils.task_utils import get_task_name, get_prog_rewards_in_dict, get_task_conf_by_id
ORIGIN_PRICE = 6

class ActivitySummerBuy(ActivityBase):
    SEC_CONFIRM_TIMESTAMP = 1628265599

    def __init__(self, dlg, activity_type):
        super(ActivitySummerBuy, self).__init__(dlg, activity_type)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.init_parameters()
        self.process_events(True)

    def init_parameters(self):
        self._game_goods_id = '694000011'
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.task_id = conf.get('cTask', '')
        self.desc_text_id = int(conf.get('cRuleTextID', 0))
        task_conf = get_task_conf_by_id(str(self.task_id))
        children_task_list = task_conf.get('children_task', [])
        self.buy_reward = get_task_conf_by_id(str(children_task_list[0])).get('reward', 0)
        self.prog_2_task_id = {}
        self.prog_2_reward_id = {}
        for prog, task_id in enumerate(children_task_list):
            self.prog_2_task_id[prog] = task_id
            if prog == 0:
                continue
            self.prog_2_reward_id[prog] = get_task_conf_by_id(str(task_id)).get('reward', 0)

        self._jelly_goods_info = global_data.lobby_mall_data.get_summer_go_sale_info()
        self.btn_buy = self.panel.temp_buy.temp_btn_get.btn_common

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'buy_good_success': self._update_goods_show
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def upload_sa_log(self):
        from logic.gutils.ui_salog_utils import add_uiclick_salog_lobby
        add_uiclick_salog_lobby('open_activity_summer_buy')

    def on_init_panel(self):
        super(ActivitySummerBuy, self).on_init_panel()
        self.upload_sa_log()
        init_common_reward_list(self.panel.temp_buy.list_reward, self.buy_reward)
        self.panel.img_mila.setVisible(not global_data.feature_mgr.is_support_spine_3_8())

        @self.panel.btn_button.callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_lottery
            jump_to_lottery('24')

        @self.btn_buy.unique_callback()
        def OnClick(btn, touch):

            def buy():
                if is_pc_global_pay():
                    from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                    jump_to_web_charge()
                elif self._jelly_goods_info:
                    global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

            from logic.gcommon.time_utility import get_server_time
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            cur_time = get_server_time()
            if cur_time > self.SEC_CONFIRM_TIMESTAMP:
                sec_confirm_dlg = SecondConfirmDlg2()
                sec_confirm_dlg.confirm(content=609828, confirm_callback=buy)
            else:
                buy()

        @self.panel.btn_tip.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(609685, self.desc_text_id)

        task_ui_list = self.panel.act_list
        task_ui_list.SetInitCount(0)
        task_ui_list.SetInitCount(len(self.prog_2_reward_id))
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            task_ui = task_ui_list.GetItem(idx).temp_common
            if not task_ui:
                return
            task_ui.lab_name.SetString(get_task_name(self.task_id, {'prog': prog}))
            reward_id = self.prog_2_reward_id.get(prog)
            init_common_reward_list(task_ui.list_reward, reward_id)

        self._update_goods_show()

    def _update_goods_show(self):
        has_bought = limite_pay(self._game_goods_id)
        if not self._jelly_goods_info:
            self.btn_buy.SetEnable(False)
            self.btn_buy.SetText(12121)
        elif has_bought:
            self.btn_buy.SetEnable(False)
            self.btn_buy.SetText(12014)
        else:
            self.btn_buy.SetEnable(True)
            if is_pc_global_pay() or is_steam_pay():
                price_txt = get_pc_charge_price_str(self._jelly_goods_info)
            else:
                price_txt = get_charge_price_str(self._jelly_goods_info['goodsid'])
            adjusted_price = adjust_price(str(price_txt))
            self.btn_buy.SetText(adjusted_price + ' ' + get_text_by_id(609817))
        self._update_act_list(has_bought)
        global_data.emgr.refresh_activity_redpoint.emit()

    def _update_act_list(self, has_bought=True):
        player = global_data.player
        if not player:
            return
        task_ui_list = self.panel.act_list
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            task_ui = task_ui_list.GetItem(idx).temp_common
            if not task_ui:
                return
            task_id = self.prog_2_task_id[prog]
            task_name = get_task_name(task_id, {'prog': prog})
            task_ui.lab_name.SetString(task_name)

            def check_btn(task_ui=task_ui):
                is_received = player.has_receive_reward(task_id)
                can_receive = player.is_task_reward_receivable(task_id)
                btn = task_ui.temp_btn_get.btn_common
                btn.SetEnable(False)
                btn.SetText('')
                task_ui.lab_icon.setVisible(False)
                task_ui.nd_get.setVisible(False)
                if not has_bought:
                    task_ui.lab_icon.setVisible(True)
                elif is_received:
                    task_ui.nd_get.setVisible(True)
                elif can_receive:
                    btn.SetEnable(True)
                    btn.SetText(604030)
                else:
                    btn.SetText(604031)

            @task_ui.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not is_activity_in_limit_time(self._activity_type):
                    return
                player.receive_task_reward(task_id)

            check_btn()

    def reorder_prog_list(self, progs):
        ret_list = sorted(progs, key=lambda p: (global_data.player.has_receive_reward(self.prog_2_task_id[p]), p))
        return ret_list

    def _on_update_reward(self, *args):
        self._update_goods_show()

    def on_finalize_panel(self):
        self.process_events(False)
        super(ActivitySummerBuy, self).on_finalize_panel()