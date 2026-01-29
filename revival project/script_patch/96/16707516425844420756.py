# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryDragonBoatFestivalWidget.py
from __future__ import absolute_import
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryBuyWidget import LotteryBuyWidget
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE, ITEM_PASS_STATE, ITEM_CHOSEN_STATE, ITEM_LOOP_STATE
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, DARK_PRICE_COLOR
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.mall_utils import get_lottery_turntable_item_data
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_lang_name
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils.item_utils import RARE_DEGREE_ICON, get_item_rare_degree
ALL_SUPPORT_LANG_NAME = {
 'cn', 'en', 'tw', 'jp'}
MULTIPLY_TEXT = get_text_by_id(602012)

class LotteryDragonBoatFestivalWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryDragonBoatFestivalWidget, self).init_parameters()
        self.turntable_item_list = get_lottery_turntable_item_data(self.lottery_id)
        self.max_draw_count = len(self.turntable_item_list)
        self.all_round_finished = False
        self.show_model_id = self.turntable_item_list[0][0]
        self.archive_data = ArchiveManager().get_archive_data('lottery_turntable_skip_anim')
        self.need_skip_anim = self.archive_data.get(self.lottery_id, False)
        self.nd_item_map = {}
        self.need_clear_chosen_anim = False
        self.cur_single_goods_id = self.data['single_goods_id']
        self.single_goods_id_list = [self.cur_single_goods_id]
        self.single_goods_id_list.extend(self.data['extra_single_goods_id'])
        self.single_goods_id_list.append(self.single_goods_id_list[-1])
        self.btn_click_anim_timer = None
        return

    def init_panel(self):
        super(LotteryDragonBoatFestivalWidget, self).init_panel()

        @global_unique_click(self.panel.btn_skip)
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            btn.img_skip.setVisible(self.need_skip_anim)

        self.panel.btn_skip.img_skip.setVisible(self.need_skip_anim)

        @global_unique_click(self.panel.btn_back.btn_back)
        def OnClick(btn, touch):
            global_data.ui_mgr.close_ui('LotteryMainUI')

        self._init_turntable_widget()
        self._init_buy_widget()
        cur_lang_name = get_cur_lang_name()
        self.panel.nd_en.setVisible(False)
        nd_lang = getattr(self.panel, 'nd_{}'.format(cur_lang_name))
        if nd_lang is None:
            nd_lang = self.panel.nd_en
        nd_lang.setVisible(True)

        @global_unique_click(nd_lang.btn_help)
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        self.refresh_round_data()
        self.panel.RecordAnimationNodeState('loop_02')
        return

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended
           }
        return econf

    def _on_click_turntable_item(self, item_id, force=False):
        if self.show_model_id == item_id and not force:
            return
        else:
            last_click_node = self.nd_item_map.get(self.show_model_id, None)
            last_click_node.img_choose.setVisible(False)
            self.show_model_id = item_id
            self.nd_item_map[self.show_model_id].img_choose.setVisible(True)
            self.on_change_show_reward(item_id)
            if self.need_clear_chosen_anim:
                self.turntable_widget.stop_turntable_item_state_anim(ITEM_CHOSEN_STATE)
                self.need_clear_chosen_anim = False
            return

    def _init_turntable_widget(self):

        def check_item_got(nd, item_id, item_idx):
            return global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0) > 0

        def init_item_data_func(nd, item_id, item_count):
            nd.lab_num.setVisible(False)
            self.nd_item_map[item_id] = nd
            if item_id == '201800336':
                nd.temp_kind.bar_level.SetDisplayFrameByPath('', RARE_DEGREE_ICON[get_item_rare_degree(int(item_id))])

        def init_item_event_func(nd, item_id, item_count):

            @global_unique_click(nd.btn_item_bg)
            def OnClick(btn, touch):
                self._on_click_turntable_item(item_id)

        def play_item_chosen_anim(nd, anim_name, item_id):
            self.panel.StopAnimation('click')
            self.panel.StopAnimation('loop_02')
            if self.btn_click_anim_timer:
                global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)
            self.panel.PlayAnimation('reward_show')
            if type(anim_name) == str:
                nd.PlayAnimation(anim_name)
            else:
                for single_anim_name in anim_name:
                    nd.PlayAnimation(single_anim_name)

            self.show_model_id = item_id
            self.on_change_show_reward(item_id)
            self.need_clear_chosen_anim = True

        self.turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, turntable_item_list=self.turntable_item_list, item_anim_name_map={ITEM_DEFAULT_STATE: 'loop',
           ITEM_PASS_STATE: 'pass',
           ITEM_CHOSEN_STATE: ('choosed', 'loop_end'),
           ITEM_LOOP_STATE: 'none'
           }, play_item_anim_func_map={ITEM_CHOSEN_STATE: play_item_chosen_anim
           }, init_item_data_func=init_item_data_func, init_item_event_func=init_item_event_func, max_single_interval=0.8, med_single_interval=0.15, min_single_interval=0.07, high_speed_count_percent=0.8, max_delighted_time=3, need_show_got=True, get_nd_got_func=lambda nd, idx: nd.img_get, check_item_got_func=check_item_got, need_anim_skip_got_item=True)
        self.nd_item_map[self.show_model_id].img_choose.setVisible(True)

    def check_buy_action_disabled(self, lottery_count):
        if self.all_round_finished:
            global_data.game_mgr.show_tip(get_text_by_id(82220))
            return True
        return False

    def _init_buy_widget(self):

        def update_price_info_callback(nd, lottery_count):
            price_width = 0
            for price_item in nd.temp_price.GetAllItem():
                if price_item.isVisible():
                    price_width += price_item.GetContentSize()[0]

            price_width -= 50
            lab_size = nd.lab_once.GetContentSize()
            lab_width = lab_size[0]
            total_width = price_width + lab_width
            half_width = total_width / 2
            price_x_offset = price_width / 2 - half_width
            lab_x_offset = half_width - lab_width / 2
            nd.temp_price.SetPosition('50%{}'.format(int(price_x_offset)), nd.temp_price.getPosition().y)
            nd.lab_once.SetPosition('50%{}'.format(int(lab_x_offset)), nd.lab_once.getPosition().y)

        def buying_callback(lottery_count):
            self.nd_item_map[self.show_model_id].img_choose.setVisible(False)
            self.turntable_widget.play_turntable_animation(lottery_count)
            if self.btn_click_anim_timer:
                global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)

            def play_btn_click_anim():
                self.panel.PlayAnimation('click')
                self.panel.PlayAnimation('loop_02')
                self.btn_click_anim_timer = None
                return

            self.btn_click_anim_timer = global_data.game_mgr.register_logic_timer(play_btn_click_anim, interval=3, times=1)

        def lottery_data_ready_callback(bought_successfully):
            if not bought_successfully:
                self.turntable_widget.lottery_failed()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once
           }, price_color=DARK_PRICE_COLOR, update_price_info_callbacks={SINGLE_LOTTERY_COUNT: update_price_info_callback
           }, buying_callback=buying_callback, lottery_data_ready_callback=lottery_data_ready_callback)

    def on_finalize_panel(self):
        super(LotteryDragonBoatFestivalWidget, self).on_finalize_panel()
        if self.turntable_widget:
            self.turntable_widget.destroy()
            self.turntable_widget = None
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        if self.btn_click_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)
            self.btn_click_anim_timer = None
        self.nd_item_map = {}
        self.archive_data[self.lottery_id] = self.need_skip_anim
        self.archive_data.save()
        self.archive_data = None
        return

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        global_data.emgr.hide_lottery_main_ui_elements.emit(True, 'lab_num_times')
        self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', False)

    def hide(self):
        self.panel.setVisible(False)
        global_data.emgr.hide_lottery_main_ui_elements.emit(False, 'lab_num_times')
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', True)

    def refresh(self):
        self.buy_widget.refresh()
        self.refresh_round_data()

    def refresh_show_model(self, show_model_id=None):
        if show_model_id:
            self._on_click_turntable_item(str(show_model_id), force=True)
        else:
            self.on_change_show_reward(self.show_model_id)

    def on_receive_lottery_result(self, item_list, origin_list):
        self.turntable_widget.set_turntable_items_got(item_list, origin_list, force_play_chosen_anim_when_skip=True)

    def refresh_round_data(self):
        drawn_count = 0
        for item_id, item_count in self.turntable_item_list:
            drawn_count += global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0)

        self.cur_single_goods_id = self.single_goods_id_list[drawn_count]
        self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
        self.all_round_finished = self.max_draw_count == drawn_count
        self.panel.lab_repeat_tips.setVisible(True)
        if drawn_count == 0:
            self.panel.lab_repeat_tips.SetString(82305)
        elif drawn_count == 4:
            self.panel.lab_repeat_tips.SetString(82306)
        elif drawn_count == 6 and global_data.player.get_reward_intervene_count(self.data['table_id']).get(self.turntable_item_list[0][0], 0) <= 0:
            self.panel.lab_repeat_tips.SetString(82307)
        else:
            self.panel.lab_repeat_tips.setVisible(False)

    def on_lottery_ended(self):
        self.refresh_round_data()
        self.panel.RecoverAnimationNodeState('loop_02')