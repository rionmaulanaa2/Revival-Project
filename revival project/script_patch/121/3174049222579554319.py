# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFABeginCountDown.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst
from logic.comsys.battle.ffa.FFABeginCountDownWidget import FFABeginCountDownWidget

class FFABeginCountDown(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_ffa/battle_begin_time'

    def on_init_panel(self):
        self._widget = FFABeginCountDownWidget(self._get_root_node())
        self._widget.on_init_panel()

    def on_finalize_panel(self):
        self._widget.on_finalize_panel()
        self._widget = None
        return

    def _get_root_node(self):
        return self.panel

    def set_context(self, context):
        return self._widget.set_context(context)

    def get_context(self):
        return self._widget.get_context()

    def on_delay_close(self, revive_time, callback=None):
        return self._widget.on_delay_close(revive_time, callback)

    def set_start_show_time(self, show_time):
        self._widget.set_start_show_time(show_time)

    def set_count_down_sound(self, sound):
        self._widget.set_count_down_sound(sound)

    def set_time_need_ceil(self, need_ceil):
        self._widget.set_time_need_ceil(need_ceil)