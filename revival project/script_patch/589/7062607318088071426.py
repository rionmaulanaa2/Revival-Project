# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/AssessTaskWidget.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from .CommonTaskWidget import CommonTaskWidget
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from common.framework import Functor
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils import task_utils
from logic.gutils.new_template_utils import init_top_tab_list
from logic.gcommon.common_const.task_const import TASK_TYPE_DAYLY, TASK_TYPE_WEEKLY, TASK_TYPE_ASSESS

class AssessTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(AssessTaskWidget, self).__init__(parent, panel, task_type)
        temp_content = getattr(self.parent, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('battle_pass/i_new_pass_task_challenge')
        self.panel.nd_cut.AddChild('assess_task', self.nd_content)
        self.nd_content.ResizeAndPosition()
        self.nd_content.SetPosition(*pos)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())
        self.sview_index_dict = {}
        self.sview_content_height_dict = {}
        self.task_ids_dict = {}
        self.top_tab_list = None
        self.cur_unlock_lv = 1
        self.cur_nbp_lv, _ = global_data.player.get_newbiepass_info()
        return

    def init_event(self):
        super(AssessTaskWidget, self).init_event()
        global_data.emgr.unlock_assess_task_event += self._on_unlock_assess_task
        global_data.emgr.sum_vitality_changed_event += self._on_sum_vitality_changed
        global_data.emgr.receive_task_reward_succ_event += self._refresh_red_point

    def init_widget(self, need_hide=True):
        super(AssessTaskWidget, self).init_widget(need_hide)
        certificate_lvs = task_utils.get_assess_unlock_levels()
        if certificate_lvs:
            data_list = []
            for unlock_lv in certificate_lvs:
                unlock_lv = int(unlock_lv)
                certificate_conf = task_utils.get_assess_unlock_conf(unlock_lv)
                data_list.append({'text': certificate_conf['certificate_name']})

            init_top_tab_list(self.nd_content.pnl_list_top_tab, data_list, self.on_click_certificate)
            for unlock_lv in certificate_lvs:
                self.init_top_tab(int(unlock_lv))

            certificate_content = self.get_certificate_task_content(int(certificate_lvs[0]))
            if certificate_content:
                self.on_click_certificate(None, 0)
                default_tab = self.nd_content.pnl_list_top_tab.GetItem(0)
                default_tab.btn_tab.SetSelect(True)
                default_tab.PlayAnimation('click')
        return

    @staticmethod
    def get_task_ids(unlock_lv):
        return global_data.player.get_assess_task_ids(unlock_lv)

    def on_click_certificate(self, item, index):
        certificate_lvs = task_utils.get_assess_unlock_levels()
        old_certificate_content = self.get_certificate_task_content(self.cur_unlock_lv)
        if old_certificate_content:
            old_certificate_content.setVisible(False)
        self.cur_unlock_lv = int(certificate_lvs[index])
        certificate_content = self.get_certificate_task_content(self.cur_unlock_lv)
        if self.cur_unlock_lv not in self.task_ids_dict:
            self.init_task_content(self.cur_unlock_lv, False)
        if certificate_content:
            certificate_content.setVisible(True)
            self.ui_view_list = certificate_content.list_task

    def _on_unlock_assess_task(self, unlock_lv):
        self.init_task_content(unlock_lv, False)

    def _on_sum_vitality_changed(self):
        unlock_lvs = global_data.player.get_assess_unlock_levels()
        sum_vitality = global_data.player.get_sum_vitality()
        for lv in range(1, len(unlock_lvs) + 1):
            certificate_content = self.get_certificate_task_content(lv)
            if not certificate_content:
                return
            unlock_text = get_text_by_id(602008)
            unlock_vitality = task_utils.get_assess_unlock_vitality(lv)
            certificate_content.nd_empty.lab_unlock.SetString(unlock_text.format(sum_vitality, unlock_vitality, unlock_vitality))

    def init_top_tab(self, unlock_lv):
        unlock_vitality = task_utils.get_assess_unlock_vitality(unlock_lv)
        sum_vitality = global_data.player.get_sum_vitality()
        if sum_vitality >= unlock_vitality:
            unlock_lvs = global_data.player.get_assess_unlock_levels()
            idx = unlock_lvs.index(unlock_lv)
            if self.check_lv_red_point(unlock_lv):
                self.nd_content.pnl_list_top_tab.GetItem(idx).img_red_dot.setVisible(True)
            else:
                self.nd_content.pnl_list_top_tab.GetItem(idx).img_red_dot.setVisible(False)

    def init_task_content(self, unlock_lv, need_hide=True):
        certificate_content = self.get_certificate_task_content(unlock_lv)
        if not certificate_content:
            return
        unlock_vitality = task_utils.get_assess_unlock_vitality(unlock_lv)
        sum_vitality = global_data.player.get_sum_vitality()
        if global_data.player.get_sum_vitality() < unlock_vitality:
            certificate_content.nd_empty.setVisible(True)
            unlock_text = get_text_by_id(602008)
            certificate_content.nd_empty.lab_unlock.SetString(unlock_text.format(sum_vitality, unlock_vitality, unlock_vitality))
            certificate_content.list_task.setVisible(False)
        else:
            certificate_content.nd_empty.setVisible(False)
            certificate_content.list_task.setVisible(True)
            task_ids = self.get_task_ids(unlock_lv)
            task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
            self.task_ids_dict[unlock_lv] = task_ids
            index = 0
            sview_height = certificate_content.list_task.getContentSize().height
            self.sview_content_height_dict[unlock_lv] = 0
            task_num = len(self.task_ids_dict[unlock_lv])
            while self.sview_content_height_dict[unlock_lv] < sview_height + 130 and index < task_num:
                task_id = self.task_ids_dict[unlock_lv][index]
                nd_task_item = self.add_task_data(task_id, True, certificate_content.list_task)
                item_height = nd_task_item.getContentSize().height
                self.sview_content_height_dict[unlock_lv] += item_height
                index += 1

            self.sview_index_dict[unlock_lv] = index - 1
            certificate_content.list_task.addEventListener(self.scroll_callback)
        if need_hide:
            certificate_content.setVisible(False)

    def resort_on_update_task_prog(self, task_id):
        assess_task_data = confmgr.get('task/assess_task_data', 'TaskData', default={})
        unlock_lv = assess_task_data.get(task_id, {}).get('unlock_level', None)
        if unlock_lv is None:
            return
        else:
            certificate_content = self.get_certificate_task_content(unlock_lv)
            if not certificate_content:
                return
            list_task = certificate_content.list_task
            if unlock_lv not in self.task_ids_dict:
                return
            task_ids = self.task_ids_dict[unlock_lv]
            if task_id not in task_ids:
                return
            self._dynamic_ajust_task_list(list_task, task_ids, task_id)
            self.sview_index_dict[unlock_lv] = task_ids.index(list_task.GetItem(-1).task_id)
            return

    def scroll_callback(self, *args):
        if not self.is_check_sview:
            self.is_check_sview = True
            certificate_content = self.get_certificate_task_content(self.cur_unlock_lv)
            if certificate_content:
                certificate_content.SetTimeOut(0.033, self.check_sview)

    def check_sview(self, *args):
        if self.cur_unlock_lv not in self.task_ids_dict or self.cur_unlock_lv not in self.sview_index_dict:
            return
        task_num = len(self.task_ids_dict[self.cur_unlock_lv])
        self.sview_index_dict[self.cur_unlock_lv] = self.ui_view_list.AutoAddAndRemoveItem(self.sview_index_dict[self.cur_unlock_lv], self.task_ids_dict[self.cur_unlock_lv], task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    def get_certificate_task_content(self, unlock_lv):
        if unlock_lv is None:
            return
        else:
            if unlock_lv == 1:
                return self.nd_content.temp_content
            nd_name = 'nd_certificate_%s' % unlock_lv
            if not getattr(self.nd_content, nd_name):
                temp_content = self.nd_content.temp_content
                pos = temp_content.GetPosition()
                certificate_content = global_data.uisystem.load_template_create('task/i_task_challenge_content')
                self.nd_content.AddChild(nd_name, certificate_content)
                certificate_content.ResizeAndPosition()
                certificate_content.SetPosition(*pos)
                certificate_content.setAnchorPoint(temp_content.getAnchorPoint())
            return getattr(self.nd_content, nd_name)
            return

    def _refresh_red_point(self, task_id):
        unlock_lvs = global_data.player.get_assess_unlock_levels()
        for idx in range(len(unlock_lvs)):
            unlock_lv = unlock_lvs[idx]
            task_ids = self.get_task_ids(unlock_lv)
            if task_id in task_ids:
                redpoint = self.check_lv_red_point(unlock_lv)
                self.nd_content.pnl_list_top_tab.GetItem(idx).img_red_dot.setVisible(redpoint)
                return

    @staticmethod
    def check_red_point():
        unlock_lvs = global_data.player.get_assess_unlock_levels()
        for unlock_lv in unlock_lvs:
            if AssessTaskWidget.check_lv_red_point(unlock_lv):
                return True

        return False

    @staticmethod
    def check_lv_red_point(unlock_lv):
        for task_id in AssessTaskWidget.get_task_ids(unlock_lv):
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        return False

    def destroy(self):
        self.sview_index_dict = None
        self.sview_content_height_dict = None
        self.task_ids_dict = None
        global_data.emgr.unlock_assess_task_event -= self._on_unlock_assess_task
        global_data.emgr.sum_vitality_changed_event -= self._on_sum_vitality_changed
        global_data.emgr.receive_task_reward_succ_event -= self._refresh_red_point
        super(AssessTaskWidget, self).destroy()
        return