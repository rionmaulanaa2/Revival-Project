# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_simple_sync/ComSimpleJumpSyncSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComSimpleJumpSyncSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_JUMP': '_sync_jump',
       'E_ACTION_SYNC_CLIMB': '_sync_do_climb'
       }

    def __init__(self):
        super(ComSimpleJumpSyncSender, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSimpleJumpSyncSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComSimpleJumpSyncSender, self).destroy()

    def _sync_jump(self, jump_state, *extra_args):
        owner = self.unit_obj.get_owner()
        owner.sync_visit_action('on_jump', (jump_state, extra_args))

    def _sync_do_climb(self, climb_type, climb_pos, climb_rotation):
        owner = self.unit_obj.get_owner()
        lst_pos = (climb_pos.x, climb_pos.y, climb_pos.z)
        owner.sync_visit_action('on_climb', (climb_type, lst_pos, climb_rotation))