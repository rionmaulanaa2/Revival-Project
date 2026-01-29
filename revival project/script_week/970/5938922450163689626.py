# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/CCMiniFactionAoiManager.py
from __future__ import absolute_import
import six
import common.utils.timer as timer
import logic.gcommon.const as const
from mobile.common.EntityManager import EntityManager
NEARBY_MIN_RADIUS_SQR = (50 * const.NEOX_UNIT_SCALE) ** 2
NEARBY_MAX_RADIUS_SQR = (60 * const.NEOX_UNIT_SCALE) ** 2

class CCMiniFactionAoiManager(object):

    def __init__(self):
        self.near_players = []
        self.near_players_stream = {}
        self.near_players_ids = set()
        self.aoi_check_timer = global_data.game_mgr.register_logic_timer(self.check_aoi, interval=1.0, times=-1, mode=timer.CLOCK)

    def check_aoi(self):
        player = global_data.player
        if not player or not player.logic:
            return
        else:
            pos = player.logic.ev_g_position()
            if not pos:
                return
            my_faction = player.logic.ev_g_camp_id()
            if my_faction is None:
                return
            in_list = []
            in_player_ids = set()
            for player in six.itervalues(global_data.war_noteam_puppets):
                if not player.is_valid():
                    continue
                if player.sd.ref_camp_id != my_faction:
                    continue
                player_pos = player.ev_g_position()
                if player_pos and (pos - player_pos).length_sqr < NEARBY_MIN_RADIUS_SQR:
                    in_list.append(player)
                    in_player_ids.add(player.id)

            out_player_ids = set()
            for player_id in self.near_players_ids:
                ent = EntityManager.getentity(player_id)
                if not ent or not ent.logic or not ent.logic.is_valid():
                    out_player_ids.add(player_id)
                    continue
                player_pos = ent.logic.ev_g_position()
                if player_pos and (pos - player_pos).length_sqr > NEARBY_MAX_RADIUS_SQR:
                    out_player_ids.add(player_id)

            for player_id in out_player_ids:
                if player_id in self.near_players_ids:
                    self.near_players_ids.remove(player_id)
                    streamid = self.near_players_stream.pop(player_id, None)
                    streamid and global_data.ccmini_mgr.unextra_stream(const.NEAR_SESSION_ID, streamid)

            for player_id in in_player_ids:
                if len(self.near_players_ids) >= const.NEARBY_STREAM_MAX_COUNT:
                    break
                if player_id in self.near_players_ids:
                    continue
                ent = EntityManager.getentity(player_id)
                if not ent or not ent.logic or not ent.logic.is_valid():
                    continue
                streamid = ent.logic.sd.ref_nearby_streamid
                if not streamid:
                    continue
                self.near_players_ids.add(player_id)
                self.near_players_stream[player_id] = streamid
                global_data.ccmini_mgr.extra_stream(const.NEAR_SESSION_ID, streamid)

            return

    def destroy(self):
        for player_id in self.near_players_ids:
            streamid = self.near_players_stream.get(player_id)
            streamid and global_data.ccmini_mgr.unextra_stream(const.NEAR_SESSION_ID, streamid)

        self.near_players = []
        self.near_players_stream = {}
        self.near_players_ids.clear()
        if self.aoi_check_timer:
            global_data.game_mgr.unregister_logic_timer(self.aoi_check_timer)
            self.aoi_check_timer = None
        return