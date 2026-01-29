# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/VoiceMgrSdk.py
from __future__ import absolute_import
import voice
import game3d
from common.framework import Singleton
import common.http
from hashlib import md5
import os
import time
import audio
from logic.comsys.login.LoginSetting import LoginSetting
from common.platform.dctool import interface
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN
from common.cfg import confmgr
from common.platform import is_ios
from logic.gcommon.common_const.lang_data import *
LANG_TO_STR_MAP = {LANG_CN: 'zh-CN',
   LANG_EN: 'en-US',
   LANG_ZHTW: 'zh-TW',
   LANG_JA: 'ja-JP',
   LANG_KO: 'ko-KR',
   LANG_TH: 'th-TH',
   LANG_ID: ''
   }
VOICE_DIR = 'ngvoice'

class VoiceMgrSdk(Singleton):
    ALIAS_NAME = 'voice_mgr'

    def init(self):
        self._is_playing = False
        self._is_recording = False
        self._is_upload_amr = False
        self._record_time = 0
        self._start_recording_time = 0
        self._send_callback = None
        self._cur_upload_voice_key = ''
        self._url = confmgr.get('channel_conf', interface.get_game_id(), 'VOICE_CHAT_URL')
        self._need_translate_lang = True
        server_info = LoginSetting().last_logined_server or {}
        self._host_num = str(server_info.get('svr_num', '0'))
        self._voice_volume = 1.0
        self._convert_task_list = []
        self._is_in_convert = False
        self._is_init_ngvoice = False
        self._cur_record_file_name = ''
        return

    def init_ngvoice(self):
        if self._is_init_ngvoice:
            return
        self._is_init_ngvoice = True
        lang = get_cur_text_lang()
        try:
            local_path = self.get_local_path()
            if not os.path.exists(local_path):
                os.makedirs(local_path)
        except Exception as e:
            log_error(e)

        json_dict = {'methodId': 'ngVoiceInit',
           'uid': str(global_data.player.uid)
           }
        global_data.channel.extend_func_by_dict(json_dict)
        json_dict = {'methodId': 'ngVoiceSetProp',
           'DEBUG_MODE': '1',
           'LOCAL_PATH': '/%s' % VOICE_DIR if is_ios() else self.get_local_path(),
           'SERVER_PATH': self.get_url(),
           'SERVER_HOST': self._host_num,
           'SERVER_TOUSER': '_1_',
           'USER_AGENT': self.get_project_id(),
           'MAX_DURATION': '60',
           'MIN_DURATION': '0',
           'LANGUAGE': LANG_TO_STR_MAP.get(lang, 'zh-CN'),
           'USE_AILAB_PREFER': '1' if lang == LANG_CN else '0'
           }
        global_data.channel.extend_func_by_dict(json_dict)
        self.set_uid()

    def set_uid(self):
        if not global_data.player:
            log_error('Should not call this when no avatar exists.')
            return
        json_dict = {'methodId': 'ngVoiceSetProp',
           'USERINFO_UID': str(global_data.player.uid)
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def on_update_userinfo(self):
        if not self._is_init_ngvoice:
            return
        self.set_uid()

    def get_local_path(self):
        return os.path.join(game3d.get_doc_dir(), VOICE_DIR)

    def on_voice_init_callback(self, json_dict):
        result = json_dict.get('result')
        if result and not result.get('success'):
            log_error('VoiceMgrSdk ngVoiceInit error')

    def get_volume(self):
        return self._voice_volume

    def set_volume(self, volume):
        self._voice_volume = volume

    def set_send_callback(self, callback):
        self._send_callback = callback

    def is_sdk(self):
        return True

    def is_upload_amr(self):
        return self._is_upload_amr

    def start_recording(self, callback):
        if self._is_upload_amr:
            return
        if self._is_recording:
            self.stop_recording(False)
        else:
            self._is_recording = True
            global_data.sound_mgr.set_background(True)
        self._start_recording_time = time.time()
        global_data.sound_mgr.set_recording(True)
        self._send_callback = callback
        self._cur_record_file_name = '%.0f.amr' % time.time()
        json_dict = {'methodId': 'ntStartRecord',
           'voiceFileName': self._cur_record_file_name
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def stop_recording(self, is_enable):
        global_data.sound_mgr.set_recording(False)
        if self._is_recording:
            self._is_recording = False
            global_data.sound_mgr.set_background(False)
            if is_enable:
                json_dict = {'methodId': 'ntStopRecord'}
                global_data.channel.extend_func_by_dict(json_dict)
            else:
                json_dict = {'methodId': 'ntCancelRecord'}
                global_data.channel.extend_func_by_dict(json_dict)
            global_data.sound_mgr.Wakeup_bg_app_music()

    def on_record_finish(self, json_dict):
        result = json_dict.get('result')
        if result and result.get('success'):
            self._record_time = time.time() - self._start_recording_time
            self.upload_amr(self._cur_record_file_name)

    def play_amr(self, key):
        global_data.sound_mgr.set_recording(True)
        json_dict = {'methodId': 'ntStartPlayback',
           'voiceFilePath': '%s.amr' % key
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def on_playback_finish(self, json_dict):
        global_data.sound_mgr.set_recording(False)
        result = json_dict.get('result')
        if result and not result.get('success'):
            log_error('VoiceMgrSdk on_playback_finish fail')
        self._is_playing = False
        global_data.emgr.chat_voice_empty.emit()

    def play_voice_msg(self, key, callback=None):
        import os
        self._is_playing = True
        path = self.get_local_path()
        if os.path.exists('%s/%s.amr' % (path, key)):
            self.play_amr(key)
        else:
            self.download_amr(key)

    def stop_play_voice(self):
        json_dict = {'methodId': 'ntStopPlayback'
           }
        global_data.channel.extend_func_by_dict(json_dict)
        self._is_playing = False

    def pause_play_voice(self):
        json_dict = {'methodId': 'ntPausePlayback'
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def resume_play_voice(self):
        json_dict = {'methodId': 'ntResumePlayback'
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def clear(self):
        json_dict = {'methodId': 'ntClearVoiceCache',
           'time': 604800
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def upload_amr(self, amr_file):
        self._is_upload_amr = True
        json_dict = {'methodId': 'ntUploadVoiceFile',
           'filePath': amr_file
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def on_upload_finish(self, json_dict):
        self._is_upload_amr = False
        result = json_dict.get('result')
        if not result or result and not result.get('success'):
            log_error('VoiceMgrSdk on_upload_finish fail')
            return
        self._cur_upload_voice_key = result.get('key')
        self.get_recognize_result(self._cur_upload_voice_key)

    def download_amr(self, key):
        json_dict = {'methodId': 'ntDownloadVoiceFile',
           'key': key,
           'voiceFileName': '%s.amr' % key
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def on_download_finish(self, json_dict):
        result = json_dict.get('result')
        if not result or result and not result.get('success'):
            log_error('VoiceMgrSdk on_download_finish fail')
            self._is_playing = False
            return
        self.play_amr(result.get('key'))

    def set_translation_language(self, lang):
        ng_voice_str_language = LANG_TO_STR_MAP.get(lang, 'en-US')
        json_dict = {'methodId': 'ngVoiceSetProp',
           'LANGUAGE': ng_voice_str_language
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def get_recognize_result(self, key):
        json_dict = {'methodId': 'ntGetTranslation',
           'key': key
           }
        global_data.channel.extend_func_by_dict(json_dict)

    def on_translate_finish(self, json_dict):
        result = json_dict.get('result')
        if result.get('errorCode') != 0:
            log_error('VoiceMgrSdk on_translate_finish fail')
            msg_str = ' '
        else:
            msg_str = result.get('translatedText')
        key = result.get('key')
        if key != self._cur_upload_voice_key or not key:
            return
        li = [str(self._record_time), self._cur_upload_voice_key]
        voice_str = '\n'.join(li)
        self.send_voice_msg(msg_str, voice_str)

    def send_voice_msg(self, msg_str, voice_str):
        if msg_str == False:
            msg_str = ''
        if callable(self._send_callback):
            global_data.game_mgr.post_exec(self._send_callback, msg_str, voice_str)
            self._send_callback = None
        return

    def is_playing(self):
        return self._is_playing

    def get_url(self):
        if global_data.channel.is_europe_america_server():
            return 'https://g93us.voice.nie.easebar.com:39690'
        else:
            return self._url

    def get_project_id(self):
        if global_data.channel.is_europe_america_server():
            return 'g93us'
        else:
            return interface.get_project_id()