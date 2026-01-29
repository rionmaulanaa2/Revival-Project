# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/CCMiniAoiManager.py
from __future__ import absolute_import
import six
import common.utils.timer as timer
import logic.gcommon.const as const
BEARBY_MIN_RADIUS_SQR = (50 * const.NEOX_UNIT_SCALE) ** 2
BEARBY_MAX_RADIUS_SQR = (60 * const.NEOX_UNIT_SCALE) ** 2
NEARBY_STREAM_MAX_COUNT = 5

class CCMiniAoiManager(object):

    def __init__(self):
        self.near_players = []
        self.near_player_steam = {}
        self._aoi_check_timer = global_data.game_mgr.register_logic_timer(self.check_aoi, interval=1.0, times=-1, mode=timer.CLOCK)

    def check_aoi(self):
        if not global_data.player or not global_data.player.logic:
            return
        pos = global_data.player.logic.ev_g_position()
        if not pos:
            return
        in_list = []
        for player in six.itervalues(global_data.war_noteam_puppets):
            if player.sd.ref_nearby_session_mic == 0:
                continue
            player_pos = player.ev_g_position()
            if player_pos and (pos - player_pos).length_sqr < BEARBY_MIN_RADIUS_SQR:
                in_list.append(player)

        out_list = []
        for player in self.near_players:
            if not player.is_valid():
                out_list.append(player)
                continue
            if player.sd.ref_nearby_session_mic == 0:
                out_list.append(player)
                continue
            player_pos = player.ev_g_position()
            if player_pos and (pos - player_pos).length_sqr > BEARBY_MAX_RADIUS_SQR:
                out_list.append(player)

        for out_player in out_list:
            self.near_players.remove(out_player)
            streamid = self.near_player_steam[out_player]
            global_data.ccmini_mgr.unextra_stream(const.NEAR_SESSION_ID, streamid)

        for in_player in in_list:
            if len(self.near_players) >= NEARBY_STREAM_MAX_COUNT:
                break
            if in_player in self.near_players:
                continue
            streamid = in_player.sd.ref_nearby_streamid
            self.near_players.append(in_player)
            self.near_player_steam[in_player] = streamid
            global_data.ccmini_mgr.extra_stream(const.NEAR_SESSION_ID, streamid)

    def destroy(self):
        for player in self.near_players:
            streamid = self.near_player_steam[player]
            global_data.ccmini_mgr.unextra_stream(const.NEAR_SESSION_ID, streamid)

        self.near_players = []
        self.near_player_steam = {}
        if self._aoi_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._aoi_check_timer)
            self._aoi_check_timer = None
        return