# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_npk_downloader.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six.moves.http_client
import urllib3
import time
import threading
import os
from patch import patch_const
from patch import patch_utils
THREAD_NUMBER = 1
import game3d
STATE_DLD_INIT = 0
STATE_DLD_PAUSE = 1
STATE_DLD_DOWNLOADING = 2
STATE_DLD_VERIFICATION = 3
STATE_DLD_FINISHED = 4
STATE_DLD_FAILED = 5
STATE_DLD_NEED_RESTART = 6
STATE_VALID = 6
STATE_PAUSING_DOWNLOADING = 7

class ExtNpkDownloader(object):

    def __init__(self, mgr, key, rw_npk_path, temp_rw_npk_path, remote_url, config, state=STATE_DLD_INIT):
        super(ExtNpkDownloader, self).__init__()
        self.mgr = mgr
        self.npk_key = key
        self.remote_url = remote_url
        self.init_state = state
        self.lock = threading.Lock()
        self.temp_filepath_map = {}
        self.rw_npk_path = rw_npk_path
        self.temp_rw_npk_path = temp_rw_npk_path
        self.space_flag = False
        self.use_akamai = False
        self.config = config
        self.thread_blocking_time_map = {}
        self.valid_download_thread_id = None
        self.init_time_zone()
        self.init_downloader()
        return

    def init_time_zone(self):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            try:
                zone = time.strftime('%z', time.localtime())
                if zone[0] == '+':
                    zone_offset = int(zone[1:])
                    if zone_offset >= 630 and zone_offset <= 900:
                        self.use_akamai = True
            except Exception:
                self.use_akamai = False

        if self.use_akamai:
            self.remote_url = self.remote_url.replace('g93na.gph.netease.com', 'g93na-12.gph.netease.com')

    def get_progress(self):
        progress = 0
        with self.lock:
            progress = min(self.downloaded_size * 1.0 / self.get_tatal_size(), 1.0)
        return progress

    def calc_download_speed(self):
        if self.state != STATE_DLD_DOWNLOADING:
            return 0
        new_check_time = time.time()
        size_diff = self.downloaded_size - self.last_check_size
        time_diff = new_check_time - self.spd_check_time
        if time_diff <= 0:
            return 0
        spd = int(size_diff * 1.0 / time_diff)
        self.spd_check_time = new_check_time
        self.last_check_size = self.downloaded_size
        self.download_speed = spd

    def get_speed(self):
        return self.download_speed

    def get_tatal_size(self):
        return self.config[1]

    def get_downloaded_size(self):
        return self.downloaded_size

    def reset_download_info(self):
        self.last_check_size = 0
        self.spd_check_time = time.time()
        self.download_speed = 0
        self.space_flag = False

    def init_downloader(self):
        self.state = STATE_DLD_INIT
        self.downloaded_size = 0
        if os.path.exists(self.temp_rw_npk_path):
            self.state = STATE_DLD_PAUSE
            self.downloaded_size = os.path.getsize(self.temp_rw_npk_path)
        elif os.path.exists(self.rw_npk_path):
            self.state = STATE_DLD_FINISHED
            self.downloaded_size = os.path.getsize(self.rw_npk_path)
        if self.init_state == STATE_VALID:
            self.state = self.init_state
        self.reset_download_info()

    def get_state(self):
        return self.state

    def pause_download(self):
        with self.lock:
            if self.state == STATE_DLD_DOWNLOADING:
                self.state = STATE_PAUSING_DOWNLOADING
                self.valid_download_thread_id = None
        return

    def get_space_flag(self):
        return self.space_flag

    def set_space_flag(self, space_flag):
        self.space_flag = space_flag

    def do_verify_tmp_npk_file(self):
        if patch_utils.check_big_file_md5(self.temp_rw_npk_path):
            os.rename(self.temp_rw_npk_path, self.rw_npk_path)
            self.state = STATE_DLD_FINISHED
            return True
        else:
            os.remove(self.temp_rw_npk_path)
            return False

    def get_temp_file_size(self):
        file_size = 0
        if os.path.exists(self.temp_rw_npk_path):
            file_size = os.path.getsize(self.temp_rw_npk_path)
        return file_size

    def on_download_finished(self):
        total_size = self.get_tatal_size()
        downloaded_size = self.get_downloaded_size()
        temp_files_size = self.get_temp_file_size()
        if total_size == downloaded_size:
            self.state = STATE_DLD_VERIFICATION
        else:
            self.state = STATE_DLD_FAILED

    def check_download_init_state(self, tid):
        if self.get_space_flag():
            return False
        if self.valid_download_thread_id != tid:
            return False
        if self.state != STATE_DLD_DOWNLOADING:
            return False
        return True

    def do_download_single_file(self, remote_url, target_path):
        remote_url = self.remote_url
        target_path = self.temp_rw_npk_path
        tid = threading.currentThread().ident
        while True:
            if not self.check_download_init_state():
                break
            file_writer = None
            range_headers = {}
            file_type = 'wb'
            if os.path.exists(target_path):
                range_headers = {'range': 'bytes=%d-' % os.path.getsize(target_path)}
                file_type = 'ab'
            dirname = os.path.dirname(target_path)
            with self.lock:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            try:
                try:
                    http = urllib3.PoolManager()
                    with self.lock:
                        self.thread_blocking_time_map[tid] = time.time()
                        r = http.request('GET', remote_url, preload_content=False, imeout=urllib3.Timeout(connect=patch_const.CONNECT_TIMEOUT, read=patch_const.DOWNLOAD_TIMEOUT), headers=range_headers)
                    with self.lock:
                        self.thread_blocking_time_map[tid] = None
                    if r.status != six.moves.http_client.OK:
                        if hasattr(r, 'release_con'):
                            r.release_con()
                        continue
                    file_writer = open(target_path, file_type)
                    self.thread_blocking_time_map[tid] = time.time()
                    for chunk in r.stream(patch_const.CHUNK_SIZE):
                        with self.block:
                            if self.valid_download_thread_id != tid:
                                break
                            file_writer.write(chunk)
                            self.downloaded_size += len(chunk)
                            file_writer.flush()
                            if self.downloaded_size >= self.get_tatal_size():
                                break
                            self.thread_blocking_time_map[tid] = time.time()

                    with self.lock:
                        if tid in self.thread_blocking_time_map:
                            del self.thread_blocking_time_map[tid]
                    if hasattr(r, 'release_con'):
                        r.release_con()
                    file_writer.close()
                except urllib3.exceptions.TimeoutError:
                    pass
                except OSError as ose:
                    try:
                        if self.valid_download_thread_id == tid:
                            error_no = ose.errno
                            if int(error_no) == 28:
                                self.set_space_flag(True)
                    except:
                        pass

                except Exception as e:
                    log_error('[NPK] DOWNLOAD FILE from %s with exception %s ' % (remote_url, str(e)))

            finally:
                if file_writer and not file_writer.closed:
                    file_writer.close()

        with self.lock:
            if tid in self.thread_blocking_time_map:
                del self.thread_blocking_time_map[tid]
        if self.valid_download_thread_id == tid and self.state == self.STATE_DLD_DOWNLOADING:
            self.on_download_finished()
        return

    def start_download(self):
        if self.state not in (STATE_DLD_INIT, STATE_DLD_PAUSE):
            return
        self.reset_download_info()
        t = threading.Thread(target=self.download_thread_func)
        t.setDaemon(True)
        t.start()
        return True

    def check_thread(self):
        tid_to_release = None
        for k, v in six.iteritems(self.thread_blocking_time_map):
            block_time = v
            if not block_time:
                block_time = time.time()
            if time.time() - block_time > patch_const.CONNECT_TIMEOUT + patch_const.DOWNLOAD_TIMEOUT:
                print(k, 'thread blocking')
                tid_to_release = k
                break

        if tid_to_release:
            del self.thread_blocking_time_map[tid_to_release]
            if tid_to_release == self.valid_download_thread_id:
                self.valid_download_thread_id = None
        return

    def restart_download_thread(self):
        worker_thread = threading.Thread(target=self.do_download_single_file)
        self.valid_download_thread_id = worker_thread.ident
        worker_thread.start()
        return worker_thread.ident

    def do_pause_downloader(self):
        with self.lock:
            if self.valid_download_thread_id in self.thread_blocking_time_map:
                del self.thread_blocking_time_map[self.valid_download_thread_id]
            self.valid_download_thread_id = None
            self.state = STATE_DLD_PAUSE
        return

    def download_thread_func(self):
        work_ident = self.restart_download_thread()
        while True:
            if self.state == STATE_PAUSING_DOWNLOADING:
                self.do_pause_downloader()
                break
            if self.state == STATE_DLD_VERIFICATION:
                if self.do_verify_tmp_npk_file():
                    self.state = self.mgr.on_download_npk_finish(self.npk_key, STATE_DLD_FINISHED)
                    break
            if self.state == STATE_DLD_FAILED:
                self.do_pause_downloader()
                self.mgr.on_download_npk_finish(self.npk_key, STATE_DLD_FAILED)
                break
            if self.valid_download_thread_id != work_ident:
                work_ident = self.restart_download_thread()
            with self.lock:
                self.check_thread()
            time.sleep(1)