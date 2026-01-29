# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_concert/ComHumanConcert.py
from __future__ import absolute_import
from ...UnitCom import UnitCom
import logic.gcommon.cdata.status_config as status_config

class ComHumanConcert(UnitCom):
    BIND_EVENT = {'E_START_CONCERT_DANCE': 'on_start_concert_dance',
       'E_STOP_CONCERT_DANCE': 'on_stop_concert_dance',
       'E_PLAY_LIVE_CONCERT_DANCE': 'on_play_concert_dance'
       }

    def __init__(self):
        super(ComHumanConcert, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanConcert, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComHumanConcert, self).destroy()

    def on_start_concert_dance(self, force_clip_name=None):
        from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
        from logic.gutils.concert_utils import get_song_action_sync_start
        if global_data.battle:
            song_idx = global_data.battle.song_idx
            if song_idx is None or song_idx == -1:
                return
            song_start_ts = global_data.battle.get_cur_song_start_ts()
            show_dance_conf = global_data.game_mode.get_cfg_data('play_data').get('show_dance_conf', [])
            if not force_clip_name:
                clip_name = ''
                if 0 <= song_idx < len(show_dance_conf):
                    clip_name = show_dance_conf[song_idx]
            else:
                clip_name = force_clip_name
            if clip_name == self.ev_g_human_performance_clip_name():
                return
            if not clip_name:
                return
            sync_start_time = get_song_action_sync_start(song_idx)
            if song_start_ts and sync_start_time and clip_name:
                from logic.gcommon import time_utility as tutil
                end_time = self.ev_g_get_anim_length(clip_name)
                server_time = tutil.get_server_time()
                passed_time = server_time - song_start_ts - sync_start_time
                if passed_time < end_time:
                    self.send_event('E_START_HUMAN_PERFORMANCE', clip_name, UP_BODY, 1, passed_time, server_time, timeScale=1)
        return

    def on_stop_concert_dance(self, miss_dance=''):
        if not miss_dance:
            self.send_event('E_STOP_HUMAN_PERFORMANCE')
        else:
            if miss_dance == self.ev_g_human_performance_clip_name():
                return
            from logic.gcommon import time_utility as tutil
            from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
            server_time = tutil.get_server_time()
            self.send_event('E_START_HUMAN_PERFORMANCE', miss_dance, UP_BODY, 1, 0, server_time, timeScale=1)

    def on_play_concert_dance(self):
        dance = 'high_call_01'
        from logic.gcommon import time_utility
        server_time = time_utility.get_server_time()
        from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
        self.send_event('E_START_HUMAN_PERFORMANCE', dance, UP_BODY, 1, 0, server_time, timeScale=1, need_weapon=True)