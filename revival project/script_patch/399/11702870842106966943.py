# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/CommonEndCountDownInfo.py
from __future__ import absolute_import
from six.moves import range
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
import logic.gcommon.common_const.battle_const as battle_const
import cc

class CommonEndCountDownInfo(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/i_count_time_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE

    def process_one_message(self, message, finish_cb):
        anim_duration = self.panel.GetAnimationMaxRunTime('count')
        ac_list = []
        count_down, extra_info = message
        self.count_down = count_down
        self.panel.nd_time.lab_time.SetString(str(self.count_down))
        self.panel.nd_time.vx_lab_time.SetString(str(self.count_down))

        def show_count_down():
            self.panel.PlayAnimation('count')

        def sub_count_down():
            self.count_down -= 1
            self.panel.nd_time.lab_time.SetString(str(self.count_down))
            self.panel.nd_time.vx_lab_time.SetString(str(self.count_down))

        def finished():
            if self and self.is_valid():
                self.panel.nd_time.setVisible(False)
                self.finish_cb()

        for i in range(count_down + 1):
            ac_list.append(cc.CallFunc.create(show_count_down))
            ac_list.append(cc.DelayTime.create(anim_duration))
            ac_list.append(cc.CallFunc.create(sub_count_down))

        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self.panel.nd_time.setVisible(True)
        self.panel.runAction(cc.Sequence.create(ac_list))