# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalTransitionUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils.judge_utils import get_player_group_id
import math
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id

class ADCrystalTransitionUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_crystal/end_crystal2_round_1'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.init_score_widget()
        self.panel.PlayAnimation('appear')
        self.panel.DelayCall(5, self.do_disappear)
        self.panel.DelayCall(5.5, self.close)

    def init_score_widget(self):
        my_group_id = get_player_group_id()
        battle = global_data.battle
        if not battle or my_group_id is None:
            return
        else:
            def_group_id = battle.get_old_def_group_id()
            atk_group_id = battle.get_old_atk_group_id()
            if battle.get_group_crystal_points(atk_group_id) > 0:
                left_hp = 0
            else:
                left_hp = battle.get_group_crystal_hp_percent(def_group_id)
            hp_percent = int(min(math.ceil(100.0 * left_hp), 100))
            hp_percent_str = '{}%'.format(str(hp_percent))
            left_time = battle.get_group_left_time(atk_group_id)
            left_time = tutil.get_delta_time_str(int(left_time))[3:]
            if my_group_id == battle.get_old_atk_group_id():
                self.panel.nd_blue.lab_value_type_1.nd_auto_fit.lab_hp.SetString(hp_percent_str)
                self.panel.nd_blue.lab_value_type_2.nd_auto_fit.lab_time.SetString(left_time)
                self.panel.nd_red.lab_value_type_1.nd_auto_fit.lab_hp.SetString('\xe2\x80\x94\xe2\x80\x94')
                self.panel.nd_red.lab_value_type_2.nd_auto_fit.lab_time.SetString('\xe2\x80\x94\xe2\x80\x94')
            else:
                self.panel.nd_red.lab_value_type_1.nd_auto_fit.lab_hp.SetString(hp_percent_str)
                self.panel.nd_red.lab_value_type_2.nd_auto_fit.lab_time.SetString(left_time)
                self.panel.nd_blue.lab_value_type_1.nd_auto_fit.lab_hp.SetString('\xe2\x80\x94\xe2\x80\x94')
                self.panel.nd_blue.lab_value_type_2.nd_auto_fit.lab_time.SetString('\xe2\x80\x94\xe2\x80\x94')
            self.panel.lab_round.SetString(get_text_by_id(17495).format(1))
            return

    def do_disappear(self):
        if self.panel and self.panel.isValid():
            self.panel.PlayAnimation('disappear')

    def close(self, *args):
        if not self or not self.panel or not self.panel.isValid():
            return
        super(ADCrystalTransitionUI, self).close()