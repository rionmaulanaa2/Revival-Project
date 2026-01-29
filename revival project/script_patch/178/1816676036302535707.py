# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/AnnivesaryASMainUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.timer import CLOCK
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.cfg import confmgr
from logic.gcommon.time_utility import get_server_time
FALSE_ANSWER_PROG_PIC = 'gui/ui_res_2/answer/img_answer_prog_dot2.png'
CHOOSE_BG_PIC = {True: 'gui/ui_res_2/answer/img_answer_tips_1.png',
   False: 'gui/ui_res_2/answer/img_answer_tips_2.png'
   }
EXPLAIN_TEXT_COLOR = {True: 7616256,
   False: 16777215
   }
MAX_SELECTION_COUNT = 4

class AnnivesaryASMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'answer/answer_sys_live'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.hide_main_ui()
        self.init_parameters()
        if not global_data.player:
            self.close()
        self.init_panel()
        self.register_click_events()
        self.panel.PlayAnimation('show')
        self.refresh_reward_info()

    def on_finalize_panel(self):
        self.show_main_ui()

    def init_parameters(self):
        self.question_conf = confmgr.get('question_system_config', 'YearLiveQuestionsConfig', 'Content')
        self.question_id = None
        self.true_answer_index = 0
        self.nd = self.panel.nd_start
        return

    def refresh_reward_info(self):
        from logic.gutils.template_utils import init_tempate_mall_i_item
        nd_list = self.panel.list_reward
        reward_info = global_data.game_mode.get_cfg_data('play_data').get('answer_correct_reward', {})
        nd_list.SetInitCount(len(reward_info))
        for index, (item_id, count) in enumerate(six.iteritems(reward_info)):
            nd_item = nd_list.GetItem(index)
            if nd_item.temp_item:
                nd_item = nd_item.temp_item
            init_tempate_mall_i_item(nd_item, item_id, count, show_tips=False)

    def _register_click_choose_item(self, index):

        @global_unique_click(self.nd.list_choose.GetItem(index).btn_choose)
        def OnClick(*args):
            if self.nd.img_answer_tips.isVisible() or not global_data.player:
                return
            global_data.battle.answer_question(self.question_id, six.int2byte(ord('A') + index))
            right = index == self.true_answer_index
            self.nd.img_answer_tips.setVisible(True)
            self.nd.img_answer_tips.SetDisplayFrameByPath('', CHOOSE_BG_PIC[right])
            question_id = self.question_id
            self.nd.img_answer_tips.lab_answer_tips.SetString(self.question_conf[question_id]['explain_text_id'])
            self.nd.img_answer_tips.lab_answer_tips.SetColor(EXPLAIN_TEXT_COLOR[right])
            nd_right_btn = self.nd.list_choose.GetItem(self.true_answer_index).btn_choose
            nd_right_btn.img_choose.setVisible(True)
            if not right:
                nd_false_btn = self.nd.list_choose.GetItem(index).btn_choose
                nd_false_btn.SetEnable(False)
            self.nd.btn_answer.setVisible(True)

    def init_panel(self):
        self.nd.list_choose.SetInitCount(MAX_SELECTION_COUNT)
        for i in range(MAX_SELECTION_COUNT):
            self._register_click_choose_item(i)

    def _update_question_describe(self, question_id):
        text_id_list = self.question_conf[question_id]['text_id_list']
        self.nd.temp_question.lab_question_num.SetString(text_id_list[0])
        selection_count = len(text_id_list) - 1
        nd_choose_list = self.nd.list_choose
        for i in range(0, selection_count):
            nd_choose = nd_choose_list.GetItem(i)
            nd_choose.setVisible(True)
            nd_choose.btn_choose.SetEnable(True)
            nd_choose.btn_choose.SetSelect(False)
            nd_choose.btn_choose.lab_choose.SetString(text_id_list[i + 1])
            nd_choose.btn_choose.img_choose.setVisible(False)

        for i in range(selection_count, MAX_SELECTION_COUNT):
            nd_choose_list.GetItem(i).setVisible(False)

        self.nd.img_answer_tips.setVisible(False)
        self.nd.btn_answer.setVisible(False)
        self.true_answer_index = ord(self.question_conf[question_id]['answer']) - ord('A')

    def refresh_data(self, question_id, close_ts):
        self.question_id = question_id

        def check_close(*args):
            cur_time = get_server_time()
            if cur_time > close_ts:
                self.close()

        cur_time = get_server_time()
        duration = close_ts - cur_time + 2
        self.panel.TimerAction(check_close, duration, check_close, interval=0.5)
        self._update_question_describe(question_id)

    def on_click_btn_next(self):
        self.close()

    def register_click_events(self):

        @global_unique_click(self.panel.temp_btn_back.btn_back)
        def OnClick(*args):
            self.close()

        @self.panel.nd_start.btn_answer.callback()
        def OnClick(btn, touch):
            self.close()