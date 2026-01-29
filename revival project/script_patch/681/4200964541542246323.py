# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/GuideBondUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER
GLOBAL_STEP = 1
from common.const import uiconst

class GuideBondUI(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/guide_bond'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_ACTION_EVENT = {'nd_step_1.OnClick': 'on_step1_click',
       'nd_step_2.OnClick': 'on_step2_click',
       'nd_step_3.OnClick': 'on_step3_click'
       }

    def on_init_panel(self, *args, **kwargs):
        global GLOBAL_STEP
        self.step_count = 3
        self.on_step(GLOBAL_STEP)

    def on_step(self, i):
        global GLOBAL_STEP
        GLOBAL_STEP = i
        self.change_step()

    def on_step1_click(self, *args):
        self.on_step(2)

    def on_step2_click(self, *args):
        self.on_step(3)

    def change_step(self):
        for i in range(1, 1 + self.step_count):
            self.panel.StopAnimation('show_%d' % i)
            step_item = getattr(self.panel, 'nd_step_%d' % i, None)
            if not step_item:
                continue
            visible = i == GLOBAL_STEP
            step_item.setVisible(visible)

        self.panel.PlayAnimation('show_%d' % GLOBAL_STEP)
        return

    def on_step3_click(self, *args):
        self.close()