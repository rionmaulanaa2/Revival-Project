# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonFinishedReportUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
import logic.gutils.season_utils as season_utils
import cc
from logic.gutils.template_utils import init_rank_title
from logic.gcommon.common_const import rank_const
from logic.gutils.dress_utils import get_role_dress_clothing_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.template_utils import set_ui_show_picture
import logic.gcommon.cdata.dan_data as dan_data
from common.cfg import confmgr

class SeasonFinishedReportUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/new_season_report'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_below.OnClick': 'on_click_btn_close',
       'btn_share.OnClick': 'on_click_btn_share'
       }
    UI_OPEN_SOUND = 'season_silver_awards'
    UI_EXIT_SOUND = 'season_tickets_next'

    def on_init_panel(self, *args, **kwargs):
        self.can_enter_new_season = False
        self.init_report_data()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)),
         cc.DelayTime.create(1.2)]

        def animation_end():
            self.can_enter_new_season = True

        action_list.append(cc.CallFunc.create(animation_end))
        loop_time = self.panel.GetAnimationMaxRunTime('show') - 1.2
        if loop_time > 0.2:
            action_list.append(cc.DelayTime.create(loop_time))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_report_data(self):
        if not global_data.player:
            return
        else:
            season_last = max(global_data.player.get_battle_season() - 1, 1)
            self.panel.lab_title.SetString(get_text_by_id(81317, {'season_last': season_last}))
            data = global_data.player.get_last_season_report()
            if not data:
                return
            mecha_title_datas = data.get('mecha_title_datas', [])
            if not self.panel.temp_title:
                return
            self.panel.temp_title.DeleteAllSubItem()
            nbest_mecha = None
            for title_data in mecha_title_datas:
                nd_title = self.panel.temp_title.AddTemplateItem()
                if not nbest_mecha:
                    nbest_mecha = int(title_data[1])
                init_rank_title(nd_title, rank_const.RANK_TITLE_MECHA_REGION, title_data)

            role_id = global_data.player.get_role()
            clothing_id = get_role_dress_clothing_id(role_id)
            if clothing_id:
                pic_path = 'gui/ui_res_2/pic/%s.png' % clothing_id
            else:
                pic_path = 'gui/ui_res_2/pic/20100%s00.png' % role_id
            self.panel.img_mecha.SetDisplayFrameByPath('', pic_path)
            last_season_dan_data = data.get('last_season_dan', {}).get(dan_data.DAN_SURVIVAL, {})
            last_season_dan = last_season_dan_data.get('dan', 1)
            last_season_lv = last_season_dan_data.get('lv', 1)
            self.panel.lab_rank.SetString(season_utils.get_dan_lv_name(last_season_dan, last_season_lv))
            self.panel.lab_title_rank.setVisible(False)
            last_season = data.get('last_season', 1)
            reward_id = season_utils.get_season_reward(last_season, last_season_dan)
            item_no, item_cnt = confmgr.get('common_reward_data', reward_id, 'reward_list')[0]
            reward_str = item_utils.get_lobby_item_name(item_no) + ' x' + str(item_cnt)
            self.panel.lab_reward_name.SetString(reward_str)
            title_content_list = [
             (
              10356, str(data.get('battlepass_lv', 1))),
             (
              10357, '%.1f' % (data.get('total_game_time', 0) / 3600.0) + 'h'),
             (
              10358, str(data.get('total_game_cnt', 0))),
             (
              10359, str(data.get('total_win_cnt', 0))),
             (
              10360, str(data.get('total_kill_human_cnt', 0))),
             (
              10361, str(data.get('total_kill_mecha_cnt', 0)))]
            nd_list = self.panel.list_report
            nd_list.SetInitCount(6)
            for i in range(6):
                item = nd_list.GetItem(i)
                item.lab_title.SetString(get_text_by_id(title_content_list[i][0]))
                item.lab_number.SetString(title_content_list[i][1])
                item.PlayAnimation('show')

            return

    def on_click_btn_close(self, *args):
        if not self.can_enter_new_season:
            return
        global_data.player.receive_season_dan_reward()
        self.can_enter_new_season = False
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('exit')))
        action_list.append(cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_EXIT_SOUND)))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('exit')))

        def animation_end():
            if False and global_data.player and global_data.player.season_stat and global_data.player.season_stat.get('sst_day_dan', []):
                from logic.comsys.battle_pass.season_memory.SeasonAchievementMemoryUI import SeasonAchievementMemoryUI
                SeasonAchievementMemoryUI()
            else:
                from .SeasonFinishedSettleUI import SeasonFinishedSettleUI
                SeasonFinishedSettleUI()
            self.close()

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))

    def on_click_btn_share(self, *args):
        from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
        screen_capture_helper = ScreenFrameHelper()
        self.panel.btn_share.setVisible(False)
        self.panel.btn_below.setVisible(False)

        def cb(*args):
            if not (self.panel and self.panel.isValid()):
                return
            self.panel.btn_share.setVisible(True and global_data.is_share_show)
            self.panel.btn_below.setVisible(True)

        screen_capture_helper.take_screen_shot(['SeasonBeginBackgroundUI', 'SeasonFinishedReportUI'], self.panel, custom_cb=cb, head_nd_name='nd_player_info_1')