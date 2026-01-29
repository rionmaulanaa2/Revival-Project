# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPageTabWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.gutils import activity_utils
from common.cfg import confmgr
from common.platform.dctool import interface
from .ActivitySubPage import ActivitySubPage
from logic.gcommon.common_const.activity_const import ACTIVITY_REDDOT_CLICK, ACTIVITY_ANNIVERSARY_GOLD
from logic.gcommon.common_const.activity_const import WIDGET_ALPHA_PLAN, WIDGET_SPRING_REWARD
from logic.gutils.nile_utils import is_nile_activity

class ActivityPageTabWidget(object):

    def __init__(self, parent, widget_type, select_cb=None, default_font_size=24, tab_init_cb=None):
        self.parent = parent
        self.panel = parent.panel
        self._request_activities = False
        self.widget_type = widget_type
        self._select_widget_cb = select_cb
        self._tab_init_cb = tab_init_cb
        self._jump_ui_activity_type = None
        self._default_font_size = default_font_size
        self.init_parameters()
        self.init_event()
        self.init_page_tab()
        return

    def on_finalize_panel(self):
        self._select_widget_cb = None
        self._tab_init_cb = None
        self.process_event(False)
        self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
        self._cur_view_sub_page_widget and self._cur_view_sub_page_widget.on_finalize_panel()
        self._cur_sub_page_name = None
        self._cur_view_page_widget = None
        self._cur_activity_index = 0
        return

    def on_resolution_changed(self):
        if self._cur_view_page_widget:
            self._cur_view_page_widget.on_resolution_changed()

    def init_parameters(self):
        self._cur_font_sizes = None
        self._cur_activity_index = 0
        self._default_activity_type = ''
        self._cur_view_page_widget = None
        self._cur_view_sub_page_widget = None
        self._cur_sub_page_name = None
        self._cur_selected_activity_type = ''
        self._activity_list = []
        self._selected_widget = None
        self._sub_page_widgets = {}
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_activity_list': self.refresh_activity_list,
           'refresh_activity_redpoint': self.refresh_red_point,
           'refresh_activity_redpoint_by_type': self.refresh_red_point_by_type,
           'show_activity_tab_list': self.show_activity_tab_list,
           'nile_activity_ready_event': self.on_nile_activity_ready_event,
           'nile_activity_reddot_event': self.on_nile_activity_reddot_event,
           'message_on_rank_data': self.refresh_rank_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_widget(self, item_widget, a_info):
        if type(a_info) == list:
            activity_type = a_info[0]['activity_type']
            tab_name_id = confmgr.get('c_activity_config', activity_type, 'iCatalogID', default='')
            activity_type = activity_utils.switch_activity_type(activity_type)
            item_widget.btn_tab.EnableCustomState(True)

            @item_widget.btn_tab.unique_callback()
            def OnClick(btn, touch, activity_type=activity_type):
                tab_name_id = confmgr.get('c_activity_config', activity_type, 'iCatalogID', default='')
                activity_type = activity_utils.switch_activity_type(activity_type)
                self.on_click_btn_tab_with_folder(activity_type, a_info)

        else:
            activity_type = a_info['activity_type']
            tab_name_id = activity_utils.get_activity_tab_name(activity_type)
            item_widget.btn_tab.EnableCustomState(True)

            @item_widget.btn_tab.unique_callback()
            def OnClick(btn, touch):
                self.on_click_btn_tab_without_folder(activity_type, a_info)

        if not self._default_activity_type:
            self._default_activity_type = activity_type
        from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_JA
        is_jp = get_cur_text_lang() == LANG_JA and not global_data.feature_mgr.is_support_TextWithCarriageReturn_Shrink() and self._cur_font_sizes
        font_scale = 20.0 / 24.0 if is_jp else 1.0
        if self._default_font_size:
            item_widget.btn_tab.SetText(int(tab_name_id), font_size=self._default_font_size * font_scale)
        elif not is_jp:
            item_widget.btn_tab.SetText(int(tab_name_id))
        else:
            item_widget.btn_tab.SetText(int(tab_name_id), self._cur_font_sizes[1] * font_scale)
            if self._cur_font_sizes[0]:
                item_widget.btn_tab.SetTextFontSizes(True, self._cur_font_sizes[1] * font_scale, self._cur_font_sizes[2] * font_scale, self._cur_font_sizes[3] * font_scale)
        if self._selected_widget != item_widget:
            item_widget.btn_tab.SetSelect(False)
        if self._tab_init_cb:
            self._tab_init_cb(item_widget)

    def set_select_widget(self, sel_a_info, is_inner=False):
        item_widget = None
        tablist = self.panel.temp_tab_list.list_tab
        for index, a_info in enumerate(self._activity_list):
            if a_info == sel_a_info:
                item_widget = tablist.GetItem(index)
                self._cur_activity_index = index
                break

        if not item_widget:
            return False
        else:
            if not is_inner:
                tablist.CenterWithNode(item_widget)
            if self._selected_widget == item_widget:
                return False
            if self._selected_widget and self._selected_widget.isValid() and not self._selected_widget.IsDestroyed():
                self._selected_widget.btn_tab and self._selected_widget.btn_tab.SetSelect(False)
                self._selected_widget.StopAnimation('continue')
                self._selected_widget.RecoverAnimationNodeState('continue')
            item_widget.btn_tab.SetSelect(True)
            item_widget.PlayAnimation('click')
            not item_widget.IsPlayingAnimation('continue') and item_widget.RecordAnimationNodeState('continue')
            item_widget.PlayAnimation('continue')
            self._selected_widget = item_widget
            return True

    def get_activity_list(self):
        if self.widget_type == WIDGET_ALPHA_PLAN:
            self._activity_list = activity_utils.get_ordered_activity_list(self.widget_type, False)
        else:
            self._activity_list = activity_utils.get_ordered_activity_list(self.widget_type)

    def show_activity_tab_list(self, flag):
        self.panel.temp_tab_list.setVisible(flag)

    def refresh_activity_list(self):
        self.init_page_tab()
        if self._jump_ui_activity_type is not None:
            self.try_select_tab(self._jump_ui_activity_type)
            self._jump_ui_activity_type = None
        else:
            self.re_select_tab()
        return

    def on_nile_activity_ready_event(self, act_id):
        self.panel.SetTimeOut(0.01, self.refresh_activity_list, tag=230221)

    def on_nile_activity_reddot_event(self, act_id):
        self.panel.SetTimeOut(0.01, self.refresh_red_point, tag=230222)

    def on_click_btn_tab_with_folder(self, activity_type, a_info):
        if is_nile_activity(activity_type):
            is_ready = global_data.nile_sdk and global_data.nile_sdk.get_activity_status(activity_type)
            if not is_ready:
                global_data.game_mgr.show_tip(get_text_by_id(81796))
                return
        if self.set_select_widget(a_info, is_inner=True):
            self.click_folder(a_info, activity_type=activity_type)

    def on_click_btn_tab_without_folder(self, activity_type, a_info):
        if is_nile_activity(activity_type):
            is_ready = global_data.nile_sdk and global_data.nile_sdk.get_activity_status(activity_type)
            if not is_ready:
                global_data.game_mgr.show_tip(get_text_by_id(81796))
                return
        if self.set_select_widget(a_info, is_inner=True):
            self._cur_view_sub_page_widget and self._cur_view_sub_page_widget.set_show(False)
            self.select_tab(activity_type, is_inner=True)

    def re_select_tab(self):
        if not self._activity_list:
            return
        else:
            cur_activity_valid = False
            for activity_info in self._activity_list:
                if type(activity_info) == list:
                    for _activity_info in activity_info:
                        if self._cur_selected_activity_type == _activity_info['activity_type']:
                            cur_activity_valid = True
                            break

                    if cur_activity_valid:
                        break
                elif type(activity_info) == dict:
                    if self._cur_selected_activity_type == activity_info['activity_type']:
                        cur_activity_valid = True
                        break

            if not cur_activity_valid:
                self._cur_selected_activity_type = ''
                self._selected_widget = None
            if self._cur_selected_activity_type:
                activity_type = self._cur_selected_activity_type
            else:
                if self._cur_activity_index >= len(self._activity_list):
                    self._cur_activity_index = 0
                a_info = self._activity_list[self._cur_activity_index]
                if type(a_info) == list:
                    for sub_index, s_a_info in enumerate(a_info):
                        activity_type = s_a_info['activity_type']
                        break

                else:
                    activity_type = a_info['activity_type']
            self.select_tab(activity_type)
            return

    def init_page_tab(self):
        self.get_activity_list()
        self._init_page_tab()

    def _init_page_tab(self):
        activity_list = self._activity_list
        tablist = self.panel.temp_tab_list.list_tab
        tablist.SetInitCount(len(activity_list))
        if not self._cur_font_sizes and activity_list:
            first_node = tablist.GetItem(0)
            self._cur_font_sizes = first_node.btn_tab.GetTextFontSizes()
        for index, a_info in enumerate(activity_list):
            item_widget = tablist.GetItem(index)
            self.on_init_widget(item_widget, a_info)
            if self.widget_type == WIDGET_ALPHA_PLAN and index == 1:
                self._default_activity_type = a_info['activity_type']

        if self.widget_type == WIDGET_ALPHA_PLAN and self._cur_view_page_widget:
            self._cur_view_page_widget.parent_refresh_page_tab()
        self.refresh_red_point()
        img_tips_node = getattr(self.panel.temp_tab_list, 'img_tips')
        if not img_tips_node:
            return
        if not activity_list or len(activity_list) <= 1:
            self.panel.temp_tab_list.img_tips.setVisible(False)
        else:
            is_bottom = [
             True]

            def OnScrolling():
                if is_bottom[0]:
                    self.panel.temp_tab_list.img_tips.setVisible(True)
                    self.panel.temp_tab_list.PlayAnimation('down_tips')
                    is_bottom[0] = False

            def OnScrollToBottom():
                if not is_bottom[0]:
                    self.panel.temp_tab_list.img_tips.setVisible(False)
                    self.panel.temp_tab_list.StopAnimation('down_tips')
                    is_bottom[0] = True

            tablist.OnScrollToBottom = OnScrollToBottom
            tablist.OnScrolling = OnScrolling
            OnScrolling()

    def refresh_rank_content(self, *args):
        self.refresh_red_point()

    def refresh_red_point(self):
        tablist = self.panel.temp_tab_list.list_tab
        for index, a_info in enumerate(self._activity_list):
            item_widget = tablist.GetItem(index)
            if type(a_info) == list:
                activity_type = a_info[0]['activity_type']
                cUiData = confmgr.get('c_activity_config', activity_type, 'cUiData', default={})
                merge_activity = cUiData.get('merge_activity')
                if merge_activity:
                    activity_type = activity_utils.switch_activity_type(activity_type)
                    tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
                    if tab_name_id:
                        count = 0
                        for sub_index, s_a_info in enumerate(a_info):
                            activity_type = s_a_info['activity_type']
                            tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
                            if tab_name_id:
                                if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                                    continue
                                count += activity_utils.get_redpoint_count_by_type(activity_type)

                    else:
                        if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                            continue
                        count = activity_utils.get_redpoint_count_by_type(activity_type)
                else:
                    count = 0
                    for sub_index, s_a_info in enumerate(a_info):
                        activity_type = s_a_info['activity_type']
                        if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                            continue
                        count += activity_utils.get_redpoint_count_by_type(activity_type)

            else:
                activity_type = a_info['activity_type']
                if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                    continue
                count = activity_utils.get_redpoint_count_by_type(activity_type)
            item_widget.img_red.setVisible(count > 0)

        self._cur_view_sub_page_widget and self._cur_view_sub_page_widget.refresh_red_point()

    def refresh_red_point_by_type(self, widget_type):
        if widget_type == self.widget_type:
            self.refresh_red_point()

    def get_activity_a_info(self, activity_type):
        for index, a_info in enumerate(self._activity_list):
            if type(a_info) == list:
                for sub_index, s_a_info in enumerate(a_info):
                    if activity_type == s_a_info['activity_type']:
                        return a_info

            elif a_info['activity_type'] == activity_type:
                return a_info

        return None

    def click_folder(self, fold_list, activity_type=None):
        ui_template = 'activity/activity/i_task_control'
        unique_node_name = 'sub_page_widget_default'
        tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        if tab_name_id:
            catalog_template = confmgr.get('activity_catalog_config', tab_name_id, 'cUiTemplate', default='').strip()
            if catalog_template:
                ui_template = catalog_template
                unique_node_name = 'sub_page_widget_{}'.format(tab_name_id)
        self._sub_page_widgets[unique_node_name] = 1
        self.reset_sub(unique_node_name)
        if not self._cur_view_sub_page_widget:
            self._cur_sub_page_name = unique_node_name
            dlg = getattr(self.panel.temp_activity_top, unique_node_name)
            if not dlg:
                dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.temp_activity_top, name=unique_node_name)
            dlg.setVisible(True)
            self._cur_view_sub_page_widget = ActivitySubPage(dlg, None)
            self._cur_view_sub_page_widget.on_init_panel()

            def select_callback--- This code section failed: ---

 379       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'select_tab'
           6  LOAD_ATTR             1  'True'
           9  LOAD_GLOBAL           1  'True'
          12  LOAD_CONST            2  'is_init'
          15  LOAD_FAST             1  'is_init'
          18  CALL_FUNCTION_513   513 
          21  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 18

            self._cur_view_sub_page_widget.set_select_callback(select_callback)
        show_sub = True
        if self._cur_view_page_widget and hasattr(self._cur_view_page_widget, 'get_sub_show'):
            show_sub = self._cur_view_page_widget.get_sub_show()
        self._cur_view_sub_page_widget.set_show(show_sub)
        self._cur_view_sub_page_widget.show_page_list(fold_list, sel_activity_type=activity_type)
        self._cur_view_sub_page_widget.refresh_red_point()
        return

    def reset_sub(self, unique_node_name):
        if self._cur_view_sub_page_widget and self._cur_sub_page_name != unique_node_name:
            self._cur_view_sub_page_widget.on_finalize_panel()
            self._cur_view_sub_page_widget = None
            for node_name, _ in six.iteritems(self._sub_page_widgets):
                if node_name != unique_node_name:
                    dlg = getattr(self.panel.temp_activity_top, node_name)
                    if dlg:
                        dlg.setVisible(False)

        return

    def try_select_tab(self, activity_type):
        a_info = self.get_activity_a_info(activity_type)
        if activity_type is not None and a_info is None and self._jump_ui_activity_type is None:
            self._jump_ui_activity_type = activity_type
            global_data.player and global_data.player.get_opened_activities()
            return
        else:
            if a_info is None:
                if self._default_activity_type:
                    a_info = self.get_activity_a_info(self._default_activity_type)
                    activity_type = self._default_activity_type
            if a_info is not None:
                self.select_tab(activity_type, is_inner=False, is_init=True)
            return

    def select_tab(self, activity_type, is_inner=False, is_init=False):
        if not activity_type and self._default_activity_type:
            activity_type = self._default_activity_type
        self._select_tab(activity_type, is_inner, is_init)

    def _select_tab(self, activity_type, is_inner, is_init):
        if not is_inner:
            a_info = self.get_activity_a_info(activity_type)
            if a_info:
                if type(a_info) == list:
                    self.set_select_widget(a_info, is_inner=is_inner)
                    self.click_folder(a_info, activity_type=activity_type)
                else:
                    self.set_select_widget(a_info, is_inner=is_inner)
                    self._cur_view_sub_page_widget and self._cur_view_sub_page_widget.set_show(False)
                    self.select_tab(activity_type, is_inner=True, is_init=is_init)
            return
        self.change_to_activity_tab(activity_type, is_init)

    def change_to_activity_tab(self, activity_type, is_init):
        ui_template = confmgr.get('c_activity_config', activity_type, 'cUiTemplate', default='').strip()
        ui_class = confmgr.get('c_activity_config', activity_type, 'cUiClass', default='')
        if global_data.channel.get_name() != 'netease' or global_data.is_pc_mode:
            cUiData = confmgr.get('c_activity_config', activity_type, 'cUiData')
            if cUiData and type(cUiData) is dict and 'change_ui_by_channel' in cUiData:
                ui_template = cUiData['change_ui_by_channel'].get('cUiTemplate').strip() or ui_template
                ui_class = cUiData['change_ui_by_channel'].get('cUiClass') or ui_class
        if not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
            cUiData = confmgr.get('c_activity_config', activity_type, 'cUiData')
            if cUiData and type(cUiData) is dict and 'change_ui_by_test_group' in cUiData:
                change_ui_data = cUiData['change_ui_by_test_group']
                if 'test_end' in change_ui_data or global_data.abtest_group:
                    ui_template = change_ui_data.get('cUiTemplate').strip() or ui_template
                    ui_class = change_ui_data.get('cUiClass') or ui_class
        cls = activity_utils.get_activity_cls(ui_class)
        unique_nodename = 'a_template_%s' % activity_type
        if not cls:
            print('[ERROR] load c_activity_config %s cUiTemplate [%s] failed:' % (activity_type, ui_template))
            return
        else:
            if self._cur_selected_activity_type == activity_type:
                return
            last_selected_activity_type = self._cur_selected_activity_type
            if not global_data.player:
                return
            global_data.player.read_activity_list(activity_type)
            self._cur_selected_activity_type = activity_type
            is_nile = is_nile_activity(activity_type)
            if is_nile:
                parent_name = confmgr.get('c_activity_config', activity_type, 'cParentNodeName', default='')
            else:
                parent_name = confmgr.get('nile_activity_conf', activity_type, 'cParentNodeName', default='')
            if parent_name:
                parent_node = getattr(self.panel, parent_name)
            else:
                parent_node = self.panel.temp_activity
            self.qa_activity_help_notify(activity_type)
            bTransferBetweenSubPage = False
            tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
            if tab_name_id and not is_nile:
                bTransferBetweenSubPage = confmgr.get('activity_catalog_config', tab_name_id, 'bTransferBetweenSubPage', default=False)
            last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
            if bTransferBetweenSubPage and self._cur_view_page_widget and last_tab_name_id == tab_name_id and self._cur_view_page_widget and hasattr(self._cur_view_page_widget, 'transfer_panel_out'):
                self._cur_view_page_widget and self._cur_view_page_widget.set_show(False)
                if self._cur_view_page_widget:
                    last_panel = self._cur_view_page_widget.get_panel() if 1 else None
                    self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
                    self.check_is_nile_activity_finalized(last_selected_activity_type, last_panel)
                    dlg = self._cur_view_page_widget.transfer_panel_out()
                    self._cur_view_page_widget = cls(dlg, activity_type)
                    if hasattr(self._cur_view_page_widget, 'transfer_panel_in'):
                        self._cur_view_page_widget.transfer_panel_in()
                else:
                    cur_view_page_widget, dlg = self.get_act_class_and_dlg(is_nile, activity_type, unique_nodename, parent_node, ui_template, cls)
                    if not cur_view_page_widget:
                        self._cur_view_page_widget = None
                        return
                    self._cur_view_page_widget and self._cur_view_page_widget.set_show(False)
                    last_panel = self._cur_view_page_widget.get_panel() if self._cur_view_page_widget else None
                    self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
                    self.check_is_nile_activity_finalized(last_selected_activity_type, last_panel)
                    self._cur_view_page_widget = cur_view_page_widget
                if hasattr(self._cur_view_page_widget, 'set_activity_info'):
                    self._cur_view_page_widget.set_activity_info(last_selected_activity_type, self._cur_view_sub_page_widget)
                if self.widget_type == WIDGET_ALPHA_PLAN:
                    self._cur_view_page_widget.set_tab_panel(self.panel)
                self._cur_view_page_widget.set_show(True, is_init)
                self._cur_view_page_widget.on_init_panel()
                if self.widget_type == WIDGET_ALPHA_PLAN:
                    self._cur_view_page_widget.play_panel_animation()
                if activity_utils.get_redpoint_type(activity_type) == ACTIVITY_REDDOT_CLICK:
                    global_data.player.save_activity_click_data(activity_type)
                if self._request_activities or global_data.player:
                    global_data.player.get_opened_activities()
                self._request_activities = True
            if self._select_widget_cb:
                self._select_widget_cb(self._cur_view_page_widget)
            return

    def get_act_class_and_dlg(self, is_nile, activity_type, unique_nodename, parent_node, ui_template, cls):
        if not is_nile:
            dlg = getattr(parent_node, unique_nodename)
            if not dlg:
                template_info = cls.get_custom_template_info()
                dlg = global_data.uisystem.load_template_create(ui_template, parent=parent_node, template_info=template_info, name=unique_nodename)
            cur_view_page_widget = cls(dlg, activity_type)
            return (
             cur_view_page_widget, dlg)
        else:
            unique_nodename = 'a_template_%s' % activity_type
            dlg = getattr(parent_node, unique_nodename)
            dlg_class_instance = global_data.nile_sdk.get_activity_panel(activity_type)
            if not dlg_class_instance:
                return (None, None)
            if not dlg:
                dlg_class_instance or log_error('Failed to get panel class for nile activity:', activity_type)
                return (None, None)
            if dlg_class_instance.panel and dlg_class_instance.panel.isValid():
                dlg = dlg_class_instance.panel if 1 else None
                if not dlg:
                    return (None, None)
                parent_node = self.panel.temp_activity
                parent_node.AddChild(unique_nodename, dlg)
            return (dlg_class_instance, dlg)
            return

    def refresh_page_widget(self):
        if self._cur_view_page_widget:
            self._cur_view_page_widget.refresh_panel()

    def get_cur_view_page_widget(self):
        return self._cur_view_page_widget

    def get_cur_view_sub_page_widget(self):
        return self._cur_view_sub_page_widget

    def on_main_ui_reshow(self):
        if self._cur_view_page_widget:
            self._cur_view_page_widget.on_main_ui_reshow()

    def on_main_ui_hide(self):
        if self._cur_view_page_widget:
            self._cur_view_page_widget.on_main_ui_hide()

    def check_is_nile_activity_finalized(self, activity_type, node):
        if is_nile_activity(activity_type):
            if node:
                node.Destroy(True)

    def qa_activity_help_notify(self, activity_type):
        if not global_data.is_inner_server:
            return
        if activity_utils.check_activity_time_changable(activity_type):
            global_data.game_mgr.show_tip('\xe3\x80\x90\xe5\x86\x85\xe6\x9c\x8d\xe9\x80\x9a\xe7\x9f\xa5\xe3\x80\x91\xe6\xad\xa4\xe6\xb4\xbb\xe5\x8a\xa8{}\xe5\xa1\xab\xe5\x86\x99\xe4\xba\x86\xe5\x8f\xaf\xe5\x8f\x98\xe6\x97\xb6\xe9\x95\xbf\xef\xbc\x8c\xe8\xaf\xb7QA\xe4\xb8\x8e\xe7\xad\x96\xe5\x88\x92\xe6\xa0\xb8\xe5\xaf\xb9\xe9\xaa\x8c\xe6\x94\xb6\xe8\x8c\x83\xe5\x9b\xb4\xef\xbc\x8c\xe5\xb9\xb6\xe6\xb3\xa8\xe6\x84\x8f\xe6\xb4\xbb\xe5\x8a\xa8\xe5\xa4\x84\xe4\xba\x8e\xe9\x9b\x86\xe5\x90\x88\xe9\xa1\xb5\xe6\x97\xb6\xe7\x9a\x84\xe9\x80\xbb\xe8\xbe\x91'.format(activity_type))