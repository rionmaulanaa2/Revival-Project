# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/video_record_utils.py
from __future__ import absolute_import
from functools import cmp_to_key
import os
import shutil
import game3d
from common.platform import is_android
from logic.gcommon.ctypes.HighlightMoment import HighlightMoment, cut_highmoments_to_max_kill, CUT_TIME_INTV_MAP
from logic.gcommon.common_const import battle_const as bconst
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.time_utility import ONE_DAY_SECONDS
NEED_MD5 = False
SETTING_NAME = 'kernel'
SHARE_SETTING_NAME = 's_kernel'
MEMORY_NEED = 450
AUTO_SAVE_NUM = 4
BEGIN_VIDEO = 'video/begin.mp4'
END_VIDEO = 'video/end.mp4'
MAX_SHARE_DAY_NUM = 50
SHARE_STORE_TIME = 2 * ONE_DAY_SECONDS
SHARE_LOCAL_STORE_TIME = 3 * ONE_DAY_SECONDS
SHARE_LOCAL_FRIEND_STORE_TIME = 10 * ONE_DAY_SECONDS
HIGH_KEY = 'high'
REFINE_KEY = 'refine'
FREE_KEY = 'free'
SMALL_COVER_KEY = 'small_cover'
BIG_COVER_KEY = 'big_cover'
AUTO_TIME_KEY = 'auto_save_time'
SMALL_COVER_SCALE = 0.25
COVER_FILE_PREFIX = 'high_cover'
SCALE_MODE_CLIP = 0
SCALE_MODE_FILL = 1
VIDEO_TYPE_BATTLE = 0
VIDEO_TYPE_FREE = 1
V_STATE_NO_VIDEO = 0
V_STATE_PROCESSING = 1
V_STATE_READY = 2
if is_android():
    BASE_PATH = os.path.join(game3d.get_internal_data_dir(), 'battle_video')
else:
    BASE_PATH = os.path.join(game3d.get_doc_dir(), 'battle_video')
TEMP_PATH = os.path.join(BASE_PATH, 'temp')
HIGH_TRIM_TEMP_PATH = os.path.join(TEMP_PATH, 'high_trim')
REFINE_TRIM_TEMP_PATH = os.path.join(TEMP_PATH, 'refine_trim')
BEGIN_VIDEO_TEMP_PATH = os.path.join(TEMP_PATH, 'begin.mp4')
END_VIDEO_TEMP_PATH = os.path.join(TEMP_PATH, 'end.mp4')
MERGE_TEMP_PATH = os.path.join(TEMP_PATH, 'merge_tmp')
HIGHLIGHT_PATH = os.path.join(BASE_PATH, 'high_light')
FREE_RECORD_PATH = os.path.join(BASE_PATH, 'free_record')
SHARE_VIDEO_PATH = os.path.join(BASE_PATH, 'share_video')
HIGH_MIX_AUDIO_TEMP_PATH = os.path.join(MERGE_TEMP_PATH, 'high_video.mp3')
REFINE_MIX_AUDIO_TEMP_PATH = os.path.join(MERGE_TEMP_PATH, 'refine_video.mp3')
AUDIO_RES_PATH_DICT = {HIGH_KEY: 'video/high_video.mp3',
   REFINE_KEY: 'video/refine_video.mp3'
   }
AUDIO_PATH_DICT = {HIGH_KEY: HIGH_MIX_AUDIO_TEMP_PATH,
   REFINE_KEY: REFINE_MIX_AUDIO_TEMP_PATH
   }

def clear_and_make_path(path_lst):
    try:
        for path in path_lst:
            if os.path.exists(path):
                shutil.rmtree(path, True)
            os.makedirs(path)

    except Exception as e:
        log_error('clear_and_make_path error: [%s]', e)
        return False

    return True


def get_video_default_name--- This code section failed: ---

 108       0  BUILD_MAP_3           3 

 109       3  LOAD_CONST            1  2255
           6  LOAD_GLOBAL           0  'HIGH_KEY'
           9  STORE_MAP        

 110      10  LOAD_CONST            2  2299
          13  LOAD_GLOBAL           1  'REFINE_KEY'
          16  STORE_MAP        

 111      17  LOAD_CONST            3  2257
          20  LOAD_GLOBAL           2  'FREE_KEY'
          23  STORE_MAP        
          24  STORE_FAST            2  'text_dict'

 113      27  LOAD_FAST             2  'text_dict'
          30  LOAD_ATTR             3  'get'
          33  LOAD_ATTR             1  'REFINE_KEY'
          36  CALL_FUNCTION_2       2 
          39  STORE_FAST            3  'text_id'

 114      42  LOAD_GLOBAL           4  'get_text_by_id'
          45  LOAD_FAST             3  'text_id'
          48  CALL_FUNCTION_1       1 
          51  STORE_FAST            4  'text'

 115      54  LOAD_FAST             1  'saved'
          57  POP_JUMP_IF_TRUE     88  'to 88'

 116      60  LOAD_FAST             4  'text'
          63  LOAD_CONST            4  '({0})'
          66  LOAD_ATTR             5  'format'
          69  LOAD_GLOBAL           4  'get_text_by_id'
          72  LOAD_CONST            5  3153
          75  CALL_FUNCTION_1       1 
          78  CALL_FUNCTION_1       1 
          81  INPLACE_ADD      
          82  STORE_FAST            4  'text'
          85  JUMP_FORWARD          0  'to 88'
        88_0  COME_FROM                '85'

 117      88  LOAD_FAST             4  'text'
          91  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 36


def get_video_name_lst(path):
    try:
        file_lst = os.listdir(path)
    except Exception as e:
        file_lst = []

    video_lst = []
    for file_name in file_lst:
        if file_name.endswith('.mp4'):
            video_lst.append(file_name)

    video_lst.sort()
    return video_lst


def get_video_merge_info(base_path, video_name_lst):
    from logic.gcommon.time_utility import get_server_time
    valid_path_lst = []
    start = get_server_time()
    end = 0
    for name in video_name_lst:
        path = os.path.join(base_path, name)
        if os.path.exists(path):
            try:
                s_t, e_t, _ = name.split('_')
                if start > int(s_t):
                    start = int(s_t)
                if end < int(e_t):
                    end = int(e_t)
                valid_path_lst.append(path)
            except Exception:
                continue

    return (
     valid_path_lst, start, end)


def get_valid_merge_info(video_path_lst):
    from logic.gcommon.time_utility import get_server_time
    valid_lst = []
    start = get_server_time()
    end = 0
    for path in video_path_lst:
        if os.path.exists(path):
            valid_lst.append(path)
            try:
                base_name = os.path.basename(path)
                s_t, e_t, _ = base_name.split('_')
                if start > int(s_t):
                    start = int(s_t)
                if end < int(e_t):
                    end = int(e_t)
            except Exception:
                continue

    if valid_lst:
        valid_lst.sort()
    return (
     valid_lst, start, end)


def get_valid_trim_time(start, end, start_time, video_length):
    start_trim = start - start_time
    end_trim = end - start_time
    if end_trim > video_length:
        end_trim = video_length
    if start_trim < 0:
        start_trim = 0
    start_trim += 0.5
    end_trim += 0.5
    start_trim = start_trim * 1000
    end_trim = end_trim * 1000
    return (
     int(start_trim), int(end_trim))


def get_refine_video_trim_info(highlights, start_record_time, video_length):
    max_kill_cnt = global_data.player.get_setting_2(uoc.HIGH_LIGHT_TIMES_KEY)
    highlights.sort(key=cmp_to_key(HighlightMoment.cmp_highlight_by_time))
    edited_highlights = []
    total_kill_cnt = 0
    for highlight in highlights:
        total_kill_cnt += highlight.kill_cnt

    max_kill_cnt = min(max_kill_cnt, total_kill_cnt)
    if max_kill_cnt <= 0 or max_kill_cnt > bconst.HIGHLIGHT_MAX_KILL:
        return []
    pre_cap, tail_cap = CUT_TIME_INTV_MAP[max_kill_cnt]
    new_high = True
    for highlight in highlights:
        new_high = True
        for kill_info in highlight.kill_info:
            dead_type, kill_time, is_lore, is_ai = kill_info
            if edited_highlights and not new_high:
                excellent_shot = edited_highlights[-1]
                if kill_time - tail_cap <= excellent_shot.end:
                    excellent_shot.end = min(kill_time - tail_cap, excellent_shot.start)
                    excellent_shot.end = max(kill_time + tail_cap, excellent_shot.end)
                    excellent_shot.add_kill_info(dead_type, kill_time, is_lore, is_ai)
                    continue
            excellent_shot = HighlightMoment()
            excellent_shot.start = kill_time - pre_cap
            excellent_shot.end = kill_time + tail_cap
            excellent_shot.add_kill_info(dead_type, kill_time, is_lore, is_ai)
            edited_highlights.append(excellent_shot)
            new_high = False

    edited_highlights.sort(key=cmp_to_key(HighlightMoment.cmp_highlight_by_priority))
    excellent_shots = []
    total_kill_cnt = 0
    for excellent_shot in edited_highlights:
        excellent_shots.append(excellent_shot)
        total_kill_cnt += excellent_shot.kill_cnt
        if total_kill_cnt >= bconst.HIGHLIGHT_MAX_KILL:
            break

    excellent_shots = cut_highmoments_to_max_kill(total_kill_cnt, excellent_shots)
    ret_lst = []
    for idx, shot in enumerate(excellent_shots):
        start = shot.start
        end = shot.end
        if end <= start_record_time:
            continue
        start_trim, end_trim = get_valid_trim_time(start, end, start_record_time, video_length)
        out_path = REFINE_TRIM_TEMP_PATH + '/{0}_{1}_refine.mp4'.format(int(start), int(end))
        ret_lst.append((out_path, start_trim, end_trim))

    return ret_lst


def read_video_chunks(file_obj, chunk_size=2048):
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data


def prepare_mix_audio(key):
    audio_path = AUDIO_PATH_DICT[key]
    try:
        if os.path.exists(audio_path):
            if not NEED_MD5:
                return audio_path
            os.remove(audio_path)
        import C_file
        import hashlib
        audio_data = C_file.get_res_file(AUDIO_RES_PATH_DICT[key], '')
        with open(audio_path, 'wb') as tmp_f:
            tmp_f.write(audio_data)
        if os.path.exists(audio_path):
            return audio_path
        return ''
    except Exception as e:
        log_error('[prepare_mix_audio] error:[%s]' % str(e))
        return ''


def cal_video_md5--- This code section failed: ---

 322       0  LOAD_FAST             0  'video_path'
           3  UNARY_NOT        
           4  POP_JUMP_IF_TRUE     26  'to 26'
           7  LOAD_GLOBAL           0  'os'
          10  LOAD_ATTR             1  'path'
          13  LOAD_ATTR             2  'exists'
          16  LOAD_FAST             0  'video_path'
          19  CALL_FUNCTION_1       1 
          22  UNARY_NOT        
        23_0  COME_FROM                '4'
          23  POP_JUMP_IF_FALSE    36  'to 36'

 323      26  LOAD_GLOBAL           3  'False'
          29  LOAD_CONST            1  ''
          32  BUILD_TUPLE_2         2 
          35  RETURN_END_IF    
        36_0  COME_FROM                '23'

 324      36  SETUP_EXCEPT        107  'to 146'

 325      39  LOAD_CONST            2  ''
          42  LOAD_CONST            0  ''
          45  IMPORT_NAME           4  'hashlib'
          48  STORE_FAST            1  'hashlib'

 326      51  LOAD_FAST             1  'hashlib'
          54  LOAD_ATTR             5  'md5'
          57  CALL_FUNCTION_0       0 
          60  STORE_FAST            2  'md5'

 327      63  LOAD_GLOBAL           6  'open'
          66  LOAD_GLOBAL           3  'False'
          69  CALL_FUNCTION_2       2 
          72  SETUP_WITH           43  'to 118'
          75  STORE_FAST            3  'f'

 328      78  SETUP_LOOP           33  'to 114'
          81  LOAD_GLOBAL           7  'read_video_chunks'
          84  LOAD_FAST             3  'f'
          87  CALL_FUNCTION_1       1 
          90  GET_ITER         
          91  FOR_ITER             19  'to 113'
          94  STORE_FAST            4  'chuck'

 329      97  LOAD_FAST             2  'md5'
         100  LOAD_ATTR             8  'update'
         103  LOAD_FAST             4  'chuck'
         106  CALL_FUNCTION_1       1 
         109  POP_TOP          
         110  JUMP_BACK            91  'to 91'
         113  POP_BLOCK        
       114_0  COME_FROM                '78'
         114  POP_BLOCK        
         115  LOAD_CONST            0  ''
       118_0  COME_FROM_WITH           '72'
         118  WITH_CLEANUP     
         119  END_FINALLY      

 330     120  LOAD_GLOBAL           9  'True'
         123  LOAD_GLOBAL          10  'str'
         126  LOAD_FAST             2  'md5'
         129  LOAD_ATTR            11  'hexdigest'
         132  CALL_FUNCTION_0       0 
         135  CALL_FUNCTION_1       1 
         138  BUILD_TUPLE_2         2 
         141  RETURN_VALUE     
         142  POP_BLOCK        
         143  JUMP_FORWARD         24  'to 170'
       146_0  COME_FROM                '36'

 331     146  DUP_TOP          
         147  LOAD_GLOBAL          12  'Exception'
         150  COMPARE_OP           10  'exception-match'
         153  POP_JUMP_IF_FALSE   169  'to 169'
         156  POP_TOP          
         157  POP_TOP          
         158  POP_TOP          

 332     159  LOAD_GLOBAL           3  'False'
         162  LOAD_CONST            1  ''
         165  BUILD_TUPLE_2         2 
         168  RETURN_VALUE     
         169  END_FINALLY      
       170_0  COME_FROM                '169'
       170_1  COME_FROM                '143'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 69


def cal_md5(data):
    try:
        import hashlib
        md5 = hashlib.md5()
        md5.update(data)
        return (
         True, str(md5.hexdigest()))
    except Exception:
        return (
         False, '')


def get_cover_name_and_path(md5_str):
    from common.utils.path import get_neox_dir
    from patch.patch_path import get_download_target_path
    small_file_name = '{0}/{1}.png'.format(COVER_FILE_PREFIX, md5_str)
    res_path = 'res/' + small_file_name
    icon_path = get_neox_dir() + '/' + get_download_target_path(res_path)
    return (
     small_file_name, icon_path)


def cal_and_set_cover_node(file_name, node, mode=SCALE_MODE_CLIP, resize_parent=False, parent_node=None, sprite_obj=None):
    if not node or not node.isValid():
        return False
    import cc
    if file_name:
        sprite_obj = cc.Sprite.create(file_name)
    if not sprite_obj:
        log_error('[cal_and_set_cover_node] sprite create failed: %s' % file_name)
        return False
    sprite_obj.setAnchorPoint(cc.Vec2(0.5, 0.5))
    size_parent = node.getContentSize()
    size_sprite = sprite_obj.getTextureRect()
    if mode == SCALE_MODE_CLIP:
        scale = max(size_parent.width / size_sprite.width, size_parent.height / size_sprite.height)
    else:
        scale = min(size_parent.width / size_sprite.width, size_parent.height / size_sprite.height)
    width = size_parent.width
    height = size_parent.height
    if resize_parent and parent_node:
        width = min(width, size_sprite.width * scale)
        height = min(height, size_sprite.height * scale)
        node.setContentSize(cc.Size(width, height))
    node.addChild(sprite_obj)
    sprite_obj.setScale(scale)
    sprite_obj.setAnchorPoint(cc.Vec2(0.5, 0.5))
    sprite_obj.setPosition(cc.Vec2(width * 0.5, height * 0.5))
    return True


def is_enough_memory():
    if is_android():
        available_memory = game3d.get_available_memory()
        return available_memory >= MEMORY_NEED
    else:
        return True


def can_record_video():
    if not is_enough_memory():
        global_data.game_mgr.show_tip(get_text_by_id(3132))
        return False
    if game3d.is_outlaw_device():
        global_data.game_mgr.show_tip(get_text_by_id(3133))
        return False
    return True


def close_free_record(need_save=False):
    global_data.ui_mgr.close_ui('FreeRecordUI')
    from logic.comsys.video.VideoRecord import VideoRecord
    VideoRecord().stop_free_record(need_save=need_save)


def close_and_show_free_record_ui():
    close_free_record(need_save=False)
    from logic.comsys.setting_ui.FreeRecordUI import FreeRecordUI
    FreeRecordUI()


def show_world_chat(channel):
    ui = global_data.ui_mgr.get_ui('MainChat')
    if not ui or ui.is_chat_open():
        return
    ui.do_show_panel()
    ui.chat_open()
    ui.touch_channel_btn(channel)


def send_video_msg_to_world(channel, msg, extra_data):
    global_data.ui_mgr.close_ui('MyVideoUI')
    global_data.ui_mgr.close_ui('MainSettingUI')
    global_data.player.send_msg(channel, msg, extra=extra_data)
    show_world_chat(channel)


def send_video_msg_to_friend(f_data, msg, extra_data):
    if global_data.message_data and global_data.player:
        from common.const.property_const import U_ID, C_NAME, U_LV, CLAN_ID
        from logic.comsys.message.MainFriend import FRIEND_TAB_RELATIONSHIP
        global_data.ui_mgr.close_ui('MyVideoUI')
        global_data.ui_mgr.close_ui('MainSettingUI')

        def ui_init_finish_cb():
            sub_panel = friend_ui.touch_tab_by_index(0)
            sub_panel.click_uid_button(f_data[U_ID])
            global_data.message_data.recv_to_friend_msg(f_data[U_ID], f_data[C_NAME], msg, f_data[U_LV], extra=extra_data)
            global_data.player.req_friend_msg(f_data[U_ID], f_data[U_LV], f_data.get(CLAN_ID, -1), msg, extra=extra_data)

        friend_ui = global_data.ui_mgr.get_ui('MainFriend')
        if friend_ui:
            ui_init_finish_cb()
            return
        friend_ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
        friend_ui.set_ui_init_finish_cb(FRIEND_TAB_RELATIONSHIP, ui_init_finish_cb)


def is_high_light_support():
    return False


def high_light_share_num_limited():
    if not global_data.player:
        return True
    from logic.gcommon.const import FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT
    uploaded_num = global_data.player.get_file_day_upload_num(FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT)
    return uploaded_num >= MAX_SHARE_DAY_NUM


def upload_record_suc_info_to_sa(video_key):
    if not global_data.player or not global_data.player.uid:
        return
    from logic.gutils.salog import SALog
    from logic.gcommon.time_utility import get_server_time, get_time_string
    date_key = 'high_light_record_day_time' if video_key == HIGH_KEY else 'free_record_day_time'
    sa_key = SALog.HIGH_LIGHT_VIDEO_RECORD_SUC if video_key == HIGH_KEY else SALog.FREE_VIDEO_RECORD_SUC
    last_day_time = global_data.achi_mgr.get_cur_user_archive_data(date_key, default=0)
    now_day_time = get_time_string('%d', get_server_time())
    if last_day_time != now_day_time:
        global_data.achi_mgr.set_cur_user_archive_data(date_key, now_day_time)
        SALog.get_instance().write(sa_key)


def upload_share_suc_info_to_sa(video_key, platform=''):
    from logic.gutils.salog import SALog
    from logic.gcommon.time_utility import get_server_time, get_time_string
    date_key = 'high_light_share_day_time' if video_key == HIGH_KEY else 'free_share_day_time'
    sa_key = SALog.HIGH_LIGHT_VIDEO_SHARE_SUC if video_key == HIGH_KEY else SALog.FREE_VIDEO_SHARE_SUC
    last_day_time = global_data.achi_mgr.get_cur_user_archive_data(date_key, default=0)
    now_day_time = get_time_string('%d', get_server_time())
    if last_day_time != now_day_time:
        global_data.achi_mgr.set_cur_user_archive_data(date_key, now_day_time)
        info = {'role_id': global_data.player or '' if 1 else global_data.player.uid,
           'platform': platform
           }
        SALog.get_instance().write(sa_key, info)