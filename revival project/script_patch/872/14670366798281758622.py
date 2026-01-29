# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupyPoint.py
from __future__ import absolute_import
from logic.gcommon.common_const.battle_const import STATE_OCCUPY_EMPTY, STATE_OCCUPY_SELF, STATE_OCCUPY_ENEMY, STATE_OCCUPY_SNATCH, OCCUPY_POINT_STATE_IDLE, OCCUPY_POINT_STATE_DEC, OCCUPY_POINT_STATE_INC, OCCUPY_POINT_STATE_SNATCH
TICK_TIME = 0.5
PROG_SCALE = 0.35
PROG_ADD = -35
PARTID_TO_TEXT = {1: 'A',
   2: 'B',
   3: 'C'
   }

class MutiOccupyPoint(object):

    def __init__(self, nd, part_id):
        self._nd = nd
        self.part_id = part_id
        self.init_parameters()

    def init_parameters(self):
        self.inc_progress = 10
        self.dec_progress = 10
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if play_data:
            self.inc_progress = play_data.get('inc_progress')
            self.dec_progress = play_data.get('dec_progress')
        if self._nd.HasAnimation('show_light'):
            self._nd.RecordAnimationNodeState('show_light')

    def init_base_data(self, base_data):
        pass

    def init_server_data(self, server_data):
        self.progress = server_data.get('progress', 0)
        self.group_id = server_data.get('group_id', 0)
        self.state = server_data.get('state', 0)
        self.is_occupy = server_data.get('is_occupy', False)

    def play_vx_animation(self):
        if not self._nd.IsPlayingAnimation('show_light'):
            self._nd.PlayAnimation('show_light')

    def stop_vx_animation(self):
        if self._nd.IsPlayingAnimation('show_light'):
            self._nd.StopAnimation('show_light')
            self._nd.RecoverAnimationNodeState('show_light')

    def update_occupy_state(self, data, is_init=False):
        if not self._nd:
            return
        else:
            group_id = data.get('group_id', 0)
            state = data.get('state', 0)
            is_occupy = data.get('is_occupy', False)
            progress = data.get('progress', 0)
            if group_id == self.group_id and state == self.state and is_occupy == self.is_occupy and not is_init and self.progress == progress:
                return
            self.progress = data.get('progress', 0)
            self.group_id = group_id
            self.state = state
            self.is_occupy = is_occupy
            if self.state == OCCUPY_POINT_STATE_IDLE or self.state == OCCUPY_POINT_STATE_SNATCH:
                progress_end = 0
                interval = 0
            elif self.state == OCCUPY_POINT_STATE_INC:
                progress_end = (100.0 - self.progress) / self.inc_progress
                interval = self.inc_progress * TICK_TIME
            else:
                progress_end = self.progress / self.dec_progress
                interval = -1.0 * (self.dec_progress * TICK_TIME)
            if self.group_id == STATE_OCCUPY_SELF:
                self._nd.img_prog_blue.setVisible(True)
                self._nd.img_prog_red.setVisible(False)
                prog_nd = self._nd.img_prog_blue
            elif self.group_id == STATE_OCCUPY_ENEMY:
                self._nd.img_prog_blue.setVisible(False)
                self._nd.img_prog_red.setVisible(True)
                prog_nd = self._nd.img_prog_red
            else:
                self._nd.img_prog_blue.setVisible(False)
                self._nd.img_prog_red.setVisible(False)
                prog_nd = self._nd.img_prog_red
            if getattr(self._nd, 'frame_red', None):
                if self.group_id == STATE_OCCUPY_SELF and is_occupy == True:
                    self._nd.frame_red.setVisible(False)
                    self._nd.frame_blue.setVisible(True)
                elif self.group_id == STATE_OCCUPY_ENEMY and is_occupy == True:
                    self._nd.frame_red.setVisible(True)
                    self._nd.frame_blue.setVisible(False)
                else:
                    self._nd.frame_red.setVisible(False)
                    self._nd.frame_blue.setVisible(False)

            def update_progress(pass_time, nd=prog_nd):
                if not nd:
                    return
                if interval == 0 and not is_init:
                    return
                nd.setVisible(True)
                now_progress = round(self.progress + pass_time * interval / TICK_TIME, 2)
                if now_progress >= 100:
                    now_progress = 100
                elif now_progress <= 0:
                    now_progress = 0
                now_progress = float(now_progress * PROG_SCALE + PROG_ADD)
                nd.SetPosition('50%0', now_progress)

            def end_callback():
                if not self._nd:
                    return
                self._nd.nd_cut.StopTimerAction()

            update_progress(0)
            self._nd.nd_cut.StopTimerAction()
            if interval != 0:
                self._nd.nd_cut.TimerAction(update_progress, progress_end, callback=end_callback, interval=TICK_TIME)
            return

    def destory(self):
        self._nd.nd_cut.StopTimerAction()
        self._nd and self._nd.Destroy()
        self._nd = None
        return