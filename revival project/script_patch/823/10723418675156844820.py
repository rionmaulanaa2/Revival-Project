# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/IntimacyList.py
from __future__ import absolute_import
from logic.comsys.intimacy.IntimacyPanel import IntimacyPanel
from common.const.property_const import U_ID

class IntimacyList(object):

    def __init__(self, main_panel, **kwargs):
        self.panel = panel_temp = global_data.uisystem.load_template_create('friend/i_intimacy_main', main_panel.panel, name='intimacy_content')
        panel_temp.SetPosition('50%', '50%')
        self.panel_widget = IntimacyPanel(self.panel)
        self.panel_widget.set_player_inf({U_ID: global_data.player.uid})

    def set_visible(self, flag):
        self.panel.setVisible(flag)
        if flag:
            self.panel_widget.show_msg()

    def destroy(self):
        self.panel_widget.destroy()