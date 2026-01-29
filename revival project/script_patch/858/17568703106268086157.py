# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoDoublePoint.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import cc

class BattleInfoDoublePoint(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_point/fight_point_mode_double'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoDoublePoint, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.check_visible('BattleInfoMessageVisibleUI')

    def init_event(self):
        self.panel.RecordAnimationNodeState('up_show')

    def process_one_message(self, message, finish_cb):
        wpos = global_data.emgr.get_map_hint_wpos_event.emit()
        if wpos and len(wpos) > 0:
            lpos = self.panel.getParent().convertToNodeSpace(wpos[0])
            self.panel.setPosition(lpos)

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        show_in_t = self.panel.GetAnimationMaxRunTime('up_show')
        ac_list = [
         cc.DelayTime.create(1)]
        ac_list.append(cc.DelayTime.create(show_in_t))
        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self.panel.RecoverAnimationNodeState('up_show')
        self.panel.PlayAnimation('up_show')
        self.panel.runAction(cc.Sequence.create(ac_list))
        self.up.setVisible(True)

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()