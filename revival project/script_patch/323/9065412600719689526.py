# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/season/SeasonMainUI.py
from __future__ import absolute_import
import math
from cocosui import cc
from common import utilities
from logic.gcommon.cdata import dan_data
from logic.gcommon.cdata import season_data
from logic.gutils import template_utils
from logic.gutils import season_utils
from logic.gutils import task_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE

class SeasonMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'season/season_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_close',
       'btn_describe.OnClick': 'on_desc',
       'btn_tier_details.OnClick': 'on_tier_desc',
       'btn_details.OnClick': 'on_reward_details'
       }

    def init(self, parent=None, *arg, **kwargs):
        self._cur_season = global_data.player.get_battle_season()
        self._cur_score = global_data.player.get_league_point(dan_data.DAN_SURVIVAL)
        self._cur_star = global_data.player.get_dan_star(dan_data.DAN_SURVIVAL)
        self._cur_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
        self._cur_lv = global_data.player.get_dan_lv(dan_data.DAN_SURVIVAL)
        self.reward_1_visible = False
        self.reward_2_visible = False
        super(SeasonMainUI, self).init(parent=parent, *arg, **kwargs)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'dan_head_frame_reward': self.show_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        global_data.ui_mgr.close_ui('SeasonFullScreenBg')
        self.show_main_ui()

    def on_custom_template_create(self, *args, **kwargs):
        stage_template = season_utils.get_dan_template(self._cur_dan)
        self._custom_template_info = {'temp_tier': {'template_info': {'temp_tier': {'ccbFile': stage_template}}}}

    def do_hide_panel(self):
        super(SeasonMainUI, self).do_hide_panel()
        bg_ui = global_data.ui_mgr.get_ui('SeasonFullScreenBg')
        bg_ui and bg_ui.do_hide_panel()

    def do_show_panel(self):
        super(SeasonMainUI, self).do_show_panel()
        bg_ui = global_data.ui_mgr.get_ui('SeasonFullScreenBg')
        bg_ui and bg_ui.do_show_panel()

    def _on_update_reward(self, task_id):
        self.show_reward()

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        global_data.ui_mgr.show_ui('SeasonFullScreenBg', 'logic.comsys.season')
        self.init_event()
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('loop')
        self.panel.temp_tier.temp_tier.PlayAnimation('glow')
        self.panel.nd_reward_1.setVisible(False)
        self.panel.nd_reward_foreign.setVisible(False)

        def cb1():
            self.panel.nd_reward_1.setVisible(self.reward_1_visible)
            self.panel.nd_reward_foreign.setVisible(self.reward_2_visible)

        def cb2():
            self.panel.PlayAnimation('jihe_liz')

        max_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.SetTimeOut(max_time * 0.23, cb1)
        self.panel.SetTimeOut(max_time, cb2)
        self.panel.lab_season.SetString(get_text_by_id(10295, [self._cur_season]))
        s_start_dtime, s_end_dtime = season_utils.get_season_datetime(self._cur_season)
        self.panel.lab_time.SetString('{0} - {1}'.format(get_text_by_id(608048, (s_start_dtime.year, s_start_dtime.month)), get_text_by_id(608048, (s_end_dtime.year, s_end_dtime.month))))
        self.panel.lab_tier_name.SetString(season_utils.get_dan_lv_name(self._cur_dan, self._cur_lv))
        self.panel.lab_tier_name.ResizeAndPosition()
        template_utils.init_tier_common(self.panel.temp_tier, self._cur_dan, self._cur_star)
        total_score = dan_data.LEAGUE_POINT_PER_STAR
        self.panel.lab_score.SetString('{0}/{1}'.format(self._cur_score, total_score))
        self.panel.prog_score.SetPercentage(utilities.safe_percent(self._cur_score, total_score))
        protect_dan = [
         dan_data.BROZE, dan_data.SILVER]
        if self._cur_dan in protect_dan:
            self.panel.lab_protect.SetString(608036)
        else:
            self.panel.lab_protect.SetString(get_text_by_id(608037, [global_data.player.get_dan_protect_num(dan_data.DAN_SURVIVAL)]))
        if not G_IS_NA_PROJECT:
            self.panel.lab_season.SetString(608201)
            self.panel.nd_season_time.setVisible(False)
            self.reward_2_visible = False
        else:
            self.reward_2_visible = True
        self.show_reward()

    def show_reward(self):
        task_id, nxt_dan = season_utils.get_todo_dan_task(self._cur_season, self._cur_dan)
        nd_reward_1 = self.panel.nd_reward_1
        if task_id:
            reward_id = task_utils.get_task_reward(task_id)
            reward_id = reward_id if reward_id else 12000003
            item_no, item_cnt = confmgr.get('common_reward_data', str(reward_id), 'reward_list')[0]
            nd_reward_1.lab_condition.SetString(get_text_by_id(608018, [season_utils.get_dan_lv_name(nxt_dan)]))
            nd_reward_1.lab_describe.SetString(task_utils.get_task_name(task_id))
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            nd_reward_1.lab_condition_finish.SetString('{0}/{1}'.format(cur_times, total_times))
            self.reward_1_visible = True
            if global_data.player.has_unreceived_task_reward(task_id):
                nd_reward_1.temp_reward.nd_get_tips.setVisible(True)
                nd_reward_1.temp_reward.PlayAnimation('get_tips')

                def callback():
                    global_data.player.receive_task_reward(task_id)

                template_utils.init_tempate_mall_i_item(nd_reward_1.temp_reward, item_no, item_cnt, callback=callback)
            elif global_data.player.is_all_received_reward(task_id):
                nd_reward_1.temp_reward.nd_get_tips.setVisible(False)
                nd_reward_1.temp_reward.StopAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(nd_reward_1.temp_reward, item_no, item_cnt, isget=True, show_tips=True, callback=False)
            else:
                nd_reward_1.temp_reward.nd_get_tips.setVisible(False)
                nd_reward_1.temp_reward.StopAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(nd_reward_1.temp_reward, item_no, item_cnt, show_tips=True, callback=False)
        else:
            self.reward_1_visible = False
        reward_id = season_utils.get_season_reward(self._cur_season, self._cur_dan)
        nd_reward_2 = self.panel.nd_reward_2
        item_no, item_cnt = confmgr.get('common_reward_data', reward_id, 'reward_list')[0]
        template_utils.init_tempate_mall_i_item(nd_reward_2.temp_reward, item_no, item_cnt, show_tips=True)
        nd_reward_2.lab_condition.SetString(608017)
        nd_reward_2.lab_condition_finish.SetString('{0}x{1}'.format(item_utils.get_lobby_item_name(item_no), item_cnt))
        if season_utils.get_dan_task_can_reward_count(self._cur_season) > 0 or season_utils.get_dan_frame_reward_redpoint():
            self.panel.PlayAnimation('reward_tips')
            self.panel.btn_details.img_red.setVisible(True)
        else:
            self.panel.StopAnimation('reward_tips')
            self.panel.btn_details.img_red.setVisible(False)

    def on_close(self, *args):
        self.close()

    def on_desc(self, *args):
        dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
        text_id = 608019 if G_IS_NA_PROJECT else 608202
        dlg.set_show_rule(608040, text_id)

    def on_tier_desc(self, *args):
        global_data.ui_mgr.show_ui('TierDetailUI', 'logic.comsys.season')

    def on_reward_details(self, *args):
        global_data.ui_mgr.show_ui('TierRewardUI', 'logic.comsys.season')