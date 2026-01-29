# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartVirtualAnchor.py
from __future__ import absolute_import
from . import ScenePart

class PartVirtualAnchor(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_refresh_poison_circle_event': 'refresh_poison_circle',
       'target_dead_event': 'on_camera_target_death',
       'target_defeated_event': 'on_camera_target_death',
       'play_virtual_anchor_voice': 'play_virtual_voice'
       }

    def __init__(self, scene, name):
        super(PartVirtualAnchor, self).__init__(scene, name)
        self.sound_mgr = global_data.sound_mgr
        self._anchor_obj = None
        self.cur_voice_priority = None
        self._cur_play_id = None
        self._cur_voice_id = None
        return

    def on_enter(self):
        if self._anchor_obj is None:
            self._anchor_obj = global_data.sound_mgr.register_game_obj('virtual_anchor')
        return

    def on_exit(self):
        if self._anchor_obj is not None:
            global_data.sound_mgr.unregister_game_obj(self._anchor_obj)
            self._anchor_obj = None
        self.sound_mgr = None
        return

    def add_delay_timer(self, delay_time, action_func):
        from common.utils.timer import CLOCK
        timer_id = global_data.game_mgr.register_logic_timer(action_func, interval=delay_time, times=1, mode=CLOCK)
        return timer_id

    def refresh_poison_circle(self, state, refresh_time, last_time, level, poison_point, safe_point, reduct_type):
        count_down_time = 5.0
        from logic.gcommon.time_utility import time
        server_time = time()
        delay_time = refresh_time + last_time - count_down_time - server_time

        def play_voice():
            self.play_virtual_voice('vo1')

        if delay_time > 0:
            self.add_delay_timer(delay_time, play_voice)

    def on_camera_target_death(self, *args):
        self.play_virtual_voice('vo7')

    def play_virtual_voice(self, voice_id):
        if self._anchor_obj is None:
            return
        else:
            global_data.sound_mgr.set_switch('anchor1', voice_id, self._anchor_obj)
            global_data.sound_mgr.post_event_2d('Play_vo1', self._anchor_obj)
            return
            from common.cfg import confmgr
            conf = confmgr.get('anchor_voice_conf', str(voice_id), default={})
            priority = conf.get('priority', 1000)
            is_can_play = False
            if self.cur_voice_priority is None or self.cur_voice_priority >= priority:
                is_can_play = True
            if is_can_play:
                if self._cur_play_id:
                    global_data.sound_mgr.stop_playing_id(self._cur_play_id)
                    self._cur_play_id = None
                self.cur_voice_priority = None
                global_data.sound_mgr.set_switch('anchor1', voice_id, self._anchor_obj)
                self._cur_play_id = global_data.sound_mgr.post_event_2d('Play_vo1', self._anchor_obj)
                self._cur_voice_id = voice_id
                self.cur_voice_priority = priority
            return