# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_decorator.py
from __future__ import absolute_import
import time
from common.cfg import confmgr
from logic.gcommon.item import item_const
from ext_package import ext_package_const
debug_mode = False
last_remind_time = 0
REMIND_TIME = 1.5
DEFAULT_MECHATRANS_ID = 8501
g_has_skin = None
g_has_kongdao = None
g_has_video = None
g_has_audio = None
g_ext_pve_dict = {}

def set_ext_debug_mode(enable):
    global debug_mode
    debug_mode = enable


def has_skin_ext():
    global g_has_skin
    if debug_mode:
        return False
    else:
        if g_has_skin is not None:
            return g_has_skin
        from ext_package.ext_ingame_manager import ExtInGameManager
        g_has_skin = ExtInGameManager().has_skin_ext()
        return g_has_skin
        return


def ext_remind():
    global last_remind_time
    if time.time() - last_remind_time > REMIND_TIME:
        global_data.game_mgr.show_tip(get_text_by_id(344))
        last_remind_time = time.time()


def has_kongdao_ext():
    global g_has_kongdao
    if debug_mode:
        return False
    else:
        if g_has_kongdao is not None:
            return g_has_kongdao
        from ext_package.ext_ingame_manager import ExtInGameManager
        g_has_kongdao = ExtInGameManager().has_kongdao_ext()
        return g_has_kongdao
        return


def has_video_ext():
    global g_has_video
    if debug_mode:
        return False
    else:
        if g_has_video is not None:
            return g_has_video
        from ext_package.ext_ingame_manager import ExtInGameManager
        g_has_video = ExtInGameManager().has_video_ext()
        return g_has_video
        return


def has_audio_ext():
    global g_has_audio
    if debug_mode:
        return False
    else:
        if g_has_audio is not None:
            return g_has_audio
        from ext_package.ext_ingame_manager import ExtInGameManager
        g_has_audio = ExtInGameManager().has_audio_ext()
        return g_has_audio
        return


PVE_EXT_LIST = (1, 2, 3)

def has_all_pve_ext():
    for chapter in PVE_EXT_LIST:
        if not has_pve_ext(chapter):
            return False

    return True


def has_pve_ext(chapter=1):
    global g_ext_pve_dict
    if debug_mode:
        return False
    else:
        ext_name = ext_package_const.get_pve_name(chapter)
        if ext_name in g_ext_pve_dict:
            return g_ext_pve_dict[ext_name]
        from ext_package.ext_ingame_manager import ExtInGameManager
        has_pve_chapter = ExtInGameManager().has_pve_ext(chapter)
        g_ext_pve_dict[ext_name] = has_pve_chapter
        return has_pve_chapter


def ext_role_use_org_skin(func):

    def wrapper(self, bdict):
        if not has_skin_ext():
            fashion = bdict.get(item_const.FASHION_KEY, {})
            if fashion:
                role_id = bdict.get('role_id', None)
                if role_id:
                    default_skin_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
                else:
                    default_skin_id = None
                if default_skin_id:
                    bdict[item_const.FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin_id}
            if 'lobby_mecha_fashion' in bdict:
                lobby_mecha_item_id = bdict.get('lobby_mecha_id', None)
                if lobby_mecha_item_id:
                    default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(lobby_mecha_item_id), 'default_fashion')
                    if default_skin:
                        bdict['lobby_mecha_fashion'] = {'fashion': {item_const.FASHION_POS_SUIT: default_skin[0]}}
        return func(self, bdict)

    return wrapper


def ext_del_owner_fashion_skin(func):

    def wrapper(self, bdict):
        if not has_skin_ext():
            if 'owner_fashion_id' in bdict:
                del bdict['owner_fashion_id']
        return func(self, bdict)

    return wrapper


def ext_clear_fashion_key(func):

    def wrapper(self, bdict):
        if not has_skin_ext():
            if 'fashion' in bdict:
                bdict['fashion'] = {}
        return func(self, bdict)

    return wrapper


def get_default_fashion(self, fashion_data, role_id=None):
    if not has_skin_ext():
        if role_id is None:
            role_id = self.ev_g_role_id()
        if role_id:
            default_skin_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
            if default_skin_id:
                return {item_const.FASHION_POS_SUIT: default_skin_id}
            else:
                return fashion_data

    else:
        return fashion_data
    return


def get_mecha_default_fashion(mecha_item_id, fashion_data):
    if not has_skin_ext():
        default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_id), 'default_fashion')
        if default_skin:
            return {item_const.FASHION_POS_SUIT: default_skin[0]}
        else:
            return fashion_data

    else:
        return fashion_data


def get_default_mecha_fashion_decorator(func):

    def wrapper(self, mecha_item_id):
        if not has_skin_ext():
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_id), 'default_fashion')
            if default_skin:
                return default_skin[0]
            else:
                return func(self, mecha_item_id)

        return func(self, mecha_item_id)

    return wrapper


def get_default_mecha_shiny(func):

    def wrapper(self, mecha_item_id):
        if not has_skin_ext():
            return item_const.DEFAULT_MECHA_SHINY
        return func(self, mecha_item_id)

    return wrapper


def mecha_unit_use_default_skin(func):

    def wrapper(self, bdict):
        if not has_skin_ext():
            mecha_id = bdict.get('mecha_id', None)
            if mecha_id and item_const.MECHA_FASHION_KEY in bdict:
                from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
                mecha_item_no = battle_id_to_mecha_lobby_id(int(mecha_id))
                default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')
                if default_skin:
                    bdict[item_const.MECHA_FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin[0]}
            bdict['mecha_custom_skin'] = {}
        return func(self, bdict)

    return wrapper


def mecha_trans_unit_use_default_skin(func):

    def wrapper(self, bdict):
        if not has_skin_ext():
            mecha_id = bdict.get('mecha_id', None)
            if mecha_id and item_const.MECHA_FASHION_KEY in bdict:
                mecha_id = DEFAULT_MECHATRANS_ID
                from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
                mecha_item_no = battle_id_to_mecha_lobby_id(int(mecha_id))
                default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')
                if default_skin:
                    bdict[item_const.MECHA_FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin[0]}
            bdict['mecha_custom_skin'] = {}
        return func(self, bdict)

    return wrapper


def ext_modify_player_info_get(func):

    def wrapper(self, *args, **kwargs):
        ret_data = func(self, *args, **kwargs)
        if ret_data and item_const.MECHA_LOBBY_INFO in ret_data:
            ret_data.update(ret_data[item_const.MECHA_LOBBY_INFO])
        if ret_data and not has_skin_ext():
            if 'role_id' in ret_data:
                role_id = ret_data['role_id']
                default_skin_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
                ret_data[item_const.INF_ROLE_FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin_id}
            if item_const.MECHA_LOBBY_ID_KEY in ret_data:
                mecha_item_no = ret_data[item_const.MECHA_LOBBY_ID_KEY]
                default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')
                if default_skin:
                    ret_data[item_const.MECHA_LOBBY_FASHION_KEY] = default_skin[0]
            if item_const.MECHA_LOBBY_WP_SFX_KEY in ret_data:
                ret_data[item_const.MECHA_LOBBY_WP_SFX_KEY] = item_const.DEFAULT_MECHA_SHINY
            if item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY in ret_data:
                ret_data[item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY] = {}
        return ret_data

    return wrapper


def ext_modify_player_info_set(func):

    def wrapper(self, info_type, in_data):
        if in_data and item_const.MECHA_LOBBY_INFO in in_data:
            in_data.update(in_data[item_const.MECHA_LOBBY_INFO])
        if in_data and not has_skin_ext():
            if 'role_id' in in_data:
                role_id = in_data['role_id']
                default_skin_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
                in_data[item_const.INF_ROLE_FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin_id}
            if item_const.MECHA_LOBBY_ID_KEY in in_data:
                mecha_item_no = in_data[item_const.MECHA_LOBBY_ID_KEY]
                default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')
                if default_skin:
                    in_data[item_const.MECHA_LOBBY_FASHION_KEY] = default_skin[0]
            if item_const.MECHA_LOBBY_WP_SFX_KEY in in_data:
                in_data[item_const.MECHA_LOBBY_WP_SFX_KEY] = item_const.DEFAULT_MECHA_SHINY
            if item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY in in_data:
                in_data[item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY] = {}
        return func(self, info_type, in_data)

    return wrapper


def ext_do_nothing_when_has_no_skin_ext(func):

    def wrapper(self, *args, **kwargs):
        if not has_skin_ext():
            return
        func(self, *args, **kwargs)

    return wrapper


def ext_do_nothing_when_not_default_skin(func):

    def wrapper--- This code section failed: ---

 294       0  LOAD_GLOBAL           0  'has_skin_ext'
           3  CALL_FUNCTION_0       0 
           6  POP_JUMP_IF_TRUE     97  'to 97'

 295       9  LOAD_GLOBAL           1  'hasattr'
          12  LOAD_GLOBAL           1  'hasattr'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    97  'to 97'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  'ext_can_show_model'
          27  UNARY_NOT        
        28_0  COME_FROM                '18'
          28  POP_JUMP_IF_FALSE    97  'to 97'

 297      31  LOAD_GLOBAL           3  'time'
          34  LOAD_ATTR             3  'time'
          37  CALL_FUNCTION_0       0 
          40  LOAD_GLOBAL           4  'last_remind_time'
          43  BINARY_SUBTRACT  
          44  LOAD_GLOBAL           5  'REMIND_TIME'
          47  COMPARE_OP            4  '>'
          50  POP_JUMP_IF_FALSE    90  'to 90'

 298      53  LOAD_GLOBAL           6  'global_data'
          56  LOAD_ATTR             7  'game_mgr'
          59  LOAD_ATTR             8  'show_tip'
          62  LOAD_GLOBAL           9  'get_text_by_id'
          65  LOAD_CONST            2  344
          68  CALL_FUNCTION_1       1 
          71  CALL_FUNCTION_1       1 
          74  POP_TOP          

 299      75  LOAD_GLOBAL           3  'time'
          78  LOAD_ATTR             3  'time'
          81  CALL_FUNCTION_0       0 
          84  STORE_GLOBAL          4  'last_remind_time'
          87  JUMP_FORWARD          0  'to 90'
        90_0  COME_FROM                '87'

 300      90  LOAD_CONST            0  ''
          93  RETURN_END_IF    
        94_0  COME_FROM                '28'
          94  JUMP_FORWARD          0  'to 97'
        97_0  COME_FROM                '94'

 301      97  LOAD_DEREF            0  'func'
         100  LOAD_FAST             0  'self'
         103  LOAD_FAST             1  'args'
         106  LOAD_FAST             2  'kwargs'
         109  CALL_FUNCTION_VAR_KW_1     1 
         112  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15

    return wrapper


def ext_do_nothing_when_no_skin_ext(func):

    def wrapper(self, *args, **kwargs):
        global last_remind_time
        if not has_skin_ext():
            if time.time() - last_remind_time > 1:
                global_data.game_mgr.show_tip(get_text_by_id(344))
                last_remind_time = time.time()
            return
        func(self, *args, **kwargs)

    return wrapper


def ext_do_nothing_when_no_skin_ext_v2(func):

    def wrapper(self, *args, **kwargs):
        if not has_skin_ext():
            return
        func(self, *args, **kwargs)

    return wrapper


def ext_get_nb_mecha_info(func):

    def wrapper(self, *args, **kwargs):
        mecha_info_lst = func(self, *args, **kwargs)
        if mecha_info_lst and not has_skin_ext():
            from copy import deepcopy
            ret_info_lst = deepcopy(mecha_info_lst)
            for idx, mecha_info in enumerate(mecha_info_lst):
                mecha_id = mecha_info[1]
                from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
                mecha_item_no = battle_id_to_mecha_lobby_id(int(mecha_id))
                default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')
                if default_skin:
                    ret_info_lst[idx][3][item_const.FASHION_KEY] = {item_const.FASHION_POS_SUIT: default_skin[0]}
                    ret_info_lst[idx][3]['custom_skin'] = {}
                    if 'sfx' in ret_info_lst[idx][3]:
                        del ret_info_lst[idx][3]['sfx']

            return ret_info_lst
        else:
            return mecha_info_lst

    return wrapper


def ext_get_nb_role_info(func):

    def wrapper(self, *args, **kwargs):
        role_info_lst = func(self, *args, **kwargs)
        if role_info_lst and not has_skin_ext():
            from copy import deepcopy
            ret_info_lst = deepcopy(role_info_lst)
            for idx, role_info in enumerate(role_info_lst):
                role_id = role_info[1]
                default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')
                if default_skin:
                    ret_info_lst[idx][3] = {item_const.FASHION_POS_SUIT: default_skin[0]}

            return ret_info_lst
        else:
            return role_info_lst

    return wrapper