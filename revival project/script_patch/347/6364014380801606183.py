# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityYueDongXinYinExchange.py
from __future__ import absolute_import
from logic.comsys.activity.Activity202203.ActivityQingMingExchange import ActivityQingMingExchange
from logic.gutils import mall_utils, task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityYueDongXinYinExchange(ActivityQingMingExchange):

    def on_init_panel(self):
        super(ActivityYueDongXinYinExchange, self).on_init_panel()
        self.panel.lab_get_number.SetString(get_text_by_id(610807) + str(global_data.player.get_item_num_by_no(70200006)))

    def show_exchange_reward(self):
        for idx, task_id in enumerate(self._exchange_tasks):
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                return
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            btn_item = getattr(self.panel, 'btn_item_' + str(idx + 1), False)
            if not btn_item:
                return

            @btn_item.unique_callback()
            def OnClick(btn, touch, item_no=target_item_no, _task_id=task_id):
                self.on_click_btn_item(btn, item_no, _task_id)

    def on_click_btn_item(self, btn, item_no, task_id):
        x, y = btn.GetPosition()
        w, h = btn.GetContentSize()
        x += w * 0.5
        wpos = btn.ConvertToWorldSpace(x, y)
        extra_info = {'show_jump': False}
        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=1)
        idx = self._children_tasks.index(task_id)
        if idx < 0 or idx >= self.panel.act_list.GetItemCount():
            return
        else:
            self.panel.act_list.LocatePosByItem(idx)
            return

    def buy_good_success(self):
        global_data.player.read_activity_list(self._activity_type)
        self.panel.lab_get_number.SetString(get_text_by_id(610807) + str(global_data.player.get_item_num_by_no(70200006)))
        self.show_list()
        self.show_exchange_reward()