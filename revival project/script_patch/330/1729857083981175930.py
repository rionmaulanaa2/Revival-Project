# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryCommonTurntableWidget.py
from __future__ import absolute_import
import six
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryBuyWidget import LotteryBuyWidget, check_buy_button_lab_and_price_same_y
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE, ITEM_PASS_STATE, ITEM_CHOSEN_STATE, ITEM_LOOP_STATE
from .LotteryExchangeRewardWidget import LotteryExchangeRewardWidget
from logic.comsys.lobby.EntryWidget.ArtCollectionActivityEntryWidget import ArtCollectionActivityEntryWidget
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DARK_PRICE_COLOR
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.mall_utils import get_lottery_turntable_item_data, get_lottery_category_floor_data, get_mall_item_price, get_goods_item_no, get_payment_item_no, get_goods_item_open_date, check_limit_time_lottery_open_info
from logic.gutils.item_utils import get_lobby_item_name
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from common.utils.timer import CLOCK
from common.cfg import confmgr
from math import ceil
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from .LotteryTurntableSecondComfirm import LotteryTurntableSecondComfirm
TURNTABLE_ITEM_ANIM_PREFIX_MAP = {'def': ITEM_DEFAULT_STATE,
   'pas': ITEM_PASS_STATE,
   'cho': ITEM_CHOSEN_STATE,
   'loo': ITEM_LOOP_STATE
   }
STATE_NAME_MAP = {'default': ITEM_DEFAULT_STATE,
   'pass': ITEM_PASS_STATE,
   'chosen': ITEM_CHOSEN_STATE,
   'loop': ITEM_LOOP_STATE
   }
CUSTOM_PLAY_TURNTABLE_ITEM_ANIM_FUNC_NAME = {ITEM_DEFAULT_STATE: 'play_item_default_anim',
   ITEM_PASS_STATE: 'play_item_pass_anim',
   ITEM_CHOSEN_STATE: 'play_item_chosen_anim',
   ITEM_LOOP_STATE: 'play_item_loop_anim'
   }
TURNTABLE_ANIM_PARAM_KEY_LIST = [
 'max_single_interval', 'med_single_interval', 'min_single_interval',
 'high_speed_count_percent', 'max_delighted_time', 'continual_interval']

class LotteryCommonTurntableWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryCommonTurntableWidget, self).init_parameters()
        self.custom_conf = confmgr.get('turntable_lottery_custom_conf', self.lottery_id, default={})
        self.need_show_model_in_main_panel = 'is_cover_ui' not in self.data
        self.auto_show_model_id_list, self.auto_switch_model_interval = [], 0
        self.auto_switch_model_timer = None
        if self.need_show_model_in_main_panel:
            if self.custom_conf['show_choose_item_model']:
                model_ids = get_lottery_turntable_item_data(self.lottery_id)
                model_ids = model_ids[0] if model_ids else None
                self.show_model_id = model_ids[0] if model_ids else None
            else:
                self.auto_show_model_id_list, self.auto_switch_model_interval = self.custom_conf['show_model_id_list']
                self.auto_show_model_count = len(self.auto_show_model_id_list)
                self.show_model_id = self.auto_show_model_id_list[0]
                self.show_model_index = 0
        self.turntable_widget = None
        self.turntable_widget_init_kwargs = {}
        self.need_show_choose_tag = False
        self.need_refresh_model_for_lottery_result = False
        self.nd_item_map = {}
        self.need_clear_chosen_anim = False
        self.exchange_reward_widget = None
        self.exchange_widget_init_kwargs = {}
        self.is_visible_close = False
        self.remind_exchange_archive_data = ArchiveManager().get_archive_data('lottery_remind_exchange_item_id')
        self.cur_remind_exchange_item_id = None
        if 'remind_exchange_item_goods_id_list' in self.custom_conf:
            self.remind_exchange_item_price_list = []
            self.payment_goods_id_map = {}
            for goods_id in self.custom_conf['remind_exchange_item_goods_id_list']:
                item_id = get_goods_item_no(str(goods_id))
                price = get_mall_item_price(str(goods_id))[0]
                self.remind_exchange_item_price_list.append([item_id, get_payment_item_no(price['goods_payment']), price['real_price']])

            for index, goods_id in enumerate(self.custom_conf['remind_exchange_item_goods_id_list']):
                item_id = self.remind_exchange_item_price_list[index][0]
                for _, payment_item_id, _ in self.remind_exchange_item_price_list:
                    if item_id == payment_item_id:
                        self.payment_goods_id_map[item_id] = self.remind_exchange_item_price_list[index][1:]

        self.buy_widget = None
        self.buy_widget_init_kwargs = {}
        self.skip_anim_archive_data = ArchiveManager().get_archive_data('lottery_turntable_skip_anim')
        self.need_skip_anim = self.skip_anim_archive_data.get(self.lottery_id, False)
        self.cur_draw_lottery_count = SINGLE_LOTTERY_COUNT
        self.price_color = DARK_PRICE_COLOR
        self.need_refresh_round_data = False
        if 'extra_single_goods_id' in self.data:
            self.need_refresh_round_data = True
            self.turntable_item_list = get_lottery_turntable_item_data(self.lottery_id)
            self.max_draw_count = len(self.turntable_item_list)
            self.all_round_finished = False
            self.cur_single_goods_id = self.data['single_goods_id']
            self.single_goods_id_list = [self.cur_single_goods_id]
            self.single_goods_id_list.extend(self.data['extra_single_goods_id'])
            self.single_goods_id_list.append(self.single_goods_id_list[-1])
        self.use_lucky_discount = bool(confmgr.get('mall_config', self.data['continual_goods_id'], default={}).get('lucky_discount', None))
        self.category_node_map = {}
        self.title_timer = 0
        self.remain_time = 0
        return

    def on_set_skip_anim_flag(self, btn):
        btn.SetSelect(self.need_skip_anim)
        btn.img_skip and btn.img_skip.setVisible(self.need_skip_anim)

    def init_panel(self):
        super(LotteryCommonTurntableWidget, self).init_panel()
        if self.panel.btn_history:

            @global_unique_click(self.panel.btn_history)
            def OnClick(btn, touch):
                global_data.emgr.lottery_history_open.emit()

        if self.panel.btn_help:

            @global_unique_click(self.panel.btn_help)
            def OnClick(btn, touch):
                dlg = GameRuleDescUI()
                title, content = self.data.get('rule_desc', [608080, 608081])
                dlg.set_lottery_rule(title, content)

        if self.use_lucky_discount and self.panel.btn_lucky:

            @global_unique_click(self.panel.btn_lucky)
            def OnClick(*args):
                dlg = GameRuleDescUI()
                title, content = 609826, 609827
                dlg.set_show_rule(title, content)

        @global_unique_click(self.panel.btn_skip)
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            self.on_set_skip_anim_flag(btn)

        self.on_set_skip_anim_flag(self.panel.btn_skip)

        @global_unique_click(self.panel.btn_describe)
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            title, content = self.data.get('rule_desc', [608106, 608107])
            dlg.set_lottery_rule(title, content)

        if self.panel.btn_back:

            @global_unique_click(self.panel.btn_back)
            def OnClick(btn, touch):
                global_data.ui_mgr.close_ui('LotteryMainUI')

        node_list = (
         self.panel.nd_schedule_s, self.panel.nd_schedule_s_plus)
        self.category_floor = get_lottery_category_floor_data(self.lottery_id)
        self.category_node_map = {}
        for index, rare_degree in enumerate(self.custom_conf['category_floor_item_rare_degree']):
            self.category_node_map[rare_degree] = node_list[index]

        self.panel_valid_anim = []
        anim_names = ('show', 'loop')
        for anim_name in anim_names:
            self.panel.HasAnimation(anim_name) and self.panel_valid_anim.append(anim_name)

        button_loop_anims = ('btn_once_loop', 'btn_repeat_loop')
        for btn_loop_anim in button_loop_anims:
            if self.panel.HasAnimation(btn_loop_anim):
                self.panel_valid_anim.append(btn_loop_anim)
                self.panel.RecordAnimationNodeState(btn_loop_anim)

        self.init_temporary_activity_entrance()
        self.init_turntable_widget()
        self.init_lab_title()
        self.init_buy_widget()
        self.init_exchange_reward_widget()
        self.refresh_round_data()
        self.update_lucky_info()

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'net_login_reconnect_event': self.on_reconnect_event
           }
        if 'remind_exchange_item_goods_id_list' in self.custom_conf:
            econf.update({'player_item_update_event': self.update_remind_exchange_item_id,
               'buy_good_success': self.update_remind_exchange_item_id
               })
        if self.category_node_map:
            econf['refresh_lottery_limited_guarantee_round'] = (
             self.refresh_limited_item_guarantee_round,)
        return econf

    def init_temporary_activity_entrance(self):
        if 'remind_jump_ui' in self.data:
            self.activity_button_widget = ArtCollectionActivityEntryWidget(self.panel, self.panel, self.data.get('activity_type'), self.data['remind_jump_ui'][0], self.data['remind_jump_ui'][1], 'btn_reward_center')
        else:
            self.activity_button_widget = None
        return

    def check_item_got(self, nd, item_id, item_idx):
        return global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0) > 0

    def on_click_turntable_item_for_show_model(self, item_id, force=False, refresh_ui_state=True):
        if self.show_model_id == item_id and not force:
            return
        else:
            item_id_for_chosen = str(item_id)
            if refresh_ui_state:
                if self.need_show_choose_tag:
                    last_click_node = self.nd_item_map.get(str(self.show_model_id), None)
                    last_click_node and last_click_node.nd_chosen.setVisible(False)
                    item_id_for_chosen in self.nd_item_map and self.nd_item_map[item_id_for_chosen].nd_chosen.setVisible(True)
                if self.need_clear_chosen_anim:
                    self.turntable_widget.stop_turntable_item_state_anim(ITEM_CHOSEN_STATE)
                    self.turntable_widget.stop_turntable_item_state_anim(ITEM_LOOP_STATE)
                    self.need_clear_chosen_anim = False
            elif self.need_show_choose_tag and self.panel.btn_once.IsEnable():
                if item_id_for_chosen in self.nd_item_map and not self.nd_item_map[item_id_for_chosen].nd_chosen.isVisible() and not self.need_clear_chosen_anim:
                    last_click_node = self.nd_item_map.get(self.show_model_id, None)
                    last_click_node and last_click_node.nd_chosen.setVisible(False)
                    item_id_for_chosen in self.nd_item_map and self.nd_item_map[item_id_for_chosen].nd_chosen.setVisible(True)
            self.show_model_id = item_id
            self.on_change_show_reward(item_id)
            return

    def init_item_event_func_for_show_model(self, nd, item_id, item_count):
        if self.need_show_choose_tag:
            self.nd_item_map[item_id] = nd

        @global_unique_click(nd.nd_click)
        def OnClick(btn, touch):
            self.on_click_turntable_item_for_show_model(item_id)

    def _get_turntable_default_item_node(self):
        return self.panel.temp_item_1

    def get_item_anim_name_map(self):
        anim_name_map = {}
        ani_names = self._get_turntable_default_item_node().GetAnimationNameList()
        for anim_name in ani_names:
            anim_name = str(anim_name)
            key = anim_name[:3]
            state = TURNTABLE_ITEM_ANIM_PREFIX_MAP.get(key)
            if state is None:
                continue
            if state not in anim_name_map:
                anim_name_map[state] = list()
            anim_name_map[state].append(anim_name)

        return anim_name_map

    def play_item_default_anim(self, nd, anim_name, item_id):
        pass

    def play_item_pass_anim(self, nd, anim_name, item_id):
        pass

    def play_item_chosen_anim(self, nd, anim_name, item_id):
        pass

    def play_item_loop_anim(self, nd, anim_name, item_id):
        pass

    def check_func_customized(self, func_name):
        return getattr(self, func_name) != getattr(super(self.__class__, self), func_name, getattr(self, func_name))

    def default_play_item_chosen_anim_for_show_model(self, nd, anim_name, item_id):
        if type(anim_name) == str:
            nd.PlayAnimation(anim_name)
        else:
            for single_anim_name in anim_name:
                nd.PlayAnimation(single_anim_name)

        if self.need_refresh_model_for_lottery_result:
            self.show_model_id = item_id
            self.on_change_show_reward(item_id)
        if self.need_show_model_in_main_panel:
            self.need_clear_chosen_anim = True
        self.play_panel_anim_aftar_item_chosen(item_id)

    def play_panel_anim_aftar_item_chosen(self, item_id):
        for anim_info in self.custom_conf['receive_result_anim']:
            anim_name, item_list = anim_info
            if not item_list or item_id in item_list:
                self.panel.PlayAnimation(anim_name)
                break

    def get_play_item_anim_func_map(self):
        anim_func_map = {}
        for state_name, item_list in six.iteritems(self.custom_conf['exclusive_anim_item_list']):

            def play_item_anim(nd, anim_name, item_id, exclusive_item_list=item_list):
                if item_id not in exclusive_item_list:
                    return
                if type(anim_name) == str:
                    nd.PlayAnimation(anim_name)
                else:
                    for single_anim_name in anim_name:
                        nd.PlayAnimation(single_anim_name)

            anim_func_map[STATE_NAME_MAP[state_name]] = play_item_anim

        anim_func_map[ITEM_CHOSEN_STATE] = self.default_play_item_chosen_anim_for_show_model
        for state, func_name in six.iteritems(CUSTOM_PLAY_TURNTABLE_ITEM_ANIM_FUNC_NAME):
            if self.check_func_customized(func_name):
                anim_func_map[state] = getattr(self, func_name)

        return anim_func_map

    def init_turntable_widget(self):
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
        need_show_got = bool(self.custom_conf['show_got_tag'])
        need_anim_skip_got_item = bool(self.custom_conf['anim_skip_got_item'])
        self.turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, nd_click_name='nd_click', item_anim_name_map=self.get_item_anim_name_map(), play_item_anim_func_map=self.get_play_item_anim_func_map(), need_show_got=need_show_got, get_nd_got_func=(lambda nd, idx: nd.nd_got), check_item_got_func=self.check_item_got, need_anim_skip_got_item=need_anim_skip_got_item, **self.turntable_widget_init_kwargs)
        return

    def init_lab_title(self):
        conf = confmgr.get('lottery_page_config', self.lottery_id, default={})
        self.panel.lab_title.SetString(get_text_by_id(conf.get('text_id')))
        self.panel.lab_tips_time.SetString('')
        single_goods_id = conf.get('single_goods_id')
        open_date_range = get_goods_item_open_date(single_goods_id)
        _, left_time = check_limit_time_lottery_open_info(open_date_range)
        self.remain_time = int(left_time)
        if self.remain_time > 0:
            self.title_timer = global_data.game_mgr.get_logic_timer().register(func=self._update_title_timer, interval=1, mode=CLOCK)

    def _release_title_timer(self):
        if self.title_timer:
            global_data.game_mgr.unregister_logic_timer(self.title_timer)
            self.title_timer = None
        return

    def _update_title_timer(self):
        self.remain_time = self.remain_time - 1
        if self.remain_time < 0:
            self._release_title_timer()
            return
        time_str = tutil.get_simply_readable_time(self.remain_time)
        if self.is_visible_close:
            self.panel.lab_tips_time.SetString('{}{}'.format(get_text_by_id(82134), time_str))
        else:
            self.panel.lab_tips_time.SetString(get_text_by_id(19446).format(time_str))

    @staticmethod
    def check_need_anim(item_no):
        return True

    def pre_init_display_item(self, item_widget, item_no=None):
        if self.check_need_anim(item_no):
            ani_names = item_widget.GetAnimationNameList()
            for anim_name in ani_names:
                anim_name = str(anim_name)
                if anim_name.startswith('loop'):
                    item_widget.PlayAnimation(anim_name)
                else:
                    item_widget.RecordAnimationNodeState(anim_name)

    def play_display_item_anim(self, item_widget, flag, item_no=None):
        item_widget.img_choose.setVisible(flag)
        if self.check_need_anim(item_no):
            if flag:
                ani_names = item_widget.GetAnimationNameList()
                for anim_name in ani_names:
                    anim_name = str(anim_name)
                    if anim_name.startswith('click'):
                        item_widget.PlayAnimation(anim_name)

            else:
                ani_names = item_widget.GetAnimationNameList()
                for anim_name in ani_names:
                    anim_name = str(anim_name)
                    if anim_name.startswith('click'):
                        item_widget.StopAnimation(anim_name)
                        item_widget.RecoverAnimationNodeState(anim_name)

    def set_exchange_reward_widget_visible_callback(self, flag):
        if flag:
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)
            self._end_auto_switch_show_model_timer()
        else:
            global_data.emgr.refresh_switch_core_model_button_visible.emit()
            self._begin_auto_switch_show_model_timer()

    def init_exchange_reward_widget(self):
        if not self.data.get('show_shop'):
            return
        self.panel.btn_shop.red_point.setVisible(False)

        @global_unique_click(self.panel.btn_shop)
        def OnClick(btn, touch):
            self.on_click_btn_shop()

        nd_visibility_opposite_relatively = [
         'lab_num_times']
        if self.custom_conf['need_hide_lottery_list']:
            nd_visibility_opposite_relatively.append('list_bar')
        nd_directly_show_visible = []
        nd_directly_show_invisible = []
        if self.panel.node_2.temp_exchange.nd_name:
            nd_kind = [
             'nd_name.temp_kind']
            nd_lab_name = ['nd_name.lab_name']
            nd_btn_detail = ['nd_name.lab_name.nd_auto_fit.btn_detail']
            if self.panel.node_2.temp_exchange.nd_name_1:
                nd_directly_show_visible.append('nd_name_1')
                nd_directly_show_invisible.append('nd_name')
                if self.panel.node_2.temp_exchange.img_title_1:
                    nd_directly_show_visible.append('img_title_1')
                    nd_directly_show_invisible.append('img_title')
                nd_kind.append('nd_name_1.temp_kind')
                nd_lab_name.append('nd_name_1.lab_name')
                nd_btn_detail.append('nd_name_1.lab_name.nd_auto_fit.btn_detail')
        else:
            nd_kind, nd_lab_name, nd_btn_detail = [], [], []
        self.exchange_reward_widget = LotteryExchangeRewardWidget(self, self.panel.node_2.temp_exchange, self.panel.node_2, self.panel.node_1, self.lottery_id, self.on_change_show_reward, nd_visibility_opposite_relatively=nd_visibility_opposite_relatively, pre_init_display_item=self.pre_init_display_item, play_display_item_anim=self.play_display_item_anim, nd_directly_show_visible=nd_directly_show_visible, nd_directly_show_invisible=nd_directly_show_invisible, nd_kind=nd_kind, nd_lab_name=nd_lab_name, nd_btn_detail=nd_btn_detail)

    def _play_buy_button_loop_anim(self):
        self.panel.HasAnimation('btn_once_loop') and self.panel.PlayAnimation('btn_once_loop')
        self.panel.HasAnimation('btn_repeat_loop') and self.panel.PlayAnimation('btn_repeat_loop')

    def _stop_buy_button_loop_anim(self):
        if self.panel.HasAnimation('btn_once_loop'):
            self.panel.StopAnimation('btn_once_loop')
            self.panel.RecoverAnimationNodeState('btn_once_loop')
        if self.panel.HasAnimation('btn_repeat_loop'):
            self.panel.StopAnimation('btn_repeat_loop')
            self.panel.RecoverAnimationNodeState('btn_repeat_loop')

    def check_buy_action_disabled(self, lottery_count):
        if self.need_refresh_round_data:
            if self.all_round_finished:
                global_data.game_mgr.show_tip(get_text_by_id(82220))
                return True
            return False
        return super(LotteryCommonTurntableWidget, self).check_buy_action_disabled(lottery_count)

    def get_special_price_info(self, price_info, lottery_count):
        return False

    def special_buy_logic_func(self, price_info, lottery_count):
        return False

    def buying_callback(self, lottery_count):
        self.cur_draw_lottery_count = lottery_count
        self._stop_buy_button_loop_anim()
        if self.need_show_choose_tag and str(self.show_model_id) in self.nd_item_map:
            self.nd_item_map[str(self.show_model_id)].nd_chosen.setVisible(False)
        self.turntable_widget.stop_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self.turntable_widget.play_turntable_animation(lottery_count)
        self._end_auto_switch_show_model_timer()

    def lottery_data_ready_callback(self, bought_successfully):
        if not bought_successfully:
            self.turntable_widget.lottery_failed()
            self._play_buy_button_loop_anim()

    def update_price_info_callback(self, nd, lottery_count):
        nd_lab = lottery_count == SINGLE_LOTTERY_COUNT and self.panel.btn_once.lab_once if 1 else self.panel.btn_repeat.lab_repeat
        price_width = 0
        for price_item in nd.temp_price.GetAllItem():
            if price_item.isVisible():
                price_width += price_item.GetContentSize()[0]

        lab_width = nd_lab.getTextContentSize().width
        total_width = price_width + lab_width
        half_width = total_width / 2
        price_x_offset = price_width / 2 - half_width - 5
        lab_x_offset = half_width - lab_width + 5
        nd.SetPosition('50%{}'.format(int(price_x_offset)), nd.getPositionY())
        nd_lab.SetPosition('50%{}'.format(int(lab_x_offset)), nd_lab.getPositionY())

    def init_buy_widget(self):
        buy_button_info = {SINGLE_LOTTERY_COUNT: self.panel.btn_once}
        buy_price_info = {SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price}
        if self.custom_conf['buy_button_count'] > 1:
            buy_button_info[CONTINUAL_LOTTERY_COUNT] = self.panel.btn_repeat
            buy_price_info[CONTINUAL_LOTTERY_COUNT] = self.panel.btn_repeat.temp_price
        update_price_info_callbacks = {}
        if check_buy_button_lab_and_price_same_y(self.panel.btn_once, SINGLE_LOTTERY_COUNT):
            update_price_info_callbacks[SINGLE_LOTTERY_COUNT] = self.update_price_info_callback
        if self.custom_conf['buy_button_count'] > 1 and check_buy_button_lab_and_price_same_y(self.panel.btn_repeat, CONTINUAL_LOTTERY_COUNT):
            update_price_info_callbacks[CONTINUAL_LOTTERY_COUNT] = self.update_price_info_callback
        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info=buy_button_info, buy_price_info=buy_price_info, price_color=self.price_color, update_price_info_callbacks=update_price_info_callbacks, get_special_price_info=self.get_special_price_info, special_buy_logic_func=self.special_buy_logic_func, buying_callback=self.buying_callback, lottery_data_ready_callback=self.lottery_data_ready_callback, **self.buy_widget_init_kwargs)

    def on_click_btn_shop(self, *args):
        self.exchange_reward_widget.visible = True
        self.remind_exchange_archive_data[self.lottery_id] = self.cur_remind_exchange_item_id
        self.update_remind_exchange_item_id()

    def on_finalize_panel(self):
        super(LotteryCommonTurntableWidget, self).on_finalize_panel()
        self._release_title_timer()
        self.destroy_widget('activity_button_widget')
        self.destroy_widget('turntable_widget')
        self.destroy_widget('exchange_reward_widget')
        self.destroy_widget('buy_widget')
        self.nd_item_map = {}
        self._end_auto_switch_show_model_timer()
        self.remind_exchange_archive_data.save()
        self.remind_exchange_archive_data = None
        self.skip_anim_archive_data[self.lottery_id] = self.need_skip_anim
        self.skip_anim_archive_data.save()
        self.skip_anim_archive_data = None
        self.category_node_map = {}
        return

    def play_panel_show_anim(self, flag):
        func = self.panel.PlayAnimation if flag else self.panel.StopAnimation
        for anim_name in self.panel_valid_anim:
            func(anim_name)

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
                self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
            if self.is_visible_close:
                self.exchange_reward_widget.visible = True
        else:
            self.play_panel_show_anim(True)
            self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self._begin_auto_switch_show_model_timer()

    def hide(self):
        self.panel.setVisible(False)
        if self.custom_conf['hide_limit_count']:
            global_data.emgr.hide_lottery_main_ui_elements.emit(False, 'lab_num_times')
        if self.panel.btn_back:
            global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', True)
        self.play_panel_show_anim(False)
        self._end_auto_switch_show_model_timer()

    def do_hide_panel(self):
        self._end_auto_switch_show_model_timer()

    def refresh_round_data(self):
        if not self.need_refresh_round_data:
            return
        drawn_count = 0
        for item_id, item_count in self.turntable_item_list:
            drawn_count += global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0)

        self.cur_single_goods_id = self.single_goods_id_list[drawn_count]
        self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
        self.all_round_finished = self.max_draw_count == drawn_count
        self.buy_widget.set_force_text(611341 if self.all_round_finished else '', price_info=([], False))
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

    def refresh(self):
        self.buy_widget.refresh()
        self.refresh_round_data()
        self.refresh_lottery_limit_count()
        self.refresh_limited_item_guarantee_round()
        self.update_exchange_coin_num()
        self.update_remind_exchange_item_id()

    def refresh_show_model(self, show_model_id=None):
        if self.data.get('show_shop'):
            if self.exchange_reward_widget and self.exchange_reward_widget.visible:
                self.exchange_reward_widget.refresh_show_model(show_model_id)
                return
        if self.need_show_model_in_main_panel:
            if self.custom_conf['show_choose_item_model']:
                if show_model_id:
                    self.on_click_turntable_item_for_show_model(show_model_id, force=True)
                else:
                    self.on_click_turntable_item_for_show_model(self.show_model_id, force=True, refresh_ui_state=False)
            elif self.auto_show_model_id_list:
                if show_model_id in self.auto_show_model_id_list:
                    self.show_model_index = self.auto_show_model_id_list.index(show_model_id)
                    self.show_model_id = show_model_id
                    self.on_change_show_reward(show_model_id)
                else:
                    self.on_change_show_reward(self.show_model_id)
            else:
                self.on_change_show_reward(self.show_model_id)

    def switch_show_model(self, offset, is_auto=False):
        if not self.custom_conf['show_choose_item_model']:
            self.show_model_index = (self.show_model_index + offset + self.auto_show_model_count) % self.auto_show_model_count
            self.show_model_id = self.auto_show_model_id_list[self.show_model_index]
            self.on_change_show_reward(self.show_model_id)
            if not is_auto:
                self._begin_auto_switch_show_model_timer()

    def _end_auto_switch_show_model_timer(self):
        if self.auto_switch_model_timer:
            global_data.game_mgr.unregister_logic_timer(self.auto_switch_model_timer)
            self.auto_switch_model_timer = None
        return

    def _begin_auto_switch_show_model_timer(self):
        if self.auto_show_model_id_list:
            if self.data.get('show_shop') and self.exchange_reward_widget and self.exchange_reward_widget.visible:
                return
            self._end_auto_switch_show_model_timer()
            self.auto_switch_model_timer = global_data.game_mgr.register_logic_timer(self.switch_show_model, interval=self.auto_switch_model_interval, args=(1, True), times=-1, mode=CLOCK)

    def on_begin_drag_model(self):
        self._end_auto_switch_show_model_timer()

    def on_end_drag_model(self):
        self._begin_auto_switch_show_model_timer()

    def set_visible_close(self, is_visible_close):
        if not self.exchange_reward_widget:
            return
        self.is_visible_close = is_visible_close
        self.exchange_reward_widget.set_directly_show(is_visible_close, ('list_bar', ))

    def on_receive_lottery_result(self, item_list, origin_list):
        self.turntable_widget.set_turntable_items_got(item_list, origin_list, force_play_chosen_anim_when_skip=self.cur_draw_lottery_count == SINGLE_LOTTERY_COUNT)

    def on_lottery_ended(self):
        if not self.panel.isVisible():
            return
        self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self._begin_auto_switch_show_model_timer()
        self._play_buy_button_loop_anim()
        self.refresh_round_data()
        self.refresh_limited_item_guarantee_round()
        self.update_exchange_coin_num()
        self.update_remind_exchange_item_id()
        self.update_lucky_info()

    def on_reconnect_event(self):
        if global_data.ui_mgr.get_ui('ScreenLockerUI'):
            global_data.emgr.lottery_data_ready.emit(False)
            global_data.ui_mgr.close_ui('LotteryMainUI')

    def refresh_limited_item_guarantee_round(self):
        for rare_degree, nd in six.iteritems(self.category_node_map):
            max_count, line_no = self.category_floor[str(rare_degree)]
            has_bought_count = global_data.player.get_reward_category_floor(self.data['table_id'], line_no)
            nd.lab_tag_num.SetString('{}/{}'.format(has_bought_count, max_count))
            nd.nd_prog.prog_tag.SetPercentage(100.0 * has_bought_count / max_count)

    def update_exchange_coin_num(self):
        if 'coin_item_id' not in self.custom_conf:
            return
        self.panel.btn_shop.lab_num.SetString(str(global_data.player.get_item_num_by_no(self.custom_conf['coin_item_id'])))

    def update_remind_exchange_item_id(self):
        if 'remind_exchange_item_goods_id_list' not in self.custom_conf:
            return
        else:
            if global_data.ui_mgr.get_ui('ScreenLockerUI'):
                return
            cur_remind_exchange_item_id = None
            exchange_item_goods_id_list = self.custom_conf['remind_exchange_item_goods_id_list']
            for index, goods_id in enumerate(exchange_item_goods_id_list):
                item_id, payment_item_id, count = self.remind_exchange_item_price_list[index]
                if global_data.player.get_item_num_by_no(item_id) > 0:
                    continue
                cur_money_count = global_data.player.get_item_money(payment_item_id)
                if cur_money_count >= count:
                    cur_remind_exchange_item_id = item_id
                    break
                need_buy_payment_count = count - cur_money_count
                if payment_item_id in self.payment_goods_id_map:
                    second_payment_item_id, second_payment_count = self.payment_goods_id_map[payment_item_id]
                    if global_data.player.get_item_money(second_payment_item_id) / second_payment_count >= need_buy_payment_count:
                        cur_remind_exchange_item_id = item_id
                        break

            self.cur_remind_exchange_item_id = cur_remind_exchange_item_id
            if self.cur_remind_exchange_item_id is None:
                self.remind_exchange_archive_data[self.lottery_id] = None
                self.panel.nd_lab_tips.setVisible(False)
                return
            if self.cur_remind_exchange_item_id != self.remind_exchange_archive_data.get(self.lottery_id, None):
                self.panel.nd_lab_tips.setVisible(True)
                self.panel.lab_tips.SetString(get_text_by_id(609794).format(get_lobby_item_name(self.cur_remind_exchange_item_id)))
                self.panel.PlayAnimation('prompt_show')
                self.panel.PlayAnimation('prompt_loop')
            else:
                self.panel.nd_lab_tips.setVisible(False)
            return

    def update_lucky_info(self):
        if not self.use_lucky_discount:
            return
        max_lucky, cur_lucky, discount = global_data.player.get_goods_lucky_discount_data(self.data['continual_goods_id'])
        self.panel.lab_progress.SetString(get_text_by_id(609791).format(cur_lucky, max_lucky))
        self.panel.prog.SetPercent(100.0 * cur_lucky / max_lucky)
        self.buy_widget.refresh()
        self.panel.img_discount.setVisible(discount < 1.0)
        if discount < 1.0:
            self.panel.lab_discount.SetString('-{}%'.format(int(ceil((1.0 - discount) * 100.0))))