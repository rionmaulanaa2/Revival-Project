# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/survival/TrainProgUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
from logic.gcommon.const import TRAJECTORY_INTERVAL
import math3d
from common.cfg import confmgr
from common.const import uiconst
import common.utils.timer as timer
from logic.gcommon.common_const import battle_const as b_const
import common.utils.timer as timer

class TrainProgUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_empty_lsland/battle_train_tips_progress'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    STATE_TO_TIP = {b_const.KD_TRAIN_START_PRE_SPEED_UP: 17285,
       b_const.KD_TRAIN_START_SPEED_UP: 17286,
       b_const.KD_TRAIN_START_SPEED_REDUCE: 17286,
       b_const.KD_TRAIN_START_IDLE: 17285,
       b_const.KD_TRAIN_START_SPEED_MAINTAIN: 17286
       }

    def init_parameters(self):
        self._prog_train = None
        self._lab_tips = None
        self._nodes_m = []
        train_node_data = confmgr.get('train_node_data')
        for key, value in six.iteritems(train_node_data):
            self._nodes_m.append(value.get('track_dis'))

        self._nodes_m.sort()
        self._rail_length = confmgr.get('rail_data', '1', 'rail_length')
        self._on_train_tag = False
        self._on_train_judge_timer = None
        self._last_prog = None
        return

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()
        self.init_timer()

    def init_timer(self):
        if not self._on_train_judge_timer:
            self._on_train_judge_timer = global_data.game_mgr.register_logic_timer(self.timed_on_train_judge, interval=2, times=-1, mode=timer.CLOCK)

    def on_finalize_panel(self):
        self.process_event(False)
        if self._on_train_judge_timer:
            global_data.game_mgr.unregister_logic_timer(self._on_train_judge_timer)

    def init_panel(self):
        self._prog_train = self.panel.prog_train
        self._lab_tips = self.panel.lab_tips
        self.panel.main_info.setVisible(False)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_update_train_prog': self.on_update_trian_prog
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def timed_on_train_judge(self):
        if not self._on_train_tag:
            self.panel.main_info.setVisible(False)
        self._on_train_tag = False

    def on_update_trian_prog(self, on_train, train_state, trian_m_pos, train_eid):
        if not on_train:
            return
        else:
            self._on_train_tag = True
            before_station_dis, after_station_dis = self.get_between_nodes_dis(trian_m_pos)
            total_dis = before_station_dis + after_station_dis
            if total_dis < 0:
                prog = 0
            else:
                prog = before_station_dis / (before_station_dis + after_station_dis)
            prog *= 100
            if prog < 0:
                prog = 0
            if prog > 100:
                prog = 100
            self._prog_train.SetPercentage(prog)
            self.panel.main_info.setVisible(True)
            if self._last_prog:
                if self._last_prog < 90 and prog >= 90:
                    global_data.emgr.show_human_tips.emit(17284, 3, cb=None)
            if 97 <= prog <= 100 or prog <= 0.5:
                self._lab_tips.SetString(17285)
                self._prog_train.SetPercentage(100)
                self.panel.StopAnimation('show')
            elif 90 <= prog <= 97:
                self._lab_tips.SetString(17287)
                if not self.panel.IsPlayingAnimation('show'):
                    self.panel.PlayAnimation('show')
            else:
                self._lab_tips.SetString(17286)
                if not self.panel.IsPlayingAnimation('show'):
                    self.panel.PlayAnimation('show')
            self._last_prog = prog
            return

    def get_between_nodes_dis(self, train_m_pos):
        for i in range(len(self._nodes_m) - 1):
            if self._nodes_m[i] <= train_m_pos <= self._nodes_m[i + 1]:
                return (train_m_pos - self._nodes_m[i], self._nodes_m[i + 1] - train_m_pos)

        be_pos = train_m_pos - self._nodes_m[len(self._nodes_m) - 1]
        af_pos = self._nodes_m[0] - train_m_pos
        be_pos = be_pos + self._rail_length if be_pos < 0 else be_pos
        af_pos = af_pos + self._rail_length if af_pos < 0 else af_pos
        return (
         be_pos, af_pos)