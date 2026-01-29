# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonFinishedSettleUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
import logic.gcommon.cdata.dan_data as dan_data
import logic.gutils.season_utils as season_utils
import logic.gutils.template_utils as template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class SeasonFinishedSettleUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/new_season_tier_settlement'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_below.OnClick': 'on_click_btn_next',
       'nd_touch.OnClick': 'on_click_btn_close'
       }
    UI_OPEN_SOUND = 'season_rank_settlement'
    STAGE_NONE = 0
    STAGE_TO_SETTLE = 1
    STAGE_SETTLED = 2
    STAGE_END = 3

    def on_init_panel(self, *args, **kwargs):
        self.cur_stage = self.STAGE_NONE
        self.cur_season_dan = 1
        self.cur_season_star = 0
        self.init_reward_data()
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : template_utils.init_tier_common(self.panel.temp_tier_2, self.cur_season_dan, self.cur_season_star, show_star='star_up', hide_nd_star=True, show_stage='level_up')))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('replace')))
        action_list.append(cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('replace')))

        def animation_end():
            self.cur_stage = self.STAGE_END

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_reward_data(self):
        if not global_data.player:
            return
        cur_battle_season = global_data.player.get_battle_season()
        self.panel.lab_title_1.setVisible(False)
        self.panel.nd_tier_1.setVisible(False)
        self.panel.lab_title_2.SetString(get_text_by_id(81322, {'season_now': cur_battle_season}))
        data = global_data.player.get_last_season_report()
        if not data:
            return
        cur_season_dan_data = data.get('season_settle_dan', {}).get(dan_data.DAN_SURVIVAL, {})
        self.cur_season_dan = cur_season_dan_data.get('dan', 1)
        cur_season_lv = cur_season_dan_data.get('lv', 1)
        self.cur_season_star = cur_season_dan_data.get('star', 0)
        self.panel.lab_tier_name_2.SetString(season_utils.get_dan_lv_name(self.cur_season_dan, cur_season_lv))

    def on_click_btn_next(self, *args):
        if self.cur_stage == self.STAGE_END:
            self.on_click_btn_close()

    def on_click_btn_close(self, *args):
        if self.cur_stage != self.STAGE_END:
            return
        self.cur_stage += 1
        global_data.ui_mgr.close_ui('SeasonBeginUI')
        self.close()