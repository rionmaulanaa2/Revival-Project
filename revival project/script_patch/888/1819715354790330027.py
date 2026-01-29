# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloween/ActivityHalloweenGo.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils.activity_utils import get_left_time, is_activity_in_limit_time
from logic.gutils.template_utils import init_common_reward_list
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from common.cfg import confmgr
from logic.gutils.template_utils import get_left_info
from logic.gutils.task_utils import get_task_name, get_task_conf_by_id
from logic.gutils.jump_to_ui_utils import jump_to_web_charge, jump_to_lottery
ORIGIN_PRICE = 6
GAME_GOODS_ID = '700400001'
REMIND_DELTA_TIME = 1636127700

class ActivityHalloweenGo(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityHalloweenGo, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_ui_events()
        self.process_events(True)

    def set_show(self, show, is_init=False):
        super(ActivityHalloweenGo, self).set_show(show, is_init)
        if show:
            self.panel.PlayAnimation('show')
            self.panel.PlayAnimation('loop')

    def init_parameters(self):
        self._timer = None
        self._timer_cb = {}
        self._game_goods_id = GAME_GOODS_ID
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.task_id = conf.get('cTask', '')
        rule_text_id = conf.get('cRuleTextID', '')
        self._desc_text_id = int(rule_text_id) if rule_text_id else ''
        task_conf = get_task_conf_by_id(str(self.task_id))
        children_task_list = task_conf.get('children_task', [])
        self.buy_reward = get_task_conf_by_id(str(children_task_list[0])).get('reward', 0)
        self.prog_2_task_id = {}
        self.prog_2_reward_id = {}
        for child_idx, task_id in enumerate(children_task_list):
            self.prog_2_task_id[child_idx] = task_id
            if child_idx == 0:
                continue
            self.prog_2_reward_id[child_idx] = get_task_conf_by_id(str(task_id)).get('reward', 0)

        self._jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info('HALLOWEEN_GO')
        self.btn_buy = self.panel.btn_buy
        return

    def process_events(self, is_bind):
        e_conf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'buy_good_success': self._update_goods_show
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_init_panel(self):
        super(ActivityHalloweenGo, self).on_init_panel()
        init_common_reward_list(self.panel.list_reward_now, self.buy_reward)
        self._register_timer()
        self._timer_cb[0] = lambda : self._refresh_left_time()
        self._refresh_left_time()

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
            if cur_time > REMIND_DELTA_TIME:
                sec_confirm_dlg = SecondConfirmDlg2()
                sec_confirm_dlg.confirm(content=610076, confirm_callback=buy)
            else:
                buy()

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(610054, self._desc_text_id)

        @self.panel.btn_lucky_house.callback()
        def OnClick(btn, touch):
            jump_to_lottery('30')

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
        self._update_act_list(has_bought)
        global_data.emgr.refresh_activity_redpoint.emit()

    def _update_act_list(self, has_bought=True):
        player = global_data.player
        if not player:
            return
        task_ui_list = self.panel.act_list
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        can_receive_num = 0
        for idx, prog in enumerate(prog_list):
            task_ui = task_ui_list.GetItem(idx).temp_common
            if not task_ui:
                return
            reward_id = self.prog_2_reward_id.get(prog)
            init_common_reward_list(task_ui.list_reward, reward_id)
            task_ui.lab_num.setVisible(False)
            task_id = self.prog_2_task_id[prog]
            task_name = get_task_name(task_id, {'prog': prog})
            task_ui.lab_name.SetString(task_name)
            can_receive = player.is_task_reward_receivable(task_id)
            if can_receive:
                can_receive_num += 1

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

        all_get_node_vis = can_receive_num >= 2
        self.panel.temp_get_all.setVisible(all_get_node_vis)
        self.panel.pnl_get_all.setVisible(all_get_node_vis)

    def _refresh_left_time(self):
        left_time_delta = get_left_time(self._activity_type)
        is_ending, left_text, left_time, left_unit = get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self.panel.lab_time.SetString(day_txt)

    def _second_callback(self):
        for timer_key, cb_func in six.iteritems(self._timer_cb):
            cb_func()

    def _register_timer(self):
        from common.utils.timer import CLOCK
        self._unregister_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self._second_callback, interval=1, times=-1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def reorder_prog_list(self, progs):
        ret_list = sorted(progs, key=lambda p: (global_data.player.has_receive_reward(self.prog_2_task_id[p]), p))
        return ret_list

    def _on_update_reward(self, *args):
        self._update_goods_show()

    def init_ui_events(self):

        @self.panel.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if global_data.player:
                global_data.player.receive_all_task_reward(self.task_id)

    def on_finalize_panel(self):
        self._unregister_timer()
        self.process_events(False)
        super(ActivityHalloweenGo, self).on_finalize_panel()