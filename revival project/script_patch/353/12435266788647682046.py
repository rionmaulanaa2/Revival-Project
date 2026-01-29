# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComObserverGlobalSenderBase.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from common.framework import Functor

class DirectForwardingHelper(object):

    def __init__(self, dir_forwarding_events_dict, unit_obj):
        self.dir_forwarding_events_dict = dir_forwarding_events_dict
        self.unit_obj = unit_obj
        self._bind_direct_forward_event(dir_forwarding_events_dict)

    def direct_forwarding_func(self, global_event_name, *args, **kwargs):
        global_data.emgr.fireEvent(global_event_name, *args, **kwargs)

    def _bind_direct_forward_event(self, einfo):
        regist_event = self.unit_obj.regist_event
        for key, event_name in six.iteritems(einfo):
            priority = 0
            if isinstance(event_name, (tuple, list)):
                event_name, priority = event_name
            func = self.add_direct_event_func(event_name)
            regist_event(key, func, priority)

    def get_direct_event_func_name(self, global_event_name):
        func_name = '_dir_forward_' + global_event_name
        return func_name

    def add_direct_event_func(self, global_event_name):
        func_name = self.get_direct_event_func_name(global_event_name)
        if not hasattr(self, func_name):
            func = Functor(self.direct_forwarding_func, global_event_name)
            setattr(self, func_name, func)
        return getattr(self, func_name)

    def _unbind_direct_forward_event(self, einfo):
        if not self.unit_obj:
            return
        else:
            unregist_event = self.unit_obj.unregist_event
            for key, event_name in six.iteritems(einfo):
                if isinstance(event_name, (tuple, list)):
                    event_name, priority = event_name
                func_name = self.get_direct_event_func_name(event_name)
                func = getattr(self, func_name, None)
                if not func:
                    continue
                unregist_event(key, func)

            return

    def destroy(self):
        if self.unit_obj and self.unit_obj._is_valid:
            self._unbind_direct_forward_event(self.dir_forwarding_events_dict)
        self.__dict__.clear()
        self.unit_obj = None
        return


class ComObserverGlobalSenderBase(UnitCom):
    BIND_EVENT = {}
    DIRECT_FORWARDING_EVENT = {}

    def __init__(self):
        super(ComObserverGlobalSenderBase, self).__init__(need_update=False)
        self.direct_forwarding_helper = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserverGlobalSenderBase, self).init_from_dict(unit_obj, bdict)
        if not self.direct_forwarding_helper:
            self.direct_forwarding_helper = DirectForwardingHelper(self.DIRECT_FORWARDING_EVENT, self.unit_obj)

    def destroy(self):
        if self.direct_forwarding_helper:
            self.direct_forwarding_helper.destroy()
        self.direct_forwarding_helper = None
        super(ComObserverGlobalSenderBase, self).destroy()
        return