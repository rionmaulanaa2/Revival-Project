# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloweenLotteryAccumulate.py
from __future__ import absolute_import
from .ActivityArtCollectionAccumulate import ActivityArtCollectionAccumulate

class ActivityHalloweenLotteryAccumulate(ActivityArtCollectionAccumulate):

    def play_show_anim(self):
        pass

    def set_show(self, show, is_init=False):
        super(ActivityHalloweenLotteryAccumulate, self).set_show(show, is_init)
        if show:
            self.panel.PlayAnimation('loop')
            self.panel.temp_list.PlayAnimation('show_common')
            if is_init:
                self.panel.PlayAnimation('show')
            else:
                title_opacity = self.panel.lab_title.getOpacity()
                if title_opacity < 255:
                    self.panel.PlayAnimation('show')
                else:
                    self.panel.PlayAnimation('show_2')

    def set_btn_get_enable(self, enable):
        super(ActivityHalloweenLotteryAccumulate, self).set_btn_get_enable(enable)
        self.panel.vx_btn_01.setVisible(enable)
        if enable:
            self.panel.PlayAnimation('loop_btn')
        else:
            self.panel.StopAnimation('loop_btn')
            self.panel.RecoverAnimationNodeState('loop_btn')
        self.panel.img_riko.setVisible(not enable)