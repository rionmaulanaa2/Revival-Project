# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRoleHead.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Int
from logic.gcommon.cdata.default_head_photo_url import get_head_photo_url
import logic.gcommon.time_utility as tutil

class impRoleHead(object):

    def _init_rolehead_from_dict(self, bdict):
        self.head_picture = None
        self.head_frame = bdict.get('head_frame') or 0
        self.head_photo = bdict.get('head_photo') or 0
        return

    def _on_login_rolehead_success(self):
        self.dress_head_frame(self.head_frame, False)
        self.update_head_photo(self.head_photo, False)
        if self.head_photo == 30200018:
            self.update_head_photo(30200011, True)

    def get_head_frame(self):
        return self.head_frame

    def get_head_photo(self):
        return self.head_photo

    def get_head_photo_url(self):
        return get_head_photo_url(self.head_photo)

    @rpc_method(CLIENT_STUB, (Int('item_no'),))
    def reset_role_head(self, item_no):
        self.dress_head_frame(item_no, False)

    def dress_head_frame(self, item_no, sync):
        self.head_frame = item_no
        global_data.emgr.player_info_update_event.emit()
        if global_data.message_data:
            global_data.message_data.set_player_role_head_info({self.uid: (tutil.get_server_time(), self.head_frame, self.head_photo)}, False, False)
        global_data.emgr.message_on_player_role_head.emit({self.uid: self.head_frame})
        if sync:
            self.call_server_method('dress_head_frame', {'item_no': item_no})

    @rpc_method(CLIENT_STUB, (Int('photo_no'),))
    def reset_role_head_photo(self, photo_no):
        self.update_head_photo(photo_no, False)

    def update_head_photo(self, photo_no, sync):
        self.head_photo = photo_no
        global_data.emgr.player_info_update_event.emit()
        if global_data.message_data:
            global_data.message_data.set_player_role_head_info({self.uid: (tutil.get_server_time(), self.head_frame, self.head_photo)}, False, False)
        global_data.emgr.message_on_player_role_head_photo.emit({self.uid: self.head_photo})
        if sync:
            self.call_server_method('update_head_photo', {'photo_no': photo_no})