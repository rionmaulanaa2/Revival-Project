# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_path.py
from __future__ import absolute_import
from __future__ import print_function
import game3d
import os
import shutil
import six
ORG_FLIST_FILEPATH = 'org_flist.lst'
RES_FLIST_FILE_PARTTEN = '%s_flist.txt'
FILELIST_FILEPATH = 'res_patch/flist.lst'
FILELIST_NAME = 'flist.lst'
CACERT_PATH = '{}/cacert.pem'.format(game3d.get_doc_dir())
TEMP_DIRNAME = 'patch_temp'
SCRIPT_PATCH_DIRNAME = 'script_patch'
RES_PATCH_DIRNAME = 'res_patch'
SCRIPT_PATCH_WEEKLY_NAME = 'script_week'
RES_PATCH_WEEKLY_NAME = 'res_week'
WEEK_FILE_NAME = 'winfo.config'
LOG_PATCH_FILEPATH = 'log_patch.txt'
LOG_STATE_FILEPATH = 'log_state.txt'
PATCH_LIST_NAME = 'patchlist.txt'
SCRIPT_PREFIX = 'script/'
SCRIPT3_PREFIX = 'script3/'
RES_PREFIX = 'res/'
BIN_PREFIX = 'bin_patch/'
NPK_INFO_FILE_NAME = 'npk_info.config'
NPK_LIST_FILE_NAME = 'npklist.txt'
HASH_FOLDER_COUNT = 1023
QUALITY_FILE_NAME = 'quality.config'
MULTI_LANG_TEXT_PATH = 'confs/text/{}/'
HIGH_RES_ZIP_FILE_PATTERN = 'patch_zip_%d.zip'
BASE_HIGH_RES_ZIP_FILE_PATTERN = 'base_patch_zip_%d.zip'
COMPATIBLE_RES_ZIP_FILE_PATTERN = 'patch_compatible_zip_%d.zip'
BASE_COMPATIBLE_RES_ZIP_FILE_PATTERN = 'base_patch_compatible_zip_%d.zip'
HIGH_RES_ZIP_RANGE_PATTERN = 'patch_zip_%d_part_%d.zip'
BASE_HIGH_RES_ZIP_RANGE_PATTERN = 'base_patch_zip_%d_part_%d.zip'
COMPATIBLE_RES_ZIP_RANGE_PATTERN = 'patch_compatible_zip_%d_part_%d.zip'
BASE_COMPATIBLE_RES_ZIP_RANGE_PATTERN = 'base_patch_compatible_zip_%d_part_%d.zip'
ASTC_RES_ZIP_FILE_PATTERN = 'astc_patch_zip_%d.zip'
ASTC_BASE_RES_ZIP_FILE_PATTERN = 'astc_base_patch_zip_%d.zip'
ASTC_RES_ZIP_RANGE_PATTERN = 'astc_patch_zip_%d_part_%d.zip'
ASTC_BASE_RES_ZIP_RANGE_PATTERN = 'astc_base_patch_zip_%d_part_%d.zip'
PATCH_CONFIG_FILE_NAME = 'res/patch_config.json'
PATCH_NPK_DIR = 'patch_npk'
G_PATCH_NPK_DIR = None
G_NEOX_DIR = None
DRFP_ERROR_CHANNEL = '[PATCH_ERROR]'
DRFP_EXCEPT_CHANNEL = '[PATCH_EXCEPT]'
BIN_TYPE = 0
RES_TYPE = 1
SCRIPT_TYPE = 2
IS_PY3 = six.PY3

def get_neox_dir():
    global G_NEOX_DIR
    if G_NEOX_DIR is None:
        doc_dir = game3d.get_doc_dir()
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            doc_dir = os.path.dirname(doc_dir)
        elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
            doc_dir = os.path.dirname(doc_dir)
        G_NEOX_DIR = doc_dir
    return G_NEOX_DIR


def get_patch_npk_dir():
    global G_PATCH_NPK_DIR
    if G_PATCH_NPK_DIR is None:
        G_PATCH_NPK_DIR = os.path.join(get_neox_dir(), PATCH_NPK_DIR)
    return G_PATCH_NPK_DIR


def get_orbit_download_path(file_relative_path):
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        return file_relative_path
    else:
        return get_rw_path(file_relative_path)


def convert_to_temp_path(url_fpath):
    tmp_dir = get_tmp_dir()
    hash_url_path = convert_to_hashed_file_path(url_fpath)
    return '{0}/{1}'.format(tmp_dir, str(hash_url_path))


def get_rw_path(file_relative_path):
    return os.path.join(get_neox_dir(), file_relative_path).replace('\\', '/')


def get_log_state_path():
    return os.path.join(get_neox_dir(), LOG_STATE_FILEPATH)


def get_res_patch_path():
    return os.path.join(get_neox_dir(), RES_PATCH_DIRNAME)


def get_weekly_file_path():
    return os.path.join(get_neox_dir(), RES_PATCH_WEEKLY_NAME, WEEK_FILE_NAME)


def get_weekly_res_path():
    return os.path.join(get_neox_dir(), RES_PATCH_WEEKLY_NAME)


def get_weekly_script_path():
    return os.path.join(get_neox_dir(), SCRIPT_PATCH_WEEKLY_NAME)


def get_script_patch_path():
    return os.path.join(get_neox_dir(), SCRIPT_PATCH_DIRNAME)


def get_flist_path():
    return os.path.join(get_neox_dir(), FILELIST_FILEPATH)


def get_tmp_dir():
    return os.path.join(get_neox_dir(), TEMP_DIRNAME)


def get_download_target_path--- This code section failed: ---

 145       0  LOAD_GLOBAL           0  'convert_to_hashed_file_path'
           3  LOAD_FAST             0  'path'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            0  'path'

 146      12  LOAD_FAST             0  'path'
          15  LOAD_ATTR             1  'startswith'
          18  LOAD_CONST            1  'res/'
          21  CALL_FUNCTION_1       1 
          24  POP_JUMP_IF_FALSE    41  'to 41'

 147      27  LOAD_CONST            2  'res_patch'
          30  LOAD_CONST            3  3
          33  SLICE+1          
          34  BINARY_ADD       
          35  STORE_FAST            0  'path'
          38  JUMP_FORWARD         29  'to 70'

 148      41  LOAD_FAST             0  'path'
          44  LOAD_ATTR             1  'startswith'
          47  LOAD_CONST            4  'script/'
          50  CALL_FUNCTION_1       1 
          53  POP_JUMP_IF_FALSE    70  'to 70'

 149      56  LOAD_CONST            5  'script_patch'
          59  LOAD_CONST            6  6
          62  SLICE+1          
          63  BINARY_ADD       
          64  STORE_FAST            0  'path'
          67  JUMP_FORWARD          0  'to 70'
        70_0  COME_FROM                '67'
        70_1  COME_FROM                '38'

 150      70  LOAD_FAST             0  'path'
          73  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_ADD' instruction at offset 34


def get_abs_download_target_path(path):
    return os.path.abspath(os.path.join(get_neox_dir(), get_download_target_path(path)))


def create_patch_temp_folder():
    try:
        temp_dir = get_tmp_dir()
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        npk_dir = get_patch_npk_dir()
        if not os.path.exists(npk_dir):
            os.makedirs(npk_dir)
        return True
    except Exception as e:
        print('[EXCEPT] create patch temp or patch npk folder except:', str(e))
        return False


def remove_patch_temp_folder():
    try:
        temp_dir = get_tmp_dir()
        shutil.rmtree(temp_dir)
    except Exception as e:
        print('remove patch temp folder failed', str(e))


def convert_to_hashed_file_path(path):
    if path.startswith(BIN_PREFIX):
        return path
    prefix = RES_PREFIX
    if path.startswith(SCRIPT_PREFIX):
        prefix = SCRIPT_PREFIX
    relative_path = path[len(prefix):]
    target_relative_path = relative_path.replace('/', '\\')
    string_id_int = game3d.calc_filename_hash64(target_relative_path)
    trans_folder_name = str(abs(string_id_int % HASH_FOLDER_COUNT))
    data_path = '%s%s/%d' % (prefix, trans_folder_name, string_id_int)
    return data_path


def get_patch_server_location(in_path):
    if in_path.startswith(BIN_PREFIX):
        return in_path
    if in_path.startswith(SCRIPT_PREFIX):
        prefix = SCRIPT_PREFIX
        ret_pre = SCRIPT3_PREFIX if IS_PY3 else SCRIPT_PREFIX
    else:
        prefix = RES_PREFIX
        ret_pre = RES_PREFIX
    relative_path = in_path[len(prefix):]
    target_relative_path = relative_path.replace('/', '\\')
    string_id_int = game3d.calc_filename_hash64(target_relative_path)
    trans_folder_name = str(abs(string_id_int % HASH_FOLDER_COUNT))
    data_path = '%s%s/%d' % (ret_pre, trans_folder_name, string_id_int)
    return data_path


def get_patch_file_hash_and_type(path):
    if path.startswith(BIN_PREFIX):
        return (path, None, BIN_TYPE)
    else:
        if path.startswith(SCRIPT_PREFIX):
            prefix = SCRIPT_PREFIX
            file_type = SCRIPT_TYPE
            ret_pre = SCRIPT3_PREFIX if IS_PY3 else SCRIPT_PREFIX
        else:
            prefix = RES_PREFIX
            ret_pre = RES_PREFIX
            file_type = RES_TYPE
        relative_path = path[len(prefix):]
        target_relative_path = relative_path.replace('/', '\\')
        string_id_int = game3d.calc_filename_hash64(target_relative_path)
        trans_folder_name = str(abs(string_id_int % HASH_FOLDER_COUNT))
        data_path = '%s%s/%d' % (ret_pre, trans_folder_name, string_id_int)
        return (
         data_path, string_id_int, file_type)


def get_patch_file_hash(path):
    if path.startswith(BIN_PREFIX):
        return None
    else:
        if path.startswith(SCRIPT_PREFIX):
            prefix = SCRIPT_PREFIX
        else:
            prefix = RES_PREFIX
        relative_path = path[len(prefix):]
        target_relative_path = relative_path.replace('/', '\\')
        string_id_int = game3d.calc_filename_hash64(target_relative_path)
        return string_id_int


def get_temp_flst_orbit_path(version_int):
    flistname = os.path.join(TEMP_DIRNAME, 'flist_%d.lst' % version_int)
    return get_orbit_download_path(flistname)


def get_temp_flst_rw_path(version_int):
    flistname = os.path.join(TEMP_DIRNAME, 'flist_%d.lst' % version_int)
    return get_rw_path(flistname)


def get_patch_zip_orbit_path(patch_pattern, version):
    zip_filename = os.path.join(TEMP_DIRNAME, patch_pattern % version)
    return get_orbit_download_path(zip_filename)


def get_patch_zip_rw_path(patch_pattern, version):
    zip_filename = os.path.join(TEMP_DIRNAME, patch_pattern % version)
    return get_rw_path(zip_filename)


def get_patch_zip_range_orbit_path(range_pattern, version, part):
    range_filename = os.path.join(TEMP_DIRNAME, range_pattern % (version, part))
    return get_orbit_download_path(range_filename)


def get_patch_zip_range_rw_path(range_pattern, version, part):
    range_filename = os.path.join(TEMP_DIRNAME, range_pattern % (version, part))
    return get_rw_path(range_filename)


def get_temp_flist_name(version_int):
    return 'flist_%d.lst' % version_int


def get_temp_patchlist_path():
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        return os.path.join(TEMP_DIRNAME, PATCH_LIST_NAME)
    else:
        return get_abs_temp_patchlist_path()


def get_abs_temp_patchlist_path():
    temp_flist_path = os.path.join(TEMP_DIRNAME, PATCH_LIST_NAME)
    return os.path.join(get_neox_dir(), temp_flist_path)


def get_patch_file_orbit_temp_path(patch_file_name):
    hash_url_path = convert_to_hashed_file_path(patch_file_name)
    path = os.path.join(TEMP_DIRNAME, hash_url_path)
    return get_orbit_download_path(path)


def get_patch_file_rw_temp_path(patch_file_name):
    hash_url_path = convert_to_hashed_file_path(patch_file_name)
    path = os.path.join(TEMP_DIRNAME, hash_url_path)
    return get_rw_path(path)


def get_npk_info_rw_path():
    return get_rw_path(NPK_INFO_FILE_NAME)


def get_npk_info_orbit_path():
    return get_orbit_download_path(NPK_INFO_FILE_NAME)


def get_patch_config_rw_path(version_int):
    temp_file_path = os.path.join(TEMP_DIRNAME, 'patch_config_%d.json' % int(version_int))
    return get_rw_path(temp_file_path)


def get_patch_config_orbit_path(version_int):
    temp_file_path = os.path.join(TEMP_DIRNAME, 'patch_config_%d.json' % int(version_int))
    return get_orbit_download_path(temp_file_path)


def is_bin_patch(path):
    return path.find(BIN_PREFIX) >= 0