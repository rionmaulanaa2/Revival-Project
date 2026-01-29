# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/nx_file_logic/logic_after_patch.py
from __future__ import absolute_import
from __future__ import print_function
import os
import zlib
import json
import time
import C_file
import game3d
import six_ex
import six.moves.builtins
from patch import patch_path, pn_utils
from ext_package import ext_package_utils
from ext_package import ext_pn_utils

def is_physxcook_mesh(in_path):
    if in_path.endswith('.mesh') and (in_path.startswith('res/model_new') or in_path.startswith('res/scene')):
        return True
    else:
        return False


def is_mp4_file--- This code section failed: ---

  26       0  LOAD_GLOBAL           0  'open'
           3  LOAD_GLOBAL           1  'read'
           6  CALL_FUNCTION_2       2 
           9  SETUP_WITH           49  'to 61'
          12  STORE_FAST            1  'tmp_f'

  27      15  LOAD_FAST             1  'tmp_f'
          18  LOAD_ATTR             1  'read'
          21  LOAD_CONST            2  8
          24  CALL_FUNCTION_1       1 
          27  STORE_FAST            2  'header'

  28      30  LOAD_FAST             2  'header'
          33  LOAD_CONST            3  4
          36  LOAD_CONST            2  8
          39  SLICE+3          
          40  LOAD_CONST            4  'ftyp'
          43  COMPARE_OP            2  '=='
          46  POP_JUMP_IF_FALSE    53  'to 53'

  29      49  LOAD_GLOBAL           2  'True'
          52  RETURN_END_IF    
        53_0  COME_FROM                '46'

  31      53  LOAD_GLOBAL           3  'False'
          56  RETURN_VALUE     
          57  POP_BLOCK        
          58  LOAD_CONST            0  ''
        61_0  COME_FROM_WITH           '9'
          61  WITH_CLEANUP     
          62  END_FINALLY      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def save_patched_file--- This code section failed: ---

  37       0  SETUP_EXCEPT        153  'to 156'

  38       3  LOAD_CONST            1  ''
           6  LOAD_CONST            2  ('patch_utils',)
           9  IMPORT_NAME           0  'patch'
          12  IMPORT_FROM           1  'patch_utils'
          15  STORE_FAST            0  'patch_utils'
          18  POP_TOP          

  39      19  LOAD_GLOBAL           2  'hasattr'
          22  LOAD_GLOBAL           3  'get_patched_file_dict'
          25  CALL_FUNCTION_2       2 
          28  POP_JUMP_IF_FALSE   152  'to 152'

  40      31  LOAD_FAST             0  'patch_utils'
          34  LOAD_ATTR             3  'get_patched_file_dict'
          37  CALL_FUNCTION_0       0 
          40  STORE_FAST            1  'record_patched_files'

  41      43  LOAD_FAST             1  'record_patched_files'
          46  POP_JUMP_IF_FALSE   152  'to 152'

  42      49  LOAD_GLOBAL           4  'zlib'
          52  LOAD_ATTR             5  'compress'
          55  LOAD_GLOBAL           6  'six'
          58  LOAD_ATTR             7  'ensure_binary'
          61  LOAD_GLOBAL           8  'json'
          64  LOAD_ATTR             9  'dumps'
          67  LOAD_FAST             1  'record_patched_files'
          70  CALL_FUNCTION_1       1 
          73  CALL_FUNCTION_1       1 
          76  CALL_FUNCTION_1       1 
          79  STORE_FAST            2  'info_str'

  43      82  LOAD_GLOBAL          10  'os'
          85  LOAD_ATTR            11  'path'
          88  LOAD_ATTR            12  'join'
          91  LOAD_GLOBAL          13  'game3d'
          94  LOAD_ATTR            14  'get_doc_dir'
          97  CALL_FUNCTION_0       0 
         100  LOAD_CONST            4  'patched_file.flag'
         103  CALL_FUNCTION_2       2 
         106  STORE_FAST            3  'save_filepath'

  44     109  LOAD_GLOBAL          15  'open'
         112  LOAD_FAST             3  'save_filepath'
         115  LOAD_CONST            5  'wb'
         118  CALL_FUNCTION_2       2 
         121  SETUP_WITH           20  'to 144'
         124  STORE_FAST            4  'tmp_file'

  45     127  LOAD_FAST             4  'tmp_file'
         130  LOAD_ATTR            16  'write'
         133  LOAD_FAST             2  'info_str'
         136  CALL_FUNCTION_1       1 
         139  POP_TOP          
         140  POP_BLOCK        
         141  LOAD_CONST            0  ''
       144_0  COME_FROM_WITH           '121'
         144  WITH_CLEANUP     
         145  END_FINALLY      
         146  JUMP_ABSOLUTE       152  'to 152'
         149  JUMP_FORWARD          0  'to 152'
       152_0  COME_FROM                '149'
         152  POP_BLOCK        
         153  JUMP_FORWARD         65  'to 221'
       156_0  COME_FROM                '0'

  46     156  DUP_TOP          
         157  LOAD_GLOBAL          17  'Exception'
         160  COMPARE_OP           10  'exception-match'
         163  POP_JUMP_IF_FALSE   220  'to 220'
         166  POP_TOP          
         167  STORE_FAST            5  'e'
         170  POP_TOP          

  47     171  LOAD_CONST            1  ''
         174  LOAD_CONST            0  ''
         177  IMPORT_NAME          18  'traceback'
         180  STORE_FAST            6  'traceback'

  48     183  LOAD_GLOBAL          19  'print'
         186  LOAD_CONST            6  '[Except] save patched file except:{}\n{}'
         189  LOAD_ATTR            20  'format'
         192  LOAD_GLOBAL          21  'str'
         195  LOAD_FAST             5  'e'
         198  CALL_FUNCTION_1       1 
         201  LOAD_FAST             6  'traceback'
         204  LOAD_ATTR            22  'format_exc'
         207  CALL_FUNCTION_0       0 
         210  CALL_FUNCTION_2       2 
         213  CALL_FUNCTION_1       1 
         216  POP_TOP          
         217  JUMP_FORWARD          1  'to 221'
         220  END_FINALLY      
       221_0  COME_FROM                '220'
       221_1  COME_FROM                '153'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 25


def init_discrete_loader():
    if not game3d.is_release_version():
        if hasattr(C_file, 'set_res_ignore_descrete_flag'):
            C_file.set_res_ignore_descrete_flag(False)


def del_old_video_cache--- This code section failed: ---

  62       0  LOAD_GLOBAL           0  'game3d'
           3  LOAD_ATTR             1  'get_doc_dir'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            0  'doc_dir'

  65      12  LOAD_GLOBAL           2  'os'
          15  LOAD_ATTR             3  'path'
          18  LOAD_ATTR             4  'join'
          21  LOAD_ATTR             1  'get_doc_dir'
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            1  'new_video_cache_folder'

  66      30  LOAD_GLOBAL           2  'os'
          33  LOAD_ATTR             3  'path'
          36  LOAD_ATTR             5  'exists'
          39  LOAD_FAST             1  'new_video_cache_folder'
          42  CALL_FUNCTION_1       1 
          45  POP_JUMP_IF_FALSE   124  'to 124'

  67      48  LOAD_CONST            2  ''
          51  LOAD_CONST            0  ''
          54  IMPORT_NAME           6  'shutil'
          57  STORE_FAST            2  'shutil'

  68      60  SETUP_EXCEPT         20  'to 83'

  69      63  LOAD_FAST             2  'shutil'
          66  LOAD_ATTR             7  'rmtree'
          69  LOAD_FAST             1  'new_video_cache_folder'
          72  LOAD_GLOBAL           8  'False'
          75  CALL_FUNCTION_2       2 
          78  POP_TOP          
          79  POP_BLOCK        
          80  JUMP_ABSOLUTE       124  'to 124'
        83_0  COME_FROM                '60'

  70      83  DUP_TOP          
          84  LOAD_GLOBAL           9  'Exception'
          87  COMPARE_OP           10  'exception-match'
          90  POP_JUMP_IF_FALSE   120  'to 120'
          93  POP_TOP          
          94  STORE_FAST            3  'e'
          97  POP_TOP          

  71      98  LOAD_GLOBAL          10  'print'
         101  LOAD_CONST            3  'rmtree v_tmp except:'
         104  LOAD_GLOBAL          11  'str'
         107  LOAD_FAST             3  'e'
         110  CALL_FUNCTION_1       1 
         113  CALL_FUNCTION_2       2 
         116  POP_TOP          
         117  JUMP_ABSOLUTE       124  'to 124'
         120  END_FINALLY      
       121_0  COME_FROM                '120'
         121  JUMP_FORWARD          0  'to 124'
       124_0  COME_FROM                '121'

  74     124  LOAD_GLOBAL           2  'os'
         127  LOAD_ATTR             3  'path'
         130  LOAD_ATTR             4  'join'
         133  LOAD_ATTR             4  'join'
         136  CALL_FUNCTION_2       2 
         139  STORE_FAST            4  'del_flag_path'

  75     142  LOAD_GLOBAL           2  'os'
         145  LOAD_ATTR             3  'path'
         148  LOAD_ATTR             5  'exists'
         151  LOAD_FAST             4  'del_flag_path'
         154  CALL_FUNCTION_1       1 
         157  POP_JUMP_IF_FALSE   164  'to 164'

  76     160  LOAD_CONST            0  ''
         163  RETURN_END_IF    
       164_0  COME_FROM                '157'

  78     164  SETUP_EXCEPT         19  'to 186'

  79     167  LOAD_GLOBAL           2  'os'
         170  LOAD_ATTR            12  'listdir'
         173  LOAD_FAST             0  'doc_dir'
         176  CALL_FUNCTION_1       1 
         179  STORE_FAST            5  'file_list'
         182  POP_BLOCK        
         183  JUMP_FORWARD         39  'to 225'
       186_0  COME_FROM                '164'

  80     186  DUP_TOP          
         187  LOAD_GLOBAL           9  'Exception'
         190  COMPARE_OP           10  'exception-match'
         193  POP_JUMP_IF_FALSE   224  'to 224'
         196  POP_TOP          
         197  STORE_FAST            3  'e'
         200  POP_TOP          

  81     201  LOAD_GLOBAL          10  'print'
         204  LOAD_CONST            5  'read old_v_cache.flag except:'
         207  LOAD_GLOBAL          11  'str'
         210  LOAD_FAST             3  'e'
         213  CALL_FUNCTION_1       1 
         216  CALL_FUNCTION_2       2 
         219  POP_TOP          

  82     220  LOAD_CONST            0  ''
         223  RETURN_VALUE     
         224  END_FINALLY      
       225_0  COME_FROM                '224'
       225_1  COME_FROM                '183'

  84     225  LOAD_GLOBAL           8  'False'
         228  STORE_FAST            6  'remove_error'

  85     231  SETUP_LOOP          156  'to 390'
         234  LOAD_FAST             5  'file_list'
         237  GET_ITER         
         238  FOR_ITER            148  'to 389'
         241  STORE_FAST            7  'file_name'

  86     244  LOAD_FAST             7  'file_name'
         247  LOAD_ATTR            13  'isdigit'
         250  CALL_FUNCTION_0       0 
         253  POP_JUMP_IF_TRUE    262  'to 262'

  87     256  CONTINUE            238  'to 238'
         259  JUMP_FORWARD          0  'to 262'
       262_0  COME_FROM                '259'

  88     262  LOAD_GLOBAL           2  'os'
         265  LOAD_ATTR             3  'path'
         268  LOAD_ATTR             4  'join'
         271  LOAD_FAST             0  'doc_dir'
         274  LOAD_FAST             7  'file_name'
         277  CALL_FUNCTION_2       2 
         280  STORE_FAST            8  'abs_file_path'

  89     283  LOAD_GLOBAL           2  'os'
         286  LOAD_ATTR             3  'path'
         289  LOAD_ATTR            14  'isfile'
         292  LOAD_FAST             8  'abs_file_path'
         295  CALL_FUNCTION_1       1 
         298  POP_JUMP_IF_TRUE    307  'to 307'

  90     301  CONTINUE            238  'to 238'
         304  JUMP_FORWARD          0  'to 307'
       307_0  COME_FROM                '304'

  91     307  LOAD_GLOBAL          15  'is_mp4_file'
         310  LOAD_FAST             8  'abs_file_path'
         313  CALL_FUNCTION_1       1 
         316  POP_JUMP_IF_FALSE   238  'to 238'

  92     319  SETUP_EXCEPT         17  'to 339'

  93     322  LOAD_GLOBAL           2  'os'
         325  LOAD_ATTR            16  'remove'
         328  LOAD_FAST             8  'abs_file_path'
         331  CALL_FUNCTION_1       1 
         334  POP_TOP          
         335  POP_BLOCK        
         336  JUMP_ABSOLUTE       386  'to 386'
       339_0  COME_FROM                '319'

  94     339  DUP_TOP          
         340  LOAD_GLOBAL           9  'Exception'
         343  COMPARE_OP           10  'exception-match'
         346  POP_JUMP_IF_FALSE   382  'to 382'
         349  POP_TOP          
         350  STORE_FAST            3  'e'
         353  POP_TOP          

  95     354  LOAD_GLOBAL          10  'print'
         357  LOAD_CONST            6  'remove old file except:'
         360  LOAD_GLOBAL          11  'str'
         363  LOAD_FAST             3  'e'
         366  CALL_FUNCTION_1       1 
         369  CALL_FUNCTION_2       2 
         372  POP_TOP          

  96     373  LOAD_GLOBAL          17  'True'
         376  STORE_FAST            6  'remove_error'
         379  JUMP_ABSOLUTE       386  'to 386'
         382  END_FINALLY      
       383_0  COME_FROM                '382'
         383  JUMP_BACK           238  'to 238'
         386  JUMP_BACK           238  'to 238'
         389  POP_BLOCK        
       390_0  COME_FROM                '231'

  97     390  LOAD_FAST             6  'remove_error'
         393  POP_JUMP_IF_FALSE   400  'to 400'

  98     396  LOAD_CONST            0  ''
         399  RETURN_END_IF    
       400_0  COME_FROM                '393'

 100     400  SETUP_EXCEPT         41  'to 444'

 101     403  LOAD_GLOBAL          18  'open'
         406  LOAD_FAST             4  'del_flag_path'
         409  LOAD_CONST            7  'w'
         412  CALL_FUNCTION_2       2 
         415  SETUP_WITH           20  'to 438'
         418  STORE_FAST            9  'tmp_f'

 102     421  LOAD_FAST             9  'tmp_f'
         424  LOAD_ATTR            19  'write'
         427  LOAD_CONST            8  '1'
         430  CALL_FUNCTION_1       1 
         433  POP_TOP          
         434  POP_BLOCK        
         435  LOAD_CONST            0  ''
       438_0  COME_FROM_WITH           '415'
         438  WITH_CLEANUP     
         439  END_FINALLY      
         440  POP_BLOCK        
         441  JUMP_FORWARD         38  'to 482'
       444_0  COME_FROM                '400'

 103     444  DUP_TOP          
         445  LOAD_GLOBAL           9  'Exception'
         448  COMPARE_OP           10  'exception-match'
         451  POP_JUMP_IF_FALSE   481  'to 481'
         454  POP_TOP          
         455  STORE_FAST            3  'e'
         458  POP_TOP          

 104     459  LOAD_GLOBAL          10  'print'
         462  LOAD_CONST            9  'write old v_cache.flag except:'
         465  LOAD_GLOBAL          11  'str'
         468  LOAD_FAST             3  'e'
         471  CALL_FUNCTION_1       1 
         474  CALL_FUNCTION_2       2 
         477  POP_TOP          
         478  JUMP_FORWARD          1  'to 482'
         481  END_FINALLY      
       482_0  COME_FROM                '481'
       482_1  COME_FROM                '441'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 24


def init_used_flist_data():
    b_time = time.time()
    valid_flist = True
    is_real_ext = ext_package_utils.is_real_ext_package()
    if is_real_ext:
        from ext_package import ext_package_manager
        ext_mgr = ext_package_manager.get_ext_package_instance()
        other_npk_lst = ext_mgr.get_active_ext_npk_lst()
    else:
        other_npk_lst = []
    script_prefix = patch_path.SCRIPT_PREFIX
    script_prefix_len = len(script_prefix)
    all_script_dict = {}
    all_physc_cook_res_dict = {}

    def parse_data(in_data, in_script_dict, in_physc_cook_res_dict, is_patch_npk=False):
        in_data = six.ensure_str(in_data)
        for line in in_data.splitlines():
            if not line:
                continue
            split_info = line.split('\t')
            if is_patch_npk:
                file_name = split_info[1]
                split_info = split_info[1:]
            else:
                file_name = split_info[0]
            if file_name.startswith(script_prefix):
                script_file_name = file_name[script_prefix_len:]
                in_script_dict[script_file_name] = split_info
            elif is_physxcook_mesh(file_name):
                in_physc_cook_res_dict[file_name] = split_info

    all_npk_lst = ext_package_utils.get_completion_npk_lst()
    all_npk_lst.extend(other_npk_lst)
    flist_files = [patch_path.ORG_FLIST_FILEPATH]
    for npk_name in all_npk_lst:
        npk_name = npk_name[:-4]
        npk_file_path = patch_path.RES_FLIST_FILE_PARTTEN % npk_name
        flist_files.append(npk_file_path)

    for file_name in flist_files:
        try:
            print('org:', file_name)
            flist_data = C_file.get_res_file(file_name, '')
            parse_data(flist_data, all_script_dict, all_physc_cook_res_dict)
        except Exception as e:
            valid_flist = False
            print('[Except] get {} flist except:{}'.format(file_name, str(e)))

    patch_npk_enable = game3d.is_feature_ready('PATCH_NPK_MERGE')
    try:
        if patch_npk_enable:
            ret, patch_npk_info = pn_utils.get_saved_patch_npk_info()
            if not ret:
                valid_flist = False
            ret, ext_patch_npk_info = ext_pn_utils.get_saved_ext_patch_npk_info()
            if not ret:
                valid_flist = False
            patch_npk_name_lst = six_ex.keys(patch_npk_info)
            patch_npk_name_lst.extend(six_ex.keys(ext_patch_npk_info))
            for patch_npk_name in patch_npk_name_lst:
                print('patch:', patch_npk_name)
                flist_file_name = '{}_flist.txt'.format(patch_npk_name[:-4])
                if patch_npk_name == pn_utils.PN_SCRIPT_NAME:
                    flist_data = C_file.get_file(flist_file_name, '')
                else:
                    flist_data = C_file.get_res_file(flist_file_name, '')
                if flist_data:
                    parse_data(flist_data, all_script_dict, all_physc_cook_res_dict, is_patch_npk=True)
                else:
                    valid_flist = False

        else:
            patch_flist_path = patch_path.get_flist_path()
            if os.path.exists(patch_flist_path):
                with open(patch_flist_path, 'rb') as tmp_f:
                    flist_data = tmp_f.read()
                flist_data = zlib.decompress(flist_data)
                parse_data(flist_data, all_script_dict, all_physc_cook_res_dict)
    except Exception as e:
        valid_flist = False
        import traceback
        print('[Except] get patch flist except:{}\n{}'.format(str(e), traceback.format_exc()))

    if valid_flist:
        six.moves.builtins.__dict__['SCRIPT_FLIST_DICT'] = all_script_dict
    print('[init flist] valid:{} cost time: {} script:{} physx:{}'.format(valid_flist, time.time() - b_time, len(all_script_dict), len(all_physc_cook_res_dict)))
    if valid_flist:
        process_physx_npk(all_physc_cook_res_dict)


def process_physx_npk(in_new_flist):
    if not game3d.is_feature_ready('PhysxCookFix'):
        return
    b_time = time.time()
    from .physx_cook_npk import PhysxCookNpkProcessor
    physx_npk_processor = PhysxCookNpkProcessor()
    ret = physx_npk_processor.process(in_new_flist)
    can_enable_cook = physx_npk_processor.can_enable_cook()
    import world
    cost_time = time.time() - b_time
    if can_enable_cook:
        physxcook_dir = os.path.join(patch_path.get_neox_dir(), 'res/physxcook')
        if not os.path.exists(physxcook_dir):
            os.makedirs(physxcook_dir)
        world.enable_physx_cook(True)
        print('[physx_cook_npk] cost time:{} ret: {} enable: True'.format(cost_time, ret))
    else:
        world.enable_physx_cook(False)
        print('[physx_cook_npk] cost time:{} ret: {} enable: False'.format(cost_time, ret))


def thread_worker_before_game():
    del_old_video_cache()
    init_discrete_loader()
    init_used_flist_data()
    save_patched_file()