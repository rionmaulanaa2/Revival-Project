# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_package_manager.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from functools import cmp_to_key
import six.moves.builtins
import os
import json
import zlib
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import C_file
import game3d
import hashlib
import threading
from . import ext_package_const as ext_c
from . import ext_package_utils
from patch import patch_const
from patch import patch_path
from patch import patch_utils
from patch import patch_critical_info
from patch.patch_dctool import get_dctool_instane
from patch.downloader_agent import orbit_downloader
from patch.downloader_agent import thread_downloader
from .ext_package_utils import cout_info, cout_error, other_err_log
import six
EXT_PACKAGE_MGR = None
LOG_CHANNEL = 'ext_mgr'
IS_MOBILE = game3d.get_platform() in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID)

def get_ext_package_instance():
    global EXT_PACKAGE_MGR
    if not EXT_PACKAGE_MGR:
        EXT_PACKAGE_MGR = ExtPackageManager()
    return EXT_PACKAGE_MGR


class ExtPackageManager(object):

    def __init__(self):
        self.state = ext_c.EXT_STATE_INIT
        self._lock = threading.Lock()
        self._ext_dl_agent = None
        self._valid_npk_list = []
        self._ext_keys_config_download_cb = None
        self._ext_npk_list_download_cb = None
        self._ext_patch_analyze_callback = None
        self._patch_zip_config_analyze_cb = None
        self._ext_patch_download_cb = None
        self._npk_update_prog = 0.0
        self._new_flist_map = {}
        self._using_ext_config_dict = {}
        self._ext_npk_list_info = {}
        if hasattr(patch_const, 'ENABLE_PATCH_NPK'):
            self._enable_patch_npk = patch_const.ENABLE_PATCH_NPK
        else:
            self._enable_patch_npk = game3d.is_feature_ready('PATCH_NPK_MERGE')
        self._new_total_ext_flist_dict = {}
        self._zip_analyze_prog = 0
        self._patch_zip_info_dict = {}
        self._zip_patch_download_list = []
        self._zip_patch_download_size = 0
        self._patch_config_in_flist = None
        self._patch_npk_processor = None
        self._patch_list = []
        self._patch_target_version = 0
        self._flist_data = None
        self._ext_ver_config = {}
        from common.utils import package_type
        is_android_dds = package_type.is_android_dds_package()
        self._support_ui_astc = not is_android_dds and IS_MOBILE and game3d.is_feature_ready('UI_ASTC')
        self._is_normal_res = patch_utils.get_patch_res_type() == patch_utils.PATCH_RES_TYPE_HIGH
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        self._ext_package_config = ext_package_utils.get_ext_package_config_v2()
        self._is_real_ext_package = ext_package_utils.is_real_ext_package()
        self.server_config, self.ver_config = ext_package_utils.init_server_and_version_config()
        self.force_stop = False
        self._init_patch_info()
        self._init_ext_npk_file_verification_data()
        self._init_ext_patch_analyze_info()
        if not self._update_npk_config_data():
            cout_error(LOG_CHANNEL, 'init_update_npk_config_failed')
        return

    def update_config(self):
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        self._ext_package_config = ext_package_utils.get_ext_package_config_v2()

    def init_ext_patch_downloader_agent(self, use_orbit, ret_queue, err_queue, msg_queue):
        if use_orbit:
            self._ext_dl_agent = orbit_downloader.OrbitDownloader(ret_queue, err_queue, msg_queue)
        else:
            self._ext_dl_agent = thread_downloader.ThreadDownloader(ret_queue, err_queue, msg_queue)

    def get_active_ext_npk_lst(self):
        if not self._is_real_ext_package:
            return []
        active_npk_names = []
        for ext_name, ext_info in six.iteritems(self._using_ext_config_dict):
            npk_state = ext_info['npk_state']
            for npk_name in npk_state:
                npk_exists, is_active = npk_state[npk_name]
                if is_active:
                    active_npk_names.append(npk_name)

        return active_npk_names

    def get_active_ext_name_lst(self):
        if not self._is_real_ext_package:
            return []
        active_ext_names = []
        for ext_name, ext_info in six.iteritems(self._using_ext_config_dict):
            if ext_info['all_active']:
                active_ext_names.append(ext_name)

        return active_ext_names

    def get_patch_space_flag(self):
        if self._ext_dl_agent is None:
            return False
        else:
            return self._ext_dl_agent.get_space_flag()

    def get_ext_npk_list_info(self):
        return self._ext_npk_list_info

    def _update_npk_config_data(self):
        self._using_ext_config_dict = {}
        if self._using_ext_info is None:
            return False
        else:
            ret_result = True
            for ext_name in self._using_ext_info:
                ext_ver = self._using_ext_info[ext_name]
                with self._lock:
                    now_config, ret = ext_package_utils.read_ext_npk_config_v2(ext_name, self._is_normal_res, ext_ver)
                    self._using_ext_config_dict[ext_name] = now_config
                    ret_result &= ret

            return ret_result

    def get_is_downloading(self):
        if not self._ext_dl_agent:
            return False
        return self._ext_dl_agent.downloading

    def get_speed_and_size(self):
        total_size = self._ext_dl_agent.total_size
        if self._ext_dl_agent.downloading:
            bytes_spd = self._ext_dl_agent.get_speed()
            return (
             bytes_spd * 1.0 / 1048576.0, total_size)
        else:
            return (
             -1, total_size)

    def get_progress(self):
        try:
            if self.state == ext_c.EXT_STATE_VERIFYING_EXT_NPK:
                if self.ext_npk_verify_total_size == 0:
                    return (0.0, True)
                return (min(1.0, self._ext_npk_checked_size / self.ext_npk_verify_total_size), True)
            if self.state == ext_c.EXT_STATE_DL_MISSING_EXT_NPK:
                return (self._ext_dl_agent.get_progress(), True)
            if self.state == ext_c.EXT_STATE_PATCH_DOWNLOADING:
                return (self._ext_dl_agent.get_progress(), True)
            if self.state == ext_c.EXT_STATE_PATCH_INFO_ANALYZE:
                return (self.get_ext_patch_info_analyze_progress(), True)
            if self.state == ext_c.EXT_STATE_PATCH_COPYING:
                return (self.get_ext_patch_copy_progress(), True)
            if self.state == ext_c.EXT_STATE_PATCH_NPK_UPDATE:
                return (self._npk_update_prog, True)
            if self.state == ext_c.EXT_STATE_PATCH_NPK_VERIFY:
                return (self._npk_update_prog, True)
            return (
             0.0, False)
        except Exception as e:
            cout_error(LOG_CHANNEL, 'get_progress with exception:{}'.format(str(e)))

        return (0.0, False)

    def get_ext_patch_info_analyze_progress(self):
        return min(1.0, self.ext_patch_analyze_info_progress)

    def get_ext_patch_copy_progress(self):
        return self._ext_patch_copy_progress

    def set_npk_update_prog(self, in_value):
        self._npk_update_prog = in_value

    def get_cur_ver_str(self):
        engine_v = game3d.get_engine_version()
        engine_svn = game3d.get_engine_svn_version()
        script_v = str(self.ver_config.get('svn_version', 0))
        return '{}.{}.{}'.format(engine_v, engine_svn, script_v)

    def _check_ext_need_patch(self):
        target_version = self._patch_target_version
        self._ext_ver_config = ext_package_utils.get_local_save_ext_version_config()

        def check_local_ver_need_patch(in_ext_name):
            if in_ext_name not in self._ext_ver_config:
                cout_info(LOG_CHANNEL, 'ext:{} has no local ver'.format(in_ext_name))
                return True
            ext_ver = self._ext_ver_config[in_ext_name]
            cout_info(LOG_CHANNEL, 'ext:{} ver:{} t_ver:{}'.format(in_ext_name, ext_ver, target_version))
            if int(ext_ver) < int(target_version):
                return True
            return False

        active_ext_lst = self.get_active_ext_name_lst()
        for ext_name in self._ext_package_config:
            if not self._is_real_ext_package:
                cout_info(LOG_CHANNEL, 'old package, check and dl patch:{}'.format(ext_name))
                if check_local_ver_need_patch(ext_name):
                    return True
            elif ext_name in active_ext_lst:
                if ext_name not in self._ext_ver_config:
                    ext_ver = self._using_ext_config_dict[ext_name]['version']
                else:
                    ext_ver = self._ext_ver_config[ext_name]
                cout_info(LOG_CHANNEL, 'using ext:{} ver:{} t_ver:{}'.format(ext_name, ext_ver, target_version))
                if int(ext_ver) < int(target_version):
                    return True
            else:
                cout_info(LOG_CHANNEL, '{} no in using, skip patch'.format(ext_name))

        return False

    def download_ext_npk_list(self, cb):
        self._ext_npk_list_download_cb = cb
        self._ext_npk_list_info = {}
        self.set_state(ext_c.EXT_STATE_DOWNLOAD_NPK_LIST)
        ext_npk_list_url = ext_package_utils.get_ext_npk_list_url(self.server_config)
        temp_file_path = os.path.join(patch_path.TEMP_DIRNAME, ext_c.EXT_PATCH_LIST_NAME)
        list_orbit_path = patch_path.get_orbit_download_path(temp_file_path)
        list_rw_path = patch_path.get_rw_path(temp_file_path)
        download_list = [(list_orbit_path, list_rw_path, ext_npk_list_url, 0)]
        if not self._ext_dl_agent.start_download(download_list, self._on_download_ext_npk_list_callback):
            cout_error(LOG_CHANNEL, 'npk list start_download return false')
            self._ext_npk_list_callback(ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_ERROR)

    def _ext_npk_list_callback(self, state):
        cout_info(LOG_CHANNEL, 'ext npk list cb:{}'.format(state))
        if self._ext_npk_list_download_cb:
            self._ext_npk_list_download_cb(state)

    def _on_download_ext_npk_list_callback(self, success_list, error_list, consume_time):
        if error_list:
            dl_url = error_list[0][2]
            cout_error(LOG_CHANNEL, 'dl ext list:{} error'.format(dl_url))
            self._ext_npk_list_callback(ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_ERROR)
        else:
            cout_info(LOG_CHANNEL, 'dl ext list time:{}'.format(consume_time))
            file_path = success_list[0][1]
            try:
                with open(file_path, 'rb') as tmp_file:
                    data = tmp_file.read()
                data = six.ensure_str(data)
                _, _, self._ext_npk_list_info = ext_package_utils.analyze_valid_ext_npk_list_info(data)
                cout_info(LOG_CHANNEL, 'npk list info len:{}'.format(len(self._ext_npk_list_info)))
                self._ext_npk_list_callback(ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_FINISHED)
            except Exception as e:
                self._err_log('read dl npk list except:{} exist:{}'.format(str(e), os.path.exists(file_path)))
                self._ext_npk_list_callback(ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_ERROR)
                return

    def _ext_config_analyze_callback(self, state):
        if self._ext_keys_config_download_cb:
            self._ext_keys_config_download_cb(state)

    def ext_npk_config_analyze(self, cb=None, need_set_cb=True):
        self.set_state(ext_c.EXT_STATE_CONFIG_ANALYZE)
        if need_set_cb:
            self._ext_keys_config_download_cb = cb
        if not self._update_npk_config_data():
            self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_DOWNLOAD_ERROR)
            return
        need_download_config_exts = []
        need_download_npk_exts = []
        downloaded_config_exts = []
        self._need_download_npk_exts = []
        original_using_ext_lst = six_ex.keys(self._using_ext_config_dict)
        for tmp_ext_name in original_using_ext_lst:
            if not self._using_ext_config_dict[tmp_ext_name]['config_exist']:
                ext_package_utils.other_err_log(LOG_CHANNEL, 'using ext but config not exists:{}'.format(tmp_ext_name))
                continue
            cnt_version = int(self._using_ext_config_dict[tmp_ext_name]['version'])
            all_npk_exist = self._using_ext_config_dict[tmp_ext_name]['all_npk_exist']
            if not all_npk_exist and cnt_version not in self._ext_npk_list_info:
                self._err_log('using ext version:{} not in npk list:{}'.format(cnt_version, six_ex.keys(self._ext_npk_list_info)))
                self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_DOWNLOAD_ERROR)
                return

        original_using_ext_lst = six_ex.keys(self._using_ext_config_dict)
        for tmp_ext_name in original_using_ext_lst:
            config_exist = self._using_ext_config_dict[tmp_ext_name]['config_exist']
            all_npk_exist = self._using_ext_config_dict[tmp_ext_name]['all_npk_exist']
            if config_exist:
                if all_npk_exist:
                    downloaded_config_exts.append(tmp_ext_name)
                else:
                    need_download_npk_exts.append(tmp_ext_name)
            else:
                need_download_config_exts.append(tmp_ext_name)

        if need_download_config_exts:
            self._download_remote_ext_configs(need_download_config_exts)
        elif need_download_npk_exts:
            self._need_download_npk_exts = need_download_npk_exts
            self.download_missing_npk()
        else:
            self._verify_ext_npk_files(downloaded_config_exts)

    def _download_remote_ext_configs(self, need_download_config_keys):
        self.set_state(ext_c.EXT_STATE_DL_MISSING_EXT_CONFIG)
        cout_info(LOG_CHANNEL, 'dl remote config:{}'.format(need_download_config_keys))
        download_list = ext_package_utils.get_ext_configs_download_items(need_download_config_keys, self._ext_npk_list_info, self._using_ext_info)
        if not download_list:
            self._err_log('ext config has not match version{} {}'.format(six_ex.keys(self._ext_npk_list_info), self._using_ext_info))
            self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_DOWNLOAD_ERROR)
            return
        if not self._ext_dl_agent.start_download(download_list, self._on_download_ext_config_callback):
            cout_error(LOG_CHANNEL, 'start dl remote config fail')
            self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_DOWNLOAD_ERROR)
            return

    def _on_download_ext_config_callback(self, success_list, error_list, consume_time):
        if error_list:
            self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_DOWNLOAD_ERROR)
        else:
            self.ext_npk_config_analyze(need_set_cb=False)

    def download_missing_npk(self):
        cout_info(LOG_CHANNEL, 'dl miss ext npk:{}'.format(self._need_download_npk_exts))
        self.set_state(ext_c.EXT_STATE_DL_MISSING_EXT_NPK)
        download_list = []
        for ext_name in self._need_download_npk_exts:
            ext_npk_state = self._using_ext_config_dict[ext_name]['npk_state']
            npk_version = self._using_ext_config_dict[ext_name]['version']
            for tmp_npk_name in ext_npk_state:
                npk_exists, is_active = ext_npk_state[tmp_npk_name]
                if npk_exists:
                    continue
                rw_path = ext_package_utils.get_ext_rw_path(tmp_npk_name)
                orbit_path = ext_package_utils.get_ext_orbit_download_path(tmp_npk_name)
                dl_url = self._get_ext_npk_dl_url(tmp_npk_name, npk_version)
                npk_md5, npk_size = self._using_ext_config_dict[ext_name]['fit_npk_info'][tmp_npk_name]
                download_list.append((orbit_path, rw_path, dl_url, npk_size, npk_md5))

        if not download_list:
            cout_info(LOG_CHANNEL, 'no npk dl list')
            game3d.frame_delay_exec(1, self._delay_ext_npk_config_analyze)
            return
        total_download_size = 0
        for data in download_list:
            total_download_size += data[3]

        ext_package_utils.del_ext_npk_md5_checked_flag()
        if not self._ext_dl_agent.start_download(download_list, self._on_download_missing_npk_cb, total_download_size, False):
            cout_error(LOG_CHANNEL, 'start dl remote config fail')
            self._ext_config_analyze_callback(ext_c.EXT_STATE_DL_MISSING_EXT_NPK_FAILED)

    def _on_download_missing_npk_cb(self, success_list, error_list, consume_time):
        if error_list:
            cout_error(LOG_CHANNEL, 'download missing npk error')
            self._ext_config_analyze_callback(ext_c.EXT_STATE_DL_MISSING_EXT_NPK_FAILED)
        else:
            cout_info(LOG_CHANNEL, 'dl miss npk time:{}'.format(consume_time))
            self.ext_npk_config_analyze(need_set_cb=False)

    def _delay_ext_npk_config_analyze(self):
        self.ext_npk_config_analyze(need_set_cb=False)

    def _verify_ext_npk_files(self, ext_list):
        self.set_state(ext_c.EXT_STATE_VERIFYING_EXT_NPK)
        self._init_ext_npk_file_verification_data()
        self._ext_npk_verify_ext_lst = ext_list
        self._get_ext_npk_to_verify_size()
        t = threading.Thread(target=self._do_verify_ext_npk_files)
        t.setDaemon(True)
        t.start()

    def _do_verify_ext_npk_files(self):
        cout_info(LOG_CHANNEL, 'verify ext npk:{}'.format(self._ext_npk_verify_ext_lst))
        self._valid_npk_list = []
        invalid_list = []
        need_check_md5 = not ext_package_utils.is_ext_npk_md5_checked()
        for ext_name in self._ext_npk_verify_ext_lst:
            fit_npk_info = self._using_ext_config_dict[ext_name]['fit_npk_info']
            npk_version = self._using_ext_config_dict[ext_name]['version']
            for tmp_npk_name in fit_npk_info:
                npk_path = ext_package_utils.get_ext_rw_path(tmp_npk_name)
                npk_md5, npk_size = fit_npk_info[tmp_npk_name]
                if not os.path.exists(npk_path):
                    invalid_list.append((ext_name, tmp_npk_name))
                    self._ext_npk_checked_size += npk_size
                    continue
                if need_check_md5:
                    try:
                        m = hashlib.md5()
                        with open(npk_path, 'rb') as tmp_file:
                            file_buffer = tmp_file.read(patch_const.CHUNK_SIZE)
                            while file_buffer:
                                self._ext_npk_checked_size += len(file_buffer)
                                m.update(file_buffer)
                                file_buffer = tmp_file.read(patch_const.CHUNK_SIZE)

                        if str(m.hexdigest()) == npk_md5:
                            self._valid_npk_list.append(tmp_npk_name)
                        else:
                            local_size = os.path.getsize(npk_path)
                            invalid_list.append(tmp_npk_name)
                            cout_error(LOG_CHANNEL, 'ver:{} ext npk:{} md5 not matched:{}:{}'.format(npk_version, tmp_npk_name, npk_size, local_size))
                            os.remove(npk_path)
                    except Exception as e:
                        self._err_log('verify ext npk md5 with exception:{}'.format(str(e)))
                        invalid_list.append(tmp_npk_name)

                else:
                    try:
                        local_size = os.path.getsize(npk_path)
                        if int(npk_size) == int(local_size):
                            self._valid_npk_list.append(tmp_npk_name)
                        else:
                            invalid_list.append(tmp_npk_name)
                            cout_error(LOG_CHANNEL, 'ver:{} ext npk:{} size not matched:{}:{}'.format(npk_version, tmp_npk_name, npk_size, local_size))
                            os.remove(npk_path)
                    except Exception as e:
                        self._ext_npk_checked_size += npk_size
                        self._err_log('verify ext npk with exception:{}'.format(str(e)))
                        invalid_list.append(tmp_npk_name)

                    self._ext_npk_checked_size += npk_size

        if invalid_list:
            game3d.frame_delay_exec(1, self._delay_ext_npk_config_analyze)
        else:
            game3d.frame_delay_exec(1, self.ext_npk_phase_done)

    def ext_npk_phase_done(self):
        met_error = False
        if self.add_ext_npk(self._valid_npk_list):
            ret = self._update_npk_config_data()
            now_active_set = set(self.get_active_ext_name_lst())
            using_ext_set = set(self._using_ext_info)
            if not ret or using_ext_set != now_active_set:
                other_err_log(LOG_CHANNEL, '[active_not_equal_using]:{} {}'.format(now_active_set, using_ext_set))
                met_error = True
        else:
            met_error = True
        if met_error:
            cout_error(LOG_CHANNEL, 'ext_npk_done_phase_met_error, retry')
            if hasattr(C_file, 'del_fileloader_by_tag'):
                C_file.del_fileloader_by_tag(ext_c.EXT_NPK_LOADER_TAG)
            self._ext_config_analyze_callback(ext_c.EXT_STATE_ADD_RES_NPK_FAILED)
        else:
            cout_info(LOG_CHANNEL, 'ext_npk_phase_done')
            self._ext_config_analyze_callback(ext_c.EXT_STATE_CONFIG_ANALYZE_FINISHED)

    def stop_patch_downloader(self):
        self.force_stop = True
        self._ext_dl_agent.stop_download()

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_npk_keys_config_path(self):
        return patch_path.get_rw_path(ext_c.EXT_REMOTE_KEYS_CONFIG_NAME)

    def _init_ext_npk_file_verification_data(self):
        self.ext_npk_verify_total_size = 0.0
        self._ext_npk_checked_size = 0.0
        self._ext_npk_verify_ext_lst = []

    def add_ext_npk(self, npk_name_list):
        root_dir = '%%WORK_DIR%%\\{}\\%s'.format(ext_c.EXTEND_FOLDER)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            root_dir = '%%DOC_DIR%%\\{}\\%s'.format(ext_c.EXTEND_FOLDER)
        for npk_filename in npk_name_list:
            name = npk_filename[:-4]
            root = root_dir % name
            if self._enable_patch_npk:
                ret = C_file.add_res_npk_loader(root, 0, ext_c.EXT_NPK_LOADER_TAG)
            else:
                ret = C_file.add_res_npk_loader(root, 0)
            if not ret:
                self._err_log('add_npk_loader_failed')
                return False
            npk_flist_path = patch_path.RES_FLIST_FILE_PARTTEN % name
            flist_exists = C_file.find_res_file(npk_flist_path, '')
            if not flist_exists:
                self._err_log('add_npk_loader_success_flist_not_exists')
                return False

        self._drpf('ExtMgr_ADD_NPK_SUCCESS', {'msg': 'npk:{}'.format(npk_name_list)})
        ext_package_utils.save_ext_npk_md5_checked_flag()
        return True

    def _init_patch_info(self):
        patch_list = six.moves.builtins.__dict__.get('PATCH_LIST', [])
        if not patch_list:
            cout_info(LOG_CHANNEL, 'PATCH_LIST in __builtin__ is None, no need ext patch')
        else:
            self._patch_target_version = int(patch_list[0].target_version)
        self._patch_list = patch_list

    def _init_ext_patch_analyze_info(self):
        self.ext_patch_error_list = []
        self._ext_patch_analyze_callback = None
        self.ext_patch_size = 0.0
        self.downloaded_ext_patch_size = 0.0
        self.ext_patch_analyze_info_progress = 0.0
        self._update_fmap = {}
        self._ext_update_fmap = {}
        self._target_fmap = {}
        self._downloaded_fmap = {}
        self._ext_patch_fpath_temp_path_map = {}
        self._ext_patch_url_map = {}
        return

    def _check_ext_patch_npk(self):
        if not self._enable_patch_npk:
            return True
        from .ext_pn_utils import verify_ext_patch_npk
        try:
            check_ret = verify_ext_patch_npk()
        except Exception as e:
            other_err_log('ext_patch_npk', '[except] verify ext patch npk:{}'.format(str(e)))
            return False

        if not check_ret:
            need_dl_file_lst = []
            for ext_name in self._ext_package_config:
                flist_name = ext_c.LOCAL_SAVED_EXT_FLIST_PATTERN.format(ext_name)
                ext_flist_path = ext_package_utils.get_ext_flist_path(flist_name)
                need_dl_file_lst.append(ext_flist_path)

            ext_version_path = os.path.join(patch_path.get_neox_dir(), ext_c.EXT_VERSION_PATH)
            need_dl_file_lst.append(ext_version_path)
            from .ext_pn_utils import get_ext_patch_npk_info_file_path
            npk_info_path = get_ext_patch_npk_info_file_path()
            need_dl_file_lst.append(npk_info_path)
            try:
                for del_path in need_dl_file_lst:
                    if os.path.exists(del_path):
                        os.remove(del_path)

            except Exception as e:
                other_err_log('ext_patch_npk', '[except] check_ext_patch_npk:{}'.format(str(e)))
                return False

        return True

    def ext_patch_info_analyze(self, cb):
        self._init_ext_patch_analyze_info()
        self.set_state(ext_c.EXT_STATE_PATCH_INFO_ANALYZE)
        self._ext_patch_analyze_callback = cb
        if not self._check_ext_patch_npk():
            self._drpf('ExtMgr_PATCH_1', {'msg': 'check ext patch npk error'})
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
            return
        if not self._patch_list:
            self._drpf('ExtMgr_PATCH_1_0', {'msg': 'no patch list'})
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
            return
        ext_need_patch_for_version_check = self._check_ext_need_patch()
        if not ext_need_patch_for_version_check:
            cout_info(LOG_CHANNEL, 'no need ext patch for version')
            self._drpf('ExtMgr_PATCH_1_1', {'msg': 'no need ext patch for version'})
            self.ext_patch_analyze_info_progress = 1.0
            if self._enable_patch_npk:
                from .ext_pn_utils import insert_ext_npk_loader
                ret = insert_ext_npk_loader()
                if not ret:
                    cout_error(LOG_CHANNEL, 'insert ext patch npk for version failed')
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                else:
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
                return
            else:
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
                return

        else:
            target_version = self._patch_target_version
            target_flist_md5 = self._patch_list[0].filelist_md5
            filelist_data = patch_utils.get_temp_flist_data(target_version, target_flist_md5)
            if not filelist_data:
                cout_error(LOG_CHANNEL, 'local has no flist:{} then download'.format(target_version))
                self._drpf('ExtMgr_PATCH_1_2', {'msg': 'local has no flist:{} then download'.format(target_version)})
                flist_url = self._get_flist_url(self._patch_list[0].url)
                flist_rw_path = patch_path.get_temp_flst_rw_path(int(target_version))
                flist_orbit_path = patch_path.get_temp_flst_orbit_path(int(target_version))
                download_list = [(flist_orbit_path, flist_rw_path, flist_url, 0)]
                if not self._ext_dl_agent.start_download(download_list, self._on_download_filelist_callback, 0):
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                    return
            else:
                self._begin_analyze_ext_patch(filelist_data)

    def _get_flist_url(self, in_url):
        if self._is_normal_res and self._support_ui_astc:
            flist_name = 'flist_astc.lst'
        else:
            flist_name = 'flist.lst'
        return '{}/{}'.format(in_url, flist_name)

    def _on_download_filelist_callback(self, success_list, error_list, consume_time):
        if error_list:
            url = error_list[0][2]
            cout_info(LOG_CHANNEL, '[PATCH]: dl filelist error:{}'.format(url))
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
        else:
            cout_info(LOG_CHANNEL, '[PATCH]: dl filelist success')
            file_path = success_list[0][1]
            if not os.path.exists(file_path):
                self._err_log('dl filelist success but no file path')
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
            else:
                try:
                    with open(file_path, 'rb') as tmp_file:
                        filelist_data = tmp_file.read()
                except Exception as e:
                    self._err_log('read flist data exception:{}'.format(str(e)))
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                    return

                self._begin_analyze_ext_patch(filelist_data)

    def _begin_analyze_ext_patch(self, compress_filelist_data):
        t = threading.Thread(target=self._thread_analyze_ext_patch, args=(compress_filelist_data,))
        t.setDaemon(True)
        t.start()

    def _thread_analyze_ext_patch(self, in_compress_filelist_data):
        try:
            data = zlib.decompress(six.ensure_binary(in_compress_filelist_data))
            self._new_flist_map = patch_utils.read_filelist(data)
        except Exception as e:
            self._err_log('get flist data except:{}'.format(str(e)))
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
            return

        active_npk_lst = self.get_active_ext_npk_lst()
        active_ext_lst = self.get_active_ext_name_lst()
        if not self._is_real_ext_package and (active_ext_lst or active_npk_lst):
            self._err_log('not real ext package has active ext npk')
        new_total_flist_dict, total_count = ext_package_utils.filter_for_ext_flist(self._new_flist_map)
        self._new_total_ext_flist_dict = new_total_flist_dict
        cout_info(LOG_CHANNEL, 'total flist ext name:{} total count:{}'.format(six_ex.keys(new_total_flist_dict), total_count))
        if total_count == 0 or self._patch_target_version == 0:
            self._err_log('patch error:{} {} {}'.format(total_count, not self._patch_list, self._patch_target_version))
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
            return
        local_npk_fmap, ret = ext_package_utils.get_local_npk_flist_info(active_npk_lst)
        if not ret:
            cout_error(LOG_CHANNEL, 'get_local_npk_flist_info failed')
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
            return
        cout_info(LOG_CHANNEL, 'active: {} local npk fmap:{}'.format(active_npk_lst, len(local_npk_fmap)))
        all_ext_name = six_ex.keys(new_total_flist_dict)
        local_ext_flist_map = {}
        for ext_name in all_ext_name:
            if self._enable_patch_npk:
                local_ext_flist_map[ext_name] = {}
            else:
                if ext_name in active_ext_lst:
                    cnt_flist_map = ext_package_utils.get_local_ext_flist(ext_name)
                else:
                    flist_exists, cnt_flist_map = ext_package_utils.get_saved_local_ext_flist(ext_name)
                local_ext_flist_map[ext_name] = ext_package_utils.filter_resource(cnt_flist_map)

        if self._enable_patch_npk:
            from .ext_pn_utils import create_ext_patch_npk_folder
            if not create_ext_patch_npk_folder():
                cout_error(LOG_CHANNEL, 'create ext patch npk folder failed')
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                return
            self._destroy_patch_npk_processor()
            from . import ext_patch_npk
            self._patch_npk_processor = ext_patch_npk.ExtPatchNpkProcessor()
            if not self._patch_npk_processor.init_npk_file_info():
                cout_error(LOG_CHANNEL, 'init patch npk failed')
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                return
            self._patch_npk_processor.set_new_flist_map(self._new_flist_map)
            self._patch_npk_processor.set_local_npk_flist_map(local_npk_fmap)
        now_unit = 1.0 / total_count
        can_record = hasattr(patch_utils, 'get_patched_file_dict')
        for ext_name in new_total_flist_dict:
            if self._is_real_ext_package and ext_name not in active_ext_lst:
                cout_info(LOG_CHANNEL, 'new package has not active ext:{}'.format(ext_name))
                continue
            new_ext_flist_map = new_total_flist_dict[ext_name]
            now_ext_flist_map = local_ext_flist_map[ext_name]
            for f_path, f_info in six.iteritems(new_ext_flist_map):
                if ext_name not in self._target_fmap:
                    self._target_fmap[ext_name] = {}
                self._target_fmap[ext_name][f_path] = f_info
                if self._enable_patch_npk:
                    check_res = self._check_patch_item_need_download_patch_npk(f_info, local_npk_fmap)
                else:
                    check_res = self._check_patch_item_need_download_old(now_ext_flist_map, f_info, local_npk_fmap)
                if check_res != ext_c.EXT_PATCH_FILE_STATE_SAME:
                    self.ext_patch_size += int(f_info[3])
                    self._update_fmap[f_path] = f_info
                    if ext_name not in self._ext_update_fmap:
                        self._ext_update_fmap[ext_name] = {}
                    file_target_ver = self._get_patch_file_target_version(f_info)
                    if file_target_ver not in self._ext_update_fmap[ext_name]:
                        self._ext_update_fmap[ext_name][file_target_ver] = []
                    self._ext_update_fmap[ext_name][file_target_ver].append(f_info)
                    if check_res == ext_c.EXT_PATCH_FILE_STATE_DOWNLOADED:
                        self.downloaded_ext_patch_size += int(f_info[3])
                        self._downloaded_fmap[f_path] = f_info
                    else:
                        ext_package_utils.check_physxcook(f_path)
                if can_record:
                    patch_utils.PATCHED_FILE_DICT[f_path] = f_info
                self.ext_patch_analyze_info_progress += now_unit

        if self.ext_patch_size == 0 and self._patch_target_version:
            if self._enable_patch_npk:
                ret = self._ext_patch_npk_flush_and_verify()
                cout_info('ext_patch_npk', 'update and flush npk in analyze flist stage:{}'.format(ret))
                if not ret:
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                    return
                cout_info('ext_patch_npk', 'update and flush npk in analyze flist stage success')
                from .ext_pn_utils import insert_ext_npk_loader
                ret = insert_ext_npk_loader()
                if not ret:
                    cout_error('ext_patch_npk', 'insert ext npk loader in analyze flist stage failed')
                    self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
                    return
                cout_info('ext_patch_npk', 'ext patch size is zero, insert ext npk success')
            cout_info(LOG_CHANNEL, 'ext patch size is zero, save ver')
            self._save_ext_version()
            self.set_state(ext_c.EXT_STATE_PATCH_DONE)
        self.ext_patch_analyze_info_progress = 1.0
        self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)

    def ext_patch_info_analyze_callback(self, state):
        if self._ext_patch_analyze_callback:
            self._ext_patch_analyze_callback(state)

    def _ext_patch_zip_config_analyze_callback(self, state):
        if self._patch_zip_config_analyze_cb:
            self._patch_zip_config_analyze_cb(state)

    def ext_patch_zip_config_analyze(self, cb):
        self.set_state(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP)
        self._patch_zip_config_analyze_cb = cb
        if patch_path.PATCH_CONFIG_FILE_NAME in self._new_flist_map:
            self._patch_config_in_flist = self._new_flist_map[patch_path.PATCH_CONFIG_FILE_NAME]
            self._try_analyze_patch_config()
        else:
            self._err_log('has no patch_config in flist')
            self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FINISH)

    def _try_analyze_patch_config(self):
        cout_info(LOG_CHANNEL, '[PATCH] 2: try analyze patch config')
        try:
            target_version = self._patch_target_version
            temp_patch_config_data = patch_utils.get_temp_patch_config_data(target_version, self._patch_config_in_flist)
            if temp_patch_config_data:
                pkg_crc_patch_config = int(self._patch_config_in_flist[2])
                if not patch_utils.check_data_crc32(temp_patch_config_data, pkg_crc_patch_config):
                    cout_error(LOG_CHANNEL, 'patch config check crc failed:{} {}'.format(target_version, pkg_crc_patch_config))
                    self._do_download_patch_config(target_version)
                else:
                    self._thread_analyze_patch_config(temp_patch_config_data)
                return
            self._do_download_patch_config(target_version)
        except Exception as e:
            self._err_log('try_analyze_patch_config with except:{}'.format(str(e)))
            self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FAILED)

    def _do_download_patch_config(self, version):
        cout_info(LOG_CHANNEL, '[PATCH] 2: download patch config')
        config_url = self._get_patch_config_url()
        config_rw_path = patch_path.get_patch_config_rw_path(version)
        config_orbit_path = patch_path.get_patch_config_orbit_path(version)
        file_size = int(self._patch_config_in_flist[3])
        download_list = [(config_orbit_path, config_rw_path, config_url, file_size)]
        if not self._ext_dl_agent.start_download(download_list, self._on_download_patch_config_callback, file_size):
            cout_error(LOG_CHANNEL, 'download patch config failed')
            self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FAILED)

    def _on_download_patch_config_callback(self, success_list, error_list, consume_time):
        if error_list:
            cout_info(LOG_CHANNEL, '[PATCH] 2: dl patch config failed')
            self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FAILED)
        else:
            file_path = success_list[0][1]
            if not os.path.exists(file_path):
                cout_error(LOG_CHANNEL, '[PATCH] 2: dl patch config success but not exists:{}'.format(file_path))
                self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FAILED)
            else:
                cout_info(LOG_CHANNEL, '[PATCH] 2: dl patch config success')
                self._try_analyze_patch_config()

    def _thread_analyze_patch_config(self, patch_config_data):
        t = threading.Thread(target=self._do_analyze_patch_config, args=(patch_config_data,))
        t.setDaemon(True)
        t.start()

    def _do_analyze_patch_config(self, patch_config_data):
        cout_info(LOG_CHANNEL, '[PATCH] 2: do analyze patch config')
        try:
            data = zlib.decompress(six.ensure_binary(patch_config_data))
            data_dict = json.loads(data)
        except Exception as e:
            data_dict = {}
            self._err_log('decompress or loads exception:{}'.format(str(e)))
            self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FAILED)

        self._zip_patch_download_list = []
        self._zip_patch_download_size = 0
        self._patch_zip_info_dict = {}
        self._zip_analyze_prog = 0.0
        patch_res_type = patch_utils.get_patch_res_type()
        patch_zip_pattern = ext_package_utils.get_ext_patch_zip_pattern()
        analyze_ext_lst = six_ex.keys(self._new_total_ext_flist_dict)
        cout_info(LOG_CHANNEL, 'patch config ext lst:{}'.format(analyze_ext_lst))
        for ext_name in analyze_ext_lst:
            zip_key = ext_package_utils.get_ext_patch_zip_name(ext_name)
            patch_zip_info = data_dict.get(zip_key, {})
            if not patch_zip_info:
                cout_info(LOG_CHANNEL, 'ext:{} has no patch zip info'.format(ext_name))
                continue
            for patch_list_info in self._patch_list:
                if patch_list_info.patch_type == patch_critical_info.PATCH_TYPE_FULL:
                    break
                tmp_tar_ver = int(patch_list_info.target_version)
                version_str = str(tmp_tar_ver)
                if version_str not in patch_zip_info:
                    continue
                else:
                    cnt_zip_info = patch_zip_info[version_str]
                    high_zip_size, high_zip_md5, low_zip_size, low_zip_md5 = (int(cnt_zip_info[0]), cnt_zip_info[1],
                     int(cnt_zip_info[2]), cnt_zip_info[3])
                    zip_size = high_zip_size if patch_res_type == patch_utils.PATCH_RES_TYPE_HIGH else low_zip_size
                    if patch_res_type == patch_utils.PATCH_RES_TYPE_HIGH:
                        zip_md5 = high_zip_md5 if 1 else low_zip_md5
                        zip_rw_path = ext_package_utils.get_ext_patch_zip_rw_path(patch_zip_pattern, ext_name, tmp_tar_ver)
                        zip_orbit_path = ext_package_utils.get_ext_patch_zip_orbit_path(patch_zip_pattern, ext_name, tmp_tar_ver)
                        zip_info = [
                         tmp_tar_ver, zip_size, zip_md5, zip_rw_path, zip_orbit_path,
                         patch_utils.PATCH_ZIP_DOWNLOAD_STATE_INIT,
                         0,
                         self._get_zip_src_url(ext_name, patch_zip_pattern, tmp_tar_ver, patch_list_info)]
                        if os.path.exists(zip_rw_path):
                            zip_downloaded_size = os.path.getsize(zip_rw_path)
                            if zip_downloaded_size == zip_size:
                                if patch_utils.check_big_file_md5(zip_rw_path, zip_md5):
                                    zip_info[5] = patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED
                        if ext_name not in self._patch_zip_info_dict:
                            self._patch_zip_info_dict[ext_name] = {}
                        self._patch_zip_info_dict[ext_name][tmp_tar_ver] = zip_info

        for f_path, f_info in six.iteritems(self._new_flist_map):
            if not patch_utils.is_base_package_item(f_info):
                ext_name = f_info[6]
                f_tar_ver = self._get_patch_file_target_version(f_info)
                if ext_name in self._patch_zip_info_dict and f_tar_ver in self._patch_zip_info_dict[ext_name]:
                    self._patch_zip_info_dict[ext_name][f_tar_ver][6] += 1

        download_list = {}
        need_download_zip_dict = {}
        zip_download_dict = {}
        for f_path in self._ext_patch_fpath_temp_path_map:
            if f_path in self._downloaded_fmap:
                continue
            f_info = self._new_flist_map[f_path]
            ext_name = f_info[6]
            download_size = int(f_info[3])
            patch_file_version = self._get_patch_file_target_version(f_info)
            rw_path, orbit_path = self._ext_patch_fpath_temp_path_map[f_path]
            url = self._ext_patch_url_map[f_path]
            download_list.setdefault(ext_name, [])
            download_list[ext_name].append((orbit_path, rw_path, url, download_size))
            if ext_name not in self._patch_zip_info_dict:
                continue
            if patch_file_version in self._patch_zip_info_dict[ext_name]:
                need_download_zip_dict.setdefault(ext_name, {})
                if patch_file_version not in need_download_zip_dict[ext_name]:
                    need_download_zip_dict[ext_name][patch_file_version] = [
                     0, 0]
                need_download_zip_dict[ext_name][patch_file_version][0] += download_size
                need_download_zip_dict[ext_name][patch_file_version][1] += 1
                zip_download_dict.setdefault(ext_name, {})
                zip_download_dict[ext_name][orbit_path] = patch_file_version

        for tmp_ext_name in need_download_zip_dict:
            for tmp_target_ver in need_download_zip_dict[tmp_ext_name]:
                patch_zip_info = self._patch_zip_info_dict[tmp_ext_name][tmp_target_ver]
                if patch_zip_info[5] == patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                    continue
                need_download_zip_info = need_download_zip_dict[tmp_ext_name][tmp_target_ver]
                zip_size = max(patch_zip_info[1], 1)
                zip_file_num = max(patch_zip_info[6], 1)
                size_download_ratio = need_download_zip_info[0] * 1.0 / zip_size
                file_num_ratio = need_download_zip_info[1] * 1.0 / zip_file_num
                cout_info(LOG_CHANNEL, 'zip:{} ver:{} size:{} num:{} org_num:{}'.format(tmp_ext_name, tmp_target_ver, size_download_ratio, file_num_ratio, zip_file_num))
                if size_download_ratio < 0.3 and file_num_ratio < 0.3:
                    if tmp_target_ver in self._patch_zip_info_dict[tmp_ext_name]:
                        del self._patch_zip_info_dict[tmp_ext_name][tmp_target_ver]

        ext_names = six_ex.keys(self._patch_zip_info_dict)
        for tmp_ext_name in ext_names:
            if tmp_ext_name not in need_download_zip_dict:
                del self._patch_zip_info_dict[tmp_ext_name]
            else:
                ver_lst = six_ex.keys(self._patch_zip_info_dict[tmp_ext_name])
                for tmp_ver in ver_lst:
                    if tmp_ver not in need_download_zip_dict[tmp_ext_name]:
                        del self._patch_zip_info_dict[tmp_ext_name][tmp_ver]

        self._zip_patch_download_size = 0
        ret_list = []
        zip_num = 0
        if self._patch_zip_info_dict:
            for tmp_ext_name in self._patch_zip_info_dict:
                for tmp_ver, tmp_info in six.iteritems(self._patch_zip_info_dict[tmp_ext_name]):
                    zip_num += 1
                    if tmp_info[5] == patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                        continue
                    ret_list.append((tmp_info[4], tmp_info[3], tmp_info[7], tmp_info[1], tmp_info[2]))
                    self._zip_patch_download_size += tmp_info[1]

        discrete_num = 0
        for tmp_ext_name in download_list:
            for dl_item in download_list[tmp_ext_name]:
                orbit_path = dl_item[0]
                if tmp_ext_name in zip_download_dict and tmp_ext_name in self._patch_zip_info_dict:
                    if orbit_path in zip_download_dict[tmp_ext_name]:
                        zip_version = zip_download_dict[tmp_ext_name][orbit_path]
                        if zip_version in self._patch_zip_info_dict[tmp_ext_name]:
                            continue
                self._zip_patch_download_size += dl_item[3]
                ret_list.append(dl_item)
                discrete_num += 1

        info_msg = 'dl ext patch discrete num:{} zip num:{}'.format(discrete_num, zip_num)
        cout_info(LOG_CHANNEL, info_msg)
        self._drpf('ExtMgr_PATCH_2_1', {'msg': info_msg})
        self._zip_patch_download_list = ret_list
        self._ext_patch_zip_config_analyze_callback(ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FINISH)

    def download_ext_patch(self, cb):
        self.set_state(ext_c.EXT_STATE_PATCH_DOWNLOADING)
        self._ext_patch_download_cb = cb
        if patch_const.ENABLE_ZIP_DOWNLOAD and self._zip_patch_download_list:
            download_list = self._zip_patch_download_list
        else:
            download_list = self._generate_ext_patch_download_list()
        if download_list:
            download_list = sorted(download_list, key=cmp_to_key(--- This code section failed: ---

1143       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_ATTR             1  'compare'
           9  BINARY_SUBSCR    
          10  LOAD_FAST             1  'b'
          13  LOAD_CONST            1  3
          16  BINARY_SUBSCR    
          17  CALL_FUNCTION_2       2 
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
), reverse=False)
        if not download_list:
            cout_info(LOG_CHANNEL, 'no download list')
            self._ext_patch_files_analyze()
            return
        if patch_const.ENABLE_ZIP_DOWNLOAD:
            dl_size = self._zip_patch_download_size if 1 else self.get_ext_patch_size()
            self._ext_dl_agent.start_download(download_list, self._on_download_ext_patch_files_callback, dl_size) or cout_error(LOG_CHANNEL, 'download_ext_patch start failed')
            self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED)

    def _on_download_ext_patch_files_callback(self, success_list, error_list, consume_time):
        if error_list:
            self.ext_patch_error_list = error_list
            self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED)
        else:
            self._ext_patch_files_analyze()

    def _ext_patch_files_analyze(self):
        self.set_state(ext_c.EXT_STATE_PATCH_COPYING)
        self._ext_patch_copy_progress = 0.0
        t = threading.Thread(target=self._do_ext_patch_files_analyze)
        t.setDaemon(True)
        t.start()

    def _do_ext_patch_files_analyze(self):
        unit = 1.0 / max(1.0, len(self._update_fmap))
        last_branch_version = self._get_last_branch_version()
        for ext_name in self._ext_update_fmap:
            for target_v in self._ext_update_fmap[ext_name]:
                finfo_lst = self._ext_update_fmap[ext_name][target_v]
                ret = self._write_patch_file(ext_name, target_v, finfo_lst, unit, last_branch_version)
                if not ret:
                    self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED)
                    return

        if self._enable_patch_npk:
            ret = self._ext_patch_npk_flush_and_verify()
            print('[ext_patch_npk] update and flush npk:', ret)
            if not ret:
                self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED)
                return
            from .ext_pn_utils import insert_ext_npk_loader
            ret = insert_ext_npk_loader()
            print('[ext_patch_npk] insert ext npk loader after patch:', ret)
            if not ret:
                self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED)
                return
        self._ext_patch_copy_progress = 1.0
        ext_package_utils.save_all_ext_flist(self._target_fmap)
        self._save_ext_version()
        self.set_state(ext_c.EXT_STATE_PATCH_DONE)
        patch_path.remove_patch_temp_folder()
        self._ext_patch_download_callback(ext_c.EXT_STATE_PATCH_DOWNLOADED_FINISHED)

    def _write_patch_file(self, ext_name, cnt_flist_ver, in_finfo_lst, unit, last_branch_version):
        if patch_const.ENABLE_ZIP_DOWNLOAD:
            ret, zip_file = self._open_zip_file_with_version(ext_name, cnt_flist_ver)
            if not ret:
                return False
        else:
            zip_file = None

        def _close_zip_file(in_zip_file):
            if in_zip_file:
                try:
                    in_zip_file.close()
                except Exception as e:
                    print('[patch] close zip error: %s' % str(e))

        for f_info in in_finfo_lst:
            if self.force_stop:
                _close_zip_file(zip_file)
                return False
            fpath = f_info[0]
            self._ext_patch_copy_progress += unit
            zip_relative_path, file_index_id = ext_package_utils.get_ext_patch_file_hash_info(fpath)
            rw_temp_path, orbit_temp_path = self._ext_patch_fpath_temp_path_map[fpath]
            try:
                src_d = None
                pkg_crc_in_flist = int(f_info[2])
                if zip_file:
                    src_d = zip_file.read(zip_relative_path)
                    if not patch_utils.check_data_crc32(src_d, pkg_crc_in_flist):
                        self._err_log('check crc32 in zip failed:{} {} {} {}'.format(ext_name, cnt_flist_ver, zip_relative_path, pkg_crc_in_flist))
                        _close_zip_file(zip_file)
                        return False
                else:
                    try:
                        with open(rw_temp_path, 'rb') as tmp_file:
                            src_d = tmp_file.read()
                    except Exception as e:
                        self._err_log('[Except] [ext_patch] get data:{} from temp except:{}'.format(fpath, str(e)))
                        _close_zip_file(zip_file)
                        return False

                    if not patch_utils.check_data_crc32(src_d, pkg_crc_in_flist):
                        self._err_log('check crc32 failed:{} {} {} {} {}'.format(ext_name, fpath, cnt_flist_ver, zip_relative_path, pkg_crc_in_flist))
                        _close_zip_file(zip_file)
                        try:
                            os.remove(rw_temp_path)
                        except Exception as e:
                            cout_error(LOG_CHANNEL, 'os remove:{} except:{}'.format(rw_temp_path, str(e)))

                        return False
                if self._enable_patch_npk:
                    ret = self._patch_npk_processor.add_ext_patch_data(src_d, file_index_id, pkg_crc_in_flist, f_info)
                    if not ret:
                        _close_zip_file(zip_file)
                        return False
                else:
                    save_path = patch_path.get_download_target_path(fpath)
                    is_prev_patch = False
                    if cnt_flist_ver <= last_branch_version:
                        week_path = save_path.replace(patch_path.SCRIPT_PATCH_DIRNAME, patch_path.SCRIPT_PATCH_WEEKLY_NAME)
                        week_path = week_path.replace(patch_path.RES_PATCH_DIRNAME, patch_path.RES_PATCH_WEEKLY_NAME)
                        week_path = patch_path.get_rw_path(week_path)
                        is_prev_patch = True
                    else:
                        week_path = None
                        save_path = save_path.replace(patch_path.SCRIPT_PATCH_DIRNAME, patch_path.SCRIPT_PATCH_WEEKLY_NAME)
                        save_path = save_path.replace(patch_path.RES_PATCH_DIRNAME, patch_path.RES_PATCH_WEEKLY_NAME)
                    save_path = patch_path.get_rw_path(save_path)
                    with self._lock:
                        dir_name = os.path.dirname(save_path)
                        if not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        with open(save_path, 'wb') as tmp_w_file:
                            tmp_w_file.write(src_d)
                    if is_prev_patch:
                        try:
                            if os.path.exists(week_path):
                                os.remove(week_path)
                        except Exception as e:
                            self._err_log('os remove week path exception:{}'.format(str(e)))

            except (IOError, OSError) as ose:
                _close_zip_file(zip_file)
                self._err_log('analyze ext patch files os exception:{}'.format(str(ose)))
                if int(ose.errno) == 28:
                    self._ext_dl_agent.set_space_flag(True)
                return False
            except Exception as final_err:
                _close_zip_file(zip_file)
                self._err_log('analyze ext patch files exception:{}'.format(str(final_err)))
                return False

        _close_zip_file(zip_file)
        return True

    def _ext_patch_download_callback(self, state):
        if self._ext_patch_download_cb:
            self._ext_patch_download_cb(state)

    def _check_patch_item_need_download_old(self, now_fmap, new_f_info, local_npk_fmap):
        fpath = new_f_info[0]
        new_org_crc = int(new_f_info[1])
        if fpath not in now_fmap or int(now_fmap[fpath][1]) != new_org_crc:
            new_pkg_crc = int(new_f_info[2])
            if ext_package_utils.check_res_has_exists(fpath, new_org_crc, new_pkg_crc, local_npk_fmap):
                return ext_c.EXT_PATCH_FILE_STATE_SAME
            ret_state = self._update_download_info(fpath, new_pkg_crc, new_f_info)
            return ret_state
        return ext_c.EXT_PATCH_FILE_STATE_SAME

    def _check_patch_item_need_download_patch_npk(self, new_f_info, local_npk_fmap):
        fpath = new_f_info[0]
        new_org_crc = int(new_f_info[1])
        if fpath not in local_npk_fmap or int(local_npk_fmap[fpath][1]) != new_org_crc:
            new_pkg_crc = int(new_f_info[2])
            if self._patch_npk_processor.is_file_in_ext_patch_npk(fpath, new_pkg_crc):
                return ext_c.EXT_PATCH_FILE_STATE_SAME
            ret_state = self._update_download_info(fpath, new_pkg_crc, new_f_info)
            return ret_state
        return ext_c.EXT_PATCH_FILE_STATE_SAME

    def _update_download_info(self, fpath, new_pkg_crc, new_f_info):
        temp_path = patch_path.get_patch_file_rw_temp_path(fpath)
        orbit_temp_path = patch_path.get_patch_file_orbit_temp_path(fpath)
        self._ext_patch_fpath_temp_path_map[fpath] = (temp_path, orbit_temp_path)
        if ext_package_utils.check_res_in_patch_temp(fpath, new_pkg_crc):
            return ext_c.EXT_PATCH_FILE_STATE_DOWNLOADED
        else:
            download_url = self._get_ext_discrete_patch_url(new_f_info)
            self._ext_patch_url_map[fpath] = download_url
            return ext_c.EXT_PATCH_FILE_STATE_NEED_DOWNLOAD

    def _get_ext_discrete_patch_url(self, f_info):
        url = None
        patch_info = self._get_patch_file_target_version(f_info)
        for patch_list_item in self._patch_list:
            if patch_list_item.start_version < patch_info <= patch_list_item.target_version:
                url = patch_list_item.url + '/' + six.moves.urllib.parse.quote(patch_path.convert_to_hashed_file_path(f_info[0]))
                break

        return url

    def _generate_ext_patch_download_list(self):
        count = 0
        download_list = []
        for k, v in six.iteritems(self._update_fmap):
            if k in self._downloaded_fmap:
                continue
            f_info = self._update_fmap[k]
            download_size = int(f_info[3])
            rw_path, orbit_path = self._ext_patch_fpath_temp_path_map[k]
            url = self._ext_patch_url_map[k]
            count += 1
            download_list.append((orbit_path, rw_path, url, download_size))

        return download_list

    def _drpf(self, type_name, info):
        tool_inst = get_dctool_instane()
        if hasattr(tool_inst, 'ext_drpf_info'):
            tool_inst.ext_drpf_info(type_name, info)

    def _get_patch_file_target_version(self, f_info):
        if len(f_info) >= 8:
            return int(f_info[7])
        else:
            return int(f_info[5])

    def _err_log(self, error_msg):
        cout_error(LOG_CHANNEL, error_msg)
        patch_utils.send_script_error('{} {}'.format(ext_c.DRFP_ERROR_CHANNEL, error_msg))

    def get_ext_patch_size(self):
        return self.ext_patch_size - self.downloaded_ext_patch_size

    def _get_last_branch_version(self):
        weekly_info = self._patch_list[0].branch_info
        if not weekly_info:
            return 0
        for patch_list_item in self._patch_list:
            branch_info = patch_list_item.branch_info
            if branch_info and weekly_info != branch_info:
                return patch_list_item.target_version

        return 0

    def _get_patch_config_url(self):
        return self._patch_list[0].url + '/' + patch_path.convert_to_hashed_file_path(patch_path.PATCH_CONFIG_FILE_NAME)

    def _get_zip_src_url(self, ext_name, patch_zip_pattern, patch_version, patch_info):
        url = patch_info.url + '/' + six.moves.urllib.parse.quote(patch_zip_pattern % (ext_name, patch_version))
        return url

    def _get_ext_npk_dl_url(self, npk_name, npk_version):
        url = self._ext_npk_list_info[int(npk_version)]
        return url + '/' + npk_name

    def _get_ext_npk_to_verify_size(self):
        for ext_name in self._ext_npk_verify_ext_lst:
            fit_npk_info = self._using_ext_config_dict[ext_name]['fit_npk_info']
            for tmp_npk_name in fit_npk_info:
                npk_md5, npk_size = fit_npk_info[tmp_npk_name]
                self.ext_npk_verify_total_size += npk_size

    def _open_zip_files(self):
        ret_dict = {}
        import zipfile
        for ext_name in self._patch_zip_info_dict:
            for ver, zip_info in six.iteritems(self._patch_zip_info_dict[ext_name]):
                zip_path = zip_info[3]
                if not os.path.exists(zip_path):
                    self._err_log('zip path not exist:{}'.format(zip_path))
                    return (
                     False, ret_dict)
                if not os.path.getsize(zip_path) == zip_info[1]:
                    self._err_log('zip size not match:{} {}'.format(os.path.getsize(zip_path), zip_info[1]))
                    return (
                     False, ret_dict)
                if not patch_utils.check_big_file_md5(zip_path, zip_info[2]):
                    self._err_log('zip md5 not match:{} {}'.format(zip_path, zip_info[2]))
                    return (
                     False, ret_dict)
                zipf = zipfile.ZipFile(zip_path)
                if ext_name not in ret_dict:
                    ret_dict[ext_name] = {}
                ret_dict[ext_name][ver] = zipf

        return (
         True, ret_dict)

    def _open_zip_file_with_version(self, in_ext_name, in_zip_vesion):
        import zipfile
        if in_ext_name in self._patch_zip_info_dict:
            if in_zip_vesion in self._patch_zip_info_dict[in_ext_name]:
                zip_info = self._patch_zip_info_dict[in_ext_name][in_zip_vesion]
                zip_path = zip_info[3]
                if not os.path.exists(zip_path):
                    self._err_log('zip path not exist:{}'.format(zip_path))
                    return (
                     False, None)
                if not os.path.getsize(zip_path) == zip_info[1]:
                    self._err_log('zip size not match:{} {}'.format(os.path.getsize(zip_path), zip_info[1]))
                    return (
                     False, None)
                if not patch_utils.check_big_file_md5(zip_path, zip_info[2]):
                    self._err_log('zip md5 not match:{} {}'.format(zip_path, zip_info[2]))
                    return (
                     False, None)
                try:
                    zipf = zipfile.ZipFile(zip_path)
                except Exception as e:
                    self._err_log('zip file open error:{}'.format(str(e)))
                    return (
                     False, None)

                return (True, zipf)
            else:
                return (
                 True, None)

        else:
            return (
             True, None)
        return

    def _save_ext_version(self):
        all_ext_name_lst = six_ex.keys(self._new_total_ext_flist_dict)
        active_ext_lst = self.get_active_ext_name_lst()
        new_ver_config = {}
        for ext_name in all_ext_name_lst:
            if not self._is_real_ext_package:
                new_ver_config[ext_name] = self._patch_target_version
            elif ext_name in active_ext_lst:
                new_ver_config[ext_name] = self._patch_target_version

        ext_package_utils.save_ext_version_config(new_ver_config)

    def _ext_patch_npk_flush_and_verify(self):
        self.set_state(ext_c.EXT_STATE_PATCH_NPK_UPDATE)
        self._npk_update_prog = 0.0
        ret = self._patch_npk_processor.ext_update_and_flush_all_npk(self.set_npk_update_prog)
        if not ret:
            self._npk_update_prog = 1
            self._destroy_patch_npk_processor()
            return False
        self.set_state(ext_c.EXT_STATE_PATCH_NPK_VERIFY)
        self._npk_update_prog = 0.0
        ret = self._patch_npk_processor.verify_and_save_new_npk_info(self.set_npk_update_prog)
        self._destroy_patch_npk_processor()
        self._npk_update_prog = 1
        return ret

    def _destroy_patch_npk_processor(self):
        if self._patch_npk_processor:
            self._patch_npk_processor.destroy()
            self._patch_npk_processor = None
        return

    def destroy_callback(self):
        self._ext_keys_config_download_cb = None
        self._ext_npk_list_download_cb = None
        self._ext_patch_analyze_callback = None
        self._patch_zip_config_analyze_cb = None
        self._ext_patch_download_cb = None
        return

    def destroy_data(self):
        self._flist_data = None
        self._new_flist_map = {}
        self._new_total_ext_flist_dict = {}
        self._ext_npk_list_info = {}
        self._init_ext_patch_analyze_info()
        self._destroy_patch_npk_processor()
        return