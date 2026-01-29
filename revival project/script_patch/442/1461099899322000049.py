# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/GrowthTaskWidget.py
from __future__ import absolute_import
from six.moves import range
from .CommonTaskWidget import CommonTaskWidget
from logic.gutils import task_utils
from logic.gutils.template_utils import init_tempate_mall_i_item, init_common_reward_list
from math import ceil
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.system_unlock_utils import get_sys_unlock_growth_icon, get_sys_name_text_id, is_sys_unlocked, get_sys_jump_info, get_sys_unlock_growth_tip
from common.cfg import confmgr
import cc
TASK_ID_LEVEL_REWARD = '2000001'
TASK_ID_EXTRA_REWARD = '2000002'
LEVEL_BTN_UPDATE_RANGE = 5

class GrowthTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(GrowthTaskWidget, self).__init__(parent, panel, task_type, False)
        temp_content = getattr(self.parent.nd_cut, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('task/i_growth_task_new')
        self.panel.nd_cut.AddChild('growth_task', self.nd_content)
        self.nd_content.ResizeAndPosition()
        self.nd_content.SetPosition(*pos)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())
        self.lv_2_level_reward_id = task_utils.get_prog_rewards_in_dict(TASK_ID_LEVEL_REWARD)
        self.lv_2_extra_reward_id = task_utils.get_prog_rewards_in_dict(TASK_ID_EXTRA_REWARD)
        self.all_levels = task_utils.get_all_growth_levels(TASK_ID_LEVEL_REWARD)
        self.cur_level_ui_item = None
        self.cur_sel_level = None
        self.last_clicked_receive_btn_lv = None
        return

    def destroy(self):
        self.all_levels = None
        self.lv_2_level_reward_id = None
        self.lv_2_extra_reward_id = None
        self.cur_level_ui_item = None
        global_data.emgr.player_lv_update_event -= self.on_task_prog_change
        global_data.emgr.receive_task_prog_reward_succ_event -= self.on_receive_task_prog_reward_succ
        super(GrowthTaskWidget, self).destroy()
        return

    def init_event(self):
        super(GrowthTaskWidget, self).init_event()
        global_data.emgr.player_lv_update_event += self.on_task_prog_change
        global_data.emgr.receive_task_prog_reward_succ_event += self.on_receive_task_prog_reward_succ

    @staticmethod
    def check_red_point():
        all_levels = task_utils.get_all_growth_levels(TASK_ID_LEVEL_REWARD)
        for lv in all_levels:
            if task_utils.can_receive_growth_prog_reward(TASK_ID_LEVEL_REWARD, lv) or task_utils.can_receive_growth_prog_reward(TASK_ID_EXTRA_REWARD, lv):
                return True

        return False

    def on_receive_task_prog_reward_succ(self, task_id, prog):
        self.update_unreceive_tip(prog)
        self.update_get_all_btn_visible()
        if prog == self.cur_sel_level:
            self.init_reward_widget(self.cur_sel_level)

    def update_unreceive_tip(self, lv=None):
        if lv is not None:
            level_to_up = lv
        else:
            level_to_up = self.last_clicked_receive_btn_lv
        if not level_to_up:
            return
        else:
            level_ui = self.get_lv_ui_by_lv(level_to_up)
            if not level_ui or not level_ui.isValid():
                return
            show_tip = task_utils.can_receive_growth_prog_reward(TASK_ID_LEVEL_REWARD, level_to_up) or task_utils.can_receive_growth_prog_reward(TASK_ID_EXTRA_REWARD, level_to_up)
            level_ui.img_not_receive.setVisible(show_tip)
            return

    def init_widget(self, need_hide=True):
        super(GrowthTaskWidget, self).init_widget(need_hide)
        self.init_lv_list_widget()
        self.init_reward_widget()
        self.init_lv_locate_widget()
        self.init_nd_touch()
        self.init_get_all_btn()

    def on_task_prog_change(self, *args):
        cur_lv = global_data.player.get_lv()
        for lv in range(cur_lv - LEVEL_BTN_UPDATE_RANGE, cur_lv + LEVEL_BTN_UPDATE_RANGE + 1):
            if lv not in self.all_levels:
                continue
            self.update_lv_ui(lv, self.get_lv_ui_by_lv(lv))

        self.nd_content.list_temp_btn.scroll_Load()
        self.nd_content.list_temp_btn._refreshItemPos()
        self.init_reward_widget()
        self.init_lv_locate_widget()
        self.update_get_all_btn_visible()

    def init_lv_list_widget(self):
        lv_cnt = len(self.all_levels)
        temp_node_cnt = ceil(lv_cnt / 2.0)
        temp_node_list = self.nd_content.list_temp_btn

        @temp_node_list.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.update_temp_node(idx, ui_item)

        temp_node_list.SetVisibleRange(5, 5)
        temp_node_list.SetInitCount(int(temp_node_cnt))
        temp_node_list.scroll_Load()
        temp_node_list._refreshItemPos()

    def update_temp_node(self, idx, temp_node):
        level_1 = self.all_levels[idx * 2]
        self.update_lv_ui(level_1, temp_node.temp_task_1)
        if idx * 2 + 1 >= len(self.all_levels):
            temp_node.temp_task_2.setVisible(False)
            return
        level_2 = self.all_levels[idx * 2 + 1]
        self.update_lv_ui(level_2, temp_node.temp_task_2)

    def update_lv_ui(self, lv, level_ui):
        if not level_ui:
            return
        if lv not in self.all_levels:
            return
        cur_lv = global_data.player.get_lv()
        level_ui.nd_default.setVisible(cur_lv > lv)
        level_ui.nd_level_now.setVisible(cur_lv == lv)
        level_ui.nd_ashing.setVisible(cur_lv < lv)
        level_ui.nd_default.img_default.lab_default.SetString(str(lv))
        level_ui.nd_level_now.img_level_now.lab_level_now.SetString(str(lv))
        level_ui.nd_ashing.img_ashing.lab_ashing.SetString(str(lv))
        unlock_systems = task_utils.get_growth_unlock_systems_by_lv(lv)
        self.init_unlock_sys_list_bubble(lv, level_ui, unlock_systems)
        self.init_extra_reward_bubble(lv, level_ui.img_tab_top)
        if cur_lv >= lv:
            show_tip = task_utils.can_receive_growth_prog_reward(TASK_ID_LEVEL_REWARD, lv) or task_utils.can_receive_growth_prog_reward(TASK_ID_EXTRA_REWARD, lv)
            level_ui.img_not_receive.setVisible(show_tip)
        else:
            level_ui.img_not_receive.setVisible(False)
        level_ui.img_level_choose.setVisible(False)

        @level_ui.btn_task.unique_callback()
        def OnClick(layer, touch):
            if self.cur_level_ui_item:
                self.cur_level_ui_item.img_level_choose.setVisible(False)
            level_ui.img_level_choose.setVisible(True)
            self.cur_level_ui_item = level_ui
            self.cur_sel_level = lv
            self.init_reward_widget(lv)

        if lv == self.all_levels[-1]:
            level_ui.img_line.setVisible(False)

    def get_temp_node_by_lv(self, lv):
        temp_node_index = int(ceil(lv / 2.0) - 1)
        return self.nd_content.list_temp_btn.GetItem(temp_node_index)

    def get_lv_ui_by_lv(self, lv):
        temp_node = self.get_temp_node_by_lv(lv)
        if not temp_node:
            return None
        else:
            lv_ui_index = lv % 2
            if lv_ui_index == 1:
                return temp_node.temp_task_1
            return temp_node.temp_task_2

    def init_unlock_sys_list_bubble(self, lv, level_ui, unlock_systems):
        if not unlock_systems:
            return
        level_ui.list_temp_1.DeleteAllSubItem()
        level_ui.list_temp_1.SetInitCount(len(unlock_systems))
        all_items_1 = level_ui.list_temp_1.GetAllItem()
        for idx, sys_type in enumerate(unlock_systems):
            sys_icon = get_sys_unlock_growth_icon(sys_type)
            sys_text_id = get_sys_name_text_id(sys_type)
            jump_info = get_sys_jump_info(sys_type)
            all_items_1[idx].img_icon.SetDisplayFrameByPath('', sys_icon)
            all_items_1[idx].lab_icon_name.SetString(get_text_by_id(sys_text_id))
            btn_look = all_items_1[idx].btn_look

            @btn_look.unique_callback()
            def OnClick(btn, touch, info=jump_info):
                if not is_sys_unlocked(sys_type):
                    unlock_text_id = get_sys_unlock_growth_tip(sys_type)
                    global_data.game_mgr.show_tip(get_text_by_id(unlock_text_id).format(lv), True)
                    return
                from logic.gutils import jump_to_ui_utils
                func_name = info.get('func')
                args = info.get('args', [])
                kargs = info.get('kargs', {})
                if func_name:
                    func = getattr(jump_to_ui_utils, func_name)
                    func and func(*args, **kargs)

        level_ui.list_temp_1.setVisible(True)
        level_ui.list_temp_2.setVisible(False)

    def init_extra_reward_bubble(self, lv, extra_reward_ui):
        extra_reward_ui and extra_reward_ui.setVisible(False)
        return
        extra_reward_id = self.lv_2_extra_reward_id.get(lv)
        if extra_reward_id and extra_reward_ui:
            extra_reward_ui.setVisible(True)
            init_common_reward_list(extra_reward_ui.list_temp_rewards_top, extra_reward_id)

    def init_reward_widget(self, lv=None):
        if not lv:
            lv = global_data.player.get_lv()
        if lv > self.all_levels[-1]:
            lv = self.all_levels[-1]
        level_reward_id = self.lv_2_level_reward_id.get(lv, -1)
        level_reward_list = confmgr.get('common_reward_data', str(level_reward_id), 'reward_list', default=[])
        level_reward_ui = self.nd_content.temp_rewads
        if level_reward_list:
            first_item_info = level_reward_list[0]
            item_no, item_num = first_item_info[0], first_item_info[1]
            init_tempate_mall_i_item(level_reward_ui, item_no, item_num=item_num, show_tips=True)
            can_receive = self.can_receive_lv_reward(TASK_ID_LEVEL_REWARD, lv)
            btn_receive = self.nd_content.temp_btn_left.btn_common
            btn_receive.SetEnable(can_receive)
            if global_data.player.has_receive_prog_reward(TASK_ID_LEVEL_REWARD, lv):
                btn_receive.SetText(get_text_by_id(80866))
            else:
                btn_receive.SetText(get_text_by_id(80930))
            self.nd_content.lab_rewards_tip_left.SetString(get_text_by_id(82067).format(lv))

            @btn_receive.unique_callback()
            def OnClick(btn, touch):
                if global_data.player.receive_task_prog_reward(TASK_ID_LEVEL_REWARD, lv):
                    btn.SetText(80866)
                    btn.SetEnable(False)
                    self.last_clicked_receive_btn_lv = lv

        extra_reward_id = self.lv_2_extra_reward_id.get(lv)
        extra_reward_ui = self.nd_content.list_temp_rewards_down
        if extra_reward_id:
            extra_reward_ui.setVisible(True)
            self.nd_content.temp_btn_right.setVisible(True)
            self.nd_content.lab_tip.setVisible(False)
            self.nd_content.lab_rewards.setVisible(True)
            init_common_reward_list(extra_reward_ui, extra_reward_id)
            extra_reward_ui.temp_btn_right.InitConfPosition()
            can_receive = self.can_receive_lv_reward(TASK_ID_EXTRA_REWARD, lv)
            btn_receive = self.nd_content.temp_btn_right.btn_common
            btn_receive.SetEnable(can_receive)
            if global_data.player.has_receive_prog_reward(TASK_ID_EXTRA_REWARD, lv):
                btn_receive.SetText(get_text_by_id(80866))
            else:
                btn_receive.SetText(get_text_by_id(80930))

            @btn_receive.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_task_prog_reward(TASK_ID_EXTRA_REWARD, lv)
                btn.SetText(80866)
                btn.SetEnable(False)
                self.last_clicked_receive_btn_lv = lv

        else:
            extra_reward_ui.setVisible(False)
            self.nd_content.temp_btn_right.setVisible(False)
            self.nd_content.lab_tip.setVisible(False)
            self.nd_content.lab_rewards.setVisible(False)

    def init_lv_locate_widget(self):

        @self.nd_content.btn_return.unique_callback()
        def OnClick(*args):
            self.on_click_btn_back()

        self.on_click_btn_back()

    def on_click_btn_back(self):
        cur_lv = global_data.player.get_lv()
        if cur_lv > self.all_levels[-1]:
            cur_lv = self.all_levels[-1]
        temp_node_idx = int(ceil(cur_lv / 2.0) - 1)
        self.nd_content.list_temp_btn.LocatePosByItem(temp_node_idx)
        if self.cur_level_ui_item:
            self.cur_level_ui_item.img_level_choose.setVisible(False)
        self.cur_level_ui_item = self.get_lv_ui_by_lv(cur_lv)
        self.cur_sel_level = cur_lv
        self.init_reward_widget(cur_lv)
        self.nd_content.list_temp_btn.scroll_Load()
        self.nd_content.list_temp_btn._refreshItemPos()

    def init_nd_touch(self):
        self.nd_content.nd_touch.setVisible(False)

    def init_get_all_btn(self):
        self.update_get_all_btn_visible()

        @self.nd_content.temp_btn_get_all.btn_common_big.unique_callback()
        def OnClick(*args):
            self.on_click_get_all_btn()

    def update_get_all_btn_visible(self):
        self.nd_content.temp_btn_get_all.setVisible(self.check_red_point())

    def on_click_get_all_btn(self):
        global_data.player.receive_all_task_prog_reward(TASK_ID_LEVEL_REWARD)
        global_data.player.receive_all_task_prog_reward(TASK_ID_EXTRA_REWARD)

    @staticmethod
    def can_receive_lv_reward(task_id, lv):
        return global_data.player.is_prog_reward_receivable(task_id, lv) and not global_data.player.has_receive_prog_reward(task_id, lv)

    def recover_sys_unlock_bubble(self, lv, lv_ui, recover=True):
        if lv_ui and task_utils.get_growth_unlock_systems_by_lv(lv):
            lv_ui.list_temp_1.setVisible(recover)
            lv_ui.list_temp_2.setVisible(not recover)