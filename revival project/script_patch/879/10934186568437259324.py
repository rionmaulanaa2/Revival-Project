# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/ui_distortor/MechaDistortHelper.py
from __future__ import absolute_import
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper

class MechaDistortHelper(object):
    GLOBAL_EVENT = {'switch_control_target_event': 'on_ctrl_target_changed',
       'scene_observed_player_setted_event': 'on_observed_player_setted'
       }

    def on_init_panel(self, *args, **kwargs):
        self._in_mecha_state = False
        self.on_ctrl_target_changed()

    def on_ctrl_target_changed(self, *args):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.switch_to_mecha()
        else:
            self.switch_to_non_mecha()

    def switch_to_mecha(self):
        if self._in_mecha_state:
            return
        self._in_mecha_state = True
        UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def switch_to_non_mecha(self):
        if not self._in_mecha_state:
            return
        self._in_mecha_state = False
        UIDistorterHelper().cancel_ui_distort(self.__class__.__name__)

    def in_mecha_state(self):
        return self._in_mecha_state

    def on_observed_player_setted(self, ltarget):
        self.on_ctrl_target_changed()