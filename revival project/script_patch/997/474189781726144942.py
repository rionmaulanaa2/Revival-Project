# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/pn_utils.py
from __future__ import absolute_import
from __future__ import print_function
import os
import zlib
import json
import game3d
import six
PATCH_NPK_FOLDER = 'patch_npk'
PATCH_NPK_INFO_FILENAME = 'patch_npk_info.config'
DRFP_ERROR_CHANNEL = '[PATCH_NPK_ERROR]'
PATCH_NPK_DIR = None
PATCH_NPK_INFO_FILE_PATH = None
MAX_NPK_SIZE = 209715200.0
RES_NPK_SUBFIX_PATTERN = 'p_res_{}.npk'
TEMP_RES_NPK_SUBFIX_PATTERN = 'p_res_{}_tmp.npk'
SCRIPT_NPK_SUBFIX_PATTERN = 'p_script_{}.npk'
TEMP_SCRIPT_NPK_SUBFIX_PATTERN = 'p_script_{}_tmp.npk'
PN_SCRIPT_PREFIX = 'p_script'
PN_SCRIPT_NAME = 'p_script.npk'

def get_nx_dir():
    doc_dir = game3d.get_doc_dir()
    if game3d.get_platform() == game3d.PLATFORM_WIN32:
        doc_dir = os.path.dirname(doc_dir)
    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        doc_dir = os.path.dirname(doc_dir)
    return doc_dir


def get_patch_npk_dir():
    global PATCH_NPK_DIR
    if PATCH_NPK_DIR is None:
        PATCH_NPK_DIR = os.path.join(get_nx_dir(), PATCH_NPK_FOLDER)
    return PATCH_NPK_DIR


def get_patch_npk_info_file_path():
    global PATCH_NPK_INFO_FILE_PATH
    if PATCH_NPK_INFO_FILE_PATH is None:
        npk_dir = get_patch_npk_dir()
        PATCH_NPK_INFO_FILE_PATH = os.path.join(npk_dir, PATCH_NPK_INFO_FILENAME)
    return PATCH_NPK_INFO_FILE_PATH


def get_saved_patch_npk_info--- This code section failed: ---

  61       0  LOAD_GLOBAL           0  'get_patch_npk_info_file_path'
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


def save_patch_npk_info(info_dict):
    info_path = get_patch_npk_info_file_path()
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

  93       0  LOAD_CONST            1  '{}_flist.txt'
           3  LOAD_ATTR             0  'format'
           6  LOAD_ATTR             2  'calc_filename_hash64'
           9  SLICE+2          
          10  CALL_FUNCTION_1       1 
          13  STORE_FAST            1  'relative_path'

  94      16  LOAD_GLOBAL           1  'game3d'
          19  LOAD_ATTR             2  'calc_filename_hash64'
          22  LOAD_FAST             1  'relative_path'
          25  CALL_FUNCTION_1       1 
          28  STORE_FAST            2  'string_id_int'

  95      31  LOAD_FAST             2  'string_id_int'
          34  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `SLICE+2' instruction at offset 9


def get_npk_flist_info(nx_open_npk, npk_name):
    flist_file_index = get_patch_npk_flist_file_id(npk_name)
    flist_data = nx_open_npk.get_file_by_id(flist_file_index)
    if flist_data is None:
        return ({}, False)
    else:
        flist_data = six.ensure_str(flist_data)
        flist_dict = {}
        for line in flist_data.splitlines():
            if not line:
                continue
            info = line.split('\t')
            flist_dict[int(info[0])] = info

        return (flist_dict, True)