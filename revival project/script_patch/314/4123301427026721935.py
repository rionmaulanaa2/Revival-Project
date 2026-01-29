# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComLobbyPlayerReceiver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common import utilities
import math3d

class ComLobbyPlayerReceiver(UnitCom):

    def init_from_dict(self, unit_obj, bdict):
        super(ComLobbyPlayerReceiver, self).init_from_dict(unit_obj, bdict)
        self.init_global_event()

    def init_global_event(self):
        emgr = global_data.emgr
        emgr.trigger_lobby_player_move += (self.trigger_lobby_player_move,)
        emgr.trigger_lobby_player_move_stop += (self.trigger_lobby_player_move_stop,)
        emgr.trigger_lobby_player_set_yaw += (self.trigger_lobby_player_set_yaw,)
        emgr.movie_model_set += self.on_movie_model_set
        emgr.movie_start += self.on_movie_start
        emgr.movie_model_anim += self.on_movie_model_anim
        emgr.movie_model_hidden += self.on_movie_model_hidden
        emgr.movie_model_showed += self.on_movie_model_showed
        emgr.enable_lobby_player_free_cam += self.enable_lobby_player_free_cam
        emgr.role_fashion_chagne += self.on_role_fashion_change

    def trigger_lobby_player_move(self, vec):
        import math3d
        norm_v = math3d.vector(vec)
        if not norm_v.is_zero:
            norm_v.normalize()
        if self.ev_g_is_celebrate():
            self.send_event('E_LOBBY_CELEBRATE_BREAK')
        self.send_event('E_MOVE', norm_v)

    def trigger_lobby_player_move_stop(self):
        self.send_event('E_MOVE_STOP')

    def trigger_lobby_player_set_yaw(self, yaw):
        self.send_event('E_SET_YAW', yaw)

    def enable_lobby_player_free_cam(self, enable):
        self.send_event('E_ENABLE_FREE_CAMERA', enable)
        if not enable:
            global_data.emgr.reset_lobby_camera_from_free.emit()

    def on_movie_model_set(self, parameter):
        if parameter.get('tag', '') == 'lobby_character':
            self.send_event('E_SET_POSITION', math3d.vector(*parameter['position']))
            self.send_event('E_SET_YAW', utilities.euler_to_matrix(parameter['rotation']).yaw)

    def on_movie_model_anim(self, parameter):
        if parameter.get('tag', '') == 'lobby_character':
            self.send_event('E_ON_MOVIE_ANIM', parameter)

    def on_movie_start(self):
        self.send_event('E_ON_LOBBY_MOVIE_START')

    def on_movie_model_hidden(self, parameter):
        if parameter.get('tag', '') == 'lobby_character':
            self.send_event('E_SET_MODEL_VISIBLE', False)

    def on_movie_model_showed(self, parameter):
        if parameter.get('tag', '') == 'lobby_character':
            self.send_event('E_SET_MODEL_VISIBLE', True)

    def on_role_fashion_change(self, *args):
        self.send_event('E_REFRESH_LOBBY_PLAYER_MODEL')