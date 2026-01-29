# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby_answering_system/LobbyASReadyWidget.py
from __future__ import absolute_import
from .LobbyASBaseWidget import LobbyASBaseWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.lobby_answering_system_utils import refresh_reward_info

class LobbyASReadyWidget(LobbyASBaseWidget):

    def refresh_data(self):
        question_count = len(global_data.player.get_cur_question())
        self.nd.temp_introduce.lab_question_num.SetString(get_text_by_id(860247, args={'num': question_count}))
        refresh_reward_info(self.nd.bar_reward.list_item)

    def on_click_btn_next(self):
        self.process_next_stage()