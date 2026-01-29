# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleMainKillAchievement.py
from __future__ import absolute_import
import six
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
import cc

class BattleMainKillAchievement(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_tips_main'
    UI_TYPE = UI_TYPE_MESSAGE

    def on_init_panel(self, on_process_done=None):
        super(BattleMainKillAchievement, self).on_init_panel(on_process_done)
        self.is_allow_multiple_show = True

    def _init_msg_ui(self, node):
        node.setOpacity(255)
        node.setScale(1)
        node.lab_1.setOpacity(255)

    def process_one_message(self, message, finish_cb):
        self.main_process_one_message(message, finish_cb)

    def yield_main_node_pos(self, main_node):
        for node in six.itervalues(self._panel_map):
            if node and node.isValid():
                node.SetEnableCascadeOpacityRecursion(True)
                act = cc.Spawn.create([cc.FadeTo.create(0.1, 150), cc.MoveBy.create(0.1, cc.Vec2(60, 0)),
                 cc.ScaleTo.create(0.1, 0.7)])
                node.lab_1.runAction(cc.FadeTo.create(0.1, 120))
                node.runAction(act)