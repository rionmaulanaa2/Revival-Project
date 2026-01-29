# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanDanSettingWidget.py
from __future__ import absolute_import
import six_ex
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.cdata import dan_data

class ClanDanSettingWidget(BaseUIWidget):

    def get_value(self):
        return self._apply_dan_limit

    def __init__(self, panel_cls, ui_panel, dan_limit, reverse=False):
        super(ClanDanSettingWidget, self).__init__(panel_cls, ui_panel)
        self._apply_dan_limit = dan_limit
        self._reverse = reverse
        self._init_panel()

    def _init_panel(self):

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.reverse_list_show()

        self.panel.tier_list.setVisible(False)
        self.panel.img_icon.setScaleY(1)
        dan_limit_name = dan_data.data.get(self._apply_dan_limit, {}).get('name', 860017)
        self.panel.SetText(dan_limit_name)
        dan_lst = six_ex.keys(dan_data.data)
        dan_lst.sort()
        dan_limit = [ {'name': dan_data.data[dan]['name'],'val': dan} for dan in dan_lst ]

        def callback(index):
            info = dan_limit[index]
            self._apply_dan_limit = info['val']
            self.panel.SetText(info['name'], font_name=info.get('font', None))
            if self.panel.tier_list.isVisible():
                self.reverse_list_show()
            return

        def close_cb(*args):
            self.panel.img_icon.setScaleY(1)

        from logic.gutils.template_utils import init_common_choose_list
        init_common_choose_list(self.panel.tier_list, dan_limit, callback, max_height=350, close_cb=close_cb, reverse=self._reverse)

    def reverse_list_show(self):
        now_vis = self.panel.tier_list.isVisible()
        self.panel.tier_list.setVisible(not now_vis)
        self.panel.img_icon.setScaleY(1 if now_vis else -1)