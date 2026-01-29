# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESuggestUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM, UI_TYPE_MESSAGE
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, init_tempate_reward
from logic.gutils.task_utils import get_task_reward
from logic.gcommon.common_utils.local_text import get_text_by_id
from .PVESuggestWidget import PVESuggestWidget
from common.cfg import confmgr

class PVESuggestUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/bg_home_system_pve'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'nd_content.btn_close.OnClick': '_on_click_back'
       }

    def on_init_panel(self):
        super(PVESuggestUI, self).on_init_panel()
        self.hide_main_ui()
        self._init_params()
        self._init_ui()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._update_reward_state,
           'task_prog_changed': self._update_reward_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_params(self):
        self.tab_widgets = {}
        self._task_id = None
        return

    def _init_ui(self):
        self._init_sheet_bar()

    def _init_sheet_bar(self):
        period_id = global_data.player and global_data.player.get_pve_suggest_is_open()
        if not period_id:
            self.close()
        sheet_id_list = confmgr.get('pve_suggest_conf', 'SuggestPeriodConf', 'Content', period_id, 'sheet_id_list')
        sheet_conf = confmgr.get('pve_suggest_conf', 'SuggestSheetConf', 'Content')
        self.tab_list = []
        for sheet_id in sheet_id_list:
            conf = sheet_conf.get(sheet_id)
            sheet_info = {'sheet_id': sheet_id,'name_id': conf.get('sheet_name', ''),'task_id': conf.get('task_id', '')}
            self.tab_list.append(sheet_info)

        def init_sheet_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('name_id', '')))

        def sheet_btn_click_cb(ui_item, data, idx):
            self._set_reward_item(data)
            self._set_list_item(data)

        list_tab = self.panel.list_tab
        self._sheet_bar_wrapper = WindowTopSingleSelectListHelper()
        self._sheet_bar_wrapper.set_up_list(list_tab, self.tab_list, init_sheet_btn, sheet_btn_click_cb)
        self._sheet_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _set_reward_item(self, data):
        self._task_id = str(data.get('task_id'))
        reward_id = get_task_reward(self._task_id)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        item_no = reward_list[0][0]
        num = reward_list[0][1]
        temp_reward = self.panel.temp_reward
        init_tempate_reward(temp_reward, item_no, num)
        self._update_reward_state()

        @temp_reward.nd_item.btn_choose.unique_callback()
        def OnClick(btn, touch):
            if global_data.player.is_task_finished(self._task_id) and not global_data.player.has_receive_reward(self._task_id):
                global_data.player.receive_tasks_reward([self._task_id])
            else:
                x, y = btn.GetPosition()
                w, _ = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
            return

    def _update_reward_state(self, *args):
        nd_item = self.panel.temp_reward.nd_item
        if global_data.player.is_task_finished(self._task_id):
            if global_data.player.has_receive_reward(self._task_id):
                nd_item.nd_get.setVisible(True)
                nd_item.nd_get_tips.setVisible(False)
            else:
                nd_item.nd_get.setVisible(False)
                nd_item.nd_get_tips.setVisible(True)
        else:
            nd_item.nd_get.setVisible(False)
            nd_item.nd_get_tips.setVisible(False)

    def _set_list_item(self, data):
        sheet_id = data.get('sheet_id')
        if sheet_id in self.tab_widgets:
            for index in self.tab_widgets:
                widget = self.tab_widgets[index]
                if sheet_id == index:
                    widget.show()
                else:
                    widget.hide()

        else:
            _nd = global_data.uisystem.load_template_create('home_system/i_home_system_pve_list', self.panel.nd_list)
            _nd.SetPosition('50%', '50%')
            self.tab_widgets[sheet_id] = self._init_opinion_template(_nd, sheet_id)
            for index in self.tab_widgets:
                cur_widget = self.tab_widgets[index]
                if sheet_id != index:
                    cur_widget.hide()

    def _init_opinion_template(self, nd, sheet_id):
        return PVESuggestWidget(nd, sheet_id)

    def _on_click_back(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.process_event(False)
        self.show_main_ui()
        self._task_id = None
        for widget in self.tab_widgets.values():
            widget.destroy()

        return