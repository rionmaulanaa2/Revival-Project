# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewSeasonReward.py
from __future__ import absolute_import
from six.moves import zip
from six.moves import range
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from common.const import uiconst
import time
from common.cinematic.VideoPlayer import VideoPlayer
import game3d
from common.cfg import confmgr
from common.utils import ui_path_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
import common.utils.timer as timer

class NewSeasonReward(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/season_reward'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    SEASON_STAGE_1_LEFT_TAG = 11111
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'on_click'
       }
    UI_OPEN_SOUND = 'season_logo'
    GLOBAL_EVENT = {'season_pass_open_type': 'season_pass_buy_card'
       }

    def on_resolution_changed(self):

        def func():
            VideoPlayer().stop_video()
            self.close()

        game3d.delay_exec(1, func)

    def on_init_panel(self, *args):
        self.regist_main_ui()
        self.hide_main_ui()
        self._video_sec = 55
        self._reward_sec = 2
        self._jump_to_new_season_ui = False
        self._stage = -1
        self._stage_sec = 0
        self._can_finish_stage = False
        self.init_season_data()
        self.init_stage_1()

    def on_finalize_panel(self):
        self.unregist_main_ui()
        self.show_main_ui()

    def init_season_data(self):
        from logic.gutils.battle_pass_utils import get_now_season_pass_data, get_now_season
        from logic.gutils.item_utils import get_skin_rare_degree_icon, get_lobby_item_name, get_lobby_item_belong_name
        now_season = get_now_season()
        season_data = get_now_season_pass_data()
        page = self.panel.nd_first_page
        core_item_list = tuple(season_data.two_core_reward)
        name_nds = (
         page.lab_name_role,
         page.lab_name_mecha)
        for item_no, name_nd in zip(core_item_list, name_nds):
            lab_text = get_lobby_item_belong_name(item_no) + '\xc2\xb7' + get_lobby_item_name(item_no)
            name_nd.SetString(lab_text)

        page = self.panel.nd_second_page
        list_container = page.list_item
        item_list = tuple(season_data.six_core_reward)
        for i, item_no in enumerate(item_list):
            nd_item = list_container.GetItem(i)
            if nd_item:
                nd_item.bar_name.lab_name.SetString(get_lobby_item_name(item_no))
                nd_item.bar_name.lab_name.nd_auto_fit.temp_level.bar_level.SetDisplayFrameByPath('', get_skin_rare_degree_icon(item_no))
                nd_item.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))

        @page.btn_get.callback()
        def OnClick(*args):
            if self._stage == 2:
                self._stage = 3
            self.on_click()

    def init_stage_1(self):
        self._stage = 1
        self._stage_sec = 1
        self._can_finish_stage = True
        self._ts = time.time()
        self.panel.nd_first_page.setVisible(True)
        self.panel.nd_second_page.setVisible(False)
        self.init_stage_1_left()
        global_data.sound_mgr.play_ui_sound('s1_pifu_reward')

    def init_stage_1_left(self):
        self._stage = 101
        self._can_finish_stage = True
        self._ts = time.time()
        self.panel.nd_first_page.PlayAnimation('show_01')
        anim_duration = 45 / 33.0
        self.panel.DelayCallWithTag(anim_duration, lambda *args: self.panel.nd_first_page.PlayAnimation('loop_01') and 0, self.SEASON_STAGE_1_LEFT_TAG)
        self._stage_sec = anim_duration + 0.5

    def init_stage_1_right(self):
        self._stage = 102
        self._can_finish_stage = True
        self._ts = time.time()
        self.panel.nd_first_page.StopAnimation('show_01')
        if self.panel.nd_first_page.IsPlayingAnimation('loop_01'):
            self.panel.nd_first_page.StopAnimation('loop_01')
        self.panel.StopTimerActionByTag(self.SEASON_STAGE_1_LEFT_TAG)
        self.panel.nd_first_page.PlayAnimation('show_02')
        anim_duration = 45 / 33.0
        self.panel.DelayCall(anim_duration, lambda *args: self.panel.nd_first_page.PlayAnimation('loop_02') and 0)
        self._stage_sec = anim_duration + 0.5

    def on_stage_1_end(self):
        self.panel.nd_first_page.setVisible(False)
        self.init_stage_2()

    def init_stage_2(self):
        self._stage = 2
        self._can_finish_stage = True
        self._ts = time.time()
        page = self.panel.nd_second_page
        page.setVisible(True)
        page.PlayAnimation('show1')
        list_container = page.list_item
        for i in range(6):
            nd_item = list_container.GetItem(i)
            nd_item.PlayAnimation('show')

        anim_duration = page.GetAnimationMaxRunTime('show1')
        self.panel.DelayCall(anim_duration, lambda *args: self.panel.nd_second_page.PlayAnimation('loop_item_light') and 0)
        self._stage_sec = anim_duration + 0.5
        global_data.sound_mgr.play_ui_sound('s1_other_reward')

    def on_stage_2_end(self):
        if self._jump_to_new_season_ui:
            self.init_stage_3()
        else:
            self.close()

    def init_stage_3(self):
        self.close()
        global_data.ui_mgr.show_ui('NewLoopSeasonUI', 'logic.comsys.battle_pass')

    def on_click(self, *args):
        if self._stage == 1:
            if time.time() - self._ts > min(self._stage_sec, self._reward_sec) and self._can_finish_stage:
                self.on_stage_1_end()
        elif self._stage == 101:
            if time.time() - self._ts > min(self._stage_sec, self._reward_sec) and self._can_finish_stage:
                self.init_stage_1_right()
        elif self._stage == 102:
            if time.time() - self._ts > min(self._stage_sec, self._reward_sec) and self._can_finish_stage:
                self.on_stage_1_end()
        else:
            if self._stage == 2:
                return
            if self._stage == 3:
                if time.time() - self._ts > min(self._stage_sec, self._reward_sec) and self._can_finish_stage:
                    from logic.gutils.jump_to_ui_utils import jump_to_buy_season_pass_card
                    if self._jump_to_new_season_ui:
                        self.on_stage_2_end()
                    else:
                        jump_to_buy_season_pass_card(battle_pass_reward_cb=self.on_stage_2_end)
                        self.close()
            else:
                self.close()

    def play_for_SeasonPassUI(self):
        self._video_sec = 0.5
        self._reward_sec = 0.5
        self._jump_to_new_season_ui = True

    def close(self, *args):
        VideoPlayer().stop_video()
        super(NewSeasonReward, self).close(*args)
        global_data.ui_mgr.close_ui('SeasonBeginUI')

    def season_pass_buy_card(self, sp_type):
        pass