# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/MyVideoUI.py
from __future__ import absolute_import
import six
from functools import cmp_to_key
import os
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.comsys.video import video_record_utils as vru
WIDGET_HIGH_VIDEO = 'widget_high_video'
WIDGET_FREE_VIDEO = 'widget_free_video'
WIDGET_EMPTY = 'widget_empty'
WIDGET_OPEN_HIGH = 'widget_open_high'
WIDGET_OPEN_FREE = 'widget_open_free'

class MyVideoUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/my_video'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'bg_node.btn_close.OnClick': '_on_click_back_btn'
       }

    def on_init_panel(self, page_id=0):
        self._archive_data = ArchiveManager().get_archive_data(vru.SETTING_NAME)
        self._init_page_id = page_id
        self._video_lst = []
        self._free_video_lst = []
        self._init_video_lst()
        self._widget_name = ''
        self._widgets = {}
        self._widget_info = {WIDGET_HIGH_VIDEO: [
                             'VideoListWidget', 'i_video_list', self._video_lst],
           WIDGET_FREE_VIDEO: [
                             'VideoListWidget', 'i_video_list', self._free_video_lst],
           WIDGET_EMPTY: [
                        'VideoWidget', 'i_empty', None],
           WIDGET_OPEN_HIGH: [
                            'VideoRecordDescribeWidget', 'i_highlight_describe', None],
           WIDGET_OPEN_FREE: [
                            'VideoRecordDescribeWidget', 'i_free_describe', None]
           }
        self.panel.bg_node.lab_title.SetString(2292)
        self._init_page_tab(self._init_page_id)
        return

    def _init_video_lst(self):
        for video_path, video_info in six.iteritems(self._archive_data):
            if not os.path.exists(video_path):
                continue
            video_key = video_info.get('key', '')
            if not video_key:
                continue
            if video_key in (vru.HIGH_KEY, vru.REFINE_KEY):
                self._video_lst.append(video_info)
            elif video_key in (vru.FREE_KEY,):
                self._free_video_lst.append(video_info)

        def sort_func(info_1, info_2):
            s_t_1 = info_1.get('start_time', 0)
            s_t_2 = info_2.get('start_time', 0)
            if s_t_1 != s_t_2:
                if s_t_1 < s_t_2:
                    return 1
                return -1
            else:
                key = info_1.get('key', '')
                if key in (vru.FREE_KEY,):
                    return 1
                return -1

        self._video_lst.sort(key=cmp_to_key(sort_func))
        self._free_video_lst.sort(key=cmp_to_key(sort_func))

    def _init_page_tab(self, page_id=0):
        from logic.gutils import new_template_utils
        data_list = [{'text': 2255}, {'text': 2257}]
        lst_tab = self.panel.nd_high_light.list_tab
        new_template_utils.init_top_tab_list(lst_tab, data_list, self._on_select_tab)
        lst_tab.GetItem(page_id).btn_tab.OnClick(None)
        return

    def _on_select_tab(self, item_widget, idx):
        if idx == 0:
            from logic.gcommon.common_const import ui_operation_const
            high_light_enable = global_data.player.get_setting_2(ui_operation_const.HIGH_LIGHT_KEY)
            if len(self._video_lst) > 0:
                widget_name = WIDGET_HIGH_VIDEO
            elif high_light_enable:
                widget_name = WIDGET_EMPTY
            else:
                widget_name = WIDGET_OPEN_HIGH
        else:
            from logic.gcommon.common_const import ui_operation_const
            free_record_enable = global_data.player.get_setting_2(ui_operation_const.FREE_RECORD_VIDEO_KEY)
            if len(self._free_video_lst) > 0:
                widget_name = WIDGET_FREE_VIDEO
            elif free_record_enable:
                widget_name = WIDGET_EMPTY
            else:
                widget_name = WIDGET_OPEN_FREE
        if self._widget_name == widget_name:
            return
        else:
            last_widget = self._widgets.get(self._widget_name, None)
            if last_widget:
                last_widget.hide()
            self._widget_name = widget_name
            sel_widget = None
            if widget_name in self._widgets:
                sel_widget = self._widgets[widget_name]
            else:
                mod_name, template_name, _ = self._widget_info[widget_name]
                mod = __import__('logic.comsys.setting_ui.%s' % (mod_name,), globals(), locals(), [mod_name])
                cls = getattr(mod, mod_name, None)
                template_name = 'setting/setting_highlight/{0}'.format(template_name)
                widget_panel = global_data.uisystem.load_template_create(template_name, parent=self.panel.nd_content)
                sel_widget = cls(self, widget_panel)
                self._widgets[widget_name] = sel_widget
            sel_widget.show()
            video_info = self._widget_info[widget_name][2]
            sel_widget.refresh(video_info)
            return

    def check_can_mouse_scroll(self):
        pass

    def _on_click_back_btn(self, *args):
        self.close()

    def on_finalize_panel(self):
        for widget_name in self._widgets:
            widget = self._widgets[widget_name]
            widget.destroy()

        self._widgets = {}