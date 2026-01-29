# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/orbit_utils.py
from __future__ import absolute_import
import time
from common.utils.path import get_neox_dir
import os
from functools import partial
import social
import json
import game3d
import re
from common.platform.dctool import interface
from common.framework import WeakMethod2, Singleton
from logic.gcommon.common_const import lang_data
ORBIT_NETWORK_LOST = '__DOWNLOAD_NETWORK_LOST__'
ORBIT_CLEAN_CACHE = '__DOWNLOAD_CLEAN_CACHE__'
ORBIT_DNS_RESOLVED = '__DOWNLOAD_DNS_RESOLVED__'
ORBIT_CONFIG = '__DOWNLOAD_CONFIG__'
ORBIT_TEMP_FOLDER_NAME = 'orbit_temp'
IP_PATTERN = '(\\d+\\.\\d+\\.\\d+\\.\\d+)'
ORBIT_COMMON_CONFIG = {'methodId': 'download',
   'projectid': str(interface.get_project_id()),
   'wifionly': 'false',
   'logopen': 'false',
   'threadnum': '10',
   'isrenew': 'true'
   }
try:
    import game3d
    ORBIT_V3 = game3d.is_feature_ready('suport_orbit_v3')
except AttributeError:
    ORBIT_V3 = False

class OrbitHelper(Singleton):

    def init(self):
        self.download_request_list = []

    def add_request(self, url, filename, callback, is_patch=False):
        dtype = 'patch' if is_patch else 'list'
        if url.startswith('http://'):
            dtype = 'other'
        self.download_request_list.append([WeakMethod2(callback), url, filename, dtype])
        if len(self.download_request_list) == 1:
            self.execute_downloader()

    def execute_downloader(self):
        callback, url, filename, dtype = self.download_request_list[0]
        download_single_file_by_orbit(url, filename, self.on_orbit_download_callback, dtype)

    def on_orbit_download_callback(self, data):
        if not self.download_request_list:
            return
        self.download_request_list[0][0](data)
        self.download_request_list = self.download_request_list[1:]
        if len(self.download_request_list) > 0:
            self.execute_downloader()


def orbit_result_parser(filename, code):
    if filename == ORBIT_NETWORK_LOST:
        return True
    if filename == ORBIT_CONFIG and code != 0:
        return True
    return False


def get_orbit_temp_file_path(filename):
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        return os.path.join(ORBIT_TEMP_FOLDER_NAME, filename)
    else:
        return abs_orbit_temp_file_path(filename).replace('\\', '/')


def get_rel_temp_file_path(filename):
    return os.path.join(ORBIT_TEMP_FOLDER_NAME, filename).replace('\\', '/')


def abs_orbit_temp_file_path(filename):
    temp_flist_path = os.path.join(ORBIT_TEMP_FOLDER_NAME, filename)
    return os.path.join(get_neox_dir(), temp_flist_path).replace('\\', '/')


def download_single_file_by_orbit--- This code section failed: ---

  91       0  LOAD_GLOBAL           0  'get_orbit_temp_file_path'
           3  LOAD_FAST             1  'filename'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            4  'file_path'

  92      12  LOAD_GLOBAL           1  'interface'
          15  LOAD_ATTR             2  'is_tw_package'
          18  CALL_FUNCTION_0       0 
          21  POP_JUMP_IF_FALSE    33  'to 33'

  93      24  LOAD_CONST            1  2
          27  STORE_FAST            5  'oversea'
          30  JUMP_FORWARD         27  'to 60'

  94      33  LOAD_GLOBAL           1  'interface'
          36  LOAD_ATTR             3  'is_global_package'
          39  CALL_FUNCTION_0       0 
          42  POP_JUMP_IF_FALSE    54  'to 54'

  95      45  LOAD_CONST            1  2
          48  STORE_FAST            5  'oversea'
          51  JUMP_FORWARD          6  'to 60'

  97      54  LOAD_CONST            2  ''
          57  STORE_FAST            5  'oversea'
        60_0  COME_FROM                '51'
        60_1  COME_FROM                '30'

  98      60  BUILD_MAP_4           4 

  99      63  LOAD_GLOBAL           4  'str'
          66  LOAD_GLOBAL           5  'int'
          69  LOAD_GLOBAL           6  'time'
          72  LOAD_ATTR             6  'time'
          75  CALL_FUNCTION_0       0 
          78  CALL_FUNCTION_1       1 
          81  CALL_FUNCTION_1       1 
          84  LOAD_CONST            3  'downloadid'
          87  STORE_MAP        

 100      88  LOAD_GLOBAL           7  'is_ip_addr'
          91  LOAD_FAST             0  'url'
          94  CALL_FUNCTION_1       1 
          97  POP_JUMP_IF_FALSE   106  'to 106'
         100  LOAD_CONST            4  'true'
         103  JUMP_FORWARD          3  'to 109'
         106  LOAD_CONST            5  'false'
       109_0  COME_FROM                '103'
         109  LOAD_CONST            6  'notusecdn'
         112  STORE_MAP        

 101     113  LOAD_FAST             5  'oversea'
         116  LOAD_CONST            7  'oversea'
         119  STORE_MAP        

 103     120  BUILD_MAP_4           4 

 104     123  BUILD_MAP_8           8 
         126  STORE_MAP        

 105     127  LOAD_FAST             4  'file_path'
         130  LOAD_CONST            9  'filepath'
         133  STORE_MAP        

 106     134  LOAD_CONST            2  ''
         137  LOAD_CONST           10  'size'
         140  STORE_MAP        

 107     141  LOAD_CONST           11  'NotMD5'
         144  LOAD_CONST           12  'md5'
         147  STORE_MAP        
         148  BUILD_LIST_1          1 
         151  LOAD_CONST           13  'downfile'
         154  STORE_MAP        
         155  STORE_FAST            6  'start_download_json'

 111     158  LOAD_GLOBAL           8  'ORBIT_V3'
         161  POP_JUMP_IF_FALSE   215  'to 215'

 112     164  LOAD_FAST             6  'start_download_json'
         167  LOAD_ATTR             9  'pop'
         170  LOAD_CONST            6  'notusecdn'
         173  CALL_FUNCTION_1       1 
         176  POP_TOP          

 113     177  LOAD_FAST             3  'dtype'
         180  LOAD_FAST             6  'start_download_json'
         183  LOAD_CONST           14  'type'
         186  STORE_SUBSCR     

 114     187  LOAD_FAST             3  'dtype'
         190  LOAD_CONST           15  'list'
         193  COMPARE_OP            2  '=='
         196  POP_JUMP_IF_FALSE   215  'to 215'

 115     199  LOAD_CONST           16  9
         202  LOAD_FAST             6  'start_download_json'
         205  LOAD_CONST           17  'priority'
         208  STORE_SUBSCR     
         209  JUMP_ABSOLUTE       215  'to 215'
         212  JUMP_FORWARD          0  'to 215'
       215_0  COME_FROM                '212'

 117     215  LOAD_FAST             6  'start_download_json'
         218  LOAD_ATTR            10  'update'
         221  LOAD_GLOBAL          11  'ORBIT_COMMON_CONFIG'
         224  CALL_FUNCTION_1       1 
         227  POP_TOP          

 118     228  LOAD_GLOBAL          12  'global_data'
         231  LOAD_ATTR            13  'channel'
         234  LOAD_ATTR            14  'is_steam_channel'
         237  CALL_FUNCTION_0       0 
         240  POP_JUMP_IF_FALSE   383  'to 383'

 119     243  LOAD_CONST           18  'g93'
         246  LOAD_FAST             6  'start_download_json'
         249  LOAD_CONST           19  'projectid'
         252  STORE_SUBSCR     

 120     253  LOAD_GLOBAL          12  'global_data'
         256  LOAD_ATTR            15  'ui_mgr'
         259  LOAD_ATTR            16  'read_lang_conf_from_setting'
         262  CALL_FUNCTION_0       0 
         265  STORE_FAST            7  'local_language_code'

 121     268  LOAD_FAST             7  'local_language_code'
         271  LOAD_GLOBAL          17  'lang_data'
         274  LOAD_ATTR            18  'LANG_CN'
         277  COMPARE_OP            2  '=='
         280  POP_JUMP_IF_FALSE   338  'to 338'

 122     283  LOAD_CONST            2  ''
         286  LOAD_FAST             6  'start_download_json'
         289  LOAD_CONST            7  'oversea'
         292  STORE_SUBSCR     

 123     293  LOAD_FAST             6  'start_download_json'
         296  LOAD_CONST           13  'downfile'
         299  BINARY_SUBSCR    
         300  LOAD_CONST            2  ''
         303  BINARY_SUBSCR    
         304  LOAD_CONST            8  'targeturl'
         307  BINARY_SUBSCR    
         308  LOAD_ATTR            19  'replace'
         311  LOAD_CONST           20  'easebar.com'
         314  LOAD_CONST           21  'netease.com'
         317  CALL_FUNCTION_2       2 
         320  LOAD_FAST             6  'start_download_json'
         323  LOAD_CONST           13  'downfile'
         326  BINARY_SUBSCR    
         327  LOAD_CONST            2  ''
         330  BINARY_SUBSCR    
         331  LOAD_CONST            8  'targeturl'
         334  STORE_SUBSCR     
         335  JUMP_ABSOLUTE       383  'to 383'

 125     338  LOAD_FAST             6  'start_download_json'
         341  LOAD_CONST           13  'downfile'
         344  BINARY_SUBSCR    
         345  LOAD_CONST            2  ''
         348  BINARY_SUBSCR    
         349  LOAD_CONST            8  'targeturl'
         352  BINARY_SUBSCR    
         353  LOAD_ATTR            19  'replace'
         356  LOAD_CONST           21  'netease.com'
         359  LOAD_CONST           20  'easebar.com'
         362  CALL_FUNCTION_2       2 
         365  LOAD_FAST             6  'start_download_json'
         368  LOAD_CONST           13  'downfile'
         371  BINARY_SUBSCR    
         372  LOAD_CONST            2  ''
         375  BINARY_SUBSCR    
         376  LOAD_CONST            8  'targeturl'
         379  STORE_SUBSCR     
         380  JUMP_FORWARD          0  'to 383'
       383_0  COME_FROM                '380'

 127     383  LOAD_GLOBAL          20  'social'
         386  LOAD_ATTR            21  'get_channel'
         389  CALL_FUNCTION_0       0 
         392  STORE_FAST            8  'channel'

 128     395  LOAD_GLOBAL          22  'partial'
         398  LOAD_GLOBAL          23  'single_file_orbit_callback_wrap'
         401  LOAD_FAST             1  'filename'
         404  LOAD_FAST             2  'callback'
         407  CALL_FUNCTION_3       3 
         410  STORE_FAST            9  'download_file_callback'

 129     413  LOAD_GLOBAL          24  'json'
         416  LOAD_ATTR            25  'dumps'
         419  LOAD_FAST             6  'start_download_json'
         422  CALL_FUNCTION_1       1 
         425  STORE_FAST           10  'orbit_parm_str'

 131     428  LOAD_FAST             8  'channel'
         431  LOAD_ATTR            26  'start_download'
         434  LOAD_FAST            10  'orbit_parm_str'
         437  LOAD_FAST             9  'download_file_callback'
         440  CALL_FUNCTION_2       2 
         443  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 126


def single_file_orbit_callback_wrap(download_filename, callback, data, result, complete):
    json_data = json.loads(data)
    filename = json_data.get('filename', '')
    file_path = json_data.get('filepath', '').replace('\\', '/')
    code = json_data.get('code', -1)
    download_failed = orbit_result_parser(filename, code)
    temp_file_path = get_orbit_temp_file_path(download_filename)
    abs_temp_file_path = abs_orbit_temp_file_path(download_filename)
    rel_temp_file_path = get_rel_temp_file_path(download_filename)
    if filename == temp_file_path and code != 0:
        download_failed = True
    if download_failed:
        orbit_stop_downloader()
        if callback and callable(callback):
            callback(None)
        return
    else:
        if filename == temp_file_path or file_path == temp_file_path:
            file_data = None
            try:
                with open(abs_temp_file_path, 'rb') as temp_reader:
                    file_data = temp_reader.read()
                os.remove(abs_temp_file_path)
            except:
                try:
                    with open(rel_temp_file_path, 'rb') as temp_reader:
                        file_data = temp_reader.read()
                    os.remove(rel_temp_file_path)
                except:
                    file_data = ''

            orbit_stop_downloader()
            if callback and callable(callback):
                callback(file_data)
        return


def orbit_stop_downloader():
    pass


def is_ip_addr(url):
    ret = re.search(IP_PATTERN, url)
    return bool(ret)