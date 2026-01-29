# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/TopFiveWidget.py
from __future__ import absolute_import
import time
from common.utils import timer
from common.uisys.BaseUIWidget import BaseUIWidget
STATE_CONTINUE = 0
STATE_END = 1
EXIT_SECOND = 3

class TopFiveWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, close_call_back):
        self.global_events = {}
        super(TopFiveWidget, self).__init__(parent_ui, panel)
        self._close_call_back = close_call_back
        self._is_closing = False
        self._init_ui_event()
        self.panel.PlayAnimation('show')
        self._timer_time = time.time()
        self._state = STATE_CONTINUE
        self.panel.lab_continue.setString(get_text_by_id(18808) + str(EXIT_SECOND))
        self.panel.lab_esc.setString(get_text_by_id(2176))
        self._timer = global_data.game_mgr.register_logic_timer(self._timer_tick, interval=1, times=-1, mode=timer.CLOCK)

    def _init_ui_event(self):

        @self.panel.btn_esc.unique_callback()
        def OnClick(btn, touch):
            if not self._is_closing:
                if self._state == STATE_CONTINUE:
                    self._state = STATE_END
                    self.panel.lab_continue.SetString(18808)
                    self.panel.lab_esc.setString(get_text_by_id(2176) + str(EXIT_SECOND))
                    self.panel.lab_main.SetString(19796)
                    self._timer_time = time.time()
                elif self._state == STATE_END:
                    self._clear_timer()
                    self._try_finish_newbie_guide()
                    global_data.player and global_data.player.quit_battle()
                    self._close_panel(need_anim=False)

        @self.panel.btn_continue.unique_callback()
        def OnClick(btn, touch):
            if not self._is_closing:
                self._close_panel()

    def _close_panel(self, need_anim=True):
        self._is_closing = True

        def finished():
            if self._close_call_back:
                self._close_call_back()
            self._close_call_back = None
            self.destroy()
            return

        if need_anim:
            animation_time = self.panel.GetAnimationMaxRunTime('hide')
            self.panel.PlayAnimation('hide')
            self.panel.SetTimeOut(animation_time, finished)
        else:
            finished()

    def _timer_tick(self, *args):
        left_time = EXIT_SECOND - int(time.time() - self._timer_time)
        txt_id = 18808 if self._state == STATE_CONTINUE else 2176
        node = self.panel.lab_continue if self._state == STATE_CONTINUE else self.panel.lab_esc
        if left_time >= 1:
            text = get_text_by_id(txt_id) + str(left_time)
            node.setString(text)
        if left_time <= 0:
            self._close_panel()
            return timer.RELEASE

    def _clear_timer(self):
        self._timer and global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def destroy(self):
        self._clear_timer()
        if self.panel and self.panel.isValid():
            self.panel.Destroy()
        self.panel = None
        if global_data.player and global_data.player.in_new_local_battle() and global_data.player.logic:
            global_data.player.logic.send_event('E_GUIDE_TOP_FIVE_WIDGET_DESTROY')
        super(TopFiveWidget, self).destroy()
        return

    def _try_finish_newbie_guide(self):
        if self._state == STATE_END and global_data.player and global_data.player.in_new_local_battle():
            from logic.client.const import game_mode_const
            from logic.gutils import newbie_stage_utils
            battle = global_data.player.get_new_local_battle()
            battle_tid = battle.get_battle_tid() if battle else None
            if battle_tid == game_mode_const.NEWBIE_STAGE_FOURTH_BATTLE_TYPE:
                newbie_stage_utils.finish_local_battle_guide(battle_tid)
        return