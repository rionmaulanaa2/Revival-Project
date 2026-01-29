# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/dctool/scenetypecfg.py
from __future__ import absolute_import
from common.platform.dctool import interface
SCENE_INFO = {'DownloadServerListFailed': (3, 'get_download_serverlist_failed_dict'),
   'LoginFailed': (4, 'get_login_failed_dict'),
   'Disconnect': (5, 'get_disconnect_dict'),
   'Normal': (11, 'get_normal_dict'),
   'DownloadServerListSuccess': (33, 'get_download_serverlist_success_dict'),
   'LoginSuccess': (34, 'get_login_success_dict'),
   'Reconnect': (35, 'get_reconnect_dict')
   }

def get_default_dict(scene_type):
    res_dict = {}
    res_dict['user_id'] = interface.get_user_id()
    res_dict['user_name'] = interface.get_user_name()
    res_dict['Scene'] = scene_type
    res_dict['ProductName'] = interface.get_project_id()
    res_dict['channel_name'] = interface.get_channel_name()
    if interface.is_tw_package() or interface.is_global_package():
        res_dict['region'] = '2'
    return res_dict


def get_download_serverlist_failed_dict--- This code section failed: ---

  37       0  BUILD_MAP_0           0 
           3  STORE_FAST            0  'res_dict'

  38       6  LOAD_GLOBAL           0  'interface'
           9  LOAD_ATTR             1  'get_serverlist_URL'
          12  CALL_FUNCTION_0       0 
          15  CALL_FUNCTION_1       1 
          18  STORE_SUBSCR     

  39      19  LOAD_GLOBAL           0  'interface'
          22  LOAD_ATTR             2  'get_serverlist_http_code'
          25  CALL_FUNCTION_0       0 
          28  CALL_FUNCTION_2       2 
          31  STORE_SUBSCR     

  40      32  LOAD_GLOBAL           0  'interface'
          35  LOAD_ATTR             3  'get_serverlist_error_log'
          38  CALL_FUNCTION_0       0 
          41  CALL_FUNCTION_3       3 
          44  STORE_SUBSCR     

  41      45  LOAD_FAST             0  'res_dict'
          48  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 15


def get_login_failed_dict(err_code=None, error_log=None):
    res_dict = {}
    res_dict['group_id'] = interface.get_group_id()
    res_dict['server_name'] = interface.get_server_name()
    res_dict['server_ip'] = interface.get_server_ip()
    res_dict['server_port'] = interface.get_server_port()
    if err_code is not None:
        res_dict['http_code'] = err_code
    if error_log is not None:
        res_dict['error_log'] = error_log
    return res_dict


def get_disconnect_dict--- This code section failed: ---

  58       0  BUILD_MAP_0           0 
           3  STORE_FAST            0  'res_dict'

  59       6  LOAD_GLOBAL           0  'interface'
           9  LOAD_ATTR             1  'get_group_id'
          12  CALL_FUNCTION_0       0 
          15  CALL_FUNCTION_1       1 
          18  STORE_SUBSCR     

  60      19  LOAD_GLOBAL           0  'interface'
          22  LOAD_ATTR             2  'get_server_name'
          25  CALL_FUNCTION_0       0 
          28  CALL_FUNCTION_2       2 
          31  STORE_SUBSCR     

  61      32  LOAD_GLOBAL           0  'interface'
          35  LOAD_ATTR             3  'get_server_ip'
          38  CALL_FUNCTION_0       0 
          41  CALL_FUNCTION_3       3 
          44  STORE_SUBSCR     

  62      45  LOAD_GLOBAL           0  'interface'
          48  LOAD_ATTR             4  'get_server_port'
          51  CALL_FUNCTION_0       0 
          54  CALL_FUNCTION_4       4 
          57  STORE_SUBSCR     

  63      58  LOAD_FAST             0  'res_dict'
          61  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 15


def get_normal_dict(is_initiative=False):
    res_dict = {}
    res_dict['group_id'] = interface.get_group_id()
    res_dict['server_name'] = interface.get_server_name()
    res_dict['server_ip'] = interface.get_server_ip()
    res_dict['server_port'] = interface.get_server_port()
    return res_dict


def get_download_serverlist_success_dict--- This code section failed: ---

  76       0  BUILD_MAP_0           0 
           3  STORE_FAST            0  'res_dict'

  77       6  LOAD_GLOBAL           0  'interface'
           9  LOAD_ATTR             1  'get_serverlist_URL'
          12  CALL_FUNCTION_0       0 
          15  CALL_FUNCTION_1       1 
          18  STORE_SUBSCR     

  78      19  LOAD_GLOBAL           0  'interface'
          22  LOAD_ATTR             2  'get_serverlist_dl_speed'
          25  CALL_FUNCTION_0       0 
          28  CALL_FUNCTION_2       2 
          31  STORE_SUBSCR     

  79      32  LOAD_GLOBAL           0  'interface'
          35  LOAD_ATTR             3  'get_serverlist_time_cost'
          38  CALL_FUNCTION_0       0 
          41  CALL_FUNCTION_3       3 
          44  STORE_SUBSCR     

  80      45  LOAD_GLOBAL           0  'interface'
          48  LOAD_ATTR             4  'get_serverlist_http_code'
          51  CALL_FUNCTION_0       0 
          54  CALL_FUNCTION_4       4 
          57  STORE_SUBSCR     

  81      58  LOAD_FAST             0  'res_dict'
          61  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 15


def get_login_success_dict(time_cost=5):
    res_dict = {}
    res_dict['server_name'] = interface.get_server_name()
    res_dict['server_ip'] = interface.get_server_ip()
    res_dict['server_port'] = interface.get_server_port()
    res_dict['time_cost'] = str(time_cost)
    res_dict['http_code'] = 1
    return res_dict


def get_reconnect_dict--- This code section failed: ---

  95       0  BUILD_MAP_0           0 
           3  STORE_FAST            0  'res_dict'

  96       6  LOAD_GLOBAL           0  'interface'
           9  LOAD_ATTR             1  'get_reconnect_stage'
          12  CALL_FUNCTION_0       0 
          15  CALL_FUNCTION_1       1 
          18  STORE_SUBSCR     

  97      19  LOAD_GLOBAL           0  'interface'
          22  LOAD_ATTR             2  'get_reconnect_error_log'
          25  CALL_FUNCTION_0       0 
          28  CALL_FUNCTION_2       2 
          31  STORE_SUBSCR     

  98      32  LOAD_GLOBAL           0  'interface'
          35  LOAD_ATTR             3  'get_server_name'
          38  CALL_FUNCTION_0       0 
          41  CALL_FUNCTION_3       3 
          44  STORE_SUBSCR     

  99      45  LOAD_GLOBAL           0  'interface'
          48  LOAD_ATTR             4  'get_server_ip'
          51  CALL_FUNCTION_0       0 
          54  CALL_FUNCTION_4       4 
          57  STORE_SUBSCR     

 100      58  LOAD_GLOBAL           0  'interface'
          61  LOAD_ATTR             5  'get_server_port'
          64  CALL_FUNCTION_0       0 
          67  CALL_FUNCTION_5       5 
          70  STORE_SUBSCR     

 101      71  LOAD_FAST             0  'res_dict'
          74  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 15