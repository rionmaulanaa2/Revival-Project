# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallItemLstWidget.py
from __future__ import absolute_import
from logic.gutils import mall_utils

class MallItemLstWidget(object):

    def __init__(self, parent):
        self.parent = parent
        self.panel = parent.panel
        self.init_parameters()
        self.init_event()
        self.init_widget()

    def on_finalize_panel(self):
        self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
        self._cur_view_page_widget = None
        return

    def init_parameters(self):
        self._cur_page_index = None
        self._cur_sub_page_index = None
        self._cur_view_page_widget = None
        return

    def init_event(self):
        pass

    def init_widget(self):
        pass

    def get_cur_page_index(self):
        return self._cur_page_index

    def get_cur_sub_page_index(self):
        return self._cur_sub_page_index

    def reset_mall_list(self):
        self.refresh_mall_list(self._cur_page_index, self._cur_sub_page_index)

    def init_mall_list(self, page_index, sub_page_index=None):
        self.refresh_mall_list(page_index, sub_page_index)

    def refresh_mall_list(self, page_index, sub_page_index=None):
        if page_index is None:
            return
        else:
            node_name, template_name, cls = mall_utils.get_mall_list_widget_info(page_index, sub_page_index)
            dlg = getattr(self.panel.temp_content, node_name)
            if not dlg:
                dlg = global_data.uisystem.load_template_create(template_name, parent=self.panel.temp_content, name=node_name)
            if not (self._cur_page_index == page_index and self._cur_sub_page_index == sub_page_index):
                self._cur_view_page_widget and self._cur_view_page_widget.set_show(False)
                self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
                self._cur_view_page_widget = cls(dlg)
                self._cur_page_index = page_index
                self._cur_sub_page_index = sub_page_index
                self._cur_view_page_widget.init_mall_list(page_index, sub_page_index)
                self._cur_view_page_widget.set_show(True)
            elif self._cur_view_page_widget:
                self._cur_view_page_widget.reset_mall_list()
            return

    def do_show_panel(self):
        if self._cur_view_page_widget and hasattr(self._cur_view_page_widget, 'do_show_panel'):
            self._cur_view_page_widget.do_show_panel()

    def do_hide_panel(self):
        if self._cur_view_page_widget and hasattr(self._cur_view_page_widget, 'do_hide_panel'):
            self._cur_view_page_widget.do_hide_panel()

    def jump_to_goods_id(self, goods_id):
        if self._cur_view_page_widget and hasattr(self._cur_view_page_widget, 'jump_to_goods_id'):
            self._cur_view_page_widget.jump_to_goods_id(goods_id)