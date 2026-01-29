# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impSunshineEdit.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict
from logic.gutils.sunshine_utils import execute_in_sunshine

class impSunshineEdit(object):

    def _init_sunshineedit_from_dict(self, bdict):
        pass

    def _init_sunshineedit_completed(self, bdict):
        pass

    def _tick_sunshineedit(self, delta):
        pass

    def _destroy_sunshineedit(self, clear_cache):
        pass

    @rpc_method(CLIENT_STUB, (Str('node_id'), Str('event_name'), Dict('event_args')))
    def on_storyline_debug_event(self, node_id, event_name, event_args):
        from sunshine.Editor.Plugin.GalaxyPlugin import GalaxyPlugin
        GalaxyPlugin().Server.PushGraphDebugEvent(node_id, event_name, event_args)

    @execute_in_sunshine()
    def remote_create_entity(self, npc_id, ent_type, npc_pos, ent_data=None):
        if ent_data is None:
            ent_data = {}
        self.call_soul_method('remote_create_entity', (npc_id, ent_type, npc_pos, ent_data))
        return

    @execute_in_sunshine()
    def remote_del_entity(self, entity_id):
        self.call_soul_method('remote_del_entity', (entity_id,))

    @execute_in_sunshine()
    def remote_event(self, entity_id, event, args):
        self.call_soul_method('remote_event', (entity_id, event, args))