# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncGoodsTaskListWidget.py
from __future__ import absolute_import
from .AsyncTaskListWidget import AsyncTaskListWidget
from common.cfg import confmgr
from logic.gutils.mall_utils import limite_pay
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_INACTIVE
from logic.gutils import task_utils

class AsyncGoodsTaskListWidget(AsyncTaskListWidget):

    def on_init_panel(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._goods_id = ui_data.get('game_goods_id', '')
        super(AsyncGoodsTaskListWidget, self).on_init_panel()

    def _refresh_task_list(self):
        player = global_data.player
        fixed_task_list = task_utils.get_children_task(self._fixed_task_id)
        if not fixed_task_list:
            log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe5\x9b\xba\xe5\xae\x9a\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._fixed_task_id)
            fixed_task_list = [self._fixed_task_id]
        else:
            fixed_task_list = fixed_task_list[1:]
        if self._random_task_id:
            random_refresh_type = task_utils.get_task_fresh_type(self._random_task_id)
            random_task_list = player.get_random_children_tasks(random_refresh_type, self._random_task_id)
            if not random_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._random_task_id)
                random_task_list = []
            task_list = fixed_task_list + random_task_list
        else:
            task_list = fixed_task_list
        if task_list:
            task_list = self._reorder_task_list(task_list)
        self._task_list = task_list

    def _update_receive_btn(self, task_id, status, ui_item):
        if limite_pay(self._goods_id):
            super(AsyncGoodsTaskListWidget, self)._update_receive_btn(task_id, status, ui_item)
        else:
            btn_receive = ui_item.temp_common.nd_task.temp_btn_get
            update_task_list_btn(btn_receive, BTN_ST_INACTIVE)