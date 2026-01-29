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

class OrbitHelper(Singleton):

    def init(self):
        self.download_request_list = []

    def add_request(self, url, filename, callback):
        self.download_request_list.append([WeakMethod2(callback), url, filename])
        if len(self.download_request_list) == 1:
            self.execute_downloader()

    def execute_downloader(self):
        callback, url, filename = self.download_request_list[0]
        download_single_file_by_orbit(url, filename, self.on_orbit_download_callback)

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

  82       0  LOAD_GLOBAL           0  'get_orbit_temp_file_path'
           3  LOAD_FAST             1  'filename'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            3  'file_path'

  83      12  LOAD_GLOBAL           1  'interface'
          15  LOAD_ATTR             2  'is_tw_package'
          18  CALL_FUNCTION_0       0 
          21  POP_JUMP_IF_FALSE    33  'to 33'

  84      24  LOAD_CONST            1  2
          27  STORE_FAST            4  'oversea'
          30  JUMP_FORWARD         27  'to 60'

  85      33  LOAD_GLOBAL           1  'interface'
          36  LOAD_ATTR             3  'is_global_package'
          39  CALL_FUNCTION_0       0 
          42  POP_JUMP_IF_FALSE    54  'to 54'

  86      45  LOAD_CONST            1  2
          48  STORE_FAST            4  'oversea'
          51  JUMP_FORWARD          6  'to 60'

  88      54  LOAD_CONST            2  ''
          57  STORE_FAST            4  'oversea'
        60_0  COME_FROM                '51'
        60_1  COME_FROM                '30'

  89      60  BUILD_MAP_4           4 

  90      63  LOAD_GLOBAL           4  'str'
          66  LOAD_GLOBAL           5  'int'
          69  LOAD_GLOBAL           6  'time'
          72  LOAD_ATTR             6  'time'
          75  CALL_FUNCTION_0       0 
          78  CALL_FUNCTION_1       1 
          81  CALL_FUNCTION_1       1 
          84  LOAD_CONST            3  'downloadid'
          87  STORE_MAP        

  91      88  LOAD_GLOBAL           7  'is_ip_addr'
          91  LOAD_FAST             0  'url'
          94  CALL_FUNCTION_1       1 
          97  POP_JUMP_IF_FALSE   106  'to 106'
         100  LOAD_CONST            4  'true'
         103  JUMP_FORWARD          3  'to 109'
         106  LOAD_CONST            5  'false'
       109_0  COME_FROM                '103'
         109  LOAD_CONST            6  'notusecdn'
         112  STORE_MAP        

  92     113  LOAD_FAST             4  'oversea'
         116  LOAD_CONST            7  'oversea'
         119  STORE_MAP        

  94     120  BUILD_MAP_4           4 

  95     123  BUILD_MAP_8           8 
         126  STORE_MAP        

  96     127  LOAD_FAST             3  'file_path'
         130  LOAD_CONST            9  'filepath'
         133  STORE_MAP        

  97     134  LOAD_CONST            2  ''
         137  LOAD_CONST           10  'size'
         140  STORE_MAP        

  98     141  LOAD_CONST           11  'NotMD5'
         144  LOAD_CONST           12  'md5'
         147  STORE_MAP        
         148  BUILD_LIST_1          1 
         151  LOAD_CONST           13  'downfile'
         154  STORE_MAP        
         155  STORE_FAST            5  'start_download_json'

 102     158  LOAD_FAST             5  'start_download_json'
         161  LOAD_ATTR             8  'update'
         164  LOAD_GLOBAL           9  'ORBIT_COMMON_CONFIG'
         167  CALL_FUNCTION_1       1 
         170  POP_TOP          

 103     171  LOAD_GLOBAL          10  'global_data'
         174  LOAD_ATTR            11  'channel'
         177  LOAD_ATTR            12  'is_steam_channel'
         180  CALL_FUNCTION_0       0 
         183  POP_JUMP_IF_FALSE   326  'to 326'

 104     186  LOAD_CONST           14  'g93'
         189  LOAD_FAST             5  'start_download_json'
         192  LOAD_CONST           15  'projectid'
         195  STORE_SUBSCR     

 105     196  LOAD_GLOBAL          10  'global_data'
         199  LOAD_ATTR            13  'ui_mgr'
         202  LOAD_ATTR            14  'read_lang_conf_from_setting'
         205  CALL_FUNCTION_0       0 
         208  STORE_FAST            6  'local_language_code'

 106     211  LOAD_FAST             6  'local_language_code'
         214  LOAD_GLOBAL          15  'lang_data'
         217  LOAD_ATTR            16  'LANG_CN'
         220  COMPARE_OP            2  '=='
         223  POP_JUMP_IF_FALSE   281  'to 281'

 107     226  LOAD_CONST            2  ''
         229  LOAD_FAST             5  'start_download_json'
         232  LOAD_CONST            7  'oversea'
         235  STORE_SUBSCR     

 108     236  LOAD_FAST             5  'start_download_json'
         239  LOAD_CONST           13  'downfile'
         242  BINARY_SUBSCR    
         243  LOAD_CONST            2  ''
         246  BINARY_SUBSCR    
         247  LOAD_CONST            8  'targeturl'
         250  BINARY_SUBSCR    
         251  LOAD_ATTR            17  'replace'
         254  LOAD_CONST           16  'easebar.com'
         257  LOAD_CONST           17  'netease.com'
         260  CALL_FUNCTION_2       2 
         263  LOAD_FAST             5  'start_download_json'
         266  LOAD_CONST           13  'downfile'
         269  BINARY_SUBSCR    
         270  LOAD_CONST            2  ''
         273  BINARY_SUBSCR    
         274  LOAD_CONST            8  'targeturl'
         277  STORE_SUBSCR     
         278  JUMP_ABSOLUTE       326  'to 326'

 110     281  LOAD_FAST             5  'start_download_json'
         284  LOAD_CONST           13  'downfile'
         287  BINARY_SUBSCR    
         288  LOAD_CONST            2  ''
         291  BINARY_SUBSCR    
         292  LOAD_CONST            8  'targeturl'
         295  BINARY_SUBSCR    
         296  LOAD_ATTR            17  'replace'
         299  LOAD_CONST           17  'netease.com'
         302  LOAD_CONST           16  'easebar.com'
         305  CALL_FUNCTION_2       2 
         308  LOAD_FAST             5  'start_download_json'
         311  LOAD_CONST           13  'downfile'
         314  BINARY_SUBSCR    
         315  LOAD_CONST            2  ''
         318  BINARY_SUBSCR    
         319  LOAD_CONST            8  'targeturl'
         322  STORE_SUBSCR     
         323  JUMP_FORWARD          0  'to 326'
       326_0  COME_FROM                '323'

 112     326  LOAD_GLOBAL          18  'social'
         329  LOAD_ATTR            19  'get_channel'
         332  CALL_FUNCTION_0       0 
         335  STORE_FAST            7  'channel'

 113     338  LOAD_GLOBAL          20  'partial'
         341  LOAD_GLOBAL          21  'single_file_orbit_callback_wrap'
         344  LOAD_FAST             1  'filename'
         347  LOAD_FAST             2  'callback'
         350  CALL_FUNCTION_3       3 
         353  STORE_FAST            8  'download_file_callback'

 114     356  LOAD_GLOBAL          22  'json'
         359  LOAD_ATTR            23  'dumps'
         362  LOAD_FAST             5  'start_download_json'
         365  CALL_FUNCTION_1       1 
         368  STORE_FAST            9  'orbit_parm_str'

 116     371  LOAD_FAST             7  'channel'
         374  LOAD_ATTR            24  'start_download'
         377  LOAD_FAST             9  'orbit_parm_str'
         380  LOAD_FAST             8  'download_file_callback'
         383  CALL_FUNCTION_2       2 
         386  POP_TOP          

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