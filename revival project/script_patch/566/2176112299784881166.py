# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/downloader_agent/orbit_downloader.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import social
import time
import re
import json
from patch import network_utils
from patch import patch_lang
from patch import lang_data
FILE_RETRY_TIME = 3
from copy import deepcopy
IP_PATTERN = '(\\d+\\.\\d+\\.\\d+\\.\\d+)'
from patch import patch_dctool
FIXED_DOWNLOAD_ID = '1'
ORBIT_NETWORK_LOST = '__DOWNLOAD_NETWORK_LOST__'
ORBIT_CLEAN_CACHE = '__DOWNLOAD_CLEAN_CACHE__'
ORBIT_DNS_RESOLVED = '__DOWNLOAD_DNS_RESOLVED__'
ORBIT_CONFIG = '__DOWNLOAD_CONFIG__'
ORBIT_START = '__DOWNLOAD_START__'
ORBIT_END = '__DOWNLOAD_END__'
DOWNLOADING = False
SPD_RECORD_COUNT = 10
ORBIT_SPACE_OUT_CODE = 5
THREAD_NUMBER = '5'

def set_thread_number(thread_num):
    global THREAD_NUMBER
    THREAD_NUMBER = str(thread_num)


def orbit_result_parser(filename, code):
    if filename == ORBIT_NETWORK_LOST:
        return True
    if filename == ORBIT_CONFIG and code != 0:
        return True
    return False


class OrbitDownloader(object):

    def __init__(self, retqueue, err_queue, msg_queue):
        super(OrbitDownloader, self).__init__()
        self.retqueue = retqueue
        self.err_queue = err_queue
        self.msg_queue = msg_queue
        self.download_map = {}
        self.space_flag = False
        self._need_override = True
        self._acc_bytes = 0.0
        self._all_num = 0
        self._support_end_flag = False
        self.init_download_config()
        self.init_download_env([], 0)

    def get_progress(self):
        if not self.downloading:
            return 1.0
        else:
            new_bytes = social.get_channel().get_download_bytes()
            if self.total_size > 0:
                return (self._acc_bytes + new_bytes) / float(self.total_size)
            return social.get_channel().get_download_progress()

    def init_download_config(self):
        dc_tool = patch_dctool.get_dctool_instane()
        oversea = 0
        if dc_tool.is_tw_package():
            oversea = 2
        elif dc_tool.is_global_package():
            oversea = 2
        proj_id = str(dc_tool.get_project_id())
        if patch_dctool.get_dctool_instane().is_steam_channel():
            proj_id = 'g93'
            if self.is_chinese_client():
                oversea = 0
        self.orbit_common_config = {'methodId': 'download',
           'projectid': proj_id,
           'wifionly': 'false',
           'logopen': 'false',
           'threadnum': THREAD_NUMBER,
           'oversea': oversea
           }
        self.cnt_orbit_config = {}

    def get_avg_spd(self):
        if not self.spd_record:
            return 0
        bytes_diff = self.spd_record[-1][0] - self.spd_record[0][0]
        time_diff = self.spd_record[-1][1] - self.spd_record[0][1]
        if time_diff <= 0:
            return 0
        return bytes_diff * 1.0 / time_diff

    def get_speed(self):
        if not self.downloading:
            return 0
        new_bytes = social.get_channel().get_download_bytes()
        new_check_time = time.time()
        self.spd_record.append((new_bytes, new_check_time))
        rec_len = len(self.spd_record)
        ret_spd = self.get_avg_spd()
        if rec_len > SPD_RECORD_COUNT:
            self.spd_record = self.spd_record[rec_len - SPD_RECORD_COUNT:]
        return ret_spd

    def check_ip_url(self, download_list):
        for item in download_list:
            url = item[2]
            ret = re.search(IP_PATTERN, url)
            if ret:
                return True

        return False

    def generate_orbit_item(self, d_item):
        str_md5 = d_item[4] if len(d_item) >= 5 else 'NotMD5'
        return {'targeturl': d_item[2],
           'filepath': d_item[0],
           'size': d_item[3],
           'md5': str_md5
           }

    def generate_orbit_download_info(self):
        all_num = 0
        self.download_map = {}
        download_items = []
        while self.download_list:
            d_item = self.download_list.pop()
            self.download_map[d_item[0]] = d_item
            orbit_item = self.generate_orbit_item(d_item)
            download_items.append(orbit_item)
            all_num += 1
            if all_num >= 1000:
                break

        download_id_str = str(int(time.time())) if self._need_override else FIXED_DOWNLOAD_ID
        self.cnt_orbit_config['downfile'] = download_items
        self.cnt_orbit_config['downloadid'] = download_id_str

    def init_download_env(self, download_list=[], total_size=0, cb=None, override=True):
        self.download_map = {}
        self.download_list = deepcopy(download_list)
        self.download_str = ''
        self.cnt_orbit_config = deepcopy(self.orbit_common_config)
        self.cnt_orbit_config['threadnum'] = THREAD_NUMBER
        if self.check_ip_url(self.download_list):
            self.cnt_orbit_config['notusecdn'] = 'true'
        if override:
            self.cnt_orbit_config['isrenew'] = 'true'
        self.total_size = total_size
        self.success_list = []
        self.failed_list = []
        self.spd_check_time = time.time()
        self.cb = cb
        self._support_end_flag = False
        self.downloading = False
        self.download_start_time = time.time()
        self.spd_record = [(0, self.download_start_time)]

    def stop_download(self, stop_orbit=True):
        if stop_orbit:
            stop_download_json = {'methodId': 'downloadcancel'}
            social.get_channel().stop_download(json.dumps(stop_download_json))
        self.downloading = False

    def get_space_flag(self):
        return self.space_flag

    def set_space_flag(self, space_flag):
        self.space_flag = space_flag

    def download_finish_callback(self):
        if self.downloading:
            self.do_download_finish_callback()

    def do_download_finish_callback(self):
        self.failed_list.extend(six_ex.values(self.download_map))
        self.retqueue.put((self.cb, (deepcopy(self.success_list), deepcopy(self.failed_list), time.time() - self.download_start_time)))
        self.stop_download(False)
        self.init_download_env()

    def orbit_download_callback(self, data, result, complete):
        json_data = json.loads(data)
        filename = json_data.get('filename', '')
        code = json_data.get('code', -1)
        if filename == ORBIT_START:
            self._support_end_flag = True
        try:
            if code != 0:
                dc_tool = patch_dctool.get_dctool_instane()
                dc_tool.set_update_phase_extra_dict({'last_orbit_code': code})
        except Exception as e:
            print('[Patch][Orbit] get_dctool_instane error:{}'.format(str(e)))

        if code == ORBIT_SPACE_OUT_CODE:
            self.space_flag = True
        download_failed = orbit_result_parser(filename, code)
        if download_failed:
            try:
                self.msg_queue.put('[Patch][Orbit] download config error?')
                self.download_finish_callback()
                print('[patch][Orbit] download file', filename, data)
            except Exception as e:
                print('[Patch][Orbit] met exception:{}'.format(str(e)))

            return
        final_filename = filename
        file_path = json_data.get('filepath', '').replace('\\', '/')
        if file_path in self.download_map and filename not in self.download_map:
            final_filename = file_path
        if final_filename in self.download_map:
            self._all_num += 1
            download_item = self.download_map.pop(final_filename)
            self.success_list.append(download_item) if code == 0 else self.failed_list.append(download_item)
        if code != 0:
            print('[ORBIT DOWNLOAD ERROR] callback data is' + data)
        if self._support_end_flag:
            if filename == ORBIT_END:
                print('[orbit downloader] batch end')
                if len(self.download_map) == 0:
                    self._download_next_batch()
                else:
                    print('[orbit downloader] error: receive end but download_map if not empty')
                    self.download_finish_callback()
        elif len(self.download_map) == 0:
            self._download_next_batch()

    def _download_next_batch(self):
        print('[orbit downloader] downloaded num:', self._all_num)
        if self.download_list:
            self.spd_record = [
             (
              0, time.time())]
            self._acc_bytes += social.get_channel().get_download_bytes()
            self.orbit_start_download()
        else:
            self.download_finish_callback()

    def is_chinese_client(self):
        language_code = patch_lang.get_multi_lang_instane().cnt_lang_code
        return language_code == lang_data.LANG_CN

    def replace_steam_url(self, downlaoder_list):
        if patch_dctool.get_dctool_instane().is_steam_channel():
            if not self.is_chinese_client():
                new_list = []
                for item in downlaoder_list:
                    new_item = []
                    for idx, value in enumerate(item):
                        if idx == 2:
                            value = value.replace('netease.com', 'easebar.com')
                        new_item.append(value)

                    new_list.append(new_item)

                return new_list
        return downlaoder_list

    def start_download(self, download_list, cb, total_size=0, override=True):
        print('[orbit downloader] dl len:', len(download_list))
        for item in download_list:
            print('[orbit downloader] start download' + str(item))

        download_list = self.replace_steam_url(download_list)
        if self.downloading:
            process_info = {'stage': 'start_download','error:': 'orbit is downloading'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            return False
        self.init_download_env(download_list, total_size, cb, override)
        self.downloading = True
        self.space_flag = False
        self._need_override = override
        self._acc_bytes = 0.0
        self._all_num = 0
        self.orbit_start_download()
        return True

    def orbit_start_download(self):
        self.generate_orbit_download_info()
        if network_utils.TYPE_INVALID == network_utils.g93_get_network_type():
            self.do_download_finish_callback()
            return
        print('[orbit downloader] orbit start:', len(self.cnt_orbit_config.get('downfile', [])))
        social.get_channel().start_download(json.dumps(self.cnt_orbit_config), self.orbit_download_callback)