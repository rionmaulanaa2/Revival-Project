# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/TrainBattleWidget.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.gutils import task_utils
from logic.comsys.task.CommonTaskWidget import CommonTaskWidget
TASK_WARM_UP_ID = '1900110'
TASK_RECOVER_ID = '1900115'
TASK_ELITE_ID = '1900119'
ALL_TASK = [TASK_WARM_UP_ID, TASK_RECOVER_ID, TASK_ELITE_ID]

class TrainBattleWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(TrainBattleWidget, self).__init__(parent, panel, task_type)
        self.nd_content = self.panel
        self._last_select_task = None
        return

    def init_widget(self, need_hide=False):
        super(TrainBattleWidget, self).init_widget(need_hide)
        self._init_top_tab()

    def _init_top_tab(self):
        from logic.gutils.new_template_utils import init_top_tab_list

        def click_cb(item, idx):
            select_task_id = ALL_TASK[idx]
            if select_task_id != self._last_select_task:
                self._last_select_task = select_task_id
                self.task_ids = task_utils.get_children_task(select_task_id)
                self._init_task_content()

        data_list = []
        for task_id in ALL_TASK:
            name_txt = task_utils.get_task_name(task_id)
            data_list.append({'text': name_txt})

        init_top_tab_list(self.panel.list_mid_btn, data_list, click_cb)
        if self._last_select_task is None:
            self.panel.list_mid_btn.GetItem(0).btn_tab.OnClick(None)
        self._update_top_tab_red()
        return

    def _update_top_tab_red(self):
        for idx, task_id in enumerate(ALL_TASK):
            btn_item = self.panel.list_mid_btn.GetItem(idx)
            if not global_data.player:
                need_red = False if 1 else global_data.player.has_unreceived_task_reward(str(task_id))
                btn_item.img_red.setVisible(need_red)

    def _init_task_content(self):
        self.panel.list_task.DeleteAllSubItem()
        if not self.task_ids or not global_data.player:
            return
        self.task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self.task_dict = {}
        index = 0
        self.sview_content_height = 0
        s_view_height = self.ui_view_list.getContentSize().height
        while self.sview_content_height <= s_view_height and index < len(self.task_ids):
            task_id = self.task_ids[index]
            nd_task_item = self.add_task_data(task_id)
            item_height = nd_task_item.getContentSize().height
            self.sview_content_height += item_height
            index += 1

        self.sview_index = index - 1

        def scroll_callback(sender, eventType):
            if not self.is_check_sview and self.nd_content:
                self.is_check_sview = True
                self.nd_content.SetTimeOut(0.033, self.check_sview)

        self.ui_view_list.addEventListener(scroll_callback)

    def check_sview(self):
        task_num = len(self.task_ids)
        self.sview_index = self.ui_view_list.AutoAddAndRemoveItem_MulCol(self.sview_index, self.task_ids, task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    def _on_update_task_prog(self, task_changes):
        super(TrainBattleWidget, self)._on_update_task_prog(task_changes)
        self._update_top_tab_red()

    def _on_receive_reward_succ(self, task_id):
        super(TrainBattleWidget, self)._on_receive_reward_succ(task_id)
        self._update_top_tab_red()

    def destroy(self):
        self.parent = None
        self.panel = None
        self.nd_content = None
        self.task_dict = None
        self.task_ids = []
        global_data.emgr.receive_task_reward_succ_event -= self._on_receive_reward_succ
        return


class ReturnTrainTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(ReturnTrainTaskWidget, self).__init__(parent, panel, task_type)
        self.nd_content = self.panel
        for parent_task_id in ALL_TASK:
            self.task_ids.extend(task_utils.get_children_task(parent_task_id))

    def init_widget(self, need_hide=False):
        super(ReturnTrainTaskWidget, self).init_widget(need_hide)
        self._init_task_content()

    def _init_task_content(self):
        if not self.task_ids or not global_data.player:
            return
        self.task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self.task_dict = {}
        index = 0
        self.sview_content_height = 0
        s_view_height = self.ui_view_list.getContentSize().height
        while self.sview_content_height <= s_view_height and index < len(self.task_ids):
            task_id = self.task_ids[index]
            nd_task_item = self.add_task_data(task_id)
            item_height = nd_task_item.getContentSize().height
            self.sview_content_height += item_height
            index += 1

        self.sview_index = index - 1

        def scroll_callback(sender, eventType):
            if not self.is_check_sview and self.nd_content:
                self.is_check_sview = True
                self.nd_content.SetTimeOut(0.033, self.check_sview)

        self.ui_view_list.addEventListener(scroll_callback)

    def check_sview(self):
        task_num = len(self.task_ids)
        self.sview_index = self.ui_view_list.AutoAddAndRemoveItem_MulCol(self.sview_index, self.task_ids, task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    @staticmethod
    def check_red_point():
        pass