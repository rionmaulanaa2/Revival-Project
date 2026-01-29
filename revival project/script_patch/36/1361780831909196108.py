# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS4Charge.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityArtCollectionCharge import ActivityArtCollectionCharge

class ActivityS4Charge(ActivityArtCollectionCharge):

    def set_show(self, show, is_init=False):
        super(ActivityS4Charge, self).set_show(show, is_init)
        show = 'show' if is_init else 'show_2'
        self.panel.PlayAnimation(show)

    def play_show_anim(self):
        pass