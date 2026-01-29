# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEChapterCareerWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, FrameLoaderTemplate, init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_rare_degree_pic_by_rare_degree, get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_mecha_id_list, get_effect_desc_text
from .PVECommonCareerWidget import PVECommonCareerWidget, PVECareerWidget
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_RECEIVED, ITEM_UNRECEIVED
from logic.gutils import career_utils
from logic.gutils import task_utils
from logic.gutils.pve_lobby_utils import get_pve_chapter_career_parent_task_list, get_pve_career_task_state
from common.cfg import confmgr
import six_ex

class PVEChapterCareerWidget(PVECommonCareerWidget):

    def init_params(self):
        super(PVEChapterCareerWidget, self).init_params()
        self._chapter_task_list = []
        self._degree_task_list = {}
        self._degree_task_list[0] = []
        self._degree_type_task_list = {}
        self._parent_task_list = get_pve_chapter_career_parent_task_list()
        self._all_task_id_list = set([])
        for index, parent_task in enumerate(self._parent_task_list):
            chapter = index + 1
            chapter_task_info_list = []
            children_task_list = task_utils.get_children_task(parent_task)
            for task_id in children_task_list:
                self._all_task_id_list.add(task_id)
                task_conf = task_utils.get_task_conf_by_id(task_id)
                cnt = career_utils.get_badge_lv_count(task_id) or 1
                for i in range(cnt):
                    lv = i + 1
                    degree_list = task_conf.get('degree')
                    if degree_list:
                        degree = degree_list[i]
                        if not self._degree_type_task_list.get(chapter):
                            self._degree_type_task_list[chapter] = {}
                            self._degree_type_task_list[chapter][0] = []
                        if not self._degree_type_task_list[chapter].get(degree):
                            self._degree_type_task_list[chapter][degree] = []
                        self._degree_type_task_list[chapter][degree].append((task_id, lv))
                        if not self._degree_task_list.get(degree):
                            self._degree_task_list[degree] = []
                        self._degree_task_list[degree].append((task_id, lv))
                    self._degree_type_task_list[chapter][0].append((task_id, lv))
                    chapter_task_info_list.append((task_id, lv))

            self._chapter_task_list.append(chapter_task_info_list)

        self._frame_loader_template = None
        self._tab_widgets = {}
        self._tab_btn_dict = {}
        self._cur_tab_widget = None
        self._cur_select_type = None
        self._chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', default={})
        self._icon_prog_dict = {20: (
              self._panel.icon_20.lab_prog, self._panel.temp_reward_20),
           40: (
              self._panel.icon_40.lab_prog, self._panel.temp_reward_40),
           70: (
              self._panel.icon_70.lab_prog, self._panel.temp_reward_70),
           100: (
               self._panel.icon_100.lab_prog, self._panel.temp_reward_100)
           }
        return

    def init_ui(self):
        super(PVEChapterCareerWidget, self).init_ui()
        self._update_reward_item()
        self._update_bar_prog()
        self._update_btn_redpoint()

    def init_ui_event(self):
        super(PVEChapterCareerWidget, self).init_ui_event()

        @self._panel.temp_get_all.btn_common_big.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            parent_task_list = get_pve_chapter_career_parent_task_list()
            for parent_task in parent_task_list:
                global_data.player.receive_all_task_prog_reward(parent_task)

            global_data.player.receive_tasks_reward(list(self._all_task_id_list))

    def _init_career_bar(self):
        list_tab = self._panel.list_tab

        def _init_career_btn(node, data):
            index = self._chapter_task_list.index(data)
            chapter = index + 1
            chapter_conf = self._chapter_conf.get(str(chapter), {})
            chapter_str = get_text_by_id(chapter_conf.get('title_text', ''))
            node.btn_tab.SetText(chapter_str)
            self._tab_btn_dict[chapter] = node

        def _career_btn_click_cb(ui_item, data, index):
            if not self._tab_widgets.get(index):
                template_node = global_data.uisystem.load_template_create('pve/ac/i_ac_pve_data_list', self._panel.nd_list)
                widget_wrapper = PVECareerWidget(template_node, data)
                self._tab_widgets[index] = widget_wrapper
            for _index in self._tab_widgets:
                widget = self._tab_widgets[_index]
                if index == _index:
                    self._cur_tab_widget = widget
                    self._cur_select_type = index + 1
                    widget.show()
                else:
                    widget.hide()

            self._refresh_all_choose()
            self._update_list_prog()
            self._update_reward_item()
            self._update_bar_prog()

        self._career_bar_wrapper = WindowTopSingleSelectListHelper()
        self._career_bar_wrapper.set_up_list(list_tab, self._chapter_task_list, _init_career_btn, _career_btn_click_cb)
        self._career_bar_wrapper.set_node_click(list_tab.GetItem(int(self._default_type)))

    def _update_reward_item(self):
        parent_task_id = self._parent_task_list[self._cur_select_type - 1]
        parent_reward_list = task_utils.get_prog_rewards(parent_task_id)
        for index, icon_prog in enumerate(self._icon_prog_dict):
            prog = parent_reward_list[index][0]
            lab_prog = self._icon_prog_dict[icon_prog][0]
            lab_prog.setString(str(prog))
            reward_id = parent_reward_list[index][1]
            reward_item = self._icon_prog_dict[icon_prog][1]
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no = reward_list[0][0]
            num = reward_list[0][1]
            init_tempate_reward(reward_item, item_no, num, show_tips=True)

            @reward_item.btn_choose.unique_callback()
            def OnClick(btn, touch, item_no=item_no, num=num, prog=prog):
                if not global_data.player:
                    return
                else:
                    cur_prog = global_data.player.get_task_prog(parent_task_id)
                    if not global_data.player.has_receive_prog_reward(parent_task_id, prog) and cur_prog >= prog:
                        global_data.player.receive_task_prog_reward(parent_task_id, prog)
                    else:
                        x, y = btn.GetPosition()
                        w, h = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, item_num=num)
                    return

    def _update_bar_prog(self):
        parent_task_id = self._parent_task_list[self._cur_select_type - 1]
        _, cur_prog, max_prog, _ = task_utils.get_task_status_info(parent_task_id)
        self._panel.lab_score.setString(str(cur_prog))
        self._panel.prog.SetPercentage(float(cur_prog) / max_prog * 100)
        parent_reward_list = task_utils.get_prog_rewards(parent_task_id)
        for index, icon_prog in enumerate(self._icon_prog_dict):
            prog = parent_reward_list[index][0]
            lab_prog = self._icon_prog_dict[icon_prog][0]
            reward_item = self._icon_prog_dict[icon_prog][1]
            if cur_prog >= prog:
                lab_prog.SetColor(60159)
            else:
                lab_prog.SetColor('#SW')
            if global_data.player.has_receive_prog_reward(parent_task_id, prog):
                reward_item.nd_get_tips.setVisible(False)
                reward_item.StopAnimation('get_tips')
                reward_item.btn_choose.SetSelect(False)
                reward_item.nd_get.setVisible(True)
            else:
                reward_item.nd_get.setVisible(False)
                if cur_prog >= prog:
                    reward_item.nd_get_tips.setVisible(True)
                    reward_item.PlayAnimation('get_tips')
                else:
                    reward_item.nd_get_tips.setVisible(False)
                    reward_item.StopAnimation('get_tips')

    def _on_task_reward_update(self, *args):
        super(PVEChapterCareerWidget, self)._on_task_reward_update()
        self._update_bar_prog()
        self._update_btn_redpoint()

    def _update_btn_redpoint(self, *args):
        all_can_receive_count = 0
        for chapter, btn_tab in six_ex.items(self._tab_btn_dict):
            can_receive_count = 0
            parent_task = self._parent_task_list[chapter - 1]
            prog_reward_list = task_utils.get_prog_rewards(parent_task)
            for reward_info in prog_reward_list:
                prog = reward_info[0]
                status = task_utils.get_prog_task_status_info(parent_task, prog)
                if status == ITEM_UNRECEIVED:
                    can_receive_count += 1

            for task_info in self._degree_type_task_list[chapter][0]:
                task_id = task_info[0]
                task_level = task_info[1]
                status = get_pve_career_task_state(task_id, task_level)
                if status == ITEM_UNRECEIVED:
                    can_receive_count += 1

            btn_tab.temp_red.setVisible(can_receive_count > 0)
            all_can_receive_count += can_receive_count

        if all_can_receive_count > 1:
            self._panel.temp_get_all.setVisible(True)
            self._panel.pnl_content.SetContentSize(1282, 'i248')
            self._panel.pnl_content.ChildResizeAndPosition()
        else:
            self._panel.temp_get_all.setVisible(False)
            self._panel.pnl_content.SetContentSize(1282, 'i200')
            self._panel.pnl_content.ChildResizeAndPosition()
        global_data.test11 = self._panel.pnl_content