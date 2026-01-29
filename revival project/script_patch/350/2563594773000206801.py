# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby_answering_system/LobbyASFinishWidget.py
from __future__ import absolute_import
from .LobbyASBaseWidget import LobbyASBaseWidget
from logic.gutils.lobby_answering_system_utils import get_right_answer_count, get_score_pic, ANSWER_TASK_ID, refresh_reward_info
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper

class LobbyASFinishWidget(LobbyASBaseWidget):

    def init_parameters(self):
        self.screen_capture_helper = ScreenFrameHelper()
        self.share_content = None
        return

    def init_panel(self):

        @global_unique_click(self.nd.btn_get)
        def OnClick(*args):
            if not global_data.player:
                return
            global_data.player.receive_all_task_prog_reward(ANSWER_TASK_ID)

        @global_unique_click(self.nd.btn_share)
        def OnClick(*args):
            if not self.share_content:
                from logic.comsys.share.LobbyASShareCreator import LobbyASShareCreator
                share_content = LobbyASShareCreator()
                share_content.create()
                self.share_content = share_content
            self.screen_capture_helper.set_custom_share_content(self.share_content)
            self.screen_capture_helper.take_screen_shot([self.parent.__class__.__name__], self.parent.panel)

    def get_event_conf(self):
        econf = {'receive_task_prog_reward_succ_event': self.on_update_task_reward_got_state
           }
        return econf

    def destroy(self):
        super(LobbyASFinishWidget, self).destroy()
        self.screen_capture_helper.destroy()
        self.screen_capture_helper = None
        self.share_content = None
        return

    def refresh_data(self):
        right_answer_count = get_right_answer_count()
        self.nd.temp_right.lab_question_num.SetString(get_text_by_id(860241, args={'num': right_answer_count}))
        pic_path, bg_path = get_score_pic(right_answer_count)
        self.nd.temp_score.bar_score.SetDisplayFrameByPath('', bg_path)
        self.nd.temp_score.txt_score.SetDisplayFrameByPath('', pic_path)
        if global_data.player:
            self.nd.temp_score.nd_light.setVisible(right_answer_count == len(global_data.player.get_cur_question()))
        refresh_reward_info(self.nd.bar_reward.list_item, right_answer_count)
        self.parent.panel.PlayAnimation('show_score')

    def on_update_task_reward_got_state(self, task_id, prog):
        if task_id != ANSWER_TASK_ID:
            return
        if not self.nd.btn_get.IsEnable():
            return
        self.nd.btn_get.SetEnable(False)
        for nd_item in self.nd.bar_reward.list_item.GetAllItem():
            nd_item.nd_get.setVisible(True)