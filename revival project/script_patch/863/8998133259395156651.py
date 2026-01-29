# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySpringRedEnvelopes.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.share_utils import share_wx_mini_program, get_mini_program_path_sign
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.platform.dctool import interface
from logic.gcommon import time_utility as tutil
from logic.gutils import role_head_utils
from logic.gutils.live_utils import format_one_line_text
from logic.gcommon.common_const import activity_const as acconst
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import time

class ActivitySpringRedEnvelopes(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySpringRedEnvelopes, self).__init__(dlg, activity_type)
        self.process_event(True)

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        self.init_parameters()
        self.init_btns()
        self.register_timer()
        self._timer_cb[0] = lambda : self.refresh_spring_envelope_time()
        self.refresh_spring_envelope_time()
        self.update_spring_envelope()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        del_keys = []
        for key, cb in six.iteritems(self._timer_cb):
            result = cb()
            if result == -1:
                del_keys.append(key)

        for key in del_keys:
            del self._timer_cb[key]

    def get_spring_envelope_left_time(self):
        player = global_data.player
        if not player:
            return (-1, -1)
        return player.get_spring_envelope_left_time()

    def refresh_spring_envelope_time(self):
        start_left_time, end_left_time = self.get_spring_envelope_left_time()
        if start_left_time > 0:
            self.panel.btn_open1.lab_time_limit1.setVisible(True)
            self.panel.btn_open1.lab_time_limit1.SetString(tutil.get_readable_time_2(start_left_time))
        elif end_left_time > 0:
            if not self.panel.btn_open1.btn_common.IsEnable():
                self.panel.btn_open1.lab_time_limit1.setVisible(False)
                self.update_spring_envelope()
        else:
            self.panel.btn_open1.lab_time_limit1.setVisible(False)
            self.update_spring_envelope()
            return -1

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'set_spring_envelope_state_event': self.update_spring_envelope
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_btns(self):
        self.panel.btn_open1.btn_common.SetEnable(False)

        @self.panel.btn_open1.btn_common.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            if player.get_lv() < 10:
                global_data.game_mgr.show_tip(get_text_by_id(607931))
            else:
                player.receive_spring_red_envelope()

    def update_spring_envelope(self):
        player = global_data.player
        if not player:
            return
        spring_envelope_state = player.get_spring_envelope_state()
        btn_open1 = self.panel.btn_open1.btn_common
        btn_open1.SetEnable(False)
        start_left_time, end_left_time = self.get_spring_envelope_left_time()
        self.panel.btn_open1.img_red.setVisible(False)
        if start_left_time > 0:
            btn_open1.SetEnable(False)
            btn_open1.SetText(19825)
        elif end_left_time > 0:
            if spring_envelope_state:
                btn_open1.SetEnable(False)
                if player.is_spring_envelope_last_day():
                    btn_open1.SetText(607911)
                else:
                    btn_open1.SetText(606046)
            else:
                btn_open1.SetEnable(True)
                if player.get_lv() < 10:
                    btn_open1.SetText(607930)
                else:
                    self.panel.btn_open1.img_red.setVisible(True)
                    btn_open1.SetText(607908)
        else:
            btn_open1.SetEnable(False)
            btn_open1.SetText(607911)
        if self.panel.btn_open1.lab_time_limit1.isVisible():
            btn_open1.SetTextOffset({'x': '50%','y': '50%15'})
        else:
            btn_open1.SetTextOffset({'x': '50%','y': '50%'})
        global_data.emgr.refresh_activity_redpoint.emit()