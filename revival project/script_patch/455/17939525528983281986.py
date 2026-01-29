# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/unpack_reader/UnpackGuiReader.py
from __future__ import absolute_import
import game3d
from common.platform.dctool import interface
from common.framework import SingletonBase
import C_file
import json
import zlib
import hashlib
from patch import patch_path
import os
import six
STATE_UNINIT = 0
STATE_INIT_LIST = 1
STATE_INIT_INFO = 2
STATE_INITED = 3
STATE_DOWNLOADING = 4

class UnpackGuiReader(SingletonBase):
    ALIAS_NAME = 'unpack_gui_reader'

    def init(self, *args):
        super(UnpackGuiReader, self).init()
        self.state = STATE_UNINIT
        self.checked_file_dict = {}
        self.recorded_file_dict = {}
        self.loading_file_list = []
        self.loading_file_dict = {}
        self.gui_list_url = None
        self.gui_info_url = None
        self.request_id = 0
        self.init_downloader()
        self.init_list()
        return

    def get_gui_list(self):
        server_conf = C_file.get_res_file('confs/server.json', '')
        server_conf = json.loads(server_conf)
        url_key = 'unpack_gui_list'
        if url_key in server_conf:
            return server_conf[url_key].encode('utf-8')
        url_channel_key = 'unpack_gui_list_channel'
        server_conf[url_channel_key][interface.get_game_id()].encode('utf-8')

    def add_loading_file(self, filename):
        if filename in self.checked_file_dict:
            self.on_gui_file_loaded(filename)
            return
        if filename in self.loading_file_dict:
            return
        self.loading_file_list.append(filename)
        self.loading_file_dict[filename] = 1
        self.check_gui_file()

    def check_gui_file_md5(self, data, md5_str):
        import six
        return hashlib.md5(six.ensure_binary(data)).hexdigest() == md5_str

    def check_gui_file(self):
        if self.state != STATE_INITED:
            return
        if not self.loading_file_list:
            return
        filename = self.loading_file_list[0]
        if filename not in self.recorded_file_dict:
            self.loading_file_list.pop(0)
            del self.loading_file_dict[filename]
            return
        if C_file.find_res_file(filename, ''):
            data = C_file.get_res_file(filename, '')
            if self.check_gui_file_md5(data, self.recorded_file_dict[filename]):
                self.on_gui_file_loaded(filename)
                return
        self.download_gui_file(filename)

    def on_gui_file_loaded(self, filename):
        if filename not in self.checked_file_dict:
            self.checked_file_dict[filename] = 1
        if self.loading_file_list[0] != filename:
            raise
        self.loading_file_list.pop(0)
        del self.loading_file_dict[filename]
        global_data.emgr.on_unpack_gui_ready.emit(filename)
        self.check_gui_file()

    def download_gui_file(self, filename):
        self.state = STATE_DOWNLOADING
        res_filename = 'res/%s' % filename
        file_rel_url = patch_path.convert_to_hashed_file_path(res_filename)
        file_url = self.gui_info_url + file_rel_url
        temp_filename = self.get_temp_filename()
        self.downloader.add_request(file_url, temp_filename, self.on_gui_file_downloaded)

    def on_gui_file_downloaded(self, data):
        self.state = STATE_INITED
        if not self.loading_file_list:
            return
        if not data:
            filename = self.loading_file_list.pop(0)
            del self.loading_file_dict[filename]
            self.add_loading_file(filename)
            return
        filename = self.loading_file_list[0]
        res_filename = 'res/%s' % filename
        file_path = patch_path.get_rw_path(patch_path.get_download_target_path(res_filename))
        dirname = os.path.dirname(file_path)
        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(file_path, 'wb').write(data)
        except:
            pass

        self.check_gui_file()

    def get_temp_filename(self):
        self.request_id += 1
        return 'gui_temp_%d.data' % self.request_id

    def init_list(self):
        self.state = STATE_INIT_LIST
        self.gui_list_url = self.get_gui_list()
        temp_filename = self.get_temp_filename()
        self.downloader.add_request(self.gui_list_url, temp_filename, self.on_download_gui_list_callback)

    def on_download_gui_list_callback(self, data):
        if not data:
            self.init_list()
            return
        else:
            self.gui_info_url = None
            data_list = data.split('\n')
            gui_pattern = 'gui_ios'
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                gui_pattern = 'gui_win32'
            else:
                if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                    gui_pattern = 'gui_android'
                data = None
                for data in data_list:
                    if data.find(gui_pattern) >= 0:
                        break

                if not data:
                    self.init_list()
                    return
            self.gui_info_url = data.strip().encode('utf-8')[:-4] + '/'
            self.init_file_info()
            return

    def init_file_info(self):
        file_info_url = self.gui_info_url + 'gui_file_list.txt'
        self.state = STATE_INIT_INFO
        temp_filename = self.get_temp_filename()
        self.downloader.add_request(file_info_url, temp_filename, self.on_download_gui_info_callback)

    def on_download_gui_info_callback(self, data):
        if not data:
            self.init_file_info()
            return
        self.state = STATE_INITED
        self.init_gui_file_dict(data)
        self.check_gui_file()

    def init_gui_file_dict(self, data):
        file_list = zlib.decompress(six.ensure_binary(data)).split('\n')
        for file_info in file_list:
            if file_info:
                file_info = file_info.split('\t')
                self.recorded_file_dict[file_info[0][4:]] = file_info[1]

    def init_downloader(self):
        self.downloader = None
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            from common.platform.thread_downloader_utils import ThreaderDownloaderHelper
            self.downloader = ThreaderDownloaderHelper()
        else:
            from common.platform.orbit_utils import OrbitHelper
            self.downloader = OrbitHelper()
        return