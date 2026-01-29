# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGift.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityGift(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGift, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        from logic.gutils import task_utils
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        parent_task = ''
        reward_id = ''
        good_id = ''
        cur_param_index = 0
        func, param_dict = self.get_func_param(cur_param_index)
        if not func:
            reward_id = param_dict.get('reward_id', '')
            good_id = param_dict.get('goods_id', '')
            cur_param_index += 1
        if conf['cTask']:
            task_list = activity_utils.parse_task_list(conf['cTask'])
            if len(task_list) <= 0:
                return
            parent_task = task_list[0]
            tmp_reward_id = task_utils.get_task_reward(parent_task)
            reward_id = str(tmp_reward_id) if tmp_reward_id else reward_id
        if reward_id:
            template_utils.init_common_reward_list(self.panel.list_reward, reward_id)
        btn = self.panel.btn_buy
        nRet, text_id = self.exec_custom_condition(0)

        @btn.unique_callback()
        def OnClick(btn, touch):
            if nRet:
                self.exec_custom_func(cur_param_index)
            else:
                self.exec_custom_func(cur_param_index + 1)

        activity_utils.set_btn_text(btn, nRet, text_id)
        if good_id:
            self.set_good_info(good_id)

    def set_good_info(self, good_id):
        from logic.gutils import mall_utils
        from logic.gcommon.common_utils.local_text import get_text_by_id
        temp_price = self.panel.temp_price
        lab_discount = self.panel.lab_discount
        prices = mall_utils.get_mall_item_price(good_id)
        for i, price_info in enumerate(prices):
            if temp_price:
                template_utils.init_price_template(price_info, temp_price)
            original_price = price_info.get('original_price')
            discount_price = price_info.get('discount_price')
            if lab_discount:
                lab_discount.SetString(get_text_by_id(606044, ('%d%%' % ((1.0 - float(discount_price) / float(original_price)) * 100),)))
            break