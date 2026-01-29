# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SimpleLabelUIBase.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.uisys.uielment.CCVerTemplateList import CCVerTemplateList
from common.uisys.uielment.CCHorzTemplateList import CCHorzTemplateList
from common.uisys.uielment.CCVerAsyncList import CCVerAsyncList
from common.uisys.uielment.CCButton import CCButton

class SimpleLabelUIBase(BasePanel):

    def get_label_type_by_name(self, name):
        if not self.label_data:
            return None
        else:
            for label_type, label_info in six.iteritems(self.label_data):
                text_name = label_info.get('text', '')
                if text_name == name:
                    return label_type

            return None

    def _init(self):
        self._init_label()
        if not self.label_type:
            return
        self._show_label_type(self.label_type)

    def _get_label_idx_by_type(self, cur_type):
        if self.label_data == None or len(self.label_data) <= 0:
            return 0
        else:
            index = 1
            for label_type, _ in six.iteritems(self.label_data):
                if label_type == cur_type:
                    return index
                index += 1

            return 0

    def _get_label_ui(self, cur_type):
        index = self._get_label_idx_by_type(cur_type)
        if hasattr(self.panel, 'lv_tab') and self.panel.lv_tab:
            tab_scroll = self.panel.lv_tab
            if isinstance(tab_scroll, CCVerTemplateList) or isinstance(tab_scroll, CCHorzTemplateList):
                return tab_scroll.GetItem(index - 1)
            if isinstance(tab_scroll, CCVerAsyncList):
                return tab_scroll.GetAsynItem(index - 1)
            log_error('Error,unsupport scroll type!')
        else:
            return None
        return None

    def _init_label(self):
        if not self.label_data:
            return
        self.before_init_label_list()
        if hasattr(self.panel, 'lv_tab') and self.panel.lv_tab:
            if isinstance(self.panel.lv_tab, CCVerTemplateList) or isinstance(self.panel.lv_tab, CCHorzTemplateList):
                self.panel.lv_tab.SetInitCount(len(self.label_data))
                self.panel.lv_tab.ScrollToTop()
                self.panel.lv_tab.setVisible(True)
            else:
                log_error('Error,Unsupport Scroll Type!')
        for label_type, label_data in six.iteritems(self.label_data):
            label_data = self.label_data[label_type]
            labelUI = self._get_label_ui(label_type)
            if not labelUI:
                continue
            self.init_one_scroll_item(labelUI, label_data, label_type)
            self.on_label_inited(labelUI, label_type)

    def on_label_selected(self):
        pass

    def on_label_unselected(self):
        pass

    def _on_label_select(self, label_ui):
        nd_select = getattr(label_ui, 'nd_select', None)
        if nd_select:
            nd_select.setVisible(True)
        nd_unselect = getattr(label_ui, 'nd_unselect', None)
        if nd_unselect:
            nd_unselect.setVisible(False)
        label_btn = getattr(label_ui, 'btn_tab', None)
        if label_btn:
            label_btn.SetSelect(True)
        self.on_label_selected()
        return

    def _on_label_unselect(self, label_ui):
        nd_select = getattr(label_ui, 'nd_select', None)
        if nd_select:
            nd_select.setVisible(False)
        nd_unselect = getattr(label_ui, 'nd_unselect', None)
        if nd_unselect:
            nd_unselect.setVisible(True)
        label_btn = getattr(label_ui, 'btn_tab', None)
        if label_btn:
            label_btn.SetSelect(False)
        self.on_label_unselected()
        return

    def show_label_type(self, label_type):
        self._close_cur_show()
        if not self.label_data:
            return
        label_info = self.label_data.get(label_type, {})
        if not label_info:
            return
        self.set_label_node_visible(label_type, True)
        label_ui = self._get_label_ui(self.label_type)
        self._on_label_unselect(label_ui)
        self.label_type = label_type
        self._show_label_type(self.label_type)

    def _close_cur_show(self):
        if self.label_type is not None:
            label_ui = self._get_label_ui(self.label_type)
            self._on_label_unselect(label_ui)
            label_data = self.label_data.get(self.label_type, {})
            node = label_data.get('node')
            if node:
                self.set_label_node_visible(self.label_type, False)
            ui_name = label_data.get('menu')
            if ui_name:
                global_data.ui_mgr.close_ui(ui_name)
        self.label_type = None
        return

    def _show_label_type(self, label_type):
        label_ui = self._get_label_ui(label_type)
        if label_ui:
            self._on_label_select(label_ui)
            label_data = self.label_data.get(self.label_type, {})
            node = label_data.get('node')
            if node:
                self.set_label_node_visible(self.label_type, True)
            ui_name = label_data.get('menu')
            module_path = label_data.get('path')
            if ui_name:
                global_data.ui_mgr.show_ui(ui_name, module_path)
            self.run_label_show_func(self.label_type)

    def init_one_scroll_item(self, labelUI, label_data, label_type):
        label_btn = getattr(labelUI, 'btn_tab', None)
        if not label_data:
            labelUI.setVisible(False)
            return
        else:
            labelUI.setVisible(True)
            label_btn.labelIndex = label_type
            label_btn.EnableCustomState(True)
            label_str = label_data.get('text', '')
            label_btn.SetText(label_str)
            if hasattr(labelUI, 'tf_select') and labelUI.tf_select:
                labelUI.tf_select.setString(label_str)
            if hasattr(labelUI, 'tf_unselect') and labelUI.tf_unselect:
                labelUI.tf_unselect.setString(label_str)
            label_btn.SetEnableTouch(True)
            nd_select = getattr(labelUI, 'nd_select', None)
            cur_show_type = label_type == self.label_type
            if nd_select:
                nd_select.setVisible(cur_show_type)
            nd_unselect = getattr(labelUI, 'nd_unselect', None)
            if nd_unselect:
                nd_unselect.setVisible(not cur_show_type)
            if isinstance(label_btn, CCButton):

                @label_btn.unique_callback()
                def OnClick(btn, touch):
                    label_type = btn.labelIndex
                    if self.label_type == label_type:
                        return
                    self.show_label_type(label_type)

            return

    def on_label_inited(self, label_ui, label_type):
        pass

    def before_init_label_list(self):
        pass

    def set_label_enable(self, label_index, enable):
        label_data = self.label_data.get(label_index, None)
        if label_data is not None:
            label_ui = self._get_label_ui(label_index)
            if label_ui is not None:
                label_ui.setVisible(enable)
        return

    def set_label_node_visible(self, label_type, visible):
        label_info = self.label_data.get(label_type, {})
        if not label_info:
            return
        else:
            node_str = label_info.get('node', None)
            if node_str is not None:
                node = getattr(self.panel, node_str, None)
                if node:
                    node.setVisible(visible)
            return

    def run_label_show_func(self, label_type):
        label_info = self.label_data.get(label_type, {})
        if not label_info:
            return
        else:
            show_func = label_info.get('show_func', None)
            if show_func is not None:
                show_func()
            return

    def close(self):
        self._close_cur_show()
        super(SimpleLabelUIBase, self).close()