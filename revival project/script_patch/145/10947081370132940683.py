# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComTeammateGlobalSender.py
from __future__ import absolute_import
from .ComObserverGlobalSenderBase import ComObserverGlobalSenderBase

class ComTeammateGlobalSender(ComObserverGlobalSenderBase):
    BIND_EVENT = {'E_ON_CONTROL_TARGET_CHANGE': ('teammate_control_target_change_event', 10)
       }
    DIRECT_FORWARDING_EVENT = {'E_ON_JOIN_MECHA': 'on_teammate_global_join_mecha',
       'E_ON_LEAVE_MECHA': 'on_teammate_global_leave_mecha',
       'E_ON_ADD_EMOJI': 'on_teammate_global_add_emoji',
       'E_ON_REMOVE_EMOJI': 'on_teammate_global_remove_emoji'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComTeammateGlobalSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComTeammateGlobalSender, self).destroy()

    def teammate_control_target_change_event(self, target_id, pos, *args):
        if self.unit_obj:
            global_data.emgr.teammate_control_target_change_event.emit(self.unit_obj.id, target_id, pos)