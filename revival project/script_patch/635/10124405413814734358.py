# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNoonCollect.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect

class ActivityNoonCollect(ActivityCollect):

    def on_init_panel(self):
        self.panel.img_icon_time.setVisible(False)
        self.panel.lab_time.setVisible(False)
        super(ActivityNoonCollect, self).on_init_panel()