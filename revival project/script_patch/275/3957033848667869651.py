# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityTreasurePavilionTaskPanelUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import exec_jump_to_ui_info
from logic.gcommon.time_utility import get_simply_readable_time, get_server_time
from common.utils.timer import CLOCK
from logic.gutils import task_utils
from common.cfg import confmgr

class ActivityTreasurePavilionTaskPanelUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202401/cangbaoge/i_cangbaoge_task'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'receive_task_reward_succ_event': '_on_receive_task_reward',
       'receive_task_prog_reward_succ_event': '_on_receive_task_reward',
       'task_prog_changed': '_on_task_prog_changed'
       }

    def on_init_panel(self, activity_type=None, *args, **kwargs):
        super(ActivityTreasurePavilionTaskPanelUI, self).on_init_panel()
        self.init_params(activity_type)
        self.init_ui()

    def init_params(self, activity_type):
        self._activity_type = activity_type
        self._activity_conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self._parent_task_id_list = self._get_parent_task_id()
        self._children_task_id_list = self._get_children_task_id()
        self._cur_select_tab = None
        self._btn_tab_dict = {}
        self._task_item_dict = {}
        self._bar_refresh_dict = {}
        self._list_task_dict = {}
        self._week_parent_task_id = None
        self._lab_tips_time = None
        self._timer = None
        self._remain_time = None
        return

    def init_ui(self):
        self._init_tab_btn()
        self._init_list_task()

    def _get_parent_task_id(self):
        all_parent_task_id = self._activity_conf.get('cTask')
        parent_task_list = task_utils.get_children_task(all_parent_task_id)
        return parent_task_list

    def _get_children_task_id(self):
        children_task_id_list = []
        for i, parent_task_id in enumerate(self._parent_task_id_list):
            children_task_list = task_utils.get_children_task(parent_task_id)
            for index, task_id in enumerate(children_task_list):
                if not task_utils.is_task_open(task_id):
                    continue
                children_task_id_list.append(task_id)

        return children_task_id_list

    def _init_tab_btn(self):
        list_tab = self.panel.list_tab
        for index, node in enumerate(list_tab.GetAllItem()):
            btn_tab = node.btn_tab
            type_index = index + 1
            if type_index > len(self._parent_task_id_list):
                btn_tab.setVisible(False)
            else:
                parent_task_id = self._parent_task_id_list[index]
                self._btn_tab_dict[parent_task_id] = btn_tab
                btn_tab.setVisible(True)
                btn_tab.EnableCustomState(True)
                if index == 0:
                    btn_tab.SetSelect(True)
                    self._cur_select_tab = btn_tab
                self._update_tab_btn_redpoint(parent_task_id)

                @btn_tab.unique_callback()
                def OnClick(btn, touch, type_index=type_index):
                    if self._cur_select_tab:
                        self._cur_select_tab.SetSelect(False)
                    btn.SetSelect(True)
                    self._cur_select_tab = btn
                    self._on_click_btn_tab(type_index)

    def _on_click_btn_tab(self, type_index):
        bar_refresh = self._bar_refresh_dict.get(type_index)
        if bar_refresh:
            self.panel.list_task.TopWithNode(bar_refresh)

    def _init_list_task(self):
        temp_list_task = self.panel.list_task
        temp_list_task.DeleteAllSubItem()
        self._list_task = temp_list_task.AddTemplateItem()
        for i, parent_task_id in enumerate(self._parent_task_id_list):
            type_index = i + 1
            bar_refresh = getattr(self._list_task, 'bar_refresh_{}'.format(type_index), None)
            list_task = getattr(self._list_task, 'list_task_{}'.format(type_index), None)
            lab_time = getattr(bar_refresh, 'lab_time_{}'.format(type_index), None)
            if bar_refresh and list_task:
                self._bar_refresh_dict[type_index] = bar_refresh
                self._list_task_dict[type_index] = list_task
                nd_auto_fit = lab_time.nd_auto_fit
                if nd_auto_fit:
                    lab_tips_time = nd_auto_fit.lab_tips_time
                    if lab_tips_time:
                        self._week_parent_task_id = parent_task_id
                        self._lab_tips_time = lab_tips_time
                        self._init_lab_tips_time()
            temp_children_task_list = task_utils.get_children_task(parent_task_id)
            children_task_list = []
            for task_id in temp_children_task_list:
                if task_utils.is_task_open(task_id):
                    children_task_list.append(task_id)

            for index, task_id in enumerate(children_task_list):
                item = list_task.GetItem(index)
                self._task_item_dict[str(task_id)] = item
                prog_reward_list = task_utils.get_prog_rewards(task_id)
                if prog_reward_list:
                    self._update_prog_task_item(task_id)
                else:
                    total_prog = task_utils.get_total_prog(task_id)
                    reward_id = task_utils.get_task_reward(task_id)
                    item.lab_name.SetString(task_utils.get_task_name(task_id))
                    task_prog = global_data.player.get_task_prog(task_id) if global_data.player else 0
                    item.lab_num.SetString('%d/%d' % (task_prog, total_prog))
                    reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                    init_tempate_mall_i_item(item.temp_reward, reward_list[0][0], reward_list[0][1], show_tips=True)

                    @item.temp_btn_get.btn_common.unique_callback()
                    def OnClick(btn, touch, task_id=task_id):
                        global_data.player and global_data.player.receive_tasks_reward([task_id])

                self._update_task_item_state(task_id)

                @item.temp_btn_go.btn_common.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    jump_conf = task_utils.get_jump_conf(task_id)
                    exec_jump_to_ui_info(jump_conf)
                    self.close()
                    global_data.ui_mgr.close_ui('ActivityCenterMainUI')

        return

    def _update_tab_btn_redpoint(self, parent_task_id):
        btn_tab = self._btn_tab_dict.get(str(parent_task_id))
        if btn_tab and btn_tab.isValid():
            btn_tab.img_red.setVisible(task_utils.has_unreceived_reward(parent_task_id))

    def _update_prog_task_item(self, task_id):
        item = self._task_item_dict.get(str(task_id))
        if item and item.isValid():
            prog_reward_list = task_utils.get_prog_rewards(task_id)
            return prog_reward_list or None
        for reward_info in prog_reward_list:
            prog = reward_info[0]
            status = task_utils.get_prog_task_status_info(task_id, prog)
            if status == ITEM_UNRECEIVED or status == ITEM_UNGAIN:
                total_prog = prog
                reward_id = reward_info[1]
                break
            elif status == ITEM_RECEIVED:
                total_prog = prog
                reward_id = reward_info[1]

        item.lab_name.SetString(task_utils.get_task_name(task_id, {'prog': total_prog}))
        if global_data.player:
            task_prog = global_data.player.get_task_prog(task_id) if 1 else 0
            item.lab_num.SetString('%d/%d' % (task_prog, total_prog))
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            init_tempate_mall_i_item(item.temp_reward, reward_list[0][0], reward_list[0][1], show_tips=True)

            @item.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch):
                global_data.player and global_data.player.receive_task_prog_reward(task_id, prog)

    def _update_task_item_state(self, task_id):
        item = self._task_item_dict.get(str(task_id))
        if item and item.isValid():
            prog_reward_list = task_utils.get_prog_rewards(task_id)
            if prog_reward_list:
                for reward_info in prog_reward_list:
                    prog = reward_info[0]
                    status = task_utils.get_prog_task_status_info(task_id, prog)
                    if status == ITEM_UNRECEIVED or status == ITEM_UNGAIN:
                        break

            else:
                status = global_data.player.get_task_reward_status(task_id) if global_data.player else ITEM_RECEIVED
            item.temp_btn_get.setVisible(status == ITEM_UNRECEIVED)
            item.temp_btn_go.setVisible(status == ITEM_UNGAIN)
            item.nd_get.setVisible(status == ITEM_RECEIVED)

    def _on_receive_task_reward(self, task_id, *args):
        parent_task_id = task_utils.get_parent_task(task_id)
        if parent_task_id:
            self._update_tab_btn_redpoint(parent_task_id)
        self._update_task_item_state(task_id)
        self._update_prog_task_item(task_id)

    def _on_task_prog_changed(self, *args):
        children_task_id_list = self._get_children_task_id()
        if not children_task_id_list:
            self.close()
            return
        if self._children_task_id_list != children_task_id_list:
            self._children_task_id_list = children_task_id_list
            self.init_ui()

    def _init_lab_tips_time(self):
        children_task_list = task_utils.get_children_task(self._week_parent_task_id)
        for index, task_id in enumerate(children_task_list):
            if not task_utils.is_task_open(task_id):
                continue
            conf = task_utils.get_task_conf_by_id(task_id)
            self._remain_time = conf.get('end_time', get_server_time() + 1) - get_server_time()
            break

        if self._remain_time and self._remain_time > 0:
            if not self._timer:
                self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_lab_time, interval=1, mode=CLOCK)
            self._update_lab_time()
        else:
            self._lab_tips_time.SetString('')

    def _update_lab_time(self):
        self._remain_time = self._remain_time - 1
        if self._remain_time < 0:
            if self._timer:
                global_data.game_mgr.get_logic_timer().unregister(self._timer)
                self._timer = None
            self._init_lab_tips_time()
        self._lab_tips_time.SetString(get_simply_readable_time(self._remain_time))
        return

    def on_finalize_panel(self):
        super(ActivityTreasurePavilionTaskPanelUI, self).on_finalize_panel()
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return