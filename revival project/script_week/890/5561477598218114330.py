# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityArtCollectionCharge.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import mall_utils, task_utils
import common.cfg.confmgr as confmgr
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import cc

class ActivityArtCollectionCharge(ActivityBase):
    INTERVAL_TIMES = 15
    SIMULATE_TIMES = 15

    def __init__(self, dlg, activity_type):
        super(ActivityArtCollectionCharge, self).__init__(dlg, activity_type)
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
        self._goods_list = conf.get('goods_list')
        self._names = conf.get('gift_names')
        self._tags = conf.get('gift_tags')
        self._goods_func_list = conf.get('goods_func_list')
        self._wait_for_charge_result = None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_goods_reward,
           'receive_task_reward_succ_event': self.refresh_goods_reward,
           'buy_good_success': self.refresh_goods_reward,
           'buy_good_fail': self.buy_good_fail,
           'message_update_global_stat': self.update_global_stat,
           'message_update_global_reward_receive': self.update_achieve_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        pass

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

    def play_show_anim(self):
        if self.panel.HasAnimation('loop'):
            show_anim = 'show'

            def cb():
                if self.panel:
                    self.panel.runAction(cc.Sequence.create([
                     cc.DelayTime.create(0.8),
                     cc.CallFunc.create(lambda : self.panel and self.panel.PlayAnimation('loop') or show_anim)]))

            time = self.panel.GetAnimationMaxRunTime(show_anim)
            self.panel.PlayAnimation(show_anim)
            self.panel.SetTimeOut(time, cb)
        else:
            self.panel.PlayAnimation('show')

    def on_init_panel(self):
        self.play_show_anim()
        self.refresh_goods_reward(True)

    def update_one_item_widget(self, item_widget, i, is_init):
        func_list = self._goods_func_list[i]
        item_widget.lab_title.SetString(self._names[i])
        template_utils.set_widget_discount_tag(item_widget, self._tags[i])
        if is_init:
            if self._is_init_show and item_widget.HasAnimation('first_show_common'):
                ani_show = 'first_show_common' if 1 else 'show_common'
                if self._is_init_show and item_widget.HasAnimation('first_loop'):
                    ani_loop = 'first_loop' if 1 else 'loop'
                    item_widget.PlayAnimation(ani_show)
                    item_widget.PlayAnimation(ani_loop)
                goods_id = self._goods_list[i]
                reward_id = mall_utils.get_goods_item_reward_id(goods_id)
                if reward_id:
                    reward_conf = confmgr.get('common_reward_data', str(reward_id))
                    return reward_conf or None
                reward_list = self.get_reward_list(reward_id)
                reward_count = len(reward_list)
                item_widget.list_item.SetInitCount(reward_count)
                all_items = item_widget.list_item.GetAllItem()
                for idx, item in enumerate(all_items):
                    item_no, item_num = reward_list[idx]
                    template_utils.init_tempate_mall_i_item(item.temp_item, item_no, show_tips=True, show_rare_vx=idx == 0)
                    item.lab_num.SetString('x%d' % item_num)
                    item.temp_item.lab_quantity.setVisible(False)
                    item.pnl_today.setVisible(False)
                    item.lab_name_day.setVisible(False)

            has_bought = mall_utils.limite_pay(goods_id)
            limit_num_all = mall_utils.get_goods_limit_num_all(goods_id)
            item_widget.lab_limit.SetString(get_text_by_id(82279).format(limit_num_all))
            item_widget.lab_limit.setVisible(True)
            if getattr(item_widget.btn_buy, 'img_light'):
                item_widget.btn_buy.img_light.setVisible(False)
            if has_bought:
                item_widget.btn_buy.btn.SetEnable(False)
                item_widget.nd_btn.vx_btn.setVisible(False)
                item_widget.lab_text_off or item_widget.lab_price.SetString(12014)
            else:
                item_widget.lab_text_off.setVisible(True)
                item_widget.lab_text_off.SetString(get_text_by_id(12014))
                item_widget.lab_price.setVisible(False)
                item_widget.lab_text_on.setVisible(False)
        else:
            goods_info = global_data.lobby_mall_data.get_activity_sale_info(func_list)
            if not goods_info:
                item_widget.btn_buy.btn.SetEnable(False)
                item_widget.nd_btn.vx_btn.setVisible(False)
                item_widget.lab_price.SetString('******')
            else:
                if getattr(item_widget.btn_buy, 'img_light'):
                    item_widget.btn_buy.img_light.setVisible(True)
                item_widget.btn_buy.btn.SetEnable(True)
                item_widget.nd_btn.vx_btn.setVisible(True)
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    key = goods_info['goodsid']
                    price_txt = mall_utils.get_charge_price_str(key)
                item_widget.lab_price.SetString(mall_utils.adjust_price(str(price_txt)))

                @item_widget.btn_buy.btn.unique_callback()
                def OnClick(btn, touch, _goods_info=goods_info, i=i):
                    self._wait_for_charge_result = i
                    if self.is_pc_global_pay:
                        jump_to_ui_utils.jump_to_web_charge()
                    elif _goods_info:
                        global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

    def update_free_item_widget(self, item_widget, i, is_init):
        item_widget.lab_title.SetString(self._names[i])
        if is_init:
            ani_show = 'first_show_common' if self._is_init_show and item_widget.HasAnimation('first_show_common') else 'show_common'
            ani_loop = 'first_loop' if self._is_init_show and item_widget.HasAnimation('first_loop') else 'loop'
            item_widget.PlayAnimation(ani_show)
            item_widget.PlayAnimation(ani_loop)
        goods_id = self._goods_list[i]
        task_id = mall_utils.get_goods_item_task_id(goods_id)
        children_tasks = task_utils.get_children_task(task_id)
        item_widget.list_item.SetInitCount(len(children_tasks))
        item_widget.lab_limit.setVisible(False)
        total_prog = task_utils.get_total_prog(task_id)
        cur_prog = global_data.player.get_task_prog(task_id)
        can_receive_task = []
        for taks_index, sub_task_id in enumerate(children_tasks):
            item = item_widget.list_item.GetItem(taks_index)
            item.lab_name_day.setString(get_text_by_id(604004).format(taks_index + 1))
            item.lab_name_day.setVisible(True)
            item.pnl_today.setVisible(taks_index == cur_prog - 1)
            reward_id = task_utils.get_task_reward(sub_task_id)
            has_rewarded = global_data.player.has_receive_reward(sub_task_id)
            if not has_rewarded:
                can_receive_task.append(sub_task_id)
            if reward_id:
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    log_error('reward_id is not exist in common_reward_data', reward_id)
                    return
                reward_list = self.get_reward_list(reward_id)
                item_no, item_num = reward_list[0]
                is_get = has_rewarded
                template_utils.init_tempate_mall_i_item(item.temp_item, item_no, item_num, is_get, show_tips=True, show_rare_vx=False)
                if not has_rewarded and cur_prog == taks_index + 1:
                    item.temp_item.nd_get_tips.setVisible(True)
                    item.temp_item.PlayAnimation('get_tips')
                else:
                    item.temp_item.StopAnimation('get_tips')
                    item.temp_item.nd_get_tips.setVisible(False)
                item.lab_num.SetString('x%d' % item_num)
                item.temp_item.lab_quantity.setVisible(False)

        btn_buy = item_widget.btn_buy.btn
        can_receive_count = len(can_receive_task)
        item_widget.lab_price.setVisible(False)
        if cur_prog >= total_prog and not can_receive_task:
            btn_buy.SetEnable(False)
            item_widget.nd_btn.vx_btn.setVisible(False)
            item_widget.lab_text_off.setVisible(True)
            item_widget.lab_text_off.SetString(get_text_by_id(80866))
            item_widget.lab_text_on.setVisible(False)
        elif cur_prog <= 0 or can_receive_task and can_receive_count > total_prog - cur_prog:
            btn_buy.SetEnable(True)
            item_widget.nd_btn.vx_btn.setVisible(True)
            item_widget.lab_text_on.setVisible(True)
            item_widget.lab_text_on.SetString(get_text_by_id(80930))
            item_widget.lab_text_off.setVisible(False)
        else:
            btn_buy.SetEnable(False)
            item_widget.nd_btn.vx_btn.setVisible(False)
            item_widget.lab_text_off.setVisible(True)
            item_widget.lab_text_off.SetString(get_text_by_id(606046))
            item_widget.lab_text_on.setVisible(False)

        @btn_buy.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            lv = player.get_lv()
            if lv >= 10:
                for sub_task_id in can_receive_task:
                    global_data.player.receive_task_reward(sub_task_id)

            else:
                global_data.game_mgr.show_tip(get_text_by_id(82172))

    def refresh_goods_reward(self, is_init=False):
        self._wait_for_charge_result = None
        goods_num = len(self._goods_list)
        if goods_num == 5:
            list_1_num = 2
        else:
            list_1_num = 3
        self.panel.list_1.SetInitCount(list_1_num)
        index = 0
        item_widget = self.panel.list_1.GetItem(index)
        self.update_free_item_widget(item_widget, index, is_init)
        for i in range(1, list_1_num):
            item_widget = self.panel.list_1.GetItem(i)
            item_widget.setLocalZOrder(10 - i)
            self.update_one_item_widget(item_widget, i, is_init)

        start_index = list_1_num
        index = 0
        self.panel.list_2.SetInitCount(3)
        for i in range(start_index, goods_num):
            item_widget = self.panel.list_2.GetItem(index)
            item_widget.setLocalZOrder(10 - i)
            index += 1
            self.update_one_item_widget(item_widget, i, is_init)

        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def buy_good_fail(self):
        if self._wait_for_charge_result is None:
            return
        else:
            fail_ui = global_data.ui_mgr.show_ui('ChargeGiftBoxFailUI', 'logic.comsys.common_ui')
            fail_ui.show_panel(self._goods_list[self._wait_for_charge_result], self._goods_func_list[self._wait_for_charge_result], self._tags[self._wait_for_charge_result], global_data.lobby_mall_data.get_activity_sale_info(self._goods_func_list[self._wait_for_charge_result]))
            self._wait_for_charge_result = None
            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def update_achieve_widget(self):
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_global_stat(self, *args, **kargs):
        global_data.emgr.refresh_activity_redpoint.emit()

    def get_reward_list(self, reward_id):
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        return reward_conf.get('reward_list', [])