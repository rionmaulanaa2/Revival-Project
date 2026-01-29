# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComCharacterLobby.py
from __future__ import absolute_import
import math3d
from common.cfg import confmgr
from logic.gcommon.component.client.com_lobby_char.ComCharacterBase import ComCharacterBase

class ComCharacterLobby(ComCharacterBase):
    BIND_EVENT = ComCharacterBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_LOBBY_MOVIE_START': 'on_lobby_movie_start',
       'G_CHAR_WAITING': '_get_char_waiting'
       })

    def __init__(self):
        super(ComCharacterLobby, self).__init__()

    def destroy(self):
        super(ComCharacterLobby, self).destroy()

    def tick_filter(self):
        if self.get_value('G_MOUNTING'):
            return False
        return True

    def on_init_complete(self):
        global_data.emgr.on_lobby_player_char_inited.emit()

    def init_prs(self):
        # Override position from lobby config (called by _init_character after physics setup)
        pos = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character')
        self.sd.ref_character.physicalPosition = math3d.vector(pos['x'], pos['y'], pos['z'])
        self._yaw = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character', 'yaw')

    def _get_rotation_matrix(self):
        if getattr(global_data, 'lobby_model_rotation', None) is None:
            return super(ComCharacterLobby, self)._get_rotation_matrix()
        else:
            rot = global_data.lobby_model_rotation
            global_data.lobby_model_rotation = None
            return rot
            return

    def _get_char_waiting(self):
        return False