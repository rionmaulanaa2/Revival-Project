# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/path.py
from __future__ import absolute_import
from __future__ import print_function
import C_file
from cocosui import cc
import game3d
import os
PATH_UI_RES = 'uires'
QUALITY_FILE_NAME = 'quality.config'
res_plist_map = {}
SCRIPT_PATCH_DIRNAME = 'script_patch'
RES_PATCH_DIRNAME = 'res_patch'
LOG_STATE_FILEPATH = 'log_state.txt'
CACERT_PATH = '{}/cacert.pem'.format(game3d.get_doc_dir())

def get_engine_version():
    return game3d.get_engine_version()


def get_engine_svn():
    return game3d.get_engine_svn_version()


def get_neox_dir():
    doc_dir = game3d.get_doc_dir()
    if game3d.get_platform() == game3d.PLATFORM_WIN32:
        doc_dir = os.path.dirname(doc_dir)
    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        doc_dir = os.path.dirname(doc_dir)
    return doc_dir


def get_share_img_weibo_dir():
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        doc_dir = game3d.get_doc_dir()
        app_name = game3d.get_app_name()
        index = doc_dir.find(app_name + '/files/')
        if index >= 0:
            weibo_dir = doc_dir[:index + len(app_name + '/files/')]
            return weibo_dir
        else:
            return None

    else:
        return None
    return None


def get_share_img_na_dir():
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        doc_dir = game3d.get_doc_dir()
        app_name = game3d.get_app_name()
        index = doc_dir.find(app_name)
        if index >= 0:
            na_dir = doc_dir[:index] + app_name + '/files/'
            return na_dir
        else:
            return get_neox_dir()

    else:
        return get_neox_dir()


def get_res_patch_path():
    return os.path.join(get_neox_dir(), RES_PATCH_DIRNAME)


def get_script_patch_path():
    return os.path.join(get_neox_dir(), SCRIPT_PATCH_DIRNAME)


def get_log_state_path():
    return os.path.join(get_neox_dir(), LOG_STATE_FILEPATH)


def init_plist_map():
    res_plist_map.clear()
    try:
        data = C_file.get_res_file('uires/plists/filelist.txt', '')
    except:
        pass

    try:
        fu = cc.FileUtils.getInstance()
        if hasattr(fu, 'clearPlistPathMap'):
            fu.clearPlistPathMap()
        sppwf_enable = hasattr(fu, 'setPlistPathWithFile')
        lines = data.splitlines()
        for line in lines:
            if not line:
                continue
            path, conf = line.split(' ')
            if sppwf_enable:
                fu.setPlistPathWithFile(path, 'uires/plists/{}0.plist'.format(conf))
            path = path[4:]
            res_plist_map[path] = conf

    except:
        pass


def load_plist_from_respath(path):
    plist_path = res_plist_map.get(path)
    if not plist_path:
        return False
    plist_path = 'uires/plists/' + plist_path
    p0 = plist_path + '0.plist'
    cc.SpriteFrameCache.getInstance().addSpriteFrames(p0)
    p1 = plist_path + '1.plist'
    if C_file.find_res_file(p1, ''):
        cc.SpriteFrameCache.getInstance().addSpriteFrames(p1)
    return True


def find_res_from_plist(path):
    return path in res_plist_map


def get_uiconf_path(filename, parent=None):
    if parent is None:
        return 'uiconf/' + filename
    else:
        return 'uiconf/' + parent + '/' + filename
        return


def check_file_exist--- This code section failed: ---

 141       0  LOAD_GLOBAL           0  'C_file'
           3  LOAD_ATTR             1  'find_res_file'
           6  LOAD_ATTR             1  'find_res_file'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


def check_document_file_exist(relative_sys_path):
    abs_path = os.path.join(game3d.get_doc_dir(), relative_sys_path)
    return os.path.exists(abs_path)


def copy_res_file_to_document--- This code section failed: ---

 148       0  LOAD_GLOBAL           0  'check_file_exist'
           3  LOAD_FAST             0  'res_path'
           6  CALL_FUNCTION_1       1 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 149      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 152      16  LOAD_GLOBAL           1  'C_file'
          19  LOAD_ATTR             2  'get_res_file'
          22  LOAD_ATTR             1  'C_file'
          25  CALL_FUNCTION_2       2 
          28  STORE_FAST            2  'file_data'

 154      31  LOAD_FAST             2  'file_data'
          34  POP_JUMP_IF_TRUE     41  'to 41'

 155      37  LOAD_CONST            0  ''
          40  RETURN_END_IF    
        41_0  COME_FROM                '34'

 157      41  LOAD_GLOBAL           3  'os'
          44  LOAD_ATTR             4  'path'
          47  LOAD_ATTR             5  'join'
          50  LOAD_GLOBAL           6  'game3d'
          53  LOAD_ATTR             7  'get_doc_dir'
          56  CALL_FUNCTION_0       0 
          59  LOAD_FAST             1  'relative_sys_path'
          62  CALL_FUNCTION_2       2 
          65  STORE_FAST            3  'abs_path'

 158      68  LOAD_GLOBAL           3  'os'
          71  LOAD_ATTR             4  'path'
          74  LOAD_ATTR             8  'dirname'
          77  LOAD_FAST             3  'abs_path'
          80  CALL_FUNCTION_1       1 
          83  STORE_FAST            4  'dir_path'

 159      86  LOAD_GLOBAL           9  'print'
          89  LOAD_CONST            2  'test--copy_res_file_to_document--step2--res_path ='
          92  LOAD_CONST            3  '--abs_path ='
          95  LOAD_FAST             3  'abs_path'
          98  BUILD_TUPLE_4         4 
         101  CALL_FUNCTION_1       1 
         104  POP_TOP          

 160     105  LOAD_GLOBAL           3  'os'
         108  LOAD_ATTR             4  'path'
         111  LOAD_ATTR            10  'exists'
         114  LOAD_FAST             4  'dir_path'
         117  CALL_FUNCTION_1       1 
         120  POP_JUMP_IF_TRUE    139  'to 139'

 161     123  LOAD_GLOBAL           3  'os'
         126  LOAD_ATTR            11  'makedirs'
         129  LOAD_FAST             4  'dir_path'
         132  CALL_FUNCTION_1       1 
         135  POP_TOP          
         136  JUMP_FORWARD          0  'to 139'
       139_0  COME_FROM                '136'

 162     139  LOAD_GLOBAL          12  'open'
         142  LOAD_FAST             3  'abs_path'
         145  LOAD_CONST            4  'wb'
         148  CALL_FUNCTION_2       2 
         151  SETUP_WITH           20  'to 174'
         154  STORE_FAST            5  'f'

 163     157  LOAD_FAST             5  'f'
         160  LOAD_ATTR            13  'write'
         163  LOAD_FAST             2  'file_data'
         166  CALL_FUNCTION_1       1 
         169  POP_TOP          
         170  POP_BLOCK        
         171  LOAD_CONST            0  ''
       174_0  COME_FROM_WITH           '151'
         174  WITH_CLEANUP     
         175  END_FINALLY      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 25