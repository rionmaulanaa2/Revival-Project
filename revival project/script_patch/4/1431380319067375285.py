# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impGameSprite.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
import game3d

class impGameSprite(object):

    def init_game_sprite_from_dict(self, bdict):
        self._game_sprite_url = bdict.get('game_sprite_url', None)
        self._game_sprite_token = None
        return

    def open_game_sprite_url(self):
        if self._game_sprite_url is not None:
            if self._game_sprite_token is not None:
                url = self._game_sprite_url + self._game_sprite_token
                game3d.open_url(url)
            else:
                self.get_game_sprite_token()
        return

    def get_game_sprite_token(self):
        self.call_server_method('get_game_sprite_token', {})

    @rpc_method(CLIENT_STUB, (Str('game_sprite_url'),))
    def update_game_sprite_url(self, game_sprite_url):
        self.update_game_sprite_url_imp(game_sprite_url)

    def update_game_sprite_url_imp(self, game_sprite_url):
        self._game_sprite_url = game_sprite_url
        self._game_sprite_token = None
        return

    @rpc_method(CLIENT_STUB, (Str('token'),))
    def get_game_sprite_token_result(self, token):
        self.get_game_sprite_token_result_imp(token)

    def get_game_sprite_token_result_imp(self, token):
        self._game_sprite_token = token
        self.open_game_sprite_url()