# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/BattleReplay.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from logic.entities.BaseClientEntity import BaseClientEntity
from logic.gcommon import const
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import battle_const
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager

class BattleReplay(BaseClientEntity):
    MAX_SPEED_FRAME_PER_TIME = 15

    def __init__(self, battle, record_name, entity_id=None):
        super(BattleReplay, self).__init__(entity_id)
        self._record_name = record_name
        self._replay_frames = None
        self._has_stop = False
        return

    def destroy(self):
        self._reset_data()
        if global_data.player:
            global_data.player.on_player_leave_room((global_data.player.uid, const.ROOM_LEAVE_DISSOLVE))
            global_data.player.destroy_global_spectate()
        super(BattleReplay, self).destroy()

    def get_playing_record_name(self):
        return self._record_name

    def has_stop_playing(self):
        return self._has_stop

    def _reset_data(self):
        self._replay_frames = None
        self._has_stop = False
        return

    def prepare_replay_data(self, first_key_frame, replay_frames):
        battle_data = first_key_frame
        global_data.player.do_start_global_spectate(battle_data, from_file=True)
        self._replay_frames = replay_frames

    def append_frames(self, frames):
        if frames:
            self._replay_frames.extend(frames)
            self._push_frame_to_spectate_mgr()

    def begin_replay(self):
        global_data.player.global_spectate_start()
        BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_PLAY_BEGIN, {'frame_count': len(self._replay_frames)})
        global_data.player.begin_decode_replay_frame_loop()
        self._push_frame_to_spectate_mgr()

    def stop_replay(self, show_lobby=False):
        if not self._replay_frames:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_PLAY_FINISHED)
        else:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_PLAY_STOP)
        self.destroy()
        self._has_stop = True
        if show_lobby:
            lobby_entities = EntityManager.get_entities_by_type('Lobby')
            if lobby_entities:
                for eid, entity in six_ex.items(lobby_entities):
                    lobby = entity
                    break

            else:
                lobby = EntityFactory.instance().create_entity('Lobby', IdManager.genid())
            lobby.init_from_dict({'is_login': False,'combat_state': battle_const.COMBAT_STATE_NONE})

    def can_close_immediately(self):
        return True

    def speed_up(self, key_frame_num):
        return global_data.player.do_global_spectate_speed_up(key_frame_num)

    def _push_frame_to_spectate_mgr(self):
        player = global_data.player
        while self._replay_frames:
            frame_data = None
            try:
                frame_data = self._replay_frames[0]
                msg_type, msg_time, msg = frame_data
                player.do_global_spectate_add_msg(msg_type, msg_time, msg)
                self._replay_frames.pop(0)
            except Exception as e:
                self._replay_frames.pop(0)
                print('----------error, tick msg', frame_data, ' exception ', e)

        return

    def get_cached_msg_size(self):
        return global_data.player.get_global_spectate_cached_size()


class BattleReplayTipMgr(object):
    tip_code_2_tips = {const.REPLAY_TIP_ERROR_SERVER_FUNCITON_OFF: '\xe5\x9b\x9e\xe6\x94\xbe\xe5\x8a\x9f\xe8\x83\xbd\xe5\xb7\xb2\xe6\x9a\x82\xe6\x97\xb6\xe5\x85\xb3\xe9\x97\xad',
       const.REPLAY_TIP_ERROR_SERVER_NO_MATCHING_RECORDS: '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe5\x8c\xb9\xe9\x85\x8d\xe7\x9a\x84\xe5\x9b\x9e\xe6\x94\xbe\xe8\xae\xb0\xe5\xbd\x95',
       const.REPLAY_TIP_ERROR_SERVER_NOT_FOUND_RECORD: '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe5\x9b\x9e\xe6\x94\xbe\xe8\xae\xb0\xe5\xbd\x95{record_name}',
       const.REPLAY_TIP_ERROR_SERVER_INVALID_QUERY_PARAMS: '\xe5\xa4\x84\xe7\x90\x86\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe6\x97\xb6\xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8f\x82\xe6\x95\xb0\xe9\x94\x99\xe8\xaf\xaf',
       const.REPLAY_TIP_ERROR_SERVER_INTERNAL_ERROR: '\xe5\xa4\x84\xe7\x90\x86\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6\xe6\x97\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\x86\x85\xe9\x83\xa8\xe9\x94\x99\xe8\xaf\xaf',
       const.REPLAY_TIP_ERROR_CLIENT_FILE_DOWNLOAD_ERROR: '\xe4\xb8\x8b\xe8\xbd\xbd\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe6\x97\xb6\xe5\x87\xba\xe9\x94\x99',
       const.REPLAY_TIP_ERROR_CLIENT_FILE_DECOMPRESS_ERROR: '\xe8\xa7\xa3\xe5\x8e\x8b\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe6\x97\xb6\xe5\x87\xba\xe9\x94\x99',
       const.REPLAY_TIP_ERROR_CLIENT_FILE_DOWNLOAD_TIMEOUT: '\xe4\xb8\x8b\xe8\xbd\xbd\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe8\xb6\x85\xe6\x97\xb6',
       const.REPLAY_TIP_ERROR_CLIENT_PLAYING_RECORD_ERROR: '\xe6\x92\xad\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe6\x97\xb6\xe5\x87\xba\xe9\x94\x99',
       const.REPLAY_TIP_INFO_CLIENT_RECORD_IS_PLAYING: '\xe6\xad\xa3\xe5\x9c\xa8\xe5\x9b\x9e\xe6\x94\xbe{record_name}\xef\xbc\x8c\xe7\xbb\x93\xe6\x9d\x9f\xe5\x90\x8e\xe5\x8f\xaf\xe7\xbb\xa7\xe7\xbb\xad\xe6\x93\x8d\xe4\xbd\x9c',
       const.REPLAY_TIP_INFO_CLIENT_RECORD_IS_DOWNLOADING: '\xe6\xad\xa3\xe5\x9c\xa8\xe4\xb8\x8b\xe8\xbd\xbd\xe5\x9b\x9e\xe8\xae\xbf\xe6\x96\x87\xe4\xbb\xb6{record_name}\xef\xbc\x8c\xe7\xbb\x93\xe6\x9d\x9f\xe5\x90\x8e\xe5\x8f\xaf\xe7\xbb\xa7\xe7\xbb\xad\xe6\x93\x8d\xe4\xbd\x9c',
       const.REPLAY_TIP_INFO_CLIENT_BEGIN_DOWNLOADING_FILE: '\xe5\xbc\x80\xe5\xa7\x8b\xe4\xb8\x8b\xe8\xbd\xbd\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}\xef\xbc\x8c\xe8\xbf\x99\xe5\x8f\xaf\xe8\x83\xbd\xe4\xbc\x9a\xe8\x8a\xb1\xe8\xb4\xb9\xe6\x82\xa8\xe5\x87\xa0\xe5\x88\x86\xe9\x92\x9f...',
       const.REPLAY_TIP_INFO_CLIENT_BEGIN_DECOMPRESS_FILE: '\xe6\xad\xa3\xe5\x9c\xa8\xe8\xa7\xa3\xe5\x8e\x8b\xe7\xbc\xa9\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}',
       const.REPLAY_TIP_INFO_CLIENT_HAS_RECEIVE_PLAY_REQUEST: '\xe5\xb7\xb2\xe6\x94\xb6\xe5\x88\xb0\xe5\x9b\x9e\xe6\x94\xbe\xe8\xae\xb0\xe5\xbd\x95{record_name}\xe6\x92\xad\xe6\x94\xbe\xe8\xaf\xb7\xe6\xb1\x82.',
       const.REPLAY_TIP_INFO_CLIENT_WAIT_SCENE_TO_CLOSE: '\xe8\xaf\xb7\xe7\xad\x89\xe5\x9c\xba\xe6\x99\xaf\xe5\x8a\xa0\xe8\xbd\xbd\xe5\xae\x8c\xe6\xaf\x95\xe5\x90\x8e\xe5\x85\xb3\xe9\x97\xad\xe5\x9b\x9e\xe6\x94\xbe\xef\xbc\x8c\xe5\x90\xa6\xe5\x88\x99\xe5\x8f\xaf\xe8\x83\xbd\xe5\xbc\x95\xe8\xb5\xb7\xe5\x8d\xa1\xe9\xa1\xbf',
       const.REPLAY_TIP_INFO_CLIENT_DOWNLOAD_PROGRESS: '\xe5\x9b\x9e\xe6\x94\xbe\xe6\x96\x87\xe4\xbb\xb6{record_name}, \xe5\xb7\xb2\xe4\xb8\x8b\xe8\xbd\xbd{progress}%.',
       const.REPLAY_TIP_INFO_CLIENT_PLAY_BEGIN: '\xe6\x92\xad\xe6\x94\xbe\xe5\xbc\x80\xe5\xa7\x8b,\xe5\xbc\x80\xe5\xa4\xb4\xe4\xbc\x9a\xe6\x9c\x89\xe5\xb0\x91\xe9\x87\x8f\xe5\x8d\xa1\xe9\xa1\xbf\xef\xbc\x8c\xe5\xb7\xb2\xe9\xa2\x84\xe5\x8a\xa0\xe8\xbd\xbd{frame_count}\xe5\xb8\xa7',
       const.REPLAY_TIP_INFO_CLIENT_PLAY_FINISHED: '\xe5\x9b\x9e\xe6\x94\xbe\xe8\xae\xb0\xe5\xbd\x95\xe6\x92\xad\xe6\x94\xbe\xe7\xbb\x93\xe6\x9d\x9f',
       const.REPLAY_TIP_INFO_CLIENT_PLAY_STOP: '\xe5\x9b\x9e\xe6\x94\xbe\xe8\xae\xb0\xe5\xbd\x95\xe6\x92\xad\xe6\x94\xbe\xe5\xb7\xb2\xe5\x81\x9c\xe6\xad\xa2',
       const.REPLAY_TIP_ERROR_SERVER_NOT_FOUND_VALIDATE_INFO: '\xe8\x8e\xb7\xe5\x8f\x96\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe9\xaa\x8c\xe8\xaf\x81\xe4\xbf\xa1\xe6\x81\xaf\xe5\xa4\xb1\xe8\xb4\xa5',
       const.REPLAY_TIP_INFO_CLIENT_GET_VALIDATE_INFO: '\xe6\xad\xa3\xe5\x9c\xa8\xe8\x8e\xb7\xe5\x8f\x96\xe9\xaa\x8c\xe8\xaf\x81\xe4\xbf\xa1\xe6\x81\xaf',
       const.REPLAY_TIP_ERROR_CLIENT_VALIDATE_FAILED: '\xe6\x96\x87\xe4\xbb\xb6{record_name}\xe9\xaa\x8c\xe8\xaf\x81\xe5\xa4\xb1\xe8\xb4\xa5',
       const.REPLAY_TIP_INFO_CLIENT_DECODING_RECORD: '\xe6\xad\xa3\xe5\x9c\xa8\xe8\xa7\xa3\xe7\xa0\x81\xe6\x96\x87\xe4\xbb\xb6{record_name}',
       const.REPLAY_TIP_INFO_VERSION_NOT_COMPATIBLE: '\xe9\x9c\x80\xe8\xa6\x81\xe6\x9b\xb4\xe6\x96\xb0\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\x90\x8e\xe9\x87\x8d\xe6\x96\xb0\xe5\xbd\x95\xe5\x88\xb6\xe6\x89\x8d\xe8\x83\xbd\xe6\x92\xad\xe6\x94\xbe',
       const.REPLAY_TIP_INFO_ALL_FRAME_LOADED: '\xe6\x81\xad\xe5\x96\x9c\xef\xbc\x8c\xe6\x89\x80\xe6\x9c\x89\xe5\x86\x85\xe5\xae\xb9\xe5\xb7\xb2\xe5\x8a\xa0\xe8\xbd\xbd\xe5\xae\x8c\xe6\xaf\x95',
       const.REPLAY_TIP_INFO_NOT_SUPPORT_SPEED_UP: '\xe6\x8a\xb1\xe6\xad\x89\xef\xbc\x8c\xe4\xbb\x85PC\xe5\xb9\xb3\xe5\x8f\xb0\xe6\x94\xaf\xe6\x8c\x81\xe5\xbf\xab\xe8\xbf\x9b\xe5\x8a\x9f\xe8\x83\xbd',
       const.REPLAY_TIP_INFO_SPEED_UP_WAIT: '\xe6\xad\xa3\xe5\x9c\xa8\xe5\xbf\xab\xe8\xbf\x9b\xef\xbc\x8c\xe8\xaf\xb7\xe6\x82\xa8\xe7\xa8\x8d\xe7\xad\x89',
       const.REPLAY_TIP_INFO_SPEED_UP_FRAMES: '\xe5\xb7\xb2\xe4\xb8\xba\xe6\x82\xa8\xe8\xb7\xb3\xe8\xbf\x87{num}\xe5\xb8\xa7'
       }

    @staticmethod
    def show_tip(tip_code, tip_params=None):
        tip_text = BattleReplayTipMgr.tip_code_2_tips.get(tip_code, None)
        if not tip_text:
            log_error('BattleReplayTipMgr show tip unknown tip code=%s' % tip_code)
            return
        else:
            if '{' in tip_text and tip_params:
                tip_text = tip_text.format(**tip_params)
            global_data.game_mgr.show_tip(tip_text)
            return