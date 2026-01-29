# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/audio/ccmini_mgr.py
from __future__ import absolute_import
import six
from six.moves import range
from common.framework import Singleton
import ccmini
import logic.gcommon.const as const
import json
import time
import common.utils.timer as timer
import game3d
import voice
import os
from logic.gcommon.common_const.voice_const import CLOSE_CHANNEL, TEAM_CHANNEL, GROUP_CHANNEL
CMD_CREATE_SESSION = 'create-session'
CMD_LOGIN_SESSION = 'login-session'
CMD_START_CAPTURE = 'start-capture'
CMD_STOP_CAPTURE = 'stop-capture'
CMD_LOGOUT_SESSION = 'logout-session'
CMD_DESTROY_SESSION = 'destroy-session'
CMD_AUTO_DEL_HOME = 'auto-deal-home'
CMD_GET_SPEAKING_LIST = 'get-speaking-list'
CMD_RESET_ENGINE = 'reset-engine'
CMD_STOP_ENGINE = 'stop-engine'
CMD_SET_PLAYBACK_VOL = 'set-playback-vol'
CMD_IGNORE_VOICE = 'ignore-voice'
CMD_NOTIFY_HOME = 'notify-home'
CMD_AUTO_DEL_CATEGORY = 'auto-deal-category'
SESSION_STATE_NONE = 0
SESSION_STATE_CREATE = 1
SESSION_STATE_LOGIN = 2
MAX_SESSION_COUNT = 8
ENGINE_STATE_NONE = 0
ENGINE_STATE_INIT_SUCCEED = 1
ENGINE_STATE_START_SUCCEED = 2
IOS_CAPTURE_VOL = 2
ANDROID_CAPTURE_VOL = 1
LOBBY_TEAM_SPEAKER = 'ccmini_battle_group_speaker'
LOBBY_TEAM_MIC = 'ccmini_battle_group_mic'

class CCMiniMgr(Singleton):
    ALIAS_NAME = 'ccmini_mgr'

    def init(self):
        self.loginSessionData = ''
        self.is_start = False
        self._reset_count = 0
        self._timer = None
        self._check_speaking_list_timer = None
        self._save_team_energy = {}
        self._save_team_list = {}
        self._wait_create_session = []
        self._wait_login_session = []
        self._wait_nearby_stream = []
        self._session_state = [ SESSION_STATE_NONE for i in range(MAX_SESSION_COUNT) ]
        self._engine_state = ENGINE_STATE_NONE
        self._login_session_data = [ {} for i in range(MAX_SESSION_COUNT) ]
        self._eid_to_uid_map = {}
        self._uid_to_entityid_map = {}
        self._entityid_to_eid_map = {}
        self._uid_to_eid_map = {}
        self._session_state_record = {}
        self._ignore_voice_record = {}
        self.duplicated_player_mute_recored = {}
        self._message_type_map = {'connect-change': self.handle_connect_change,
           'engine-state': self.handle_engine_state,
           'ban-change': self.handle_ban_change,
           'create-session': self.handle_create_session,
           'login-session': self.handle_login_session,
           'logout-session': self.handle_logout_session,
           'get-speaking-list': self.handle_speaking_list
           }
        global_data.emgr.on_mic_permission_event += self.on_mic_premission_cb
        self.setting_key_speaker = LOBBY_TEAM_SPEAKER
        self.setting_key_mic = LOBBY_TEAM_MIC
        return

    def set_team_keys(self, key_speaker, key_mic):
        self.setting_key_speaker = key_speaker
        self.setting_key_mic = key_mic

    def start(self):
        if self.is_start:
            return
        self.is_start = True
        if self._engine_state == ENGINE_STATE_NONE:
            ccmini.start()
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                self.auto_deal_category()
        if not self._timer:
            self._timer = global_data.game_mgr.register_logic_timer(self.on_timer, interval=4, times=-1, mode=timer.LOGIC)
        self.create_session(const.TEAM_SESSION_ID)
        self.create_session(const.TEAM_ALL_SESSION_ID)

    def close(self):
        self.destroy_session(const.TEAM_SESSION_ID)
        self.destroy_session(const.TEAM_ALL_SESSION_ID)
        if self._engine_state != ENGINE_STATE_NONE:
            if self._timer:
                global_data.game_mgr.unregister_logic_timer(self._timer)
                self._timer = None
            ccmini.close()
            self._engine_state = ENGINE_STATE_NONE
        self.is_start = False
        return

    def create_speaking_list_timer(self):
        if not self._check_speaking_list_timer:
            self._check_speaking_list_timer = global_data.game_mgr.register_logic_timer(self.on_speaking_list_timer, interval=15, times=-1, mode=timer.LOGIC)

    def destroy_speaking_list_timer(self):
        if self._check_speaking_list_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_speaking_list_timer)
            self._check_speaking_list_timer = None
        return

    def on_speaking_list_timer(self):
        if self._engine_state == ENGINE_STATE_NONE:
            return
        for session_id in range(len(self._session_state)):
            session_state = self._session_state[session_id]
            if session_state == SESSION_STATE_LOGIN:
                self.get_speaking_list(session_id)

    def on_timer(self):
        ret = ccmini.get_message()
        while ret:
            self.on_message(ret)
            ret = ccmini.get_message()

    def on_message(self, ret):
        message_data = json.loads(ret)
        message_type = message_data['type']
        func = self._message_type_map.get(message_type, None)
        if func:
            func(message_data)
        return

    def handle_engine_state(self, message):
        result = message['result']
        if result == -201:
            self._engine_state = ENGINE_STATE_INIT_SUCCEED
            self.reset_engine()
            for channel_id in self._wait_create_session:
                self.create_session(channel_id)

            self._wait_create_session = []
            self._reset_count = 0
        elif result == -204:
            if self._reset_count > 2:
                self.close()
                return
            self.reset_engine()
            self._reset_count += 1
        elif result == -203:
            self._engine_state = ENGINE_STATE_START_SUCCEED
            for channel_id in self._wait_create_session:
                self.create_session(channel_id)

            self._wait_create_session = []
            self._reset_count = 0
        elif result == -211:
            self._engine_state = ENGINE_STATE_INIT_SUCCEED
        elif result == -205:
            pass
        elif result == -206:
            pass
        elif result == -208:
            pass
        elif result == -209:
            pass

    def handle_connect_change(self, message):
        result = message['result']
        session_id = message['session-id']
        if result == -100:
            self.set_playback_vol(session_id, 100)
            self.init_teammate_talk_state()
        elif result in (-103, -104, -105, -106, -109, -112):
            pass
        elif result == -107:
            pass

    def handle_ban_change(self, message):
        pass

    def handle_create_session(self, message):
        result = message['result']
        session_id = message['session-id']
        if result >= 0:
            self._session_state[session_id] = SESSION_STATE_CREATE
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                self.set_capture_vol(IOS_CAPTURE_VOL)
            else:
                self.set_capture_vol(ANDROID_CAPTURE_VOL)
            if session_id in self._wait_login_session:
                self.login_session(session_id)

    def handle_login_session(self, message):
        result = message['result']
        session_id = message['session-id']
        if result >= 0:
            self.reset_engine()
            self._session_state_record = {}
            self._session_state[session_id] = SESSION_STATE_LOGIN
            self.reset_session_state(session_id)

    def reset_session_state(self, session_id, reset_ignore_voice=False):
        if reset_ignore_voice:
            if session_id in self._ignore_voice_record:
                for eid in list(self._ignore_voice_record[session_id]):
                    self.ignore_voice(session_id, eid, False)

            self.init_teammate_talk_state()
        if session_id in [const.TEAM_SESSION_ID, const.TEAM_ALL_SESSION_ID]:
            required_open_value = GROUP_CHANNEL if session_id == const.TEAM_ALL_SESSION_ID else TEAM_CHANNEL
            team_speaker = global_data.message_data.get_seting_inf(self.setting_key_speaker)
            if team_speaker >= required_open_value:
                self.mute_playback(session_id, 0)
            else:
                self.mute_playback(session_id, 1)
            team_mic = global_data.message_data.get_seting_inf(self.setting_key_mic)
            if team_mic >= required_open_value:
                self.start_capture(session_id)
            else:
                self.stop_capture_ex(session_id)
        elif const.NEAR_SESSION_ID == session_id:
            near_speaker = global_data.message_data.get_seting_inf('ccmini_near_speaker')
            if near_speaker:
                self.mute_playback(session_id, 0)
            else:
                self.mute_playback(session_id, 1)
            near_mic = global_data.message_data.get_seting_inf('ccmini_near_mic')
            if near_mic:
                self.start_capture(session_id)
            else:
                self.stop_capture_ex(session_id)
            for stream in self._wait_nearby_stream:
                self.extra_stream(session_id, stream)

            self._wait_nearby_stream = []

    def handle_logout_session(self, message):
        result = message['result']
        session_id = message['session-id']
        if result >= 0:
            self._session_state[session_id] = SESSION_STATE_CREATE
            if session_id in self._wait_login_session:
                self.login_session(session_id)

    def handle_speaking_list(self, message):
        result = message['result']
        if result >= 0:
            session_id = message['session-id']
            all_list = message['list']
            all_energy = message['energy']
            if all_list != self._save_team_list.get(session_id, []) or all_energy != self._save_team_energy.get(session_id, []):
                self._save_team_list[session_id] = all_list
                self._save_team_energy[session_id] = all_energy
                global_data.emgr.ccmini_team_speaking_list.emit(session_id, all_list, all_energy)

    def create_session(self, session_id):
        if self._engine_state == ENGINE_STATE_NONE:
            if session_id not in self._wait_create_session:
                self._wait_create_session.append(session_id)
            return
        if self._session_state[session_id] != SESSION_STATE_NONE:
            return
        cmd_dict = {'type': 'create-session','session-id': session_id}
        self.send_cmd(cmd_dict)

    def destroy_session(self, session_id):
        if self._session_state[session_id] != SESSION_STATE_NONE:
            cmd_dict = {'type': 'destroy-session','session-id': session_id}
            self.clear_session_record(session_id)
            self.send_cmd(cmd_dict)
            self._session_state[session_id] = SESSION_STATE_NONE
        elif session_id in self._wait_create_session:
            self._wait_create_session.remove(session_id)

    def login_session(self, session_id):
        self.start()
        if self._session_state[session_id] == SESSION_STATE_CREATE and self._login_session_data[session_id]:
            cmd_dict = {'type': 'login-session','session-id': session_id,'info': self._login_session_data[session_id]}
            self.send_cmd(cmd_dict)
            if session_id in self._wait_login_session:
                self._wait_login_session.remove(session_id)
        elif session_id not in self._wait_login_session:
            self._wait_login_session.append(session_id)

    def logout_session(self, session_id):
        if self._session_state[session_id] == SESSION_STATE_LOGIN:
            cmd_dict = {'type': 'logout-session','session-id': session_id}
            self.clear_session_record(session_id)
            self.send_cmd(cmd_dict)
        elif session_id in self._wait_login_session:
            self._wait_login_session.remove(session_id)

    def clear_session_record(self, session_id):
        if session_id in self._ignore_voice_record:
            del self._ignore_voice_record[session_id]
        if session_id in self._session_state_record:
            del self._session_state_record[session_id]

    def is_in_room(self, session_id, login_session_data):
        old_login_session_data = self._login_session_data[session_id]
        is_in = login_session_data.get('streamid') == old_login_session_data.get('streamid')
        return is_in

    def set_capture_vol(self, vol):
        cmd_dict = {'type': 'set-capture-vol','ratio': vol}
        self.send_cmd(cmd_dict)

    def start_capture(self, session_id):
        self.start()
        if self._session_state[session_id] == SESSION_STATE_NONE:
            return
        cmd_dict = {'type': 'start-capture','session-id': session_id}
        self._session_state_record.setdefault(session_id, {})
        self._session_state_record[session_id].update({'stop-capture': False})
        self.send_cmd(cmd_dict)
        global_data.sound_mgr.reset_ignore_mute_check()
        global_data.emgr.ccmini_start_capture.emit()

    def stop_capture_ex(self, session_id):
        if self._session_state[session_id] == SESSION_STATE_NONE:
            return
        cmd_dict = {'type': 'stop-capture','session-id': session_id}
        self._session_state_record.setdefault(session_id, {})
        self._session_state_record[session_id].update({'stop-capture': True})
        self.send_cmd(cmd_dict)
        global_data.emgr.ccmini_stop_capture.emit()

    def stop_capture(self, session_id):
        if self._session_state[session_id] == SESSION_STATE_NONE:
            return
        cmd_dict = {'type': 'stop-capture','session-id': session_id}
        self._session_state_record.setdefault(session_id, {})
        self._session_state_record[session_id].update({'stop-capture': True})
        self.send_cmd(cmd_dict)
        team_mic = global_data.message_data.get_seting_inf(self.setting_key_mic)
        near_mic = global_data.message_data.get_seting_inf('ccmini_near_mic')
        if not (team_mic or near_mic):
            global_data.sound_mgr.Wakeup_bg_app_music()
        global_data.sound_mgr.reset_ignore_mute_check()
        global_data.emgr.ccmini_stop_capture.emit()

    def mute_capture(self, session_id, mute):
        cmd_dict = {'type': 'mute-capture','session-id': session_id,'mute': mute}
        self._session_state_record.setdefault(session_id, {})
        self._session_state_record[session_id].update({'mute_capture': mute})
        self.send_cmd(cmd_dict)

    def mute_playback(self, session_id, mute):
        self._session_state_record.setdefault(session_id, {})
        self._session_state_record[session_id].update({'mute_playback': mute})
        self.start()
        if self._session_state[session_id] != SESSION_STATE_NONE:
            cmd_dict = {'type': 'mute-playback','session-id': session_id,'mute': mute}
            self.send_cmd(cmd_dict)

    def notify_home(self, is_background):
        if global_data.deviceinfo.is_ios_ver_13_1():
            return
        cmd_dict = {'type': 'notify-home','is-background': is_background}
        self.send_cmd(cmd_dict)

    def set_playback_vol(self, session_id, percent):
        if self._session_state[session_id] != SESSION_STATE_NONE:
            cmd_dict = {'type': 'set-playback-vol','session-id': session_id,'percent': percent}
            self._session_state_record.setdefault(session_id, {})
            self._session_state_record[session_id].update({'playback': percent})
            self.send_cmd(cmd_dict)

    def mute_duplicated_session_eid(self, eid, ignore, session_id):
        self.ignore_voice(session_id, eid, ignore)
        if ignore:
            self.duplicated_player_mute_recored[eid] = session_id
        elif eid in self.duplicated_player_mute_recored:
            del self.duplicated_player_mute_recored[eid]

    def ignore_voice(self, session_id, eid, ignore):
        cmd_dict = {'type': 'ignore-voice','session-id': session_id,'eid': eid,'ignore': ignore}
        self._ignore_voice_record.setdefault(session_id, set())
        if ignore:
            self._ignore_voice_record[session_id].add(eid)
        elif eid in self._ignore_voice_record[session_id]:
            self._ignore_voice_record[session_id].remove(eid)
        self.send_cmd(cmd_dict)

    def ignore_voice_by_entity_id(self, entity_id, ignore):
        has_open_dict = {}
        for session_id in range(len(self._session_state)):
            session_state = self._session_state[session_id]
            if session_state != SESSION_STATE_NONE:
                eid = self.get_eid_by_entity_id(entity_id, session_id)
                if eid:
                    if ignore:
                        self.ignore_voice(session_id, eid, ignore)
                    elif not has_open_dict.get(entity_id):
                        if not ignore:
                            has_open_dict[entity_id] = session_id
                        self.ignore_voice(session_id, eid, ignore)

    def test_mic(self, session_id, start):
        cmd_dict = {'type': 'test-mic','session-id': session_id,'start': start}
        self.send_cmd(cmd_dict)

    def extra_stream(self, session_id, stream):
        if self._session_state[session_id] == SESSION_STATE_LOGIN:
            cmd_dict = {'type': 'extra-stream','session-id': session_id,'op': 'listen-stream','stream': stream}
            self.send_cmd(cmd_dict)
        elif stream not in self._wait_nearby_stream:
            self._wait_nearby_stream.append(stream)

    def unextra_stream(self, session_id, stream):
        if self._session_state[session_id] == SESSION_STATE_LOGIN:
            cmd_dict = {'type': 'extra-stream','session-id': session_id,'op': 'unlisten-stream','stream': stream}
            self.send_cmd(cmd_dict)
        elif stream in self._wait_nearby_stream:
            self._wait_nearby_stream.remove(stream)

    def get_speaking_list(self, session_id):
        cmd_dict = {'type': 'get-speaking-list','session-id': session_id}
        self.send_cmd(cmd_dict)

    def get_capture_energy(self, session_id):
        cmd_dict = {'type': 'get-capture-energy','session-id': session_id}
        self.send_cmd(cmd_dict)

    def reset_engine(self):
        cmd_dict = {'type': 'reset-engine'}
        self.send_cmd(cmd_dict)

    def stop_engine(self):
        cmd_dict = {'type': 'stop-engine'}
        self.send_cmd(cmd_dict)

    def auto_deal_category(self):
        cmd_dict = {'type': 'auto-deal-category','category': 'ambient'}
        self.send_cmd(cmd_dict)

    def send_cmd(self, cmd_dict):
        cmd = json.dumps(cmd_dict)
        result = ccmini.control(cmd, 0)
        if result:
            self.on_message(result)

    def set_login_session_info(self, session_id, login_session_data):
        self._login_session_data[session_id] = login_session_data
        cc_eid = login_session_data.get('eid', 0)
        cc_eid and self.set_eid_map(cc_eid, global_data.player.uid, session_id)

    def get_uid_by_eid(self, eid, session_id=const.TEAM_SESSION_ID):
        return self._eid_to_uid_map.get(session_id, {}).get(eid, None)

    def clean_eid_map(self):
        self._eid_to_uid_map = {}
        self._uid_to_eid_map = {}
        self.duplicated_player_mute_recored = {}

    def set_eid_map(self, eid, uid, session_id=const.TEAM_SESSION_ID):
        self._eid_to_uid_map.setdefault(session_id, {})
        self._eid_to_uid_map[session_id].update({eid: uid})
        self._uid_to_eid_map.setdefault(uid, {})
        self._uid_to_eid_map[uid].update({session_id: eid})
        entity_id = self._uid_to_entityid_map.get(uid, None)
        if entity_id:
            self._entityid_to_eid_map.setdefault(entity_id, {})
            self._entityid_to_eid_map[entity_id].update({session_id: eid})
        return

    def get_entity_id_by_eid(self, eid, session_id=const.TEAM_SESSION_ID):
        uid = self.get_uid_by_eid(eid, session_id)
        return self._uid_to_entityid_map.get(uid, 0)

    def get_eid_by_entity_id(self, entity_id, session_id=const.TEAM_SESSION_ID):
        return self._entityid_to_eid_map.get(entity_id, {}).get(session_id, 0)

    def set_entityid_map(self, uid, entityid):
        self._uid_to_entityid_map[uid] = entityid
        session_id_eid_dict = self._uid_to_eid_map.get(uid, {})
        if session_id_eid_dict:
            self._entityid_to_eid_map[entityid] = {}
            for session_id, eid in six.iteritems(session_id_eid_dict):
                self._entityid_to_eid_map[entityid].update({session_id: eid})

    def del_uid_by_entityid(self, entityid):
        fine_uid = None
        for uid, temp_entityid in six.iteritems(self._uid_to_entityid_map):
            if temp_entityid == entityid:
                fine_uid = uid
                break

        if fine_uid:
            del self._uid_to_entityid_map[uid]
        return

    def check_microphone_permission(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            return self.check_android_permission()
        else:
            return voice.check_permission()

    def check_android_permission(self):
        path = game3d.get_doc_dir() + '/android_test.amr'
        if os.path.exists(path):
            os.remove(path)
        status = voice.start_recording(path, 'amr', 1, 8000, 1.0)
        if not status:
            return False
        voice.stop_recording()
        if not os.path.exists(path):
            return False
        return os.path.getsize(path) != 0

    def request_mic_premission(self):

        def on_confirm_clicked(*args):
            voice.check_permission()

        from logic.comsys.common_ui.NormalConfirmUI import TopLevelConfirmUI2
        TopLevelConfirmUI2(content=604101, on_confirm=on_confirm_clicked)

    def on_mic_premission_cb(self, result_code):
        import game3d
        from patch.patch_utils import show_confirm_box
        from logic.gcommon.common_utils.local_text import get_text_by_id
        if result_code == 2:
            if self.is_first_check_permission():
                self.set_first_check_permission()
                return

            def confirm_go_to_setting():
                game3d.go_to_setting()

            def cancel_go_to_setting():
                pass

            show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, get_text_by_id(11017), get_text_by_id(80284), get_text_by_id(19002))
        elif result_code == 1:
            pass

    def is_first_check_permission(self):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        return archive_data.get_field('first_check_permission', 1)

    def set_first_check_permission(self):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        archive_data.set_field('first_check_permission', 0)

    def init_teammate_talk_state(self):
        if not global_data.player.logic:
            return
        voice_block_mate = global_data.player.logic.ev_g_voice_block_mate()
        if voice_block_mate:
            for entityid in voice_block_mate:
                self.ignore_voice_by_entity_id(entityid, 1)