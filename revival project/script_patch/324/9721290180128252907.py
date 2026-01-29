# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impHouseSys.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Int
from logic.gcommon.time_utility import get_time
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
from logic.gcommon.item.item_const import DEFAULT_LOBBY_SKIN, DEFAULT_LOBBY_SKYBOX

class impHouseSys(object):

    def _init_housesys_from_dict(self, bdict):
        self._wall_picture = bdict.get('wall_picture', 0)
        self._lobby_bgm = bdict.get('lobby_bgm', 0)
        self._lobby_skin_id = bdict.get('lobby_skin_id', 0)
        self._lobby_skybox_id = bdict.get('lobby_skybox_id', 0)

    def get_wall_picture(self):
        return self._wall_picture

    @rpc_method(CLIENT_STUB, (Int('picture_no'),))
    def reset_wall_picture(self, picture_no):
        self.select_wall_picture(picture_no, False)

    def select_wall_picture(self, picture_no, sync=True):
        if picture_no == self._wall_picture:
            return
        self._wall_picture = picture_no
        global_data.emgr.housesys_wall_picture_change.emit()
        global_data.emgr.housesys_wall_picture_change_success.emit()
        if sync:
            self.call_server_method('lobby_select_wall_picture', {'picture_no': picture_no})

    def select_lobby_bgm(self, bgm_id):
        if bgm_id == self._lobby_bgm:
            return
        self.call_server_method('lobby_select_bgm', (bgm_id,))
        self._lobby_bgm = bgm_id
        global_data.emgr.lobby_bgm_change.emit(-1)
        global_data.emgr.lobby_bgm_change_success.emit()

    def default_lobby_bgm(self):
        from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
        self.select_lobby_bgm(DEFAULT_LOBBY_BGM)

    @rpc_method(CLIENT_STUB, (Int('bgm_id'),))
    def reset_lobby_bgm(self, bgm_id):
        self._lobby_bgm = bgm_id
        global_data.emgr.lobby_bgm_change.emit(-1)
        global_data.emgr.lobby_bgm_change_success.emit()

    def get_lobby_bgm(self):
        return self._lobby_bgm

    def change_lobby_skin(self, skin_id):
        if self._lobby_skin_id == skin_id:
            return
        if str(skin_id) == str(DEFAULT_LOBBY_SKIN):
            skin_id = 0
        self.call_server_method('lobby_select_skin', (skin_id,))
        self._lobby_skin_id = skin_id
        global_data.emgr.miaomiao_lobby_skin_change.emit(-1)
        global_data.emgr.miaomiao_lobby_skin_change_success.emit()

    @rpc_method(CLIENT_STUB, (Int('skin_id'),))
    def reset_lobby_skin(self, skin_id):
        self._lobby_skin_id = skin_id
        global_data.emgr.miaomiao_lobby_skin_change.emit(-1)
        global_data.emgr.miaomiao_lobby_skin_change_success.emit()

    def get_lobby_skin(self):
        if self._lobby_skin_id not in (0, -1):
            return self._lobby_skin_id
        return DEFAULT_LOBBY_SKIN

    @rpc_method(CLIENT_STUB, (Int('skybox_id'),))
    def reset_lobby_skybox(self, skybox_id):
        self._lobby_skybox_id = skybox_id
        global_data.emgr.privilege_lobby_skin_change.emit()

    def change_lobby_skybox(self, skybox_id):
        if self._lobby_skybox_id == skybox_id:
            return
        if str(skybox_id) == str(DEFAULT_LOBBY_SKYBOX):
            skybox_id = -1
        self._lobby_skybox_id = skybox_id
        self.call_server_method('lobby_select_skybox', (skybox_id,))
        global_data.emgr.privilege_lobby_skin_change.emit()

    def get_lobby_skybox_id(self):
        if self._lobby_skybox_id not in (0, -1):
            return self._lobby_skybox_id
        return DEFAULT_LOBBY_SKYBOX