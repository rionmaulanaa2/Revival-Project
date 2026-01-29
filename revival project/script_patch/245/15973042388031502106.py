# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckCharacter.py
from __future__ import absolute_import
import math3d
from common.cfg import confmgr
from logic.gcommon.component.client.com_lobby_char.ComCharacterBase import ComCharacterBase

class ComArtCheckCharacter(ComCharacterBase):

    def __init__(self):
        super(ComArtCheckCharacter, self).__init__()

    def destroy(self):
        super(ComArtCheckCharacter, self).destroy()

    def tick_filter(self):
        return True

    def on_init_complete(self):
        pass

    def init_prs(self):
        self.sd.ref_character.physicalPosition = math3d.vector(0, 300, 0)

    def tick_rotation(self):
        rotation_matrix = math3d.matrix.make_rotation_y(self._yaw)
        self.send_event('E_SET_ROTATION_MATRIX', rotation_matrix)