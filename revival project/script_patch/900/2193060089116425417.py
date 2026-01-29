# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/CommonTaskWidget.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_common_reward_list_simple
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils import task_utils
from logic.gcommon.common_const.task_const import TASK_TYPE_DAYLY
from logic.comsys.lottery.LotteryTurntableSecondComfirm import LotteryTurntableSecondComfirm

class CommonTaskWidget(object):

    def __init__(self, parent, panel, task_type, auto_sort=True):
        self.parent = parent
        self.panel = panel
        self.task_type = task_type
        self.nd_content = None
        self.task_dict = {}
        self.is_check_sview = False
        self.sview_index = 0
        self.sview_content_height = 0
        self.task_ids = []
        self.auto_sort = auto_sort
        return

    def init_event(self):
        global_data.emgr.task_prog_changed += self._on_update_task_prog
        global_data.emgr.receive_task_reward_succ_event += self._on_receive_reward_succ

    def _on_task_update(self, task_id):
        pass

    def init_widget(self, need_hide=True):
        self.ui_view_list = self.nd_content.list_task
        if need_hide:
            self.set_visible(False)
        self.init_event()

    def set_visible(self, is_visible):
        self.nd_content.setVisible(is_visible)

    def _on_update_task_prog(self, task_changes):
        for task_change in task_changes:
            task_id = task_change.task_id
            if task_id not in self.task_ids:
                continue
            self._on_task_update(task_id)
            task_item = self.task_dict.get(task_id, None)
            if task_item:
                self._set_task_item_progress(task_item)
                self._set_task_reward_status(task_item)
            if self.auto_sort:
                self.resort_on_update_task_prog(task_id)

        return

    def resort_on_update_task_prog(self, task_id):
        list_task = self.nd_content.list_task
        task_ids = self.task_ids
        if task_id not in task_ids:
            return
        self._dynamic_ajust_task_list(list_task, task_ids, task_id)
        self.sview_index = task_ids.index(list_task.GetItem(-1).task_id)

    def _dynamic_ajust_task_list(self, list_task, task_ids, task_id):
        old_idx = task_ids.index(task_id)
        if list_task.GetItem(0).task_id not in task_ids:
            return
        start_idx = task_ids.index(list_task.GetItem(0).task_id)
        task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        list_num = list_task.GetItemCount()
        new_idx = task_ids.index(task_id)
        if old_idx == new_idx:
            return
        if start_idx <= old_idx < start_idx + list_num:
            del_item = list_task.GetItem(old_idx - start_idx)
            self.task_dict.pop(del_item.task_id)
            list_task.DeleteItemIndex(old_idx - start_idx)
            new_start_idx = task_ids.index(list_task.GetItem(0).task_id)
            if new_idx < new_start_idx:
                nd_task_item = list_task.AddTemplateItem(0)
                self.init_task_item(nd_task_item, task_ids[new_start_idx - 1])
            elif new_idx < new_start_idx + list_num:
                nd_task_item = list_task.AddTemplateItem(new_idx - new_start_idx)
                self.init_task_item(nd_task_item, task_id)
            else:
                nd_task_item = list_task.AddTemplateItem(list_num - 1)
                self.init_task_item(nd_task_item, task_ids[new_start_idx + list_num - 1])
        elif start_idx <= new_idx < start_idx + list_num - 1:
            del_item = list_task.GetItem(list_num - 1)
            self.task_dict.pop(del_item.task_id)
            list_task.DeleteItemIndex(list_num - 1)
            nd_task_item = list_task.AddTemplateItem(new_idx - start_idx)
            self.init_task_item(nd_task_item, task_id)

    def _on_receive_reward_succ(self, task_id):
        self._on_task_update(task_id)
        task_item = self.task_dict.get(task_id, None)
        if task_item:
            self._set_task_reward_status(task_item)
        if self.auto_sort:
            self.resort_on_update_task_prog(task_id)
        return

    def _set_task_reward_status(self, task_item):
        if not task_item:
            return
        task_item.temp_btn_get.setVisible(False)
        task_item.temp_btn_go.setVisible(False)
        task_item.nd_get.setVisible(False)
        task_item.lab_working.setVisible(False)
        status = global_data.player.get_task_reward_status(task_item.task_id)
        if status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_item.task_id)
            if jump_conf:
                task_item.temp_btn_go.setVisible(True)
            else:
                task_item.lab_working.setVisible(True)
        elif status == ITEM_UNRECEIVED:
            task_item.temp_btn_get.setVisible(True)
            if self.task_type == TASK_TYPE_DAYLY and task_item.btn_refresh:
                task_item.btn_refresh.setVisible(False)
        else:
            task_item.nd_get.setVisible(True)
            if self.task_type == TASK_TYPE_DAYLY and task_item.btn_refresh:
                task_item.btn_refresh.setVisible(False)

    def add_task_data(self, task_id, is_back_item=True, index=-1, ui_list=None):
        if ui_list:
            view_list = ui_list if 1 else self.ui_view_list
            if is_back_item:
                nd_task_item = view_list.AddTemplateItem(bRefresh=True)
            else:
                nd_task_item = view_list.AddTemplateItem(0, bRefresh=True)
            return nd_task_item or None
        else:
            self.init_task_item(nd_task_item, task_id)
            return nd_task_item

    def on_del_task_item(self, task_item, index):
        if task_item.task_id in self.task_dict:
            self.task_dict.pop(task_item.task_id)

    def init_task_item(self, nd_task_item, task_id):
        task_conf = task_utils.get_task_conf_by_id(task_id)
        nd_task_item.lab_task_name.SetString(task_utils.get_task_name(task_id))
        self.task_dict[task_id] = nd_task_item
        nd_task_item.task_id = task_id
        self._set_task_item_progress(nd_task_item)
        if self.task_type == TASK_TYPE_DAYLY:
            changed_list = global_data.player.get_changed_day_tasks()
            is_unstable = task_utils.is_can_refresh_task(task_id)
            if is_unstable and task_id not in changed_list:
                nd_task_item.btn_refresh.setVisible(True)
            else:
                nd_task_item.btn_refresh.setVisible(False)
            is_challenge = task_utils.is_challenge_task(task_id)
            if is_challenge:
                nd_task_item.nd_tag.setVisible(True)
            else:
                nd_task_item.nd_tag.setVisible(False)

            @nd_task_item.btn_refresh.unique_callback()
            def OnClick(btn, touch, tid=task_id):
                if tid:

                    def change_random_day_task():
                        global_data.player.change_random_day_task(tid)

                    LotteryTurntableSecondComfirm(text_id=634593, first_click_callback=None, second_click_callback=change_random_day_task)
                return

        reward_st = global_data.player.get_task_reward_status(task_id)
        self._set_task_reward_status(nd_task_item)
        reward_id = task_utils.get_task_reward(task_id)
        init_common_reward_list_simple(nd_task_item.list_award, reward_id)

        @nd_task_item.temp_btn_get.btn_common.unique_callback()
        def OnClick(btn, touch, tid=task_id):
            global_data.player.receive_task_reward(tid)

        jump_conf = task_utils.get_jump_conf(task_id)
        if jump_conf:
            func_name = jump_conf.get('func')
            if func_name in ('jump_to_weapon_type', 'jump_to_mecha_type'):
                nd_task_item.temp_btn_go.btn_common.SetText(get_text_by_id(80821))

            @nd_task_item.temp_btn_go.btn_common.unique_callback()
            def OnClick(btn, touch, tid=task_id):
                from logic.gutils import jump_to_ui_utils
                func_name = jump_conf.get('func')
                args = jump_conf.get('args', [])
                kargs = jump_conf.get('kargs', {})
                if func_name:
                    func = getattr(jump_to_ui_utils, func_name)
                    func and func(*args, **kargs)
                if func_name == 'jump_to_pve_level_select':
                    global_data.ui_mgr.close_ui('TaskMainUI')

        else:
            nd_task_item.temp_btn_go.btn_common.SetText(get_text_by_id(602014))

    def _set_task_item_progress(self, task_item):
        player = global_data.player
        if not player:
            return
        if not task_item:
            return
        task_id = task_item.task_id
        prog = player.get_task_prog(task_id)
        total_prog = task_utils.get_total_prog(task_id)
        task_item.nd_progress.lab_task_progress.SetString('%s/%s' % (prog, total_prog))
        task_item.nd_progress.progress_task.SetPercentage(100.0 * prog / total_prog)
        task_item.lab_task_name.SetString(task_utils.get_task_name(task_id))
        if prog >= total_prog:
            self._set_task_reward_status(task_item)

    @staticmethod
    def check_red_point():
        raise NotImplementedError

    def destroy(self):
        if self.nd_content:
            self.nd_content.Destroy()
        self.parent = None
        self.panel = None
        self.nd_content = None
        self.task_dict = None
        self.task_ids = []
        global_data.emgr.task_prog_changed -= self._on_update_task_prog
        global_data.emgr.receive_task_reward_succ_event -= self._on_receive_reward_succ
        return