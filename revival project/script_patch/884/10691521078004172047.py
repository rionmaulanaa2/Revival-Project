# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/WidgetCommonComponent.py
from __future__ import absolute_import
import six

class WidgetCommonComponent(object):

    def __init__(self, widget_content_nd, widget_list_data):
        self.tab_widgets = {}
        self.cur_index = None
        self.widget_switch_func = None
        self.tab_list = widget_list_data
        self.widget_content_nd = widget_content_nd
        if not self.widget_content_nd:
            log_error('Invalid Node for mounting widget!')
        return

    def set_widget_switch_func(self, widget_switch_func):
        self.widget_switch_func = widget_switch_func

    def destroy(self):
        for name, widget in six.iteritems(self.tab_widgets):
            widget.destroy()

        self.tab_widgets = {}
        self.tab_list_ui_item = None
        self.widget_switch_func = None
        self.tab_list = None
        return

    def get_cur_index(self):
        return self.cur_index

    def get_cur_widget(self):
        if self.cur_index in self.tab_widgets:
            return self.tab_widgets[self.cur_index]
        else:
            return None
            return None

    def get_widget_by_index(self, index):
        if index in self.tab_widgets:
            return self.tab_widgets[index]
        else:
            return None
            return None

    def on_switch_to_widget(self, widget_index):
        if widget_index not in self.tab_widgets:
            if widget_index < len(self.tab_list):
                data = self.tab_list[widget_index]
                widget = data.get('widget_template')
                widget_func = data.get('widget_func')
                if widget and widget_func:
                    _nd = global_data.uisystem.load_template_create(widget, self.widget_content_nd)
                    _nd.SetPosition('50%', '50%')
                    widget_wrapper = widget_func(_nd)
                    self.tab_widgets[widget_index] = widget_wrapper
        if widget_index == self.cur_index:
            return
        if self.cur_index in self.tab_widgets:
            cur_widget = self.tab_widgets[self.cur_index]
            cur_widget.hide()
            if callable(self.widget_switch_func):
                self.widget_switch_func(self.cur_index, cur_widget, False)
        self.cur_index = widget_index
        if self.cur_index in self.tab_widgets:
            cur_widget = self.tab_widgets[self.cur_index]
            cur_widget.show()
            if callable(self.widget_switch_func):
                self.widget_switch_func(self.cur_index, cur_widget, True)