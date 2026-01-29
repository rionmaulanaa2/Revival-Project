# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaSuicideState.py
from __future__ import absolute_import
from logic.gcommon.common_const.mecha_const import MECHA_SHOOT_NORMAL, MECHA_SHOOT_QUICK
from logic.gcommon.common_utils.local_text import get_text_by_id

class MechaSuicideState(object):

    def __init__(self, parent, nd_aprent, kargs):
        self.parent = parent
        self.nd_parent = nd_aprent

    def bind_events(self, mecha):
        mecha.regist_event('E_SWITCH_SUICIDE_STATE', self.switch_suicide_state)
        self.nd_parent.RecordAnimationNodeState('8002loop')

    def unbind_events(self, mecha):
        mecha.unregist_event('E_SWITCH_SUICIDE_STATE', self.switch_suicide_state)

    def switch_suicide_state(self, state):
        if state:
            self.nd_parent.PlayAnimation('8002loop')
        else:
            self.nd_parent.StopAnimation('8002loop')
            self.nd_parent.RecoverAnimationNodeState('8002loop')

    def destroy(self):
        self.nd_parent.StopAnimation('8002loop')
        self.nd_parent.RecoverAnimationNodeState('8002loop')
        self.parent = None
        self.nd_parent = None
        return