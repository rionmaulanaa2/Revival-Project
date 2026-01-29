# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveMirrativPageWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.observe_utils import LiveObserveUIHelper, goto_spectate_player

class LiveMirrativPageWidget(object):

    def __init__(self, parent_panel, list_type):
        self._parent_panel = parent_panel
        self._list_type = list_type

    def on_finalize_panel(self):
        self._parent_panel = None
        self._list_type = None
        return

    def init_parameters(self):
        pass

    def get_spectate_type(self):
        return self._list_type

    def set_other_spectate_type(self, other_list_type):
        pass

    def get_other_spectate_type(self):
        return None

    def refresh_content_with_brief(self, refresh_ui=False):
        pass

    def get_real_content_size(self):
        return 2

    def init_panel(self):
        import game3d

        @self._parent_panel.temp_mirrativ.temp_record.btn_bar.unique_callback()
        def OnClick(*args):
            url = 'https://ws9f.adj.st//broadcast/live?adjust_t=wils1a7_r3790e2&adjust_deeplink=mirr%3A%2F%2F%2Fbroadcast%2Flive%3Fapp_id%3Dcom.netease.g93na&app_id=com.netease.g93na'
            game3d.open_url(url)

        @self._parent_panel.temp_mirrativ.temp_observe.btn_bar.unique_callback()
        def OnClick(*args):
            url = 'https://ws9f.adj.st//app/com.netease.g93na?adjust_t=wils1a7_r3790e2&adjust_deeplink=mirr:///app/com.netease.g93na'
            game3d.open_url(url)

    def show_panel(self):
        self._parent_panel.temp_mirrativ.setVisible(True)

    def hide_panel(self):
        self._parent_panel.temp_mirrativ.setVisible(False)