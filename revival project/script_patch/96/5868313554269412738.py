# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleBuffProgressUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst
INVINCIBLE_BUFF_IDS = frozenset([
 364,
 409,
 442,
 477,
 479,
 478])

class BattleBuffProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/fight_invincible'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'battle_add_buff': 'update_buff_count_down',
       'battle_add_mecha_buff': 'update_buff_count_down',
       'battle_remove_buff': 'remove_buff',
       'battle_remove_mecha_buff': 'remove_buff',
       'player_destroy_event': 'clear_buff',
       'scene_camera_player_setted_event': 'on_camera_player_setted'
       }

    def on_init_panel(self):
        self.cur_cam_target_id = None
        self._duration = 0
        self._buff_id = None
        self.clear_buff(False)
        self.on_camera_player_setted()
        return

    def on_finalize_panel(self):
        pass

    def update_buff_count_down(self, buff_id, remain_time, add_time, duration, buff_data):
        if buff_id not in INVINCIBLE_BUFF_IDS:
            return
        self._buff_id = buff_id
        self.update_buff_prog(duration, add_time)

    def update_buff_prog(self, duration, add_time):
        from logic.gcommon import time_utility
        pass_time = time_utility.get_server_time() - add_time
        remain_time = duration - pass_time
        if duration > 0 and remain_time > 0:
            self._duration = max(duration, self._duration)
            self.show_buff()

            def finish():
                self.clear_buff()

            def update_progress_time(dt):
                _remain_time = remain_time - dt
                self.panel.progress.SetPercent(_remain_time / self._duration * 100)

            self.panel.progress.stopAllActions()
            self.panel.progress.TimerAction(update_progress_time, remain_time, callback=finish, interval=0.05)
        else:
            self.clear_buff()

    def on_camera_player_setted(self, *args):
        if global_data.cam_lplayer is None:
            self.clear_buff()
        elif global_data.cam_lplayer.id != self.cur_cam_target_id:
            self.clear_buff()
            self.cur_cam_target_id = global_data.cam_lplayer.id
        return

    def remove_buff(self, buff_id, *args, **kwargs):
        if self._buff_id != buff_id:
            return
        self.clear_buff()

    def clear_buff(self, need_ani=True):
        self.panel.progress.stopAllActions()
        self._duration = 0
        self._buff_id = None
        if need_ani:
            self.panel.StopAnimation('disappear')
            self.panel.PlayAnimation('disappear')
            self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('disappear'), lambda : self.hide())
        else:
            self.hide()
        return

    def show_buff(self):
        if self.panel.isVisible():
            return
        self.panel.stopAllActions()
        self.panel.PlayAnimation('show')
        self.show()