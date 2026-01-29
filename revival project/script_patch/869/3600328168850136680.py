# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEAllCareerWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, FrameLoaderTemplate
from logic.gutils.item_utils import get_lobby_item_rare_degree_pic_by_rare_degree, get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_mecha_id_list, get_effect_desc_text
from .PVECommonCareerWidget import PVECommonCareerWidget, PVECareerWidget
from logic.gcommon.item.item_const import ITEM_UNRECEIVED
from logic.gutils import career_utils
from logic.gutils import task_utils
from logic.gutils.pve_lobby_utils import get_pve_all_career_parent_task_list, get_pve_career_task_state
from common.cfg import confmgr
import six_ex

class PVEAllCareerWidget(PVECommonCareerWidget):

    def init_params(self):
        super(PVEAllCareerWidget, self).init_params()
        self._degree_task_list = {}
        self._degree_task_list[0] = []
        self._type_task_list = {}
        self._type_task_id_list = []
        self._degree_type_task_list = {}
        parent_task = get_pve_all_career_parent_task_list()
        children_task_list = task_utils.get_children_task(parent_task)
        self._all_task_id_list = set([])
        for task_id in children_task_list:
            self._all_task_id_list.add(task_id)
            task_conf = task_utils.get_task_conf_by_id(task_id)
            cnt = career_utils.get_badge_lv_count(task_id) or 1
            for i in range(cnt):
                lv = i + 1
                pve_career_type = task_conf.get('pve_career_type')
                if pve_career_type:
                    if not self._type_task_list.get(pve_career_type):
                        self._type_task_list[pve_career_type] = []
                        self._type_task_id_list.append(pve_career_type)
                    self._type_task_list[pve_career_type].append((task_id, lv))
                degree_list = task_conf.get('degree')
                if degree_list:
                    degree = degree_list[i]
                    if not self._degree_type_task_list.get(pve_career_type):
                        self._degree_type_task_list[pve_career_type] = {}
                        self._degree_type_task_list[pve_career_type][0] = []
                    if not self._degree_type_task_list[pve_career_type].get(degree):
                        self._degree_type_task_list[pve_career_type][degree] = []
                    self._degree_type_task_list[pve_career_type][degree].append((task_id, lv))
                    if not self._degree_task_list.get(degree):
                        self._degree_task_list[degree] = []
                    self._degree_task_list[degree].append((task_id, lv))
                self._degree_type_task_list[pve_career_type][0].append((task_id, lv))

        self._frame_loader_template = None
        self._tab_widgets = {}
        self._tab_btn_dict = {}
        self._cur_tab_widget = None
        self._cur_select_type = None
        return

    def init_ui(self):
        super(PVEAllCareerWidget, self).init_ui()
        self._update_btn_redpoint()

    def init_ui_event(self):
        super(PVEAllCareerWidget, self).init_ui_event()

        @self._panel.temp_get_all.btn_common_big.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            print list(self._all_task_id_list)
            global_data.player.receive_tasks_reward(list(self._all_task_id_list))

    def _init_career_bar(self):
        list_tab = self._panel.list_tab

        def _init_career_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data))
            self._tab_btn_dict[data] = node

        def _career_btn_click_cb(ui_item, data, index):
            if not self._tab_widgets.get(index):
                template_node = global_data.uisystem.load_template_create('pve/ac/i_ac_pve_data_list', self._panel.nd_list)
                widget_wrapper = PVECareerWidget(template_node, self._type_task_list[data])
                self._tab_widgets[index] = widget_wrapper
            for _index in self._tab_widgets:
                widget = self._tab_widgets[_index]
                if index == _index:
                    self._cur_tab_widget = widget
                    self._cur_select_type = self._type_task_id_list[index]
                    widget.show()
                else:
                    widget.hide()

            self._refresh_all_choose()
            self._update_list_prog()

        self._career_bar_wrapper = WindowTopSingleSelectListHelper()
        self._career_bar_wrapper.set_up_list(list_tab, self._type_task_id_list, _init_career_btn, _career_btn_click_cb)
        self._career_bar_wrapper.set_node_click(list_tab.GetItem(int(self._default_type)))

    def _on_task_reward_update(self, *args):
        super(PVEAllCareerWidget, self)._on_task_reward_update()
        self._update_btn_redpoint()

    def _update_btn_redpoint(self, *args):
        all_can_receive_count = 0
        for pve_career_type, btn_tab in six_ex.items(self._tab_btn_dict):
            can_receive_count = 0
            for task_info in self._type_task_list[pve_career_type]:
                task_id = task_info[0]
                task_level = task_info[1]
                status = get_pve_career_task_state(task_id, task_level)
                if status == ITEM_UNRECEIVED:
                    can_receive_count += 1

            btn_tab.temp_red.setVisible(can_receive_count > 0)
            all_can_receive_count += can_receive_count

        pnl_content = self._panel.pnl_content
        if all_can_receive_count > 1:
            self._panel.temp_get_all.setVisible(True)
            pnl_content.SetContentSize(1282, 'i248')
            pnl_content.ChildResizeAndPosition()
        else:
            self._panel.temp_get_all.setVisible(False)
            pnl_content.SetContentSize(1282, 'i200')
            pnl_content.ChildResizeAndPosition()