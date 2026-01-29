# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareInGameWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget

class ShareInGameWidget(BaseUIWidget):

    def __init__(self, panel_cls, ui_panel):
        self.global_events = {}
        super(ShareInGameWidget, self).__init__(panel_cls, ui_panel)

    def init_btn_lst(self, info_lst):
        len_info = len(info_lst)
        self.panel.list_btn.SetInitCount(len_info)
        for idx in range(len_info):
            item = self.panel.list_btn.GetItem(idx)
            ret_info, txt_id, func_cb = info_lst[idx]
            item.btn_all.data = (ret_info, func_cb)
            item.lab_name.SetString(txt_id)

            @item.btn_all.unique_callback()
            def OnClick(btn, touch):
                func_param, func = btn.data
                if func and callable(func):
                    func(func_param)