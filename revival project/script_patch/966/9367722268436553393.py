# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyInfoMessage.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gutils import item_utils
from logic.comsys.common_ui import CommonInfoUtils
import cc
from logic.gcommon.common_const import battle_const
from common.const.uiconst import DIALOG_LAYER_ZORDER_2, UI_TYPE_MESSAGE
from logic.gutils import role_head_utils
from logic.comsys.common_ui.CommonInfoMessage import CommonInfoMessage

class LobbyInfoMessage(CommonInfoMessage):
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2

    def on_init_panel(self, on_process_done=None):
        super(LobbyInfoMessage, self).on_init_panel(on_process_done)

    def is_last_message(self):
        ui = global_data.ui_mgr.get_ui('LobbyInfoUI')
        if ui:
            return ui._bottom_message_queue.is_last_message()
        return True

    def main_process_one_message(self, message, finish_cb):
        if type(message) in (list, tuple):
            msg_dict = message[0]
        else:
            msg_dict = message
        content_txt = msg_dict.get('content_txt')
        item_id = msg_dict.get('item_id')
        i_type = msg_dict.get('i_type')
        show_num = msg_dict.get('show_num')
        last_show_num = msg_dict.get('last_show_num', 0)
        num_func_name = msg_dict.get('set_num_func')
        icon_path = msg_dict.get('icon_path')
        bar_path = msg_dict.get('bar_path')
        bar_module_path = msg_dict.get('bar_module_path', None)
        icon_module_path = msg_dict.get('icon_module_path', None)
        set_attr_dict = msg_dict.get('set_attr_dict')
        hide_nodes = msg_dict.get('hide_nodes', [])
        ext_message_func = msg_dict.get('ext_message_func', None)
        panel_var_name = self.get_panel_var_name()
        cur_panel = self._panel_map.get(panel_var_name, None)
        if cur_panel and cur_panel.isValid():
            CommonInfoUtils.destroy_ui(cur_panel)
        self.set_panel_map(panel_var_name, None)
        cur_panel = CommonInfoUtils.create_ui(i_type, self.panel)
        self.set_panel_map(panel_var_name, cur_panel)
        if not cur_panel:
            finish_cb()
            return
        else:
            set_num_func = None
            if num_func_name:
                set_num_func = getattr(CommonInfoUtils, num_func_name)
            set_num_func = set_num_func if set_num_func else CommonInfoUtils.set_show_num
            if cur_panel.lab_1:
                self.reset_panel_size_and_position(cur_panel)
            content_txt and self.set_content_txt(cur_panel, content_txt, i_type)
            item_id and self.set_icon(cur_panel, item_id)
            icon_path and self.set_icon_path(cur_panel, icon_path)
            bar_path and self.set_bar_path(cur_panel, bar_path)
            bar_module_path and self.set_bar_module_path(cur_panel, bar_module_path)
            icon_module_path and self.set_icon_module_path(cur_panel, icon_module_path)
            set_attr_dict and self.set_panel_attr(cur_panel, set_attr_dict)
            hide_nodes and self.hide_panel_nodes(cur_panel, hide_nodes)
            set_num_info = None
            if show_num:
                set_num_info = (
                 set_num_func, show_num, last_show_num, ext_message_func)

            def finish_cd_wrapper(panel_var_name=panel_var_name):
                cur_panel = self._panel_map.get(panel_var_name, None)
                if cur_panel and cur_panel.isValid():
                    CommonInfoUtils.destroy_ui(cur_panel)
                self.set_panel_map(panel_var_name, None)
                finish_cb()
                return

            self.message_ani(finish_cd_wrapper, cur_panel, set_num_info)
            return