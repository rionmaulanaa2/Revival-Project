# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETopTipsUI.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import TOP_ZORDER, UI_VKB_NO_EFFECT
from .PVEBlessDonateTipsWidget import PVEBlessDonateTipsWidget
from .PVERightTipsWidget import PVERightTipsWidget
from .PVETeamTeleportWidget import PVETeamTeleportWidget
from common.uisys.basepanel import BasePanel

class PVETopTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/info/i_info_empty'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    HOT_KEY_FUNC_MAP = {'pve_team_teleport': 'keyborad_team_teleport'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVETopTipsUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.process_events(True)
        self.init_bless_donate_tips_widget()
        self.init_right_tips_widget()
        self.init_team_teleport_widget()

    def init_params(self):
        self.bless_donate_tips_widget = None
        self.right_tips_widget = None
        self.team_teleport_widget = None
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.clear_all()
        self.process_events(False)
        self.init_params()
        self.destroy_widget('bless_donate_tips_widget')
        self.destroy_widget('right_tips_widget')
        self.destroy_widget('team_teleport_widget')
        super(PVETopTipsUI, self).on_finalize_panel()

    def clear_all(self):
        self.bless_donate_tips_widget and self.bless_donate_tips_widget.clear()
        self.right_tips_widget and self.right_tips_widget.clear()
        self.team_teleport_widget and self.team_teleport_widget.clear()

    def init_bless_donate_tips_widget(self):
        self.bless_donate_tips_widget = PVEBlessDonateTipsWidget(self.panel)

    def init_right_tips_widget(self):
        self.right_tips_widget = PVERightTipsWidget(self.panel)

    def init_team_teleport_widget(self):
        self.team_teleport_widget = PVETeamTeleportWidget(self.panel)

    def keyborad_team_teleport(self, msg, keycode):
        if self.team_teleport_widget and self.team_teleport_widget.is_showing():
            self.team_teleport_widget.on_click_confirm()