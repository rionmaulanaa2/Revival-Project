# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityPinganjingEmote.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import activity_utils, task_utils, mall_utils
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_reward, init_price_view, set_node_position_in_screen
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from common.utils.timer import CLOCK
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon import time_utility
from logic.comsys.lobby import LobbyMatchWidget
from logic.comsys.lobby.MatchMode import MatchMode
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_PINGANJING_PAPER, SHOP_PAYMENT_ITEM_PINGANJING_PAPER
import six
import six_ex
import cc
OPEN_BOX_ITEM_ID = 70200013
EMOTE_GOODS_ID = '701500001'
OPEN_BOX_GOODS_ID = '701500002'
SPECIAL_EMOTE_ITEM_ID = 30620089
SPECIAL_EMOTE_TASK_ID = '1451189'

class ActivityPinganjingEmote(ActivityBase):

    def on_init_panel(self):
        self.init_parameters()
        self.init_ui_event()
        self.init_widget()
        self.init_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_received_task_reward,
           'task_prog_changed': self._update_task_list,
           'player_item_update_event': self.on_player_item_update,
           'receive_lottery_result': self.on_receive_lottery_result,
           'on_pickable_item_limit_change': self._update_pickable_item
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            log_error('[ERROR] activity [%s] task [%s] has no chidren task' % (activity_type, conf['cTask']))
            return
        else:
            self.parent_task = task_list[0]
            self.children_task_list = task_utils.get_children_task(self.parent_task)
            self.emote_item_list = confmgr.get('preview_12302473')['turntable_goods_info']
            self.emote_id_list = []
            self.emote_own_count = 0
            self.common_emote_count = len(self.emote_item_list)
            self._count_down_timer = None
            self.turntable_item_chosen_sound_name_list = []
            self.turntable_item_map = dict()
            self.turntable_item_node_list = []
            self.max_delighted_time = 2
            self.max_single_interval = 0.6
            self.high_speed_count_percent = 0.8
            self.delta_delight_interval = 0.0
            self.final_delta_delight_interval = 0.06
            self.med_single_interval = 0.15
            self.min_single_interval = 0.05
            self.delight_anim_timer = None
            self._price_top_widget = None
            return

    def init_ui_event(self):

        def show_item_desc(item_id, btn):
            x, y = btn.GetPosition()
            w, _ = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos)
            return

        @self.panel.btn_box.unique_callback()
        def OnClick(btn, touch):
            show_item_desc(OPEN_BOX_ITEM_ID, btn)

        @self.panel.img_emote.btn_choose.unique_callback()
        def OnClick(btn, touch):
            show_item_desc(SPECIAL_EMOTE_ITEM_ID, btn)

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            _, sel_battle_type, sel_match_mode, sel_play_type = LobbyMatchWidget.get_battle_infos()
            MatchMode(None, sel_play_type, sel_battle_type, sel_match_mode)
            global_data.ui_mgr.close_ui('ActivityPinganjingMainUI')
            return

    def init_widget(self):
        self._init_money_widget()
        self._init_task_list()
        self._init_emote_list()
        self._update_pickable_item()
        self._update_price_list()
        self._update_emote_own_state()
        self._update_limit_label()
        self._start_count_down_timer()

    def _init_money_widget--- This code section failed: ---

 114       0  LOAD_GLOBAL           0  'PriceUIWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'list_money'
          15  LOAD_CONST            2  'pnl_title'
          18  LOAD_GLOBAL           3  'False'
          21  CALL_FUNCTION_513   513 
          24  LOAD_FAST             0  'self'
          27  STORE_ATTR            4  '_price_top_widget'

 115      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             4  '_price_top_widget'
          36  LOAD_ATTR             5  'show_money_types'
          39  LOAD_GLOBAL           6  'SHOP_PAYMENT_ITEM_PINGANJING_PAPER'
          42  BUILD_LIST_1          1 
          45  CALL_FUNCTION_1       1 
          48  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 21

    def _init_task_list(self):
        list_task = self.panel.list_task
        list_task.DeleteAllSubItem()
        for index, task_id in enumerate(self.children_task_list):
            reward_id = task_utils.get_task_reward(task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if reward_list:
                item = list_task.AddTemplateItem()
                item.lab_name.SetString(task_utils.get_task_name(task_id))

                @item.temp_btn_get.btn_common.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    global_data.player.receive_tasks_reward([task_id])

                @item.temp_btn_go.btn_common.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    jump_conf = task_utils.get_jump_conf(task_id)
                    func_name = None
                    if jump_conf:
                        func_name = jump_conf.get('func')
                    if func_name == 'jump_to_mode_choose_new':
                        global_data.ui_mgr.close_ui('ActivityPinganjingMainUI')
                    task_utils.try_do_jump(task_id)
                    return

                list_reward = item.list_reward
                list_reward.DeleteAllSubItem()
                for item_no, num in reward_list:
                    reward_item = list_reward.AddTemplateItem()
                    init_tempate_reward(reward_item, item_no, num, show_tips=True)

        self._update_task_list()

    def _update_task_list(self, *args):
        list_task = self.panel.list_task
        for index, task_id in enumerate(self.children_task_list):
            reward_id = task_utils.get_task_reward(task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if reward_list:
                item = list_task.GetItem(index)
                task_prog = global_data.player.get_task_prog(task_id)
                total_prog = task_utils.get_total_prog(task_id)
                item.lab_num.SetString('%d/%d' % (task_prog, total_prog))
                btn_get = item.temp_btn_get
                btn_go = item.temp_btn_go
                nd_get = item.nd_get
                if global_data.player.is_task_finished(task_id):
                    btn_go.setVisible(False)
                    if not global_data.player.has_receive_reward(task_id):
                        btn_get.setVisible(True)
                        nd_get.setVisible(False)
                    else:
                        btn_get.setVisible(False)
                        nd_get.setVisible(True)
                else:
                    btn_get.setVisible(False)
                    btn_go.setVisible(True)
                    nd_get.setVisible(False)

        global_data.emgr.refresh_activity_redpoint.emit()

    def _init_emote_list(self):
        emote_conf = confmgr.get('chat_all_emotes').get_conf()
        emote_text_map = dict()
        for values in six.itervalues(emote_conf):
            if values.get('iItemId', None):
                emote_text_map[str(values['iItemId'])] = values['iTxtId']

        nd_list = self.panel.list_item
        nd_list.DeleteAllSubItem()
        for index, (item_id, item_count) in enumerate(self.emote_item_list):
            self.emote_id_list.append(int(item_id))
            item = nd_list.AddTemplateItem()
            item.lab_name.SetString(emote_text_map[item_id])
            emoji_path = get_lobby_item_pic_by_item_no(item_id)
            item.img_item.SetDisplayFrameByPath('', emoji_path)
            btn_choose = item.btn_choose
            btn_choose.EnableCustomState(True)
            self.turntable_item_map[int(item_id), item_count] = index
            self.turntable_item_node_list.append(item)

            @btn_choose.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                x, y = btn.GetPosition()
                w, _ = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos)
                return

        emoji_path = get_lobby_item_pic_by_item_no(SPECIAL_EMOTE_ITEM_ID)
        self.panel.img_emote.SetDisplayFrameByPath('', emoji_path)
        return

    def _update_pickable_item(self):
        pickable_item_num = global_data.player.get_pickable_item_num_by_lobby_item_id(SHOP_PAYMENT_PINGANJING_PAPER)
        battle_bag_item = confmgr.get('lobby_item', str(SHOP_PAYMENT_PINGANJING_PAPER), 'battle_bag_item')
        daily_max_amount = confmgr.get('item', str(battle_bag_item), 'max_amount_daily')
        pickable_item_str = '{}/{}'.format(pickable_item_num, daily_max_amount)
        self.panel.lab_got.SetString(get_text_by_id(634845).format(pickable_item_str))

    def _update_price_list(self):
        init_price_view(self.panel.btn_click.temp_price, EMOTE_GOODS_ID, DARK_PRICE_COLOR)
        init_price_view(self.panel.btn_open.temp_price, OPEN_BOX_GOODS_ID, DARK_PRICE_COLOR)

    def _update_emote_own_state(self):
        self.cur_delight_item_index = 0
        self.target_delighted_time = 0
        self.delight_interval = 0.17
        self.target_delight_item_index_list = []
        self.turntable_item_anim_sequence = []
        self.turntable_item_list = []
        own_count = 0
        for index, (item_id, item_count) in enumerate(self.emote_item_list):
            item = self.panel.list_item.GetItem(index)
            own = global_data.player.get_item_num_by_no(int(item_id)) > 0
            item.nd_got.setVisible(own)
            item.bar.SetShowEnable(not own)
            if own:
                own_count += 1
            else:
                self.turntable_item_anim_sequence.append(index)
                self.turntable_item_list.append(item)

        if global_data.player.get_item_num_by_no(SPECIAL_EMOTE_ITEM_ID) > 0:
            self.panel.img_emote.icon_got.setVisible(True)
            own_count += 1
        else:
            self.panel.img_emote.icon_got.setVisible(False)
            if own_count == self.common_emote_count:
                global_data.player.receive_task_reward(SPECIAL_EMOTE_TASK_ID)
        self.emote_own_count = own_count
        self.turntable_item_count = self.common_emote_count - self.emote_own_count
        self.turntable_item_anim_sequence_length = len(self.turntable_item_anim_sequence)
        if self.turntable_item_count > 0:
            self.panel.lab_tips.setString(get_text_by_id(634846))
            self.panel.btn_click.setVisible(True)
            self.panel.btn_open.SetEnable(False)
        else:
            self.panel.lab_tips.setString(get_text_by_id(634849))
            self.panel.btn_click.setVisible(False)
            self.panel.btn_open.SetEnable(True)

    def _update_limit_label(self):
        self.panel.lab_prog.setVisible(False)

    def _start_count_down_timer(self):
        self._stop_count_down_timer()
        self._count_down_timer = global_data.game_mgr.register_logic_timer(self._update_count_down, interval=1, times=-1, mode=CLOCK)
        self.panel.lab_refresh.SetString('')

    def _stop_count_down_timer(self):
        if self._count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self._count_down_timer)
            self._count_down_timer = None
        return

    def _update_count_down(self):
        now = time_utility.time()
        if now <= time_utility.get_utc8_day_start_timestamp() + 5 * time_utility.ONE_HOUR_SECONS:
            left_time = time_utility.get_utc8_day_start_timestamp() + 5 * time_utility.ONE_HOUR_SECONS - time_utility.time()
        else:
            left_time = time_utility.get_utc8_day_start_timestamp() + time_utility.ONE_DAY_SECONDS + 5 * time_utility.ONE_HOUR_SECONS - time_utility.time()
        if left_time > 0.0:
            time_str = time_utility.get_readable_time(left_time)
            self.panel.lab_refresh.SetString(get_text_by_id(83145) + time_str)

    def show_lottery_result(self):
        global_data.emgr.refresh_common_reward_ui_performance_temporarily.emit(0.05, True)
        global_data.emgr.receive_award_succ_event_from_lottery.emit(*self.turntable_ret)
        global_data.emgr.on_lottery_ended_event.emit()
        global_data.emgr.player_money_info_update_event.emit()
        if self.panel and self.panel.isValid():
            self.on_player_item_update()
            self._update_emote_own_state()

    def _delight_single_turntable_item(self):
        if not self.panel or not self.panel.isValid():
            return
        cur_index = self.turntable_item_anim_sequence[self.cur_delight_item_index]
        cur_item = self.turntable_item_node_list[cur_index]
        pass_anim_duration = max(0, cur_item.GetAnimationMaxRunTime('pass'))
        if pass_anim_duration < self.delight_interval:
            scale = pass_anim_duration / self.delight_interval + 0.05 if 1 else 1.0
            cur_item.PlayAnimation('pass', scale=scale)
            if self.target_delight_item_index_list:
                if cur_index == self.target_delight_item_index_list[0] and (self.target_delighted_time >= self.max_delighted_time or self.delight_interval >= self.max_single_interval - self.delta_delight_interval):
                    action_list = list()
                    cur_item.btn_choose.SetSelect(True)
                    action_list.append(cc.DelayTime.create(0.4))
                    action_list.append(cc.CallFunc.create(self.show_lottery_result))
                    cur_item.runAction(cc.Sequence.create(action_list))
                    return
                self.target_delighted_time += 1
            self.delight_interval += self.delta_delight_interval
            if self.delight_interval >= self.med_single_interval:
                self.delta_delight_interval = self.final_delta_delight_interval
            if self.delight_interval > self.max_single_interval + self.delta_delight_interval:
                self.delight_interval = self.max_single_interval + self.delta_delight_interval
        self.cur_delight_item_index = (self.cur_delight_item_index + 1) % self.turntable_item_anim_sequence_length
        self.delight_anim_timer = global_data.game_mgr.register_logic_timer(self._delight_single_turntable_item, interval=self.delight_interval, times=1, mode=CLOCK)

    def _release_delight_anim_timer(self):
        if self.delight_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.delight_anim_timer)
            self.delight_anim_timer = None
        return

    def set_turntable_items_got(self, item_list, origin_list):
        self.turntable_ret = (item_list, origin_list)
        for i, item_info in enumerate(item_list):
            turntable_item_key = tuple(origin_list[i]) if origin_list[i] else tuple(item_info)
            if turntable_item_key in self.turntable_item_map:
                self.target_delight_item_index_list.append(self.turntable_item_map[turntable_item_key])

        if self.turntable_item_count == 1:
            cur_item_index = self.target_delight_item_index_list[0]
            cur_item = self.turntable_item_node_list[cur_item_index]
            action_list = list()
            action_list.append(cc.CallFunc.create(self.show_lottery_result))
            cur_item.runAction(cc.Sequence.create(action_list))
        else:
            target_item_index = self.target_delight_item_index_list[0]
            if target_item_index == self.cur_delight_item_index:
                left_delight_count = self.max_delighted_time * self.turntable_item_count
            else:
                left_delight_count = self.max_delighted_time * self.turntable_item_count + (target_item_index + self.turntable_item_count - self.cur_delight_item_index) % self.turntable_item_count
            med_left_delight_count = int(left_delight_count * self.high_speed_count_percent)
            self.delta_delight_interval = (self.med_single_interval - self.min_single_interval) / med_left_delight_count
            self._delight_single_turntable_item()

    def init_event(self):
        btn_describe_title = self.panel.btn_describe_title
        if btn_describe_title:

            @btn_describe_title.unique_callback()
            def OnClick(btn, touch):
                self._on_click_describe()

        btn_describe = self.panel.btn_describe
        if btn_describe:

            @btn_describe.unique_callback()
            def OnClick(btn, touch):
                self._on_click_describe()

        @self.panel.btn_click.unique_callback()
        def OnClick(btn, touch):
            self._on_click_emote()

        @self.panel.btn_open.unique_callback()
        def OnClick(btn, touch):
            self._on_click_open_box()

    def _on_click_describe(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        name_id = conf['cNameTextID']
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(name_id), get_text_by_id(conf.get('cDescTextID', '')))

    def _on_click_emote(self):
        if self.turntable_item_count > 0:
            for index, _ in enumerate(self.emote_item_list):
                item = self.panel.list_item.GetItem(index)
                item.btn_choose.SetSelect(False)

            self._release_delight_anim_timer()
            prices = mall_utils.get_mall_item_price(EMOTE_GOODS_ID, pick_list='item')
            if not prices:
                return
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            if mall_utils.check_payment(goods_payment, price_info.get('real_price')):
                global_data.player and global_data.player.buy_goods(EMOTE_GOODS_ID, 1, goods_payment)

    def _on_click_open_box(self):
        if self.common_emote_count > self.emote_own_count:
            pass
        else:
            prices = mall_utils.get_mall_item_price(OPEN_BOX_GOODS_ID, pick_list='item')
            if not prices:
                return
        price_info = prices[0]
        goods_payment = price_info.get('goods_payment')
        if mall_utils.check_payment(goods_payment, price_info.get('real_price')):
            global_data.player and global_data.player.buy_goods(OPEN_BOX_GOODS_ID, 1, goods_payment)

    def on_received_task_reward(self, task_id):
        if self.parent_task == task_id or task_id in self.children_task_list:
            self._update_task_list()
            global_data.player.read_activity_list(self._activity_type)

    def on_player_item_update(self, *args):
        self._update_price_list()
        self._update_limit_label()
        if global_data.player.get_item_num_by_no(SPECIAL_EMOTE_ITEM_ID) > 0:
            self.panel.img_emote.icon_got.setVisible(True)
        else:
            self.panel.img_emote.icon_got.setVisible(False)
        global_data.emgr.player_money_info_update_event.emit()
        global_data.emgr.refresh_activity_redpoint.emit()

    def on_receive_lottery_result(self, item_list, origin_list, extra_data, extra_info):
        item_id = item_list[0][0]
        if item_id in self.emote_id_list:
            self.set_turntable_items_got(item_list, origin_list)
        else:
            global_data.emgr.receive_award_succ_event_from_lottery.emit(*(item_list, origin_list))
        global_data.emgr.refresh_activity_redpoint.emit()

    def on_finalize_panel(self):
        super(ActivityPinganjingEmote, self).on_finalize_panel()
        self.parent_task = None
        self.children_task_list = None
        self.emote_item_list = None
        self.emote_id_list = None
        self.emote_own_count = None
        self.common_emote_count = None
        self.process_event(False)
        self._stop_count_down_timer()
        self._release_delight_anim_timer()
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        self.cur_delight_item_index = None
        self.target_delighted_time = None
        self.delight_interval = None
        self.target_delight_item_index_list = None
        self.turntable_item_anim_sequence = None
        self.turntable_item_list = None
        self.turntable_item_chosen_sound_name_list = None
        self.turntable_item_map = None
        self.turntable_item_node_list = None
        self.max_delighted_time = None
        self.max_single_interval = None
        self.high_speed_count_percent = None
        self.delta_delight_interval = None
        self.final_delta_delight_interval = None
        self.med_single_interval = None
        self.min_single_interval = None
        return