# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_pn_utils.py
from __future__ import absolute_import
from __future__ import print_function
import os
import zlib
import json
import game3d
import C_file
import six
from patch import patch_path
EXT_PATCH_NPK_FOLDER = 'ext_patch_npk'
EXT_PATCH_NPK_INFO_FILENAME = 'ext_pn_info.config'
DRFP_ERROR_CHANNEL = '[EXT_PN_ERROR]'
EXT_PATCH_NPK_DIR = None
EXT_PATCH_NPK_INFO_FILE_PATH = None
MAX_NPK_SIZE = 209715200.0
EXT_LOADER_TAG = 'ext_patch_npk'
EXT_RES_NPK_SUBFIX_PATTERN = 'ep_res_{}.npk'
TEMP_EXT_RES_NPK_SUBFIX_PATTERN = 'ep_res_{}_tmp.npk'

def get_ext_patch_npk_dir():
    global EXT_PATCH_NPK_DIR
    if EXT_PATCH_NPK_DIR is None:
        EXT_PATCH_NPK_DIR = os.path.join(patch_path.get_neox_dir(), EXT_PATCH_NPK_FOLDER)
    return EXT_PATCH_NPK_DIR


def create_ext_patch_npk_folder():
    try:
        npk_dir = get_ext_patch_npk_dir()
        if not os.path.exists(npk_dir):
            os.makedirs(npk_dir)
        return True
    except Exception as e:
        print('[ERROR] create ext patch npk folder with exception:', str(e))
        return False


def get_ext_patch_npk_info_file_path():
    global EXT_PATCH_NPK_INFO_FILE_PATH
    if EXT_PATCH_NPK_INFO_FILE_PATH is None:
        npk_dir = get_ext_patch_npk_dir()
        EXT_PATCH_NPK_INFO_FILE_PATH = os.path.join(npk_dir, EXT_PATCH_NPK_INFO_FILENAME)
    return EXT_PATCH_NPK_INFO_FILE_PATH


def get_saved_ext_patch_npk_info--- This code section failed: ---

  61       0  LOAD_GLOBAL           0  'get_ext_patch_npk_info_file_path'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            0  'file_path'

  62       9  LOAD_GLOBAL           1  'os'
          12  LOAD_ATTR             2  'path'
          15  LOAD_ATTR             3  'exists'
          18  LOAD_FAST             0  'file_path'
          21  CALL_FUNCTION_1       1 
          24  POP_JUMP_IF_FALSE   149  'to 149'

  63      27  SETUP_EXCEPT         65  'to 95'

  64      30  LOAD_GLOBAL           4  'open'
          33  LOAD_GLOBAL           1  'os'
          36  CALL_FUNCTION_2       2 
          39  SETUP_WITH           37  'to 79'
          42  STORE_FAST            1  'tmp_file'

  65      45  LOAD_GLOBAL           5  'json'
          48  LOAD_ATTR             6  'loads'
          51  LOAD_GLOBAL           7  'zlib'
          54  LOAD_ATTR             8  'decompress'
          57  LOAD_FAST             1  'tmp_file'
          60  LOAD_ATTR             9  'read'
          63  CALL_FUNCTION_0       0 
          66  CALL_FUNCTION_1       1 
          69  CALL_FUNCTION_1       1 
          72  STORE_FAST            2  'npk_config'
          75  POP_BLOCK        
          76  LOAD_CONST            0  ''
        79_0  COME_FROM_WITH           '39'
          79  WITH_CLEANUP     
          80  END_FINALLY      

  66      81  LOAD_GLOBAL          10  'True'
          84  LOAD_FAST             2  'npk_config'
          87  BUILD_TUPLE_2         2 
          90  RETURN_VALUE     
          91  POP_BLOCK        
          92  JUMP_ABSOLUTE       159  'to 159'
        95_0  COME_FROM                '27'

  67      95  DUP_TOP          
          96  LOAD_GLOBAL          11  'Exception'
          99  COMPARE_OP           10  'exception-match'
         102  POP_JUMP_IF_FALSE   145  'to 145'
         105  POP_TOP          
         106  STORE_FAST            3  'e'
         109  POP_TOP          

  68     110  LOAD_GLOBAL          12  'print'
         113  LOAD_CONST            2  '[Except] get local save ext version:{}'
         116  LOAD_ATTR            13  'format'
         119  LOAD_GLOBAL          14  'str'
         122  LOAD_FAST             3  'e'
         125  CALL_FUNCTION_1       1 
         128  CALL_FUNCTION_1       1 
         131  CALL_FUNCTION_1       1 
         134  POP_TOP          

  69     135  LOAD_GLOBAL          15  'False'
         138  BUILD_MAP_0           0 
         141  BUILD_TUPLE_2         2 
         144  RETURN_VALUE     
         145  END_FINALLY      
       146_0  COME_FROM                '145'
         146  JUMP_FORWARD         10  'to 159'

  71     149  LOAD_GLOBAL          10  'True'
         152  BUILD_MAP_0           0 
         155  BUILD_TUPLE_2         2 
         158  RETURN_VALUE     
       159_0  COME_FROM                '146'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 36


def save_ext_patch_npk_info(info_dict):
    info_path = get_ext_patch_npk_info_file_path()
    dir_name = os.path.dirname(info_path)
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        info_str = zlib.compress(six.ensure_binary(json.dumps(info_dict)))
        with open(info_path, 'wb') as tmp_file:
            tmp_file.write(info_str)
        return (True, '')
    except Exception as e:
        print('[Except] save patch npk info except:{}'.format(str(e)))
        return (
         False, str(e))


def get_patch_npk_flist_file_id--- This code section failed: ---

  92       0  LOAD_CONST            1  '{}_flist.txt'
           3  LOAD_ATTR             0  'format'
           6  LOAD_ATTR             2  'calc_filename_hash64'
           9  SLICE+2          
          10  CALL_FUNCTION_1       1 
          13  STORE_FAST            1  'relative_path'

  93      16  LOAD_GLOBAL           1  'game3d'
          19  LOAD_ATTR             2  'calc_filename_hash64'
          22  LOAD_FAST             1  'relative_path'
          25  CALL_FUNCTION_1       1 
          28  STORE_FAST            2  'string_id_int'

  94      31  LOAD_FAST             2  'string_id_int'
          34  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `SLICE+2' instruction at offset 9


def get_npk_flist_info(nx_open_npk, npk_name):
    flist_file_index = get_patch_npk_flist_file_id(npk_name)
    flist_data = nx_open_npk.get_file_by_id(flist_file_index)
    flist_data = six.ensure_str(flist_data)
    if flist_data is None:
        return ({}, False)
    else:
        flist_dict = {}
        for line in flist_data.splitlines():
            if not line:
                continue
            info = line.split('\t')
            flist_dict[int(info[0])] = info

        return (flist_dict, True)


def verify_ext_patch_npk():
    root_dir = get_ext_patch_npk_dir()
    info_path = get_ext_patch_npk_info_file_path()
    if not os.path.exists(info_path):
        return True
    with open(info_path, 'rb') as tmp_file:
        info_data = tmp_file.read()
        info = json.loads(zlib.decompress(info_data))
        for npk_name in info:
            npk_path = os.path.join(root_dir, npk_name)
            record_size = int(info[npk_name].get('size', 0))
            if os.path.exists(npk_path):
                real_size = os.path.getsize(npk_path)
                if int(real_size) != record_size:
                    print('[verify_ext_patch_npk] size not match:{} {} {}'.format(npk_name, record_size, real_size))
                    return False
            else:
                print('[verify_ext_patch_npk] npk:{} recorded but not exist'.format(npk_name))
                return False

    return True


def _insert_ext_patch_npk():
    root_dir = get_ext_patch_npk_dir()
    ret, npk_config = get_saved_ext_patch_npk_info()
    if not ret:
        return False
    if not npk_config:
        return True
    all_res_name_lst = set()
    for npk_name in npk_config:
        npk_path = os.path.join(root_dir, npk_name)
        record_size = int(npk_config[npk_name].get('size', -1))
        if os.path.exists(npk_path):
            real_size = os.path.getsize(npk_path)
            if int(real_size) != record_size:
                print('[ERROR] [ext_patch_npk] [insert] size not match:{} {} {}'.format(npk_name, record_size, real_size))
                return False
        else:
            print('[ERROR] [ext_patch_npk] [insert] npk:{} recorded but not exist'.format(npk_name))
            return False
        all_res_name_lst.add(npk_name)

    if C_file.del_fileloader_by_tag(EXT_LOADER_TAG) < 0:
        return False
    for npk_name in all_res_name_lst:
        res_npk_path = os.path.join(root_dir, npk_name)
        ret_code = C_file.insert_res_npk_loader(res_npk_path[:-4], EXT_LOADER_TAG, 0, 1)
        if ret_code < 0:
            print('[ERROR] [ext_patch_npk] insert res npk:{} loader failed, ret_code:{}'.format(npk_name, ret_code))
            return False
        print('[ext_patch_npk] insert rest npk loader success:{}'.format(res_npk_path))

    return True


def insert_ext_npk_loader():
    try:
        ret = _insert_ext_patch_npk()
    except Exception as e:
        print('[EXCEPT] [ext_patch_npk] insert except:{}'.format(str(e)))
        ret = False

    if not ret:
        try:
            C_file.del_fileloader_by_tag(EXT_LOADER_TAG)
        except Exception as e:
            print('[EXCEPT] [ext_patch_npk] del file loader except:{}'.format(str(e)))

    return ret