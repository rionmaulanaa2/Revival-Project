# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impPveDropItemMgr.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, List, Dict, Bool, Float, Tuple, Uuid
from logic.gcommon.item.item_const import ITEM_DROP_ANIM_BOX
from mobile.common.IdManager import IdManager
import six
import six_ex

class impPveDropItemMgr(object):

    def _init_pvedropitemmgr_from_dict(self, bdict):
        self.drop_item = bdict.get('drop_item', {})
        self.drop_item_key = six_ex.keys(self.drop_item)
        self.now_item_id = set()
        self.refresh_item_timer = None
        if self.drop_item_key:
            self.refresh_item_timer = global_data.game_mgr.register_logic_timer(self.refresh_item, 1)
        return

    def _destroy_pvedropitemmgr(self, clear_cache):
        self.reset_refresh_timer()
        self.drop_item = None
        self.drop_item_key = None
        return

    def refresh_item(self):
        if not self.drop_item_key:
            self.reset_refresh_timer()
            return
        entity_id = self.drop_item_key.pop(0)
        if entity_id not in self.drop_item:
            self.reset_refresh_timer()
            return
        item_data = self.drop_item[entity_id]
        self.do_pve_drop_item(entity_id, item_data)

    def reset_refresh_timer(self):
        if self.refresh_item_timer:
            global_data.game_mgr.unregister_logic_timer(self.refresh_item_timer)
            self.refresh_item_timer = None
        return

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Dict('item_data')))
    def pve_drop_item(self, entity_id, item_data):
        self.drop_item[entity_id] = item_data
        self.do_pve_drop_item(entity_id, item_data, show_sfx=True)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'),))
    def pve_remove_item(self, entity_id):
        if entity_id in self.drop_item_key:
            self.drop_item_key.remove(entity_id)
        self.drop_item.pop(entity_id, None)
        global_data.battle.destroy_entity(entity_id)
        self.now_item_id.discard(entity_id)
        return

    @rpc_method(CLIENT_STUB, (Dict('drop_item'),))
    def reset_drop_item(self, drop_item):
        for entity_id in self.now_item_id:
            global_data.battle.destroy_entity(entity_id)

        self.drop_item = drop_item
        self.drop_item_key = six_ex.keys(self.drop_item)
        self.now_item_id = set()
        self.reset_refresh_timer()
        if self.drop_item_key:
            self.refresh_item_timer = global_data.game_mgr.register_logic_timer(self.refresh_item, 1)

    def do_pve_drop_item(self, entity_id, item_data, show_sfx=False):
        if show_sfx:
            item_data['show_sfx'] = ITEM_DROP_ANIM_BOX
        global_data.battle.create_entity('Item', entity_id, -1, item_data)
        self.now_item_id.add(entity_id)