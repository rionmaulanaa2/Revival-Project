# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyCtrl.py
from __future__ import absolute_import
from . import ScenePart
import logic.gcommon.common_const.animation_const as animation_const
from data.camera_state_const import FREE_MODEL, FIRST_PERSON_MODEL, AIM_MODE, THIRD_PERSON_MODEL, OBSERVE_FREE_MODE
from logic.client.const import camera_const
from logic.comsys.parachute_ui.ParachuteInfoUI import ParachuteInfoUI
from logic.gcommon.cdata import mecha_status_config as mecha_st_const
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.animation_const import MOVE_STATE_WALK, MOVE_STATE_RUN
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils import parachute_utils

class PartLobbyCtrl(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLobbyCtrl, self).__init__(scene, name)
        self.key_ctrls = []

    def on_enter(self):
        self.register_keys()

    def on_exit(self):
        self.unregister_keys()
        self.key_ctrls = []

    def register_keys(self):
        from .keyboard import LobbyKeyboard
        self.key_ctrls = [
         LobbyKeyboard.LobbyKeyboard()]
        for key_ctrl in self.key_ctrls:
            key_ctrl.install()
            key_ctrl.enable()

    def unregister_keys(self):
        for key_ctrl in self.key_ctrls:
            key_ctrl.disable()
            key_ctrl.uninstall()

        self.key_ctrls = []