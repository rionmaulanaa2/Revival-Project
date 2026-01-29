# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/revert.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import os
import shutil
import game3d
import threading
import render
import C_file
from patch import patch_path
from patch import patch_utils
from patch.patch_lang import get_patch_text_id
REVERTING = False
REVERTRING_FINISH = False
PREV_LOGIC = None
REVERT_FAIL_TIMES = 0
LOADER_TAG = 'patch_npk'
SCRIPT_LOADER_TAG = 'script_patch_npk'
EXT_LOADER_TAG = 'ext_patch_npk'
PHYSX_COOK_NPK_TAG = 'physx_cook_npk'

def remove_dir(base_dir, dir_name):
    ret = True
    try:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    except Exception as e:
        print('[revert] remove dir except:{}'.format(str(e)))
        ret = False

    return ret


def remove_file(base_dir, file_path):
    try:
        file_path = os.path.join(base_dir, file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print('[revert] remove file except:{}'.format(str(e)))
        return False

    if os.path.exists(file_path):
        return False
    return True


def remove_all_npks():
    doc_dir = patch_path.get_neox_dir()
    files = os.listdir(doc_dir)
    for file in files:
        if file.endswith('.npk'):
            try:
                os.remove(os.path.join(doc_dir, file))
            except Exception as e:
                patch_utils.send_script_error('remove npk %s error with exception %s' % (file, str(e)))


def remove_patch_npk--- This code section failed: ---

  73       0  SETUP_EXCEPT        113  'to 116'

  74       3  LOAD_GLOBAL           0  'os'
           6  LOAD_ATTR             1  'path'
           9  LOAD_ATTR             2  'join'
          12  LOAD_ATTR             1  'path'
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'patch_npk_dir'

  75      21  LOAD_GLOBAL           0  'os'
          24  LOAD_ATTR             1  'path'
          27  LOAD_ATTR             2  'join'
          30  LOAD_FAST             1  'patch_npk_dir'
          33  LOAD_CONST            2  'patch_npk_info.config'
          36  CALL_FUNCTION_2       2 
          39  STORE_FAST            2  'npk_info_dir'

  76      42  LOAD_GLOBAL           0  'os'
          45  LOAD_ATTR             1  'path'
          48  LOAD_ATTR             3  'exists'
          51  LOAD_FAST             2  'npk_info_dir'
          54  CALL_FUNCTION_1       1 
          57  POP_JUMP_IF_FALSE    86  'to 86'

  77      60  LOAD_GLOBAL           0  'os'
          63  LOAD_ATTR             4  'remove'
          66  LOAD_FAST             2  'npk_info_dir'
          69  CALL_FUNCTION_1       1 
          72  POP_TOP          

  78      73  LOAD_GLOBAL           5  'print'
          76  LOAD_CONST            3  '[revert] remove patch npk config done'
          79  CALL_FUNCTION_1       1 
          82  POP_TOP          
          83  JUMP_FORWARD          0  'to 86'
        86_0  COME_FROM                '83'

  79      86  LOAD_GLOBAL           6  'C_file'
          89  LOAD_ATTR             7  'del_fileloader_by_tag'
          92  LOAD_GLOBAL           8  'LOADER_TAG'
          95  CALL_FUNCTION_1       1 
          98  POP_TOP          

  80      99  LOAD_GLOBAL           6  'C_file'
         102  LOAD_ATTR             7  'del_fileloader_by_tag'
         105  LOAD_GLOBAL           9  'SCRIPT_LOADER_TAG'
         108  CALL_FUNCTION_1       1 
         111  POP_TOP          
         112  POP_BLOCK        
         113  JUMP_FORWARD         38  'to 154'
       116_0  COME_FROM                '0'

  81     116  DUP_TOP          
         117  LOAD_GLOBAL          10  'Exception'
         120  COMPARE_OP           10  'exception-match'
         123  POP_JUMP_IF_FALSE   153  'to 153'
         126  POP_TOP          
         127  STORE_FAST            3  'e'
         130  POP_TOP          

  82     131  LOAD_GLOBAL           5  'print'
         134  LOAD_CONST            4  '[revert] remove patch npk except:'
         137  LOAD_GLOBAL          11  'str'
         140  LOAD_FAST             3  'e'
         143  CALL_FUNCTION_1       1 
         146  CALL_FUNCTION_2       2 
         149  POP_TOP          
         150  JUMP_FORWARD          1  'to 154'
         153  END_FINALLY      
       154_0  COME_FROM                '153'
       154_1  COME_FROM                '113'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15


def remove_ext_patch_npk--- This code section failed: ---

  89       0  SETUP_EXCEPT        100  'to 103'

  90       3  LOAD_GLOBAL           0  'os'
           6  LOAD_ATTR             1  'path'
           9  LOAD_ATTR             2  'join'
          12  LOAD_ATTR             1  'path'
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'patch_npk_dir'

  91      21  LOAD_GLOBAL           0  'os'
          24  LOAD_ATTR             1  'path'
          27  LOAD_ATTR             2  'join'
          30  LOAD_FAST             1  'patch_npk_dir'
          33  LOAD_CONST            2  'ext_pn_info.config'
          36  CALL_FUNCTION_2       2 
          39  STORE_FAST            2  'npk_info_dir'

  92      42  LOAD_GLOBAL           0  'os'
          45  LOAD_ATTR             1  'path'
          48  LOAD_ATTR             3  'exists'
          51  LOAD_FAST             2  'npk_info_dir'
          54  CALL_FUNCTION_1       1 
          57  POP_JUMP_IF_FALSE    86  'to 86'

  93      60  LOAD_GLOBAL           0  'os'
          63  LOAD_ATTR             4  'remove'
          66  LOAD_FAST             2  'npk_info_dir'
          69  CALL_FUNCTION_1       1 
          72  POP_TOP          

  94      73  LOAD_GLOBAL           5  'print'
          76  LOAD_CONST            3  '[revert] remove patch npk config done'
          79  CALL_FUNCTION_1       1 
          82  POP_TOP          
          83  JUMP_FORWARD          0  'to 86'
        86_0  COME_FROM                '83'

  95      86  LOAD_GLOBAL           6  'C_file'
          89  LOAD_ATTR             7  'del_fileloader_by_tag'
          92  LOAD_GLOBAL           8  'EXT_LOADER_TAG'
          95  CALL_FUNCTION_1       1 
          98  POP_TOP          
          99  POP_BLOCK        
         100  JUMP_FORWARD         38  'to 141'
       103_0  COME_FROM                '0'

  96     103  DUP_TOP          
         104  LOAD_GLOBAL           9  'Exception'
         107  COMPARE_OP           10  'exception-match'
         110  POP_JUMP_IF_FALSE   140  'to 140'
         113  POP_TOP          
         114  STORE_FAST            3  'e'
         117  POP_TOP          

  97     118  LOAD_GLOBAL           5  'print'
         121  LOAD_CONST            4  '[revert] remove ext patch npk except:'
         124  LOAD_GLOBAL          10  'str'
         127  LOAD_FAST             3  'e'
         130  CALL_FUNCTION_1       1 
         133  CALL_FUNCTION_2       2 
         136  POP_TOP          
         137  JUMP_FORWARD          1  'to 141'
         140  END_FINALLY      
       141_0  COME_FROM                '140'
       141_1  COME_FROM                '100'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15


def remove_physx_cook_cache--- This code section failed: ---

 102       0  LOAD_GLOBAL           0  'remove_dir'
           3  LOAD_GLOBAL           1  'C_file'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            1  'ret'

 104      12  SETUP_EXCEPT         17  'to 32'

 105      15  LOAD_GLOBAL           1  'C_file'
          18  LOAD_ATTR             2  'del_fileloader_by_tag'
          21  LOAD_GLOBAL           3  'PHYSX_COOK_NPK_TAG'
          24  CALL_FUNCTION_1       1 
          27  POP_TOP          
          28  POP_BLOCK        
          29  JUMP_FORWARD         44  'to 76'
        32_0  COME_FROM                '12'

 106      32  DUP_TOP          
          33  LOAD_GLOBAL           4  'Exception'
          36  COMPARE_OP           10  'exception-match'
          39  POP_JUMP_IF_FALSE    75  'to 75'
          42  POP_TOP          
          43  STORE_FAST            2  'e'
          46  POP_TOP          

 107      47  LOAD_GLOBAL           5  'print'
          50  LOAD_CONST            2  '[revert] file system del physx except:{}'
          53  LOAD_ATTR             6  'format'
          56  LOAD_GLOBAL           7  'str'
          59  LOAD_FAST             2  'e'
          62  CALL_FUNCTION_1       1 
          65  CALL_FUNCTION_1       1 
          68  CALL_FUNCTION_1       1 
          71  POP_TOP          
          72  JUMP_FORWARD          1  'to 76'
          75  END_FINALLY      
        76_0  COME_FROM                '75'
        76_1  COME_FROM                '29'

 108      76  LOAD_FAST             1  'ret'
          79  LOAD_GLOBAL           0  'remove_dir'
          82  LOAD_GLOBAL           3  'PHYSX_COOK_NPK_TAG'
          85  CALL_FUNCTION_2       2 
          88  INPLACE_AND      
          89  STORE_FAST            1  'ret'

 109      92  LOAD_FAST             1  'ret'
          95  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def revert():
    global REVERTING
    REVERTING = True
    ret = True
    print('reverting game client')
    if game3d.get_platform() == game3d.PLATFORM_WIN32:
        dirname = os.path.dirname(game3d.get_doc_dir())
    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        dirname = os.path.dirname(game3d.get_doc_dir())
    elif game3d.get_platform() == game3d.PLATFORM_IOS:
        dirname = game3d.get_doc_dir()
    else:
        return
    doc_dir = game3d.get_doc_dir()
    ret &= remove_file(doc_dir, 'game_flag')
    ret &= remove_file(dirname, 'game_flag')
    ret &= remove_file(doc_dir, 'game_init_mode_flag')
    remove_patch_npk(dirname)
    remove_ext_patch_npk(dirname)
    temp_dir = os.path.join(dirname, patch_path.TEMP_DIRNAME)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    version_patch = patch_path.get_download_target_path('res/confs/version.json')
    version_week = version_patch.replace(patch_path.RES_PATCH_DIRNAME, patch_path.RES_PATCH_WEEKLY_NAME)
    ret &= remove_file(dirname, version_week)
    ret &= remove_file(dirname, version_patch)
    res_weekly = os.path.join(dirname, patch_path.RES_PATCH_WEEKLY_NAME)
    res_patch = os.path.join(dirname, patch_path.RES_PATCH_DIRNAME)
    ret &= remove_file(res_weekly, patch_path.FILELIST_NAME)
    ret &= remove_file(res_patch, patch_path.FILELIST_NAME)
    try:
        import json
        data = C_file.get_res_file('confs/ext_package.json', '')
        data_dict = json.loads(data)
        ext_name_lst = six_ex.keys(data_dict)
    except Exception as e:
        print('[revert] get ext package except:', str(e))
        ext_name_lst = ['kongdao_scene', 'skin', 'audio', 'video', 'pve', 'pve2', 'pve3']

    for ext_name in ext_name_lst:
        ext_flist_name = 'ext_flist_{}.lst'.format(ext_name)
        ret &= remove_file(res_patch, ext_flist_name)

    ret &= remove_file(res_patch, 'ext_version.config')
    res_temp = os.path.join(dirname, patch_path.TEMP_DIRNAME, 'res')
    script_temp = os.path.join(dirname, patch_path.TEMP_DIRNAME, 'script')
    script_patch = os.path.join(dirname, patch_path.SCRIPT_PATCH_DIRNAME)
    script_weekly = os.path.join(dirname, patch_path.SCRIPT_PATCH_WEEKLY_NAME)
    ret &= patch_utils.move_folder(res_patch, res_temp)
    ret &= patch_utils.move_folder(res_weekly, res_temp)
    ret &= patch_utils.move_folder(script_patch, script_temp)
    ret &= patch_utils.move_folder(script_weekly, script_temp)
    try:
        for t_path in (script_patch, script_weekly, res_patch, res_weekly):
            if not os.path.exists(t_path):
                os.makedirs(t_path)
            else:
                print('[revert] move_folder error:{}'.format(t_path))

    except Exception as e:
        print('[revert] make folder except:', str(e))

    ret &= remove_dir(dirname, 'res/effect_cache')
    ret &= remove_physx_cook_cache(dirname)
    remove_dir(dirname, 'res_debug')
    remove_dir(dirname, 'script_debug')
    print('revert game client finish, all success:', ret)
    REVERTING = False
    return ret


def revert_and_exit_game():
    if REVERTING:
        return False

    def do_revert():
        revert()

        def exit_func--- This code section failed: ---

 210       0  LOAD_GLOBAL           0  'render'
           3  LOAD_ATTR             1  'set_post_logic'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

 211      13  LOAD_GLOBAL           3  'game3d'
          16  LOAD_ATTR             4  'get_root_dir'
          19  CALL_FUNCTION_0       0 
          22  LOAD_CONST            1  '\\..\\launcher.exe'
          25  BINARY_ADD       
          26  STORE_FAST            0  'bin_launcher_path'

 213      29  LOAD_GLOBAL           3  'game3d'
          32  LOAD_ATTR             5  'get_platform'
          35  CALL_FUNCTION_0       0 
          38  LOAD_GLOBAL           3  'game3d'
          41  LOAD_ATTR             6  'PLATFORM_WIN32'
          44  COMPARE_OP            2  '=='
          47  POP_JUMP_IF_FALSE   130  'to 130'
          50  LOAD_GLOBAL           7  'os'
          53  LOAD_ATTR             8  'path'
          56  LOAD_ATTR             9  'exists'
          59  LOAD_FAST             0  'bin_launcher_path'
          62  CALL_FUNCTION_1       1 
        65_0  COME_FROM                '47'
          65  POP_JUMP_IF_FALSE   130  'to 130'

 214      68  LOAD_GLOBAL          10  'hasattr'
          71  LOAD_GLOBAL           3  'game3d'
          74  LOAD_CONST            2  'is_feature_ready'
          77  CALL_FUNCTION_2       2 
          80  POP_JUMP_IF_FALSE   114  'to 114'
          83  LOAD_GLOBAL           3  'game3d'
          86  LOAD_ATTR            11  'is_feature_ready'
          89  LOAD_CONST            3  'OpenExeWithParm'
          92  CALL_FUNCTION_1       1 
        95_0  COME_FROM                '80'
          95  POP_JUMP_IF_FALSE   114  'to 114'

 215      98  LOAD_GLOBAL           3  'game3d'
         101  LOAD_ATTR            12  'open_exe'
         104  LOAD_ATTR             4  'get_root_dir'
         107  CALL_FUNCTION_2       2 
         110  POP_TOP          
         111  JUMP_ABSOLUTE       150  'to 150'

 217     114  LOAD_GLOBAL           3  'game3d'
         117  LOAD_ATTR            13  'open_url'
         120  LOAD_FAST             0  'bin_launcher_path'
         123  CALL_FUNCTION_1       1 
         126  POP_TOP          
         127  JUMP_FORWARD         20  'to 150'

 219     130  LOAD_GLOBAL           3  'game3d'
         133  LOAD_ATTR            14  'restart'
         136  CALL_FUNCTION_0       0 
         139  POP_TOP          

 220     140  LOAD_GLOBAL           3  'game3d'
         143  LOAD_ATTR            15  'exit'
         146  CALL_FUNCTION_0       0 
         149  POP_TOP          
       150_0  COME_FROM                '127'
         150  LOAD_CONST            0  ''
         153  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 107

        render.set_post_logic(exit_func)

    t = threading.Thread(target=do_revert)
    t.setDaemon(True)
    t.start()
    return True


def revert_to_original_version_noerror():
    text = get_patch_text_id(90029)

    def ok_cb():
        game3d.show_msg_box(get_patch_text_id(90026), get_patch_text_id(90001), revert_and_exit_game, lambda : None, get_patch_text_id(90004), get_patch_text_id(90005))

    def cancel_cb():
        pass

    game3d.show_msg_box(text, get_patch_text_id(90001), ok_cb, cancel_cb, get_patch_text_id(90003), get_patch_text_id(90005))