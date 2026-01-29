# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDaliyCharge.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price, get_goods_item_reward_id, get_mall_item_price_list, get_goods_limit_num_all
from logic.gutils.task_utils import get_task_name, get_task_conf_by_id, get_total_prog, get_children_task, get_raw_left_open_time
from logic.gutils.template_utils import init_common_reward_list, init_tempate_mall_i_item, get_reward_list_by_reward_id
from logic.gutils.activity_utils import get_left_time, is_activity_in_limit_time
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils.jump_to_ui_utils import jump_to_charge, jump_to_web_charge
from .ActivityDaliyChargeExchange import ActivityDaliyChargeExchange, REMIND_PREIX
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS, get_rela_day_no
from logic.client.const import mall_const
from logic.comsys.activity.widget import widget
import copy

def check_show_red_point(goods_id):
    item_cost = get_mall_item_price_list(goods_id)
    if not global_data.player:
        return False
    buy_num = global_data.player.get_buy_num_all(goods_id)
    max_num = get_goods_limit_num_all(goods_id)
    item_num = global_data.player.get_item_num_by_no(int(item_cost[0]))
    if buy_num < max_num and item_num >= item_cost[1]:
        return True
    return False


@widget('AsyncChooseRewardTaskListWidget')
class ActivityDaliyCharge(ActivityTemplate):

    def __init__(self, dlg, activity_type):
        super(ActivityDaliyCharge, self).__init__(dlg, activity_type)
        self.init_panel()
        self.register_timer()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self.task_id = conf.get('cTask', '')
        self.name_text_id = conf.get('cNameTextID', '')
        self.desc_text_id = conf.get('cDescTextID', '')
        self.daliy_charge_task_id = ui_data.get('charge_task_id', '')
        self.goods_id = ui_data.get('goods_id', '') if not is_steam_pay() and not G_IS_NA_USER else ui_data.get('goods_id_steam', '')
        goods_list = copy.deepcopy(ui_data.get('goods_list', ['g93.onemoney.1', 'g93na.avatar.6']))
        if is_steam_pay():
            goods_list[0] = ui_data.get('goods_steam', 'g93.avatar.6')
        self.jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
        self.goods_reward = get_goods_item_reward_id(self.goods_id)
        self.exchange_goods_list = ui_data.get('exchange_goods_list', [])
        self.default_show_redpoint = ui_data.get('default_show_redpoint', [])
        self.day = get_rela_day_no()
        self.timer = None
        self.exchange_widget = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.update_daliy_goods_state,
           'refresh_activity_redpoint': self.update_exchange_redpoint
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        init_common_reward_list(self.panel.list_reward_now, self.goods_reward)
        self.update_daliy_goods_state()
        self.panel.btn_describe.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_describe())
        self.panel.btn_buy.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_buy())
        self.panel.btn_exchange.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_exchange())

    def refresh_panel(self):
        self.update_daliy_goods_state()

    def register_timer(self):
        self.unregister_timer()
        self.refresh_left_time()
        self.timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self.timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self.timer)
        self.timer = 0

    def refresh_left_time(self):
        left_time = get_raw_left_open_time(self.task_id)
        if left_time > 0:
            self.panel.lab_tips_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = ONE_DAY_SECONDS + left_time
            self.panel.lab_tips_time.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))
        new_day = get_rela_day_no()
        if self.day != new_day:
            self.update_daliy_goods_state()
        self.day = new_day

    def on_click_btn_buy(self):
        if not is_activity_in_limit_time(self._activity_type):
            global_data.game_mgr.show_tip(607911)
            return
        if limite_pay(self.goods_id):
            return
        if is_pc_global_pay():
            jump_to_web_charge()
        elif self.jelly_goods_info:
            global_data.player and global_data.player.pay_order(self.jelly_goods_info['goodsid'])

    def on_click_btn_describe(self):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(int(self.name_text_id), int(self.desc_text_id))

    def on_click_btn_exchange(self):
        self.exchange_widget = ActivityDaliyChargeExchange(activity_type=self._activity_type)

    def update_daliy_goods_state(self):
        has_bought = limite_pay(self.goods_id)
        if not self.jelly_goods_info:
            self.panel.btn_buy.SetEnable(False)
            self.panel.btn_buy.SetText(12121)
            self.panel.btn_buy.setVisible(True)
            self.panel.img_get.setVisible(False)
        elif has_bought:
            self.panel.btn_buy.SetEnable(False)
            self.panel.btn_buy.setVisible(False)
            self.panel.img_get.setVisible(True)
            self.panel.btn_buy.SetText(80836)
        else:
            self.panel.img_get.setVisible(False)
            self.panel.btn_buy.setVisible(True)
            self.panel.btn_buy.SetEnable(True)
            if is_pc_global_pay() or is_steam_pay():
                price_txt = get_pc_charge_price_str(self.jelly_goods_info)
            else:
                price_txt = get_charge_price_str(self.jelly_goods_info['goodsid'])
            real_price = adjust_price(str(price_txt))
            self.panel.btn_buy.SetText(real_price + ' ' + get_text_by_id(609817))

    def update_exchange_redpoint(self):
        for idx in range(len(self.exchange_goods_list)):
            remind_str = REMIND_PREIX.format(self.exchange_goods_list[idx])
            state = global_data.achi_mgr.get_cur_user_archive_data(remind_str, None)
            if state is None and idx in self.default_show_redpoint:
                global_data.achi_mgr.set_cur_user_archive_data(remind_str, True)
                state = True
            elif state is None:
                state = False
            if state == True:
                show_redpoint = check_show_red_point(self.exchange_goods_list[idx])
                if show_redpoint:
                    self.panel.temp_red.setVisible(True)
                    return

        self.panel.temp_red.setVisible(False)
        return

    def on_finalize_panel(self):
        super(ActivityDaliyCharge, self).on_finalize_panel()
        self.panel = None
        self.unregister_timer()
        if self.exchange_widget:
            self.exchange_widget.close()
        return

    def on_main_ui_hide(self):
        if self.exchange_widget:
            self.exchange_widget.close()

    @staticmethod
    def show_tab_rp(activity_id):
        activity_conf = confmgr.get('c_activity_config', str(activity_id))
        ui_data = activity_conf['cUiData']
        exchange_list = ui_data.get('exchange_goods_list', [])
        for idx in range(len(exchange_list)):
            remind_str = REMIND_PREIX.format(exchange_list[idx])
            state = global_data.achi_mgr.get_cur_user_archive_data(remind_str, None)
            if state == True:
                if check_show_red_point(exchange_list[idx]):
                    return True

        return False