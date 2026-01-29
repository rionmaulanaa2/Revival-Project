# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520MatchTeamate.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMatchTeammate import ActivityMatchTeammate

class Activity520MatchTeamate(ActivityMatchTeammate):
    TIMER_TAG = 210520

    def on_init_panel(self):
        super(Activity520MatchTeamate, self).on_init_panel()
        if self.panel.img_title_1.GetDisplayFramePath() == 'gui/ui_res_2/txt_pic/text_pic_en/activity_202105/520/img_title_recruit.png':
            self.panel.img_light.setVisible(False)
        else:
            self.panel.img_light.setVisible(True)