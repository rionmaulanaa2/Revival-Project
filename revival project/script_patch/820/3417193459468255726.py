# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/KothRewardRateChangedInfo.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class KothRewardRateChangedInfo(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/koth_tips/i_koth_double_point_tips'
    UI_TYPE = UI_TYPE_MESSAGE

    def process_one_message(self, message, finish_cb):
        message = message[0]
        rate = message.get('reward_rate', 2)
        show_on_t = self.panel.GetAnimationMaxRunTime('show')
        show_off_t = self.panel.GetAnimationMaxRunTime('disappear')
        ac_list = []
        text = get_text_by_id(8211).format(rate)
        self.panel.lab_1.SetString(text)

        def finished():
            if self and self.is_valid():
                self.panel.setVisible(False)
                self.finish_cb()

        ac_list.append(cc.CallFunc.create(lambda : self.panel.StopAnimation('show')))
        ac_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')))
        ac_list.append(cc.DelayTime.create(show_on_t))
        ac_list.append(cc.CallFunc.create(lambda : self.panel.StopAnimation('disappear')))
        ac_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('disappear')))
        ac_list.append(cc.DelayTime.create(show_off_t))
        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self.panel.setVisible(True)
        self.panel.runAction(cc.Sequence.create(ac_list))