# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impClothing.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict
from logic.gcommon.item import item_const as iconst

class impClothing(object):

    def _init_clothing_from_dict(self, bdict):
        self.clothing_dict = bdict.get('clothing_dict', {})

    def dress_clothing(self, clothing_dict):
        dress_clothing_dict = {}
        for part, item_no in six.iteritems(clothing_dict):
            if part not in iconst.CLOTHING_DRESS_PARTS:
                continue
            dress_clothing_dict[part] = item_no
            self.clothing_dict[part] = item_no

        self.call_server_method('dress_clothing', (dress_clothing_dict,))
        global_data.emgr.player_dress_update_event.emit(six_ex.keys(dress_clothing_dict))
        return dress_clothing_dict

    def undress_clothing(self, clothing_parts):
        undress_clothing_parts = []
        for part in clothing_parts:
            if part in self.clothing_dict:
                del self.clothing_dict[part]
                undress_clothing_parts.append(part)

        if undress_clothing_parts:
            self.call_server_method('undress_clothing', (undress_clothing_parts,))
            global_data.emgr.player_dress_update_event.emit(undress_clothing_parts)
        return undress_clothing_parts

    def get_clothing(self):
        return self.clothing_dict

    def get_clothing_by_part_id(self, part_id):
        return self.clothing_dict.get(str(part_id), None)

    @rpc_method(CLIENT_STUB, (Dict('clothing_dict'),))
    def reset_clothing(self, clothing_dict):
        clothing_parts = six_ex.keys(self.clothing_dict)
        self.clothing_dict = clothing_dict
        global_data.emgr.player_dress_update_event.emit(clothing_parts)