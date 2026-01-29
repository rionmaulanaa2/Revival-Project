# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanLevelSettingUI.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget

class ClanLevelSettingUI(BaseUIWidget):

    def get_value(self):
        return self._apply_level_limit

    def __init__(self, panel_cls, ui_panel, level_limit, reverse=False):
        super(ClanLevelSettingUI, self).__init__(panel_cls, ui_panel)
        self._apply_level_limit = 0 if level_limit < 0 else level_limit
        self._reverse = reverse
        self._init_panel()

    def _init_panel(self):

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.reverse_list_show()

        self.panel.level_list.setVisible(False)
        self.panel.img_icon.setScaleY(1)
        level_limit = [{'name': 860018,'val': 0}, {'name': 'Lv 5','val': 5}, {'name': 'Lv 10','val': 10}, {'name': 'Lv 20','val': 20}, {'name': 'Lv 40','val': 40}]
        if self._apply_level_limit > 0:
            self.panel.SetText('Lv {}'.format(self._apply_level_limit))
        else:
            self.panel.SetText(860018)

        def callback(index):
            info = level_limit[index]
            self._apply_level_limit = info['val']
            self.panel.SetText(info['name'])
            if self.panel.level_list.isVisible():
                self.reverse_list_show()

        def close_cb(*args):
            self.panel.img_icon.setScaleY(1)

        from logic.gutils.template_utils import init_common_choose_list
        init_common_choose_list(self.panel.level_list, level_limit, callback, max_height=350, close_cb=close_cb, reverse=self._reverse)

    def reverse_list_show(self):
        now_vis = self.panel.level_list.isVisible()
        self.panel.level_list.setVisible(not now_vis)
        self.panel.img_icon.setScaleY(1 if now_vis else -1)