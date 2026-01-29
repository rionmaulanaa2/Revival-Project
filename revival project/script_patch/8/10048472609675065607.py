# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryMultiLayerTurntableWidget.py
from __future__ import absolute_import
from six.moves import range
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget, TURNTABLE_ANIM_PARAM_KEY_LIST
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE, ITEM_PASS_STATE, ITEM_CHOSEN_STATE, ITEM_LOOP_STATE
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT
from logic.gutils.mall_utils import get_goods_item_lottery_table_id, get_lottery_turntable_item_data_by_goods_id
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.utils.timer import CLOCK
ITEM_ID_INDEX = 0
ITEM_COUNT_INDEX = 1
DRAW_COUNT_INDEX = 0
GOODS_ID_INDEX = 1

class LotteryMultiLayerTurntableWidget(LotteryCommonTurntableWidget):

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
        self.cur_single_goods_id = None
        self.turntable_item_list = [ get_lottery_turntable_item_data_by_goods_id(self.single_goods_id_list[i][0][GOODS_ID_INDEX]) for i in range(self.layer_count) ]
        self.turntable_item_list.append(self.turntable_item_list[-1])
        self.table_id_list = [ get_goods_item_lottery_table_id(self.single_goods_id_list[i][0][GOODS_ID_INDEX]) for i in range(self.layer_count) ]
        self.table_id_list.append(self.table_id_list[-1])
        self.nd_belong_layer = {}
        self.refresh_round_data(only_data=True)
        self.last_click_layer = self.layer_count - 1
        self.show_model_id = self.turntable_item_list[self.last_click_layer][0][ITEM_ID_INDEX]
        self.nd_item_map = {}
        self.cur_init_layer = 0
        self.scroll_layer_timer = None
        self.price_color = [2366765, '#SR', '#BC']
        return

    def init_panel(self):
        super(LotteryMultiLayerTurntableWidget, self).init_panel()

        @global_unique_click(self.nd_turntable.img_up)
        def OnClick(*args):
            self.panel.list_lottery.ScrollToTop(0.2)

    def get_nd_got(self, nd, item_idx):
        belong_layer = self.nd_belong_layer[nd]
        if global_data.player.get_reward_intervene_count(self.table_id_list[belong_layer]).get(str(item_idx), 0) > 0:
            return nd.nd_got
        return nd.nd_giving

    def check_item_got(self, nd, item_id, item_idx):
        belong_layer = self.nd_belong_layer[nd]
        table_id = self.table_id_list[belong_layer]
        main_item_idx = str(ITEM_ID_INDEX)
        all_got = global_data.player.get_reward_intervene_count(table_id).get(main_item_idx, 0) > 0
        self_drawn = global_data.player.get_reward_intervene_count(table_id).get(str(item_idx), 0) > 0
        return all_got or self_drawn

    def on_click_turntable_item_for_show_model(self, item_id, force=False, refresh_ui_state=True, click_layer=0):
        if self.last_click_layer == click_layer and self.show_model_id == item_id and not force:
            return
        else:
            if refresh_ui_state:
                if self.need_show_choose_tag:
                    last_click_node = self.nd_item_map[self.last_click_layer].get(self.show_model_id, None)
                    last_click_node and last_click_node.nd_chosen.setVisible(False)
                    item_id in self.nd_item_map[click_layer] and self.nd_item_map[click_layer][item_id].nd_chosen.setVisible(True)
                if self.need_clear_chosen_anim:
                    self.turntable_widget.stop_turntable_item_state_anim(ITEM_CHOSEN_STATE)
                    self.turntable_widget.stop_turntable_item_state_anim(ITEM_LOOP_STATE)
                    self.need_clear_chosen_anim = False
            elif self.need_show_choose_tag and self.panel.btn_once.IsEnable():
                if item_id in self.nd_item_map[click_layer] and not self.nd_item_map[click_layer][item_id].nd_chosen.isVisible() and not self.need_clear_chosen_anim:
                    last_click_node = self.nd_item_map[self.last_click_layer].get(self.show_model_id, None)
                    last_click_node and last_click_node.nd_chosen.setVisible(False)
                    item_id in self.nd_item_map[click_layer] and self.nd_item_map[click_layer][item_id].nd_chosen.setVisible(True)
            self.show_model_id = item_id
            self.last_click_layer = click_layer
            self.on_change_show_reward(item_id)
            return

    def _get_turntable_default_item_node(self):
        return self.nd_turntable.temp_item_1_1

    def init_item_event_func_for_show_model(self, nd, item_id, item_count):
        if self.need_show_choose_tag:
            if self.cur_init_layer not in self.nd_item_map:
                self.nd_item_map[self.cur_init_layer] = {}
            self.nd_item_map[self.cur_init_layer][item_id] = nd

        @global_unique_click(nd.nd_click)
        def OnClick(btn, touch, click_layer=self.cur_init_layer):
            self.on_click_turntable_item_for_show_model(item_id, click_layer=click_layer)

        @nd.nd_click.unique_callback()
        def OnBegin(*args):
            self.end_scroll_layer_timer()

    def get_chosen_action_extra_delay_time(self, nd, item_id):
        layer = self.nd_belong_layer.get(nd, -1)
        if str(item_id) == self.turntable_item_list[layer][0][ITEM_ID_INDEX]:
            return 0.8
        return 0.0

    def default_play_item_chosen_anim_for_show_model(self, nd, anim_name, item_id):
        super(LotteryMultiLayerTurntableWidget, self).default_play_item_chosen_anim_for_show_model(nd, anim_name, item_id)
        layer = self.nd_belong_layer.get(nd, -1)
        if layer >= 0:
            if str(item_id) == self.turntable_item_list[layer][0][ITEM_ID_INDEX]:
                nd = getattr(self.nd_turntable, 'nd_%d' % (layer + 1))
                nd and nd.setLocalZOrder(1)
                nd = getattr(self.nd_turntable, 'temp_lantern_%d' % (layer + 1))
                nd and nd.PlayAnimation('chosen')

                def play_core_item_chosen_anim():
                    if not self.nd_turntable:
                        return
                    nd = getattr(self.nd_turntable, 'temp_line_%d' % (layer + 1))
                    nd and nd.PlayAnimation('chosen_gold')

                global_data.game_mgr.register_logic_timer(play_core_item_chosen_anim, interval=0.7, times=1, mode=CLOCK)

    def _set_layer_tag_visible(self, layer, visible):
        nd = getattr(self.nd_turntable, 'bar_bg_%d' % (layer + 1))
        nd and nd.setVisible(visible)
        nd = getattr(self.nd_turntable, 'temp_line_%d' % (layer + 1))
        if nd:
            nd.setVisible(visible)
            func = nd.PlayAnimation if visible else nd.StopAnimation
            func('loop')

    def _set_layer_delighted(self, layer, delighted):
        nd = getattr(self.nd_turntable, 'temp_lantern_%d' % (layer + 1))
        nd and nd.img_lantern_1.SetEnable(delighted)

    def scroll_callback(self, *args):
        self.end_scroll_layer_timer()

    def init_turntable_widget(self):
        self.nd_turntable = self.panel.list_lottery.GetItem(0)
        for layer in range(self.layer_count):
            self._set_layer_tag_visible(layer, False)
            self._set_layer_delighted(layer, False)
            layer_capacity = len(self.turntable_item_list[layer])
            layer_num = layer + 1
            for index in range(1, layer_capacity + 1):
                nd = getattr(self.nd_turntable, 'temp_item_%d_%d' % (layer_num, index), None)
                if nd:
                    self.nd_belong_layer[nd] = layer
                else:
                    self.turntable_item_list[layer] = self.turntable_item_list[layer][:index - 1]
                    break

        self.scroll_layer_timer = global_data.game_mgr.register_logic_timer(self.scroll_to_cur_layer, interval=3.5, times=1, mode=CLOCK)
        self.panel.list_lottery.addEventListener(self.scroll_callback)
        kwargs = {}
        turntable_anim_param = self.custom_conf.get('turntable_anim_param', None)
        if turntable_anim_param:
            for i, param in enumerate(turntable_anim_param):
                kwargs[TURNTABLE_ANIM_PARAM_KEY_LIST[i]] = param

        self.need_show_choose_tag = bool(self.custom_conf['show_choose_tag'])
        self.need_refresh_model_for_lottery_result = bool(self.custom_conf['refresh_model_for_lottery_result'])
        if self.custom_conf['show_choose_item_model']:
            kwargs['init_item_event_func'] = self.init_item_event_func_for_show_model
        self.turntable_widget_init_kwargs.update(kwargs)
        self.turntable_widget_init_kwargs['get_item_action_extra_delay_func_map'] = {ITEM_CHOSEN_STATE: self.get_chosen_action_extra_delay_time
           }
        need_show_got = bool(self.custom_conf['show_got_tag'])
        need_anim_skip_got_item = bool(self.custom_conf['anim_skip_got_item'])
        for i in range(self.layer_count):
            self.cur_init_layer = i
            self.turntable_widgets.append(LotteryTurntableWidget(self, self.nd_turntable, self.lottery_id, turntable_item_list=self.turntable_item_list[i], nd_item_format=('temp_item_%d_{}' % (i + 1)), nd_click_name='nd_click', item_anim_name_map=self.get_item_anim_name_map(), play_item_anim_func_map=self.get_play_item_anim_func_map(), need_show_got=need_show_got, get_nd_got_func=self.get_nd_got, check_item_got_func=self.check_item_got, need_anim_skip_got_item=need_anim_skip_got_item, **self.turntable_widget_init_kwargs))

        self.turntable_widgets.append(self.turntable_widgets[-1])
        self.turntable_widget = self.turntable_widgets[self.cur_layer]
        self._set_layer_tag_visible(self.cur_layer, True)
        self._set_layer_delighted(self.cur_layer, True)
        return

    def buying_callback(self, lottery_count):
        self.cur_draw_lottery_count = lottery_count
        self._stop_buy_button_loop_anim()
        if self.need_show_choose_tag and self.show_model_id in self.nd_item_map[self.last_click_layer]:
            self.nd_item_map[self.last_click_layer][self.show_model_id].nd_chosen.setVisible(False)
        self.turntable_widget.stop_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self.turntable_widget.play_turntable_animation(lottery_count)
        self._end_auto_switch_show_model_timer()
        self.end_scroll_layer_timer()
        if self.need_skip_anim:
            self.scroll_to_cur_layer(duration=0.2)
        else:
            self.scroll_layer_timer = global_data.game_mgr.register_logic_timer(self.scroll_to_cur_layer, interval=3, times=1)

    def on_finalize_panel(self):
        super(LotteryMultiLayerTurntableWidget, self).on_finalize_panel()
        self.end_scroll_layer_timer()
        self.nd_turntable = None
        for index, turntable_widget in enumerate(self.turntable_widgets):
            if index == self.cur_layer:
                continue
            turntable_widget.destroy()

        self.turntable_widgets = []
        self.nd_belong_layer = {}
        self.nd_item_map = {}
        return

    def play_panel_show_anim(self, flag):
        super(LotteryMultiLayerTurntableWidget, self).play_panel_show_anim(flag)
        func = self.nd_turntable.PlayAnimation if flag else self.nd_turntable.StopAnimation
        func('loop')
        func('loop_arrow')
        for layer in range(1, self.layer_count + 1):
            nd = getattr(self.nd_turntable, 'temp_lantern_%d' % layer)
            if flag:
                func = nd.PlayAnimation if 1 else nd.StopAnimation
                func('show')
                func('loop')

    def show(self):
        if self.panel.isVisible() and self.exchange_reward_widget and self.exchange_reward_widget.visible:
            return
        self.panel.setVisible(True)
        if self.custom_conf['hide_limit_count']:
            global_data.emgr.hide_lottery_main_ui_elements.emit(True, 'lab_num_times')
        if self.panel.btn_back:
            global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', False)
        if self.exchange_reward_widget:
            if not self.exchange_reward_widget.visible and not self.is_visible_close:
                self.play_panel_show_anim(True)
                for turntable_widget in self.turntable_widgets:
                    turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)

            if self.is_visible_close:
                self.exchange_reward_widget.visible = True
        else:
            self.play_panel_show_anim(True)
            for turntable_widget in self.turntable_widgets:
                turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)

        self._begin_auto_switch_show_model_timer()

    def end_scroll_layer_timer(self):
        if self.scroll_layer_timer:
            global_data.game_mgr.unregister_logic_timer(self.scroll_layer_timer)
            self.scroll_layer_timer = None
        return

    def scroll_to_cur_layer(self, duration=0.6):
        if self.cur_layer < self.layer_count / 2:
            self.panel.list_lottery.ScrollToBottom(duration)
        else:
            self.panel.list_lottery.ScrollToTop(duration)
        self.end_scroll_layer_timer()

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

        for draw_count, goods_id in self.single_goods_id_list[self.cur_layer]:
            if drawn_count < draw_count:
                self.cur_single_goods_id = goods_id
                break

        if not only_data:
            self.turntable_widget = self.turntable_widgets[self.cur_layer]
            self._set_layer_tag_visible(self.cur_layer, True)
            self._set_layer_delighted(self.cur_layer, True)
            self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)

    def refresh_show_model(self, show_model_id=None):
        if self.data.get('show_shop'):
            if self.exchange_reward_widget and self.exchange_reward_widget.visible:
                self.exchange_reward_widget.refresh_show_model(show_model_id)
                return
        if self.need_show_model_in_main_panel:
            if self.custom_conf['show_choose_item_model']:
                if show_model_id:
                    target_layer = 0
                    for i in range(self.layer_count):
                        if self.turntable_item_list[i][ITEM_ID_INDEX] == str(show_model_id):
                            target_layer = i
                            break

                    self.on_click_turntable_item_for_show_model(show_model_id, force=True, click_layer=target_layer)
                else:
                    self.on_click_turntable_item_for_show_model(self.show_model_id, force=True, refresh_ui_state=False, click_layer=self.last_click_layer)
            elif self.auto_show_model_id_list:
                if show_model_id in self.auto_show_model_id_list:
                    self.show_model_index = self.auto_show_model_id_list.index(show_model_id)
                    self.show_model_id = show_model_id
                    self.on_change_show_reward(show_model_id)
                else:
                    self.on_change_show_reward(self.show_model_id)
            else:
                self.on_change_show_reward(self.show_model_id)

    def on_receive_lottery_result(self, item_list, origin_list):
        if len(item_list) > 1:
            cur_layer_item_list = self.turntable_item_list[self.cur_layer]
            sorted_item_list, sorted_origin_list, correspond_index_list = [], [], []
            for i in range(len(item_list)):
                if origin_list[i]:
                    item_info = origin_list[i] if 1 else item_list[i]
                    correspond_index = cur_layer_item_list.index([str(item_info[0]), item_info[1]])
                    correspond_index_list.append((correspond_index, i))

            correspond_index_list.sort()
            for index_map in correspond_index_list:
                index = index_map[1]
                sorted_item_list.append(item_list[index])
                sorted_origin_list.append(origin_list[index])

            item_list, origin_list = sorted_item_list, sorted_origin_list
        self.turntable_widget.set_turntable_items_got(item_list, origin_list, force_play_chosen_anim_when_skip=self.cur_draw_lottery_count == SINGLE_LOTTERY_COUNT)