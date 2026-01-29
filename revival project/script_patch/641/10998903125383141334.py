# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComPuppetTeamateTips.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.comsys.battle.TeammateWidget.LobbyTeammateTipUI import LobbyTeammateTipUI

class ComPuppetTeamateTips(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_animator_loaded',
       'E_ON_LOBBYPUPPET_DATA_CHANGE': 'on_puppet_data_update'
       }

    def __init__(self):
        super(ComPuppetTeamateTips, self).__init__()

    def destroy(self):
        self.clear_tips_ui()
        super(ComPuppetTeamateTips, self).destroy()

    def on_animator_loaded(self):
        self.update_tips_ui()

    def update_tips_ui(self):
        user_data = self.ev_g_lobby_user_data()
        LobbyTeammateTipUI.cls_update_tips(self.unit_obj, user_data)

    def clear_tips_ui(self):
        LobbyTeammateTipUI.cls_destroy_ui(self.unit_obj)

    def on_puppet_data_update(self):
        self.update_tips_ui()