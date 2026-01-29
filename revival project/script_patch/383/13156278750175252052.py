# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivityGangUp.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
import logic.gcommon.time_utility as tutil
import cc
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN

class ActivityGangUp(ActivityBase):

    def on_init_panel(self):
        self.panel.RecordAnimationNodeState('show')
        self.panel.RecordAnimationNodeState('loop')
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%Y.%m.%d', conf.get('cEndTime', 0), ignore_second=21600)
        self.panel.lab_time_title.SetString(get_text_by_id(601149).format(start_date, finish_date))

        @self.panel.btn_play.btn_common_big.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.close_ui('ActivitySpringFestivalMainUI')
            jump_to_mode_choose(PLAY_TYPE_CHICKEN)

    def set_show(self, show, is_init=False):
        super(ActivityGangUp, self).set_show(show, is_init)
        if show:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.RecoverAnimationNodeState('show')),
             cc.CallFunc.create(lambda : self.panel.RecoverAnimationNodeState('loop')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
             cc.DelayTime.create(0.6),
             cc.CallFunc.create(lambda : self.panel.img_title.PlayAnimation('loop'))]))