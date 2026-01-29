# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ItemNumBtnWidget.py
from __future__ import absolute_import

class ItemNumBtnWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.item_data = {}
        self.init_add_sub_widget()
        self.init_btns()

    def init_add_sub_widget(self):
        from logic.comsys.common_ui.PressBtnComponent import PressBtnComponent
        self.add_sub_widget = PressBtnComponent(self.panel)

    def init_item(self, item_data, on_num_changed, init_quantity=1, max_tips=None, max_callback=None):
        quantity = item_data.get('quantity', 1)
        self.item_data = item_data
        self.add_sub_widget.set_args({'min_num': item_data.get('min_num', 1),
           'max_num': quantity,
           'per_num': item_data.get('per_num', 1),
           'begin_num': init_quantity,
           'begin_ttf': 1
           })

        def callback(num):
            self.panel.lab_num.SetString(''.join([str(num), '/', str(quantity)]))
            if callable(on_num_changed):
                on_num_changed(item_data, num)

        self.add_sub_widget.set_num_change_callback(callback)
        self.add_sub_widget.set_max_callback(max_callback)
        if max_tips != None:
            self.add_sub_widget.set_max_tips(max_tips)
        callback(init_quantity)
        return

    def set_num(self, num):
        if self.add_sub_widget:
            self.add_sub_widget.set_num(num)

    def init_btns(self):

        @self.panel.btn_increase_max.callback()
        def OnClick(btn, touch):
            if not self.item_data:
                return
            quantity = self.item_data.get('quantity', 1)
            self.add_sub_widget.set_num(quantity)

    def destroy(self):
        self.add_sub_widget.set_num_change_callback(None)
        self.add_sub_widget.destroy()
        self.add_sub_widget = None
        self.panel = None
        self.item_data = {}
        return