# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/pve_lobby_utils.py
from __future__ import absolute_import
from logic.gcommon.common_const.pve_const import PVE_BOOK_KEY, DIFFICUTY_LIST, PVE_STORY_DEBRIS_CACHE
from logic.gutils.item_utils import get_lobby_item_name, payment_item_pic
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from common.cfg import confmgr
import six_ex

def check_pve_ext_entry():
    if not global_data.enable_pve:
        global_data.game_mgr.show_tip(get_text_by_id(10063))
        return False
    from ext_package.ext_decorator import has_skin_ext, has_pve_ext
    if not has_skin_ext():
        global_data.game_mgr.show_tip(get_text_by_id(635076))
        return False
    if not has_pve_ext(1):
        global_data.game_mgr.show_tip(get_text_by_id(635076))
        return False
    return True


def get_debris_chapter_is_finished(chapter_id):
    chapter_debris_conf = confmgr.get('story_debris_chapter_data', str(chapter_id))
    clue_list = chapter_debris_conf.get('clue')
    conf = confmgr.get('story_debris_clue_data')
    for clue_id in clue_list:
        clue_conf = conf.get(str(clue_id))
        debris_list = clue_conf.get('debris')
        is_own = True
        for debris_no in debris_list:
            is_own = bool(global_data.player and global_data.player.get_item_by_no(debris_no))
            if not is_own:
                return False

    return True


def get_debris_clue_is_finished(clue_id):
    clue_conf = confmgr.get('story_debris_clue_data').get(str(clue_id))
    debris_list = clue_conf.get('debris')
    all_count = len(debris_list)
    finish_count = 0
    for debris_no in debris_list:
        is_own = bool(global_data.player and global_data.player.get_item_by_no(debris_no))
        if not is_own:
            break
        finish_count += 1

    return finish_count == all_count


def init_story_debris_item(item, item_no, item_num, need_show_red_point=True):
    item.lab_name.SetString(get_lobby_item_name(item_no))
    lab_num = item.lab_num
    nd_lock = item.nd_lock
    if item_num > 0:
        lab_num.SetString('\xc3\x97{}'.format(item_num))
        lab_num.setVisible(True)
        nd_lock and nd_lock.setVisible(False)
    else:
        lab_num.setVisible(False)
        nd_lock and nd_lock.setVisible(True)
    item.img_item.SetDisplayFrameByPath('', payment_item_pic(item_no))
    pve_story_debris_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_STORY_DEBRIS_CACHE, [])
    has_item = bool(global_data.player and global_data.player.get_item_num_by_no(int(item_no)))
    item.img_tag.setVisible(has_item and int(item_no) not in pve_story_debris_cache and need_show_red_point)
    btn_item = item.btn_item
    btn_item and btn_item.EnableCustomState(True)


def check_chapter_difficulty_monster_book_redpoint(monster_id, chapter, difficulty, cache_data=None):
    if not global_data.player:
        return False
    if not global_data.player.has_unlock_difficulty_monster_book(difficulty, monster_id):
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    monster_cache_key = '%s_%s_%s' % (monster_id, chapter, difficulty)
    return monster_cache_key not in cache_data


def check_chapter_monster_book_redpoint(chapter, cache_data=None):
    if not global_data.player:
        return False
    pve_all_chapter_kill_monster_cnt = global_data.player.get_pve_all_chapter_kill_monster_cnt()
    if not pve_all_chapter_kill_monster_cnt:
        return False
    pve_chapter_kill_monster_cnt = pve_all_chapter_kill_monster_cnt.get(chapter, {})
    if not pve_chapter_kill_monster_cnt:
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    for difficulty, monster_kill_data in six_ex.items(pve_chapter_kill_monster_cnt):
        if type(monster_kill_data) != dict:
            continue
        monster_id_list = six_ex.keys(monster_kill_data)
        if not monster_id_list:
            continue
        for monster_id in monster_id_list:
            if check_chapter_difficulty_monster_book_redpoint(monster_id, chapter, difficulty, cache_data):
                return True

    return False


def check_monster_book_redpoint(cache_data=None):
    if not global_data.player:
        return False
    pve_all_chapter_kill_monster_cnt = global_data.player.get_pve_all_chapter_kill_monster_cnt()
    if not pve_all_chapter_kill_monster_cnt:
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    for chapter, chapter_kill_info in six_ex.items(pve_all_chapter_kill_monster_cnt):
        if check_chapter_monster_book_redpoint(chapter, cache_data):
            return True

    return False


def check_bless_book_redpoint(bless_id, cache_data=None):
    if not global_data.player:
        return False
    if not global_data.player.has_unlock_bless_book(bless_id):
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    bless_cache_key = str(bless_id)
    return bless_cache_key not in cache_data


def check_bless_type_book_redpoint(bless_type=None, cache_data=None):
    if not global_data.player:
        return False
    else:
        all_unlock_blesses_data = global_data.player.get_all_choose_blesses_cnt()
        if not all_unlock_blesses_data:
            return False
        if not cache_data:
            cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        all_bless_conf = confmgr.get('bless_data', default={})
        all_unlock_blesses_id_list = six_ex.keys(all_unlock_blesses_data)
        for bless_id in all_unlock_blesses_id_list:
            bless_conf = all_bless_conf.get(str(bless_id))
            if not bless_conf or bless_conf.get('limit_inner', 0) == 1:
                continue
            if bless_conf.get('belong_type_id') == bless_type or bless_type == None:
                if check_bless_book_redpoint(bless_id, cache_data):
                    return True

        return False


def check_all_bless_book_redpoint(cache_data=None):
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    return check_bless_type_book_redpoint(cache_data=cache_data)


def check_mecha_break_slot_book_redpoint(mecha_id, slot_id, cache_data=None):
    if not global_data.player:
        return False
    if not global_data.player.has_unlock_breakthrough_book(mecha_id, slot_id):
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    break_cache_key = '%s_%s' % (mecha_id, slot_id)
    return break_cache_key not in cache_data


def check_mecha_break_book_redpoint(mecha_id, cache_data=None):
    if not global_data.player:
        return False
    all_unlock_break_data = global_data.player.get_all_choose_breakthrough_cnt()
    if not all_unlock_break_data:
        return False
    mecha_unlock_break_data = all_unlock_break_data.get(str(mecha_id))
    if not mecha_unlock_break_data:
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    all_unlock_slot_id_list = six_ex.keys(mecha_unlock_break_data)
    for slot_id in all_unlock_slot_id_list:
        if check_mecha_break_slot_book_redpoint(mecha_id, slot_id, cache_data):
            return True

    return False


def check_all_mecha_break_book_redpoint(cache_data=None):
    if not global_data.player:
        return False
    all_unlock_break_data = global_data.player.get_all_choose_breakthrough_cnt()
    if not all_unlock_break_data:
        return False
    if not cache_data:
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    mecha_id_list = six_ex.keys(all_unlock_break_data)
    for mecha_id in mecha_id_list:
        if check_mecha_break_book_redpoint(mecha_id, cache_data):
            return True

    return False


def check_pve_book_redpoint():
    cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
    has_monster_redpoint = check_monster_book_redpoint(cache_data)
    if has_monster_redpoint:
        return True
    has_bless_redpoint = check_all_bless_book_redpoint(cache_data)
    if has_bless_redpoint:
        return True
    has_break_redpoint = check_all_mecha_break_book_redpoint(cache_data)
    return has_break_redpoint


def get_pve_all_career_parent_task_list--- This code section failed: ---

 269       0  BUILD_LIST_0          0 
           3  STORE_FAST            0  'parent_task_list'

 270       6  LOAD_GLOBAL           0  'confmgr'
           9  LOAD_ATTR             1  'get'
          12  LOAD_CONST            1  'task/pve_career_task_data'
          15  LOAD_CONST            2  'default'
          18  BUILD_MAP_0           0 
          21  CALL_FUNCTION_257   257 
          24  STORE_FAST            1  'conf'

 271      27  SETUP_LOOP           69  'to 99'
          30  LOAD_GLOBAL           2  'six_ex'
          33  LOAD_ATTR             3  'items'
          36  LOAD_FAST             1  'conf'
          39  CALL_FUNCTION_1       1 
          42  GET_ITER         
          43  FOR_ITER             52  'to 98'
          46  UNPACK_SEQUENCE_2     2 
          49  STORE_FAST            2  'task_id'
          52  STORE_FAST            3  'task_info'

 272      55  LOAD_FAST             3  'task_info'
          58  LOAD_ATTR             1  'get'
          61  LOAD_CONST            3  'auto_regist'
          64  LOAD_CONST            4  ''
          67  CALL_FUNCTION_2       2 
          70  LOAD_CONST            5  1
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_FALSE    43  'to 43'

 273      79  LOAD_FAST             0  'parent_task_list'
          82  LOAD_ATTR             4  'append'
          85  LOAD_FAST             2  'task_id'
          88  CALL_FUNCTION_1       1 
          91  POP_TOP          
          92  JUMP_BACK            43  'to 43'
          95  JUMP_BACK            43  'to 43'
          98  POP_BLOCK        
        99_0  COME_FROM                '27'

 275      99  LOAD_FAST             0  'parent_task_list'
         102  LOAD_ATTR             5  'sort'
         105  CALL_FUNCTION_0       0 
         108  POP_TOP          

 276     109  LOAD_FAST             0  'parent_task_list'
         112  POP_JUMP_IF_FALSE   120  'to 120'

 277     115  POP_JUMP_IF_FALSE     4  'to 4'
         118  BINARY_SUBSCR    
         119  RETURN_END_IF    
       120_0  COME_FROM                '115'
       120_1  COME_FROM                '112'

 278     120  LOAD_CONST            0  ''
         123  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 115


def get_pve_chapter_career_parent_task_list--- This code section failed: ---

 282       0  BUILD_LIST_0          0 
           3  STORE_FAST            0  'parent_task_list'

 283       6  LOAD_GLOBAL           0  'confmgr'
           9  LOAD_ATTR             1  'get'
          12  LOAD_CONST            1  'task/pve_career_task_data'
          15  LOAD_CONST            2  'default'
          18  BUILD_MAP_0           0 
          21  CALL_FUNCTION_257   257 
          24  STORE_FAST            1  'conf'

 284      27  SETUP_LOOP           69  'to 99'
          30  LOAD_GLOBAL           2  'six_ex'
          33  LOAD_ATTR             3  'items'
          36  LOAD_FAST             1  'conf'
          39  CALL_FUNCTION_1       1 
          42  GET_ITER         
          43  FOR_ITER             52  'to 98'
          46  UNPACK_SEQUENCE_2     2 
          49  STORE_FAST            2  'task_id'
          52  STORE_FAST            3  'task_info'

 285      55  LOAD_FAST             3  'task_info'
          58  LOAD_ATTR             1  'get'
          61  LOAD_CONST            3  'auto_regist'
          64  LOAD_CONST            4  ''
          67  CALL_FUNCTION_2       2 
          70  LOAD_CONST            5  1
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_FALSE    43  'to 43'

 286      79  LOAD_FAST             0  'parent_task_list'
          82  LOAD_ATTR             4  'append'
          85  LOAD_FAST             2  'task_id'
          88  CALL_FUNCTION_1       1 
          91  POP_TOP          
          92  JUMP_BACK            43  'to 43'
          95  JUMP_BACK            43  'to 43'
          98  POP_BLOCK        
        99_0  COME_FROM                '27'

 288      99  LOAD_FAST             0  'parent_task_list'
         102  LOAD_ATTR             5  'sort'
         105  CALL_FUNCTION_0       0 
         108  POP_TOP          

 289     109  LOAD_FAST             0  'parent_task_list'
         112  POP_JUMP_IF_FALSE   122  'to 122'

 290     115  POP_JUMP_IF_FALSE     4  'to 4'
         118  DELETE_SUBSCR    
         119  JUMP_FORWARD          0  'to 122'
       122_0  COME_FROM                '119'

 291     122  LOAD_FAST             0  'parent_task_list'
         125  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 115


def get_pve_career_task_state(task_id, task_level):
    from logic.gcommon.item.item_const import ITEM_RECEIVED
    if not task_id or not task_level:
        return ITEM_RECEIVED
    prog_reward_list = task_utils.get_prog_rewards(task_id)
    if prog_reward_list:
        prog = prog_reward_list[task_level - 1][0]
        status = task_utils.get_prog_task_status_info(task_id, prog)
    else:
        status, _, _, _ = task_utils.get_task_status_info(task_id)
    return status


def get_pve_career_degree(task_id, task_level):
    from common.utilities import get_rome_num
    if not task_id or not task_level:
        return 0
    task_conf = task_utils.get_task_conf_by_id(task_id)
    degree_list = task_conf.get('degree')
    degree = degree_list[task_level - 1]
    return int(degree)


def get_pve_career_format_text(task_id, task_level):
    from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST
    from logic.gutils.item_utils import get_mecha_name_by_id
    from logic.gutils.career_utils import get_badge_career_pts_reward_segs_readonly
    import copy
    task_conf = copy.deepcopy(task_utils.get_task_conf_by_id(task_id))
    task_template_conf = task_utils.get_task_temp_conf_by_id(task_id)
    name_id = task_conf.get('name', None)
    if name_id:
        name_text = get_text_by_id(name_id)
    else:
        tmp_name_id = task_template_conf.get('text_id', '')
        if not tmp_name_id:
            return ''
        name_text = get_text_by_id(tmp_name_id)
    desc_id = task_conf.get('desc', '')
    desc_text = ''
    if desc_id:
        desc_text = get_text_by_id(desc_id)
    name_text = name_text + desc_text
    text_param_dict = task_conf.get('arg')
    if not text_param_dict:
        return name_text
    else:
        for key, text_param in six_ex.items(text_param_dict):
            if key == 'chapter':
                conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(text_param))
                text_param_dict[key] = get_text_by_id(conf.get('title_text'))
            elif key == 'difficulty':
                text_param_dict[key] = get_text_by_id(DIFFICULTY_TEXT_LIST[text_param])
            elif key == 'mecha_id':
                text_param_dict[key] = get_mecha_name_by_id(text_param)
            elif key == 'monster_id':
                conf = confmgr.get('monster_data', 'Monster', 'Content', str(text_param))
                text_param_dict[key] = get_text_by_id(conf.get('NameText'))

        segs = get_badge_career_pts_reward_segs_readonly(task_id)
        if len(segs) >= task_level:
            index = task_level - 1
            text_param_dict['prog'] = segs[index][0]
        try:
            return name_text.format(**text_param_dict)
        except:
            print (
             '[Error] invalid text format, task_id = ', task_id)
            return str(task_id)

        return