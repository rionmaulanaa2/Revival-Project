# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/downloader_agent/thread_downloader.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import six.moves.http_client
import urllib3
import time
import threading
import traceback
import os
import social
from patch import patch_const
from patch import patch_utils
THREAD_NUMBER = 15
FILE_RETRY_TIME = 3
from copy import deepcopy
import game3d

class ThreadDownloader(object):

    def __init__(self, retqueue, err_queue, msg_queue):
        super(ThreadDownloader, self).__init__()
        self.lock = threading.Lock()
        self.retqueue = retqueue
        self.err_queue = err_queue
        self.msg_queue = msg_queue
        channel = social.get_channel()
        channel.init_downloader()
        self.temp_filepath_map = {}
        self.downloaded_map = {}
        self.space_flag = False
        self.use_akamai = False
        self.init_time_zone()
        self.init_download_env([], 0)

    def init_time_zone(self):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            try:
                zone = time.strftime('%z', time.localtime())
                if zone[0] == '+':
                    zone_offset = int(zone[1:])
                    if zone_offset >= 630 and zone_offset <= 900:
                        self.use_akamai = True
            except Exception as e:
                self.use_akamai = False

    def get_progress(self):
        if not self.downloading:
            return 1.0
        total_size = self.total_size or self.record_size
        if total_size == 0:
            return 0
        return self.downloaded_size * 1.0 / total_size

    def get_speed(self):
        if not self.downloading:
            return 0
        new_check_time = time.time()
        size_diff = self.downloaded_size - self.last_check_size
        time_diff = new_check_time - self.spd_check_time
        if time_diff <= 0:
            return 0
        spd = int(size_diff * 1.0 / time_diff)
        self.spd_check_time = new_check_time
        self.last_check_size = self.downloaded_size
        return spd

    def init_download_env(self, download_list=[], total_size=0, cb=None, override=True):
        self.download_list = deepcopy(download_list)
        self.total_size = total_size
        self.record_size = 0
        self.success_list = []
        self.failed_list = []
        self.last_check_size = 0
        self.spd_check_time = time.time()
        self.downloaded_size = 0
        self.pool = {}
        self.cb = cb
        self.downloading = False
        self.download_start_time = time.time()

    def stop_download(self, stop_orbit=True):
        self.downloading = False

    def get_space_flag(self):
        return self.space_flag

    def set_space_flag(self, space_flag):
        self.space_flag = space_flag

    def download_single_file(self, target_path, url):
        tid = threading.currentThread().ident
        for trycount in range(FILE_RETRY_TIME):
            file_writer = None
            if os.path.exists(target_path):
                os.remove(target_path)
            dirname = os.path.dirname(target_path)
            with self.lock:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            try:
                try:
                    result = False
                    http = urllib3.PoolManager()
                    with self.lock:
                        self.pool[tid]['block_time'] = time.time()
                    r = http.request('GET', url, preload_content=False, timeout=urllib3.Timeout(connect=patch_const.CONNECT_TIMEOUT, read=patch_const.DOWNLOAD_TIMEOUT))
                    with self.lock:
                        self.pool[tid]['block_time'] = None
                    if r.status != six.moves.http_client.OK:
                        if hasattr(r, 'release_con'):
                            r.release_con()
                        continue
                    file_size = r.getheader('Content-Length')
                    with self.lock:
                        self.record_size += int(file_size)
                    file_writer = open(target_path, 'wb')
                    with self.lock:
                        self.pool[tid]['block_time'] = time.time()
                    for chunk in r.stream(patch_const.CHUNK_SIZE):
                        if not self.downloading:
                            break
                        file_writer.write(chunk)
                        with self.lock:
                            self.downloaded_size += len(chunk)
                        file_writer.flush()
                        with self.lock:
                            self.pool[tid]['block_time'] = time.time()

                    with self.lock:
                        self.pool[tid]['block_time'] = None
                    result = True
                    if hasattr(r, 'release_con'):
                        r.release_con()
                    file_writer.close()
                    self.msg_queue.put('[PATCH] DOWNLOAD FILE FINISH FROM url %s' % url)
                    return result and self.downloading
                except urllib3.exceptions.TimeoutError:
                    pass
                except Exception as e:
                    self.msg_queue.put('[PATCH] DOWNLOAD FILE from %s with exception %s ' % (url, str(e)))

            finally:
                if file_writer and not file_writer.closed:
                    file_writer.close()

        return False

    def start_download(self, download_list, cb, total_size=0, override=True):
        if self.downloading:
            return False
        self.init_download_env(download_list, total_size, cb, override)
        self.downloading = True
        self.space_flag = False
        t = threading.Thread(target=self.download_thread_func)
        t.setDaemon(True)
        t.start()
        return True

    def check_thread(self):
        tid_to_release = None
        for k, v in six.iteritems(self.pool):
            block_time = v.get('block_time', time.time())
            if not block_time:
                block_time = time.time()
            if time.time() - block_time > patch_const.CONNECT_TIMEOUT + patch_const.DOWNLOAD_TIMEOUT:
                print(k, 'thread blocking')
                tid_to_release = k
                break

        if tid_to_release:
            pool_item = self.pool[tid_to_release]
            del self.pool[tid_to_release]
            downloading_item = pool_item.get('item', None)
            if downloading_item:
                self.put_downlod_res_item(downloading_item, False)
        return

    def download_thread_func(self):
        thread_list = []
        for i in range(THREAD_NUMBER):
            thread_list.append(threading.Thread(target=self.download_file_worker))

        with self.lock:
            for thread_item in thread_list:
                thread_item.start()
                self.pool[thread_item.ident] = {'thread': thread_item}

        while True:
            with self.lock:
                if len(self.pool) == 0:
                    break
                self.check_thread()
            time.sleep(1)

        with self.lock:
            if self.download_list:
                self.failed_list.extend(self.download_list)
                self.download_list = []
            if self.downloading:
                self.retqueue.put((self.cb, (deepcopy(self.success_list), deepcopy(self.failed_list), time.time() - self.download_start_time)))
                self.init_download_env()

    def download_file_worker(self):
        try:
            self.download_file()
        except:
            self.msg_queue.put('[PATCH] download file thread error:\n' + traceback.format_exc())

        with self.lock:
            tid = threading.currentThread().ident
            if tid in self.pool:
                del self.pool[tid]
            else:
                print('error thread invalid 1', tid)

    def put_downlod_res_item(self, download_item, download_res):
        self.success_list.append(download_item) if download_res else self.failed_list.append(download_item)

    def download_file(self):
        if not self.downloading:
            return
        else:
            tid = threading.currentThread().ident
            while True:
                download_item = None
                with self.lock:
                    if len(self.download_list) == 0 or not self.downloading:
                        break
                    if tid not in self.pool:
                        break
                    download_item = self.download_list.pop()
                self.pool[tid]['item'] = download_item
                rw_path = download_item[1]
                remote_url = download_item[2]
                if self.use_akamai:
                    remote_url = remote_url.replace('g93na.gph.netease.com', 'g93na-12.gph.netease.com')
                download_res = self.download_single_file(rw_path, remote_url)
                with self.lock:
                    if tid in self.pool:
                        del self.pool[tid]['item']
                        self.put_downlod_res_item(download_item, download_res)

            return