# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/LobbyASShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gutils.lobby_answering_system_utils import get_right_answer_count, get_score_pic
from logic.gcommon.common_utils.local_text import get_text_by_id

class LobbyASShareCreator(ShareTemplateBase):
    KIND = 'LOBBY_ANSWERING_SYSTEM_RESULT_SHARE'
    SCORE_TEXT_MAP = {0: 860232,
       1: 860233,
       2: 860234,
       3: 860235,
       4: 860236
       }

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(LobbyASShareCreator, self).create(parent, tmpl)
        question_count = len(global_data.player.get_cur_question())
        right_answer_count = get_right_answer_count()
        fault_answer_count = question_count - right_answer_count
        if fault_answer_count <= 2:
            evaluate_text_id = 860230
        else:
            evaluate_text_id = 860231
        nd = self.panel.nd_share
        nd.setVisible(True)
        nd.lab_grade.SetString(evaluate_text_id)
        nd.lab_right_num.SetString(get_text_by_id(860245, args={'name': global_data.player.get_name(),'num': right_answer_count}))
        nd.lab_score.SetString(LobbyASShareCreator.SCORE_TEXT_MAP.get(fault_answer_count, 860236))
        pic_path, bg_path = get_score_pic(right_answer_count)
        nd.temp_score.bar_score.SetDisplayFrameByPath('', bg_path)
        nd.temp_score.txt_score.SetDisplayFrameByPath('', pic_path)
        nd.temp_score.nd_light.setVisible(right_answer_count == question_count)

    def update_ui_bg_sprite(self):
        pass