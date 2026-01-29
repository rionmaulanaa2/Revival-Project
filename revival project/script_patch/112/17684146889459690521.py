# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryVideoBeforeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
import cc

class LotteryVideoBeforeUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/get_model_display_before'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.hide()

    def show_transition(self, callback=None):
        self.panel.stopAllActions()
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear2')))
        action_list.append(cc.CallFunc.create(self.show))
        duration = self.panel.GetAnimationMaxRunTime('appear2')
        action_list.append(cc.DelayTime.create(duration / 3.0 * 2))
        if callback and callable(callback):
            action_list.append(cc.CallFunc.create(callback))
        action_list.append(cc.DelayTime.create(duration / 3.0))
        self.panel.runAction(cc.Sequence.create(action_list))

    def hide(self):
        super(LotteryVideoBeforeUI, self).hide()
        self.panel.stopAllActions()