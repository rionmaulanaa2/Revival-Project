# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_effect/ComHumanSkateEffect.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.skate_appearance_utils import SkateAppearanceAgent
from common.utils.timer import CLOCK

class ComHumanSkateEffect(UnitCom):
    BIND_EVENT = {'E_BOARD_SKATE_FINISHED': 'on_board_skate',
       'E_LEAVE_SKATE': 'on_leave_skate',
       'E_ON_DETACHED': ('on_skate_detached', -1)
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanSkateEffect, self).init_from_dict(unit_obj, bdict)
        self.skate_model = None
        self.sd.ref_skate_appearance_agent = SkateAppearanceAgent(self)
        return

    def destroy(self):
        if self.sd.ref_skate_appearance_agent:
            self.sd.ref_skate_appearance_agent.destroy()
            self.sd.ref_skate_appearance_agent = None
        super(ComHumanSkateEffect, self).destroy()
        self.skate_model = None
        return

    def on_board_skate(self, skate_model):
        if self.skate_model is skate_model:
            return
        self.skate_model = skate_model
        self.sd.ref_skate_appearance_agent.on_board_skate(skate_model)

    def on_leave_skate(self):
        self.sd.ref_skate_appearance_agent.on_leave_skate()
        self.skate_model = None
        return

    def on_skate_detached(self, entity_id, broken):
        if self.skate_model and broken:
            self.sd.ref_skate_appearance_agent.on_skate_destroyed()