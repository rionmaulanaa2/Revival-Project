# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby_answering_system/LobbyASAnswerWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from .LobbyASBaseWidget import LobbyASBaseWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.lobby_answering_system_utils import refresh_reward_info
from common.cfg import confmgr
FALSE_ANSWER_PROG_PIC = 'gui/ui_res_2/answer/img_answer_prog_dot2.png'
CHOOSE_BG_PIC = {True: 'gui/ui_res_2/answer/img_answer_tips_1.png',
   False: 'gui/ui_res_2/answer/img_answer_tips_2.png'
   }
EXPLAIN_TEXT_COLOR = {True: 7616256,
   False: 16777215
   }
MAX_SELECTION_COUNT = 4

class LobbyASAnswerWidget(LobbyASBaseWidget):

    def _initialize_local_cache_param(self):
        if global_data.player:
            self.question_list = global_data.player.get_cur_question()
            self.answered_info = global_data.player.get_cur_answers()

    @property
    def right_answer_count(self):
        return self._right_answer_count

    @right_answer_count.setter
    def right_answer_count(self, value):
        if self._right_answer_count == value:
            return
        self._right_answer_count = value
        refresh_reward_info(self.nd.nd_reward.list_reward, value)

    def init_parameters(self):
        self.question_conf = confmgr.get('question_system_config', 'QuestionsConfig', 'Content')
        self.question_list = None
        self.answered_info = None
        self._right_answer_count = -1
        self.true_answer_index = 0
        self._initialize_local_cache_param()
        self.anim_timer = None
        return

    def _initialize_list_prog(self):
        if global_data.player:
            self.nd.list_prog.SetInitCount(len(self.question_list))
            self.nd.list_prog.GetItem(-1).img_line.setVisible(False)

    def _play_reward_show_anim(self):
        self.anim_timer = None
        for nd_reward in self.nd.nd_reward.list_reward.GetAllItem():
            nd_reward.PlayAnimation('show')

        return

    def _register_click_choose_item(self, index):

        @global_unique_click(self.nd.list_choose.GetItem(index).btn_choose)
        def OnClick(*args):
            if self.nd.img_answer_tips.isVisible() or not global_data.player:
                return
            else:
                cur_question_index = len(self.answered_info)
                global_data.player.commit_answer(self.question_list[cur_question_index], chr(ord('A') + index))
                right = index == self.true_answer_index
                self.nd.img_answer_tips.setVisible(True)
                self.nd.img_answer_tips.SetDisplayFrameByPath('', CHOOSE_BG_PIC[right])
                question_id = self.question_list[cur_question_index]
                self.nd.img_answer_tips.lab_answer_tips.SetString(self.question_conf[question_id]['explain_text_id'])
                self.nd.img_answer_tips.lab_answer_tips.SetColor(EXPLAIN_TEXT_COLOR[right])
                self._update_answer_progress(cur_question_index, ret=right)
                nd_right_btn = self.nd.list_choose.GetItem(self.true_answer_index).btn_choose
                nd_right_btn.img_choose.setVisible(True)
                if not right:
                    nd_false_btn = self.nd.list_choose.GetItem(index).btn_choose
                    nd_false_btn.SetEnable(False)
                if right:
                    self.right_answer_count += 1
                    if self.anim_timer:
                        global_data.game_mgr.unregister_logic_timer(self.anim_timer)
                        self.anim_timer = None
                    self.anim_timer = global_data.game_mgr.register_logic_timer(self._play_reward_show_anim, interval=3, times=1)
                self.nd.btn_answer.setVisible(True)
                return

    def init_panel(self):
        self.nd.list_prog.DeleteAllSubItem()
        self._initialize_list_prog()
        self.nd.list_choose.SetInitCount(MAX_SELECTION_COUNT)
        for i in range(MAX_SELECTION_COUNT):
            self._register_click_choose_item(i)

    def destroy(self):
        super(LobbyASAnswerWidget, self).destroy()
        self.question_list = None
        self.answered_info = None
        if self.anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.anim_timer)
            self.anim_timer = None
        return

    def _update_answer_progress(self, index, ret=None):
        question_id = self.question_list[index]
        answer = self.answered_info[question_id]
        nd_dot_pic = self.nd.list_prog.GetItem(index).img_prog_dot
        nd_dot_pic.setVisible(True)
        if ret is None:
            true_answer = self.question_conf[question_id]['answer']
            ret = answer == true_answer
        if not ret:
            nd_dot_pic.SetDisplayFrameByPath('', FALSE_ANSWER_PROG_PIC)
        return int(ret)

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

    def refresh_data(self):
        self._initialize_local_cache_param()
        self._initialize_list_prog()
        right_answer_count = 0
        for index, question_id in enumerate(self.question_list):
            if question_id not in self.answered_info:
                break
            right_answer_count += self._update_answer_progress(index)

        self.right_answer_count = right_answer_count
        cur_question_index = len(self.answered_info)
        self._update_question_describe(self.question_list[cur_question_index])

    def on_click_btn_next(self):
        cur_question_index = len(self.answered_info)
        if cur_question_index < len(self.question_list):
            self._update_question_describe(self.question_list[cur_question_index])
        else:
            self.process_next_stage()