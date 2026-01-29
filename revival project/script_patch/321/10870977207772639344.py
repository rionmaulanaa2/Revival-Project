# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2GuideUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id

class Flag2GuideUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_flagsnatch2/guide_human_flagsnatch2'
    GLOBAL_EVENT = {'show_flag2_guide2': 'on_show_flag2_guide2',
       'death_begin_count_down_over': 'ready_guide'
       }
    SHOW_READY_GUIDE_DELAY_TIME = 3.0
    SHOW_GUIDE1_TIME = 5.0
    SHOW_GUIDE2_TIME = 5.0

    def on_init_panel(self):
        self.set_guide1_invisible(False)
        self.set_guide2_invisible(False)

    def set_guide1_invisible(self, is_visible):
        self.panel.nd_step_1.setVisible(is_visible)

    def set_guide2_invisible(self, is_visible):
        self.panel.nd_step_2.setVisible(is_visible)

    def ready_guide(self):
        self.panel.DelayCall(Flag2GuideUI.SHOW_READY_GUIDE_DELAY_TIME, lambda : self.on_show_flag2_guide1())

    def on_show_flag2_guide1(self):
        if global_data.player:
            show_flag2_guide_name = 'Flag2Guide' + str(global_data.player.uid)
            show_guide_ui_cnt = global_data.achi_mgr.get_cur_user_archive_data(show_flag2_guide_name, 0)
            if show_guide_ui_cnt < 2:
                text = get_text_by_id(17914)
                self.panel.nd_step_1.temp_hint.lab_tips.SetString(text)
                self.set_guide1_invisible(True)
                self.panel.StopAnimation('show_step_1')
                self.panel.PlayAnimation('show_step_1')
                global_data.achi_mgr.set_cur_user_archive_data(show_flag2_guide_name, show_guide_ui_cnt + 1)
                self.panel.DelayCall(Flag2GuideUI.SHOW_GUIDE1_TIME, lambda : self.set_guide1_invisible(False))
        self.check_show_introduct_ui()

    def on_show_flag2_guide2(self):
        if global_data.player:
            show_flag2_plant_name = 'Flag2PlantSucc' + str(global_data.player.uid)
            show_guide_ui_cnt = global_data.achi_mgr.get_cur_user_archive_data(show_flag2_plant_name, 0)
            if show_guide_ui_cnt < 2:
                text = get_text_by_id(17915)
                self.panel.nd_step_2.temp_human_tips.nd_contention_riko_tips.lab_tips.SetColor('#SS')
                self.panel.nd_step_2.temp_human_tips.nd_contention_riko_tips.lab_tips.SetString(text)
                self.set_guide2_invisible(True)
                self.panel.StopAnimation('show_step_2')
                self.panel.PlayAnimation('show_step_2')
                global_data.achi_mgr.set_cur_user_archive_data(show_flag2_plant_name, show_guide_ui_cnt + 1)
                self.panel.DelayCall(Flag2GuideUI.SHOW_GUIDE1_TIME, lambda : self.set_guide2_invisible(False))

    def check_show_introduct_ui(self):
        showed_intro = global_data.achi_mgr.get_cur_user_archive_data('showed_flag2_intro', 0)
        if not showed_intro:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 46)
            global_data.achi_mgr.set_cur_user_archive_data('showed_flag2_intro', 1)
        return