# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/downloader.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from functools import cmp_to_key
import os
import sys
import time
import json
import six.moves.builtins
import six.moves.urllib.parse
import six.moves.urllib.error
import six.moves.urllib.request
import six.moves.collections_abc
import collections
import threading
import zlib
import traceback
import queue
import game3d
import C_file
import hashlib
from . import patch_utils
from . import patch_dctool
from . import patch_path
from . import patch_const
import package_utils
import six
from copy import deepcopy
from version import get_npk_version
from patch import patch_critical_info
from patch.downloader_agent import thread_downloader
from patch.downloader_agent import orbit_downloader
COM_NPK_LOADER = 'com_npk'
HIGH_END_NPK_NAME = 'highend'
LOW_END_NPK_NAME = 'lowend'
BASIC_COMPLETION_NPK_NAME = 'files'
NOW_PLATFORM = game3d.get_platform()
IS_WIN = NOW_PLATFORM == game3d.PLATFORM_WIN32
IS_MOBILE = NOW_PLATFORM in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID)
PLATFORM_NAME_DICT = {game3d.PLATFORM_ANDROID: 'android',
   game3d.PLATFORM_IOS: 'ios',
   'default': 'win32'
   }
NOW_PLATFORM_NAME = PLATFORM_NAME_DICT.get(NOW_PLATFORM, 'win32')
IS_PY3 = six.PY3

def get_patch_const_bool(attribute_name):
    if hasattr(patch_const, attribute_name):
        return getattr(patch_const, attribute_name)
    else:
        return False


class Downloader(object):

    def __init__(self, retqueue):
        self.is_orbit = False
        self.retqueue = retqueue
        self.is_error = False
        self.patch_fmap = None
        self.patch_fpath_temp_path_map = None
        self.patch_temp_path_fpath_map = None
        self.patch_fpath_url_map = None
        self.patch_size = 0
        self.patch_version = 0
        self.flist_data = None
        self.config = None
        self.verconfig = None
        self.lock = threading.Lock()
        self.err_queue = queue.Queue()
        self.msg_queue = queue.Queue()
        self.state = patch_utils.DST_PLIST
        self.network_type = 1
        self.analyze_prog = 0.0
        self.zip_analyze_prog = 0.0
        self.patch_list_redirect_url = ''
        self.npk_list_redirect_url = ''
        self.download_patch_url_file_map = {}
        self.patchlist = []
        self.patch_dctool = patch_dctool.get_dctool_instane()
        game3d.set_dump_info('project', self.patch_dctool.get_game_id())
        self.patch_download_id_str = '0'
        self.weekly_info = ''
        self.new_weekly_info = ''
        self.real_weekly_info = ''
        self.real_last_week_version = 0
        self._npk_svn_version = get_npk_version()
        self.init_config()
        self.patch_check_callback = None
        self.patch_files_dld_callback = None
        self.npk_check_callback = None
        self.downloader_agent = thread_downloader.ThreadDownloader(self.retqueue, self.err_queue, self.msg_queue)
        self.force_stop = False
        self._flist_error = False
        self.npk_file_info = {}
        self.npk_download_size = 0
        self._patch_npk_processor = None
        self.npk_prev_download_size = 0
        self.npk_unchecked_list = []
        self.npk_info_list = []
        self.patch_zip_info_dict = {}
        self.patch_zip_range_info_dict = {}
        self.zip_patch_download_list = []
        self.zip_patch_download_size = 0
        self._zip_dl_num = 0
        self._discrete_dl_num = 0
        self.config_flist_data = None
        self.patch_config_finfo = None
        self.patch_error_list = []
        self._support_astc = True
        self._support_new_ui_astc_patch = False
        self._support_completion_npk = True
        self._game_init_mode = package_utils.GAME_NO_INITED
        self._support_base_package = patch_utils.is_support_base_package()
        if IS_PY3:
            sys.setswitchinterval(100)
        else:
            sys.setcheckinterval(100)
        return

    def init_config(self):
        server_conf = C_file.get_res_file('confs/server.json', '')
        server_conf = json.loads(server_conf)
        self.config = server_conf
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        self.verconfig = version_conf
        six.moves.builtins.__dict__['ACE_PACKAGE_INNER'] = server_conf.get('ace_package_inner', 0)

    def set_network_type(self, network_type):
        self.network_type = network_type

    def get_patch_size(self):
        ret_size = self.patch_size
        if patch_const.ENABLE_ZIP_DOWNLOAD:
            ret_size = self.zip_patch_download_size
        return ret_size

    def get_download_num_info(self):
        return (
         self._discrete_dl_num, self._zip_dl_num)

    def is_flist_error(self):
        return self._flist_error

    def get_real_stand_npk_download_size(self):
        return self.npk_download_size - self.npk_prev_download_size

    def get_npk_size(self):
        return self.npk_download_size

    def get_patch_list_url(self):
        if self.patch_list_redirect_url:
            return six.ensure_str(self.patch_list_redirect_url)
        url_key = 'patch_list_url'
        if url_key in self.config:
            return six.ensure_str(self.config[url_key])
        url_channel_key = 'patch_list_url_channel'
        game_id = self.patch_dctool.get_game_id()
        try:
            game_id = 'g93_steam' if self.patch_dctool.is_steam_channel() else self.patch_dctool.get_game_id()
        except Exception as e:
            print('[Except] [patch] get patch list url except:{}\n{}'.format(str(e), traceback.format_exc()))
            game_id = self.patch_dctool.get_game_id()

        patch_list_conf = self.config[url_channel_key]
        return six.ensure_str(patch_list_conf.get(game_id, patch_list_conf['g93']))

    def get_npk_list_url(self):
        if self.npk_list_redirect_url:
            return six.ensure_str(self.npk_list_redirect_url)
        url_key = 'npk_list_url'
        if url_key in self.config:
            return six.ensure_str(self.config[url_key])
        url_channel_key = 'npk_list_url_channel'
        return six.ensure_str(self.config[url_channel_key][self.patch_dctool.get_game_id()])

    def is_ignore_week_patch(self):
        ignore_key = 'ignore_week_patch'
        if ignore_key in self.config:
            return True
        return False

    def get_patch_version(self):
        return self.patch_version

    def get_patch_fmap(self):
        return self.patch_fmap

    def get_cur_ver(self):
        return int(self.verconfig.get('svn_version', 0))

    def get_cur_ver_str(self):
        engine_v = game3d.get_engine_version()
        engine_svn = game3d.get_engine_svn_version()
        script_v = str(self.get_cur_ver())
        return '{}.{}.{}'.format(engine_v, engine_svn, script_v)

    def get_prog(self):
        if self.downloader_agent.downloading:
            return self.downloader_agent.get_progress()
        else:
            return self.analyze_prog

    def is_donwloading(self):
        return self.downloader_agent.downloading

    def get_speed(self):
        if self.downloader_agent.downloading:
            bytes_spd = self.downloader_agent.get_speed()
            return bytes_spd * 1.0 / 1048576.0
        else:
            return -1

    def set_patchlist(self, patch_list):
        six.moves.builtins.__dict__['PATCH_LIST'] = patch_list
        self.patchlist = patch_list

    def get_flist_md5(self):
        if self.patchlist:
            return self.patchlist[0].filelist_md5
        else:
            return None

    def get_flist_url(self, in_url=None):
        if IS_PY3:
            appendix = '_py3' if 1 else ''
            if self._support_new_ui_astc_patch:
                flist_name = 'flist_astc{}.lst'.format(appendix)
            else:
                flist_name = 'flist{}.lst'.format(appendix)
            dl_url = in_url if in_url else self.patchlist[0].url
            return dl_url or ''
        else:
            return '{}/{}'.format(dl_url, flist_name)

    def get_npk_info_url(self):
        if not self.npk_info_list:
            return ''
        return self.npk_info_list[0][0] + '/' + patch_path.NPK_INFO_FILE_NAME

    def set_npk_info_url(self, npk_info_list):
        self.npk_info_list = npk_info_list

    def set_patch_version(self, patch_version):
        self.patch_version = patch_version

    def set_download_fmap(self, fmap, size):
        self.patch_fmap = fmap
        self.patch_size = size

    def set_error(self, error):
        self.is_error = error

    def analyze_zip_map(self, new_map, cur_ver):
        try:
            self.patch_zip_info_dict = {}
            self.patch_zip_range_info_dict = {}
            self.zip_analyze_prog = 0.0
            if self._support_new_ui_astc_patch:
                patch_res_type = patch_utils.PATCH_RES_TYPE_HIGH
            else:
                patch_res_type = patch_utils.get_patch_res_type()
            patch_zip_pattern = patch_utils.get_patch_zip_pattern(self._support_new_ui_astc_patch)
            patch_range_pattern = patch_utils.get_patch_range_pattern(self._support_new_ui_astc_patch)
            for patch_info in self.patchlist:
                if patch_info.patch_type == patch_critical_info.PATCH_TYPE_FULL:
                    break
                if patch_info.target_version < int(cur_ver):
                    break
                if not (patch_info.high_res_zip_size > 0 and patch_info.low_res_zip_size > 0):
                    continue
                zip_size = patch_info.high_res_zip_size if patch_res_type == patch_utils.PATCH_RES_TYPE_HIGH else patch_info.low_res_zip_size
                zip_md5 = patch_info.high_res_zip_md5 if patch_res_type == patch_utils.PATCH_RES_TYPE_HIGH else patch_info.low_res_zip_md5
                zip_rw_path = patch_path.get_patch_zip_rw_path(patch_zip_pattern, patch_info.target_version)
                zip_orbit_path = patch_path.get_patch_zip_orbit_path(patch_zip_pattern, patch_info.target_version)
                zip_info = [
                 patch_info.target_version,
                 zip_size,
                 zip_md5,
                 zip_rw_path, zip_orbit_path, patch_utils.PATCH_ZIP_DOWNLOAD_STATE_INIT, 0, self.get_zip_src_url(patch_zip_pattern, patch_info.target_version, patch_info)]
                if os.path.exists(zip_rw_path):
                    zip_downloaded_size = os.path.getsize(zip_rw_path)
                    if zip_downloaded_size == zip_size:
                        if patch_utils.check_big_file_md5(zip_rw_path, zip_md5):
                            zip_info[5] = patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED
                if patch_utils.is_enable_patch_range():
                    if zip_info[5] != patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                        if patch_res_type == patch_utils.PATCH_RES_TYPE_HIGH:
                            zip_range_info_list = patch_info.high_res_zip_range_info if 1 else patch_info.low_res_zip_range_info
                            if zip_range_info_list:
                                zip_range_info_items = []
                                for idx, zip_range_info in enumerate(zip_range_info_list):
                                    zip_range_file_name = patch_path.get_patch_zip_range_rw_path(patch_range_pattern, int(patch_info.target_version), idx)
                                    zip_range_orbit_name = patch_path.get_patch_zip_range_orbit_path(patch_range_pattern, int(patch_info.target_version), idx)
                                    range_info = [
                                     patch_info.target_version, zip_range_file_name, zip_range_orbit_name]
                                    range_info.extend(zip_range_info)
                                    if patch_utils.check_is_file_downloaded_with_md5(zip_range_file_name, zip_range_info[2], zip_range_info[1] - zip_range_info[0]):
                                        download_state = patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED if 1 else patch_utils.PATCH_ZIP_DOWNLOAD_STATE_INIT
                                        range_info.append(download_state)
                                        range_info.append(self.get_zip_range_src_url(patch_zip_pattern, patch_info.target_version, patch_info, idx))
                                        zip_range_info_items.append(range_info)

                                self.patch_zip_range_info_dict[patch_info.target_version] = zip_range_info_items
                    self.patch_zip_info_dict[patch_info.target_version] = zip_info

            for fpath, f_info in six.iteritems(new_map):
                f_target_ver = self.get_patch_file_target_version(f_info)
                if f_target_ver in self.patch_zip_info_dict:
                    self.patch_zip_info_dict[f_target_ver][6] += 1

        except Exception as e:
            print('[Except] [patch] analyze_zip_map except:{}\n{}'.format(str(e), traceback.format_exc()))
            self.zip_analyze_prog = 1.0
            self.patch_zip_info_dict = {}

    def get_cnt_flist_info(self):
        try:
            saved_com_npk_lst = six.moves.builtins.__dict__.get('COM_NPK_NAMES', None)
            if saved_com_npk_lst:
                com_npk_dict = {npk_name:'' for npk_name in saved_com_npk_lst}
            else:
                com_npk_dict = deepcopy(self.npk_file_info)
            if hasattr(patch_utils, 'get_local_flist_info_v2'):
                ret, old_map = patch_utils.get_local_flist_info_v2(com_npk_dict)
            else:
                old_map = patch_utils.get_local_flist_info(com_npk_dict)
                ret = True
            return (ret, old_map)
        except Exception as e:
            error_str = '[Except] [patch] local flist read except:{}\n{}'.format(str(e), traceback.format_exc())
            print(error_str)
            self.err_queue.put(error_str)
            return (
             False, {})

        return

    def analyze_map(self, new_map, cur_ver):
        self._flist_error = False
        self.patch_fmap = None
        self.patch_size = 0
        self.patch_fpath_temp_path_map = None
        self.patch_temp_path_fpath_map = None
        self.patch_fpath_url_map = None
        self.analyze_prog = 0
        self._discrete_dl_num = 0
        self._zip_dl_num = 0
        ret_size = 0
        enable_local_flist = get_patch_const_bool('ENABLE_LOCAL_FLIST')
        if enable_local_flist and hasattr(patch_utils, 'get_base_npk_flist_dict'):
            base_npk_flist, ret = patch_utils.get_base_npk_flist_dict()
            old_map = base_npk_flist
        else:
            base_npk_flist = {}
            ret, old_map = self.get_cnt_flist_info()
        if not ret:
            self._flist_error = True
            return False
        else:
            ret_map = collections.OrderedDict()
            fpath_temp_path_map = collections.OrderedDict()
            temp_path_fpath_map = collections.OrderedDict()
            fpath_url_map = collections.OrderedDict()
            analyze_start_time = time.time()
            analyze_map_count = len(new_map)
            analyzed_count = 0
            enable_script_crc = patch_const.ENABLE_CHECK_SCRIPT_PKG_CRC
            enable_check_ext = patch_const.ENABLE_CHECK_EXT_NAME
            enable_patch_npk = patch_const.ENABLE_PATCH_NPK
            enable_check_week_and_patch = patch_const.ENABLE_CHECK_WEEK_AND_PATCH
            if enable_patch_npk:
                self._destroy_patch_npk_processor()
                from . import patch_npk
                self._patch_npk_processor = patch_npk.PatchNpkProcessor(self.err_queue)
                if not self._patch_npk_processor.init_npk_file_info():
                    return False
                self._patch_npk_processor.set_new_flist_map(new_map)
                if hasattr(self._patch_npk_processor, 'set_base_npk_flist_map'):
                    self._patch_npk_processor.set_base_npk_flist_map(base_npk_flist)
            if not hasattr(patch_utils, 'PATCHED_FILE_DICT'):
                setattr(patch_utils, 'PATCHED_FILE_DICT', {})
            for fpath, finfo in six.iteritems(new_map):
                analyzed_count += 1
                self.analyze_prog = analyzed_count * 1.0 / analyze_map_count
                if fpath == 'script/init.nxs':
                    continue
                old_finfo = old_map.get(fpath)
                is_script = fpath.endswith('.nxs')
                if not old_finfo or int(old_finfo[1]) != int(finfo[1]):
                    need_download = True
                elif is_script and enable_script_crc and int(old_finfo[2]) != 0 and int(old_finfo[2]) != int(finfo[2]):
                    need_download = True
                elif enable_check_ext and self.get_ext_name(old_finfo) != self.get_ext_name(finfo):
                    old_name = self.get_ext_name(old_finfo)
                    new_name = self.get_ext_name(finfo)
                    self.msg_queue.put('ext old:{}, ext new:{}, file:{}\n'.format(old_name, new_name, fpath))
                    need_download = True
                else:
                    need_download = False
                if IS_WIN and not self.patch_dctool.need_download_by_cur_channel(fpath):
                    need_download = False
                if need_download:
                    if enable_patch_npk:
                        if self._patch_npk_processor.is_file_in_patch_npk(fpath, int(finfo[2]), is_script):
                            self.msg_queue.put('no need dl 1: ' + fpath + '\n')
                            need_download = False
                    elif enable_check_week_and_patch:
                        if patch_utils.check_res_in_week_or_patch(fpath, int(finfo[2])):
                            self.msg_queue.put('no need dl 2: ' + fpath + '\n')
                            need_download = False
                if need_download:
                    patch_utils.PATCHED_FILE_DICT[fpath] = finfo
                    temp_path = patch_path.get_patch_file_rw_temp_path(fpath)
                    orbit_temp_path = patch_path.get_patch_file_orbit_temp_path(fpath)
                    if not (os.path.exists(temp_path) and patch_utils.check_file_crc32(temp_path, int(finfo[2]), self.err_queue)):
                        if os.path.exists(temp_path) and os.path.getsize(temp_path) == int(finfo[3]):
                            os.remove(temp_path)
                        ret_size += int(finfo[3])
                        patch_utils.check_physxcook(fpath)
                        self.msg_queue.put('need download: ' + fpath + '\n')
                    else:
                        self.msg_queue.put('need download:{} and has downloaded\n'.format(fpath))
                        finfo[3] = -1
                    ret_map[fpath] = finfo
                    download_url = self.get_file_src_url(finfo)
                    fpath_url_map[fpath] = download_url
                    fpath_temp_path_map[fpath] = (temp_path, orbit_temp_path)
                    temp_path_fpath_map[temp_path] = fpath
                    if not download_url:
                        self.patch_dctool.on_patch_check_failed(self.get_flist_url(), 'get file download url fail @ file %s' % fpath)
                        return False

            file_num = len(ret_map) if ret_map else 0
            cnt_time = time.time()
            self.patch_fmap = ret_map
            self.patch_size = ret_size
            self.patch_fpath_temp_path_map = fpath_temp_path_map
            self.patch_temp_path_fpath_map = temp_path_fpath_map
            self.patch_fpath_url_map = fpath_url_map
            self.patch_dctool.on_patch_check_ok(self.get_flist_url(), ret_size / 1024.0, file_num, (cnt_time - analyze_start_time) * 1000)
            return True

    def patchlist_analyze(self, ret):
        lines = ret.splitlines()
        for idx, line in enumerate(lines):
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            line = line.strip()
            lines[idx] = line

        name_dict = {game3d.PLATFORM_ANDROID: 'android',game3d.PLATFORM_IOS: 'ios',
           'default': 'win32'
           }
        try:
            is_android_dds_package = patch_utils.is_android_dds_package()
        except Exception as e:
            print('[Except] [patch_ui] get android dds flag except:{}'.format(str(e)))
            is_android_dds_package = False

        if is_android_dds_package:
            name = 'simulator'
        else:
            name = name_dict.get(game3d.get_platform(), 'win32')
        redirect_url = patch_utils.analyze_redirect_url(self, lines, name)
        if redirect_url:
            self.patch_list_redirect_url = redirect_url
            self.put_check_patch_ret_cb(2)
            return
        patch_utils.analyze_remote_code(self, lines, name)
        cur_ver = self.get_cur_ver()
        if cur_ver == 0:
            print('[patch]: no need to update patch, because cur version is zero')
            self.put_check_patch_ret_cb(0)
            return
        patch_utils.check_package_type(name, lines, cur_ver)
        if patch_utils.check_ignore_patch(name, lines, cur_ver):
            self.msg_queue.put('[patch] ignore patch')
            self.put_check_patch_ret_cb(0)
            return
        max_patch_version = patch_utils.check_max_patch(name, lines)
        ignore_week_patch_mechanism = False
        try:
            ignore_week_patch_mechanism = patch_utils.check_ignore_week_patch_mechanism(lines)
        except Exception as e:
            print('[Except] [patch_ui] check ignore week patch mechanism except:{}'.format(str(e)))
            ignore_week_patch_mechanism = False

        target_patchlist, analyze_res = patch_utils.analyze_patchlist(name, lines)
        is_new_package = package_utils.check_new_package()
        if max_patch_version > 0:
            target_patchlist = patch_utils.filter_target_patchlist_by_max_patch_version(target_patchlist, max_patch_version)
        if not analyze_res:
            self.err_queue.put('analyze patch list error @ url %s' % self.get_patch_list_url())
            process_info = {'PATCH_LIST_NOT_VALID': 'patchlist not valid',
               'url': self.get_patch_list_url()
               }
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_PATCH_LIST_ANALYZE})
            return
        if not target_patchlist:
            process_info = {'TARGET_PATCH_LIST_IS_EMPTY': 'target_patchlist is empty'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            print('[patch] target list is empty')
            self.put_check_patch_ret_cb(0)
            return
        self.real_weekly_info = target_patchlist[0].branch_info
        if max_patch_version <= 0 and not is_new_package and not ignore_week_patch_mechanism:
            target_patchlist = patch_utils.filter_target_patchlsit_by_version(target_patchlist, cur_ver)
        self.real_last_week_version = self.get_last_branch_version(target_patchlist)
        target_version = target_patchlist[0].target_version
        self.set_patchlist(target_patchlist)
        if target_version != 0 and cur_ver >= target_version:
            if not hasattr(patch_utils, 'need_tidy_patch_npk'):
                need_tidy = True if 1 else patch_utils.need_tidy_patch_npk()
                need_tidy or print('[patch]: no need to update patch for version')
                self.put_check_patch_ret_cb(0)
                return
            print('[patch] need tidy patch npk')
        try:
            patch_utils.drpf_check_update(patch_dctool.PATCH_UPDATE_PHASE_ENTER)
        except Exception as e:
            print('[Except] [patch_ui] drpf_check_update error:{}'.format(str(e)))

        try:
            if cur_ver <= self.real_last_week_version:
                if get_patch_const_bool('ENABLE_PATCH_ANNOUNCE'):
                    from .patch_announce import get_patch_announce_instance
                    game3d.frame_delay_exec(2, get_patch_announce_instance)
        except Exception as e:
            print('[Except] [patch_ui] get patch announcement except:{}'.format(str(e)))

        self.new_weekly_info = target_patchlist[0].branch_info
        self.set_patch_version(target_version)
        self.download_filelist(target_patchlist[0].url, target_version)

    def download_patchlist(self, callback):
        self._flist_error = False
        self.patch_error_list = []
        self.downloader_agent.set_space_flag(False)
        self.state = patch_utils.DST_PLIST
        self.weekly_info = patch_utils.get_cnt_weekly_info()
        self.new_weekly_info = ''
        file_name = patch_path.PATCH_LIST_NAME
        relative_file_path = os.path.join(patch_path.TEMP_DIRNAME, file_name)
        orbit_path = patch_path.get_orbit_download_path(relative_file_path)
        if os.path.exists(orbit_path):
            try:
                os.remove(orbit_path)
            except Exception as e:
                print('[Error]:remove patchlist.txt failed! e:', str(e))

        rw_path = patch_path.get_rw_path(relative_file_path)
        patch_list_url = self.get_patch_list_url()
        self.patch_check_callback = callback
        download_list = [(orbit_path, rw_path, patch_list_url, 0)]
        if not self.downloader_agent.start_download(download_list, self.on_download_patch_list_callback, 0):
            self.put_check_patch_ret_cb(-1)

    def on_download_patch_list_callback(self, success_list, error_list, consume_time):
        if error_list:
            url = error_list[0][2]
            self.patch_dctool.on_download_patch_list_failed(url, '[PATCH]patch list failed')
            process_info = {'DL_PATCH_LIST_ERROR': 'download patch list failed'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_PATCH_LIST_DOWNLOAD})
        else:
            file_path = success_list[0][1]
            if not os.path.exists(file_path):
                process_info = {'DL_PATCH_LIST_SUCCESS_FILE_NOT_EXISTS': 'has download patch list but path not exist'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_PATCH_LIST_DOWNLOADED_AND_NOT_EXISTS})
            else:
                url = success_list[0][2]
                with open(file_path, 'r') as tmp_file:
                    patchlist_data = tmp_file.read()
                avrg_spd_str = patch_utils.get_avg_spd_str(consume_time * 1000, len(patchlist_data))
                self.patch_dctool.on_download_patch_list_ok(url, avrg_spd_str, consume_time)
                process_info = {'DL_PATCH_LIST_DONE': 'begin patch list analyze'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.patchlist_analyze(patchlist_data)

    def filelist_analyze(self, data):
        self.set_state(patch_utils.DST_FLIST_CHECK)
        process_info = {'BEGIN_ANALYZE_FILELIST': 'begin analyze file list'}
        self.patch_dctool.send_patch_process_info_info(process_info)

        def callback_thread_func(downloader, data):
            try:
                downloader.flist_data = data
                data = zlib.decompress(six.ensure_binary(data))
                data = six.ensure_str(data)
                fmap = patch_utils.read_filelist(data)
                if self._support_new_ui_astc_patch:
                    fmap = patch_utils.filter_base_package_resource(fmap)
                else:
                    fmap = patch_utils.filter_android_resource(fmap)
                if patch_const.ENABLE_ZIP_DOWNLOAD:
                    downloader.analyze_zip_map(fmap, downloader.get_cur_ver())
                analyze_res = downloader.analyze_map(fmap, downloader.get_cur_ver())
                if patch_const.ENABLE_ZIP_DOWNLOAD:
                    downloader.zip_patch_download_list = downloader.generate_zip_patch_download_list()
                    for item in downloader.zip_patch_download_list:
                        self.msg_queue.put(str(item))

                if not analyze_res:
                    self.put_check_patch_ret_cb(-1)
                else:
                    new_map = self.get_patch_fmap()
                    if new_map:
                        self.msg_queue.put('need download patch')
                        self.put_check_patch_ret_cb(1)
                    else:
                        if self._patch_npk_processor:
                            ret = self._patch_npk_flush_and_verify()
                            if not ret:
                                print('[patch_npk] flush and verify failed when analyze flist')
                                self.put_check_patch_ret_cb(-1)
                                return
                            from . import patch_npk_before
                            ret = patch_npk_before.insert_patch_npk_before_patch()
                            if not ret:
                                self.put_check_patch_ret_cb(-1)
                                return
                            patch_utils.save_local_flist(downloader.flist_data, self.err_queue)
                        print('[patch] no need to update patch for flist')
                        self.put_check_patch_ret_cb(0)
            except Exception as e:
                error_str = '[Except] [patch] filelist_analyze except:{}\n{}'.format(str(e), traceback.format_exc())
                print(error_str)
                upload_info = {'ANALYZE_FILELIST_EXCEPT': error_str}
                self.patch_dctool.send_patch_process_info_info(upload_info)
                patch_utils.force_error_next_frame()

        t = threading.Thread(target=callback_thread_func, args=(self, data))
        t.setDaemon(True)
        t.start()

    def get_prev_branch_version(self):
        for patchlist_item in self.patchlist:
            branch_info = patchlist_item.branch_info
            if branch_info and self.new_weekly_info != branch_info:
                return patchlist_item.target_version

        return 0

    def get_last_branch_version(self, patchlist):
        if not patchlist:
            return 0
        weekly_info = patchlist[0].branch_info
        if not weekly_info:
            return 0
        for patchlist_item in patchlist:
            branch_info = patchlist_item.branch_info
            if branch_info and weekly_info != branch_info:
                return patchlist_item.target_version

        return 0

    def try_analyze_patch_config(self):
        try:
            file_version = self.patchlist[0].target_version
            temp_patch_config_data = patch_utils.get_temp_patch_config_data(file_version, self.patch_config_finfo)
            if temp_patch_config_data:
                if not patch_utils.check_data_crc32(temp_patch_config_data, int(self.patch_config_finfo[2])):
                    print('[ERROR] patch config check crc failed:{} {}'.format(file_version, int(self.patch_config_finfo[2])))
                    self.filelist_analyze(self.config_flist_data)
                else:
                    self.do_analyze_patch_config(temp_patch_config_data)
                return
            self.do_download_patch_config(file_version, self.patch_config_finfo)
        except Exception as e:
            error_str = '[Except] [patch] analyze_patch_config except:{}\n{}'.format(str(e), traceback.format_exc())
            print(error_str)
            flist_data = self.config_flist_data
            self.config_flist_data = None
            self.patch_config_finfo = None
            patch_utils.send_script_error(error_str)
            self.filelist_analyze(flist_data)

        return

    def analyze_patch_zip_info(self, patch_config_data):
        zip_key = patch_utils.get_patch_zip_config_key(self._support_new_ui_astc_patch)
        range_key = patch_utils.get_patch_range_config_key(self._support_new_ui_astc_patch)
        patch_zip_info = patch_config_data.get(zip_key, {})
        patch_zip_range_info = patch_config_data.get(range_key, {})
        for patchlist_info in self.patchlist:
            version_str = str(patchlist_info.target_version)
            if version_str in patch_zip_info:
                cnt_zip_info = patch_zip_info[version_str]
                zip_size, zip_md5, low_zip_size, low_zip_md5 = (int(cnt_zip_info[0]), cnt_zip_info[1], int(cnt_zip_info[2]), cnt_zip_info[3])
                patchlist_info.high_res_zip_size = zip_size
                patchlist_info.high_res_zip_md5 = zip_md5
                patchlist_info.low_res_zip_size = low_zip_size
                patchlist_info.low_res_zip_md5 = low_zip_md5
            if patch_utils.is_enable_patch_range():
                if version_str in patch_zip_range_info:
                    cnt_range_info = patch_zip_range_info[version_str]
                    patchlist_info.high_res_zip_range_info = cnt_range_info.get('high_res', None)
                    patchlist_info.low_res_zip_range_info = cnt_range_info.get('compatible', None)

        return

    def do_analyze_patch_config(self, patch_config_data):
        try:
            process_info = {'BEGIN_PATCH_CONFIG_ANALYZE': 'begin analyze patch config'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            data = zlib.decompress(six.ensure_binary(patch_config_data))
            data_dict = json.loads(data)
            self.analyze_patch_zip_info(data_dict)
            self.filelist_analyze(self.config_flist_data)
        except Exception as e:
            print('[Except] [patch] analyze_patch_config except:{}'.format(str(e)))
            self.patch_config_finfo = None
            self.filelist_analyze(self.config_flist_data)

        return

    def analyze_patch_config_from_filelist(self, in_filelist_data):

        def thread_analyze_func(filelist_data):
            try:
                data = zlib.decompress(six.ensure_binary(filelist_data))
                fmap = patch_utils.read_filelist(data)
                if patch_path.PATCH_CONFIG_FILE_NAME in fmap:
                    self.patch_config_finfo = fmap[patch_path.PATCH_CONFIG_FILE_NAME]
                    del fmap[patch_path.PATCH_CONFIG_FILE_NAME]
                    new_flist_str = []
                    for k, v in six.iteritems(fmap):
                        new_flist_str.append('\t'.join(v))

                    tmp_file = '\n'.join(new_flist_str)
                    self.config_flist_data = zlib.compress(six.ensure_binary(tmp_file))
                    self.retqueue.put((self.try_analyze_patch_config, ()))
                else:
                    self.retqueue.put((self.filelist_analyze, (filelist_data,)))
            except Exception as e:
                error_str = '[Except] [patch] analyze patch config except:{}\n{}'.format(str(e), traceback.format_exc())
                print(error_str)
                self.config_flist_data = None
                self.patch_config_finfo = None
                patch_utils.send_script_error(error_str)
                process_info = {'PATCH_CONFIG_ANALYZE_EXCEPT': error_str}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.retqueue.put((self.filelist_analyze, (filelist_data,)))

            return

        t = threading.Thread(target=thread_analyze_func, args=(in_filelist_data,))
        t.setDaemon(True)
        t.start()

    def on_download_filelist_callback(self, success_list, error_list, consume_time):
        if error_list:
            url = error_list[0][2]
            print('[downloader] dl filelist failed')
            process_info = {'DL_FILE_LIST_FAILED': 'downloader download file list failed'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.patch_dctool.on_download_patch_list_failed(url, '[PATCH]file list failed')
            self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_FILE_LIST_DOWNLOAD})
        else:
            file_path = success_list[0][1]
            if not os.path.exists(file_path):
                process_info = {'DL_FILE_LIST_SUCCESS_FILE_NOT_EXISTS': 'has download file list but not exist'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_FILE_LIST_DOWNLOADED_AND_NOT_EXISTS})
            else:
                url = success_list[0][2]
                with open(file_path, 'rb') as tmp_file:
                    filelist_data = tmp_file.read()
                avrg_spd_str = patch_utils.get_avg_spd_str(consume_time * 1000, len(filelist_data))
                self.patch_dctool.on_download_patch_list_ok(url, avrg_spd_str, consume_time)
                process_info = {'DL_FILE_LIST_DONE': 'download file list success, begin analyze patch config'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.analyze_patch_config_from_filelist(filelist_data)

    def on_download_patch_config_callback(self, success_list, error_list, consume_time):
        if error_list:
            url = error_list[0][2]
            self.patch_dctool.on_download_patch_list_failed(url, '[PATCH]file config data')
            process_info = {'DL_PATCH_CONFIG_FAILED': 'download patch config failed'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.put_check_patch_ret_cb(-1, {'error_code': patch_utils.PATCH_ERROR_PATCH_CONFIG_DOWNLOAD})
        else:
            self.try_analyze_patch_config()

    def do_download_patch_config(self, version, finfo):
        try:
            config_url = self.get_patch_config_url()
            config_rw_path = patch_path.get_patch_config_rw_path(version)
            config_orbit_path = patch_path.get_patch_config_orbit_path(version)
            file_size = int(finfo[3])
            download_list = [(config_orbit_path, config_rw_path, config_url, file_size)]
            if not self.downloader_agent.start_download(download_list, self.on_download_patch_config_callback, file_size):
                self.put_check_patch_ret_cb(-1)
        except Exception as e:
            error_str = '[Except] [patch] dl patch config except:{}\n{}'.format(str(e), traceback.format_exc())
            print(error_str)
            flist_data = self.config_flist_data
            self.config_flist_data = None
            self.patch_config_finfo = None
            patch_utils.send_script_error(error_str)
            self.filelist_analyze(flist_data)

        return

    def download_filelist(self, url, version):
        self.state = patch_utils.DST_FLIST
        try:
            data = patch_utils.get_temp_flist_data(version, self.get_flist_md5())
            if not data:
                flist_url = self.get_flist_url(url)
                flist_rw_path = patch_path.get_temp_flst_rw_path(int(version))
                flist_orbit_path = patch_path.get_temp_flst_orbit_path(int(version))
                dl_list = [(flist_orbit_path, flist_rw_path, flist_url, 0)]
                if not self.downloader_agent.start_download(dl_list, self.on_download_filelist_callback, 0):
                    self.put_check_patch_ret_cb(-1)
                    return
                process_info = {'DL_FILE_LIST': 'begin dl file list'}
                self.patch_dctool.send_patch_process_info_info(process_info)
            else:
                self.retqueue.put((self.analyze_patch_config_from_filelist, (data,)))
        except Exception as e:
            process_info = {'DL_FILE_LIST_EXCEPT': 'except:{}'.format(str(e) + traceback.format_exc())}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.err_queue.put(str(e) + traceback.format_exc())
            self.put_check_patch_ret_cb(-1, process_info)

    def get_npk_src_url(self, npk_name):
        for url, version in self.npk_info_list:
            if version == self._npk_svn_version:
                return url + '/' + npk_name

        return ''

    def get_file_src_url(self, finfo):
        url = None
        f_target_ver = self.get_patch_file_target_version(finfo)
        for patchlist_item in self.patchlist:
            if patchlist_item.start_version < f_target_ver <= patchlist_item.target_version:
                if IS_PY3:
                    server_location = patch_path.get_patch_server_location(finfo[0])
                else:
                    server_location = patch_path.convert_to_hashed_file_path(finfo[0])
                url = patchlist_item.url + '/' + six.moves.urllib.parse.quote(server_location)
                break

        return url

    def get_patch_config_url(self):
        patchlist_item = self.patchlist[0]
        if IS_PY3:
            server_location = patch_path.get_patch_server_location(patch_path.PATCH_CONFIG_FILE_NAME)
        else:
            server_location = patch_path.convert_to_hashed_file_path(patch_path.PATCH_CONFIG_FILE_NAME)
        return patchlist_item.url + '/' + server_location

    def get_zip_src_url(self, patch_zip_pattern, patch_version, patch_info):
        url = patch_info.url + '/' + six.moves.urllib.parse.quote(patch_zip_pattern % patch_version)
        return url

    def get_zip_range_src_url(self, patch_zip_pattern, patch_version, patch_info, index):
        return self.get_zip_src_url(patch_zip_pattern, patch_version, patch_info) + str(index)

    def get_target_fmap_version_info(self):
        dist_map = {}
        for key, v in six.iteritems(self.patch_fmap):
            f_target_ver = self.get_patch_file_target_version(v)
            dist_map[patch_path.get_abs_download_target_path(key)] = f_target_ver

        return dist_map

    def generate_zip_patch_download_list(self):
        self._discrete_dl_num = 0
        self._zip_dl_num = 0
        download_list = []
        need_download_zip_dict = {}
        zipable_file_dict = {}
        if not self.patch_fpath_temp_path_map:
            return download_list
        for k, v in six.iteritems(self.patch_fpath_temp_path_map):
            finfo = self.patch_fmap[k]
            download_size = int(finfo[3])
            downloaded = download_size == -1
            if not downloaded:
                rw_path, orbit_path = v
                url = self.patch_fpath_url_map[k]
                download_list.append((orbit_path, rw_path, url, download_size))
                patch_file_version = self.get_patch_file_target_version(finfo)
                if patch_file_version in self.patch_zip_info_dict and (not IS_WIN or not patch_path.is_bin_patch(k)):
                    if patch_file_version not in need_download_zip_dict:
                        need_download_zip_dict[patch_file_version] = [0, 0]
                    need_download_zip_dict[patch_file_version][0] += download_size
                    need_download_zip_dict[patch_file_version][1] += 1
                    zipable_file_dict[orbit_path] = patch_file_version

        zip_keys = six_ex.keys(need_download_zip_dict)
        for key in zip_keys:
            patch_zip_info = self.patch_zip_info_dict[key]
            need_download_zip_info = need_download_zip_dict[key]
            if patch_zip_info[5] == patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                continue
            zip_size = max(patch_zip_info[1], 1)
            size_download_ratio = need_download_zip_info[0] * 1.0 / zip_size
            if size_download_ratio < 0.5:
                if key in self.patch_zip_info_dict:
                    del self.patch_zip_info_dict[key]

        zip_info_keys = six_ex.keys(self.patch_zip_info_dict)
        for key in zip_info_keys:
            if key not in need_download_zip_dict:
                del self.patch_zip_info_dict[key]
                if key in self.patch_zip_range_info_dict:
                    del self.patch_zip_range_info_dict[key]

        self.zip_patch_download_size = 0
        ret_list = []
        if self.patch_zip_info_dict:
            for k, v in six.iteritems(self.patch_zip_info_dict):
                if v[5] == patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                    continue
                if patch_utils.is_enable_patch_range() and k in self.patch_zip_range_info_dict:
                    zip_range_info_list = self.patch_zip_range_info_dict[k]
                    for idx, range_info in enumerate(zip_range_info_list):
                        if range_info[6] == patch_utils.PATCH_ZIP_DOWNLOAD_STATE_DOWNLOAED:
                            continue
                        start_index = range_info[3]
                        end_index = range_info[4]
                        range_size = end_index - start_index
                        range_download_info = (range_info[2], range_info[1], range_info[7], range_size)
                        ret_list.append(range_download_info)
                        self.zip_patch_download_size += range_size

                else:
                    ret_list.append((v[4], v[3], v[7], v[1], v[2]))
                    self.zip_patch_download_size += v[1]
                    self._zip_dl_num += 1

        for item in download_list:
            orbit_path = item[0]
            if orbit_path in zipable_file_dict:
                zip_version = zipable_file_dict[orbit_path]
                if zip_version in self.patch_zip_info_dict:
                    continue
            self.zip_patch_download_size += item[3]
            ret_list.append(item)
            self._discrete_dl_num += 1

        download_list = ret_list
        return download_list

    def generate_patch_download_list(self):
        download_list = []
        if not self.patch_fpath_temp_path_map:
            return download_list
        count = 0
        for k, v in six.iteritems(self.patch_fpath_temp_path_map):
            finfo = self.patch_fmap[k]
            download_size = int(finfo[3])
            downloaded = download_size == -1
            if not downloaded:
                rw_path, orbit_path = v
                url = self.patch_fpath_url_map[k]
                count += 1
                if count <= 300 and not game3d.is_release_version():
                    print(' [patch] try to download patch file', k, rw_path, orbit_path, url)
                download_list.append((orbit_path, rw_path, url, download_size))

        return download_list

    def on_download_patch_files_callback(self, success_list, error_list, consume_time):
        if error_list:
            process_info = {'DL_PATCH_FILES_FAILED': 'downloader download patch failed'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.patch_error_list = error_list
            self.put_download_patch_files_ret_cb(False)
        else:
            process_info = {'DL_PATCH_FILES_SUCCESS': 'download patch success, begin analyze patch files'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            time_cost = consume_time * 1000
            patch_size = self.get_patch_size()
            spd_str = patch_utils.get_avg_spd_str(time_cost, patch_size)
            self.patch_dctool.on_download_patch_ok(self.patchlist[0].url, spd_str, time_cost, self.patch_download_id_str, len(success_list), self.get_patch_version(), patch_size)
            self.patch_files_analyze()

    def patch_files_analyze(self):
        t = threading.Thread(target=self.patch_files_analyze_thread_func)
        t.setDaemon(True)
        t.start()

    def validate_patch_zip_file(self, verify_info):
        zip_path = verify_info[3]
        zip_size = verify_info[1]
        zip_md5 = verify_info[2]
        return os.path.exists(zip_path) and os.path.getsize(zip_path) == zip_size and patch_utils.check_big_file_md5(zip_path, zip_md5)

    def _get_zip_file_with_version(self, in_zip_vesion):
        import zipfile
        ret_zipf = None
        zip_info = self.patch_zip_info_dict[in_zip_vesion]
        zip_path = zip_info[3]
        assmeble_finish = False
        if patch_utils.is_enable_patch_range():
            if in_zip_vesion in self.patch_zip_range_info_dict and not self.validate_patch_zip_file(zip_info):
                assemble_res, error_str = patch_utils.assemble_ranged_zip_file(self.patch_zip_range_info_dict[in_zip_vesion], zip_path)
                if assemble_res & patch_utils.PATCH_RANGE_FILE_CHECK_STATUS_RUN_OUT_SPACE != 0:
                    self.downloader_agent.set_space_flag(True)
                if assemble_res != patch_utils.PATCH_RANGE_FILE_CHECK_STATUS_FINISHED:
                    self.err_queue.put(error_str)
                else:
                    assmeble_finish = True
        if not os.path.exists(zip_path):
            if self.err_queue:
                self.err_queue.put('[PATCH] get zip file info error [error] zip path not exist %s' % str(zip_path))
            if assmeble_finish:
                patch_utils.increase_range_error_count()
            return (False, ret_zipf)
        else:
            if not os.path.getsize(zip_path) == zip_info[1]:
                if self.err_queue:
                    self.err_queue.put('[PATCH] get zip file info error error] size not match %s %s' % (
                     str(os.path.getsize(zip_path)), str(zip_info[1])))
                if assmeble_finish:
                    patch_utils.increase_range_error_count()
                return (False, ret_zipf)
            if not patch_utils.check_big_file_md5(zip_path, zip_info[2]):
                if self.err_queue:
                    self.err_queue.put('[PATCH] get zip file info error error] md5 not match %s %s' % (
                     str(zip_path), str(zip_info[2])))
                if assmeble_finish:
                    patch_utils.increase_range_error_count()
                return (False, ret_zipf)
            try:
                ret_zipf = zipfile.ZipFile(zip_path)
            except Exception as e:
                if self.err_queue:
                    self.err_queue.put('[PATCH] get zip file info error error] error %s' % str(e))
                if assmeble_finish:
                    patch_utils.increase_range_error_count()
                return (False, ret_zipf)

            return (True, ret_zipf)

    def patch_files_analyze_thread_func--- This code section failed: ---

1187       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'set_state'
           6  LOAD_GLOBAL           1  'patch_utils'
           9  LOAD_ATTR             2  'DST_COPY'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

1188      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             3  'get_patch_fmap'
          22  CALL_FUNCTION_0       0 
          25  STORE_FAST            1  'patch_fmap'

1189      28  LOAD_GLOBAL           4  'len'
          31  LOAD_FAST             1  'patch_fmap'
          34  CALL_FUNCTION_1       1 
          37  STORE_FAST            2  'analyze_map_count'

1190      40  LOAD_CONST            1  ''
          43  LOAD_FAST             0  'self'
          46  STORE_ATTR            5  'analyze_prog'

1191      49  LOAD_GLOBAL           6  'time'
          52  LOAD_ATTR             6  'time'
          55  CALL_FUNCTION_0       0 
          58  LOAD_FAST             0  'self'
          61  STORE_ATTR            7  'check_time'

1195      64  STORE_ATTR            2  'DST_COPY'
          67  MAKE_FUNCTION_1       1 
          70  STORE_FAST            3  'update_progress'

1197      73  LOAD_GLOBAL           1  'patch_utils'
          76  LOAD_ATTR             8  'analyze_weekly_info'
          79  LOAD_FAST             0  'self'
          82  LOAD_ATTR             9  'weekly_info'
          85  LOAD_FAST             0  'self'
          88  LOAD_ATTR            10  'new_weekly_info'
          91  LOAD_FAST             3  'update_progress'
          94  CALL_FUNCTION_3       3 
          97  STORE_FAST            4  'weekly_info_res'

1198     100  LOAD_CONST            1  ''
         103  LOAD_FAST             0  'self'
         106  STORE_ATTR            5  'analyze_prog'

1199     109  LOAD_FAST             4  'weekly_info_res'
         112  POP_JUMP_IF_TRUE    132  'to 132'

1200     115  LOAD_FAST             0  'self'
         118  LOAD_ATTR            11  'put_download_patch_files_ret_cb'
         121  LOAD_GLOBAL          12  'False'
         124  CALL_FUNCTION_1       1 
         127  POP_TOP          

1201     128  LOAD_CONST            0  ''
         131  RETURN_END_IF    
       132_0  COME_FROM                '112'

1202     132  LOAD_FAST             0  'self'
         135  LOAD_ATTR             9  'weekly_info'
         138  LOAD_FAST             0  'self'
         141  LOAD_ATTR            10  'new_weekly_info'
         144  COMPARE_OP            3  '!='
         147  POP_JUMP_IF_FALSE   169  'to 169'

1203     150  LOAD_GLOBAL           1  'patch_utils'
         153  LOAD_ATTR            13  'save_cnt_weekly_info'
         156  LOAD_FAST             0  'self'
         159  LOAD_ATTR            10  'new_weekly_info'
         162  CALL_FUNCTION_1       1 
         165  POP_TOP          
         166  JUMP_FORWARD          0  'to 169'
       169_0  COME_FROM                '166'

1205     169  LOAD_CONST            3  'res/confs/version.json'
         172  STORE_FAST            5  'version_file_path'

1207     175  LOAD_FAST             5  'version_file_path'
         178  LOAD_FAST             1  'patch_fmap'
         181  COMPARE_OP            6  'in'
         184  POP_JUMP_IF_FALSE   215  'to 215'

1208     187  LOAD_FAST             1  'patch_fmap'
         190  LOAD_FAST             5  'version_file_path'
         193  BINARY_SUBSCR    
         194  STORE_FAST            6  'version_file_info'

1209     197  LOAD_FAST             0  'self'
         200  LOAD_ATTR            14  'get_patch_file_target_version'
         203  LOAD_FAST             6  'version_file_info'
         206  CALL_FUNCTION_1       1 
         209  STORE_FAST            7  'version_file_version'
         212  JUMP_FORWARD         12  'to 227'

1211     215  LOAD_CONST            0  ''
         218  STORE_FAST            6  'version_file_info'

1212     221  LOAD_CONST            4  -1
         224  STORE_FAST            7  'version_file_version'
       227_0  COME_FROM                '212'

1213     227  BUILD_LIST_0          0 
         230  STORE_FAST            8  'version_file_lst'

1214     233  BUILD_MAP_0           0 
         236  STORE_FAST            9  'versioned_info_dict'

1215     239  SETUP_LOOP          127  'to 369'
         242  LOAD_FAST             1  'patch_fmap'
         245  GET_ITER         
         246  FOR_ITER            119  'to 368'
         249  STORE_FAST           10  'f_path'

1216     252  LOAD_FAST            10  'f_path'
         255  LOAD_FAST             5  'version_file_path'
         258  COMPARE_OP            2  '=='
         261  POP_JUMP_IF_FALSE   270  'to 270'

1217     264  CONTINUE            246  'to 246'
         267  JUMP_FORWARD          0  'to 270'
       270_0  COME_FROM                '267'

1218     270  LOAD_FAST             1  'patch_fmap'
         273  LOAD_FAST            10  'f_path'
         276  BINARY_SUBSCR    
         277  STORE_FAST           11  'f_info'

1219     280  LOAD_FAST             0  'self'
         283  LOAD_ATTR            14  'get_patch_file_target_version'
         286  LOAD_FAST            11  'f_info'
         289  CALL_FUNCTION_1       1 
         292  STORE_FAST           12  'target_v'

1220     295  LOAD_FAST            12  'target_v'
         298  LOAD_FAST             7  'version_file_version'
         301  COMPARE_OP            2  '=='
         304  POP_JUMP_IF_FALSE   323  'to 323'

1221     307  LOAD_FAST             8  'version_file_lst'
         310  LOAD_ATTR            16  'append'
         313  LOAD_FAST            11  'f_info'
         316  CALL_FUNCTION_1       1 
         319  POP_TOP          
         320  JUMP_BACK           246  'to 246'

1223     323  LOAD_FAST            12  'target_v'
         326  LOAD_FAST             9  'versioned_info_dict'
         329  COMPARE_OP            7  'not-in'
         332  POP_JUMP_IF_FALSE   348  'to 348'

1224     335  BUILD_LIST_0          0 
         338  LOAD_FAST             9  'versioned_info_dict'
         341  LOAD_FAST            12  'target_v'
         344  STORE_SUBSCR     
         345  JUMP_FORWARD          0  'to 348'
       348_0  COME_FROM                '345'

1225     348  LOAD_FAST             9  'versioned_info_dict'
         351  LOAD_FAST            12  'target_v'
         354  BINARY_SUBSCR    
         355  LOAD_ATTR            16  'append'
         358  LOAD_FAST            11  'f_info'
         361  CALL_FUNCTION_1       1 
         364  POP_TOP          
         365  JUMP_BACK           246  'to 246'
         368  POP_BLOCK        
       369_0  COME_FROM                '239'

1226     369  LOAD_FAST             6  'version_file_info'
         372  POP_JUMP_IF_FALSE   391  'to 391'

1227     375  LOAD_FAST             8  'version_file_lst'
         378  LOAD_ATTR            16  'append'
         381  LOAD_FAST             6  'version_file_info'
         384  CALL_FUNCTION_1       1 
         387  POP_TOP          
         388  JUMP_FORWARD          0  'to 391'
       391_0  COME_FROM                '388'

1229     391  LOAD_CONST            1  ''
         394  STORE_FAST           13  'finished_count'

1231     397  SETUP_LOOP           93  'to 493'
         400  LOAD_FAST             9  'versioned_info_dict'
         403  GET_ITER         
         404  FOR_ITER             85  'to 492'
         407  STORE_FAST           12  'target_v'

1232     410  LOAD_FAST             9  'versioned_info_dict'
         413  LOAD_FAST            12  'target_v'
         416  BINARY_SUBSCR    
         417  STORE_FAST           14  'finfo_lst'

1233     420  LOAD_FAST             0  'self'
         423  LOAD_ATTR            17  '_write_patch_file'
         426  LOAD_FAST            12  'target_v'
         429  LOAD_FAST            14  'finfo_lst'
         432  LOAD_FAST            13  'finished_count'
         435  LOAD_FAST             2  'analyze_map_count'
         438  CALL_FUNCTION_4       4 
         441  UNPACK_SEQUENCE_2     2 
         444  STORE_FAST           15  'ret'
         447  STORE_FAST           16  'up_info'

1234     450  LOAD_FAST            15  'ret'
         453  POP_JUMP_IF_TRUE    473  'to 473'

1235     456  LOAD_FAST             0  'self'
         459  LOAD_ATTR            18  '_analyze_patch_file_failed'
         462  LOAD_FAST            16  'up_info'
         465  CALL_FUNCTION_1       1 
         468  POP_TOP          

1236     469  LOAD_CONST            0  ''
         472  RETURN_END_IF    
       473_0  COME_FROM                '453'

1238     473  LOAD_FAST            13  'finished_count'
         476  LOAD_GLOBAL           4  'len'
         479  LOAD_FAST            14  'finfo_lst'
         482  CALL_FUNCTION_1       1 
         485  INPLACE_ADD      
         486  STORE_FAST           13  'finished_count'
         489  JUMP_BACK           404  'to 404'
         492  POP_BLOCK        
       493_0  COME_FROM                '397'

1240     493  LOAD_FAST             7  'version_file_version'
         496  LOAD_CONST            1  ''
         499  COMPARE_OP            4  '>'
         502  POP_JUMP_IF_FALSE   561  'to 561'

1241     505  LOAD_FAST             0  'self'
         508  LOAD_ATTR            17  '_write_patch_file'
         511  LOAD_FAST             7  'version_file_version'
         514  LOAD_FAST             8  'version_file_lst'
         517  LOAD_FAST            13  'finished_count'
         520  LOAD_FAST             2  'analyze_map_count'
         523  CALL_FUNCTION_4       4 
         526  UNPACK_SEQUENCE_2     2 
         529  STORE_FAST           15  'ret'
         532  STORE_FAST           16  'up_info'

1242     535  LOAD_FAST            15  'ret'
         538  POP_JUMP_IF_TRUE    561  'to 561'

1243     541  LOAD_FAST             0  'self'
         544  LOAD_ATTR            18  '_analyze_patch_file_failed'
         547  LOAD_FAST            16  'up_info'
         550  CALL_FUNCTION_1       1 
         553  POP_TOP          

1244     554  LOAD_CONST            0  ''
         557  RETURN_END_IF    
       558_0  COME_FROM                '538'
         558  JUMP_FORWARD          0  'to 561'
       561_0  COME_FROM                '558'

1246     561  LOAD_GLOBAL          19  'patch_const'
         564  LOAD_ATTR            20  'ENABLE_PATCH_NPK'
         567  POP_JUMP_IF_FALSE   628  'to 628'

1247     570  LOAD_FAST             0  'self'
         573  LOAD_ATTR            21  '_patch_npk_flush_and_verify'
         576  CALL_FUNCTION_0       0 
         579  STORE_FAST           15  'ret'

1248     582  LOAD_FAST            15  'ret'
         585  POP_JUMP_IF_TRUE    628  'to 628'

1249     588  LOAD_GLOBAL          22  'print'
         591  LOAD_CONST            5  '[patch_npk] update and verify npk failed'
         594  CALL_FUNCTION_1       1 
         597  POP_TOP          

1253     598  LOAD_GLOBAL          23  'C_file'
         601  LOAD_ATTR            24  'reload_file_system'
         604  CALL_FUNCTION_0       0 
         607  POP_TOP          

1254     608  LOAD_FAST             0  'self'
         611  LOAD_ATTR            11  'put_download_patch_files_ret_cb'
         614  LOAD_GLOBAL          12  'False'
         617  CALL_FUNCTION_1       1 
         620  POP_TOP          

1255     621  LOAD_CONST            0  ''
         624  RETURN_END_IF    
       625_0  COME_FROM                '585'
         625  JUMP_FORWARD          0  'to 628'
       628_0  COME_FROM                '625'

1257     628  LOAD_GLOBAL           1  'patch_utils'
         631  LOAD_ATTR            25  'save_local_flist'
         634  LOAD_FAST             0  'self'
         637  LOAD_ATTR            26  'flist_data'
         640  LOAD_FAST             0  'self'
         643  LOAD_ATTR            27  'err_queue'
         646  CALL_FUNCTION_2       2 
         649  POP_TOP          

1258     650  LOAD_FAST             0  'self'
         653  LOAD_ATTR            28  '_support_base_package'
         656  POP_JUMP_IF_TRUE    672  'to 672'

1259     659  LOAD_GLOBAL          29  'patch_path'
         662  LOAD_ATTR            30  'remove_patch_temp_folder'
         665  CALL_FUNCTION_0       0 
         668  POP_TOP          
         669  JUMP_FORWARD          0  'to 672'
       672_0  COME_FROM                '669'

1260     672  LOAD_FAST             0  'self'
         675  LOAD_ATTR            11  'put_download_patch_files_ret_cb'
         678  LOAD_GLOBAL          31  'True'
         681  CALL_FUNCTION_1       1 
         684  POP_TOP          
         685  LOAD_CONST            0  ''
         688  RETURN_VALUE     

Parse error at or near `STORE_ATTR' instruction at offset 64

    def _analyze_patch_file_failed(self, in_up_info=None):
        if in_up_info:
            print('[patch] analyze patch file failed, info: {}'.format(in_up_info))
            self.patch_dctool.send_patch_process_info_info(in_up_info)
        self.put_download_patch_files_ret_cb(False)

    def _write_patch_file(self, file_version, finfo_lst, finished_count, all_count):
        enable_patch_npk = patch_const.ENABLE_PATCH_NPK
        enable_zip_dl = patch_const.ENABLE_ZIP_DOWNLOAD
        zip_file = None
        analyzed_count = finished_count
        cnt_fversion = file_version

        def _close_zip_file(in_zip_file):
            if in_zip_file:
                try:
                    in_zip_file.close()
                except Exception as e:
                    print('[patch] close zip error: %s' % str(e))

        if enable_zip_dl and cnt_fversion in self.patch_zip_info_dict:
            generate_res, zip_file = self._get_zip_file_with_version(cnt_fversion)
            if not generate_res:
                process_info = {'PATCH_FILE_ANALYZE_FAILED_1': 'generate zip error'}
                return (False, process_info)
        else:
            zip_file = None
        for finfo in finfo_lst:
            if self.force_stop:
                _close_zip_file(zip_file)
                return (
                 False, None)
            fpath = finfo[0]
            analyzed_count += 1
            self.analyze_prog = analyzed_count * 1.0 / all_count
            zip_relative_path, file_index_id, file_type = patch_path.get_patch_file_hash_and_type(fpath)
            rw_temp_path, orbit_temp_path = self.patch_fpath_temp_path_map[fpath]
            src_d = None
            pkg_crc = int(finfo[2])
            is_bin = file_type == patch_path.BIN_TYPE
            is_bin = IS_WIN and file_type == patch_path.BIN_TYPE
            if zip_file and not is_bin:
                try:
                    src_d = zip_file.read(zip_relative_path)
                except Exception as e:
                    self.err_queue.put('[Except] [PATCH] get data:{} from zip except:{}'.format(zip_relative_path, str(e)))
                    process_info = {'PATCH_FILE_ANALYZE_FAILED_6': 'get file from zip except!'}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)

                if not patch_utils.check_data_crc32(src_d, pkg_crc, self.err_queue):
                    print('[downloader] check crc32 failed 1:', fpath, pkg_crc)
                    process_info = {'PATCH_FILE_ANALYZE_FAILED_2': 'check_data_crc32 failed:{} {}'.format(fpath, pkg_crc)}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)
            else:
                try:
                    with open(rw_temp_path, 'rb') as tmp_file:
                        src_d = tmp_file.read()
                except Exception as e:
                    self.err_queue.put('[Except] [PATCH] get data:{} from temp except:{}'.format(fpath, str(e)))
                    process_info = {'PATCH_FILE_ANALYZE_FAILED_4': 'get data:{} except:{}'.format(fpath, str(e))}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)

                if not patch_utils.check_data_crc32(src_d, pkg_crc, self.err_queue):
                    print('[downloader] check crc error 2:', fpath, pkg_crc)
                    process_info = {'PATCH_FILE_ANALYZE_FAILED_3': 'check_file_crc32 failed:{} {}'.format(fpath, int(finfo[2]))}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)
            if enable_patch_npk and not is_bin:
                ret = self._patch_npk_processor.add_patch_data(file_type, src_d, file_index_id, pkg_crc, finfo)
                if not ret:
                    print('[downloader] [ERROR] add_patch_data failed:{}'.format(fpath))
                    process_info = {'PATCH_FILE_ANALYZE_FAILED_5': 'add_patch_data failed:{}'.format(fpath + traceback.format_exc())}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)
            else:
                try:
                    save_path = patch_path.get_download_target_path(fpath)
                    is_prev_patch = False
                    week_path = None
                    if cnt_fversion > self.real_last_week_version:
                        save_path = save_path.replace(patch_path.SCRIPT_PATCH_DIRNAME, patch_path.SCRIPT_PATCH_WEEKLY_NAME)
                        save_path = save_path.replace(patch_path.RES_PATCH_DIRNAME, patch_path.RES_PATCH_WEEKLY_NAME)
                    else:
                        week_path = save_path.replace(patch_path.SCRIPT_PATCH_DIRNAME, patch_path.SCRIPT_PATCH_WEEKLY_NAME)
                        week_path = week_path.replace(patch_path.RES_PATCH_DIRNAME, patch_path.RES_PATCH_WEEKLY_NAME)
                        week_path = patch_path.get_rw_path(week_path)
                        is_prev_patch = True
                    save_path = patch_path.get_rw_path(save_path)
                    with self.lock:
                        dirname = os.path.dirname(save_path)
                        if not os.path.exists(dirname):
                            os.makedirs(dirname)
                        tar_f = open(save_path, 'wb')
                        tar_f.write(src_d)
                        tar_f.close()
                    if is_prev_patch and not is_bin:
                        try:
                            if os.path.exists(week_path):
                                os.remove(week_path)
                        except Exception as e:
                            print('[Except] remove invalid week path file except:{}'.format(str(e)))

                except (IOError, OSError) as ose:
                    try:
                        error_no = ose.errno
                        if int(error_no) == 28:
                            self.downloader_agent.set_space_flag(True)
                        process_info = {'PATCH_FILE_ANALYZE_IO_EXCEPT': 'except:{}'.format(error_no)}
                        _close_zip_file(zip_file)
                        return (
                         False, process_info)
                    except Exception as e:
                        process_info = {'PATCH_FILE_ANALYZE_EXCEPT_1': 'check_file_crc32 failed:{} {} {}'.format(fpath, int(finfo[2]), str(e))}
                        _close_zip_file(zip_file)
                        return (
                         False, process_info)

                except Exception as e:
                    process_info = {'PATCH_FILE_ANALYZE_EXCEPT_2': 'except:{}'.format(str(e))}
                    _close_zip_file(zip_file)
                    return (
                     False, process_info)

        _close_zip_file(zip_file)
        return (
         True, '')

    def _patch_npk_flush_and_verify(self):
        self.set_state(patch_utils.DST_PATCH_NPK_UPDATE)
        self.analyze_prog = 0
        ret = self._patch_npk_processor.update_and_flush_all_npk(self.set_analyze_prog)
        if not ret:
            self._destroy_patch_npk_processor()
            self.analyze_prog = 1
            return False
        self.set_state(patch_utils.DST_PATCH_NPK_VERIFY)
        self.analyze_prog = 0
        ret = self._patch_npk_processor.verify_and_save_new_npk_info(self.set_analyze_prog)
        self._destroy_patch_npk_processor()
        self.analyze_prog = 1
        return ret

    def _destroy_patch_npk_processor(self):
        if self._patch_npk_processor:
            self._patch_npk_processor.destroy()
            self._patch_npk_processor = None
        return

    def download_patch_files(self, callback):
        self.set_state(patch_utils.DST_FILES)
        self.patch_files_dld_callback = callback
        self.patch_download_id_str = str(int(time.time()))
        if patch_const.ENABLE_ZIP_DOWNLOAD:
            download_list = self.zip_patch_download_list
        else:
            download_list = self.generate_patch_download_list()
        if download_list:
            download_list = sorted(download_list, key=cmp_to_key(--- This code section failed: ---

1428       0  LOAD_GLOBAL           0  'six_ex'
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
            self.on_download_patch_files_callback([], [], 0)
            return
        if not self.downloader_agent.start_download(download_list, self.on_download_patch_files_callback, self.get_patch_size()):
            self.err_queue.put('start downlod patch files failed')
            self.put_download_patch_files_ret_cb(False)

    def stop_downloader(self):
        self.force_stop = True
        self.downloader_agent.stop_download()

    def put_check_patch_ret_cb(self, ret, cb_info=None):
        cb = self.patch_check_callback
        if not cb:
            raise
        self.patch_check_callback = None
        self.retqueue.put((cb, (ret, cb_info)))
        return

    def put_download_patch_files_ret_cb(self, ret, cb_info=None):
        cb = self.patch_files_dld_callback
        if not cb:
            raise
        self.patch_files_dld_callback = None
        self.retqueue.put((cb, (ret, cb_info)))
        return

    def set_state(self, state):
        self.state = state

    def put_npk_check_ret_cb(self, ret):
        cb = self.npk_check_callback
        if not cb:
            raise
        self.npk_check_callback = None
        self.retqueue.put((cb, (ret,)))
        return

    def download_npklist(self, cb):
        self.set_state(patch_utils.DST_NPK_LIST_DLD)
        self.npk_check_callback = cb
        npk_list_url = self.get_npk_list_url()
        temp_file_path = os.path.join(patch_path.TEMP_DIRNAME, patch_path.NPK_LIST_FILE_NAME)
        list_orbit_path = patch_path.get_orbit_download_path(temp_file_path)
        list_rw_path = patch_path.get_rw_path(temp_file_path)
        download_list = [(list_orbit_path, list_rw_path, npk_list_url, 0)]
        if not self.downloader_agent.start_download(download_list, self.on_download_npklist_callback):
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_ERROR)
        else:
            process_info = {'DL_NPK_LIST': npk_list_url}
            self.patch_dctool.send_patch_process_info_info(process_info)

    def on_download_npklist_callback(self, success_list, error_list, consume_time):
        if error_list:
            process_info = {'DL_NPK_LIST_FAILED': 'download error','consume_time': consume_time}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_ERROR)
        else:
            file_path = success_list[0][1]
            if not os.path.exists(file_path):
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_ERROR)
            else:
                process_info = {'DL_NPK_LIST_SUCCESS': 'download success','consume_time': consume_time}
                self.patch_dctool.send_patch_process_info_info(process_info)
                with open(file_path, 'rb') as tmp_file:
                    data = tmp_file.read()
                t = threading.Thread(target=self.npklist_analyze, args=(data,))
                t.setDaemon(True)
                t.start()

    def npklist_analyze(self, ret):
        try:
            lines = ret.splitlines()
            for idx, line in enumerate(lines):
                line = six.ensure_str(line)
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                line = line.strip()
                lines[idx] = line

            npk_list_redirect_url = patch_utils.analyze_redirect_url(self, lines, NOW_PLATFORM_NAME)
            if npk_list_redirect_url:
                self.npk_list_redirect_url = npk_list_redirect_url
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_REDIRECT)
                return
            patch_utils.analyze_remote_code(self, lines, NOW_PLATFORM_NAME)
            can_ignore_npk = self.can_ignore_npk_process()
            if can_ignore_npk:
                print('[downloader] ignore npk:', can_ignore_npk)
                process_info = {'npklist_analyze_ignore': 'ignore npk'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
                return
            valid_npk_info = patch_utils.filter_valid_npk_info(lines, NOW_PLATFORM_NAME, self._npk_svn_version)
            if not valid_npk_info:
                print('[downloader] force npk process and no valid npk info')
                npk_list_url = self.get_npk_list_url()
                process_info = {'NPKLIST_ANALYZE_FAILED': 'no match npk info',
                   'url_and_version': 'url:{}, npk_version:{}'.format(npk_list_url, self._npk_svn_version)
                   }
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_ERROR)
            else:
                self.set_npk_info_url(valid_npk_info)
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_LIST_FILE_SUCCESS)
        except Exception as e:
            print('[Except] [downloader] npk list_analyze except:', str(e))
            patch_utils.force_error_next_frame()

    def do_generate_npk_download_list(self, unchecked_list, info_map):
        download_list = []
        for npk_name in unchecked_list:
            rw_path = patch_path.get_rw_path(npk_name)
            orbit_path = patch_path.get_orbit_download_path(npk_name)
            npk_size = info_map[npk_name][1]
            npk_md5 = info_map[npk_name][0]
            if os.path.exists(rw_path):
                os.remove(rw_path)
            url = self.get_npk_src_url(npk_name)
            download_list.append((orbit_path, rw_path, url, npk_size, npk_md5))

        return download_list

    def generate_npk_download_list(self):
        download_list = []
        download_list.extend(self.do_generate_npk_download_list(self.npk_unchecked_list, self.npk_file_info))
        return download_list

    def on_download_npkfiles_callback(self, success_list, error_list, consume_time):
        if error_list:
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_FILE_ERROR)
        else:
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_FILE_SUCCESS)

    def download_npkfiles(self, cb):
        self.set_state(patch_utils.DST_NPK_FILES)
        self.npk_check_callback = cb
        download_list = self.generate_npk_download_list()
        if not download_list:
            self.err_queue.put('try download npk file but list is empty')
            self.on_download_npkfiles_callback([], [], 0)
            return
        total_download_size = 0
        for data in download_list:
            total_download_size += data[3]

        if not self.downloader_agent.start_download(download_list, self.on_download_npkfiles_callback, total_download_size, False):
            self.err_queue.put('start download npk files failed')
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_FILE_ERROR)

    def on_npkinfo_download_finished(self, success_list, error_list, consume_time):
        if error_list:
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_INFO_FILE_ERROR)
        else:
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_INFO_FILE_SUCCESS)

    def download_npkinfo(self, cb):
        self.set_state(patch_utils.DST_NPK_INFO)
        self.npk_check_callback = cb
        try:
            download_list = []
            npk_info_url = self.get_npk_info_url()
            info_orbit_path = patch_path.get_orbit_download_path(patch_path.NPK_INFO_FILE_NAME)
            info_rw_path = patch_path.get_rw_path(patch_path.NPK_INFO_FILE_NAME)
            download_list.append((info_orbit_path, info_rw_path, npk_info_url, 0))
            if not (npk_info_url and self.downloader_agent.start_download(download_list, self.on_npkinfo_download_finished)):
                self.err_queue.put('download_npkinfo with version error')
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_INFO_FILE_ERROR)
        except Exception as e:
            self.err_queue.put('download npk list function with error' + str(e))
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_DLD_INFO_FILE_ERROR)

    def resert_npk_info(self):
        self.npk_file_info = {}
        self.npk_download_size = 0
        self.npk_prev_download_size = 0
        self.npk_unchecked_list = []
        self.npk_info_list = []

    def revert_thread_func(self, callback):

        def revert_func():
            print('thread func start revert')
            from patch.revert import revert
            revert()
            print('reinit config')
            self.init_config()
            callback()

        t = threading.Thread(target=revert_func)
        t.setDaemon(True)
        t.start()

    def check_npk_info(self, cb):
        self.set_state(patch_utils.DST_NPK_CHECK)
        npk_info = patch_utils.read_npk_info()
        self.npk_check_callback = cb
        if not npk_info:
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)
            return
        try:
            files_info = npk_info.get(BASIC_COMPLETION_NPK_NAME, {})
            high_end_files_info = npk_info.get(HIGH_END_NPK_NAME, {})
            low_end_files_info = npk_info.get(LOW_END_NPK_NAME, {})
            if self._support_astc:
                files_info.update(high_end_files_info)
            else:
                files_info.update(low_end_files_info)
            local_npk_version = int(npk_info.get('version', 0))
            npk_valid = patch_utils.check_npk_version_valid(self.npk_info_list, local_npk_version, self._npk_svn_version)
            if not npk_valid:
                print('[downloader] npk no valid:{},{}'.format(local_npk_version, self._npk_svn_version))
                process_info = {'CHECK_NPK_INVALID': 'npk info config not match',
                   'version_info': 'npk_info record version:{}, npk_svn_version:{}'.format(local_npk_version, self._npk_svn_version)
                   }
                self.patch_dctool.send_patch_process_info_info(process_info)
                try:
                    for tmp_npk_name, v in six.iteritems(files_info):
                        file_path = patch_path.get_rw_path(tmp_npk_name)
                        if os.path.exists(file_path) and str(self._npk_svn_version) not in str(tmp_npk_name):
                            print('downloader remove npk:', tmp_npk_name)
                            os.remove(file_path)

                    self._remove_npk_info_config_file()
                    self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)
                    return
                except Exception as e:
                    print('[Exception] e when delete invalid npk info file', str(e))
                    process_info = {'CHECK_NPK_REMOVE_EXCEPT': 'exception:{}'.format(str(e))}
                    self.patch_dctool.send_patch_process_info_info(process_info)
                    patch_utils.send_script_error(str(e))
                    self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)

                return
            if not files_info:
                print('[downloader] no need download files')
                process_info = {'CHECK_NPK_INFO_NO_NEED_NPK': 'no need download npk files, npk stage done'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
                return
            npk_name_lst = six_ex.keys(files_info)
            print('[downloader] files info:', npk_name_lst)
            process_info = {'CHECK_NPK_INFO_DONE': 'check npk info success, begin analyze local npk',
               'npk_files': npk_name_lst
               }
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.npk_file_info = files_info
            self.npkinfo_analyze()
        except Exception as e:
            process_info = {'CHECK_NPK_INFO_EXCEPT': 'local npk info maybe modified!!! info:{}, exception:{}'.format(npk_info, str(e))}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.err_queue.put('check npk info with error' + str(e))
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)

    def check_npk_old(self, cb):
        self.set_state(patch_utils.DST_NPK_CHECK)
        npk_info = patch_utils.read_npk_info()
        self.npk_check_callback = cb
        if not npk_info:
            process_info = {'stage': 'check npk old','info': 'no npk info file'}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
            return
        try:
            files_info = npk_info.get(BASIC_COMPLETION_NPK_NAME, {})
            if not files_info:
                process_info = {'stage': 'check npk old','info': 'npk info file exist, but no files info'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
                return
            self.npk_file_info = files_info
            self.npkinfo_analyze()
        except Exception as e:
            process_info = {'stage': 'check npk old','error': str(e)}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.err_queue.put('check npk info with error' + str(e))
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)

    def npkinfo_analyze(self):
        t = threading.Thread(target=self.npkinfo_analyze_thread_func)
        t.setDaemon(True)
        t.start()

    def calc_npk_analyze_info(self, file_info, valid_npk_list):
        uncheck_list = []
        download_size = 0
        prev_download_size = 0
        for k, v in six.iteritems(file_info):
            if k not in valid_npk_list:
                download_size += v[1]
                temp_file_name = k + '.tmp'
                temp_file_path = patch_path.get_rw_path(temp_file_name)
                if os.path.exists(temp_file_path):
                    prev_download_size += os.path.getsize(temp_file_path)
                uncheck_list.append(k)

        return (download_size, prev_download_size, uncheck_list)

    def npkinfo_analyze_callback(self, valid_npk_list):
        try:
            self.npk_download_size, self.npk_prev_download_size, self.npk_unchecked_list = self.calc_npk_analyze_info(self.npk_file_info, valid_npk_list)
            checked_ok = self.npk_download_size == 0
            print('[downloader] down npk size:', self.npk_download_size)
            process_info = {'CHECK_NPK_FILE_DL_SIZE': 'download size:{}'.format(self.npk_download_size)}
            self.patch_dctool.send_patch_process_info_info(process_info)
            if checked_ok:
                package_utils.set_game_init_mode(package_utils.GAME_INIT_WITH_NPK)
                if hasattr(patch_utils, 'save_com_npk_md5_checked_flag'):
                    patch_utils.save_com_npk_md5_checked_flag()
            if self._support_completion_npk:
                state = patch_utils.NPK_STATE_CHECK_OK if checked_ok else patch_utils.NPK_STATE_FILE_MISS_OR_ERROR
                self.put_npk_check_ret_cb(state)
            else:
                if self.npk_unchecked_list:
                    print('[downloader] unchecked list:', self.npk_unchecked_list)
                    process_info = {'stage': 'check npk file cb','info': 'old npk has unchecked:{}'.format(self.npk_unchecked_list)}
                    self.patch_dctool.send_patch_process_info_info(process_info)
                    for npk_name in self.npk_unchecked_list:
                        if npk_name in self.npk_file_info:
                            del self.npk_file_info[npk_name]

                self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
        except Exception as e:
            self.err_queue.put('npkinfo_analyze_callback' + str(e))
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)

    def npkinfo_analyze_thread_func(self):
        info = deepcopy(self.npk_file_info)
        valid_npk_list = []
        try:
            md5_checked = patch_utils.is_com_npk_md5_checked()
        except Exception as e:
            print('[PATCH] get npk check flag except:', str(e))
            md5_checked = False

        try:
            self.analyze_prog = 0
            total_size = 0
            checked_size = 0
            for k, v in six.iteritems(info):
                total_size += v[1]

            if total_size == 0:
                process_info = {'NPK_ANALYZE_SIZE_ZERO': 'get npk size is zero from npk_info.config'}
                self.patch_dctool.send_patch_process_info_info(process_info)
                if self._support_completion_npk:
                    self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)
                else:
                    self.put_npk_check_ret_cb(patch_utils.NPK_STATE_CHECK_OK)
                self.err_queue.put('get npk size is zero????')
                return
            for k, v in six.iteritems(info):
                file_path = patch_path.get_rw_path(k)
                if not os.path.exists(file_path):
                    checked_size += v[1]
                    self.analyze_prog = checked_size * 1.0 / total_size
                    continue
                if not md5_checked:
                    cmp_mid = v[0]
                    m = hashlib.md5()
                    with open(file_path, 'rb') as npk_file:
                        file_buffer = npk_file.read(patch_const.CHUNK_SIZE)
                        while file_buffer:
                            checked_size += len(file_buffer)
                            self.analyze_prog = checked_size * 1.0 / total_size
                            m.update(file_buffer)
                            file_buffer = npk_file.read(patch_const.CHUNK_SIZE)

                    if str(m.hexdigest()) == cmp_mid:
                        valid_npk_list.append(k)
                    else:
                        os.remove(file_path)
                else:
                    cmp_size = v[1]
                    try:
                        local_size = os.path.getsize(file_path)
                        if int(cmp_size) == int(local_size):
                            valid_npk_list.append(k)
                        else:
                            self.msg_queue.put('remove npk:{}'.format(k))
                            self.err_queue.put('com_npk:{} size not match {}:{}'.format(file_path, local_size, cmp_size))
                            os.remove(file_path)
                    except Exception as e:
                        self.err_queue.put('check com_npk size exception:{}'.format(str(e)))

            self.retqueue.put((self.npkinfo_analyze_callback, (valid_npk_list,)))
        except Exception as e:
            process_info = {'NPK_ANALYZE_EXCEPT': 'exception:{}'.format(str(e))}
            self.patch_dctool.send_patch_process_info_info(process_info)
            self.err_queue.put('check npk file with error ' + str(e) + '\n' + traceback.format_exc())
            self.put_npk_check_ret_cb(patch_utils.NPK_STATE_INFO_MISS_OR_ERROR)

    def add_npk_loader(self, npk_file_info):
        root_dir = '%%WORK_DIR%%\\%s'
        if NOW_PLATFORM == game3d.PLATFORM_IOS:
            root_dir = '%%DOC_DIR%%\\%s'
        npk_names = six_ex.keys(npk_file_info)
        for name in npk_names:
            name = name[:-4]
            root = root_dir % name
            if patch_const.ENABLE_PATCH_NPK:
                ret = C_file.add_res_npk_loader(root, 0, COM_NPK_LOADER)
            else:
                ret = C_file.add_res_npk_loader(root, 0)
            if not ret:
                self.err_queue.put('add_com_npk_loader_failed')
                return False

        if hasattr(patch_const, 'ENABLE_CHECK_NPK_FLIST') and patch_const.ENABLE_CHECK_NPK_FLIST:
            for npk_name in npk_names:
                npk_flist_path = patch_path.RES_FLIST_FILE_PARTTEN % npk_name[:-4]
                flist_exists = C_file.find_res_file(npk_flist_path, '')
                if not flist_exists:
                    self.err_queue.put('add_com_npk_success_flist_not_exists')
                    return False

        six.moves.builtins.__dict__['COM_NPK_NAMES'] = npk_names
        process_info = {'ADD_NPK_LOADER_SUCCESS': 'npk names:{}'.format(npk_names)}
        self.patch_dctool.send_patch_process_info_info(process_info)
        return True

    def init_npk_filesystem(self):
        ret = self.add_npk_loader(self.npk_file_info)
        if not ret and hasattr(C_file, 'del_fileloader_by_tag'):
            C_file.del_fileloader_by_tag(COM_NPK_LOADER)
        return ret

    def get_space_flag(self):
        return self.downloader_agent.get_space_flag()

    def _remove_npk_info_config_file(self):
        try:
            npk_file_info_path = patch_path.get_rw_path(patch_path.NPK_INFO_FILE_NAME)
            if os.path.exists(npk_file_info_path):
                os.remove(npk_file_info_path)
        except Exception as e:
            print('[Exception] remove npk_info_config_file except:{}'.format(str(e)))

    def set_support_astc(self, support_astc):
        self._support_astc = support_astc

    def set_support_new_ui_astc_patch(self, enable):
        self._support_new_ui_astc_patch = enable

    def set_support_completion_npk(self, support_completion_npk):
        self._support_completion_npk = support_completion_npk

    def set_game_init_mode(self, mode_code):
        self._game_init_mode = mode_code

    def set_npk_version(self, in_npk_version):
        self._npk_svn_version = in_npk_version

    def force_npk_process(self):
        return self._game_init_mode == package_utils.GAME_INIT_WITH_NPK

    def can_ignore_npk_process(self):
        ignore_npk_download = six.moves.builtins.__dict__.get('IGNORE_DOWNLOAD_NPK', False)
        return self._game_init_mode != package_utils.GAME_INIT_WITH_NPK and ignore_npk_download

    def get_patch_file_target_version(self, f_info):
        if self._support_base_package and len(f_info) >= 8:
            return int(f_info[7])
        else:
            return int(f_info[5])

    def get_ext_name(self, f_info):
        try:
            if self._support_base_package and len(f_info) >= 7:
                return f_info[6]
            return 'base'
        except Exception as e:
            self.err_queue.put('get_ext_name:{}'.format(str(e)))
            return 'base'

    def set_analyze_prog(self, in_value):
        self.analyze_prog = in_value


class OrbitDownloader(Downloader):

    def __init__(self, retqueue):
        super(OrbitDownloader, self).__init__(retqueue)
        self.is_orbit = True
        self.downloader_agent = orbit_downloader.OrbitDownloader(self.retqueue, self.err_queue, self.msg_queue)