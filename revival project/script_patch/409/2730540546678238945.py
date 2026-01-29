# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryScratchCardWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from .LotteryBaseWidget import LotteryBaseWidget
from logic.gcommon import time_utility
from logic.gcommon.const import SHOP_PAYMENT_GOLD, SHOP_PAYMENT_YUANBAO
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.mall_utils import get_mall_item_price, check_payment, get_goods_item_no, is_good_opened, limite_pay
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_name
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_const.activity_const import CARD_HEIGHT, CARD_WIDTH, MAX_SELECT_NUM, CARD_SUM
from .LotteryScratchItemWidget import LotteryScratchItemWidget
from .LotteryScratchBuyWidget import LotteryScratchBuyWidget
from .LotteryScratchShopWidget import LotteryScratchShopWidget
from .LotteryScratchListWidget import LotteryScratchListWidget
from logic.gutils.lobby_model_display_utils import is_chuchang_scene
from logic.gcommon.time_utility import get_rela_day_no
from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
import copy
import random
import cc
from common.cfg import confmgr
from logic.gutils.mall_utils import get_lottery_exchange_list
STATE_CLOSE = 1
STATE_SELECT = 2
STATE_OPEN = 3
SHOW_TIP_KEY = 'LOTTERY_SCRATCH_CARD_{}'
SHOW_MODEL_DISPLAY_KEY = 'LOTTERY_SCRATCH_CARD_MODEL_DISPLAY_{}'
CARD_FULL_LIST = set([ str(i) for i in range(CARD_SUM) ])

class LotteryScratchCardWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryScratchCardWidget, self).init_parameters()
        self.is_show_scratch = True
        self.is_first_show_model = False
        self.card_sum = CARD_SUM
        self.final_reward_item = self.data.get('extra_data', {}).get('display_item_id')
        self.scratch_main_widget = None
        self.scratch_confirm_widget = None
        self.scratch_exchange_widget = None
        self.scratch_buy_widget = None
        self.show_tip_key = SHOW_TIP_KEY.format(self.lottery_id)
        self.extra_goods_id = self.data.get('extra_single_goods_id', [])
        self.ticket_goods_id = self.data.get('ticket_goods_id')
        self.single_goods_id = self.data.get('single_goods_id')
        self.ticket_item_no = self.data.get('ticket_item_id')
        self.free_goods_id = self.data.get('free_single_goods_id')
        self.free_text_id = self.data.get('free_single_lottery_text')
        if self.free_goods_id:
            self.free_single_goods_limit_level = confmgr.get('mall_config', self.data['free_single_goods_id'], 'level', default=0)
        self.use_ticket_count = 0
        self.receive_reward_count = 0
        self.reward_item_list = []
        self.reward_origin_list = []
        self.buy_idx_list = []
        self.open_card = global_data.player.get_reward_intervene_count(self.data['table_id']) if global_data.player else {}
        self.open_num = len(self.open_card)
        _, exchange_goods_dict = get_lottery_exchange_list()
        exchange_goods_list = exchange_goods_dict.get(self.lottery_id, {})
        self.exchange_item_list = [ get_goods_item_no(goods_id) for goods_id in exchange_goods_list ]
        return

    def init_panel(self):
        super(LotteryScratchCardWidget, self).init_panel()
        self.init_list_widget()
        self.init_exchange_widget()
        self.init_buy_widget()
        check_skin_tag(self.panel.temp_level, self.final_reward_item)
        self.panel.lab_name.SetString(get_lobby_item_name(self.final_reward_item))
        self.panel.btn_show.BindMethod('OnClick', self.on_click_btn_show)
        self.panel.btn_describe.BindMethod('OnClick', self.on_click_btn_describe)
        self.panel.btn_gift.BindMethod('OnClick', self.on_click_btn_gift)
        self.panel.nd_shop.temp_btn_close.btn_back.BindMethod('OnClick', self.on_click_btn_exit_exchange)
        if 'exclusice_gift' in self.data:
            self.panel.btn_gift.BindMethod('OnClick', self.on_click_btn_gift)
        if not global_data.achi_mgr.get_cur_user_archive_data(self.show_tip_key):
            self.panel.RecordAnimationNodeState('head_loop')
            self.panel.PlayAnimation('head_loop')
        self.refresh_price()

    def init_list_widget(self):

        def show_main_widget():
            self.is_show_scratch = True
            self.panel.PlayAnimation('show')
            self.panel.bg.setVisible(True)
            self.panel.list_item.setVisible(True)
            self.panel.nd_touch.setVisible(True)
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video()
            if is_chuchang_scene():
                global_data.emgr.end_mecha_chuchang_scene.emit()
                global_data.emgr.set_last_chuchang_id.emit(None)
            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.set_lottery_reward_info_label_visible.emit(False)
            global_data.emgr.set_mecha_preview_advanced_appearance_visible.emit(False)
            global_data.emgr.set_mecha_translation_widget_visible.emit(False)
            return

        def hide_main_widget():
            self.is_show_scratch = False
            self.panel.bg.setVisible(False)
            self.panel.list_item.setVisible(False)
            self.panel.nd_touch.setVisible(False)
            self.panel.PlayAnimation('rotatechange')

        self.scratch_main_widget = LotteryScratchListWidget(self.panel.nd_content, self.panel, self.on_change_show_reward, self.data['table_id'], self.lottery_id, self.on_scratch_drag_end, show_callback=show_main_widget, hide_callback=hide_main_widget)

    def init_buy_widget(self):
        self.scratch_buy_widget = LotteryScratchBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_many
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.price,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_many.price
           }, special_buy_logic_func=self.special_buy_logic, get_special_price_info=self.get_special_price_info)

    def init_exchange_widget(self):
        if not self.data.get('show_shop'):
            return
        self.panel.btn_exchange.BindMethod('OnClick', self.on_click_btn_exchange)

        def show_callback():
            self.panel.PlayAnimation('shop_in')
            global_data.emgr.set_lottery_reward_info_label_visible.emit(True)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            self.panel.PlayAnimation('shop_out')
            global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.scratch_exchange_widget = LotteryScratchShopWidget(self.panel.nd_shop, self.panel, self.on_change_show_reward, self.lottery_id, show_callback=show_callback, hide_callback=hide_callback)

    def get_random_card_list(self, count):
        if not global_data.player:
            return []
        intervene_count = global_data.player.get_reward_intervene_count(self.data['table_id'])
        opened_list = six_ex.keys(intervene_count)
        choose_list = []
        random_list = list(CARD_FULL_LIST.difference(set(opened_list)))
        rand = random.Random()
        for i in range(count):
            idx = rand.randint(0, len(random_list) - 1)
            choose_list.append(random_list[idx])
            random_list.remove(random_list[idx])

        return choose_list

    def get_special_price_info(self, price_info, lottery_count):
        self.refresh_price()
        if lottery_count == CONTINUAL_LOTTERY_COUNT:
            if price_info:
                return self.get_special_multi_scratch_price_info(self.ticket_goods_id, self.single_goods_id, self.ticket_item_no, 5)
            return False
        if lottery_count == SINGLE_LOTTERY_COUNT:
            if price_info:
                return self.get_special_price_info_for_free_scratch_card_single_lottery(self.free_goods_id)
            return False
        return False

    def special_buy_logic(self, price_info, lottery_count):
        if self.card_sum - self.open_num == 0:
            global_data.game_mgr.show_tip(633868)
            return True
        if lottery_count == CONTINUAL_LOTTERY_COUNT:
            self.special_buy_multi_logic(5)
            return True
        if lottery_count == SINGLE_LOTTERY_COUNT:
            if not self.special_buy_logic_for_free_scratch_card_single_lottery(self.free_goods_id):
                self.special_buy_multi_logic(1)
            return True
        return False

    def check_price_free_single_scratch_valid(self, free_goods_id):
        if not free_goods_id:
            return False
        return is_good_opened(free_goods_id) and not limite_pay(free_goods_id)

    def special_buy_logic_for_free_scratch_card_single_lottery(self, free_goods_id, select_list=[]):
        if self.check_price_free_single_scratch_valid(self.free_goods_id):
            if global_data.player and global_data.player.get_lv() < self.free_single_goods_limit_level:
                global_data.game_mgr.show_tip(get_text_by_id(603007).format(self.free_single_goods_limit_level))
                return True
            choose_idx = None
            if select_list:
                choose_idx = select_list[0]
            else:
                choose_list = self.get_random_card_list(1)
                if choose_list:
                    choose_idx = choose_list[0]
            if choose_idx:
                self.buy_idx_list = [
                 choose_idx]
                self.show_buying_process(1)
                global_data.player.buy_goods(free_goods_id, 1, SHOP_PAYMENT_YUANBAO, need_show=False, extra_info={'grid': int(choose_idx)})
            return True
        else:
            return False

    def get_special_price_info_for_free_scratch_card_single_lottery(self, free_goods_id):
        if self.check_price_free_single_scratch_valid(free_goods_id):
            final_price_info = get_mall_item_price(self.ticket_goods_id)
            final_price_info[0]['discount_price'] = 0
            return (
             final_price_info, False)
        return False

    def special_buy_multi_logic(self, count, select_list=[]):
        price_info, _ = self.get_special_multi_scratch_price_info(self.ticket_goods_id, self.single_goods_id, self.ticket_item_no, count)
        if len(price_info) >= 2:
            ticket_price_info, money_price_info = price_info
            if self.buy_lottery_ticket(money_price_info):
                need_buy_ticket_count = money_price_info.get('need_buy_ticket_count', 0)
                real_price = ticket_price_info['real_price']
                new_goods_info = copy.deepcopy(ticket_price_info)
                new_goods_info['real_price'] = need_buy_ticket_count + real_price
                if self.buy_lottery_goods(new_goods_info, select_list=select_list):
                    return True
            return False
        else:
            price_info = price_info[0]
            if price_info.get('goods_payment') == SHOP_PAYMENT_YUANBAO:
                if self.buy_lottery_ticket(price_info):
                    need_buy_ticket_count = price_info.get('need_buy_ticket_count', 0)
                    if need_buy_ticket_count > 0:
                        single_goods_info = get_mall_item_price(self.single_goods_id)[0]
                        new_goods_info = copy.deepcopy(single_goods_info)
                        new_goods_info['real_price'] *= need_buy_ticket_count
                        if self.buy_lottery_goods(new_goods_info, select_list=select_list):
                            return True
                return False
            if self.buy_lottery_goods(price_info, select_list=select_list):
                return True
            return False

    def buy_lottery_ticket(self, price_info):
        if not price_info or not check_payment(price_info['goods_payment'], price_info['real_price']):
            return False
        ticket_price = get_mall_item_price(self.ticket_goods_id)[0]
        need_buy_ticket_count = price_info.get('need_buy_ticket_count', 0)
        if price_info['goods_payment'] == ticket_price['goods_payment']:
            if need_buy_ticket_count > 0:
                global_data.player.buy_goods(self.ticket_goods_id, need_buy_ticket_count, ticket_price['goods_payment'], need_show=False, extra_info={'ticket_lottery_id': self.lottery_id})
                return True
        return False

    def buy_lottery_goods(self, price_info, select_list=None):
        if price_info:
            goods_list = []
            need_use_count = price_info['real_price']
            if not select_list:
                select_list = self.get_random_card_list(need_use_count)
            if not select_list:
                log_error('[LotteryScratchCard] can`t get random grid')
                return True
            for i in range(need_use_count):
                good_info = {'goods_id': self.single_goods_id,
                   'goods_num': 1,
                   'goods_payment_type': price_info['goods_payment'],
                   'need_show': False,
                   'extra_info': {'grid': int(select_list[i])}}
                goods_list.append(good_info)

            self.buy_idx_list = select_list
            self.show_buying_process(need_use_count)
            global_data.player.buy_multi_goods(goods_list)
            return True
        return False

    def show_buying_process(self, need_use_count):
        self.use_ticket_count = need_use_count
        global_data.emgr.refresh_lottery_btn_enable.emit(False)
        ScreenLockerUI(None, False)
        return

    def get_special_multi_scratch_price_info(self, ticket_goods_id, single_goods_id, ticket_item_no, max_scratch_num):
        price_info = get_mall_item_price(single_goods_id)[0]
        remain_card = CARD_SUM - len(self.open_card)
        if remain_card > max_scratch_num:
            remain_card = max_scratch_num
        real_goods_price = price_info['real_price']
        real_cost_price = real_goods_price * remain_card
        has_ticket_num = global_data.player.get_item_money(ticket_item_no) if global_data.player else 0
        real_need_buy_count = real_cost_price - has_ticket_num
        money_price_info = get_mall_item_price(ticket_goods_id, real_need_buy_count)[0]
        money_price_info['need_buy_ticket_count'] = real_need_buy_count
        if real_need_buy_count <= 0:
            ticket_price_info = {'goods_payment': price_info.get('goods_payment'),'original_price': real_cost_price,
               'real_price': real_cost_price
               }
            return (
             [
              ticket_price_info], False)
        else:
            if real_need_buy_count > 0 and real_need_buy_count < remain_card:
                ticket_price_info = {'goods_payment': price_info.get('goods_payment'),'original_price': has_ticket_num,
                   'real_price': has_ticket_num
                   }
                return (
                 [
                  ticket_price_info, money_price_info], False)
            return (
             [
              money_price_info], False)

    def on_scratch_drag_end(self, select_idx_list, cancel_callback=None, confirm_callback=None):
        self.buy_idx_list = select_idx_list
        self.scratch_confirm_widget = LotteryScratchItemWidget(main_widget=self, lottery_id=self.lottery_id, scratch_select_list=select_idx_list, scratch_open_list=six_ex.keys(self.open_card), half_single_get_price=self.get_special_price_info_for_free_scratch_card_single_lottery(self.free_goods_id), get_price=lambda select_num: self.get_special_multi_scratch_price_info(self.ticket_goods_id, self.single_goods_id, self.ticket_item_no, select_num), half_single_buy_logic=lambda select_list: self.special_buy_logic_for_free_scratch_card_single_lottery(self.free_goods_id, select_list=select_list), buy_logic=self.special_buy_multi_logic, close_cb=cancel_callback, confirm_cb=confirm_callback)

    def on_click_btn_exchange(self, *args):
        self.scratch_main_widget.parent_hide()
        self.scratch_exchange_widget.parent_show()

    def on_click_btn_exit_exchange(self, *args):
        self.scratch_main_widget.parent_show()
        self.scratch_exchange_widget.parent_hide()

    def on_click_btn_describe(self, *args):
        dlg = GameRuleDescUI()
        title, content = self.data.get('rule_desc', [608080, 608081])
        dlg.set_lottery_rule(title, content)

    def on_click_btn_show(self, *args):
        jump_to_display_detail_by_item_no(self.final_reward_item, {'skin_list': True})

    def on_click_btn_gift(self, *args):
        self.panel.RecoverAnimationNodeState('head_loop')
        self.panel.StopAnimation('head_loop')
        global_data.achi_mgr.set_cur_user_archive_data(self.show_tip_key, 1)
        from logic.comsys.lottery.LotteryMultiExclusiveGiftUI import LotteryMultiExclusiveGiftUI
        gift_template = self.data['exclusive_gift'].get('gift_template', '')
        LotteryMultiExclusiveGiftUI(None, self.data['exclusive_gift'], gift_template=gift_template)
        return

    def refresh_price(self):
        self.open_card = global_data.player.get_reward_intervene_count(self.data['table_id']) if global_data.player else {}
        self.open_num = len(self.open_card)
        card_remain = self.card_sum - self.open_num
        if card_remain < 5 and card_remain > 0:
            self.panel.btn_many.lab_times.SetString(get_text_by_id(633840).format(card_remain))
        elif card_remain > 5:
            self.panel.btn_many.lab_times.SetString(get_text_by_id(633840).format(5))
        else:
            self.panel.btn_many.lab_times.SetString(get_text_by_id(633840).format(5))
            self.panel.btn_many.price.setVisible(False)
            self.panel.btn_once.price.setVisible(False)
        if self.check_price_free_single_scratch_valid(self.free_goods_id):
            self.panel.btn_once.temp_red.setVisible(card_remain > 0)
            self.panel.btn_once.lab_times.SetString(self.free_text_id)
        else:
            self.panel.btn_once.temp_red.setVisible(False)
            self.panel.btn_once.lab_times.SetString(get_text_by_id(633840).format(1))

    def get_event_conf(self):
        econf = {'display_model_end_show_anim': self.on_model_end_show_anim,
           'receive_lottery_result': self.on_receive_lottery_result
           }
        return econf

    def on_receive_lottery_result(self, item_list, origin_list, *args):
        if not self.panel.isVisible():
            return
        self.receive_reward_count += 1
        self.reward_item_list.extend(item_list)
        self.reward_origin_list.extend(origin_list)
        if self.receive_reward_count == self.use_ticket_count:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.scratch_main_widget.reset_buy_idx_list()),
             cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound('lottery_spluse')),
             cc.CallFunc.create(lambda : self.scratch_main_widget.set_buy_idx_list(self.buy_idx_list)),
             cc.DelayTime.create(1.0),
             cc.CallFunc.create(lambda : self.receive_all_lottery_result())]))

    def receive_all_lottery_result(self):
        global_data.emgr.on_lottery_ended_event.emit()
        global_data.emgr.receive_award_succ_event_from_lottery.emit(self.reward_item_list, self.reward_origin_list)
        global_data.emgr.player_money_info_update_event.emit()
        self.receive_reward_count = 0
        self.use_ticket_count = 0
        self.reward_item_list = []
        self.reward_origin_list = []

    def on_model_end_show_anim(self):
        if not self.is_first_show_model:
            return
        self.panel.setVisible(True)
        self.is_first_show_model = False
        self.scratch_main_widget.parent_show()

    def show(self):
        self.panel.setVisible(True)
        if self.is_first_show_model:
            return
        if self.is_show_scratch:
            self.scratch_main_widget.parent_show()
        else:
            self.scratch_exchange_widget.parent_show()

    def hide(self):
        self.panel.setVisible(False)
        self.is_first_show_model = False
        if self.scratch_confirm_widget:
            self.scratch_confirm_widget.close()
        global_data.emgr.set_lottery_reward_info_label_visible.emit(True)

    def refresh(self):
        self.refresh_price()

    def check_per_day_model_display(self, show_model_id=None):
        state = global_data.achi_mgr.get_cur_user_archive_data(SHOW_MODEL_DISPLAY_KEY.format(self.lottery_id), None)
        if (not state or int(state) != get_rela_day_no()) and show_model_id not in self.exchange_item_list:
            self.panel.setVisible(False)
            self.scratch_main_widget.parent_hide()
            self.is_show_scratch = True
            self.is_first_show_model = True
            self.on_change_show_reward(self.final_reward_item)
            global_data.achi_mgr.set_cur_user_archive_data(SHOW_MODEL_DISPLAY_KEY.format(self.lottery_id), get_rela_day_no())
            return True
        else:
            return False

    def refresh_show_model(self, show_model_id=None):
        if self.panel.nd_shop.isVisible():
            self.scratch_exchange_widget.refresh_show_model()
        else:
            self.check_per_day_model_display(show_model_id)

    def get_is_visible(self):
        return self.panel and self.panel.isVisible()

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        if not self.scratch_exchange_widget:
            return
        if not self.exchange_item_list:
            global_data.game_mgr.show_tip(get_text_by_id(12128))
            return
        self.scratch_main_widget.parent_hide()
        self.scratch_exchange_widget.parent_show(goods_id)

    def on_finalize_panel(self):
        if self.scratch_confirm_widget:
            self.scratch_confirm_widget.close()
        if self.scratch_main_widget:
            self.scratch_main_widget.destroy()
        if self.scratch_buy_widget:
            self.scratch_buy_widget.destroy()
        if self.scratch_exchange_widget:
            self.scratch_exchange_widget.destroy()
        self.scratch_confirm_widget = None
        self.scratch_exchange_widget = None
        self.scratch_main_widget = None
        self.scratch_buy_widget = None
        super(LotteryScratchCardWidget, self).on_finalize_panel()
        return