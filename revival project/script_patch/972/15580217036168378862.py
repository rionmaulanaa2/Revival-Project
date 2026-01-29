# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummerLotteryAccumulate.py
from __future__ import absolute_import
from .ActivityArtCollectionAccumulate import ActivityArtCollectionAccumulate

class ActivitySummerLotteryAccumulate(ActivityArtCollectionAccumulate):

    def __init__(self, *args):
        super(ActivitySummerLotteryAccumulate, self).__init__(*args)
        self.panel.RecordAnimationNodeState('loop')

    def play_show_anim(self):
        pass

    def set_show(self, show, is_init=False):
        super(ActivitySummerLotteryAccumulate, self).set_show(show, is_init)
        if show:
            if is_init:
                self.panel.PlayAnimation('show_01')
            else:
                self.panel.PlayAnimation('show_02')

    def set_btn_get_enable(self, enable):
        super(ActivitySummerLotteryAccumulate, self).set_btn_get_enable(enable)
        if enable:
            self.panel.PlayAnimation('loop')
        else:
            self.panel.StopAnimation('loop')
            self.panel.RecoverAnimationNodeState('loop')