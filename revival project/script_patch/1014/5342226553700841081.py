# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbyMovieAnim.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import world
import math3d
from logic.gcommon.common_const import lobby_ani_const

class ComLobbyMovieAnim(UnitCom):
    BIND_EVENT = {'E_ON_MOVIE_ANIM': 'on_movie_anim'
       }

    def __init__(self):
        super(ComLobbyMovieAnim, self).__init__()

    def on_movie_anim(self, parameter):
        if parameter['anim_name'] == 'mount':
            mecha_model = global_data.emgr.lobby_cur_display_mecha.emit()[0]
            model = self.ev_g_model()
            if not model:
                return
            model.remove_from_parent()
            model.position = math3d.vector(0, 0, 0)
            model.rotation_matrix = math3d.matrix()

            def end_transmit(*args):
                self.send_event('E_SET_MODEL_VISIBLE', False)

            model.register_action_key_event('hide', end_transmit)
            if mecha_model:
                mecha_model.bind('mount', model, world.BIND_TYPE_ALL)
            self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', lobby_ani_const.STATE_MOUNT)