# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndTransitionUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_0
import cc
from common.const import uiconst

class EndTransitionUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/bg_end_background'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, callback=None, need_close_self=False, animation_played_callback=None):
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('logo_bg')))
        animation_played_callback and action_list.append(cc.CallFunc.create(animation_played_callback))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('logo_bg')))
        if callback and callable(callback):
            action_list.append(cc.CallFunc.create(callback))
        if need_close_self:
            action_list.append(cc.CallFunc.create(self.close))
        self.panel.runAction(cc.Sequence.create(action_list))