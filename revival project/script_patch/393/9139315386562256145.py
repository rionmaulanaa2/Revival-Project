# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyLeftFlexibleWidgetList.py
from __future__ import absolute_import
from common.cfg import confmgr
from .LobbyFlexibleWidgetList import LobbyFlexibleWidgetList

class LobbyLeftFlexibleWidgetList(LobbyFlexibleWidgetList):

    def __init__(self, parent_ui, panel):
        super(LobbyLeftFlexibleWidgetList, self).__init__(parent_ui, panel)

    def init_data(self):
        self.btn_list = self.panel.list_left_temp
        self.widget_list = []
        cfg = confmgr.get('activity_lobby_widget_config', default={})
        self.sorted_widget_ids = cfg.get('left_sorted_id', [])
        self.widget_cfgs = cfg.get('widget_cfgs', {})