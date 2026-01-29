# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/MechaFreeUI.py
from __future__ import absolute_import
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.comsys.activity.SpringFestival.ActivityMechaFree import MechaFreeBase

class MechaFreeUI(SimpleAdvance, MechaFreeBase):
    PANEL_CONFIG_NAME = 'activity/open_202101/i_open_mech_free'
    APPEAR_ANIM = 'show'
    NEED_GAUSSIAN_BLUR = False
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close'
       }

    def __init__(self, *arg, **kwargs):
        MechaFreeBase.__init__(self, *arg, **kwargs)

    def set_content(self):
        self._activity_type = activity_const.ACTIVITY_SPRING_MECHA_FREE
        self._init_panel(root_panel=self.panel.temp_mech_free)