# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/EggMarkUI.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
import common.utils.timer as timer
from common.const import uiconst
from logic.comsys.battle.SnatchEgg.EggMarkWidget import EggMarkWidget
from common.utils.ui_utils import get_scale

class EggMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'snatchegg_round_interval_event': 'snatchegg_round_interval',
       'snatchegg_round_begin_event': 'snatchegg_round_begin',
       'update_battle_data': 'on_update_battle_data'
       }

    def on_init_panel(self):
        self.regist_main_ui()
        self.init_parameters()
        self.init_mark_icon()

    def init_parameters(self):
        self.show_egg_list = []
        self.mark_widgets = []

    def on_finalize_panel(self):
        self.clear_marks()

    def clear_marks(self):
        self.show_egg_list = []
        for tmp_mark_widget in self.mark_widgets:
            tmp_mark_widget.on_finalize()

        self.mark_widgets = []

    def init_mark_icon(self):
        egg_list = global_data.battle.egg_list
        if egg_list != self.show_egg_list:
            self.clear_marks()
            self.show_egg_list = list(egg_list)
            for egg_id in egg_list:
                self.mark_widgets.append(EggMarkWidget(egg_id, self.panel))

    def refresh(self):
        if not global_data.battle:
            return
        self.init_mark_icon()

    def snatchegg_round_interval(self):
        self.refresh()

    def snatchegg_round_begin(self):
        self.refresh()

    def on_update_battle_data(self):
        self.refresh()

    def do_hide_panel(self):
        super(EggMarkUI, self).do_hide_panel()
        for tmp_mark_widget in self.mark_widgets:
            tmp_mark_widget.hide()

    def do_show_panel(self):
        super(EggMarkUI, self).do_show_panel()
        for tmp_mark_widget in self.mark_widgets:
            tmp_mark_widget.show()