# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryGridWidget.py
from __future__ import absolute_import
import six_ex
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, MODE_SPECIAL
from logic.gutils.mall_utils import get_mall_item_price, has_bought_limit_item, has_yueka_lottery_discount, get_lottery_category_floor_data
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const import shop_const
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryGridItemWidget import LotteryGridItemWidget
from .LotteryPreviewWidget import LotteryPreviewWidget
from .LotteryBuyWidget import LotteryBuyWidget
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.item.item_const import RARE_DEGREE_4, RARE_DEGREE_6
from logic.gcommon import time_utility as tutil
from logic.gutils.mall_utils import get_special_price_info_for_yueka_single_lottery, special_buy_logic_for_yueka_single_lottery
from common.cfg import confmgr
from random import randint
import copy

class LotteryGridWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryGridWidget, self).init_parameters()
        self.item_list = self.get_item_list()
        index = randint(0, len(self.item_list) - 1)
        self.show_model_id = self.item_list[index][0]
        self.has_yueka_lottery_discount = has_yueka_lottery_discount(self.lottery_id, shop_const.GOOD_ID_LOTTERY_HALF_PRICE)
        self.category_floor = get_lottery_category_floor_data(self.lottery_id)
        self.guarantee_rare_degree_list = (RARE_DEGREE_4, RARE_DEGREE_6)

    def update_continual_lottery_info(self):
        is_manland = not G_IS_NA_PROJECT
        is_na_new_preium = self.lottery_id == '18'
        if not self.data.get('first_continual_goods_id', None):
            if is_manland or is_na_new_preium:
                self.has_bought_first_continual_lottery = global_data.player.get_reward_count(self.data['table_id']) >= 10
            else:
                self.has_bought_first_continual_lottery = True
        else:
            self.has_bought_first_continual_lottery = has_bought_limit_item(self.data['first_continual_goods_id'])
        self.panel.nd_first.setVisible(not self.has_bought_first_continual_lottery)
        self.panel.nd_prog.setVisible(self.has_bought_first_continual_lottery and (is_manland or is_na_new_preium))
        self.panel.nd_tag_na.setVisible(self.has_bought_first_continual_lottery and not is_manland and not is_na_new_preium)
        if not self.has_bought_first_continual_lottery:
            reward_count = 0
            if is_manland or is_na_new_preium:
                reward_count = global_data.player.get_reward_count(self.data['table_id'])
            self.panel.prog_first.SetPercentage(reward_count * 0.1 * 100)
        else:
            self.refresh_limited_item_guarantee_round()
        return

    def init_panel(self):
        super(LotteryGridWidget, self).init_panel()

        @global_unique_click(self.panel.btn_question)
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_view)
        def OnClick(*args):
            self.preview_widget.show()

        @global_unique_click(self.panel.temp_review.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        self._init_preview_widget()
        self._init_grid_widget()
        self._init_buy_widget()
        self.update_yueka_lottery_tips()
        if not G_IS_NA_PROJECT or self.lottery_id == '18':
            self.panel.lab_tips.SetString(82092)
        else:
            self.panel.lab_tips.SetString(12093)
        self.update_continual_lottery_info()

    def _init_grid_widget(self):
        if self.lottery_id == MODE_SPECIAL and G_IS_NA_PROJECT:
            percent_up_item_id_set = set()
        else:
            conf = confmgr.get('preview_%s' % self.data['table_id'], 'percent_up_item_goods_id', default={})
            percent_up_item_id_set = set(six_ex.keys(conf))
        self.grid_item_widget = LotteryGridItemWidget(self, self.panel, self.item_list, percent_up_item_id_set, self.show_model)
        self.panel.PlayAnimation('loop_wave')

    def get_item_list(self):
        conf = confmgr.get('preview_%s' % self.data['table_id'])
        layout_info = conf.get('grid_layout', default=[])
        now = tutil.get_server_time()
        for start_time, end_time, item_list in layout_info:
            if start_time <= now <= end_time:
                return copy.deepcopy(item_list)

        return []

    def on_resolution_changed(self):
        if self.grid_item_widget:
            self.grid_item_widget.destroy()
            self.grid_item_widget = None
        self._init_grid_widget()
        self.panel.StopAnimation('show')
        self.panel.nd_show.DelActionFromCache(hash('show'))
        self.panel.PlayAnimation('show')
        self.panel.nd_show.ReConfPosition()
        self.panel.PlayAnimation('loop_wave')
        return

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'refresh_lottery_limited_guarantee_round': self.refresh_limited_item_guarantee_round,
           'refresh_lottery_probability_up_data': self.refresh_probability_up_data
           }
        return econf

    def _init_preview_widget(self):

        def show_callback():
            self.refresh_preview()

        self.preview_widget = LotteryPreviewWidget(self.panel.temp_review, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, close_callback=self.refresh_show_model)

    def _init_buy_widget(self):

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == SINGLE_LOTTERY_COUNT:
                return get_special_price_info_for_yueka_single_lottery(self.lottery_id, price_info)
            return False

        def special_buy_logic_func(price_info, lottery_count):
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                first_continual_goods_id = self.data.get('first_continual_goods_id', None)
                if first_continual_goods_id and not has_bought_limit_item(first_continual_goods_id):
                    price_info = get_mall_item_price(first_continual_goods_id)
                    if price_info:
                        price_info = price_info[0]
                        price_info['goods_id'] = first_continual_goods_id
                        return self.buy_widget.do_buy_lottery(price_info, lottery_count)
            else:
                return special_buy_logic_for_yueka_single_lottery(self.lottery_id, self.panel, price_info, lambda : self.buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count))
            return

        def buying_callback(lottery_count):
            self.preview_widget.hide()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback)

    def show(self):
        self.panel.setVisible(True)
        self.preview_widget.parent_show()
        self.grid_item_widget.play_animation()
        self.panel.PlayAnimation('show')
        global_data.emgr.scene_switch_background.emit('LuckyHouse')
        self.update_continual_lottery_info()
        if global_data.scene_background:
            bg = global_data.scene_background.get_ui('LuckyHouse')
            bg and bg.on_appear()

    def hide(self):
        self.panel.setVisible(False)
        self.preview_widget.parent_hide()
        global_data.emgr.scene_switch_background.emit(None)
        return

    def on_finalize_panel(self):
        super(LotteryGridWidget, self).on_finalize_panel()
        self.destroy_widget('preview_widget')
        self.destroy_widget('buy_widget')
        self.destroy_widget('grid_item_widget')

    def refresh(self):
        self.buy_widget.refresh()
        self.update_continual_lottery_info()
        self.refresh_lottery_limit_count()

    def on_lottery_ended(self):
        if self.has_yueka_lottery_discount:
            self.update_yueka_lottery_tips()
        self.update_continual_lottery_info()

    def refresh_preview(self):
        self.preview_widget.refresh_preview_list(self.lottery_id, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}))
        return

    def force_refresh_preview(self):
        self.preview_widget.refresh_preview_list(self.lottery_id, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}), True)
        return

    def update_yueka_lottery_tips(self):
        self.has_yueka_lottery_discount = has_yueka_lottery_discount(self.lottery_id, shop_const.GOOD_ID_LOTTERY_HALF_PRICE)
        if self.has_yueka_lottery_discount:
            cur_week_day = tutil.get_utc8_weekday()
            data = ArchiveManager().get_archive_data('last_close_yueka_tips_info')
            data['week_day'] = cur_week_day
            data.save()
        self.panel.nd_tips_month.setVisible(self.has_yueka_lottery_discount)
        self.panel.nd_buy_1.img_red.setVisible(self.has_yueka_lottery_discount)

    def refresh_limited_item_guarantee_round(self):
        if not G_IS_NA_PROJECT or self.lottery_id == '18':
            cnt_count = self.panel.list_tag.GetItemCount()
            init_count = 2
            if cnt_count != init_count:
                self.panel.list_tag.SetInitCount(init_count)
            items = self.panel.list_tag.GetAllItem()
            for idx, rare_degree in enumerate(self.guarantee_rare_degree_list):
                max_count, line_no = self.category_floor[str(rare_degree)]
                has_bought_count = global_data.player.get_reward_category_floor(self.data['table_id'], line_no)
                if rare_degree == RARE_DEGREE_4:
                    suffix = 's' if 1 else 's_plus'
                    pic_path = 'gui/ui_res_2/lottery/img_quality_%s.png' % (suffix,)
                    items[idx].img_class.SetDisplayFrameByPath('', pic_path)
                    items[idx].prog_tag.SetPercentage(has_bought_count * 100.0 / max_count)
                    items[idx].lab_tag_num.SetString(get_text_by_id(609508).format(has_bought_count, max_count))
                    items[idx].nd_tag.BindMethod('OnClick', lambda b, t, r=rare_degree: self.on_go_to_preview(r))

        else:
            guarantee_count, max_guarantee_count = global_data.player.get_reward_guarantee_round_data(self.data['table_id'])
            self.panel.prog_tag.SetPercentage(guarantee_count * 100.0 / max_guarantee_count)
            self.panel.lab_tag.SetString(get_text_by_id(609507))
            self.panel.lab_tag_num.SetString(get_text_by_id(609508).format(guarantee_count, max_guarantee_count))

    def on_go_to_preview(self, rare_degree):
        self.preview_widget.show(rare_degree)

    def refresh_probability_up_data(self):
        if not self.grid_item_widget:
            return
        self.grid_item_widget.refresh_item_data(self.item_list)
        self.grid_item_widget.play_animation()
        self.panel.PlayAnimation('show')
        self.force_refresh_preview()

    def refresh_show_model(self, show_model_id=None):
        if self.panel and self.panel.isValid():
            if show_model_id and show_model_id not in self.data['core_item_id_list']:
                show_model_id = None
            if not show_model_id:
                if self.preview_widget.panel.isVisible():
                    self.preview_widget.show()
                    return
                show_model_id = self.show_model_id
            self.grid_item_widget.refresh_show_model(show_model_id)
        return

    def show_model(self, item_id):
        self.on_change_show_reward(item_id)
        bg = global_data.scene_background.get_cur_panel()
        if bg != 'LuckyHouse':
            global_data.emgr.scene_switch_background.emit('LuckyHouse')
            bg = global_data.scene_background.get_ui('LuckyHouse')
            if bg:
                bg.on_appear()

    def hide_preview_widget--- This code section failed: ---

 280       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  JUMP_IF_FALSE_OR_POP    27  'to 27'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'preview_widget'
          21  LOAD_ATTR             3  'hide'
          24  CALL_FUNCTION_0       0 
        27_0  COME_FROM                '12'
          27  POP_TOP          
          28  LOAD_CONST            0  ''
          31  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9