# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRogueBoxLogic.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gutils import rogue_utils as r_u
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata import rogue_gift_config

class ComRogueBoxLogic(UnitCom):
    BIND_EVENT = {'E_SCENE_BOX_HOLDER_CHANGE': 'on_scene_box_holder_change',
       'G_SCENE_BOX_HOLDER': 'get_scene_box_holder',
       'G_CAN_OPEN_BOX': '_can_open_box'
       }

    def __init__(self):
        super(ComRogueBoxLogic, self).__init__()
        self._holder_soul_id = None
        self._begin_hold_time = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRogueBoxLogic, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComRogueBoxLogic, self).destroy()

    def on_scene_box_holder_change(self, holder_soul_id):
        self._holder_soul_id = holder_soul_id
        if not holder_soul_id:
            self._begin_hold_time = None
        else:
            self._begin_hold_time = tutil.get_time()
        return

    def get_scene_box_holder(self):
        return self._holder_soul_id

    def _can_open_box(self, unit_obj):
        if not unit_obj:
            return False
        if not unit_obj.ev_g_can_add_more_gift():
            global_data.game_mgr.show_tip(17054)
            return False
        if self._holder_soul_id and self._holder_soul_id != unit_obj.id:
            if self._begin_hold_time and tutil.get_time() - self._begin_hold_time < rogue_gift_config.ROGUE_BOX_MAX_HOLD_TIME:
                return False
        return True