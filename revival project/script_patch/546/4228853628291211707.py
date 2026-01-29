# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombDeviceBloodUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from logic.comsys.battle.ADCrystal.ADCrystalLocateWidget import ADCrystalLocateWidget
from logic.comsys.battle.NBomb.NBombBattleDefines import NBOMB_DEVICE_BLOOD_BLUE, NBOMB_DEVICE_BLOOD_RED
WIDGET_TYPE_TO_TEMPLATE = {NBOMB_DEVICE_BLOOD_BLUE: 'battle_crystal/i_crystal_mark_blue',
   NBOMB_DEVICE_BLOOD_RED: 'battle_crystal/i_crystal_mark_red'
   }

class NBombDeviceBloodUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.locate_widget = None
        return

    def on_finalize_panel(self):
        self.locate_widget and self.locate_widget.destroy()
        self.locate_widget = None
        return

    def add_locate_widget(self, widget_type, position):
        if self.locate_widget:
            self.locate_widget.destroy()
            self.locate_widget = None
        template = WIDGET_TYPE_TO_TEMPLATE.get(widget_type)
        self.locate_widget = ADCrystalLocateWidget(template, position)
        if not self.locate_widget:
            return
        else:
            self.panel.AddChild('', self.locate_widget.node)
            if global_data.aim_transparent_mgr:
                global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.locate_widget.node])
            return

    def on_update_crystal_hp(self, hp_ratio):
        self.locate_widget and self.locate_widget.on_update_crystal_hp(hp_ratio)

    def set_icon(self, icon_path):
        self.locate_widget and self.locate_widget.set_icon(icon_path)