# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/KothCommonCountDownInfo.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
import logic.gcommon.common_const.battle_const as battle_const
import cc

class KothCommonCountDownInfo(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/koth_tips/i_koth_round_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }

    def process_one_message(self, message, finish_cb):
        message = message[0]
        if message['i_type'] == battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_WARN_TIME:
            anim_name = 'up_show'
            self.panel.lab_num30.SetString(str(battle_const.KOTH_BATTLE_TIP_ROUND_FINISH_TIME_WARN_BEFORE_TIME))
            self.panel.lab_num30.setVisible(True)
        else:
            anim_name = 'up_show2'
            self.panel.lab_num30.setVisible(False)

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        def disappear_animation():
            self.panel.PlayAnimation('up_disappear')

        show_in_t = self.panel.GetAnimationMaxRunTime(anim_name)
        show_off_t = self.panel.GetAnimationMaxRunTime('up_disappear')
        ac_list = []
        ac_list.append(cc.DelayTime.create(show_in_t))
        ac_list.append(cc.CallFunc.create(disappear_animation))
        ac_list.append(cc.DelayTime.create(show_off_t))
        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self.panel.RecoverAnimationNodeState(anim_name)
        self.panel.PlayAnimation(anim_name)
        self.panel.runAction(cc.Sequence.create(ac_list))
        self.up.setVisible(True)

    def on_click_bg_layer(self, *args):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()