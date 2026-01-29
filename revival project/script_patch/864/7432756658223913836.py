# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/clan_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gcommon.common_const import clan_const
import logic.gcommon.const as gconst
from logic.gutils import system_unlock_utils
CLAN_HOME_PAGE = 1
CLAN_MEMBER_LIST = 2
CLAN_TASK_LIST = 3
CLAN_APPLY_LIST = 4
CLAN_RANK_BOARD = 5
CLAN_MALL = 6
CLAN_JOIN_LIST = 10
CLAN_CREATE_PAGE = 11
CLAN_RANK_SCORE = 20
CLAN_RANK_FASHION = 21

def get_clan_cls(cls_name):
    mod = __import__('logic.comsys.clan.%s' % cls_name, globals(), locals(), [cls_name])
    cls = getattr(mod, cls_name, None)
    return cls


def get_uncreated_page_list():
    tab_list = [{'key': CLAN_JOIN_LIST,'name': 800020,'template': 'crew/i_crew_join','class': 'ClanJoinPageUI'}, {'key': CLAN_CREATE_PAGE,'name': 800021,'template': 'crew/i_crew_create','class': 'ClanCreatePageUI'}, {'key': CLAN_RANK_BOARD,'name': 80270,'template': 'crew/i_crew_rank','class': 'ClanRankPage'}]
    return tab_list


def get_created_page_list():
    tab_list = [{'key': CLAN_HOME_PAGE,'name': 800037,'template': 'crew/i_crew_homepage','class': 'ClanHomePage'}, {'key': CLAN_MEMBER_LIST,'name': 800038,'template': 'crew/i_crew_member','class': 'ClanMemberList'}, {'key': CLAN_TASK_LIST,'name': 80841,'template': 'task/i_crew_task','class': 'ClanTaskList'}, {'key': CLAN_MALL,'name': 634222,'template': 'crew/i_crew_logistics','class': 'ClanMall'}, {'key': CLAN_RANK_BOARD,'name': 80270,'template': 'crew/i_crew_rank','class': 'ClanRankPage'}]
    if get_permission('audit_permission_titles'):
        tab_list.append({'key': CLAN_APPLY_LIST,'name': 10275,'template': 'crew/i_crew_application','class': 'ClanApplyList'})
    return tab_list


def get_clan_rank_page_list():
    tab_list = [{'key': CLAN_RANK_SCORE,'name': 800069,'template': 'crew/i_crew_rank_score','class': 'ClanRankScore'}, {'key': CLAN_RANK_FASHION,'name': 15018,'template': 'crew/i_crew_rank_fashion','class': 'ClanRankFashion'}]
    return tab_list


def get_clan_title_text(title):
    text_ids = {str(clan_const.COMMANDER): 800027,
       str(clan_const.MINISTER): 800040,
       str(clan_const.ADMIN): 800041,
       str(clan_const.MASS): 800042
       }
    return text_ids.get(str(title), 800042)


def get_clan_title_icon(title):
    path_map = {str(clan_const.COMMANDER): 'gui/ui_res_2/crew/icon_commander.png',
       str(clan_const.MINISTER): 'gui/ui_res_2/crew/icon_deputy_commander.png',
       str(clan_const.ADMIN): 'gui/ui_res_2/crew/icon_admin.png',
       str(clan_const.MASS): ''
       }
    return path_map.get(str(title), '')


def get_clan_max_lv():
    max_lv = 0
    clan_lv_data = confmgr.get('clan_lv_data')
    for info in clan_lv_data:
        if type(info) != dict:
            continue
        if info['iLv'] > max_lv:
            max_lv = info['iLv']

    return max_lv


def get_clan_person_limit(lv):
    return confmgr.get('clan_lv_data', str(lv), 'iMember', default=0)


def get_clan_lv_exp(lv):
    return confmgr.get('clan_lv_data', str(lv), 'iPoint', default=0)


def get_clan_title_count_limit(lv, title):
    title_map = {clan_const.COMMANDER: 'iCommander',
       clan_const.MINISTER: 'iMinister',
       clan_const.ADMIN: 'iAdmin',
       clan_const.MASS: ''
       }
    if title == clan_const.MASS:
        members_count = confmgr.get('clan_lv_data', str(lv), 'iMember', default=0)
        return members_count
    return confmgr.get('clan_lv_data', str(lv), title_map.get(title, ''), default=0)


def get_my_clan_title_count_limit(title):
    lv = global_data.player.get_clan_lv()
    return get_clan_title_count_limit(lv, title)


def get_my_clan_info_by_field(field, default=0):
    info = global_data.player.get_my_clan_info()
    return info.get(field, default)


def is_clan_commander():
    my_title = get_my_clan_info_by_field('title')
    if my_title == clan_const.COMMANDER:
        return True
    else:
        return False


def get_clan_member_info_by_field(uid, field, default=0):
    info = global_data.player.get_member_clan_info(uid)
    return info.get(field, default)


def get_clan_title_count(title):
    count = 0
    member_list = global_data.player.get_clan_member_list()
    for i, info in enumerate(member_list):
        if title == info['title']:
            count += 1

    return count


def get_permission--- This code section failed: ---

 141       0  LOAD_GLOBAL           0  'get_my_clan_info_by_field'
           3  LOAD_CONST            1  'title'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            3  'my_title'

 142      12  LOAD_FAST             1  'title'
          15  LOAD_CONST            0  ''
          18  COMPARE_OP            3  '!='
          21  POP_JUMP_IF_FALSE    43  'to 43'

 143      24  LOAD_FAST             3  'my_title'
          27  LOAD_FAST             1  'title'
          30  COMPARE_OP            5  '>='
          33  POP_JUMP_IF_FALSE    43  'to 43'

 144      36  LOAD_GLOBAL           2  'False'
          39  RETURN_END_IF    
        40_0  COME_FROM                '33'
          40  JUMP_FORWARD          0  'to 43'
        43_0  COME_FROM                '40'

 146      43  LOAD_GLOBAL           3  'confmgr'
          46  LOAD_ATTR             4  'get'
          49  LOAD_CONST            2  'clan_data'
          52  LOAD_CONST            3  'default'
          55  BUILD_LIST_0          0 
          58  CALL_FUNCTION_258   258 
          61  STORE_FAST            4  'permission_list'

 147      64  LOAD_FAST             3  'my_title'
          67  LOAD_FAST             4  'permission_list'
          70  COMPARE_OP            6  'in'
          73  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 58


def _set_permission_func--- This code section failed: ---

 150       0  LOAD_GLOBAL           0  'get_permission'
           3  LOAD_FAST             0  'key'
           6  LOAD_FAST             2  'kwargs'
           9  CALL_FUNCTION_KW_1     1 
          12  STORE_FAST            3  'has_permission'

 151      15  LOAD_FAST             3  'has_permission'
          18  POP_JUMP_IF_TRUE     53  'to 53'

 152      21  POP_JUMP_IF_TRUE      1  'to 1'
          24  COMPARE_OP            2  '=='
          27  POP_JUMP_IF_FALSE    49  'to 49'

 153      30  LOAD_GLOBAL           1  'global_data'
          33  LOAD_ATTR             2  'game_mgr'
          36  LOAD_ATTR             3  'show_tip'
          39  LOAD_CONST            2  '\xe5\x8f\xaa\xe8\x83\xbd\xe8\xb0\x83\xe6\x95\xb4\xe4\xb8\x8b\xe7\xba\xa7\xe8\x81\x8c\xe5\x8a\xa1'
          42  CALL_FUNCTION_1       1 
          45  POP_TOP          
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

 154      49  LOAD_CONST            0  ''
          52  RETURN_END_IF    
        53_0  COME_FROM                '21'
        53_1  COME_FROM                '18'

 155      53  LOAD_FAST             1  'callback'
          56  CALL_FUNCTION_0       0 
          59  POP_TOP          

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 21


def _set_permission_widget(key, btn, btn_enable=True, set_visible=False, **kwargs):
    has_permission = get_permission(key, **kwargs)
    if btn_enable:
        btn.SetEnable(has_permission)
    if set_visible:
        btn.setVisible(has_permission)


def set_permission(key, void, **kwargs):
    if callable(void):
        _set_permission_func(key, void, **kwargs)
    else:
        _set_permission_widget(key, void, **kwargs)


def has_level_red_point():
    has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_CLAN)
    if not has_unlock:
        return False
    red_point_lv = 5
    lv = global_data.player.get_lv()
    first_visit_lv = global_data.achi_mgr.get_cur_user_archive_data('clan_level_red_point', default=1)
    return first_visit_lv < red_point_lv and lv >= red_point_lv


def set_first_visit_entry_lv():
    lv = global_data.player.get_lv()
    global_data.achi_mgr.set_cur_user_archive_data('clan_level_red_point', lv)


def get_clan_task_ids():
    task_ids = []
    for task_id, conf in six.iteritems(confmgr.get('task/clan_task_data')):
        if not conf.get('need_hide', 0):
            task_ids.append(task_id)

    return task_ids


def get_clan_redpoint_count():
    count = 0
    has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_CLAN)
    if not has_unlock:
        return count
    if not global_data.player.is_in_clan():
        return count
    count += get_clan_rank_reward_count()
    count += get_clan_task_redpoint_count()
    count += get_clan_new_intro_count()
    return count


def get_clan_new_intro_count():
    if not global_data.player.is_in_clan():
        return 0
    if global_data.player.new_clan_intro:
        return 1
    return 0


def get_clan_rank_reward_count():
    from logic.gcommon.common_const import rank_const
    count = 0
    rank_types = [
     rank_const.RANK_TYPE_CLAN_WEEK_POINT, rank_const.RANK_TYPE_CLAN_SEASON_POINT]
    for rank_type in rank_types:
        if global_data.player.is_offer_clan_rank_reward(rank_type):
            count += 1

    return count


def get_clan_task_redpoint_count():
    if not global_data.player.is_in_clan():
        return 0
    count = get_clan_task_reward_count()
    count += get_clan_vitality_reward_count()
    return count


def get_clan_apply_count():
    if not global_data.player.is_in_clan():
        return 0
    if not get_permission('audit_permission_titles'):
        return 0
    if global_data.player.get_request_member_list():
        return 1
    return 0


def get_clan_task_reward_count():
    from logic.gutils import task_utils
    from logic.gcommon.item.item_const import ITEM_UNRECEIVED
    if not global_data.player.is_in_clan():
        return 0
    count = 0
    task_ids = get_clan_task_ids()
    for task_id in task_ids:
        task_conf = task_utils.get_task_conf_by_id(task_id)
        if not task_conf:
            continue
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_UNRECEIVED:
            count += 1

    return count


def get_clan_vitality_reward_count():
    from logic.gcommon.item import item_const
    from logic.gcommon.cdata import clan_point_reward_conf
    if not global_data.player.is_in_clan():
        return 0
    count = 0
    max_vitality_level = clan_point_reward_conf.get_week_vitality_count()
    for lv in range(1, max_vitality_level + 1):
        reward_st = global_data.player.get_week_clan_reward_st(lv)
        if reward_st == item_const.ITEM_UNRECEIVED:
            count += 1

    return count


def is_active_clan--- This code section failed: ---

 282       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('time_utility',)
           6  IMPORT_NAME           0  'logic.gcommon'
           9  IMPORT_FROM           1  'time_utility'
          12  STORE_FAST            2  'tutil'
          15  POP_TOP          

 284      16  LOAD_GLOBAL           2  'confmgr'
          19  LOAD_ATTR             3  'get'
          22  LOAD_CONST            3  'clan_active_conf'
          25  LOAD_GLOBAL           4  'str'
          28  LOAD_GLOBAL           5  'global_data'
          31  LOAD_ATTR             6  'channel'
          34  LOAD_ATTR             7  'get_host_num'
          37  CALL_FUNCTION_0       0 
          40  CALL_FUNCTION_1       1 
          43  LOAD_CONST            4  'default'
          46  LOAD_CONST            0  ''
          49  CALL_FUNCTION_258   258 
          52  STORE_FAST            3  'clan_active_data'

 285      55  LOAD_FAST             3  'clan_active_data'
          58  POP_JUMP_IF_TRUE     65  'to 65'

 286      61  LOAD_GLOBAL           9  'False'
          64  RETURN_END_IF    
        65_0  COME_FROM                '58'

 288      65  LOAD_FAST             1  'day_no'
          68  LOAD_CONST            0  ''
          71  COMPARE_OP            8  'is'
          74  POP_JUMP_IF_FALSE    89  'to 89'
          77  LOAD_FAST             2  'tutil'
          80  LOAD_ATTR            10  'get_rela_day_no'
          83  CALL_FUNCTION_0       0 
          86  JUMP_FORWARD          3  'to 92'
          89  LOAD_FAST             1  'day_no'
        92_0  COME_FROM                '86'
          92  STORE_FAST            1  'day_no'

 289      95  LOAD_FAST             0  'clan_info'
          98  LOAD_ATTR             3  'get'
         101  LOAD_CONST            5  'active_dayno'
         104  LOAD_CONST            1  ''
         107  CALL_FUNCTION_2       2 
         110  STORE_FAST            4  'active_dayno'

 290     113  LOAD_FAST             1  'day_no'
         116  LOAD_FAST             4  'active_dayno'
         119  BINARY_SUBTRACT  
         120  LOAD_GLOBAL          11  'clan_const'
         123  LOAD_ATTR            12  'CLAN_ACTIVE_DAY'
         126  COMPARE_OP            4  '>'
         129  POP_JUMP_IF_FALSE   136  'to 136'

 291     132  LOAD_GLOBAL           9  'False'
         135  RETURN_END_IF    
       136_0  COME_FROM                '129'

 293     136  LOAD_FAST             0  'clan_info'
         139  LOAD_ATTR             3  'get'
         142  LOAD_CONST            6  'active'
         145  LOAD_CONST            1  ''
         148  CALL_FUNCTION_2       2 
         151  STORE_FAST            5  'active'

 294     154  LOAD_FAST             5  'active'
         157  LOAD_FAST             3  'clan_active_data'
         160  LOAD_CONST            7  'active_limit'
         163  BINARY_SUBSCR    
         164  COMPARE_OP            0  '<'
         167  POP_JUMP_IF_FALSE   174  'to 174'

 295     170  LOAD_GLOBAL           9  'False'
         173  RETURN_END_IF    
       174_0  COME_FROM                '167'

 297     174  LOAD_CONST            8  'member_list'
         177  LOAD_FAST             0  'clan_info'
         180  COMPARE_OP            6  'in'
         183  POP_JUMP_IF_FALSE   202  'to 202'

 298     186  LOAD_GLOBAL          13  'len'
         189  LOAD_GLOBAL           8  'None'
         192  BINARY_SUBSCR    
         193  CALL_FUNCTION_1       1 
         196  STORE_FAST            6  'member_num'
         199  JUMP_FORWARD         18  'to 220'

 300     202  LOAD_FAST             0  'clan_info'
         205  LOAD_ATTR             3  'get'
         208  LOAD_CONST            9  'member_num'
         211  LOAD_CONST            1  ''
         214  CALL_FUNCTION_2       2 
         217  STORE_FAST            6  'member_num'
       220_0  COME_FROM                '199'

 302     220  LOAD_FAST             5  'active'
         223  LOAD_FAST             6  'member_num'
         226  LOAD_CONST           10  5
         229  BINARY_MULTIPLY  
         230  LOAD_CONST           11  6
         233  BINARY_DIVIDE    
         234  COMPARE_OP            1  '<='
         237  POP_JUMP_IF_FALSE   244  'to 244'

 303     240  LOAD_GLOBAL           9  'False'
         243  RETURN_END_IF    
       244_0  COME_FROM                '237'

 305     244  LOAD_GLOBAL          14  'True'
         247  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 193


def get_apply_active_limit--- This code section failed: ---

 308       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'clan_active_conf'
           9  LOAD_GLOBAL           2  'str'
          12  LOAD_GLOBAL           3  'global_data'
          15  LOAD_ATTR             4  'channel'
          18  LOAD_ATTR             5  'get_host_num'
          21  CALL_FUNCTION_0       0 
          24  CALL_FUNCTION_1       1 
          27  LOAD_CONST            2  'default'
          30  LOAD_CONST            0  ''
          33  CALL_FUNCTION_258   258 
          36  STORE_FAST            0  'clan_active_data'

 309      39  LOAD_FAST             0  'clan_active_data'
          42  POP_JUMP_IF_TRUE     49  'to 49'

 310      45  LOAD_CONST            3  ''
          48  RETURN_END_IF    
        49_0  COME_FROM                '42'

 311      49  RETURN_VALUE     
          50  RETURN_VALUE     
          51  RETURN_VALUE     
          52  BINARY_SUBSCR    
          53  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 49


def get_quit_active_limit--- This code section failed: ---

 314       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'clan_active_conf'
           9  LOAD_GLOBAL           2  'str'
          12  LOAD_GLOBAL           3  'global_data'
          15  LOAD_ATTR             4  'channel'
          18  LOAD_ATTR             5  'get_host_num'
          21  CALL_FUNCTION_0       0 
          24  CALL_FUNCTION_1       1 
          27  LOAD_CONST            2  'default'
          30  LOAD_CONST            0  ''
          33  CALL_FUNCTION_258   258 
          36  STORE_FAST            0  'clan_active_data'

 315      39  LOAD_FAST             0  'clan_active_data'
          42  POP_JUMP_IF_TRUE     49  'to 49'

 316      45  LOAD_CONST            3  ''
          48  RETURN_END_IF    
        49_0  COME_FROM                '42'

 317      49  RETURN_VALUE     
          50  RETURN_VALUE     
          51  RETURN_VALUE     
          52  BINARY_SUBSCR    
          53  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 49