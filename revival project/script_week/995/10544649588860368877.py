# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonBeginUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from .SeasonBeginBackgroundUI import SeasonBeginBackgroundUI
import logic.gutils.season_utils as season_utils
import cc

class SeasonBeginUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/new_season_open'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_content.OnClick': 'on_click_btn_enter'
       }
    UI_OPEN_SOUND = 'season_admission'
    UI_EXIT_SOUND = 'season_admission_ticket'
    APPEAR_ANIM_NAME = 'appear_s11' if G_IS_NA_PROJECT else 'appear_s6'

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self.can_enter_new_season = False
        self.init_season_range_text()
        SeasonBeginBackgroundUI()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(self.APPEAR_ANIM_NAME)),
         cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)),
         cc.DelayTime.create(1.2)]

        def aim_end():
            self.can_enter_new_season = True

        action_list.append(cc.CallFunc.create(aim_end))
        loop_time = self.panel.GetAnimationMaxRunTime(self.APPEAR_ANIM_NAME) - 1.2
        if loop_time > 0.2:
            action_list.append(cc.DelayTime.create(loop_time))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_season_range_text(self):
        cur_season = global_data.player.get_battle_season()
        s_start_dtime, s_end_dtime = season_utils.get_season_datetime(cur_season)
        self.panel.lab_season_time.SetString('{0} - {1}'.format(get_text_by_id(608048, (s_start_dtime.year, s_start_dtime.month)), get_text_by_id(608048, (s_end_dtime.year, s_end_dtime.month))))

    def on_click_btn_enter(self, *args):
        if not self.can_enter_new_season:
            return
        self.can_enter_new_season = False
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('entry')))
        action_list.append(cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_EXIT_SOUND)))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('entry')))

        def animation_end():
            from .SeasonFinishedReportUI import SeasonFinishedReportUI
            SeasonFinishedReportUI()
            self.hide()

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('SeasonBeginBackgroundUI')
        self.show_main_ui()