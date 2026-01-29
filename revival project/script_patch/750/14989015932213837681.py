# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySSCharge.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.common_const import activity_const
from logic.gutils import mall_utils
import common.cfg.confmgr as confmgr
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
from logic.gutils import activity_utils
from logic.gutils import item_utils
import random

class ActivitySSCharge(ActivityBase):
    INTERVAL_TIMES = 15
    SIMULATE_TIMES = 15

    def __init__(self, dlg, activity_type):
        super(ActivitySSCharge, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.register_timer()

    def init_parameters(self):
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self._times = 0
        self._timer = 0
        self._timer_cb = {}
        self._activity_define = confmgr.get('c_activity_config', str(self._activity_type), 'cDefine')
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self._parent_achieve_id = conf.get('global_achieve_id')[0]
        self._goods_list = conf.get('goods_list')
        self._names = conf.get('gift_names')
        self._tags = conf.get('gift_tags')
        self._goods_func_list = conf.get('goods_func_list')
        self._is_first_open = True
        self._tick_goal_num_map = {}
        self._tick_now_num_map = {}
        self._second_tick_increase_num_map = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.refresh_goods_reward,
           'message_update_global_stat': self.update_global_stat,
           'message_update_global_reward_receive': self.update_achieve_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def on_finalize_panel(self):
        self.panel = None
        self.process_event(False)
        self.unregister_timer()
        return

    def on_init_panel(self):
        show_anim = 'show'

        def cb():
            self.panel and self.panel.PlayAnimation('loop')

        time = self.panel.GetAnimationMaxRunTime(show_anim)
        self.panel.PlayAnimation(show_anim)
        self.panel.SetTimeOut(time, cb)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            lv = player.get_lv()
            if lv >= 10:
                player.try_get_global_achieve(self._parent_achieve_id, need_check=False)
            else:
                global_data.game_mgr.show_tip(get_text_by_id(82172))

        self.refresh_goods_reward(True)
        self.show_gifts()
        self.update_progress()

    def refresh_btns(self):
        count = self.panel.list_gift.GetItemCount()
        for i in range(count):
            item_widget = self.panel.list_gift.GetItem(i)
            btn = item_widget.btn_buy_common.btn
            if not btn.IsEnable():
                continue

    def refresh_goods_reward(self, is_init=False):
        goods_func_list = self._goods_func_list
        for i, func_str in enumerate(goods_func_list):
            item_widget = self.panel.list_gift.GetItem(i)
            item_widget.lab_title.SetString(self._names[i])
            item_widget.lab_tag1.SetString(self._tags[i])
            item_widget.lab_tag2.SetString('%')
            if is_init:
                item_widget.PlayAnimation('show_common')
            goods_id = self._goods_list[i]
            reward_id = mall_utils.get_goods_item_reward_id(goods_id)
            if reward_id:
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    return
                reward_list = reward_conf.get('reward_list', [])
                reward_count = len(reward_list)
                item_widget.list_item.SetInitCount(reward_count)
                all_items = item_widget.list_item.GetAllItem()
                for idx, item in enumerate(all_items):
                    item_no, item_num = reward_list[idx]
                    template_utils.init_tempate_mall_i_item(item.nd_item, item_no, show_tips=True)
                    item.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
                    item.lab_num.SetString('*%d' % item_num)

            has_bought = mall_utils.limite_pay(goods_id)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            left_num, _ = num_info
            item_widget.lab_limit_common.SetString(get_text_by_id(82129).format(left_num))
            item_widget.nd_tag.setVisible(not has_bought)
            if getattr(item_widget.btn_buy_common, 'img_light'):
                item_widget.btn_buy_common.img_light.setVisible(False)
            if has_bought:
                item_widget.btn_buy_common.btn.SetEnable(False)
                if not item_widget.lab_btn_text:
                    item_widget.lab_price_common.SetString(12014)
                else:
                    item_widget.lab_btn_text.setVisible(True)
                    item_widget.lab_price_common.setVisible(False)
            else:
                goods_info = getattr(global_data.lobby_mall_data, func_str)()
                if not goods_info:
                    item_widget.btn_buy_common.btn.SetEnable(False)
                    item_widget.lab_price_common.SetString('******')
                else:
                    if getattr(item_widget.btn_buy_common, 'img_light'):
                        item_widget.btn_buy_common.img_light.setVisible(True)
                    item_widget.btn_buy_common.btn.SetEnable(True)
                    if self.is_pc_global_pay or mall_utils.is_steam_pay():
                        price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                    else:
                        key = goods_info['goodsid']
                        price_txt = mall_utils.get_charge_price_str(key)
                    item_widget.lab_price_common.SetString(mall_utils.adjust_price(str(price_txt)))

                    @item_widget.btn_buy_common.btn.unique_callback()
                    def OnClick(btn, touch, _goods_info=goods_info):
                        if self.is_pc_global_pay:
                            jump_to_ui_utils.jump_to_web_charge()
                        elif _goods_info:
                            global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

    def show_gifts(self):
        self.refresh_gifts()
        self._timer_cb[0] = self.second_simulate_up

    def refresh_gifts(self):
        self.up_tick_goal_num()
        self._update_achieve_widget()

    def try_get_global_achieve(self, aid):
        lv = global_data.player.get_lv()
        if lv >= 10:
            global_data.player.try_get_global_achieve(aid)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(82172))

    def update_achieve_widget(self):
        self._update_achieve_widget()
        global_data.emgr.refresh_activity_redpoint.emit()

    def _update_achieve_widget(self):
        from logic.gutils.live_utils import format_view_person
        parent_id = self._parent_achieve_id
        achieve_conf = confmgr.get('global_achieve_data', str(parent_id), default=None)
        if not achieve_conf:
            return
        else:
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            nd_achieve_list = self.panel.list_achieve
            nd_achieve_list.SetInitCount(len(children_achieves))
            for i, achieve_item in enumerate(nd_achieve_list.GetAllItem()):
                aid = children_achieves[i]
                child_conf = confmgr.get('global_achieve_data', str(aid))
                des_num = child_conf.get('iCondValue')
                achieve_item.lab_name.SetString('{}'.format(format_view_person(des_num, num_format='%d')))
                achieve_item.btn_get.UnBindMethod('OnClick')
                reward_id = child_conf.get('iRewardID')
                reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                if not reward_list:
                    return
                show_tips = True
                has_receive = False
                global_stat = global_data.player.get_gl_reward_receive_state(aid)
                simulate_latest_num = int(self._tick_now_num_map.get(parent_id, 0))
                cond_val = confmgr.get('global_achieve_data', str(aid), 'iCondValue', default=0)
                if global_stat == ITEM_UNRECEIVED:
                    if simulate_latest_num >= cond_val:
                        achieve_item.lab_name.SetString(get_text_by_id(81708))
                        show_tips = False
                        achieve_item.btn_get.BindMethod('OnClick', lambda b, t, aid=aid: self.try_get_global_achieve(aid))
                elif global_stat == ITEM_RECEIVED:
                    has_receive = True
                    achieve_item.lab_name.SetString(get_text_by_id(80866))
                achieve_item.img_get.setVisible(has_receive)
                reward_items = achieve_item.item_list
                reward_items.SetInitCount(len(reward_list))
                for i, reward_item_widget in enumerate(reward_items.GetAllItem()):
                    reward_info = reward_list[i]
                    item_no, item_num = reward_info[0], reward_info[1]
                    reward_item_widget.btn_choose.SetFrames('', [None, None, None], False, None)
                    reward_item_widget.img_frame.setVisible(False)
                    reward_item_widget.img_shadow.setVisible(False)
                    reward_item_widget.lab_quantity.SetPosition('100%-7', 8)
                    reward_item_widget.lab_quantity.setScale(0.7, 0.7)
                    template_utils.init_tempate_mall_i_item(reward_item_widget, item_no, item_num=item_num, show_rare_degree=False, show_tips=show_tips)
                    reward_item_widget.item.SetColor(8421504 if global_stat == ITEM_UNGAIN else 16777215)

            if global_data.player.get_lv() >= 10:
                self.panel.btn_get.SetEnable(activity_utils.has_achieve_reward_lottery_global_reward(self._activity_define))
            else:
                self.panel.btn_get.SetEnable(True)
                self.panel.btn_get.SetShowEnable(False)
            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def second_simulate_up(self, *args):
        parent_id = self._parent_achieve_id
        _tick_goal_num = self._tick_goal_num_map.get(parent_id, None)
        _tick_now_num = self._tick_now_num_map.get(parent_id, None)
        if _tick_goal_num is None or _tick_now_num is None:
            return
        else:
            _tick_now_num += self._second_tick_increase_num_map[parent_id]
            if _tick_now_num >= _tick_goal_num:
                _tick_now_num = _tick_goal_num
            self._tick_now_num_map[parent_id] = _tick_now_num
            self._times += 1
            if self._times > self.INTERVAL_TIMES:
                self.up_tick_goal_num()
                self._times = 0
            self.update_progress()
            self._update_achieve_widget()
            return

    def update_global_stat(self, *args, **kargs):
        self.up_tick_goal_num()
        global_data.emgr.refresh_activity_redpoint.emit()

    def up_tick_goal_num(self):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            self.update_progress()
            return
        else:
            parent_id = self._parent_achieve_id
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            achieve_name = confmgr.get('global_achieve_data', str(children_achieves[0]), 'cGStatName', default='')
            latest_num = int(global_stat_data.get(str(parent_id), {}).get(achieve_name, 0))
            cond_vals = [
             0]
            for ca in children_achieves:
                cond_vals.append(confmgr.get('global_achieve_data', str(ca), 'iCondValue', default=0))

            cond_ranges = [ [cond_vals[i], cond_vals[i + 1]] for i in range(len(cond_vals) - 1) ]
            stage = 0
            for i, val in enumerate(cond_vals):
                if latest_num <= val:
                    stage = i
                    break

            stage -= 1
            if stage < 0:
                stage = len(cond_ranges) - 1
            cur_range = cond_ranges[stage]
            range_val = cur_range[1] - cur_range[0]
            _tick_now_num = self._tick_now_num_map.get(parent_id, 0)
            if self._is_first_open:
                last_cache = global_data.player or 0 if 1 else global_data.player.get_simulate_cache(parent_id)
                if last_cache >= latest_num:
                    last_cache = latest_num
                else:
                    last_cache = random.uniform(max(last_cache, max(cur_range[0], latest_num - 0.1 * range_val)), latest_num)
                _tick_now_num = last_cache
            if self._tick_goal_num_map.get(parent_id, 0) == latest_num:
                return
            self._tick_goal_num_map[parent_id] = latest_num
            self._tick_now_num_map[parent_id] = min(latest_num, _tick_now_num)
            self._second_tick_increase_num_map[parent_id] = max(int((latest_num - _tick_now_num) / self.SIMULATE_TIMES), 0)
            self._is_first_open = False
            return

    def update_progress(self):
        parent_id = self._parent_achieve_id
        children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
        simulate_latest_num = int(self._tick_now_num_map.get(parent_id, 0))
        children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
        cur_rank = 0
        last_cond_val = 0
        next_cond_val = 0
        for i, aid in enumerate(children_achieves):
            cond_val = confmgr.get('global_achieve_data', str(aid), 'iCondValue', default=0)
            if simulate_latest_num < cond_val:
                next_cond_val = cond_val
                break
            cur_rank = i
            last_cond_val = cond_val

        each_rank_percent = 1.0 / (len(children_achieves) - 1)
        if next_cond_val < last_cond_val:
            percent = 1.0
        elif next_cond_val == 0:
            percent = 0.0
        else:
            percent = each_rank_percent * cur_rank + (simulate_latest_num - last_cond_val) * 1.0 / (next_cond_val - last_cond_val) * each_rank_percent
        self.panel.progress_bar.SetPercent(percent * 100.0)