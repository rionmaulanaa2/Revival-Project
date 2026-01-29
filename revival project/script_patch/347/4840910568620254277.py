# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby_answering_system/LobbyASMainUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from .LobbyASReadyWidget import LobbyASReadyWidget
from .LobbyASAnswerWidget import LobbyASAnswerWidget
from .LobbyASFinishWidget import LobbyASFinishWidget
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.lobby_answering_system_utils import ANSWER_TASK_ID, update_open_answer_ui_time, check_auto_receive_lobby_answering_system_reward
from logic.gutils.career_utils import get_badge_name_text, get_badge_ongoing_cur_prog, get_badge_ongoing_max_prog
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.timer import CLOCK
STAGE_READY = 0
STAGE_ANSWER = 1
STAGE_FINISH = 2
TOTAL_PROG_TASKS = ('2410072', '2410073', '2410074')

class LobbyASMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'answer/answer_sys'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.hide_main_ui()
        update_open_answer_ui_time()
        if not global_data.player:
            self.close()
        self.init_parameters()
        self.init_widgets()
        self.register_click_events()
        self.process_event(True)
        question_count = len(global_data.player.get_cur_question())
        answered_count = len(global_data.player.get_cur_answers())
        if answered_count > 0:
            if answered_count < question_count:
                self.enter_stage(STAGE_ANSWER)
            elif answered_count == question_count:
                if global_data.player.is_prog_reward_receivable(ANSWER_TASK_ID, 0):
                    self.enter_stage(STAGE_FINISH)
                else:
                    log_error('\xe9\xa2\x98\xe9\x83\xbd\xe7\xad\x94\xe5\xae\x8c\xe4\xba\x86\xe8\xbf\x98\xe8\x83\xbd\xe6\x89\x93\xe5\xbc\x80\xe8\xbf\x99\xe4\xb8\xaa\xe7\x95\x8c\xe9\x9d\xa2\xef\xbc\x8c\xe5\xbf\xab\xe6\x89\xbe\xe7\xa8\x8b\xe5\xba\x8f')
        else:
            self.enter_stage(STAGE_READY, force=True)
        self.update_total_prog_tips()
        self.panel.PlayAnimation('show')
        self.panel.RecordAnimationNodeState('loop_btn')

        def delay_play_lopp():
            if self.cur_stage == STAGE_READY:
                self.panel.PlayAnimation('loop_btn')
            self.anim_timer = None
            return

        if self.cur_stage == STAGE_READY:
            self.anim_timer = global_data.game_mgr.register_logic_timer(delay_play_lopp, interval=0.7, times=1, mode=CLOCK)

    def init_parameters(self):
        self.cur_stage = STAGE_READY
        self.anim_timer = None
        return

    def init_widgets(self):
        self.stage_widgets = {STAGE_READY: LobbyASReadyWidget(self.panel.nd_ready, self),
           STAGE_ANSWER: LobbyASAnswerWidget(self.panel.nd_start, self),
           STAGE_FINISH: LobbyASFinishWidget(self.panel.nd_done, self)
           }

    def register_click_events(self):

        @global_unique_click(self.panel.btn_question)
        def OnClick(*args):
            dlg = GameRuleDescUI()
            title, content = (82332, 82333)
            dlg.set_show_rule(title, content)

        @global_unique_click(self.panel.temp_btn_back.btn_back)
        def OnClick(*args):
            if not global_data.player:
                return
            answered_count = len(global_data.player.get_cur_answers())
            if answered_count == 0 or answered_count == len(global_data.player.get_cur_question()):
                self.close()
            else:
                SecondConfirmDlg2().confirm(content=860246, confirm_callback=self.close)

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'lobby_answering_system_question_updated': self.on_question_updated,
           'net_login_reconnect_before_destroy_event': self.close,
           'task_prog_changed': self.update_total_prog_tips
           }
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def on_finalize_panel(self):
        self.show_main_ui()
        for widget in six.itervalues(self.stage_widgets):
            widget.destroy()

        self.process_event(False)
        self.stage_widgets = None
        if self.anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.anim_timer)
            self.anim_timer = None
        check_auto_receive_lobby_answering_system_reward()
        return

    def enter_stage(self, stage, force=False):
        if not global_data.player:
            return
        else:
            if stage not in self.stage_widgets:
                return
            if stage == self.cur_stage and not force:
                return
            if self.cur_stage == STAGE_READY:
                if self.anim_timer:
                    global_data.game_mgr.unregister_logic_timer(self.anim_timer)
                    self.anim_timer = None
                else:
                    self.panel.StopAnimation('loop_btn')
                    self.panel.RecoverAnimationNodeState('loop_btn')
            self.stage_widgets[self.cur_stage].hide()
            self.cur_stage = stage
            self.stage_widgets[self.cur_stage].show()
            return

    def process_next_stage(self):
        next_stage = self.cur_stage + 1
        self.enter_stage(next_stage)

    def on_question_updated(self):
        global_data.game_mgr.show_tip(82334)
        self.close()

    def update_total_prog_tips(self, *args):
        for task_id in TOTAL_PROG_TASKS:
            cur_prog = get_badge_ongoing_cur_prog(task_id)
            max_prog = get_badge_ongoing_max_prog(task_id)
            if cur_prog < max_prog:
                self.panel.bar_tips.lab_tips.SetString(get_text_by_id(860240, args={'num1': cur_prog,'num2': max_prog - cur_prog,'reward': get_badge_name_text(task_id)}))
                break
        else:
            self.panel.bar_tips.setVisible(False)