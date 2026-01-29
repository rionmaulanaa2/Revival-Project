# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_ingame_manager.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
import os
import time
import json
import queue
import game3d
import social
import hashlib
from . import ext_package_utils
from . import ext_package_const as ext_c
import six
from .ext_package_utils import cout_info, cout_error
from logic.gcommon.common_utils.local_text import get_text_by_id
from ext_package.ext_package_utils import get_left_available_space, other_err_log
from patch import patch_path
from patch import patch_utils
from patch.patch_dctool import get_dctool_instane
from patch.downloader_agent import orbit_downloader
from common.utils import timer
from common.framework import Singleton
from common.daemon_thread import DaemonThreadPool
from logic.comsys.archive.archive_manager import ArchiveManager
RE_TRY_TIMES = 10000
LOG_CHANNEL = 'ext_ingame_mgr'
NO_LIMIT_DRPF = ('ExtIngame_Verify', 'ExtIngame_Verify_Invalid', 'ExtIngame_DelInvalidExt',
                 'ExtIngameNpkProg')

class ExtInGameManager(Singleton):
    ALIAS_NAME = 'ext_ingame_mgr'

    def init(self):
        self._state = ext_c.EXT_IN_GAME_DL_INIT
        self._ext_dl_agent = None
        self._is_normal_res = patch_utils.get_patch_res_type() == patch_utils.PATCH_RES_TYPE_HIGH
        self._ext_package_config = ext_package_utils.get_ext_package_config_v2()
        self._server_config, self._version_config = ext_package_utils.init_server_and_version_config()
        self._is_real_ext_package = ext_package_utils.is_real_ext_package()
        self._downloaded_ext_lst = set()
        self._need_download_ext_lst = set()
        self._dl_queue_clear_func = None
        self._timer = None
        self._need_up = False
        self._drpf_up_time = time.time()
        self._npk_download_list = []
        self._downloaded_size = 0
        self._all_npk_size = 0
        self._downloading_size = 0
        self._downloading_ext = ''
        self._wait_for_retry = False
        self._is_downloading_npk = False
        self._is_force_stop = False
        self._ext_npk_list_info = {}
        self._newest_npk_version = 0
        self._newest_npk_url = ''
        self._need_download_npk_exts = []
        self._only_analyze_cb = None
        self._all_drpf_type = set()
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        self._ext_npk_config_dict = {}
        self._verified_ext_set = set()
        self._last_saved_using = self._using_ext_info
        self._archive_data = None
        self._init_success = False
        self._make_sure_init_success()
        self._choose_download_ext = set()
        self._init_manual_ext()
        self._ret_queue = queue.Queue()
        self._err_queue = queue.Queue()
        self._msg_queue = queue.Queue()
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        cout_info(LOG_CHANNEL, 'init:{} using:{}'.format(self._init_success, self._using_ext_info))
        drpf_info = {'need_download': self.need_download_ext(),'using': self._using_ext_info,'init': self._init_success}
        self._drpf('ExtIngame_Init', drpf_info)
        return

    def has_active_ext(self, in_ext_name):
        if not self._is_real_ext_package:
            return True
        else:
            if not self._make_sure_init_success():
                return False
            if in_ext_name not in self._ext_package_config:
                return True
            if in_ext_name in self._ext_npk_config_dict:
                all_active = self._ext_npk_config_dict[in_ext_name]['all_active']
                return all_active and in_ext_name in self._using_ext_info
            return False

    def has_skin_ext(self):
        return self.has_active_ext(ext_c.EXT_SKIN_NAME)

    def has_kongdao_ext(self):
        return self.has_active_ext(ext_c.EXT_KONGDAO_SCENE_NAME)

    def has_video_ext(self):
        return self.has_active_ext(ext_c.EXT_VIDEO_NAME)

    def has_audio_ext(self):
        return self.has_active_ext(ext_c.EXT_AUDIO_NAME)

    def has_pve_ext(self, chapter=1):
        pve_ext_name = ext_c.get_pve_name(chapter)
        return self.has_active_ext(pve_ext_name)

    def set_state(self, in_state):
        self._state = in_state

    def is_in_downloading_process(self):
        return self._is_downloading_npk or self._wait_for_retry

    def get_is_in_force(self):
        return self._is_force_stop

    def get_all_ext_downloaded(self):
        for ext_name in self._ext_package_config:
            if ext_name not in self._last_saved_using:
                return False

        return True

    def get_ext_state(self, ext_name):
        if ext_name in self._using_ext_info:
            return ext_c.EXT_OLD_USING
        else:
            if ext_name in self._last_saved_using:
                return ext_c.EXT_NEW_USING
            return ext_c.EXT_OTHER

    def stop_all_download(self, force=True):
        self._is_force_stop = True
        self._is_downloading_npk = False
        self._unregister_timer()
        self._state = ext_c.EXT_IN_GAME_FORCE_STOP
        if self._ext_dl_agent:
            if self._dl_queue_clear_func:
                self._dl_queue_clear_func()
            self._ext_dl_agent.stop_download()

    def get_speed_and_size(self):
        if not self._ext_dl_agent:
            return (-1, 0)
        else:
            if self._ext_dl_agent.downloading:
                bytes_spd = self._ext_dl_agent.get_speed()
                return (
                 bytes_spd * 1.0 / 1048576.0, self._all_npk_size)
            return (
             -1, self._all_npk_size)

    def get_now_speed_and_size(self):
        if not self._ext_dl_agent:
            return (-1, 0)
        else:
            if self._ext_dl_agent.downloading:
                bytes_spd = self._ext_dl_agent.get_speed()
                return (
                 bytes_spd * 1.0 / 1048576.0, self._downloading_size)
            return (
             -1, self._downloading_size)

    def restart_download(self):
        self._is_force_stop = False
        self.start_download_auto_npk(True)

    def need_download_ext(self):
        if not self._is_real_ext_package:
            return False
        if not self._make_sure_init_success():
            return True
        if not self._ext_package_config:
            return False
        if not self._using_ext_info:
            return True
        saved_using_info, ret = ext_package_utils.get_downloaded_ext_info_v2()
        if not ret:
            cout_error(LOG_CHANNEL, 'get using failed')
            return True
        for ext_name in self._ext_package_config:
            if ext_name not in saved_using_info:
                return True

        return False

    def start_download_manual_ext_npk(self, ext_name, download):
        if download:
            self._choose_download_ext.add(ext_name)
        elif ext_name in self._choose_download_ext:
            self._choose_download_ext.remove(ext_name)
            if self._downloading_ext == ext_name:
                self.stop_all_download()
                self.start_download_auto_npk(True)
        if self._state in (ext_c.EXT_IN_GAME_DL_FINISHED,):
            self.start_download_auto_npk(True)

    def start_download_auto_npk(self, reset_state=False, only_analyze_cb=None):
        if reset_state:
            self._is_force_stop = False
        elif self._is_force_stop:
            cout_info(LOG_CHANNEL, 'is in state: force stop')
            return
        if self._is_downloading_npk:
            cout_info(LOG_CHANNEL, 'is downloading')
            return
        else:
            self._state = ext_c.EXT_IN_GAME_DL_INFO
            self._wait_for_retry = False
            self._is_downloading_npk = True
            self._init_downloader()
            if not self._make_sure_init_success():
                game3d.delay_exec(RE_TRY_TIMES, self.start_download_auto_npk, (False, only_analyze_cb))
                return
            if not self._update_ext_state():
                game3d.delay_exec(RE_TRY_TIMES, self.start_download_auto_npk, (False, only_analyze_cb))
                return
            self._need_up = True
            if not self._timer:
                self._timer = global_data.game_mgr.register_logic_timer(self._logic_tick, interval=1, times=-1, mode=timer.LOGIC)
            self._only_analyze_cb = only_analyze_cb
            self._need_download_ext_lst = set()
            for ext_name in self._ext_npk_config_dict:
                if ext_name in self._using_ext_info:
                    cout_info(LOG_CHANNEL, '{} is using'.format(ext_name))
                    continue
                self._need_download_ext_lst.add(ext_name)

            cout_info(LOG_CHANNEL, 'need dl:{}'.format(self._need_download_ext_lst))
            self._drpf('ExtIngame_StartDownload', {'need': self._need_download_ext_lst})
            if self._need_download_ext_lst:
                self._download_ext_npk_list()
                return
            self._verify_all_ext_success()
            return

    def get_state_and_progress(self):
        if self._state in (ext_c.EXT_IN_GAME_DL_INIT, ext_c.EXT_IN_GAME_DL_NO_NEED, ext_c.EXT_IN_GAME_DL_INFO):
            return (self._state, 0, get_text_by_id(203))
        if self._state == ext_c.EXT_IN_GAME_DL_NPK:
            if self._downloading_ext:
                txt_id = ext_c.EXT_NAME_DICT.get(self._downloading_ext, 330)
                return (
                 self._state, self._get_npk_progress(), '({})'.format(get_text_by_id(txt_id)))
            else:
                return (
                 self._state, self._get_npk_progress(), '')

        else:
            if self._state == ext_c.EXT_IN_GAME_DL_VERIFY:
                if self._ext_npk_verify_total_size == 0:
                    ret_progress = 0.0
                else:
                    ret_progress = min(1.0, self._ext_npk_checked_size / self._ext_npk_verify_total_size)
                if self._downloading_ext:
                    ext_txt_id = ext_c.EXT_NAME_DICT.get(self._downloading_ext, 330)
                    txt = get_text_by_id(352).format(get_text_by_id(ext_txt_id))
                else:
                    txt = get_text_by_id(205)
                return (self._state, ret_progress, txt)
            if self._state == ext_c.EXT_IN_GAME_DL_FINISHED:
                if self.get_all_ext_downloaded():
                    txt = get_text_by_id(333)
                    prog = 1
                else:
                    txt = get_text_by_id(83609)
                    prog = 0
                return (self._state, prog, txt)
            if self._state == ext_c.EXT_IN_GAME_DL_ERROR:
                txt_id = 354 if self._ext_dl_agent and self._ext_dl_agent.get_space_flag() else 3128
                return (
                 self._state, 0, get_text_by_id(txt_id))
            if self._state == ext_c.EXT_IN_GAME_DL_WAITING_WIFI:
                return (self._state, 0, get_text_by_id(236))
            return (
             self._state, 0, '')

    def _get_npk_progress(self):
        if self._all_npk_size > 0:
            return self._ext_dl_agent.get_progress()
        else:
            return 0

    def get_download_ext_npk_size(self):
        if not self._make_sure_init_success():
            return 0
        all_size = 0
        for ext_name in self._need_download_npk_exts:
            ext_npk_state = self._ext_npk_config_dict[ext_name]['npk_state']
            for tmp_npk_name in ext_npk_state:
                npk_exists, is_active = ext_npk_state[tmp_npk_name]
                if npk_exists:
                    continue
                npk_md5, npk_size = self._ext_npk_config_dict[ext_name]['fit_npk_info'][tmp_npk_name]
                all_size += npk_size

        return all_size

    def _init_manual_ext(self):
        if not self._archive_data:
            self._archive_data = ArchiveManager().get_archive_data('setting')
        for ext_name in self._ext_package_config:
            auto_dl = self._ext_package_config.get(ext_name, {}).get('auto_download', 1)
            if auto_dl < 1:
                choose_dl = self._archive_data.get_field(ext_c.EXT_MANUAL_ARCHIVE_NAME_DICT.get(ext_name, 'ext_dl_manual'), False)
                if choose_dl:
                    self._choose_download_ext.add(ext_name)

    def _make_sure_init_success(self):
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        if self._using_ext_info is None:
            self._init_success = False
        else:
            if not self._init_success:
                self._update_ext_state()
            self._init_success = True
        if not self._init_success:
            cout_error(LOG_CHANNEL, 'init met error, using:{}'.format(self._using_ext_info))
        return self._init_success

    def _init_downloader(self):
        if self._ext_dl_agent:
            return
        else:
            channel = social.get_channel()
            if channel.is_downloader_enable():
                from patch.downloader_agent import orbit_downloader
                self._ext_dl_agent = orbit_downloader.OrbitDownloader(self._ret_queue, self._err_queue, self._msg_queue)
                self._dl_queue_clear_func = self.clear_downloader_queque
            else:
                from patch.downloader_agent import thread_downloader
                self._ext_dl_agent = thread_downloader.ThreadDownloader(self._ret_queue, self._err_queue, self._msg_queue)
                self._dl_queue_clear_func = None
            return

    def _set_downloader_thread_num(self):
        from patch.downloader_agent import orbit_downloader
        if hasattr(orbit_downloader, 'set_thread_number'):
            self._archive_data = self._archive_data or ArchiveManager().get_archive_data('setting')
        is_full_speed = self._archive_data.get_field(ext_c.EXT_DL_FULL_SPEED, False)
        if is_full_speed:
            t_num = '3' if 1 else '1'
            try:
                orbit_downloader.set_thread_number(t_num)
            except Exception as e:
                cout_error(LOG_CHANNEL, 'set_thread_number error:{}'.format(str(e)))

    def _update_ext_state(self):
        ret_result = True
        for ext_name in self._ext_package_config:
            if ext_name in self._using_ext_info:
                ext_ver = self._using_ext_info[ext_name]
            else:
                ext_ver = None
            now_config, ret = ext_package_utils.read_ext_npk_config_v2(ext_name, self._is_normal_res, ext_ver)
            self._ext_npk_config_dict[ext_name] = now_config
            ret_result &= ret

        return ret_result

    def _download_ext_npk_list(self):
        self._state = ext_c.EXT_IN_GAME_DL_INFO
        if self._ext_npk_list_info:
            cout_info(LOG_CHANNEL, 'has ext npk list')
            self.ext_npk_config_analyze()
        else:
            cout_info(LOG_CHANNEL, 'dl npk list')
            ext_npk_list_url = ext_package_utils.get_ext_npk_list_url(self._server_config)
            temp_file_path = os.path.join(patch_path.TEMP_DIRNAME, ext_c.EXT_PATCH_LIST_NAME)
            list_orbit_path = patch_path.get_orbit_download_path(temp_file_path)
            list_rw_path = patch_path.get_rw_path(temp_file_path)
            download_list = [(list_orbit_path, list_rw_path, ext_npk_list_url, 0)]
            if not self._ext_dl_agent.start_download(download_list, self._on_download_ext_list_callback):
                cout_error(LOG_CHANNEL, 'npk list start_download return false')

    def _on_download_ext_list_callback(self, success_list, error_list, consume_time):
        if error_list:
            dl_url = error_list[0][2]
            cout_error(LOG_CHANNEL, 'dl ext list:{} error'.format(dl_url))
            self.error_and_retry()
        else:
            cout_info(LOG_CHANNEL, 'dl ext list time:{}'.format(consume_time))
            file_path = success_list[0][1]
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as tmp_file:
                        data = tmp_file.read()
                    data = six.ensure_str(data)
                except Exception as e:
                    cout_error(LOG_CHANNEL, 'read ext list except:{}'.format(str(e)))
                    self.error_and_retry()
                    return

                DaemonThreadPool().add_threadpool(self._ext_npk_list_analyze, None, data)
            else:
                cout_error(LOG_CHANNEL, 'ext list:{} not exists after downloaded'.format(file_path))
                self.error_and_retry()
        return

    def _ext_npk_list_analyze(self, dl_data):
        self._state = ext_c.EXT_IN_GAME_DL_INFO
        try:
            newest_v, newest_url, npk_info_dict = ext_package_utils.analyze_valid_ext_npk_list_info(dl_data)
            if newest_v > 0 and newest_url and len(npk_info_dict) > 0:
                self._newest_npk_version = newest_v
                self._newest_npk_url = newest_url
                self._ext_npk_list_info = npk_info_dict
                self._ret_queue.put((self.ext_npk_config_analyze, ()))
            else:
                cout_error(LOG_CHANNEL, 'has no valid npk list info')
                self._ret_queue.put((self.error_and_retry, ()))
        except Exception as e:
            cout_error(LOG_CHANNEL, 'analyze ext npk list exception:{}'.format(str(e)))
            self._ret_queue.put((self.error_and_retry, ()))

    def del_config_related_info(self, ext_name):
        config_path = ext_package_utils.get_ext_npk_config_rw_path(ext_name)
        try:
            os.remove(config_path)
        except Exception as e:
            cout_error(LOG_CHANNEL, 'remove {} with exception:{}'.format(config_path, str(e)))

        npk_info = self._ext_npk_config_dict[ext_name]['fit_npk_info']
        for npk_filename in npk_info:
            npk_path = ext_package_utils.get_ext_rw_path(npk_filename)
            temp_npk_path = ext_package_utils.get_ext_npk_temp_path(ext_name)
            try:
                if os.path.exists(npk_path):
                    os.remove(npk_path)
                if os.path.exists(temp_npk_path):
                    os.remove(temp_npk_path)
            except Exception as e:
                cout_error(LOG_CHANNEL, 'remove path:{} {} with exception:{}'.format(npk_path, temp_npk_path, str(e)))

    def _delay_retry_analyze(self):
        game3d.delay_exec(RE_TRY_TIMES, self.ext_npk_config_analyze)

    def can_download_ext(self, ext_name):
        auto_download = self._ext_package_config.get(ext_name, {}).get('auto_download', 1)
        if auto_download > 0 or ext_name in self._choose_download_ext:
            return True
        else:
            return False

    def ext_npk_config_analyze(self, check_all=True):
        if self._is_force_stop:
            self._state = ext_c.EXT_IN_GAME_FORCE_STOP
            self._is_downloading_npk = False
            return
        cout_info(LOG_CHANNEL, 'analyze ext npk config')
        self._state = ext_c.EXT_IN_GAME_DL_INFO
        if not self._update_ext_state():
            self._delay_retry_analyze()
            return
        need_download_config_exts = []
        need_download_npk_exts = []
        downloaded_exts = []
        self._need_download_npk_exts = []
        for tmp_ext_name in self._need_download_ext_lst:
            if not check_all and not self.can_download_ext(tmp_ext_name):
                cout_info(LOG_CHANNEL, '{} not choose for dl'.format(tmp_ext_name))
                continue
            config_exist = self._ext_npk_config_dict[tmp_ext_name]['config_exist']
            all_npk_exist = self._ext_npk_config_dict[tmp_ext_name]['all_npk_exist']
            if config_exist:
                if all_npk_exist:
                    downloaded_exts.append(tmp_ext_name)
                else:
                    need_download_npk_exts.append(tmp_ext_name)
            else:
                need_download_config_exts.append(tmp_ext_name)

        if need_download_config_exts:
            cout_info(LOG_CHANNEL, 'dl remote config:{}'.format(need_download_config_exts))
            self._download_remote_ext_configs(need_download_config_exts)
        elif need_download_npk_exts:
            self._need_download_npk_exts = need_download_npk_exts
            cout_info(LOG_CHANNEL, 'need dl npk:{}'.format(need_download_npk_exts))
            if self._only_analyze_cb:
                self._call_analyze_cb()
                return
            self.download_ext_npk()
        else:
            if self._only_analyze_cb:
                self._call_analyze_cb()
                return
            self._downloading_ext = ''
            cout_info(LOG_CHANNEL, 'verify all ext npk:{}'.format(downloaded_exts))
            self._verify_ext_npk_files(downloaded_exts)

    def _call_analyze_cb(self):
        if self._only_analyze_cb:
            self._state = ext_c.EXT_IN_GAME_DL_INIT
            cb_func = self._only_analyze_cb
            self._only_analyze_cb = None
            self.set_end_state()
            cb_func()
        return

    def _download_remote_ext_configs(self, need_download_config_keys):
        self._drpf('ExtIngame_Dl_Config', {'need': need_download_config_keys})
        self._state = ext_c.EXT_IN_GAME_DL_INFO
        download_list = ext_package_utils.get_ext_configs_download_items_v2(need_download_config_keys, self._newest_npk_url)
        if not self._ext_dl_agent.start_download(download_list, self._on_download_ext_config_callback):
            cout_error(LOG_CHANNEL, 'start dl remote config fail')
            self.error_and_retry()

    def _on_download_ext_config_callback(self, success_list, error_list, consume_time):
        if error_list:
            cout_error(LOG_CHANNEL, 'download_ext_config_callback failed')
            self.error_and_retry()
        else:
            cout_info(LOG_CHANNEL, 'download_ext_config_callback success')
            self.ext_npk_config_analyze()

    def _init_npk_dl_info(self):
        self._npk_download_list = []
        self._all_npk_size = 0
        self._downloading_size = 0
        self._downloading_ext = ''
        self._downloaded_size = 0

    def download_ext_npk(self):
        self._init_npk_dl_info()
        ext_name_lst = self._need_download_npk_exts

        def cmp_func(a, b):
            priority_a = self._ext_package_config.get(a, {}).get('priority', 100)
            priority_b = self._ext_package_config.get(b, {}).get('priority', 100)
            return six_ex.compare(priority_a, priority_b)

        ext_name_lst.sort(key=cmp_to_key(cmp_func))
        met_error = False
        for ext_name in ext_name_lst:
            ext_dl_lst = []
            config_exist = self._ext_npk_config_dict[ext_name]['config_exist']
            ext_npk_state = self._ext_npk_config_dict[ext_name]['npk_state']
            npk_version = int(self._ext_npk_config_dict[ext_name]['version'])
            if npk_version not in self._ext_npk_list_info:
                self.del_config_related_info(ext_name)
                met_error = True
                break
            if npk_version <= 0 or not config_exist:
                self._err_log('[EXT_CONFIG_ERROR_2] {}'.format(self._ext_npk_config_dict))
                met_error = True
                break
            for tmp_npk_name in ext_npk_state:
                npk_exists, is_active = ext_npk_state[tmp_npk_name]
                if npk_exists:
                    continue
                rw_path = ext_package_utils.get_ext_rw_path(tmp_npk_name)
                orbit_path = ext_package_utils.get_ext_orbit_download_path(tmp_npk_name)
                dl_url = self._ext_npk_list_info[npk_version] + '/' + tmp_npk_name
                npk_md5, npk_size = self._ext_npk_config_dict[ext_name]['fit_npk_info'][tmp_npk_name]
                ext_dl_item = (orbit_path, rw_path, dl_url, npk_size, npk_md5)
                ext_dl_lst.append(ext_dl_item)

            self._npk_download_list.append((ext_dl_lst, ext_name))

        if not self._npk_download_list or met_error:
            self._init_npk_dl_info()
            self._delay_retry_analyze()
            return
        self._all_npk_size = 0
        for tmp_dl_lst, ext_name in self._npk_download_list:
            for dl_item in tmp_dl_lst:
                self._all_npk_size += dl_item[3]

        self._drpf('ExtIngame_Dl_NPK', {'download_list': self._npk_download_list,'total_size': self._all_npk_size})
        self._start_download_ext_npk()

    def _start_download_ext_npk(self):
        if not self._npk_download_list:
            cout_error(LOG_CHANNEL, 'begin dl, but not dl list')
            self.error_and_retry()
            return
        else:
            new_dl_list = []
            ext_dl_lst = None
            ext_name = None
            for _dl_lst, _ext_name in self._npk_download_list:
                can_dl = self.can_download_ext(_ext_name)
                if can_dl and not ext_name:
                    ext_name = _ext_name
                    ext_dl_lst = _dl_lst
                if not ext_name:
                    new_dl_list.append((_dl_lst, _ext_name))

            self._npk_download_list = new_dl_list
            if not ext_name:
                self.ext_npk_config_analyze(False)
                return
            now_dl_size = 0
            for dl_item in ext_dl_lst:
                now_dl_size += dl_item[3]

            self._downloading_size = now_dl_size
            self._downloading_ext = ext_name
            self._set_downloader_thread_num()
            if not self._ext_dl_agent.start_download(ext_dl_lst, self._on_download_ext_npk_cb, now_dl_size, False):
                cout_error(LOG_CHANNEL, 'start dl remote npk, is downloading')
                self.error_and_retry()
                return
            self._state = ext_c.EXT_IN_GAME_DL_NPK
            return

    def _on_download_ext_npk_cb(self, success_list, error_list, consume_time):
        if error_list:
            cout_error(LOG_CHANNEL, 'download missing npk error')
            if self._ext_dl_agent.get_space_flag():
                self.error_and_retry(False)
                global_data.game_mgr.show_tip(get_text_by_id(354))
            else:
                self.error_and_retry()
        else:
            if not self._downloading_ext:
                self._delay_retry_analyze()
                return
            self._downloaded_size += self._downloading_size
            self._verify_single_ext_after_download(self._downloading_ext)

    def _verify_single_ext_after_download(self, ext_name):
        cout_info(LOG_CHANNEL, 'verify single ext:{}'.format(ext_name))
        self._drpf('ExtIngame_Verify', {'verify_ext': ext_name})
        self._state = ext_c.EXT_IN_GAME_DL_VERIFY
        self._ext_npk_verify_total_size = 0.0
        self._ext_npk_checked_size = 0.0
        fit_npk_info = self._ext_npk_config_dict[ext_name]['fit_npk_info']
        for tmp_npk_name in fit_npk_info:
            npk_md5, npk_size = fit_npk_info[tmp_npk_name]
            self._ext_npk_verify_total_size += npk_size

        DaemonThreadPool().add_threadpool(self._do_verify_single_ext_npk_files, None, ext_name)
        return

    def _do_verify_single_ext_npk_files(self, ext_name):
        invalid_list = []
        from patch import patch_const
        fit_npk_info = self._ext_npk_config_dict[ext_name]['fit_npk_info']
        npk_version = self._ext_npk_config_dict[ext_name]['version']
        for tmp_npk_name in fit_npk_info:
            npk_path = ext_package_utils.get_ext_rw_path(tmp_npk_name)
            npk_md5, npk_size = fit_npk_info[tmp_npk_name]
            if not os.path.exists(npk_path):
                self._ext_npk_checked_size += npk_size
                invalid_list.append((ext_name, tmp_npk_name))
                continue
            try:
                m = hashlib.md5()
                with open(npk_path, 'rb') as npk_file:
                    file_buffer = npk_file.read(patch_const.CHUNK_SIZE)
                    while file_buffer:
                        self._ext_npk_checked_size += len(file_buffer)
                        m.update(file_buffer)
                        file_buffer = npk_file.read(patch_const.CHUNK_SIZE)

                if str(m.hexdigest()) != npk_md5:
                    invalid_list.append(tmp_npk_name)
                    local_size = os.path.getsize(npk_path)
                    left_bytes = get_left_available_space()
                    cout_error(LOG_CHANNEL, 'ver:{} npk:{} md5:{} not matched, size:{}:{}, left megabytes:{}'.format(npk_version, tmp_npk_name, npk_md5, npk_size, local_size, left_bytes))
                    os.remove(npk_path)
            except Exception as e:
                self._ext_npk_checked_size += npk_size
                self._err_log('verify ext npk with exception:{}'.format(str(e)))
                invalid_list.append(tmp_npk_name)

        if invalid_list:
            self._drpf('ExtIngame_Verify_Invalid', {'invalid': invalid_list})
            self._ret_queue.put((self.ext_npk_config_analyze, ()))
        else:
            self._ret_queue.put((self._on_verify_single_ext_success, (ext_name,)))

    def _on_verify_single_ext_success(self, ext_name):
        if not self._update_ext_state():
            self._delay_retry_analyze()
            return
        config_exist = self._ext_npk_config_dict[ext_name]['config_exist']
        config_ver = int(self._ext_npk_config_dict[ext_name]['version'])
        all_npk_exist = self._ext_npk_config_dict[ext_name]['all_npk_exist']
        if not config_exist or config_ver <= 0 or not all_npk_exist:
            self._err_log('[EXT_CONFIG_ERROR_1] {}'.format(self._ext_npk_config_dict))
            self._delay_retry_analyze()
            return
        saved_using_info, ret = ext_package_utils.get_downloaded_ext_info_v2()
        if not ret:
            cout_error(LOG_CHANNEL, 'get using failed')
            self._delay_retry_analyze()
            return
        saved_using_info[ext_name] = config_ver
        cout_info(LOG_CHANNEL, 'save:{}'.format(ext_name))
        ret = ext_package_utils.save_downloaded_extends(saved_using_info)
        if not ret:
            self._delay_retry_analyze()
            return
        if self._is_force_stop:
            self._state = ext_c.EXT_IN_GAME_FORCE_STOP
            self._is_downloading_npk = False
            return
        if self._npk_download_list:
            game3d.frame_delay_exec(1, self._start_download_ext_npk)
        else:
            game3d.frame_delay_exec(1, self.ext_npk_config_analyze)

    def _del_saved_using(self, invalid_ext_lst):
        self._drpf('ExtIngame_DelInvalidExt', {'invalid': invalid_ext_lst})
        cout_error(LOG_CHANNEL, '[del_invalid_using] del invalid:{}'.format(invalid_ext_lst))
        saved_using_info, ret = ext_package_utils.get_downloaded_ext_info_v2()
        if not ret:
            cout_error(LOG_CHANNEL, '[del_invalid_using]: get using failed')
            return
        for ext_name in invalid_ext_lst:
            if ext_name in saved_using_info:
                del saved_using_info[ext_name]

        ret = ext_package_utils.save_downloaded_extends(saved_using_info)
        if not ret:
            cout_error(LOG_CHANNEL, '[del_invalid_using]: save using failed')

    def _verify_ext_npk_files(self, ext_list):
        self._drpf('ExtIngame_Verify_All', {'verify_all_ext': ext_list})
        self._state = ext_c.EXT_IN_GAME_DL_VERIFY
        self._ext_npk_verify_ext_lst = []
        for ext_name in ext_list:
            if ext_name in self._verified_ext_set:
                cout_info(LOG_CHANNEL, '{} is verified, skip'.format(ext_name))
                continue
            self._ext_npk_verify_ext_lst.append(ext_name)

        self._ext_npk_verify_total_size = 0.0
        self._ext_npk_checked_size = 0.0
        for ext_name in self._ext_npk_verify_ext_lst:
            fit_npk_info = self._ext_npk_config_dict[ext_name]['fit_npk_info']
            for tmp_npk_name in fit_npk_info:
                npk_md5, npk_size = fit_npk_info[tmp_npk_name]
                self._ext_npk_verify_total_size += npk_size

        DaemonThreadPool().add_threadpool(self._do_verify_all_ext_npk_files, None)
        return

    def _do_verify_all_ext_npk_files(self):
        invalid_list = set()
        from patch import patch_const
        met_except = False
        for ext_name in self._ext_npk_verify_ext_lst:
            fit_npk_info = self._ext_npk_config_dict[ext_name]['fit_npk_info']
            npk_version = self._ext_npk_config_dict[ext_name]['version']
            for tmp_npk_name in fit_npk_info:
                npk_path = ext_package_utils.get_ext_rw_path(tmp_npk_name)
                npk_md5, npk_size = fit_npk_info[tmp_npk_name]
                if not os.path.exists(npk_path):
                    self._ext_npk_checked_size += npk_size
                    invalid_list.add(ext_name)
                    continue
                try:
                    m = hashlib.md5()
                    with open(npk_path, 'rb') as tmp_file:
                        file_buffer = tmp_file.read(patch_const.CHUNK_SIZE)
                        while file_buffer:
                            self._ext_npk_checked_size += len(file_buffer)
                            m.update(file_buffer)
                            file_buffer = tmp_file.read(patch_const.CHUNK_SIZE)

                    if str(m.hexdigest()) != npk_md5:
                        invalid_list.add(ext_name)
                        local_size = os.path.getsize(npk_path)
                        left_bytes = get_left_available_space()
                        cout_error(LOG_CHANNEL, 'all ver:{} npk:{} md5:{} not matched, size:{}:{}, left megabytes:{}'.format(npk_version, tmp_npk_name, npk_md5, npk_size, local_size, left_bytes))
                        os.remove(npk_path)
                except Exception as e:
                    self._ext_npk_checked_size += npk_size
                    self._err_log('verify ext npk with exception:{}'.format(str(e)))
                    met_except = True

        if met_except:
            self._ret_queue.put((self.ext_npk_config_analyze, ()))
        elif invalid_list:
            self._drpf('ExtIngame_Verify_Invalid', {'invalid': invalid_list})
            self._del_saved_using(invalid_list)
            self._ret_queue.put((self.ext_npk_config_analyze, ()))
        else:
            for ext_name in self._ext_npk_verify_ext_lst:
                self._verified_ext_set.add(ext_name)

            self._drpf('ExtIngame_Verify_Success', {'verify_lst': self._ext_npk_verify_ext_lst})
            self._ret_queue.put((self._verify_all_ext_success, ()))

    def _verify_all_ext_success(self):
        if not self._update_ext_state():
            self._delay_retry_analyze()
            return
        saved_using_info, ret = ext_package_utils.get_downloaded_ext_info_v2()
        if not ret:
            cout_error(LOG_CHANNEL, 'verify all: get using failed')
            self._delay_retry_analyze()
            return
        has_new = False
        met_error = False
        for ext_name in self._ext_package_config:
            if ext_name not in saved_using_info and self.can_download_ext(ext_name):
                config_ver = int(self._ext_npk_config_dict[ext_name]['version'])
                config_exist = self._ext_npk_config_dict[ext_name]['config_exist']
                all_npk_exist = self._ext_npk_config_dict[ext_name]['all_npk_exist']
                if not config_exist or config_ver <= 0 or not all_npk_exist:
                    self._err_log('[EXT_CONFIG_ERROR_3] {}'.format(self._ext_npk_config_dict))
                    met_error = True
                    break
                saved_using_info[ext_name] = config_ver
                has_new = True

        if met_error:
            self._delay_retry_analyze()
            return
        save_success = True
        if has_new:
            save_success = ext_package_utils.save_downloaded_extends(saved_using_info)
        cout_info(LOG_CHANNEL, '[verify_all], saved:{}, success:{}'.format(six_ex.keys(saved_using_info), save_success))
        if not save_success:
            self._delay_retry_analyze()
            return
        self._drpf('ExtIngame_FINISH', {'saved_using': saved_using_info,'save_success': save_success})
        self.download_ext_finished()
        self._is_downloading_npk = False
        self._state = ext_c.EXT_IN_GAME_DL_FINISHED
        self._last_saved_using = saved_using_info

    def download_ext_finished(self):
        self.set_end_state()
        self._unregister_timer()

    def _logic_tick(self):
        while self._err_queue.qsize() > 0:
            err = self._err_queue.get()
            patch_utils.send_script_error('{} error:{}'.format(ext_c.DRFP_ERROR_CHANNEL, err))
            cout_error(LOG_CHANNEL, err)

        msg_queue_log_limit = 3000
        cnt_count = 0
        while self._msg_queue.qsize() > 0:
            msg = self._msg_queue.get()
            cout_info(LOG_CHANNEL, msg)
            cnt_count += 1
            if msg_queue_log_limit <= cnt_count:
                break

        while 1:
            try:
                callback, args = self._ret_queue.get_nowait()
                callback(*args)
            except queue.Empty:
                break

        try:
            if self._state == ext_c.EXT_IN_GAME_DL_NPK:
                cnt_time = time.time()
                if cnt_time - self._drpf_up_time > 60:
                    self._drpf_up_time = cnt_time
                    prog = self._ext_dl_agent.get_progress()
                    self._drpf('ExtIngameNpkProg', {'ext_ingame_prog': prog,'dl_ext_name': self._downloading_ext})
        except Exception as e:
            cout_error(LOG_CHANNEL, 'drpf exception:{}'.format(str(e)))

    def error_and_retry(self, need_retry=True):
        self._is_downloading_npk = False
        self._state = ext_c.EXT_IN_GAME_DL_ERROR
        if need_retry:
            self._wait_for_retry = True
            cout_info(LOG_CHANNEL, 'error and retry')
            game3d.delay_exec(RE_TRY_TIMES, self.start_download_auto_npk)

    def delay_retry(self):
        self._is_downloading_npk = False
        cout_info(LOG_CHANNEL, 'delay_retry')
        game3d.delay_exec(RE_TRY_TIMES, self.start_download_auto_npk)

    def set_end_state(self):
        self._is_downloading_npk = False

    def clear_downloader_queque(self):
        clear_json = {'methodId': 'downloadqueueclear'
           }
        social.get_channel().stop_download(json.dumps(clear_json))

    def _drpf(self, type_name, info):
        if type_name in NO_LIMIT_DRPF or type_name not in self._all_drpf_type:
            self._all_drpf_type.add(type_name)
            tool_inst = get_dctool_instane()
            if hasattr(tool_inst, 'ext_drpf_info'):
                tool_inst.ext_drpf_info(type_name, info)

    def _err_log(self, error_msg):
        other_err_log(ext_c.DRFP_ERROR_CHANNEL, error_msg)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def on_login_reconnect(self):
        if self._need_up:
            cout_info(LOG_CHANNEL, 'reconnect')
            self._unregister_timer()
            self._timer = global_data.game_mgr.register_logic_timer(self._logic_tick, interval=1, times=-1, mode=timer.LOGIC)