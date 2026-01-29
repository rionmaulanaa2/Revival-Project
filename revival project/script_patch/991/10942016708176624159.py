# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryOptionalTurntableWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget
from .LotterySelectRewardsWidget import LotterySelectRewardsWidget
from .LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT
import six.moves.collections_abc
import collections

class LotteryOptionalTurntableWidget(LotteryCommonTurntableWidget):

    def init_parameters(self):
        super(LotteryOptionalTurntableWidget, self).init_parameters()
        self.need_show_first_enter_tips = self.lottery_id not in self.skip_anim_archive_data.get_conf()
        self.selectable_turntable_item_map = collections.OrderedDict()
        self.global_max_draw_count = len(self.turntable_item_list)
        self.all_selectable_items = set()
        for index, item_info_list in enumerate(self.turntable_item_list):
            if isinstance(item_info_list[0], list):
                self.selectable_turntable_item_map[index] = item_info_list
                self.global_max_draw_count += len(item_info_list) - 1
                for item_id, _ in item_info_list:
                    self.all_selectable_items.add(item_id)

        self.cur_turntable_item_list = list(self.turntable_item_list)
        self.refresh_selected_items_info(update_panel=False)
        self.update_cur_turntable_item_list()
        self.show_model_id = self.cur_turntable_item_list[0][0]
        self.nd_force_select_reward_btn_list = []

    def init_panel(self):
        super(LotteryOptionalTurntableWidget, self).init_panel()
        self.select_rewards_widget = None
        return

    def get_event_conf(self):
        econf = super(LotteryOptionalTurntableWidget, self).get_event_conf()
        econf.update({'receive_award_end_event': self.on_check_show_remind_select_rewards_dlg
           })
        return econf

    def check_item_drawn_func(self, item_id):
        return self.check_item_got(None, item_id)

    def check_item_got_func(self, item_id):
        return global_data.player.get_item_num_by_no(int(item_id))

    def select_rewards_callback(self, new_selected_items_set):
        self.refresh_selected_items_info(new_selected_items_set=new_selected_items_set)
        global_data.player.request_choose_reward(self.data['table_id'], list(new_selected_items_set))
        self.update_cur_turntable_item_list()
        self.nd_force_select_reward_btn_list = []
        self.turntable_widget.refresh_turntable_item_list(self.cur_turntable_item_list)
        self.on_click_turntable_item_for_show_model(self.cur_turntable_item_list[0][0])

    def show_select_rewards_widget(self):
        if self.cur_selectable_items_all_drawn:
            cur_selected_items_set = set() if 1 else self.cur_selected_items_set.copy()
            self.select_rewards_widget = self.select_rewards_widget or LotterySelectRewardsWidget(None, six_ex.values(self.selectable_turntable_item_map), cur_selected_items_set, self.check_item_drawn_func, self.check_item_got_func, self.select_rewards_callback)
        self.select_rewards_widget.show(cur_selected_items_set)
        return

    def update_cur_turntable_item_list(self):
        for index, item_info_list in six.iteritems(self.selectable_turntable_item_map):
            first_not_got_item_info = None
            for item_info_index, (item_id, item_count) in enumerate(item_info_list):
                if item_id in self.cur_selected_items_set:
                    if self.cur_turntable_item_list[index] != item_info_list[item_info_index]:
                        self.cur_turntable_item_list[index] = item_info_list[item_info_index]
                    break
                elif not self.check_item_got_func(item_id) and first_not_got_item_info is None:
                    first_not_got_item_info = item_info_list[item_info_index]
            else:
                if first_not_got_item_info is None:
                    self.cur_turntable_item_list[index] = item_info_list[0]
                else:
                    self.cur_turntable_item_list[index] = first_not_got_item_info

        return

    @staticmethod
    def _get_nd_img_reward--- This code section failed: ---

 102       0  LOAD_FAST             1  'index'
           3  POP_JUMP_IF_TRUE     13  'to 13'

 103       6  LOAD_FAST             0  'nd'
           9  LOAD_ATTR             0  'img_reward'
          12  RETURN_END_IF    
        13_0  COME_FROM                '3'

 104      13  LOAD_GLOBAL           1  'getattr'
          16  LOAD_GLOBAL           1  'getattr'
          19  LOAD_FAST             1  'index'
          22  LOAD_CONST            2  1
          25  BINARY_ADD       
          26  BINARY_MODULO    
          27  LOAD_CONST            0  ''
          30  CALL_FUNCTION_3       3 
          33  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 30

    def init_item_data_func(self, nd, item_id, item_count):
        nd.lab_num.SetString('x ' + str(item_count))
        nd.lab_num.setVisible(item_count > 1)
        if nd.img_reward._cur_target_path is None:
            nd.img_reward.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_id))
        elif item_id in self.all_selectable_items:
            if nd.img_reward2:
                for item_info_list in six.itervalues(self.selectable_turntable_item_map):
                    for index, (_item_id, _) in enumerate(item_info_list):
                        if _item_id == item_id:
                            for i in range(len(item_info_list)):
                                i != index and self._get_nd_img_reward(nd, i).setVisible(False)

                            self._get_nd_img_reward(nd, index).setVisible(True)
                            return

            else:
                nd.img_reward.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_id))
        return

    def init_item_event_func_for_show_model(self, nd, item_id, item_count):
        if self.need_show_choose_tag:
            self.nd_item_map[item_id] = nd
        if nd.btn_change:
            self.nd_force_select_reward_btn_list.append(nd.btn_change)
            nd.btn_change.setVisible(self.can_select_rewards)
            nd.btn_change2.setVisible(False)

            @global_unique_click(nd.btn_change)
            def OnClick(btn, touch):
                self.show_select_rewards_widget()

        @global_unique_click(nd.nd_click)
        def OnClick(btn, touch):
            self.on_click_turntable_item_for_show_model(item_id)

    def init_turntable_widget(self):
        self.turntable_widget_init_kwargs['turntable_item_list'] = self.cur_turntable_item_list
        self.turntable_widget_init_kwargs['init_item_data_func'] = self.init_item_data_func
        super(LotteryOptionalTurntableWidget, self).init_turntable_widget()

    def special_buy_logic_func(self, price_info, lottery_count):
        if self.force_select_rewards:
            self.show_select_rewards_widget()
            return True
        return super(LotteryOptionalTurntableWidget, self).special_buy_logic_func(price_info, lottery_count)

    def init_buy_widget(self):
        super(LotteryOptionalTurntableWidget, self).init_buy_widget()

    def refresh_round_data(self):
        if not self.need_refresh_round_data:
            return
        drawn_count, global_drawn_count = (0, 0)
        for index, (item_id, item_count) in enumerate(self.cur_turntable_item_list):
            got_ret = global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0)
            if index in self.selectable_turntable_item_map:
                drawn_count += got_ret
                continue
            drawn_count += got_ret
            global_drawn_count += got_ret

        for item_info_list in six.itervalues(self.selectable_turntable_item_map):
            for item_id, item_count in item_info_list:
                global_drawn_count += global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0)

        self.cur_single_goods_id = self.single_goods_id_list[global_drawn_count]
        self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
        self.all_round_finished = self.global_max_draw_count == global_drawn_count
        if 'round_tips_info' in self.custom_conf:
            self.panel.lab_repeat_tips.setVisible(True)
            for round_tip in self.custom_conf['round_tips_info']:
                round_count, text_id = round_tip[:2]
                if round_count == drawn_count:
                    if len(round_tip) > 2:
                        correspond_item_id = str(round_tip[2])
                        if global_data.player.get_reward_intervene_count(self.data['table_id']).get(correspond_item_id, 0) > 0:
                            continue
                    self.panel.lab_repeat_tips.SetString(text_id)
                    break
            else:
                self.panel.lab_repeat_tips.setVisible(False)

    def _get_force_text(self):
        if self.force_select_rewards:
            return 611330
        if self.all_round_finished:
            return 611341
        return ''

    def refresh_selected_items_info(self, update_panel=True, new_selected_items_set=None):
        if new_selected_items_set is None:
            self.cur_selected_items_set = set((str(e) for e in global_data.player.get_reward_choose_list(self.data['table_id'])))
            self.cur_selectable_items_all_drawn = True
            for selected_item in self.cur_selected_items_set:
                if not self.check_item_got(None, selected_item):
                    self.cur_selectable_items_all_drawn = False
                    break

        else:
            self.cur_selectable_items_all_drawn = False
            self.cur_selected_items_set = new_selected_items_set
        all_selectable_items_got = True
        for item_info_list in six.itervalues(self.selectable_turntable_item_map):
            for item_id, item_count in item_info_list:
                if global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0) <= 0:
                    all_selectable_items_got = False
                    break

            if not all_selectable_items_got:
                break

        self.force_select_rewards = not all_selectable_items_got and (not self.cur_selected_items_set or self.cur_selectable_items_all_drawn)
        self.can_select_rewards = not all_selectable_items_got and global_data.player.is_reward_choose_valid(self.data['table_id'])
        if update_panel:
            self.buy_widget.set_force_text(self._get_force_text(), ([], False))
            for nd_btn in self.nd_force_select_reward_btn_list:
                nd_btn.setVisible(self.can_select_rewards)

        return

    def on_finalize_panel(self):
        super(LotteryOptionalTurntableWidget, self).on_finalize_panel()
        if self.select_rewards_widget:
            self.select_rewards_widget.close()
            self.select_rewards_widget = None
        return

    def hide(self):
        super(LotteryOptionalTurntableWidget, self).hide()
        self.select_rewards_widget and self.select_rewards_widget.hide()

    def refresh(self):
        self.refresh_round_data()
        self.refresh_selected_items_info()
        self.refresh_lottery_limit_count()
        self.refresh_limited_item_guarantee_round()
        self.update_exchange_coin_num()
        self.update_remind_exchange_item_id()
        if self.need_show_first_enter_tips and self.force_select_rewards:
            self.show_select_rewards_widget()
            self.need_show_first_enter_tips = False

    def on_lottery_ended(self):
        super(LotteryOptionalTurntableWidget, self).on_lottery_ended()
        self.refresh_selected_items_info()

    def on_check_show_remind_select_rewards_dlg(self):
        if not self.panel.isVisible():
            return
        if self.cur_single_goods_id == self.single_goods_id_list[0] or self.all_round_finished:
            return
        if self.force_select_rewards:
            LotterySmallSecondConfirmWidget(title_text_id=611330, content_text_id=611333, confirm_callback=self.show_select_rewards_widget)