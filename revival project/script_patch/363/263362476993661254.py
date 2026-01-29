# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonTaskLottery.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_server_time, get_delta_time_str, get_utc8_day_start_timestamp, ONE_DAY_SECONDS, ONE_HOUR_SECONS
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_reward, init_price_template
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils.activity_utils import is_activity_in_limit_time
from logic.gutils.jump_to_ui_utils import jump_to_web_charge
from logic.gcommon.const import SHOP_PAYMENT_ITEM
from common.utils.timer import CLOCK
from logic.gutils import task_utils
from logic.gutils import mall_utils
from common.cfg import confmgr
import six_ex
import copy

class ActivityCommonTaskLottery(ActivityBase):

    def on_init_panel(self):
        self.init_params()
        self.init_widget()
        self.init_ui_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.on_task_prog_changed,
           'receive_task_reward_succ_event': self.on_received_task_reward,
           'receive_lottery_result': self.on_receive_lottery_result,
           'buy_good_success': self.on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_params(self):
        self._conf = confmgr.get('c_activity_config', self._activity_type)
        self._ui_data = self._conf.get('cUiData')
        goods_list = copy.deepcopy(self._ui_data.get('goods_list', ['g93.xianshitehui.48', 'g93na.xianshitehui.48']))
        self.jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
        self._price_top_widget = None
        self._goods_id = None
        self._get_item_info()
        self._update_goods_id()
        self._timer = None
        self._random_task_id = None
        self._reward_id = None
        self._max_prog = 0
        self._total_prog = 0
        self._goods_payment = None
        self._get_random_task()
        return

    def _get_item_info(self):
        self._goods_id_list = self._ui_data.get('goods_id_list', {})
        self._item_info_list = {}
        self._turntable_goods_info = {}
        self._mall_config = confmgr.get('mall_config')
        for goods_id in self._goods_id_list:
            goods_id = str(goods_id)
            goods_info = self._mall_config.get(goods_id, {})
            if not goods_info:
                continue
            preview_id = int(goods_info.get('item_no'))
            preview_conf = confmgr.get('preview_{}'.format(preview_id))
            if not preview_conf:
                continue
            turntable_goods_info = preview_conf.get('turntable_goods_info', {})
            if not turntable_goods_info:
                continue
            self._turntable_goods_info[preview_id] = turntable_goods_info
            for item_info in turntable_goods_info:
                item_id = item_info[0]
                item_count = item_info[1]
                if not self._item_info_list.get(item_id):
                    self._item_info_list[item_id] = 0
                self._item_info_list[item_id] += item_count

        self.item_list = {}
        self._guaranteed_item_id = None
        item_sort = self._ui_data.get('item_sort', {})
        for index, item_id in six_ex.items(item_sort):
            if index == '3':
                self._guaranteed_item_id = item_id
            temp_item = getattr(self.panel, 'temp_item_{}'.format(index))
            if temp_item:
                self.item_list[item_id] = temp_item
                self._init_item(temp_item, item_id)

        return

    def _update_goods_id(self):
        for goods_id in self._goods_id_list:
            goods_id = str(goods_id)
            goods_info = self._mall_config.get(goods_id, {})
            if not goods_info:
                continue
            limit_by_all, _, _ = mall_utils.buy_num_limit_by_all(goods_id)
            if not limit_by_all:
                self._goods_id = goods_id
                return

    def _init_item(self, temp_item, item_id):
        temp_item.nd_cut.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_id))

        @temp_item.btn_choose.unique_callback()
        def OnClick(btn, touch):
            x, y = btn.GetPosition()
            w, _ = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos)
            return

    def _get_random_task(self):
        if not global_data.player:
            return
        else:
            random_task_id = self._ui_data.get('daily_random', None)
            if not random_task_id:
                return
            random_refresh_type = task_utils.get_task_fresh_type(random_task_id)
            random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, random_task_id)
            if not random_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % random_task_id)
                random_task_list = []
                return
            self._random_task_id = random_task_list[0]
            self._reward_id = task_utils.get_task_reward(self._random_task_id)
            return

    def init_ui_event(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            name_text_id = self._conf.get('cNameTextID')
            game_rule_text_id = self._conf.get('cRuleTextID')
            dlg.set_show_rule(get_text_by_id(name_text_id), get_text_by_id(game_rule_text_id))

        @self.panel.temp_btn_buy.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self._buy_goods(self._goods_id, 1)

        @self.panel.temp_btn_open.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            goods_count = global_data.player.get_item_num_by_no(int(self._goods_payment.split('_')[1]))
            for goods_id in self._goods_id_list:
                goods_id = str(goods_id)
                goods_info = self._mall_config.get(goods_id, {})
                if not goods_info:
                    continue
                limit_by_all, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
                if not limit_by_all:
                    left_count, _ = num_info
                    self._buy_goods(goods_id, min(goods_count, left_count))
                    goods_count -= left_count
                    if goods_count <= 0:
                        return

        @self.panel.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if mall_utils.is_pc_global_pay():
                jump_to_web_charge()
            elif self.jelly_goods_info:
                global_data.player and global_data.player.pay_order(self.jelly_goods_info['goodsid'])

    def _buy_goods(self, goods_id, buy_count):
        if not global_data.player:
            return
        if not goods_id:
            return
        prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
        if not prices:
            return
        price_info = prices[0]
        goods_payment = price_info.get('goods_payment')
        for _ in range(buy_count):
            if mall_utils.check_payment(goods_payment, price_info.get('real_price')):
                global_data.player.buy_goods(goods_id, 1, goods_payment)

    def init_widget(self):
        if not self._random_task_id or not self._reward_id:
            return
        reward_list = confmgr.get('common_reward_data', str(self._reward_id), 'reward_list', default=[])
        if not reward_list:
            return
        self.panel.lab_task.SetString(task_utils.get_task_name(self._random_task_id))
        self._goods_payment = '{}_{}'.format(SHOP_PAYMENT_ITEM, reward_list[0][0])
        init_tempate_reward(self.panel.temp_item, reward_list[0][0], reward_list[0][1], show_tips=True)
        self._update_task_progress()
        self._init_task_timer()

        @self.panel.temp_btn_task.btn_common.unique_callback()
        def OnClick(btn, touch):
            self._on_task_btn_click()

        self._init_money_widget()
        self._update_buy_btn_state()
        self._init_money_buy_widget()
        self._update_cash_buy_btn_state()
        self._update_cost_widget()
        self._update_item_info()

    def _on_task_btn_click(self):
        if not global_data.player:
            return
        else:
            if self._reward_id is None:
                is_prog_task = True if 1 else False
                cur_prog = global_data.player.get_task_prog(self._random_task_id)
                return is_activity_in_limit_time(self._activity_type) or None
            if cur_prog < self._total_prog:
                jump_conf = task_utils.get_jump_conf(self._random_task_id)
                item_utils.exec_jump_to_ui_info(jump_conf)
            else:
                if is_prog_task:
                    global_data.player.receive_task_prog_reward(self._random_task_id, self._total_prog)
                else:
                    global_data.player.receive_task_reward(self._random_task_id)
                if self._max_prog == self._total_prog:
                    btn.SetText(80866)
                    btn.SetEnable(False)
            return

    def _update_task_progress(self):
        if not global_data.player:
            return
        if not self._goods_id:
            self.panel.bar_task.setVisible(False)
            return
        status, cur_prog, _, total_prog = task_utils.get_task_status_info(self._random_task_id)
        self._total_prog = total_prog
        self.panel.lab_prog_task.setString('{}/{}'.format(cur_prog, self._total_prog))
        btn_receive = self.panel.temp_btn_task.btn_common
        btn_receive.EnableCustomState(True)
        if status == ITEM_RECEIVED:
            btn_receive.SetText(get_text_by_id(604029))
            btn_receive.SetEnable(False)
        elif status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(self._random_task_id)
            if jump_conf:
                btn_receive.SetText(jump_conf.get('unreach_text', ''))
                btn_receive.SetEnable(True)
                btn_receive.SetSelect(False)
            else:
                btn_receive.SetText(get_text_by_id(604031))
                btn_receive.SetEnable(False)
        elif status == ITEM_UNRECEIVED:
            btn_receive.SetText(get_text_by_id(604030))
            btn_receive.SetEnable(True)
            btn_receive.SetSelect(True)

    def _init_task_timer(self):
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_task_timer, interval=1, mode=CLOCK)
        self._update_task_timer()

    def _update_task_timer(self):
        refresh_time = get_utc8_day_start_timestamp() + ONE_DAY_SECONDS + 5 * ONE_HOUR_SECONS
        remain_time = int(refresh_time - get_server_time()) % ONE_DAY_SECONDS
        time_str = get_delta_time_str(remain_time)
        self.panel.lab_tips_time.SetString(get_text_by_id(633922).format(time_str))

    def _init_money_widget--- This code section failed: ---

 300       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_TRUE     64  'to 64'

 301       9  LOAD_GLOBAL           1  'PriceUIWidget'
          12  LOAD_GLOBAL           1  'PriceUIWidget'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_money'
          24  LOAD_CONST            2  'pnl_title'
          27  LOAD_GLOBAL           4  'False'
          30  CALL_FUNCTION_513   513 
          33  LOAD_FAST             0  'self'
          36  STORE_ATTR            0  '_price_top_widget'

 302      39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             0  '_price_top_widget'
          45  LOAD_ATTR             5  'show_money_types'
          48  LOAD_FAST             0  'self'
          51  LOAD_ATTR             6  '_goods_payment'
          54  BUILD_LIST_1          1 
          57  CALL_FUNCTION_1       1 
          60  POP_TOP          
          61  JUMP_FORWARD         13  'to 77'

 304      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             0  '_price_top_widget'
          70  LOAD_ATTR             7  '_on_player_info_update'
          73  CALL_FUNCTION_0       0 
          76  POP_TOP          
        77_0  COME_FROM                '61'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 30

    def _update_buy_btn_state(self):
        item_id = int(self._goods_payment.split('_')[1])
        item_count = global_data.player.get_item_num_by_no(item_id) if global_data.player else 0
        btn_buy = self.panel.temp_btn_buy.btn_common_big
        if item_count:
            btn_buy.SetEnable(True)
        else:
            btn_buy.SetEnable(False)
        btn_buy_all = self.panel.temp_btn_open
        if item_count > 1:
            btn_buy_all.setVisible(True)
        else:
            btn_buy_all.setVisible(False)

    def _update_cash_buy_btn_state(self):
        if not global_data.player:
            self.panel.btn_buy.setVisible(False)
            return
        if not self.jelly_goods_info:
            self.panel.btn_buy.setVisible(False)
            return
        goodsid = self.jelly_goods_info['goodsid']
        goods_info = global_data.player.get_goods_info(goodsid)
        if not goods_info:
            self.panel.btn_buy.setVisible(False)
            return
        cash_goods_id = goods_info.get('cShopGoodsId', '700200212')
        cash_goods_info = self._mall_config.get(cash_goods_id, {})
        item_no = cash_goods_info.get('item_no', 0)
        item = global_data.player.get_item_by_no(item_no)
        if not item:
            self.panel.btn_buy.setVisible(True)
        elif item.get_expire_time() > get_server_time():
            self.panel.btn_buy.setVisible(True)
        else:
            self.panel.btn_buy.setVisible(False)

    def _init_money_buy_widget(self):
        btn_buy = self.panel.btn_buy
        if not self.jelly_goods_info:
            btn_buy.setVisible(False)
            return
        if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
            price_text = mall_utils.get_pc_charge_price_str(self.jelly_goods_info)
        else:
            price_text = mall_utils.get_charge_price_str(self.jelly_goods_info['goodsid'])
        btn_buy.setVisible(True)
        btn_buy.lab_price.SetString(mall_utils.adjust_price_decimal2(str(price_text)))

    def _update_cost_widget(self):
        if not self._goods_id:
            self.panel.temp_btn_buy.setVisible(False)
            return
        prices = mall_utils.get_mall_item_price(self._goods_id)
        init_price_template(prices[0], self.panel.temp_price)

    def _update_item_info(self):
        has_item_info_list = {}
        for preview_id, turntable_goods_info in six_ex.items(self._turntable_goods_info):
            if global_data.player:
                intervene_count = global_data.player.get_reward_intervene_count(preview_id) if 1 else {}
                for index, count in six_ex.items(intervene_count):
                    item_info = turntable_goods_info[int(index)]
                    item_id = item_info[0]
                    item_count = item_info[1]
                    if not has_item_info_list.get(item_id):
                        has_item_info_list[item_id] = 0
                    has_item_info_list[item_id] += item_count

        has_item_count = 0
        has_receive_guaranteed_item = False
        for item_id, all_count in six_ex.items(self._item_info_list):
            item_count = has_item_info_list.get(item_id, 0)
            has_item_count += item_count
            if item_id == self._guaranteed_item_id and item_count >= all_count:
                has_receive_guaranteed_item = True
            lab_quantity = self.item_list[item_id].pnl_prog.lab_prog
            lab_quantity.SetString('{}/{}'.format(str(all_count - item_count), str(all_count)))
            nd_got = self.item_list[item_id].nd_got
            nd_got.setVisible(int(item_count) == int(all_count))

        max_precent = 76
        if not has_receive_guaranteed_item:
            guaranteed_count = self._ui_data.get('guaranteed_count', 0)
            self.panel.lab_tips.setVisible(False)
            self.panel.lab_title.setVisible(True)
            self.panel.lab_prog.setVisible(True)
            self.panel.lab_prog.setString('{}/{}'.format(str(has_item_count), str(guaranteed_count)))
            percentage = int(has_item_count / float(guaranteed_count) * max_precent)
            self.panel.prog.setPercentage(percentage)
        else:
            self.panel.lab_tips.setVisible(True)
            self.panel.lab_title.setVisible(False)
            self.panel.lab_prog.setVisible(False)
            self.panel.prog.setPercentage(max_precent)

    def on_received_task_reward(self, task_id):
        if self._random_task_id == task_id:
            self._update_task_progress()
            self._update_item_info()
            self._update_buy_btn_state()
            self._update_cost_widget()
            self._init_money_widget()
            global_data.player and global_data.player.read_activity_list(self._activity_type)

    def on_task_prog_changed(self, changes):
        for change in changes:
            if self._random_task_id == change.task_id:
                self._update_task_progress()
                global_data.emgr.refresh_activity_redpoint.emit()
                break

    def on_receive_lottery_result(self, item_list, origin_list, extra_data, extra_info):
        global_data.emgr.receive_award_succ_event_from_lottery.emit(*(item_list, origin_list))
        global_data.emgr.refresh_activity_redpoint.emit()
        self._update_goods_id()
        self._update_item_info()
        self._update_buy_btn_state()
        self._update_cost_widget()
        self._init_money_widget()

    def on_buy_good_success(self, *args):
        self._update_goods_id()
        self._update_buy_btn_state()
        self._update_cash_buy_btn_state()
        self._init_money_widget()

    def on_finalize_panel(self):
        self.process_event(False)
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return