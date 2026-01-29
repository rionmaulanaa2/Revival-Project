# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonFinishedRewardUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
import logic.gcommon.cdata.dan_data as dan_data
import logic.gutils.season_utils as season_utils
import logic.gutils.item_utils as item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
import cc

class SeasonFinishedRewardUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/new_season_tier_reward'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    GLOBAL_EVENT = {}
    UI_ACTION_EVENT = {'btn_below.OnClick': 'on_click_btn_get_reward'
       }
    UI_OPEN_SOUND = 'season_reward_preview'
    STAGE_NONE = 0
    STAGE_GET_REWARD = 1
    STAGE_REWARD_GOT = 2

    def on_init_panel(self, *args, **kwargs):
        self.cur_stage = self.STAGE_NONE
        self.init_reward_data()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear')),
         cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)),
         cc.DelayTime.create(1.2)]

        def animation_end():
            self.cur_stage = self.STAGE_GET_REWARD

        action_list.append(cc.CallFunc.create(animation_end))
        continue_time = self.panel.GetAnimationMaxRunTime('appear') - 1.2
        if continue_time > 0.2:
            action_list.append(cc.DelayTime.create(continue_time))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('continue')))
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_reward_data(self):
        if not global_data.player:
            return
        data = global_data.player.get_last_season_report()
        if not data:
            return
        last_season_dan = data.get('last_season_dan', {}).get(dan_data.DAN_SURVIVAL, {}).get('dan', 1)
        last_season = data.get('last_season', 1)
        reward_id = season_utils.get_season_reward(last_season, last_season_dan)
        item_no, item_cnt = confmgr.get('common_reward_data', reward_id, 'reward_list')[0]
        reward_str = item_utils.get_lobby_item_name(item_no) + '<size=50><fontname="gui/fonts/g93_num.ttf">' + ' x' + str(item_cnt) + '</fontname></size>'
        reward_str = '<align=0>' + reward_str + '</align>'
        self.panel.lab_reward_name.SetString(reward_str)
        dan_name = get_text_by_id(dan_data.get_dan_name_id(last_season_dan))
        dan_str = get_text_by_id(10362).format(dan_name)
        self.panel.lab_bp_level.SetString(dan_str)
        self.panel.lab_title.SetString(get_text_by_id(608192, {'season_last': last_season}))
        self.panel.lab_tips.SetString(get_text_by_id(81320, {'season_last': last_season}))

    def on_click_btn_get_reward(self, *args):
        if self.cur_stage == self.STAGE_GET_REWARD:
            self.cur_stage = self.STAGE_REWARD_GOT
            global_data.player.receive_season_dan_reward()
            self.get_reward_callback()

    def get_reward_callback(self):
        if self.cur_stage != self.STAGE_REWARD_GOT:
            return
        self.cur_stage = self.STAGE_NONE
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('exit')))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('exit')))

        def animation_end():
            self.close()

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))
        if global_data.player and global_data.player.season_stat and global_data.player.season_stat.get('sst_day_dan', []):
            from logic.comsys.battle_pass.season_memory.SeasonAchievementMemoryUI import SeasonAchievementMemoryUI
            SeasonAchievementMemoryUI()
        else:
            from .SeasonFinishedSettleUI import SeasonFinishedSettleUI
            SeasonFinishedSettleUI()