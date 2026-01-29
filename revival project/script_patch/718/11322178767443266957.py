# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySeniorMultiLayerTurntableWidget.py
from __future__ import absolute_import
from six.moves import range
from .LotteryMultiLayerTurntableWidget import LotteryMultiLayerTurntableWidget
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DARK_PRICE_COLOR
from logic.gutils.mall_utils import get_goods_item_lottery_table_id, get_lottery_turntable_item_data_by_goods_id, get_mall_item_price, check_payment
from logic.gutils.template_utils import splice_price
from logic.gcommon.const import SHOP_PAYMENT_DYNAMIC
from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
from logic.comsys.item_use.ItemUseConfirmUI import ItemUseConfirmUI
ITEM_ID_INDEX = 0
ITEM_COUNT_INDEX = 1
DRAW_COUNT_INDEX = 0
GOODS_ID_INDEX = 1

class LotterySeniorMultiLayerTurntableWidget(LotteryMultiLayerTurntableWidget):

    def init_panel(self):
        super(LotterySeniorMultiLayerTurntableWidget, self).init_panel()
        if 'exclusive_gift' in self.data:
            self.task_list = self.data['exclusive_gift'].get('task_list', [])
            self.refresh_gift_red_point()

            @self.panel.btn_bones.unique_callback()
            def OnClick(btn, touch):
                from logic.comsys.lottery.LotteryExclusiveGiftUI import LotteryExclusiveGiftUI
                gift_template = self.data['exclusive_gift'].get('gift_template', '')
                self.refresh_gift_red_point()
                LotteryExclusiveGiftUI(None, self.data['exclusive_gift'], gift_template=gift_template)
                return

    def refresh_gift_red_point(self, *args):
        if self.task_list:
            for task in self.task_list:
                if global_data.player and global_data.player.has_unreceived_task_reward(str(task)):
                    self.panel.btn_bones.red_point.setVisible(True)
                    return True

            self.panel.btn_bones.red_point.setVisible(False)
            return False
        return False

    def init_parameters(self):
        super(LotteryMultiLayerTurntableWidget, self).init_parameters()
        self.nd_turntable = None
        self.turntable_widgets = []
        self.need_refresh_round_data = True
        self.all_round_finished = False
        self.single_goods_id_list = list(self.data['extra_single_goods_id'])
        self.layer_count = len(self.single_goods_id_list)
        self.single_goods_id_list.append(self.single_goods_id_list[-1])
        self.cur_layer = 0
        self.cur_layer_lottery_count = 0
        self.cur_single_goods_id = None
        self.cur_senior_goods_id_list = None
        self.turntable_item_list = [ get_lottery_turntable_item_data_by_goods_id(self.single_goods_id_list[i][0]) for i in range(self.layer_count) ]
        self.turntable_item_list.append(self.turntable_item_list[-1])
        self.table_id_list = [ get_goods_item_lottery_table_id(self.single_goods_id_list[i][0]) for i in range(self.layer_count) ]
        self.table_id_list.append(self.table_id_list[-1])
        self.nd_belong_layer = {}
        self.refresh_round_data(only_data=True)
        self.last_click_layer = self.layer_count - 1
        self.show_model_id = self.turntable_item_list[self.last_click_layer][0][ITEM_ID_INDEX]
        self.nd_item_map = {}
        self.cur_init_layer = 0
        self.scroll_layer_timer = None
        self.price_color = [2366765, '#SR', '#BC']
        self.is_senior_buy = False
        self.item_use_id = None
        self.item_use_num = None
        self.task_list = []
        return

    def get_event_conf(self):
        econf = super(LotterySeniorMultiLayerTurntableWidget, self).get_event_conf()
        econf.update({'receive_award_end_event': self.show_special_item_use_comfirm_ui,
           'receive_task_reward_succ_event': self.refresh_gift_red_point
           })
        return econf

    def refresh_round_data(self, only_data=False):
        if not only_data:
            self._set_layer_tag_visible(self.cur_layer, False)
            nd = getattr(self.nd_turntable, 'nd_%d' % (self.cur_layer + 1))
            nd and nd.setLocalZOrder(0)
            self._set_layer_delighted(self.cur_layer, False)
        main_item_idx = str(ITEM_ID_INDEX)
        for layer in range(self.layer_count):
            if global_data.player.get_reward_intervene_count(self.table_id_list[layer]).get(main_item_idx, 0) <= 0:
                self.cur_layer = layer
                break
        else:
            self.cur_layer = self.layer_count

        self.all_round_finished = self.cur_layer == self.layer_count
        drawn_count = 0
        for item_idx in range(len(self.turntable_item_list[self.cur_layer])):
            drawn_count += global_data.player.get_reward_intervene_count(self.table_id_list[self.cur_layer]).get(str(item_idx), 0)

        self.cur_layer_lottery_count = drawn_count
        self.cur_single_goods_id = self.single_goods_id_list[self.cur_layer][0]
        self.cur_senior_goods_id_list = self.single_goods_id_list[self.cur_layer][1]
        if not only_data:
            self.turntable_widget = self.turntable_widgets[self.cur_layer]
            self._set_layer_tag_visible(self.cur_layer, True)
            self._set_layer_delighted(self.cur_layer, True)
            self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
            self.buy_widget.update_lottery_price_info(CONTINUAL_LOTTERY_COUNT, self.cur_single_goods_id)
            self._refresh_layer_discount_num()

    def _refresh_layer_discount_num(self):
        senior_goods_id, per_ticket_count = self.cur_senior_goods_id_list
        original_count = get_mall_item_price(self.cur_single_goods_id)[0].get('original_price')
        self.panel.discount_num.SetString('-' + str(100 - per_ticket_count * 100 / original_count) + '%')

    def get_special_price_info(self, price_info, lottery_count):
        if lottery_count == CONTINUAL_LOTTERY_COUNT:
            senior_goods_id, per_ticket_count = self.cur_senior_goods_id_list
            last_num = len(self.turntable_item_list[self.cur_layer]) - self.cur_layer_lottery_count
            last_num = 1 if last_num == 0 else last_num
            need_ticket_count = last_num * per_ticket_count
            has_ticket_num = global_data.player.get_item_money(self.data['ticket_item_id']) if global_data.player else 0
            if has_ticket_num:
                if has_ticket_num >= need_ticket_count:
                    ticket_price_info = {'goods_payment': price_info['goods_payment'],
                       'original_price': need_ticket_count,
                       'real_price': need_ticket_count
                       }
                    return (
                     [
                      ticket_price_info], False)
                else:
                    ticket_price_info = {'goods_payment': price_info['goods_payment'],'original_price': has_ticket_num,
                       'real_price': has_ticket_num
                       }
                    need_buy_count = need_ticket_count - has_ticket_num
                    yuanbao_price = get_mall_item_price(self.data['ticket_goods_id'], need_buy_count)[0]
                    return (
                     [
                      ticket_price_info, yuanbao_price], False)

            else:
                return (
                 [
                  get_mall_item_price(self.data['ticket_goods_id'], need_ticket_count)[0]], False)
        return False

    def special_buy_logic_func(self, price_info, lottery_count):
        if lottery_count == CONTINUAL_LOTTERY_COUNT:
            senior_goods_id, per_ticket_count = self.cur_senior_goods_id_list
            last_num = len(self.turntable_item_list[self.cur_layer]) - self.cur_layer_lottery_count
            need_ticket_count = last_num * per_ticket_count
            if global_data.player:
                has_ticket_num = global_data.player.get_item_money(self.data['ticket_item_id']) if 1 else 0
                need_buy_num = need_ticket_count - has_ticket_num
                if need_buy_num > 0:
                    ticket_price = get_mall_item_price(self.data['ticket_goods_id'], need_buy_num)[0]
                    return check_payment(ticket_price['goods_payment'], ticket_price['real_price']) or True
                global_data.player.buy_goods(self.data['ticket_goods_id'], need_buy_num, ticket_price['goods_payment'], need_show=False)
            self.show_buying_process()
            global_data.player.buy_goods(senior_goods_id, 1, SHOP_PAYMENT_DYNAMIC, need_show=True)
            return True
        return False

    def show_buying_process(self):
        self.is_senior_buy = True
        self.buying_callback(SINGLE_LOTTERY_COUNT)
        global_data.emgr.refresh_lottery_btn_enable.emit(False)
        global_data.emgr.set_cur_lucky_draw_info.emit(self.lottery_id, CONTINUAL_LOTTERY_COUNT)
        ScreenLockerUI(None, False)
        return

    def buying_callback(self, lottery_count):
        self.cur_draw_lottery_count = lottery_count
        self._stop_buy_button_loop_anim()
        if self.need_show_choose_tag and self.show_model_id in self.nd_item_map[self.last_click_layer]:
            self.nd_item_map[self.last_click_layer][self.show_model_id].nd_chosen.setVisible(False)
        self.turntable_widget.stop_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self.turntable_widget.play_turntable_animation(lottery_count, self.is_senior_buy)
        self._end_auto_switch_show_model_timer()
        self.end_scroll_layer_timer()
        if self.need_skip_anim or self.is_senior_buy:
            self.scroll_to_cur_layer(duration=0.2)
        else:
            self.scroll_layer_timer = global_data.game_mgr.register_logic_timer(self.scroll_to_cur_layer, interval=3, times=1)

    def show_special_item_use_comfirm_ui(self):
        if self.item_use_id and self.item_use_num:
            global_data.ui_mgr.close_ui('ItemUseComfirmUI')
            ItemUseConfirmUI(item_no=int(self.item_use_id), item_num=self.item_use_num)
            self.item_use_num = None
            self.item_use_id = None
        return

    def on_receive_lottery_result(self, item_list, origin_list):
        if len(item_list) > 1:
            cur_layer_item_list = self.turntable_item_list[self.cur_layer]
            sorted_item_list, sorted_origin_list, correspond_index_list = [], [], []
            for i in range(len(item_list)):
                if origin_list[i]:
                    item_info = origin_list[i] if 1 else item_list[i]
                    if item_info[0] == 70400101:
                        self.item_use_id = item_info[0]
                        self.item_use_num = item_info[1]
                    correspond_index = cur_layer_item_list.index([str(item_info[0]), item_info[1]])
                    correspond_index_list.append((correspond_index, i))

            correspond_index_list.sort()
            for index_map in correspond_index_list:
                index = index_map[1]
                sorted_item_list.append(item_list[index])
                sorted_origin_list.append(origin_list[index])

            item_list, origin_list = sorted_item_list, sorted_origin_list
        elif len(item_list) == 1:
            item_info = item_list[0]
            if item_info[0] == 70400101:
                self.item_use_id = item_info[0]
                self.item_use_num = item_info[1]
        self.turntable_widget.set_turntable_items_got(item_list, origin_list, force_play_chosen_anim_when_skip=self.cur_draw_lottery_count == SINGLE_LOTTERY_COUNT, force_skip_turntable_anim=self.is_senior_buy)
        self.is_senior_buy = False

    def update_price_info_callback(self, nd, lottery_count):
        nd_lab = lottery_count == SINGLE_LOTTERY_COUNT and self.panel.btn_once.lab_once if 1 else self.panel.btn_repeat.lab_repeat
        price_width = 0
        for price_item in nd.temp_price.GetAllItem():
            if price_item.isVisible():
                price_width += price_item.GetContentSize()[0] * nd.getScaleX()

        lab_width = nd_lab.getTextContentSize().width
        total_width = price_width + lab_width
        half_width = total_width / 2
        price_x_offset = price_width / 2 - half_width - 5 * nd.getScaleX()
        lab_x_offset = half_width - lab_width + 5 * nd.getScaleX()
        nd.SetPosition('50%{}'.format(int(price_x_offset)), nd.getPositionY())
        nd_lab.SetPosition('50%{}'.format(int(lab_x_offset)), nd_lab.getPositionY())