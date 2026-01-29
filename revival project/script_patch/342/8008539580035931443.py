# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/SpringSignUI.py
from __future__ import absolute_import
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.comsys.activity.SpringFestival.ActivitySpringSign import SpringSignBase

class SpringSignUI(SimpleAdvance, SpringSignBase):
    PANEL_CONFIG_NAME = 'activity/activity_202101/i_activity_enter_benefits'
    APPEAR_ANIM = 'show'
    NEED_GAUSSIAN_BLUR = False
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close'
       }

    def __init__(self, *arg, **kwargs):
        SpringSignBase.__init__(self, *arg, **kwargs)

    def set_content(self):
        self._activity_type = activity_const.ACTIVITY_SPRING_SIGN
        self._init_panel()

    def on_finalize_panel(self):
        SimpleAdvance.on_finalize_panel(self)
        self._finalize_panel()