# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/filePicker.py
from __future__ import absolute_import
import six.moves.urllib.parse
import json
from mobile.mobilelog.LogManager import LogManager
from mobile.mobilerpc import SimpleHttpClient2, HttpBase
from mobile.common.mobilecommon import Singleton
from common.platform.dctool import interface
from common.cfg import confmgr

class FilePicker(Singleton):

    def init(self):
        self.logger = LogManager.get_logger(self.__class__.__name__)
        self.get_url_loc = confmgr.get('channel_conf', interface.get_game_id(), 'FILE_PICKER_HOST')
        self.post_url_info = six.moves.urllib.parse.urlparse(self.get_url_loc + 'new/')
        self.http_client = SimpleHttpClient2.SimpleAsyncHTTPClient2()

    def set_host_url(self, url):
        if not url:
            return
        self.get_url_loc = url
        self.post_url_info = six.moves.urllib.parse.urlparse(self.get_url_loc + 'new/')

    def get_real_file_url(self, record_name):
        return self.get_url_loc + record_name

    def upload_to_filepicker(self, token, file_content, callback=None):
        try:
            headers = {'Authorization': token
               }
            request = HttpBase.HttpRequest(self.post_url_info.netloc, 'POST', self.post_url_info.path, headers=headers, body=file_content)
            cb = lambda req, rep, cbfunc=callback: self._reply(req, rep, cbfunc)
            self.http_client.http_request(request, 60, cb)
        except Exception as e:
            self.logger.error('FilePicker upload_to_filepicker Exception=%s.', e)
            if callback:
                callback(False, -1, None)

        return

    def download_from_filepicker(self, file_name, callback=None, mode=0):
        if mode == 0:
            file_url = self.get_url_loc + file_name
        else:
            file_url = file_name
        file_url_info = six.moves.urllib.parse.urlparse(file_url)
        request = HttpBase.HttpRequest(file_url_info.netloc, 'GET', file_url_info.path)
        cb = lambda req, rep, cbfunc=callback: self._reply(req, rep, cbfunc)
        self.http_client.http_request(request, 60, cb)

    def query_info_from_filepicker(self, file_url, info, callback=None):
        file_url_info = six.moves.urllib.parse.urlparse(file_url)
        request = HttpBase.HttpRequest(file_url_info.netloc, 'GET', file_url_info.path + '/info?' + info, usessl=True)
        cb = lambda req, rep, cbfunc=callback: self._reply(req, rep, cbfunc)
        self.http_client.http_request(request, 10, cb)

    def _reply(self, request, reply, callback):
        content = (
         False, None)
        if not reply:
            if callback:
                callback(False, -1, content)
            return
        else:
            header = reply.header.dict
            body = reply.body
            status_code = int(header.get('status_code', 400))
            if status_code >= 400:
                if callback:
                    callback(False, status_code, content)
                return
            try:
                content = json.loads(body)
            except Exception as e:
                log_error('[FilePicker] json loads error:[%s]' % str(e))
                content = body

            if callback:
                callback(True, status_code, content)
            return