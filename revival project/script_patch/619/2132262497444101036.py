# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/crashhunter/crashhunter_utils.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import traceback
import os
import six
import queue
import game3d
import six.moves.builtins
UPLOAD_SIZE_LIMIT = 1048576
err_queue = queue.Queue()

def get_dump_user_info():
    uid = ''
    server_name = ''
    username = six.moves.builtins.__dict__.get('user', '')
    if 'global_data' not in __builtins__ or global_data.player is None:
        return ('', '', '')
    else:
        uid = global_data.player.uid
        from logic.comsys.login.LoginSetting import LoginSetting
        server_info = LoginSetting().last_logined_server or {}
        server_name = server_info.get('svr_name', '')
        if username:
            username = '%s(%s)' % (global_data.player.char_name, username)
        else:
            username = global_data.player.char_name
        return (
         server_name, uid, username)


def get_dump_urs():
    from common.platform.channel import Channel
    return Channel().get_login_name() or ''


def get_bit_name():
    try:
        import sys
        if sys.maxsize > 4294967296:
            return '64bit'
        return '32bit'
    except:
        return 'except'


def update_dump_user_info():
    server_name, uid, username = get_dump_user_info()
    urs = get_dump_urs()
    game3d.set_dump_info('server_name', str(server_name))
    game3d.set_dump_info('uid', str(uid))
    game3d.set_dump_info('username', str(username))
    game3d.set_dump_info('urs', str(urs))
    import social
    channel = social.get_channel()
    if channel:
        app_channel = channel.distribution_channel
        if not app_channel:
            app_channel = channel.name
    else:
        app_channel = 'unknown'
    python_version = 'p2' if six.PY2 else 'p3'
    condition_str = '{"sys_arch":["%s",],"channel_name":["%s", ],"py_ver":["%s", ]}' % (get_bit_name(), app_channel, python_version)
    game3d.set_dump_info('conditions', condition_str)


def init_project(project):
    game3d.set_dump_info('project', project)


def init_dump_appkey(app_key):
    game3d.set_dump_info('appkey', app_key)


def init_dump_version():
    import exception_hook
    exception_hook.update_game_version()


def push_err(msg, func_handle=True):
    if not msg:
        return
    key = str(hash(msg))
    err = msg
    err_queue.put((key, err, func_handle))


def push_exc():
    push_err(traceback.format_exc())


def update(func=None):
    while True:
        try:
            key, err, func_handle = err_queue.get_nowait()
            game3d.post_script_error(key, err)
            if func and func_handle:
                func(err)
        except queue.Empty:
            return
        except:
            log_error('post_script_error failed!', traceback.format_exc())


def upload_client_log():
    from common.daemon_thread import DaemonThreadPool
    DaemonThreadPool().add_threadpool(do_upload_client_log, None)
    return


def do_upload_client_log():
    from common.utils.path import get_neox_dir
    neox_dir = get_neox_dir()
    cnt_log_name = 'log.txt'
    log_path = os.path.join(neox_dir, cnt_log_name)
    upload_file_info(log_path)
    prev_log_pattern = 'log_old_%d.txt'
    for i in range(0, 8):
        prev_log_path = os.path.join(neox_dir, prev_log_pattern % i)
        upload_file_info(prev_log_path, i + 1)

    print('do_upload_client_log finish')


def upload_client_cur_log():
    from common.daemon_thread import DaemonThreadPool
    DaemonThreadPool().add_threadpool(do_upload_client_cur_log, None)
    return


def do_upload_client_cur_log():
    from common.utils.path import get_neox_dir
    neox_dir = get_neox_dir()
    cnt_log_name = 'log.txt'
    log_path = os.path.join(neox_dir, cnt_log_name)
    upload_file_info(log_path)


def upload_file_info--- This code section failed: ---

 152       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'time'
           9  STORE_FAST            2  'time'

 153      12  LOAD_GLOBAL           1  'os'
          15  LOAD_ATTR             2  'path'
          18  LOAD_ATTR             3  'exists'
          21  LOAD_FAST             0  'file_path'
          24  CALL_FUNCTION_1       1 
          27  POP_JUMP_IF_TRUE     34  'to 34'

 154      30  LOAD_CONST            0  ''
          33  RETURN_END_IF    
        34_0  COME_FROM                '27'

 155      34  LOAD_GLOBAL           1  'os'
          37  LOAD_ATTR             2  'path'
          40  LOAD_ATTR             4  'getsize'
          43  LOAD_FAST             0  'file_path'
          46  CALL_FUNCTION_1       1 
          49  STORE_FAST            3  'file_size'

 156      52  LOAD_CONST            2  ''
          55  STORE_FAST            4  'data'

 157      58  LOAD_GLOBAL           5  'UPLOAD_SIZE_LIMIT'
          61  LOAD_CONST            3  2
          64  BINARY_DIVIDE    
          65  STORE_FAST            5  'limit'

 158      68  LOAD_GLOBAL           6  'open'
          71  LOAD_GLOBAL           4  'getsize'
          74  CALL_FUNCTION_2       2 
          77  SETUP_WITH           78  'to 158'
          80  STORE_FAST            6  'file_reader'

 159      83  LOAD_CONST            1  ''
          86  STORE_FAST            7  'offset'

 160      89  LOAD_FAST             3  'file_size'
          92  LOAD_FAST             5  'limit'
          95  COMPARE_OP            4  '>'
          98  POP_JUMP_IF_FALSE   114  'to 114'

 161     101  LOAD_FAST             3  'file_size'
         104  LOAD_FAST             5  'limit'
         107  BINARY_SUBTRACT  
         108  STORE_FAST            7  'offset'
         111  JUMP_FORWARD          0  'to 114'
       114_0  COME_FROM                '111'

 162     114  LOAD_FAST             6  'file_reader'
         117  LOAD_ATTR             7  'seek'
         120  LOAD_FAST             7  'offset'
         123  CALL_FUNCTION_1       1 
         126  POP_TOP          

 163     127  LOAD_FAST             6  'file_reader'
         130  LOAD_ATTR             8  'read'
         133  CALL_FUNCTION_0       0 
         136  STORE_FAST            4  'data'

 164     139  LOAD_GLOBAL           9  'six'
         142  LOAD_ATTR            10  'ensure_str'
         145  LOAD_FAST             4  'data'
         148  CALL_FUNCTION_1       1 
         151  STORE_FAST            4  'data'
         154  POP_BLOCK        
         155  LOAD_CONST            0  ''
       158_0  COME_FROM_WITH           '77'
         158  WITH_CLEANUP     
         159  END_FINALLY      

 166     160  LOAD_GLOBAL          11  'global_data'
         163  LOAD_ATTR            12  'player'
         166  LOAD_ATTR            13  'id'
         169  STORE_FAST            8  'player_id'

 167     172  LOAD_CONST            5  '_'
         175  LOAD_ATTR            14  'join'
         178  LOAD_GLOBAL          15  'str'
         181  LOAD_GLOBAL          16  'hash'
         184  LOAD_FAST             0  'file_path'
         187  CALL_FUNCTION_1       1 
         190  CALL_FUNCTION_1       1 
         193  LOAD_GLOBAL          15  'str'
         196  LOAD_FAST             1  'idx'
         199  CALL_FUNCTION_1       1 
         202  LOAD_GLOBAL          15  'str'
         205  LOAD_FAST             2  'time'
         208  LOAD_ATTR             0  'time'
         211  CALL_FUNCTION_0       0 
         214  CALL_FUNCTION_1       1 
         217  LOAD_GLOBAL          15  'str'
         220  LOAD_FAST             8  'player_id'
         223  CALL_FUNCTION_1       1 
         226  BUILD_LIST_4          4 
         229  CALL_FUNCTION_1       1 
         232  STORE_FAST            9  'title_str'

 168     235  LOAD_GLOBAL          17  'print'
         238  LOAD_CONST            6  'upload file info'
         241  LOAD_FAST             9  'title_str'
         244  LOAD_FAST             7  'offset'
         247  LOAD_GLOBAL          18  'len'
         250  LOAD_FAST             4  'data'
         253  CALL_FUNCTION_1       1 
         256  CALL_FUNCTION_5       5 
         259  POP_TOP          

 169     260  LOAD_GLOBAL          19  'game3d'
         263  LOAD_ATTR            20  'post_hunter_message'
         266  LOAD_FAST             9  'title_str'
         269  LOAD_FAST             4  'data'
         272  CALL_FUNCTION_2       2 
         275  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 74


SHADER_COMPILE_ERROR_TIMES = 0
SHADER_COMPILE_ERROR_UPLOAD_TIME = 0

def check_shader_compile_error--- This code section failed: ---

 178       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'render'
           9  STORE_FAST            0  'render'

 179      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'exception_hook'
          21  STORE_FAST            1  'exception_hook'

 180      24  LOAD_GLOBAL           2  'hasattr'
          27  LOAD_GLOBAL           2  'hasattr'
          30  CALL_FUNCTION_2       2 
          33  POP_JUMP_IF_FALSE   124  'to 124'

 181      36  LOAD_FAST             0  'render'
          39  LOAD_ATTR             3  'get_shader_compile_error_times'
          42  CALL_FUNCTION_0       0 
          45  STORE_FAST            2  'error_times'

 182      48  LOAD_FAST             2  'error_times'
          51  LOAD_GLOBAL           4  'SHADER_COMPILE_ERROR_TIMES'
          54  COMPARE_OP            4  '>'
          57  POP_JUMP_IF_FALSE   124  'to 124'

 183      60  LOAD_FAST             2  'error_times'
          63  STORE_GLOBAL          4  'SHADER_COMPILE_ERROR_TIMES'

 184      66  LOAD_GLOBAL           5  'SHADER_COMPILE_ERROR_UPLOAD_TIME'
          69  LOAD_CONST            3  1
          72  INPLACE_ADD      
          73  STORE_GLOBAL          5  'SHADER_COMPILE_ERROR_UPLOAD_TIME'

 187      76  LOAD_GLOBAL           5  'SHADER_COMPILE_ERROR_UPLOAD_TIME'
          79  LOAD_CONST            4  3
          82  COMPARE_OP            4  '>'
          85  POP_JUMP_IF_FALSE    92  'to 92'

 188      88  LOAD_CONST            0  ''
          91  RETURN_END_IF    
        92_0  COME_FROM                '85'

 190      92  LOAD_CONST            5  'shader compile error: detail info see log.txt\n'
          95  STORE_FAST            3  'error_content'

 191      98  LOAD_FAST             1  'exception_hook'
         101  LOAD_ATTR             6  'post_error'
         104  LOAD_FAST             3  'error_content'
         107  CALL_FUNCTION_1       1 
         110  POP_TOP          

 194     111  LOAD_GLOBAL           7  'upload_client_cur_log'
         114  CALL_FUNCTION_0       0 
         117  POP_TOP          
         118  JUMP_ABSOLUTE       124  'to 124'
         121  JUMP_FORWARD          0  'to 124'
       124_0  COME_FROM                '121'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 30


# global SHADER_COMPILE_ERROR_UPLOAD_TIME ## Warning: Unused global# global SHADER_COMPILE_ERROR_TIMES ## Warning: Unused global