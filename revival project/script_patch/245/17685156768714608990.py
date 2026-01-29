# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CSnipeMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_AIM_SHOOT
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock

class CSnipeMode(CDeathMode):
    FORBIDDEN_ACTIONS = ('action1', 'action2', 'action3')

    def __init__(self, map_id):
        super(CSnipeMode, self).__init__(map_id)

    def process_event(self, is_bind):
        super(CSnipeMode, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'mecha_control_main_ui_event': self._forbid_main_weapon,
           'mecha_switch_action': self._on_mecha_switch_action,
           'on_init_mecha_ui': self._hide_mecha_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def is_need_weapon_ui(self):
        return False

    def _hide_mecha_ui(self):
        global_data.ui_mgr.hide_ui('MechaUI')

    def _forbid_main_weapon(self):
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not ui:
            return
        for action in self.FORBIDDEN_ACTIONS:
            ui.on_set_action_forbidden(action, True)

    def _on_mecha_switch_action(self, action, state_id):
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not ui:
            return
        if state_id == MC_SHOOT:
            for act in self.FORBIDDEN_ACTIONS:
                ui.on_set_action_forbidden(act, True)
                bar = ui.action_btns[act].nd.bar
                bar.SetEnableTouch(False)
                t = TouchMock()
                bar.OnCancel(t)
                bar.SetEnableTouch(True)