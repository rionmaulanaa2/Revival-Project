# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8036LockedUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaAutoAimWidget import MechaAutoAimWidget

class Mecha8036LockedUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8036_2'
    WEAPON_INFO = {}

    def on_init_panel(self, *args, **kwargs):
        super(Mecha8036LockedUI, self).on_init_panel()
        self.init_auto_aim_widget()

    def init_parameters(self):
        super(Mecha8036LockedUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        pass

    def init_bullet_widget(self):
        pass

    def init_auto_aim_widget(self):
        self.auto_aim_widget = MechaAutoAimWidget(self.panel)

    def on_finalize_panel(self):
        super(Mecha8036LockedUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
        self.mecha = None
        return

    def enable_weapon_aim_helper(self, enabled, weapon_pos):
        if enabled and self.auto_aim_widget.refresh_auto_aim_range_appearance(weapon_pos, set_size_directly=True, size_offset=0.0, use_center_scale=True):
            self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
            self.auto_aim_widget.show()
            self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
        else:
            self.auto_aim_widget.hide()
            self.auto_aim_widget.update_aim_target(None, weapon_pos)
        return