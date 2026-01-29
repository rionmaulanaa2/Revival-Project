# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombCountDownUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.comsys.battle.NBomb import nbomb_utils
from common.const import uiconst

class NBombCountDownUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_bomb/i_battle_bomb_tip_countdown'
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.update_act = None
        self.update_count_down()
        return

    def on_finalize_panel(self):
        self.update_act = None
        return

    def init_bg_path(self):
        self.SELF_BG_PATH = 'res/gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_countdown_0.png'
        self.EMENY_BG_PATH = 'res/gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_countdown_1.png'

    def update_count_down(self):
        if not self.panel:
            return
        self.update_bg_path()
        self.register_timer()

    def update_bg_path(self):
        is_self_camp_installed = global_data.nbomb_battle_data.is_self_group_install_nbomb()
        self_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_countdown_0.png'
        emeny_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_countdown_1.png'
        bar_path = self_path if is_self_camp_installed else emeny_path
        self.panel.bar.SetDisplayFrameByPath('', bar_path)

    def count_down(self):
        if not nbomb_utils.is_data_ready():
            return
        end_time = global_data.nbomb_battle_data.get_nbomb_cd_timestamp()
        cur_time = tutil.get_server_time_battle()
        left_time = max(end_time - cur_time, 0)
        if left_time > 0:
            cd_txt = get_text_by_id(18308, {'countdown': int(left_time)})
            self.panel.lab_title.SetString(cd_txt)
        else:
            global_data.ui_mgr.close_ui('NBombCountDownUI')

    def register_timer(self):
        if self.update_act:
            return
        self.count_down()
        if self.panel:
            self.update_act = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
             cc.DelayTime.create(1.0),
             cc.CallFunc.create(self.count_down)])))