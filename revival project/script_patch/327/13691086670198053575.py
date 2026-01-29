# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/red_point_utils.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.utils.redpoint_check_func import check_lobby_red_point
from logic.gcommon.const import PRIVILEGE_SETTING_TO_RED_POINT, PRIVILEGE_LEVEL_TO_SETTING
import game3d
RED_POINT_LEVEL_10 = 10
RED_POINT_LEVEL_20 = 20
RED_POINT_LEVEL_30 = 30
red_point_path = {RED_POINT_LEVEL_10: 'gui/ui_res_2/txt_pic/text_pic_en/img_tips_new.png',
   RED_POINT_LEVEL_20: 'gui/ui_res_2/main/img_red_small.png',
   RED_POINT_LEVEL_30: 'gui/ui_res_2/main/pnl_new_tips.png'
   }
default_path = 'gui/ui_res_2/main/pnl_new_tips.png'

def show_red_point_template(node, visible, level=RED_POINT_LEVEL_10, play_anim=False):
    visible = bool(visible)
    if not node:
        return
    node.setVisible(visible)
    img_path = red_point_path.get(level, default_path)
    node.img_red.SetDisplayFrameByPath('', img_path)


def show_red_point_img(node, visible, level=RED_POINT_LEVEL_10):
    visible = bool(visible)
    node.setVisible(visible)
    if visible:
        img_path = red_point_path.get(level, default_path)
        node.SetDisplayFrameByPath('', img_path)


def get_player_info_ui_red():
    from logic.gcommon.item import lobby_item_type
    new_frame = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_PHOTO)
    new_photo = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_FRAME)
    tab_role_rp = new_frame or new_photo
    return tab_role_rp


def get_credit_reward_rd():
    from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_CREDIT
    if not is_sys_unlocked(SYSTEM_CREDIT):
        return False
    else:
        from common.cfg import confmgr
        tab_credit_rp = False
        if global_data.player:
            credit_conf_dict = confmgr.get('credit_conf', 'CreditLevel', 'Content')
            reward_sts = global_data.player.get_credit_reward_sts()
            credit_level = global_data.player.get_credit_level()
            for level in credit_conf_dict:
                reward_id = credit_conf_dict.get(str(level), {}).get('Reward', None)
                if reward_id and int(level) <= int(credit_level) and int(level) not in reward_sts:
                    tab_credit_rp = True
                    break

        return tab_credit_rp


def get_newbie_assessment_rd(node):
    from logic.gutils import task_utils
    parent_task_id = global_data.player.get_newbie_parent_task_id()
    task_list = task_utils.get_children_task(parent_task_id)
    node.setVisible(False)
    if not check_lobby_red_point():
        return
    for task_id in task_list:
        if global_data.player.is_task_finished(task_id) and not global_data.player.has_receive_reward(task_id):
            node.setVisible(True)
            return


def get_priv_setting_rp--- This code section failed: ---

  84       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  POP_JUMP_IF_TRUE     13  'to 13'

  85       9  LOAD_GLOBAL           2  'False'
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

  86      13  LOAD_GLOBAL           0  'global_data'
          16  LOAD_ATTR             1  'player'
          19  LOAD_ATTR             3  'get_privilege_level'
          22  CALL_FUNCTION_0       0 
          25  STORE_FAST            0  'new_lv'

  87      28  LOAD_GLOBAL           2  'False'
          31  STORE_FAST            1  'new_setting'

  88      34  SETUP_LOOP          169  'to 206'
          37  LOAD_GLOBAL           4  'range'
          40  LOAD_CONST            1  1
          43  LOAD_CONST            1  1
          46  BINARY_ADD       
          47  CALL_FUNCTION_2       2 
          50  GET_ITER         
          51  FOR_ITER            151  'to 205'
          54  STORE_FAST            2  'i'

  89      57  LOAD_GLOBAL           5  'PRIVILEGE_LEVEL_TO_SETTING'
          60  LOAD_ATTR             6  'get'
          63  LOAD_FAST             2  'i'
          66  BUILD_LIST_0          0 
          69  CALL_FUNCTION_2       2 
          72  STORE_FAST            3  'priv_settings'

  90      75  LOAD_FAST             3  'priv_settings'
          78  POP_JUMP_IF_FALSE    51  'to 51'

  91      81  SETUP_LOOP          118  'to 202'
          84  LOAD_FAST             3  'priv_settings'
          87  GET_ITER         
          88  FOR_ITER            107  'to 198'
          91  STORE_FAST            4  'setting'

  92      94  LOAD_GLOBAL           7  'PRIVILEGE_SETTING_TO_RED_POINT'
          97  LOAD_FAST             4  'setting'
         100  BINARY_SUBSCR    
         101  LOAD_GLOBAL           8  'str'
         104  LOAD_GLOBAL           0  'global_data'
         107  LOAD_ATTR             1  'player'
         110  LOAD_ATTR             9  'uid'
         113  CALL_FUNCTION_1       1 
         116  BINARY_ADD       
         117  STORE_FAST            5  'setting_red_point'

  93     120  LOAD_GLOBAL           0  'global_data'
         123  LOAD_ATTR            10  'achi_mgr'
         126  LOAD_ATTR            11  'get_cur_user_archive_data'
         129  LOAD_FAST             5  'setting_red_point'
         132  LOAD_CONST            2  'default'
         135  LOAD_CONST            3  -1
         138  CALL_FUNCTION_257   257 
         141  STORE_FAST            6  'state'

  94     144  LOAD_FAST             6  'state'
         147  LOAD_CONST            3  -1
         150  COMPARE_OP            2  '=='
         153  POP_JUMP_IF_TRUE     88  'to 88'
         156  LOAD_FAST             6  'state'
         159  LOAD_CONST            1  1
         162  COMPARE_OP            2  '=='
       165_0  COME_FROM                '153'
         165  POP_JUMP_IF_FALSE   174  'to 174'

  95     168  CONTINUE             88  'to 88'
         171  JUMP_BACK            88  'to 88'

  96     174  LOAD_FAST             6  'state'
         177  LOAD_CONST            4  ''
         180  COMPARE_OP            2  '=='
         183  POP_JUMP_IF_FALSE    88  'to 88'

  97     186  LOAD_GLOBAL          12  'True'
         189  STORE_FAST            1  'new_setting'
         192  JUMP_BACK            88  'to 88'
         195  JUMP_BACK            88  'to 88'
         198  POP_BLOCK        
       199_0  COME_FROM                '81'
         199  JUMP_BACK            51  'to 51'
         202  JUMP_BACK            51  'to 51'
         205  POP_BLOCK        
       206_0  COME_FROM                '34'

  98     206  LOAD_FAST             1  'new_setting'
         209  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 47


def get_LobbyUI_role_head_level():
    if not check_lobby_red_point():
        return 0
    if get_credit_reward_rd():
        return RED_POINT_LEVEL_30
    if global_data.lobby_red_point_data.check_main_rp('role_head_rp'):
        return RED_POINT_LEVEL_10
    return 0


def get_LobbyUI_role_rp_level():
    if not check_lobby_red_point():
        return 0
    from logic.gutils import bond_utils
    if bond_utils.any_role_can_get_gift_reward():
        return RED_POINT_LEVEL_30
    if global_data.lobby_red_point_data.check_main_rp('role_info_rp'):
        return RED_POINT_LEVEL_10
    return 0


def get_LobbyUI_mecha_rp_level():
    if not global_data.player:
        return 0
    if not check_lobby_red_point():
        return 0
    if global_data.player.has_unreceived_prof_reward_all_mecha():
        return RED_POINT_LEVEL_30
    if global_data.lobby_red_point_data.check_main_rp('mecha_info_rp'):
        return RED_POINT_LEVEL_10
    return 0


def get_LobbyUI_item_book_rp_level():
    if not check_lobby_red_point():
        return 0
    if global_data.lobby_red_point_data.check_main_rp('item_book_rp'):
        return RED_POINT_LEVEL_10
    from common.cfg import confmgr
    from logic.gutils import items_book_utils
    tab_conf = confmgr.get('items_book_conf', 'TabConfig', 'Content')
    tab_type_lst = six_ex.keys(tab_conf)
    for tab_type in tab_type_lst:
        tab_info = items_book_utils.get_items_book_list_widget_info(tab_type)
        tab_cls = tab_info[2]
        if tab_cls and hasattr(tab_cls, 'get_widget_red_points'):
            show_rp = tab_cls.get_widget_red_points()
            if show_rp:
                return RED_POINT_LEVEL_10

    return 0


def get_RoleChooseUI_rp_level(role_id):
    show_rp = global_data.lobby_red_point_data.get_rp_by_no(role_id)
    show_rp = global_data.lobby_red_point_data.get_rp_by_belong_no(role_id) or show_rp
    level = RED_POINT_LEVEL_10 if show_rp else 0
    has_role = True if global_data.player.get_item_by_no(role_id) else False
    if has_role:
        from logic.gutils import bond_utils
        if bond_utils.can_get_gift_reward(role_id):
            level = RED_POINT_LEVEL_30
    return level


def get_MechaDisplay_rp_level(mecha_id):
    if global_data.player.has_unreceived_prof_reward(mecha_id):
        return RED_POINT_LEVEL_30
    from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
    mecha_lobby_id = battle_id_to_mecha_lobby_id(mecha_id)
    if global_data.lobby_red_point_data.get_rp_by_no(mecha_lobby_id):
        return RED_POINT_LEVEL_10
    if global_data.lobby_red_point_data.get_rp_by_belong_no(mecha_lobby_id):
        return RED_POINT_LEVEL_10
    return 0


def check_dict_addition(base_dict, add_dict):
    for k, v in six.iteritems(add_dict):
        if not v:
            continue
        if str(k) not in base_dict:
            return True
        if isinstance(v, dict) and check_dict_addition(base_dict[str(k)], add_dict[k]):
            return True

    return False


def copy_dict(d):
    return {str(k):copy_dict(v) if 1 else v for k, v in six.iteritems(d) if isinstance(v, dict)}


def set_interaction_item_type_rp_click_time(category, item_type, role_id):
    if not global_data.player:
        return False
    user_arch = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
    belong_type_click_table = user_arch.get_field(category, {})
    import logic.gcommon.time_utility as tutil
    belong_type_click_table[str(role_id)] = tutil.get_server_time()
    user_arch.set_field(category, belong_type_click_table)


def get_interaction_item_type_rp_click_time(category, item_type, role_id=None):
    if not global_data.player:
        return False
    user_arch = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
    return user_arch.get_field(category, {}).get(str(role_id), 0)


def check_bgm_rp():
    from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MUSIC
    if global_data.lobby_red_point_data:
        return global_data.lobby_red_point_data.get_rp_by_type(L_ITEM_TYPE_MUSIC)
    return False