# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloweenLotteryCollect.py
from __future__ import absolute_import
from .ActivityArtCollectionCollect import ActivityArtCollectionCollect
from common.cfg import confmgr

class ActivityHalloweenLotteryCollect(ActivityArtCollectionCollect):

    def play_show_anim(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def on_init_panel(self):
        super(ActivityHalloweenLotteryCollect, self).on_init_panel()
        role_ids = [11, 13, 12]
        role_info = confmgr.get('role_info', 'RoleProfile', 'Content')
        for idx, role_id in enumerate(role_ids):
            card_item = self.panel.list_card.GetItem(idx)
            role_name = role_info[str(role_id)]['role_name']
            card_item and card_item.lab_role_name.SetString(role_name)

        global_data.ui_mgr.close_ui('ChangeHeadUI')

    def set_btn_get_enable(self, enable):
        super(ActivityHalloweenLotteryCollect, self).set_btn_get_enable(enable)
        if enable:
            self.panel.vx_btn_01.setVisible(True)
            self.panel.PlayAnimation('loop_btn')
        else:
            self.panel.vx_btn_01.setVisible(False)
            self.panel.StopAnimation('loop_btn')
            self.panel.RecoverAnimationNodeState('loop_btn')

    def refresh_panel(self):
        super(ActivityHalloweenLotteryCollect, self).refresh_panel()
        global_data.ui_mgr.close_ui('ChangeHeadUI')