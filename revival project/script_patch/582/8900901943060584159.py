# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/VoiceMgr.py
from __future__ import absolute_import
from __future__ import print_function
import six
import voice
import game3d
from common.framework import Singleton
import common.http
import os
import time
import audio
from logic.comsys.login.LoginSetting import LoginSetting
from common.platform.dctool import interface
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW
from common.cfg import confmgr
import hashlib
LEAST_RECORD_TIME = 0.5
NOT_PLAY = 0
MANUAL_PLAY = 1
AUTO_PLAY = 2
cur_record_file = 'cur_voice'

class VoiceMgr(Singleton):
    ALIAS_NAME = 'voice_mgr'

    def init(self):
        from poster.streaminghttp import register_openers
        self._play_state = voice.VOICE_PLAYSTATE_END
        self._voice_id = None
        self._is_playing = False
        self._is_recording = False
        self._is_upload_amr = False
        self._record_time = 0
        self._start_recording_time = 0
        self._send_friend_callback = None
        self._send_callback = None
        conf = confmgr.get('channel_conf', interface.get_game_id(), default={})
        self._url = conf.get('VOICE_CHAT_URL')
        self._need_translate_lang = int(conf.get('VOICE_TRANSLATE_LANG'))
        server_info = LoginSetting().last_logined_server or {}
        self._host_num = str(server_info.get('svr_num', '0'))
        self._voice_volume = 1.0
        self._convert_task_list = []
        self._is_in_convert = False
        register_openers()

        def call_back(play_state, voice_id):
            self._voice_id = voice_id
            self._play_state = play_state
            if self._play_state == voice.VOICE_PLAYSTATE_INIT:
                global_data.sound_mgr.set_recording(True)
            if play_state == voice.VOICE_PLAYSTATE_END or play_state == voice.VOICE_PLAYSTATE_STOP:
                global_data.sound_mgr.set_recording(False)
                self._is_playing = False
                global_data.emgr.chat_voice_empty.emit()

        voice.set_voice_cb(call_back)
        return

    def init_ngvoice(self):
        pass

    def on_update_userinfo(self):
        pass

    def get_volume(self):
        return self._voice_volume

    def set_volume(self, volume):
        self._voice_volume = volume

    def is_sdk(self):
        return False

    def set_send_callback(self, callback):
        self._send_callback = callback

    def is_upload_amr(self):
        return self._is_upload_amr

    def start_recording(self, callback):
        if self._is_recording:
            self._is_recording = False
            voice.stop_recording()
        if self._is_upload_amr:
            return
        self._send_callback = callback
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            sound_type = 'wav'
        else:
            sound_type = 'amr'
        path = game3d.get_doc_dir() + '/%s.%s' % (cur_record_file, sound_type)
        status = voice.start_recording(path, sound_type, 1, 8000, 1.0)
        if status:
            self._is_recording = True
            self._start_recording_time = time.time()
            global_data.sound_mgr.set_recording(True)

    def stop_recording(self, is_enable):
        global_data.sound_mgr.set_recording(False)
        if self._is_recording:
            self._is_recording = False
            voice.stop_recording()
            if is_enable:
                self._record_time = time.time() - self._start_recording_time
                if game3d.get_platform() == game3d.PLATFORM_IOS:

                    def callback(*args):
                        self.upload_amr('%s.amr' % cur_record_file)

                    self.convert_voice('%s.wav' % cur_record_file, '%s.amr' % cur_record_file, callback)
                else:
                    self.upload_amr('%s.amr' % cur_record_file)
            global_data.sound_mgr.Wakeup_bg_app_music()

    def play_amr(self, key):
        if self._play_state != voice.VOICE_PLAYSTATE_END and self._play_state != voice.VOICE_PLAYSTATE_STOP:
            voice.stop_voice(self._voice_id)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            voice_file = '%s/%s.wav' % (game3d.get_doc_dir(), key)
            if os.path.exists(voice_file):
                voice.play_voice(voice_file, self._voice_volume)
            else:

                def callback(*args):
                    voice.play_voice(voice_file, self._voice_volume)

                self.convert_voice('%s.amr' % key, '%s.wav' % key, callback)
        else:
            voice_file = '%s/%s.amr' % (game3d.get_doc_dir(), key)
            voice.play_voice(voice_file, self._voice_volume)

    def play_voice_msg(self, key, callback=None):
        import os
        self._is_playing = True
        path = game3d.get_doc_dir()
        if os.path.exists('%s/%s.amr' % (path, key)):
            self.play_amr(key)
        else:
            self.download_amr(key)

    def clear(self):
        path = game3d.get_doc_dir()
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.amr') or name.endswith('.wav'):
                    os.remove(os.path.join(root, name))

    def upload_amr(self, amr_file):
        if not global_data.player:
            return
        if self._host_num == '0':
            server_info = LoginSetting().last_logined_server or {}
            self._host_num = str(server_info.get('svr_num', '0'))
        path = game3d.get_doc_dir() + '/' + amr_file
        if not os.path.exists(path):
            return
        file_handle = open(path, 'rb')
        voice_data = file_handle.read()
        sign = hashlib.md5(six.ensure_binary(voice_data)).hexdigest()
        if six.PY2:
            from poster.encode import multipart_encode
            datagen, header = multipart_encode({'file': file_handle})
        else:
            import urllib3
            datagen, content_type = urllib3.encode_multipart_formdata({'file': (path, voice_data, 'application/octet-stream')})
            header = {'User-Agent': self.get_project_id(),'Content-Type': content_type}
        header['User-Agent'] = self.get_project_id()
        url = '%s/upload?host=%s&usernum=%s&tousers=_1_&md5=%s' % (self.get_url(), self._host_num, global_data.player.uid, sign)

        def callback(ret, url, args):
            file_handle.close()
            if ret == None:
                return
            else:
                ret = six.ensure_str(ret)
                status, key = ret.split('\n', 1)
                if int(status) != 0:
                    print('[ERROR] upload_amr error.')
                    self._is_upload_amr = False
                    return
                self.get_recognize_result(key)
                return

        self._is_upload_amr = True
        common.http.request_v2(url, data=datagen, header=header, callback=callback)

    def download_amr(self, key):
        if self._host_num == '0':
            server_info = LoginSetting().last_logined_server or {}
            self._host_num = str(server_info.get('svr_num', '0'))
        if not global_data.player:
            return
        else:
            url = '%s/getfile?key=%s&host=%s&usernum=%s' % (self.get_url(), key, self._host_num, global_data.player.uid)

            def callback(ret, ret1, ret2):
                status, msg = ret.split('\n', 1)
                if int(status) != 0:
                    print('[ERROR] download_amr error.')
                    return
                voice_file = open('%s/%s.amr' % (game3d.get_doc_dir(), key), 'wb')
                voice_file.write(msg)
                voice_file.close()
                self.play_amr(key)

            header = {'User-Agent': self.get_project_id()}
            common.http.request_v2(url, None, header, callback)
            return

    def get_recognize_result(self, key):
        if get_cur_text_lang() in (LANG_CN, LANG_ZHTW):
            url = '%s/get_translation?key=%s' % (self.get_url(), key)

            def callback(ret, ret1, ret2):
                self._is_upload_amr = False
                if ret == None:
                    return
                else:
                    ret = six.ensure_str(ret)
                    status, msg = ret.split('\n', 1)
                    if int(status) != 0:
                        print('[ERROR] get_recognize_result error.')
                        return
                    li = [
                     str(self._record_time), key]
                    s = '\n'.join(li)
                    self.send_voice_msg(msg, s)
                    return

            header = {'User-Agent': self.get_project_id()}
            common.http.request_v2(url, None, header, callback)
        else:
            self._is_upload_amr = False
            li = [str(self._record_time), key]
            s = '\n'.join(li)
            self.send_voice_msg(' ', s)
        return

    def send_voice_msg(self, msg_str, voice_str):
        if msg_str == False:
            msg_str = ''
        if self._send_callback:
            self._send_callback(msg_str, voice_str)
            self._send_callback = None
        return

    def is_playing(self):
        return self._is_playing

    def convert_voice(self, from_file, to_file, callback):
        self._is_in_convert = True
        from_path = game3d.get_doc_dir() + '/' + from_file
        to_path = game3d.get_doc_dir() + '/' + to_file
        voice.wait_all_convert_tasks()
        voice.on_convert_voice_finish = callback
        voice.convert_voice_async(from_path, to_path)

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