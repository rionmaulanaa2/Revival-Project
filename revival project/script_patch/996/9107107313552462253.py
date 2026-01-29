# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/WeekTaskWidget.py
from __future__ import absolute_import
from functools import cmp_to_key
from .CommonTaskWidget import CommonTaskWidget
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from common.framework import Functor
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils import task_utils

class WeekTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(WeekTaskWidget, self).__init__(parent, panel, task_type)
        temp_content = getattr(self.parent, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('battle_pass/i_new_pass_task_weekly')
        self.panel.nd_cut.AddChild('week_task', self.nd_content)
        self.nd_content.ResizeAndPosition()
        self.nd_content.SetPosition(*pos)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())

    def init_widget(self, need_hide=True):
        super(WeekTaskWidget, self).init_widget(need_hide)
        self.nd_content.lab_refresh.SetString(get_text_by_id(602009))
        self.init_task_content()

    def init_event(self):
        super(WeekTaskWidget, self).init_event()
        global_data.emgr.reset_week_task_content_event += self._on_reset_week_task

    @staticmethod
    def get_task_ids():
        player = global_data.player
        cur_week_no = player.get_cur_task_week_no()
        return player.get_week_task_ids(cur_week_no)

    def _on_reset_week_task(self):
        self.init_task_content()

    def init_task_content(self):
        player = global_data.player
        if not player:
            return
        self.task_ids = self.get_task_ids()
        self.task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self.task_dict = {}
        index = 0
        self.sview_content_height = 0
        sview_height = self.ui_view_list.getContentSize().height
        while self.sview_content_height < sview_height and index < len(self.task_ids):
            task_id = self.task_ids[index]
            nd_task_item = self.add_task_data(task_id)
            item_height = nd_task_item.getContentSize().height
            self.sview_content_height = item_height * (index + 1) / 3
            index += 1

        self.sview_index = index - 1
        self.add_list_view_check()

    def add_list_view_check(self):

        def scroll_callback(sender, eventType):
            if not self.is_check_sview:
                self.is_check_sview = True
                self.nd_content.SetTimeOut(0.033, self.check_sview)

        self.ui_view_list.addEventListener(scroll_callback)

    def check_sview(self):
        task_num = len(self.task_ids)
        self.sview_index = self.ui_view_list.AutoAddAndRemoveItem_MulCol(self.sview_index, self.task_ids, task_num, self.add_task_data, 400, 400, self.on_del_task_item)
        self.is_check_sview = False

    @staticmethod
    def check_red_point():
        for task_id in WeekTaskWidget.get_task_ids():
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        return False

    def destroy(self):
        global_data.emgr.reset_week_task_content_event -= self._on_reset_week_task
        super(WeekTaskWidget, self).destroy()