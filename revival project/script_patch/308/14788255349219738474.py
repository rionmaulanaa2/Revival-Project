# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncChristmasBtnTaskListWidget.py
from __future__ import absolute_import
from .AsyncTaskListWidget import AsyncTaskListWidget
from logic.gutils import task_utils

def update_task_list_btn(nd_btn, status, extra_args=None):
    status_dict = {1: {'text_color': 7616256,'btn_text': 604030,'enable': True},4: {'text_color': 14674164,'btn_text': 604031,'enable': False},5: {'show_nd_get': True,'enable': False},8: {'text_color': 2369169,'btn_text': 906672,'enable': False}}
    if status not in status_dict:
        return
    else:
        if not extra_args:
            extra_args = {}
        text_color = status_dict[status].get('text_color')
        extra_btn_text = extra_args.get('btn_text', '')
        btn_text = extra_btn_text if extra_btn_text else status_dict[status].get('btn_text', '')
        nd_btn.btn_common.SetText(btn_text)
        extra_enable = extra_args.get('enable')
        if extra_enable is not None:
            nd_btn.btn_common.SetEnable(extra_enable)
            nd_btn.btn_common.SetSelect(extra_enable)
        else:
            nd_btn.btn_common.SetEnable(True)
            nd_btn.btn_common.SetSelect(status_dict[status].get('enable', True))
        show_nd_get = status_dict[status].get('show_nd_get')
        if show_nd_get:
            nd_btn.btn_common.SetText('')
            nd_btn.btn_common.setVisible(False)
            nd_btn.nd_get.setVisible(True)
        else:
            nd_btn.btn_common.setVisible(True)
            nd_btn.nd_get.setVisible(False)
        return


class AsyncChristmasBtnTaskListWidget(AsyncTaskListWidget):

    def _update_receive_btn(self, task_id, status, ui_item):
        from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
        from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO
        if ui_item.temp_common:
            ui_item = ui_item.temp_common
        btn_receive = ui_item.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
            for reward_item in ui_item.list_reward.GetAllItem():
                reward_item.nd_get.setVisible(True)

        elif status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                update_task_list_btn(btn_receive, BTN_ST_GO, {'btn_text': jump_conf.get('unreach_text', '')})
            else:
                update_task_list_btn(btn_receive, BTN_ST_ONGOING)
            for reward_item in ui_item.list_reward.GetAllItem():
                reward_item.nd_get.setVisible(False)

        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)
            for reward_item in ui_item.list_reward.GetAllItem():
                reward_item.nd_get.setVisible(False)

    def set_task_id(self, fix_task_id, random_task_id, force_task_list):
        self._fixed_task_id = fix_task_id
        self._random_task_id = random_task_id
        self._force_task_list = force_task_list
        self.refresh_panel()