# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleTips.py
from __future__ import absolute_import
from logic.comsys.common_ui.CommonTips import Tips, TipsManager
from common.uisys.uielment.CCRichText import CCRichText
import cc

class BattleTips(Tips):

    def _gen_tips_nd(self):
        return global_data.uisystem.load_template_create('battle/i_feedback_msg_nd')

    def on_show(self):
        self._nd.SetPosition('50%', '50%')
        if isinstance(self._msg_data, str):
            self._nd.lab_tips.SetString(self._msg_data)
        self._nd.PlayAnimation('tips_show')
        act0 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('tips_show'))
        act1 = cc.DelayTime.create(0.5)
        act2 = cc.CallFunc.create(self._cc_allow_callback)
        act2_5 = cc.DelayTime.create(1.5)

        def _tips_hide():
            if self.is_valid():
                self._nd.PlayAnimation('tips_hide')

        act3 = cc.CallFunc.create(_tips_hide)
        act4 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('tips_hide'))
        act5 = cc.CallFunc.create(self._cc_finish_callback)
        self._nd.runAction(cc.Sequence.create([
         act0, act1, act2, act2_5, act3, act4, act5]))

    def on_other_tips_show(self):
        self._nd.stopAllActions()
        self._nd.PlayAnimation('tips_hide')
        act4 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('tips_hide'))
        act1 = cc.DelayTime.create(0.5)
        act5 = cc.CallFunc.create(self._cc_finish_callback)
        self._nd.runAction(cc.Sequence.create([
         act4, act1, act5]))


class BattleTipsManager(TipsManager):

    def add_tips(self, tips_data, ignore_check=False):
        if ignore_check or self.get_previous_tips_data() != tips_data:
            super(BattleTipsManager, self).add_tips(tips_data)

    def get_previous_tips_data(self):
        if len(self._message_queue) > 0:
            return self._message_queue[-1]
        else:
            if len(self._on_fly_msg_nds) > 0:
                last_nd = self._on_fly_msg_nds[-1]
                return last_nd.get_msg_data()
            return None
            return None