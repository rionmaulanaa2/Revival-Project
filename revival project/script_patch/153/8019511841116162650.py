# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/mecha_memory/MechaMemorySimpleUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_NO_EFFECT
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gutils.mecha_career_utils import MechaMemoryStatWidget

class MechaMemorySimpleUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/career/open_mech_career_data'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {}
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.mecha_type = None
        self.memory_widget = MechaMemoryStatWidget()
        self.memory_widget.set_node(self.panel.list_lab, self.panel.list_btn)
        return

    def on_finalize_panel(self):
        super(MechaMemorySimpleUI, self).on_finalize_panel()
        if self.memory_widget:
            self.memory_widget.destroy()
            self.memory_widget = None
        return

    def on_switch_to_mecha_type(self, uid, mecha_type):
        if self.mecha_type == mecha_type:
            return
        self.mecha_type = mecha_type
        if not self.mecha_type:
            return
        from logic.gutils import item_utils
        mecha_name = item_utils.get_mecha_name_by_id(self.mecha_type)
        name = get_text_by_id(83256, {'name': mecha_name})
        self.panel.lab_title.SetString(name)
        if self.memory_widget:
            self.memory_widget.set_uid(uid)
            self.memory_widget.set_mecha_type(self.mecha_type)
            self.memory_widget.on_need_show_show_battle_season_id(global_data.player.get_battle_season())
            self.memory_widget.refresh()

    def show_mecha_memory_simple_info(self, uid, mecha_type):
        self.on_switch_to_mecha_type(uid, mecha_type)

    def set_position(self, wpos):
        lpos = self.panel.getParent().convertToNodeSpace(wpos)
        self.panel.setPosition(lpos)