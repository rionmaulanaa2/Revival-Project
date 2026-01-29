# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_simple_sync/ComSimpleJumpSyncReceiver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComSimpleJumpSyncReceiver(UnitCom):
    BIND_EVENT = {'E_SIMPLE_SYNC_JUMP': '_sync_jump',
       'E_SIMPLE_SYNC_CLIMB': '_sync_do_climb'
       }

    def __init__(self):
        super(ComSimpleJumpSyncReceiver, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSimpleJumpSyncReceiver, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComSimpleJumpSyncReceiver, self).destroy()

    def _sync_jump(self, jump_state, *extra_args):
        from logic.gcommon.common_const import animation_const
        if jump_state == animation_const.JUMP_STATE_UP:
            self.send_event('E_CTRL_JUMP')
        elif jump_state == animation_const.JUMP_STATE_IN_AIR:
            self.send_event('E_FALL')
        elif jump_state == animation_const.JUMP_STATE_FALL_GROUND:
            self.send_event('E_ACTION_SYNC_ON_GROUND', *extra_args)

    def _sync_do_climb(self, climb_type, climb_pos, climb_rotation):
        self.send_event('E_CLIMB', climb_type, climb_pos, climb_rotation)