# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySakuganCollect.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityArtCollectionCollect import ActivityArtCollectionCollect

class ActivitySakuganCollect(ActivityArtCollectionCollect):

    def play_show_anim(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def update_skin(self, is_init=False):
        super(ActivitySakuganCollect, self).update_skin(is_init)
        if is_init:
            nd_item = self.panel.item3
            nd_item.nd_cut.item.setVisible(False)
            nd_photo = global_data.uisystem.load_template_create('head/i_vx_30290008', parent=nd_item.nd_cut, name='vx_node')
            nd_photo.PlayAnimation('show_head')
            s1 = nd_item.GetContentSize()
            s2 = nd_photo.GetContentSize()
            nd_photo.setScale(s1[0] / s2[0])