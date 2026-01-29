# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAvatarEvent2GlobalEvent.py
from __future__ import absolute_import
from ..UnitCom import UnitCom

class ComAvatarEvent2GlobalEvent(UnitCom):
    BIND_EVENT = {'E_REGISTER_A2G_EVENT': '_register_avatar_event',
       'E_UNREGISTER_A2G_EVENT': '_unregister_avatar_event'
       }

    def __init__(self):
        super(ComAvatarEvent2GlobalEvent, self).__init__()
        self._event_map = {}
        self.dy_handler = {}

    def _unregister_avatar_event(self, avatar_event, global_event):
        emap = self._event_map
        if avatar_event not in emap:
            return
        elist = self._event_map[avatar_event]
        if global_event in elist:
            elist.remove(global_event)
        if not elist:
            self.clean_event(avatar_event)
            del emap[avatar_event]

    def _register_avatar_event(self, avatar_event, global_event):
        emap = self._event_map
        if avatar_event in emap:
            if global_event not in emap[avatar_event]:
                emap[avatar_event].append(global_event)
        else:
            from functools import partial
            emap[avatar_event] = [
             global_event]
            unit_obj = self.unit_obj
            func = partial(self.notify, avatar_event)
            self.dy_handler[avatar_event] = func
            unit_obj.regist_event(avatar_event, func)

    def clean_event(self, ename):
        if ename in self.dy_handler:
            handler = self.dy_handler[ename]
            del self.dy_handler[ename]
            unit_obj = self.unit_obj
            unit_obj.unregist_event(ename, handler)

    def notify(self, ename, *arg, **kwarg):
        elist = self._event_map.get(ename)
        if not elist:
            self.clean_event(ename)
        else:
            for event in elist:
                global_data.emgr.fireEvent(event, *arg, **kwarg)