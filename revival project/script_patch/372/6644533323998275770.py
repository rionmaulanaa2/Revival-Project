# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummerLotteryCollect.py
from __future__ import absolute_import
from .ActivityArtCollectionCollect import ActivityArtCollectionCollect

class ActivitySummerLotteryCollect(ActivityArtCollectionCollect):

    def __init__(self, *args):
        super(ActivitySummerLotteryCollect, self).__init__(*args)
        self.panel.RecordAnimationNodeState('btn_get_loop')

    def play_show_anim(self):
        self.panel.PlayAnimation('show')

    def set_btn_get_enable(self, enable):
        super(ActivitySummerLotteryCollect, self).set_btn_get_enable(enable)
        if enable:
            self.panel.PlayAnimation('btn_get_loop')
        else:
            self.panel.StopAnimation('btn_get_loop')
            self.panel.RecoverAnimationNodeState('btn_get_loop')