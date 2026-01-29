# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComEventForward.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from functools import partial

class ComEventForward(UnitCom):
    BIND_EVENT = {'G_SET_FORWARD_ENTITY': '_set_forward_entity',
       'G_REGISTER_FORWARD_EVENTS': '_register_forward_event',
       'G_UNREGISTER_FORWARD_EVENTS': '_unregister_forward_event'
       }

    def __init__(self):
        super(ComEventForward, self).__init__()
        self._forward_logic = None
        self._event_map = {}
        return

    def destroy(self):
        self._forward_logic = None
        self._event_map = {}
        super(ComEventForward, self).destroy()
        return

    def _set_forward_entity(self, entity_id=None):
        self._forward_logic = None
        if entity_id:
            from mobile.common.EntityManager import EntityManager
            entity = EntityManager.getentity(entity_id)
            if entity:
                self._forward_logic = entity.logic
        return

    def _register_forward_event(self, events_name):
        regist_event = self.unit_obj.regist_event
        for event in events_name:
            if event in self._event_map:
                continue
            if event.startswith('G_'):
                func = partial(self._forward_g_event, event)
            else:
                func = partial(self._forward_event, event)
            self._event_map[event] = func
            regist_event(event, func)

    def _unregister_forward_event(self, events_name):
        unregist_event = self.unit_obj.unregist_event
        for event in events_name:
            func = self._event_map.pop(event, None)
            if func:
                unregist_event(event, func)

        return

    def _forward_event(self, event_name, *args, **kwargs):
        if not self._forward_logic:
            return
        self._forward_logic.send_event(event_name, *args, **kwargs)

    def _forward_g_event(self, event_name, *args, **kwargs):
        if not self._forward_logic or self._forward_logic is self.unit_obj:
            return None
        else:
            return self._forward_logic.get_value(event_name, *args, **kwargs)