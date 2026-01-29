# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impFileService.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game3d
from logic.gcommon import const
from logic.gcommon import time_utility as tutil
from mobile.common.RpcMethodArgs import Dict
from mobile.common.IdManager import IdManager
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from common.platform.filePicker import FilePicker

class impFileService(object):

    def _init_fileservice_from_dict(self, bdict):
        upload_file_records = bdict.get('upload_file_records', {})
        self._upload_file_records = {self._get_real_file_url(record_name):data for record_name, data in six.iteritems(upload_file_records)}
        self._upload_day_nums = bdict.get('upload_day_nums', {})
        self._request_callbacks = {}
        self._check_high_light_video()
        file_picker_url = bdict.get('file_picker_url', None)
        if file_picker_url:
            FilePicker().set_host_url(file_picker_url)
        return

    def _get_real_file_url(self, record_name):
        return FilePicker().get_real_file_url(record_name)

    def get_file_day_upload_num(self, function_key):
        return self._upload_day_nums.get(function_key, 0)

    def _request_upload_file_token(self, function_key, file_type, timeout, extra_info, callback):
        timeout = min(const.FILE_SERVICE_TIME_OUT_MAX_DAYS * tutil.ONE_DAY_SECONDS, timeout)
        if not extra_info:
            extra_info = {}
        request_id = str(IdManager.genid())
        self._request_callbacks[request_id] = callback
        self.call_server_method('request_file_token', (function_key, request_id, file_type, timeout, extra_info))

    def _request_upload_file_token_list(self, function_key, file_type_list, timeout, extra_info, callback):
        timeout = min(const.FILE_SERVICE_TIME_OUT_MAX_DAYS * tutil.ONE_DAY_SECONDS, timeout)
        if not extra_info:
            extra_info = {}
        request_id = str(IdManager.genid())
        self._request_callbacks[request_id] = callback
        self.call_server_method('request_file_token_list', (function_key, request_id, file_type_list, timeout, extra_info))

    @rpc_method(CLIENT_STUB, (Dict('reply'),))
    def reply_file_token(self, reply):
        request_id = reply.get('request_id')
        callback = self._request_callbacks.get(request_id)
        if not callback:
            return
        callback(reply.get('success', False), reply)
        del self._request_callbacks[request_id]

    @rpc_method(CLIENT_STUB, (Dict('reply'),))
    def reply_file_token_list(self, reply):
        request_id = reply.get('request_id')
        callback = self._request_callbacks.get(request_id)
        if not callback:
            return
        callback(reply.get('success', False), reply)
        del self._request_callbacks[request_id]

    def fs_upload_file(self, function_key, file_type, file_content, file_path, timeout, extra_info, finish_cb):
        record_names = {}

        def upload_callback(status, content, file_type, timeout):
            if status:
                record_name = content.get(u'url') or content.get('url') if type(content) is dict else None
                if record_name:
                    record_names[record_name] = file_type
                    record_name = record_name.split('/')[-1]
                    self._upload_file_save_info(function_key, record_name, file_type, timeout, file_path)
                    finish_cb(True, None, record_names)
                else:
                    finish_cb(False, None, record_names)
            else:
                finish_cb(False, None, record_names)
            return

        def get_token_callback(status, reply):
            if not status or not reply.get('token'):
                finish_cb(False, reply.get('error'), {})
            else:
                FilePicker().upload_to_filepicker(reply.get('token'), file_content, lambda status, status_code, content: upload_callback(status, content, file_type, timeout))

        self._request_upload_file_token(function_key, file_type, timeout, extra_info, get_token_callback)

    def fs_upload_file_list(self, function_key, file_list, timeout, extra_info, finish_cb):
        upload_status_list = []
        record_names = {}

        def upload_callback(index, status, state_code, content, file_type, timeout):
            if status:
                record_name = content.get(u'url') or content.get('url') if type(content) is dict else None
                if record_name:
                    record_names[record_name] = file_type
                    record_name = record_name.split('/')[-1]
                    _, local_path, _ = file_list[index]
                    upload_status_list.append(True)
                    self._upload_file_save_info(function_key, record_name, file_type, timeout, local_path)
                else:
                    upload_status_list.append(False)
            else:
                upload_status_list.append(False)
            if len(upload_status_list) == len(file_list):
                upload_success = True if upload_status_list == [True] * len(file_list) else False
                finish_cb(upload_success, state_code, None, record_names)
            return

        def get_token_callback(status, reply):
            if not status:
                finish_cb(False, -1, reply.get('error'), {})
            else:
                token_list = reply.get('token_list', [])
                if not token_list or len(token_list) != len(file_list):
                    finish_cb(False, -1, reply.get('error'), {})
                else:
                    for index, token in enumerate(token_list):
                        file_type, local_path, file_content = file_list[index]
                        FilePicker().upload_to_filepicker(token, file_content, lambda status, state_code, content, file_type=file_type, timeout=timeout, index=index: upload_callback(index, status, state_code, content, file_type, timeout))

        file_type_list = [ file_type for file_type, path, file_content in file_list ]
        self._request_upload_file_token_list(function_key, file_type_list, timeout, extra_info, get_token_callback)

    def _upload_file_save_info(self, function_key, record_name, file_type, timeout, local_path, extra_info=None):
        extra_info = extra_info or {} if 1 else extra_info
        self.call_server_method('save_file_upload_record', (function_key, record_name, file_type, timeout, local_path, extra_info))
        record_info = {'type': file_type,'timeout': timeout,'timestamp': tutil.get_time(),'local_path': local_path}
        record_info.update(extra_info)
        self._upload_file_records.update({self._get_real_file_url(record_name): record_info})

    @rpc_method(CLIENT_STUB, (Dict('file_record'), Dict('upload_day_nums')))
    def add_file_upload_record(self, file_record, upload_day_nums):
        if file_record:
            self._upload_file_records.update({self._get_real_file_url(record_name):data for record_name, data in six.iteritems(file_record)})
        self._upload_day_nums = upload_day_nums
        global_data.emgr.on_upload_file_day_nums_changed.emit()

    def try_upload_file(self):

        def finish_cb(status, state_code, error, record_names):
            pass

        video_file_dir = game3d.get_doc_dir() + '/replayRecords/smc-highlight-test.mp4'
        with open(video_file_dir, 'rb') as f:
            video_content = f.read()
        img_file_dir = game3d.get_doc_dir() + '/replayRecords/smc-highlight-test.png'
        with open(img_file_dir, 'rb') as f:
            img_content = f.read()
        file_list = [(const.FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_IMG, img_file_dir, img_content),
         (
          const.FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO, video_file_dir, video_content)]
        try:
            self.fs_upload_file_list(const.FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT, file_list, 2 * tutil.ONE_DAY_SECONDS, {}, finish_cb)
        except Exception as e:
            log_error('impFileService try_upload_file except=%s', e)

    def try_upload_video(self, video_path, cover_path, finish_func, store_time=2 * tutil.ONE_DAY_SECONDS):

        def finish_cb(status, state_code, error, record_names):
            if finish_func and callable(finish_func):
                finish_func(status, error, record_names)
            if global_data.is_inner_server:
                print('impFileService try_upload_video finish_cb status=%s, record_names=%s, state_code=%s' % (status, record_names, state_code))

        try:
            with open(video_path, 'rb') as f:
                video_content = f.read()
            with open(cover_path, 'rb') as f:
                img_content = f.read()
            file_list = [(const.FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_IMG, cover_path, img_content),
             (
              const.FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO, video_path, video_content)]
            self.fs_upload_file_list(const.FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT, file_list, store_time, {}, finish_cb)
        except Exception as e:
            log_error('impFileService try_upload_video except=%s', e)
            return False

    def try_upload_shader_collect(self, zip_path, finish_func, store_time=tutil.ONE_DAY_SECONDS):

        def finish_cb(status, error, record_names, file_path=zip_path):
            if finish_func and callable(finish_func):
                finish_func(status, error, record_names, file_path)
            if global_data.is_inner_server:
                print('impFileService try_upload_shader_collect finish_cb status=%s, record_names=%s, error=%s' % (status, record_names, error))

        try:
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            file_type = const.FILE_SERVICE_UPLOAD_TYPE_SHADER_COLLECT
            function_key = const.FILE_SERVICE_FUNCTION_KEY_SHADER_COLLECT
            self.fs_upload_file(function_key, file_type, zip_content, zip_path, store_time, {}, finish_cb)
        except Exception as e:
            log_error('impFileService try_upload_video except=%s', e)
            return False

    def try_upload_usage_collect(self, zip_path, finish_func, store_time=tutil.ONE_DAY_SECONDS):

        def finish_cb(status, error, record_names, file_path=zip_path):
            if finish_func and callable(finish_func):
                finish_func(status, error, record_names, file_path)
            if global_data.is_inner_server:
                print('impFileService try_upload_shader_collect finish_cb status=%s, record_names=%s, error=%s' % (status, record_names, error))

        try:
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            file_type = const.FILE_SERVICE_UPLOAD_TYPE_USAGE_COLLECT
            function_key = const.FILE_SERVICE_FUNCTION_KEY_USAGE_COLLECT
            self.fs_upload_file(function_key, file_type, zip_content, zip_path, store_time, {}, finish_cb)
        except Exception as e:
            log_error('impFileService try_upload_video except=%s', e)
            return False

    def _check_high_light_video(self):
        import os
        from logic.comsys.archive.archive_manager import ArchiveManager
        from logic.comsys.video.video_record_utils import SHARE_SETTING_NAME, SETTING_NAME, SHARE_LOCAL_STORE_TIME, SHARE_LOCAL_FRIEND_STORE_TIME
        archive_data = ArchiveManager().get_archive_data(SHARE_SETTING_NAME)
        archive_data_high = ArchiveManager().get_archive_data(SETTING_NAME)
        del_keys = set()
        for video_url, info in six.iteritems(archive_data):
            is_friend = archive_data.get('is_friend', False)
            is_local = archive_data.get('local', False)
            if is_local:
                path = archive_data.get('path', '')
                if path in archive_data_high:
                    continue
            start_time = archive_data.get('time', 0)
            overdue_time = SHARE_LOCAL_FRIEND_STORE_TIME if is_friend else SHARE_LOCAL_STORE_TIME
            if tutil.get_server_time() - start_time > overdue_time:
                video_path = archive_data.get('path', '')
                _, cover_path, _ = archive_data.get('cover_info', ('', '', ''))
                for path in (video_path, cover_path):
                    if path and os.path.exists(path):
                        try:
                            os.remove(path)
                        except Exception as e:
                            log_error('[impFileService] remove {0} error:{1}'.format(path, str(e)))

                del_keys.add(video_url)

        for v_url in del_keys:
            archive_data.del_field(v_url)

        if del_keys:
            archive_data.save()

    @rpc_method(CLIENT_STUB, (Dict('upload_day_nums'),))
    def update_file_upload_nums(self, upload_day_nums):
        self._upload_day_nums = upload_day_nums
        global_data.emgr.on_upload_file_day_nums_changed.emit()