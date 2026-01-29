# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/ChangeHeadUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const as iconst
from logic.gutils import role_head_utils
from logic.comsys.role.ChangeHeadFrameWidget import ChangeHeadFrameWidget
from logic.comsys.role.ChangeRolePhotoWidget import ChangeRolePhotoWidget
from logic.comsys.role.ChangeChatFrameWidget import ChangeChatFrameWidget
from common.cfg import confmgr
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_TALKING, L_ITEM_TYPE_HEAD_PHOTO, L_ITEM_TYPE_HEAD_FRAME
from common.const import uiconst

class ChangeHeadUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/change_head'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self.init_parameters()
        tab_index = kargs.get('tab_index', 0)
        item_no = kargs.get('item_no', None)
        self.init_event(True)
        self.init_panel()
        self.hide_main_ui(exceptions=['PlayerInfoUI'])
        if tab_index > 0:
            self.on_tab_selected(tab_index)
        if item_no:
            self.select_item_by_item_no(item_no)
        return

    def init_parameters(self):
        self._my_uid = global_data.player.uid
        self._cur_index = None
        self.tab_widgets = {}
        self.widget_nd = [{'widget_func': self.init_change_frame_template,'node': self.panel.nd_change_frame,'text_id': 80732}, {'widget_func': self.init_change_photon_template,'node': self.panel.nd_change_photo,'text_id': 80830}, {'widget_func': self.init_change_chat_template,'node': self.panel.nd_change_chat,'text_id': 81159}]
        return

    def init_panel(self):
        self.init_tab_list()
        self.on_tab_selected(0, False)

    def init_event(self, bind):
        if bind:
            global_data.emgr.refresh_item_red_point += self.refresh_red_point
        else:
            global_data.emgr.refresh_item_red_point -= self.refresh_red_point

    def init_tab_list(self):
        tab_list = self.panel.temp_bg.list_tab
        tab_list.SetInitCount(len(self.widget_nd))
        all_tab_widgets = tab_list.GetAllItem()
        for index, data in enumerate(self.widget_nd):
            tab_widget = all_tab_widgets[index]
            button = tab_widget.btn_window_tab
            tab_widget.btn_window_tab.SetText(get_text_local_content(data['text_id']))
            button.EnableCustomState(True)

            @button.unique_callback()
            def OnClick(btn, touch, index=index):
                self.on_tab_selected(index)

        self.refresh_red_point()

    def on_click_close_btn(self, *args):
        self.close()

    def on_tab_selected(self, sel_index, really=True):
        cur_widget = None
        for index, data in enumerate(self.widget_nd):
            ui_item = self.panel.temp_bg.list_tab.GetItem(index)
            if index != sel_index:
                widget = self.tab_widgets.get(index, None)
                if widget:
                    widget.hide()
                ui_item.btn_window_tab.SetSelect(False)
                ui_item.StopAnimation('continue')
                ui_item.RecoverAnimationNodeState('continue')
            else:
                widget = self.tab_widgets.get(sel_index, None)
                if widget:
                    widget.refresh()
                    widget.show()
                else:
                    widget_func = data.get('widget_func', None)
                    if widget_func:
                        widget = widget_func()
                        self.tab_widgets[index] = widget
                        widget.show()
                cur_widget = widget
                if really:
                    widget.set_really_show()
                ui_item.btn_window_tab.SetSelect(True)
                ui_item.PlayAnimation('click')
                ui_item.RecordAnimationNodeState('continue')
                ui_item.PlayAnimation('continue')

        return cur_widget

    def init_change_frame_template(self):
        return ChangeHeadFrameWidget(self.panel.nd_change_frame, self.panel)

    def init_change_photon_template(self):
        return ChangeRolePhotoWidget(self.panel.nd_change_photo, self.panel)

    def init_change_chat_template(self):
        return ChangeChatFrameWidget(self.panel.nd_change_chat, self.panel.nd_change_chat)

    def refresh_red_point(self):
        from logic.gutils import red_point_utils
        from logic.gcommon.item import lobby_item_type
        new_photo = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_PHOTO)
        new_frame = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_FRAME)
        red_point_utils.show_red_point_template(self.panel.temp_bg.list_tab.GetItem(1).img_hint, new_photo)
        red_point_utils.show_red_point_template(self.panel.temp_bg.list_tab.GetItem(0).img_hint, new_frame)

    def on_finalize_panel(self):
        self.show_main_ui()
        self.init_event(False)
        self._cur_index = None
        for widget in six.itervalues(self.tab_widgets):
            if hasattr(widget, 'on_finalize_panel'):
                widget.on_finalize_panel()

        self.tab_widgets = {}
        return

    def jump_to_item_no_page(self, item_no):
        if item_no is not None:
            from logic.gutils import item_utils
            from logic.gcommon.item import lobby_item_type
            item_type = item_utils.get_lobby_item_type(item_no)
            page_index_dict = {L_ITEM_TYPE_TALKING: 2,
               L_ITEM_TYPE_HEAD_PHOTO: 1,
               L_ITEM_TYPE_HEAD_FRAME: 0
               }
            page_index = page_index_dict.get(item_type, None)
            if page_index is not None:
                return self.on_tab_selected(page_index)
        return

    def select_item_by_item_no(self, item_no):
        cur_widget = self.jump_to_item_no_page(item_no)
        if cur_widget is not None:
            select_func = getattr(cur_widget, 'select_item_by_item_no')
            if callable(select_func):
                select_func(item_no)
        return