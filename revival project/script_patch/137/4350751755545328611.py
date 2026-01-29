# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoPoint.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.common_ui import CommonInfoUtils
from logic.gcommon.common_const import battle_const

class BattleInfoPoint(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_tips_main'
    UI_TYPE = UI_TYPE_MESSAGE

    def init_parameters(self):
        super(BattleInfoPoint, self).init_parameters()
        self.cur_point_panel = None
        return

    def on_finalize_panel(self):
        super(BattleInfoPoint, self).on_finalize_panel()
        if self.cur_point_panel:
            CommonInfoUtils.destroy_ui(self.cur_point_panel)
            self.cur_point_panel = None
        return

    def process_one_message(self, message, finish_cb):
        self.main_process_one_message(message, finish_cb)
        msg_dict = message[0]
        cur_point = msg_dict.get('cur_point', None)
        if cur_point:
            self.panel.nd_player_point.setVisible(True)
            if self.cur_point_panel is None:
                self.cur_point_panel = CommonInfoUtils.create_ui(battle_const.MAIN_KOTH_DAMAGE_POINT, self.panel.nd_player_point)
            self.cur_point_panel.PlayAnimation('show')
            self.cur_point_panel.lab_player_point.SetString(str(cur_point))
        else:
            self.panel.nd_player_point.setVisible(False)
        return