# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityYueDongXinYinTask.py
from __future__ import absolute_import
from logic.comsys.activity.Activity202203.ActivityQingMingTask import ActivityQingMingTask
from logic.gutils import mall_utils, task_utils
from logic.gcommon.common_const import activity_const
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityYueDongXinYinTask(ActivityQingMingTask):

    def on_init_panel(self):
        super(ActivityYueDongXinYinTask, self).on_init_panel()
        self.panel.lab_get_number.SetString(get_text_by_id(610807) + str(global_data.player.get_item_num_by_no(70200006)))

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.panel.lab_get_number.SetString(get_text_by_id(610807) + str(global_data.player.get_item_num_by_no(70200006)))
        self.show_list()
        self.show_exchange_reward()

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
        ui = global_data.ui_mgr.get_ui('ActivityCenterMainUI')
        if not ui:
            return
        else:
            page_tab_widget = ui.get_page_tab_widget()
            if not page_tab_widget:
                return
            cur_view_sub_page_widget = page_tab_widget.get_cur_view_sub_page_widget()
            if not cur_view_sub_page_widget:
                return
            cur_view_sub_page_widget.select_tab(activity_const.ACTIVITY_LIU2022_2)
            exchange_activity = page_tab_widget.get_cur_view_page_widget()
            if not exchange_activity or not exchange_activity.panel.isValid():
                return
            idx = exchange_activity._children_tasks.index(task_id)
            if idx < 0 or idx >= exchange_activity.panel.act_list.GetItemCount():
                return
            exchange_activity.panel.act_list.LocatePosByItem(idx)
            return

    def update_get_all_btn(self):
        receivable_task_num = len(self.get_all_receivable_tasks())
        if receivable_task_num >= 1:
            self.panel.nd_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(receivable_task_num))
        else:
            self.panel.nd_get_all.setVisible(False)

    def on_click_get_all_btn(self, *args):
        global_data.player.receive_tasks_reward([self.fixed_task_id, self.week_1_task_id, self.week_2_task_id])