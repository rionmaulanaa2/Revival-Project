# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MotorcycleAimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
import cc
import math
from logic.comsys.mecha_ui.Mecha8501AimUI import Mecha8501AimUI
NO_WEAPON_SEAT_INDEX = 2

class MotorcycleAimUI(Mecha8501AimUI):

    def on_init_panel(self):
        super(MotorcycleAimUI, self).on_init_panel()
        self.owner = None
        return

    def init_parameters(self):
        super(MotorcycleAimUI, self).init_parameters()
        self.seat_index = -1

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.seat_index = mecha.ev_g_passenger_seat_index(self.player.id)
            seat_name = mecha.ev_g_passenger_seat(self.player.id)
            seat_logic = mecha.ev_g_seat_logic(seat_name)
            self.mecha = seat_logic
            regist_func = seat_logic.regist_event
            regist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            regist_func('E_AIM_SPREAD', self._on_aim_spread)
            regist_func('E_RELOADING', self.on_reload_bullet)
            owner_regist_func = mecha.regist_event
            owner_regist_func('E_STAND', self._on_spread, 1)
            owner_regist_func('E_JUMP', self._on_spread, 1)
            owner_regist_func('E_MECHA_ON_GROUND', self._on_spread, 1)
            owner_regist_func('E_ACTION_MOVE', self._on_spread, 1)
            owner_regist_func('E_ACTION_MOVE_STOP', self._on_spread, 1)
            self.init_event()
            self._on_spread()
            if self._aimColorWidget:
                self._aimColorWidget.setup_color()

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            unregist_func('E_AIM_SPREAD', self._on_aim_spread)
            unregist_func('E_RELOADING', self.on_reload_bullet)
            owner = self.mecha.ev_g_owner()
            owner_unregist_func = owner.unregist_event
            owner_unregist_func('E_STAND', self._on_spread)
            owner_unregist_func('E_JUMP', self._on_spread)
            owner_unregist_func('E_MECHA_ON_GROUND', self._on_spread)
            owner_unregist_func('E_ACTION_MOVE', self._on_spread)
            owner_unregist_func('E_ACTION_MOVE_STOP', self._on_spread)
        self.mecha = None
        return

    def _on_spread(self, *args):
        if NO_WEAPON_SEAT_INDEX == self.seat_index:
            return
        super(MotorcycleAimUI, self)._on_spread(*args)

    def on_reload_bullet(self, reload_time, times, *args):
        global_data.emgr.on_reload_bullet_event.emit(reload_time, times)