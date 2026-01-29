# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBattleReplay.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, List, Str, Int
import base64
from mobile.common.ProtoEncoder import ProtoEncoder
from logic.gutils.ConnectHelper import ConnectHelper
import zlib
import os
from logic.entities.BattleReplay import BattleReplay
from logic.entities.BattleReplay import BattleReplayTipMgr
from logic.gcommon import const
from mobile.common.IdManager import IdManager
from logic.gcommon import time_utility as tutil
from datetime import date, timedelta
import game3d
import hashlib
import six.moves.collections_abc
import collections
from logic.gutils import delay
from logic.manager import Manager
import six

class impBattleReplay(object):
    MAX_PRE_CACHED_MSG_SIZE = 300

    def _init_battlereplay_from_dict(self, bdict):
        self._decode_replay_frame_size = bdict.get('decode_replay_frame_size', 100)
        self.proto_encoder = ProtoEncoder(ConnectHelper.GATE_CLIENT_CONFIG.get('proto', 'BSON'))
        self._battle_replaying_status = False
        self._battle_replay = None
        self._download_queue = collections.defaultdict(list)
        self._download_size = collections.defaultdict(int)
        self._record_meta_infos = {}
        self._encrypt_keys = {}
        self._decode_timer = None
        self._left_frame_data = None
        self._is_speed_up = False
        return

    def _read_record_call_back(self, record_name, record_check_sum):
        if not record_name:
            return
        if self.check_is_processing_request():
            return
        file_path = impBattleReplay._get_local_file_path(record_name)
        if not os.path.isfile(file_path):
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_CLIENT_FILE_DOWNLOAD_ERROR, {'record_name': record_name})
            return
        BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_DECODING_RECORD, {'record_name': record_name})
        try:
            first_key_frame, replay_frames = self._decode_file(record_name, file_path, record_check_sum)
            if first_key_frame and replay_frames:
                self._play_replay_record(record_name, first_key_frame, replay_frames)
            else:
                raise ValueError('_decode_file %s failed.' % file_path)
        except Exception as e:
            if os.path.isfile(file_path):
                os.remove(file_path)
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_CLIENT_VALIDATE_FAILED, {'record_name': record_name})
            log_error('_read_record_call_back record name=%s, exception=%s' % (record_name, repr(e)))

    def _get_record_list_call_back(self, query_params, record_meta_infos):
        for meta_info in record_meta_infos:
            self._record_meta_infos[meta_info['record_name']] = meta_info

        if query_params and query_params.get('for_validate', False):
            self._get_record_validate_info_call_back(record_meta_infos[0] if record_meta_infos else None)
        global_data.emgr.replay_download_record_list.emit(query_params, record_meta_infos)
        return

    def _get_record_validate_info_call_back(self, record_meta_info):
        if not record_meta_info:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_SERVER_NOT_FOUND_VALIDATE_INFO)
            return
        else:
            record_name = record_meta_info.get('record_name', None)
            origin_check_sum = record_meta_info.get('check_sum', None)
            if not record_name or not origin_check_sum:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_SERVER_INTERNAL_ERROR)
                return
            self._record_meta_infos[record_name] = record_meta_info
            self._read_record_call_back(record_name, origin_check_sum)
            return

    def battle_replay_show_record_list(self):
        record_infos = []
        for record_name, meta_info in six.iteritems(self._record_meta_infos):
            output_info = {}
            for k, v in six.iteritems(meta_info):
                if k not in ('ek', 'check_sum'):
                    output_info[k] = v

            record_infos.append(output_info)

        return record_infos

    def _decode_frame_(self, frame):
        frame = base64.b64decode(frame)
        frame = self.proto_encoder.decode(frame)
        return frame

    @staticmethod
    def get_encrypt_key--- This code section failed: ---

 138       0  LOAD_FAST             0  'record_name'
           3  POP_JUMP_IF_TRUE     20  'to 20'

 139       6  LOAD_GLOBAL           0  'log_error'
           9  LOAD_CONST            1  'impBattleReplay get_encrpy_key record_name None.'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

 140      16  LOAD_CONST            0  ''
          19  RETURN_END_IF    
        20_0  COME_FROM                '3'

 141      20  RETURN_VALUE     
          21  RETURN_VALUE     
          22  RETURN_VALUE     
          23  LOAD_CONST            0  ''
          26  LOAD_CONST            2  -1
          29  BUILD_SLICE_3         3 
          32  BINARY_SUBSCR    
          33  LOAD_CONST            3  'moc.esaeten'
          36  BINARY_ADD       
          37  LOAD_FAST             0  'record_name'
          40  BINARY_ADD       
          41  LOAD_CONST            4  'netease.com'
          44  BINARY_ADD       
          45  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 20

    @staticmethod
    def _encrypt_raw_data(record_name, raw_data):
        encrypt_key = impBattleReplay.get_encrypt_key(record_name)
        if raw_data:
            from mobile.common.SessionEncrypter import ARC4Crypter
            return ARC4Crypter(key=encrypt_key).encrypt(raw_data)
        else:
            log_error('impBattleReplay _encrypt_raw_data raw_data None.')
            return None
            return None

    @staticmethod
    def _decrypt_data(record_name, encrypted_data):
        from mobile.common.SessionEncrypter import ARC4Crypter
        encrypt_key = impBattleReplay.get_encrypt_key(record_name)
        return ARC4Crypter(key=encrypt_key).decrypt(encrypted_data)

    def _decode_file(self, record_name, file_path, origin_check_sum):
        self._destroy_replay()
        if not record_name or not os.path.isfile(file_path):
            return (None, None)
        else:
            with open(file_path, 'rb') as in_file:
                encrpted_data = in_file.read()
                frames = impBattleReplay._decrypt_data(record_name, encrpted_data)
                import six
                local_check_sum = hashlib.md5(six.ensure_binary(frames)).hexdigest()
                if origin_check_sum and local_check_sum != origin_check_sum:
                    return (None, None)
            if not frames:
                log_error('_decode_file failed to decode file=%s', file_path)
                return (None, None)
            frames_text_data = frames.splitlines()
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                init_frames = frames_text_data
                self._left_frame_data = []
            else:
                init_frames = frames_text_data[:const.REPLAY_MIN_FRAMES_TO_SAVE]
                self._left_frame_data = frames_text_data[const.REPLAY_MIN_FRAMES_TO_SAVE:]
            replay_frames = []
            first_key_frame = self._decode_frame_(init_frames[0])
            for frame_index, frame in enumerate(init_frames[1:]):
                frame = self._decode_frame_(frame)
                if first_key_frame:
                    replay_frames.append(frame)

            print('-----first_key_frame', first_key_frame)
            print('--impBattleReplay _decode_file', len(first_key_frame or {}), len(replay_frames or []))
            return (
             first_key_frame, replay_frames)

    def begin_decode_replay_frame_loop(self):
        if self._battle_replay and self._left_frame_data:
            self._decode_timer = Manager().delay_exec(1.2, self._decode_frame_loop)

    def has_left_replay_frames(self):
        if self._left_frame_data:
            return True
        return False

    def _decode_frame_loop(self):
        self._decode_timer = None
        if not self._battle_replay or not self._left_frame_data:
            return
        else:
            if self._battle_replay.get_cached_msg_size() >= impBattleReplay.MAX_PRE_CACHED_MSG_SIZE:
                self._decode_timer = Manager().delay_exec(1.2, self._decode_frame_loop)
                return
            decode_size = min(self._decode_replay_frame_size, impBattleReplay.MAX_PRE_CACHED_MSG_SIZE)
            if len(self._left_frame_data) < decode_size:
                decode_size = len(self._left_frame_data)
            print('impBattleReplay _decode_frame_loop decode_size=', decode_size, ', left_frame size=', len(self._left_frame_data))
            replay_frames = []
            for frame in self._left_frame_data[:decode_size]:
                frame = self._decode_frame_(frame)
                replay_frames.append(frame)

            self._battle_replay.append_frames(replay_frames)
            self._left_frame_data = self._left_frame_data[decode_size:]
            if self._left_frame_data:
                self._decode_timer = Manager().delay_exec(1.2, self._decode_frame_loop)
            else:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_ALL_FRAME_LOADED)
                print('impBattleReplay _decode_frame_loop all frame decode finished.')
            return

    @staticmethod
    def _get_local_file_path(record_name):
        if not record_name:
            return None
        else:
            file_dir = game3d.get_doc_dir() + '/replayRecords'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = os.path.join(file_dir, record_name)
            return file_path

    def _play_replay_record(self, record_name, first_key_frame, replay_frames):
        try:
            self._battle_replay = BattleReplay(None, record_name, IdManager.genid())
            self._battle_replay.prepare_replay_data(first_key_frame, replay_frames)
        except Exception as e:
            self._destroy_replay()
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_CLIENT_PLAYING_RECORD_ERROR, {'record_name': record_name})
            log_error('_play_replay_record failed exception=%s' % repr(e))

        return

    def check_is_processing_request(self, show_tip=False):
        if self._battle_replay and not self._battle_replay.has_stop_playing():
            if show_tip:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_RECORD_IS_PLAYING, {'record_name': self._battle_replay.get_playing_record_name()})
            return True
        if self._download_queue:
            if show_tip:
                for record_name in six_ex.keys(self._download_queue):
                    BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_RECORD_IS_DOWNLOADING, {'record_name': record_name})
                    break

            return True
        return False

    def play_battle_record(self, record_name):
        if self.check_is_processing_request(show_tip=True):
            return
        else:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_HAS_RECEIVE_PLAY_REQUEST, {'record_name': record_name})
            record_file_path = impBattleReplay._get_local_file_path(record_name)
            if os.path.isfile(record_file_path):
                self._read_record_call_back(record_name, None)
            else:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_BEGIN_DOWNLOADING_FILE, {'record_name': record_name})
                self.battle_replay_get_record(record_name)
            return

    def is_battle_replaying(self):
        return self.check_is_processing_request()

    def _destroy_replay(self):
        if self._battle_replay:
            self._battle_replay.stop_replay(show_lobby=False)
            self._battle_replay = None
            self._left_frame_data = None
        if self._decode_timer:
            delay.cancel(self._decode_timer)
            self._decode_timer = None
        self._is_speed_up = False
        return

    def battle_replay_stop(self):
        if not self._battle_replay:
            return True
        else:
            if self._battle_replay and not self._battle_replay.can_close_immediately():
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_WAIT_SCENE_TO_CLOSE)
                return False
            if self._battle_replay:
                self._battle_replay.stop_replay(show_lobby=True)
                self._battle_replay = None
            self._is_speed_up = False
            return True

    def battle_replay_start(self):
        self._battle_replay.begin_replay()

    def play_battle_record_speed_up(self, key_frame_num=1):
        if key_frame_num <= 0:
            key_frame_num = 1
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_NOT_SUPPORT_SPEED_UP)
            return
        if global_data.player.is_battle_replaying() and self._battle_replay:
            if self._is_speed_up:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_SPEED_UP_WAIT)
                return
            self._is_speed_up = True
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_SPEED_UP_WAIT)
            num = self._battle_replay.speed_up(key_frame_num)
            if num > 0:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_SPEED_UP_FRAMES, {'num': num})
            else:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_SPEED_UP_FAIL)
            self._is_speed_up = False
        else:
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_PLAY_STOP)

    def battle_replay_get_record_list(self, query_params=None):
        if not query_params:
            start_time = date.today() - timedelta(7)
            start_time = start_time.strftime('%Y%m%d%H%M%S')
            end_time = tutil.get_time_string(fmt='%Y%m%d%H%M%S')
            query_params = {'start_time': start_time,'end_time': end_time}
        self.call_server_method('battle_replay_get_record_list', {'query_params': query_params})

    def battle_replay_get_record(self, record_name):
        if record_name in self._download_queue:
            self._download_queue.pop(record_name)
        if record_name in self._download_size:
            self._download_size.pop(record_name)
        self.call_server_method('battle_replay_get_record', {'record_name': record_name})

    def battle_replay_get_record_validate_info(self, record_name):
        if not record_name:
            return
        if record_name in self._record_meta_infos:
            self._get_record_validate_info_call_back(self._record_meta_infos[record_name])
            return
        query_params = {'record_name': record_name,'for_validate': True}
        self.call_server_method('battle_replay_get_record_list', {'query_params': query_params})

    @rpc_method(CLIENT_STUB, (Dict('query_params'), List('record_meta_infos')))
    def battle_replay_receive_record_list(self, query_params, record_meta_infos):
        self._get_record_list_call_back(query_params, record_meta_infos)

    @rpc_method(CLIENT_STUB, (Str('record_name'), Int('record_total_size'), Str('part')))
    def battle_replay_download_record_part(self, record_name, record_total_size, part):
        if not record_name or record_total_size <= 0 or not part:
            log_error('battle_replay_download_record_part method args error.')
            return
        self._download_queue[record_name].append(part)
        self._download_size[record_name] += len(part)
        progress = int(self._download_size[record_name] / float(record_total_size) * 100)
        global_data.emgr.replay_download_progress.emit(record_name, progress)
        ui_inst = global_data.ui_mgr.get_ui('ReplayDownloadProgressUI')
        if not ui_inst:
            ui_inst = global_data.ui_mgr.show_ui('ReplayDownloadProgressUI', 'logic.comsys.replay')
        if not ui_inst.isVisible():
            ui_inst.show()

    @rpc_method(CLIENT_STUB, (Str('record_name'), Dict('record_meta_info')))
    def battle_replay_download_record_end(self, record_name, record_meta_info):
        if not record_name or not record_meta_info:
            log_error('battle_replay_download_record_end method args error.')
            BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_SERVER_INTERNAL_ERROR)
            return
        else:
            record_check_sum = record_meta_info.get('check_sum', None)
            self._record_meta_infos[record_name] = record_meta_info
            record_file_path = impBattleReplay._get_local_file_path(record_name)
            try:
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_INFO_CLIENT_BEGIN_DECOMPRESS_FILE, {'record_name': record_name})
                if six.PY2:
                    all_part_data = ''.join(self._download_queue.get(record_name, []))
                else:
                    all_part_data = ''.join(self._download_queue.get(record_name, []))
                if not all_part_data:
                    raise ValueError('battle_replay_download_record_end merge data error, with record name=%s' % record_name)
                decompressed_data = zlib.decompressobj(15).decompress(all_part_data)
                if not decompressed_data:
                    raise ValueError('battle_replay_download_record_end decompress error, with record name=%s' % record_name)
                if record_check_sum:
                    download_record_check_sum = hashlib.md5(six.ensure_binary(decompressed_data)).hexdigest()
                    if download_record_check_sum != record_check_sum:
                        raise ValueError('battle_replay_download_record_end check sum error, with record name=%s' % record_name)
                with open(record_file_path, 'wb') as f:
                    encrypted_data = impBattleReplay._encrypt_raw_data(record_name, decompressed_data)
                    f.write(encrypted_data)
                self._download_queue.pop(record_name)
                self._download_size.pop(record_name)
            except Exception as e:
                log_error('battle_replay_frame_end record_name=%s, exception=%s' % (record_name, repr(e)))
                BattleReplayTipMgr.show_tip(const.REPLAY_TIP_ERROR_CLIENT_FILE_DOWNLOAD_ERROR, {'record_name': record_name})
                if os.path.isfile(record_file_path):
                    os.remove(record_file_path)
                if record_name in self._download_queue:
                    self._download_queue.pop(record_name)
                if record_name in self._download_size:
                    self._download_size.pop(record_name)

            self._read_record_call_back(record_name, record_check_sum)
            return

    @rpc_method(CLIENT_STUB, (Int('error_code'), Dict('error_params')))
    def battle_replay_error_msg(self, error_code, error_params):
        log_error('battle_replay_error_msg errorCode=%d, error_params=%s' % (error_code, repr(error_params)))
        record_name = error_params.get('record_name', '')
        if record_name:
            BattleReplayTipMgr.show_tip(error_code, {'record_name': record_name})
        else:
            BattleReplayTipMgr.show_tip(error_code)