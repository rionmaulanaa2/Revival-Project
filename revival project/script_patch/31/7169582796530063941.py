# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVECareerWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.item_utils import get_all_lobby_item_by_item_type
from logic.gutils.pve_utils import reset_model_and_cam_pos
from logic.gutils import task_utils, career_utils
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from .PVEAllCareerWidget import PVEAllCareerWidget
from .PVEChapterCareerWidget import PVEChapterCareerWidget
from logic.gcommon import time_utility
from logic.gcommon.common_const.pve_const import PVE_CAREER_CACHE_KEY
import six_ex

class PVECareerWidgetUI(BasePanel):
    DELAY_CLOSE_TAG = 20240105
    PANEL_CONFIG_NAME = 'catalogue/catalogue_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, default_tab_index=0, default_type=0, *args, **kwargs):
        super(PVECareerWidgetUI, self).on_init_panel()
        self.init_params(default_tab_index, default_type)
        self.init_ui()
        self.init_ui_events()
        self.process_events(True)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._update_tab_red_point,
           'receive_task_prog_reward_succ_event': self._update_tab_red_point
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('in')
        self.hide_main_ui()

    def init_params(self, default_tab_index, default_type):
        self._default_tab_index = default_tab_index
        self._default_type = default_type
        self._disappearing = False
        self._career_bar_wrapper = None
        self._tab_widgets = {}
        self._tab_list = [{'index': 0,'text': 709255,'ui_cls': PVEAllCareerWidget,'template_path': 'pve/ac/i_ac_pve_main_career','check_redpoint_func': PVECareerWidgetUI.check_all_career_red_point}, {'index': 1,'text': 709256,'ui_cls': PVEChapterCareerWidget,'template_path': 'pve/ac/i_ac_pve_main_reward','check_redpoint_func': PVECareerWidgetUI.check_chapter_career_red_point}]
        self._tab_btn_dict = {}
        return

    def init_ui(self):
        tab_list = self.panel.tab_list
        tab_list.lab_title.setVisible(False)
        lab_title_pve = tab_list.lab_title_pve
        lab_title_pve.setVisible(True)
        lab_title_pve.setString(get_text_by_id(709254))
        self._init_career_bar()
        self._update_tab_red_point()
        self._write_local_data()

    def init_ui_events(self):

        @self.panel.top.btn_back.btn_back.unique_callback()
        def OnClick(btn, touch, *args):
            self.play_disappear_anim()

        @self.panel.tab_list.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(709254, 635417)

    def on_resolution_changed(self):
        super(PVECareerWidgetUI, self).on_resolution_changed()

    def _init_career_bar(self):
        tab_list = self.panel.tab_list.nd_tab_list.tab_list

        def _init_career_btn(node, data):
            node.btn.SetText(get_text_by_id(data.get('text', '')))
            self._tab_btn_dict[data['index']] = node

        def _career_btn_click_cb(ui_item, data, index):
            if not self._tab_widgets.get(index):
                template_path = data.get('template_path')
                ui_cls = data.get('ui_cls')
                template_node = global_data.uisystem.load_template_create(template_path, self.panel.temp_content)
                template_node.SetPosition('50%', '50%')
                widget_wrapper = ui_cls(template_node, self._default_type)
                self._tab_widgets[index] = widget_wrapper
            for _index in self._tab_widgets:
                widget = self._tab_widgets[_index]
                if index == _index:
                    widget.show()
                else:
                    widget.hide()

        self._career_bar_wrapper = WindowTopSingleSelectListHelper(btn_tab_name='btn')
        self._career_bar_wrapper.set_up_list(tab_list, self._tab_list, _init_career_btn, _career_btn_click_cb)
        self._career_bar_wrapper.set_node_click(tab_list.GetItem(int(self._default_tab_index)))

    def _update_tab_red_point(self, *args):
        for index, btn_tab in six_ex.items(self._tab_btn_dict):
            redpoint_check_func = self._tab_list[index].get('check_redpoint_func')
            if redpoint_check_func:
                btn_tab.img_red.setVisible(redpoint_check_func())

    def _write_local_data(self):
        time_str = time_utility.get_date_str(format='%Y%m%d', timestamp=time_utility.get_server_time())
        global_data.achi_mgr.get_general_archive_data().set_field(PVE_CAREER_CACHE_KEY, time_str)
        global_data.emgr.refresh_task_main_redpoint.emit()

    @staticmethod
    def check_red_point():
        if PVECareerWidgetUI.check_all_career_red_point() or PVECareerWidgetUI.check_chapter_career_red_point() or PVECareerWidgetUI.check_daily_red_point():
            return True
        return False

    @staticmethod
    def check_all_career_red_point():
        from logic.gutils import task_utils
        from logic.gutils.pve_lobby_utils import get_pve_all_career_parent_task_list, get_pve_career_task_state
        from logic.gcommon.item.item_const import ITEM_UNRECEIVED
        parent_task = get_pve_all_career_parent_task_list()
        children_task_list = task_utils.get_children_task(parent_task)
        try:
            for task_id in children_task_list:
                task_conf = task_utils.get_task_conf_by_id(task_id)
                cnt = career_utils.get_badge_lv_count(task_id) or 1
                for i in range(cnt):
                    task_level = i + 1
                    status = get_pve_career_task_state(task_id, task_level)
                    if status == ITEM_UNRECEIVED:
                        return True

        except Exception as e:
            import exception_hook
            exception_hook.traceback_uploader()

        return False

    @staticmethod
    def check_chapter_career_red_point():
        from logic.gutils import task_utils
        from logic.gutils.pve_lobby_utils import get_pve_chapter_career_parent_task_list, get_pve_career_task_state
        from logic.gcommon.item.item_const import ITEM_UNRECEIVED
        parent_task_list = get_pve_chapter_career_parent_task_list()
        for index, parent_task in enumerate(parent_task_list):
            prog_reward_list = task_utils.get_prog_rewards(parent_task)
            for reward_info in prog_reward_list:
                prog = reward_info[0]
                status = task_utils.get_prog_task_status_info(parent_task, prog)
                if status == ITEM_UNRECEIVED:
                    return True

            children_task_list = task_utils.get_children_task(parent_task)
            for task_id in children_task_list:
                task_conf = task_utils.get_task_conf_by_id(task_id)
                cnt = career_utils.get_badge_lv_count(task_id) or 1
                for i in range(cnt):
                    task_level = i + 1
                    status = get_pve_career_task_state(task_id, task_level)
                    if status == ITEM_UNRECEIVED:
                        return True

        return False

    @staticmethod
    def check_daily_red_point():
        return False

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()
            if global_data.player:
                global_data.emgr.on_pve_mecha_changed.emit(global_data.player.get_pve_select_mecha_id())

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVECareerWidgetUI, self).on_finalize_panel()
        for index, widget in six_ex.items(self._tab_widgets):
            widget.destroy()
            widget = None

        global_data.emgr.set_reward_show_blocking_item_no_event.emit([])
        self.show_main_ui()
        return