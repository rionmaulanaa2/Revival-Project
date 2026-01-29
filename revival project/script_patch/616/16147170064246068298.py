# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckMechaMoveAppr.py
from __future__ import absolute_import
from .ComArtCheckMoveAppr import ComArtCheckMoveAppr
from logic.gcommon.common_const import lobby_ani_const
from logic.gcommon.component.client.com_lobby_char.com_lobby_appearance.ComLobbyMoveAppr import ComLobbyMoveAppr

class ComArtCheckMechaMoveAppr(ComArtCheckMoveAppr):

    def __init__(self):
        super(ComArtCheckMechaMoveAppr, self).__init__()

    def _on_animator_loaded(self):
        self.replace_move_anim()

    def on_move_stop(self, *args):
        self.on_move_state_changed()

    def on_move(self, vec):
        self.on_move_state_changed(vec)

    def _on_grounded(self):
        self.on_move_state_changed()

    def _on_end_climb(self):
        self.on_move_state_changed()

    def on_move_state_changed(self, vec=None):
        if self.ev_g_is_jump() or self.ev_g_is_climb():
            return
        else:
            if self.ev_g_is_camera_slerp():
                return
            if vec is None or vec.is_zero:
                dir_x = 0
                dir_y = 0
            else:
                dir_x = vec.x
                dir_y = vec.z
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', dir_x, dir_y)
            return

    def replace_move_anim(self):
        pass