# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/lobby_model_display_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import re
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const as lconst
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_WEAPON_SFX, L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT, L_ITEM_TYPE_FACE_DEC, L_ITEM_TYPE_WAIST_DEC, L_ITEM_TYPE_LEG_DEC, L_ITEM_TYPE_HAIR_DEC, L_ITEM_TYPE_ARM_DEC, L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_PET_SKIN
from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no, mecha_lobby_id_2_battle_id, get_pendant_conf
from logic.gutils import dress_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.skin_define_utils import get_assure_socket
from logic.gutils.role_skin_utils import get_unfold_role_skin_list
import os
ITEM_BOOK_DISPLAY_ROT_Y = -25
LITTLE_MECHA_ID = (
 8001, 8005)

def is_little_mecha(mecha_id):
    mecha_id = int(mecha_id)
    if mecha_id in LITTLE_MECHA_ID:
        return True
    return False


REFLECT_SCENE_TYPE = {}
SHADOW_PNL_SCENE_TYPE = {}
SHADOW_REL_SCENE_TYPE = {}
SCENE_RES_CONFIG = {}
WEAPON_FILTER = re.compile('(.*)weapons/(\\w*)/(.*)')

def is_ignore_weapon(path, ignore_list):
    for ignore in ignore_list:
        if ignore in path:
            return True

    return False


def is_scene_surpport_pnl_shadow(scene_type):
    global SHADOW_PNL_SCENE_TYPE
    if not SHADOW_PNL_SCENE_TYPE:
        data = confmgr.get('lobby_model_display_conf', 'ReflectSceneType', 'Content')
        for one_config in six.itervalues(data):
            tmp_scene_type = one_config['scene_type']
            SHADOW_PNL_SCENE_TYPE[tmp_scene_type] = bool(one_config.get('surpport_pnl_shadow'))

    return SHADOW_PNL_SCENE_TYPE.get(scene_type)


def is_scene_surpport_rel_shadow(scene_type):
    global SHADOW_REL_SCENE_TYPE
    if not SHADOW_REL_SCENE_TYPE:
        data = confmgr.get('lobby_model_display_conf', 'ReflectSceneType', 'Content')
        for one_config in six.itervalues(data):
            tmp_scene_type = one_config['scene_type']
            SHADOW_REL_SCENE_TYPE[tmp_scene_type] = bool(one_config.get('surpport_rel_shadow', 0))

    if scene_type not in SHADOW_REL_SCENE_TYPE:
        return False
    return SHADOW_REL_SCENE_TYPE.get(scene_type)


def is_scene_surpport_reflect(scene_type):
    global REFLECT_SCENE_TYPE
    if not REFLECT_SCENE_TYPE:
        data = confmgr.get('lobby_model_display_conf', 'ReflectSceneType', 'Content')
        for one_config in six.itervalues(data):
            if one_config.get('surpport_reflect', 0):
                tmp_scene_type = one_config['scene_type']
                REFLECT_SCENE_TYPE[tmp_scene_type] = 1

    return scene_type in REFLECT_SCENE_TYPE


def get_scene_res_config(scene_type):
    global SCENE_RES_CONFIG
    if not SCENE_RES_CONFIG:
        data = confmgr.get('lobby_model_display_conf', 'ReflectSceneType', 'Content')
        for one_config in six.itervalues(data):
            one_scene_type = one_config['scene_type']
            SCENE_RES_CONFIG[one_scene_type] = {'model_texture': one_config.get('model_texture', ''),'scene_path': one_config.get('scene_path', ''),'scene_type': one_scene_type}

    config = SCENE_RES_CONFIG.get(scene_type, None)
    return config


def get_display_scene_data(scene_type):
    data = confmgr.get('lobby_model_display_conf', 'DisplayScene', 'Content').get(scene_type, {})
    return data


def get_mecha_display_cam_data(mecha_id, skin_id=None):
    data = confmgr.get('lobby_model_display_conf', 'MechaDisplayCam', 'Content').get(str(mecha_id), {})
    if skin_id:
        offset = confmgr.get('lobby_model_display_conf', 'MechaSkinDisplayOffset', 'Content', str(skin_id), 'offset', default=None)
        data['skin_offset'] = offset
    if not data:
        data = confmgr.get('lobby_model_display_conf', 'MechaDisplayCam', 'Content').get('8002', {})
    return data


def get_mecha_display_anim_data(mecha_id, skin_id=None):
    data = None
    if skin_id is not None:
        data = confmgr.get('lobby_model_display_conf', 'MechaChangeAnim', 'Content').get(str(skin_id), {})
    if not data:
        data = confmgr.get('lobby_model_display_conf', 'MechaChangeAnim', 'Content').get(str(mecha_id), {})
    return data


def get_role_display_cam_data(role_id, skin_id):
    data = confmgr.get('lobby_model_display_conf', 'RoleDisplayCam', 'Content', default={})
    cam_data = data.get(str(skin_id), {})
    if not cam_data:
        cam_data = data.get(str(role_id), {})
    return cam_data


def get_valid_mpath(mpath):
    valid_mpath = []
    if not mpath:
        return valid_mpath
    if type(mpath) is str:
        return [mpath]
    for path in mpath:
        if path:
            valid_mpath.append(path)

    return valid_mpath


def get_items_book_interaction_model_data--- This code section failed: ---

 150       0  LOAD_CONST            1  'l'
           3  STORE_FAST            5  'lod_level'

 151       6  LOAD_GLOBAL           0  'type'
           9  LOAD_FAST             1  'dress_id'
          12  CALL_FUNCTION_1       1 
          15  LOAD_GLOBAL           1  'tuple'
          18  LOAD_GLOBAL           2  'list'
          21  BUILD_TUPLE_2         2 
          24  COMPARE_OP            6  'in'
          27  POP_JUMP_IF_FALSE    40  'to 40'
          30  LOAD_FAST             1  'dress_id'
          33  LOAD_CONST            2  ''
          36  BINARY_SUBSCR    
          37  JUMP_FORWARD          3  'to 43'
          40  LOAD_FAST             1  'dress_id'
        43_0  COME_FROM                '37'
          43  STORE_FAST            6  'skin_id'

 152      46  LOAD_GLOBAL           3  'get_lobby_model_data'
          49  LOAD_FAST             6  'skin_id'
          52  LOAD_CONST            3  'is_add_empty'
          55  LOAD_GLOBAL           4  'True'
          58  LOAD_CONST            4  'lod_level'
          61  LOAD_FAST             5  'lod_level'
          64  LOAD_CONST            5  'consider_second_model'
          67  LOAD_GLOBAL           5  'False'
          70  CALL_FUNCTION_769   769 
          73  STORE_FAST            7  'model_data'

 167      76  SETUP_LOOP          270  'to 349'
          79  LOAD_FAST             7  'model_data'
          82  GET_ITER         
          83  FOR_ITER            262  'to 348'
          86  STORE_FAST            8  'm_data'

 168      89  LOAD_FAST             2  'show_anim'
          92  LOAD_FAST             8  'm_data'
          95  LOAD_CONST            6  'show_anim'
          98  STORE_SUBSCR     

 169      99  LOAD_FAST             4  'end_anim'
         102  JUMP_IF_TRUE_OR_POP   108  'to 108'
         105  LOAD_CONST            7  'emptyhand_idle'
       108_0  COME_FROM                '102'
         108  LOAD_FAST             8  'm_data'
         111  LOAD_CONST            8  'end_anim'
         114  STORE_SUBSCR     

 170     115  LOAD_CONST            2  ''
         118  LOAD_FAST             3  'is_manage'
         121  POP_JUMP_IF_FALSE   130  'to 130'
         124  LOAD_GLOBAL           6  'ITEM_BOOK_DISPLAY_ROT_Y'
         127  JUMP_FORWARD          3  'to 133'
         130  LOAD_CONST            2  ''
       133_0  COME_FROM                '127'
         133  LOAD_CONST            2  ''
         136  BUILD_LIST_3          3 
         139  LOAD_FAST             8  'm_data'
         142  LOAD_CONST            9  'off_euler_rot'
         145  STORE_SUBSCR     

 171     146  LOAD_GLOBAL           7  'int'
         149  LOAD_FAST             0  'role_id'
         152  CALL_FUNCTION_1       1 
         155  LOAD_FAST             8  'm_data'
         158  LOAD_CONST           10  'role_id'
         161  STORE_SUBSCR     

 172     162  LOAD_GLOBAL           4  'True'
         165  LOAD_FAST             8  'm_data'
         168  LOAD_CONST           11  'force_end_ani_loop'
         171  STORE_SUBSCR     

 174     172  STORE_SUBSCR     
         173  ROT_FOUR         
         174  ROT_FOUR         
         175  COMPARE_OP            2  '=='
         178  POP_JUMP_IF_FALSE    83  'to 83'

 175     181  LOAD_GLOBAL           8  'dress_utils'
         184  LOAD_ATTR             9  'check_force_default_head_dec'
         187  LOAD_FAST             6  'skin_id'
         190  CALL_FUNCTION_1       1 
         193  STORE_FAST            9  'force_default_head_dec'

 176     196  LOAD_FAST             9  'force_default_head_dec'
         199  POP_JUMP_IF_FALSE   345  'to 345'

 177     202  LOAD_FAST             9  'force_default_head_dec'
         205  STORE_FAST           10  'head_id'

 178     208  LOAD_GLOBAL           8  'dress_utils'
         211  LOAD_ATTR            10  'get_pendant_conf'
         214  LOAD_FAST             6  'skin_id'
         217  LOAD_FAST            10  'head_id'
         220  CALL_FUNCTION_2       2 
         223  STORE_FAST           11  'pendant_conf'

 179     226  LOAD_FAST            11  'pendant_conf'
         229  LOAD_ATTR            11  'get'
         232  LOAD_CONST           13  'pendant_socket_name'
         235  CALL_FUNCTION_1       1 
         238  STORE_FAST           12  'pendant_socket_name'

 180     241  LOAD_FAST            11  'pendant_conf'
         244  LOAD_ATTR            11  'get'
         247  LOAD_CONST           14  'pendant_socket_res_path'
         250  CALL_FUNCTION_1       1 
         253  STORE_FAST           13  'pendant_socket_res_path'

 181     256  LOAD_FAST            13  'pendant_socket_res_path'
         259  POP_JUMP_IF_FALSE   319  'to 319'

 182     262  LOAD_FAST            13  'pendant_socket_res_path'
         265  LOAD_ATTR            12  'endswith'
         268  LOAD_CONST           15  'h.gim'
         271  CALL_FUNCTION_1       1 
         274  POP_JUMP_IF_FALSE   298  'to 298'

 183     277  LOAD_FAST            13  'pendant_socket_res_path'
         280  LOAD_ATTR            13  'replace'
         283  LOAD_CONST           15  'h.gim'
         286  LOAD_CONST           19  'l.gim'
         289  CALL_FUNCTION_2       2 
         292  STORE_FAST           13  'pendant_socket_res_path'
         295  JUMP_ABSOLUTE       319  'to 319'

 185     298  LOAD_FAST            13  'pendant_socket_res_path'
         301  LOAD_ATTR            13  'replace'
         304  LOAD_CONST           17  'h_'
         307  LOAD_CONST           20  'l_'
         310  CALL_FUNCTION_2       2 
         313  STORE_FAST           13  'pendant_socket_res_path'
         316  JUMP_FORWARD          0  'to 319'
       319_0  COME_FROM                '316'

 186     319  LOAD_FAST            12  'pendant_socket_name'
         322  LOAD_FAST             8  'm_data'
         325  LOAD_CONST           13  'pendant_socket_name'
         328  STORE_SUBSCR     

 187     329  LOAD_FAST            13  'pendant_socket_res_path'
         332  LOAD_FAST             8  'm_data'
         335  LOAD_CONST           14  'pendant_socket_res_path'
         338  STORE_SUBSCR     
         339  JUMP_ABSOLUTE       345  'to 345'
         342  JUMP_BACK            83  'to 83'
         345  JUMP_BACK            83  'to 83'
         348  POP_BLOCK        
       349_0  COME_FROM                '76'

 189     349  LOAD_FAST             7  'model_data'
         352  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 172


def get_lobby_model_data(item_no, is_add_empty=False, is_in_battlepass=False, skin_id=None, head_id=None, bag_id=None, suit_id=None, is_get_player_data=True, rotate_pendant=False, lod_level='h', other_pendants=(), consider_second_model=True, second_model_dir='', pet_level=1):
    import world
    mpath, itype = item_utils.get_lobby_item_model_display_info(item_no, lod_level)
    if itype == L_ITEM_TYPE_WEAPON_SFX:
        mount_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
        mount_model_data = get_lobby_model_data(mount_item_no, is_add_empty, is_in_battlepass, skin_id, head_id, bag_id, suit_id, is_get_player_data)
        data = []
        for m_d in mount_model_data:
            copy_md = dict(m_d)
            copy_md['shiny_preview'] = item_no
            data.append(copy_md)

        return data
    else:
        second_model_data = []
        need_correct_show_anim_phase = False
        if consider_second_model and itype in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN):
            mecha_lobby_id = confmgr.get('lobby_item', str(item_no), 'belong_id')
            if not mecha_lobby_id:
                mecha_lobby_id = item_no
            mecha_id = mecha_lobby_id_2_battle_id(mecha_lobby_id)
            _second_model_dir = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'second_model_dir')
            if _second_model_dir:
                second_model_data = get_lobby_model_data(item_no, is_add_empty, is_in_battlepass, skin_id, head_id, bag_id, suit_id, is_get_player_data, rotate_pendant, lod_level, other_pendants, consider_second_model=False, second_model_dir=_second_model_dir)
                need_correct_show_anim_phase = True
                second_model_data[0]['second_model_tag'] = True
        mpaths = get_valid_mpath(mpath)
        if second_model_dir:
            for i, path in enumerate(mpaths):
                mpaths[i] = os.path.dirname(path) + '/' + second_model_dir + '/' + os.path.basename(path)

            need_correct_show_anim_phase = True
        model_data = []
        if len(mpaths) == 1:
            new_data = {}
            data = confmgr.get('lobby_item', str(item_no), default={})
            new_data['skin_id'] = item_no
            new_data['item_no'] = item_no
            new_data['mpath'] = mpaths[0]
            new_data['model_scale'] = data.get('model_scale', 1)
            new_data['off_euler_rot'] = data.get('off_euler_rot', [0, 0, 0])
            new_data['follow_center_pos'] = data.get('follow_center_pos')
            new_data['show_anim'] = data.get('first_ani_name')
            new_data['zoom_in_camera'] = data.get('zoom_in_camera')
            new_data['show_trk'] = data.get('first_trk')
            new_data['bond_show_anim'] = data.get('bond_ani_name')
            new_data['bond_end_anim'] = data.get('bond_end_ani_name')
            new_data['chuchang_trk'] = data.get('chuchang_trk')
            new_data['end_anim'] = data.get('end_ani_name')
            new_data['end_ani_list'] = data.get('end_ani_list')
            new_data['end_anim_loop_time'] = data.get('end_ani_name_loop_time')
            new_data['move_anim'] = data.get('move_ani_name')
            new_data['mecha_first_ani'] = data.get('first_ani_name')
            new_data['mecha_end_ani'] = data.get('end_ani_name')
            new_data['need_correct_show_anim_phase'] = need_correct_show_anim_phase
            new_data['light_dir'] = data.get('light_dir')
            new_data['hdr_config'] = data.get('hdr_config')
            new_data['env_config'] = data.get('env_config')
            if lod_level == 'l':
                new_data['is_l_model'] = True
            assure_socket = get_assure_socket(item_no)
            if assure_socket is not None:
                new_data['assure_socket'] = assure_socket
            force_empty = False
            if itype == L_ITEM_TYPE_MECHA or itype == L_ITEM_TYPE_MECHA_SKIN:
                force_empty = True
            if is_add_empty and lod_level != 'h' or force_empty:
                new_data['sub_mesh_path_list'] = [new_data['mpath']]
                index = new_data['mpath'].find('{}.gim'.format(lod_level))
                if index != -1:
                    new_data['mpath'] = new_data['mpath'][0:index] + 'empty.gim'
            if is_get_player_data and itype == L_ITEM_TYPE_MECHA_SKIN and global_data.player:
                skin_item = global_data.player.get_item_by_no(item_no)
                if skin_item:
                    shiny_weapon_id = skin_item.get_weapon_sfx()
                    new_data['shiny_weapon_id'] = shiny_weapon_id
            improved_skin_sfx_id = None
            if is_get_player_data and itype == L_ITEM_TYPE_ROLE_SKIN and global_data.player:
                skin_item = global_data.player.get_item_by_no(item_no)
                if skin_item:
                    improved_skin_sfx_id = skin_item.get_weapon_sfx()
                    new_data['improved_skin_sfx_id'] = improved_skin_sfx_id
            if itype == L_ITEM_TYPE_ROLE:
                new_data['role_id'] = item_no
                default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(item_no), 'default_skin')
                skin_id = skin_id if skin_id else default_skin[0]
            elif itype == L_ITEM_TYPE_ROLE_SKIN:
                new_data['role_id'] = data.get('belong_id')
                skin_id = skin_id if skin_id else item_no
            if itype == L_ITEM_TYPE_PET_SKIN:
                socket_res = confmgr.get('c_pet_info', str(item_no), 'normal_res_info_list', default=[])
                for res_info in socket_res:
                    res_path = res_info.get('res_path', None)
                    if not res_path:
                        continue
                    if pet_level < res_info.get('level', 1) or pet_level > res_info.get('level_cap', 99):
                        continue
                    if res_path.endswith('.gim'):
                        socket_list = res_info.get('socket_list', [])
                        if socket_list:
                            if 'socket_model' not in new_data:
                                new_data['socket_model'] = {}
                            for socket in socket_list:
                                if socket not in new_data['socket_model']:
                                    new_data['socket_model'][socket] = []
                                new_data['socket_model'][socket].append({'model_path': res_path,'ignore_on_shadow': res_info.get('ignore_on_shadow', False)})

                        else:
                            if 'sub_mesh_path_list' not in new_data:
                                new_data['sub_mesh_path_list'] = []
                            new_data['sub_mesh_path_list'].append(res_path)
                    elif res_path.endswith('.sfx'):
                        socket_list = res_info.get('socket_list', [])
                        if socket_list:
                            if 'socket_model' not in new_data:
                                new_data['socket_model'] = {}
                            for socket in socket_list:
                                if socket not in new_data['socket_model']:
                                    new_data['socket_model'][socket] = []
                                new_data['socket_model'][socket].append({'model_path': res_path,'res_type': 'SFX','ignore_on_shadow': res_info.get('ignore_on_shadow', False)
                                   })

            if skin_id:
                head_id, bag_id, suit_id, other_pendants = dress_utils.get_real_dec_dict_with_check_completion_and_replacement(skin_id, head_id, bag_id, suit_id, other_pendants, improved_skin_sfx_id)
            new_data['follow_same_bone_pendants'] = []
            if head_id is not None or bag_id is not None or suit_id is not None or any(other_pendants):
                head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, head_pendant_l_same_gis, pendant_random_anim_list, bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2, bag_pendant_l_same_gis, pendant_data_list = dress_utils.get_pendant_res_lod_conf(lod_level, None, skin_id, head_id, bag_id, suit_id, other_pendants)
                new_data['head_pendant_type'] = head_pendant_type
                new_data['head_res_path'] = head_res_path
                new_data['pendant_socket_name'] = pendant_socket_name
                new_data['pendant_socket_res_path'] = pendant_socket_res_path
                new_data['pendant_random_anim_list'] = pendant_random_anim_list
                new_data['bag_model_path'] = bag_model_path
                new_data['bag_socket_name'] = bag_socket_name
                new_data['bag_model_path2'] = bag_model_path2
                new_data['bag_socket_name2'] = bag_socket_name2
                new_data['head_pendant_l_same_gis'] = head_pendant_l_same_gis
                new_data['bag_pendant_l_same_gis'] = bag_pendant_l_same_gis
                new_data['pendant_data_list'] = pendant_data_list
                use_skin_show_anim, pendant_show_anim, use_skin_end_anim, pendant_end_anim = dress_utils.get_pendant_anim(skin_id, bag_id, suit_id, other_pendants)
                if head_id is not None and head_pendant_type:
                    if rotate_pendant:
                        data = confmgr.get('lobby_item', str(head_id), default={})
                        if data.get('off_euler_rot'):
                            new_data['off_euler_rot'] = data.get('off_euler_rot')
                    pendant_config = get_pendant_conf(skin_id, head_id)
                    if pendant_config and pendant_config.get('socket_follow_same_bone'):
                        new_data['follow_same_bone_pendants'].append(pendant_socket_res_path)
                if bag_id is not None and bag_model_path:
                    bag_data = confmgr.get('lobby_item', str(bag_id), default={})
                    new_data['show_anim'] = use_skin_show_anim or (bag_data.get('first_ani_name') if bag_data.get('first_ani_name') else new_data['show_anim'])
                    new_data['show_trk'] = bag_data.get('first_trk') if bag_data.get('first_trk') else new_data['show_trk']
                new_data['end_anim'] = use_skin_end_anim or (bag_data.get('end_ani_name') if bag_data.get('end_ani_name') else new_data['end_anim'])
            if rotate_pendant and bag_data.get('off_euler_rot'):
                new_data['off_euler_rot'] = bag_data.get('off_euler_rot')
        if suit_id is not None and head_pendant_type:
            suit_data = confmgr.get('lobby_item', str(suit_id), default={})
            new_data['show_anim'] = use_skin_show_anim or (suit_data.get('first_ani_name') if suit_data.get('first_ani_name') else new_data['show_anim'])
            new_data['show_trk'] = suit_data.get('first_trk') if suit_data.get('first_trk') else new_data['show_trk']
        if not use_skin_end_anim:
            if suit_data.get('end_ani_name'):
                new_data['end_anim'] = suit_data.get('end_ani_name') if 1 else new_data['end_anim']
            if rotate_pendant and suit_data.get('off_euler_rot'):
                new_data['off_euler_rot'] = suit_data.get('off_euler_rot')
        if pendant_show_anim:
            new_data['show_anim'] = pendant_show_anim if 1 else new_data['show_anim']
            if pendant_end_anim:
                new_data['end_anim'] = pendant_end_anim if 1 else new_data['end_anim']
            model_data.append(new_data)
        else:
            for index, path in enumerate(mpaths):
                new_data = {}
                data = confmgr.get('lobby_model_display_conf', 'MoreModelItem', 'Content').get(str(item_no), {})
                new_data['mpath'] = path
                new_data['item_no'] = item_no
                new_data['model_scale'] = data.get('model_scale%d' % index, 1)
                new_data['off_euler_rot'] = data.get('off_euler_rot%d' % index, [0, 0, 0])
                new_data['follow_center_pos'] = data.get('follow_center_pos%d' % index)
                new_data['show_anim'] = data.get('ani_name')
                new_data['chuchang_trk'] = data.get('chuchang_trk')
                new_data['end_anim'] = data.get('end_ani_name')
                new_data['end_ani_list'] = data.get('end_ani_list')
                new_data['end_anim_loop_time'] = data.get('end_ani_name_loop_time')
                new_data['move_anim'] = data.get('move_ani_name')
                new_data['mecha_first_ani'] = data.get('mecha_first_ani_name')
                new_data['mecha_end_ani'] = data.get('mecha_end_ani_name')
                if is_add_empty and lod_level != 'h':
                    new_data['sub_mesh_path_list'] = [new_data['mpath']]
                    index = new_data['mpath'].find('{}.gim'.format(lod_level))
                    if index != -1:
                        new_data['mpath'] = new_data['mpath'][0:index] + 'empty.gim'
                if is_get_player_data and itype == L_ITEM_TYPE_MECHA_SKIN and global_data.player:
                    skin_item = global_data.player.get_item_by_no(item_no)
                    if skin_item:
                        shiny_weapon_id = skin_item.get_weapon_sfx()
                        new_data['shiny_weapon_id'] = shiny_weapon_id
                if is_get_player_data and itype == L_ITEM_TYPE_ROLE_SKIN and global_data.player:
                    skin_item = global_data.player.get_item_by_no(item_no)
                    if skin_item:
                        improved_skin_sfx_id = skin_item.get_weapon_sfx()
                        new_data['improved_skin_sfx_id'] = improved_skin_sfx_id
                model_data.append(new_data)

        if is_in_battlepass:
            param = confmgr.get('lobby_model_display_conf', 'BattlePassModelDisplayParam', 'Content').get(str(item_no), {})
            if param:
                for data in model_data:
                    data['follow_center_pos'] = param.get('follow_center_pos')
                    data['model_scale'] = param.get('model_scale')

        if itype in (L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN):
            for data in model_data:
                danjia_path = get_weapon_socket_models(data['mpath'])
                if not danjia_path:
                    continue
                socket_model = data.get('socket_model', {})
                socket_model['danjia'] = {'model_path': danjia_path,'bind_type': world.BIND_TYPE_ALL}
                data['socket_model'] = socket_model

        if second_model_data:
            model_data.extend(second_model_data)
        return model_data


def get_weapon_socket_models(weapon_path):
    res_root_dir = re.match(WEAPON_FILTER, weapon_path)
    if not res_root_dir:
        return ''
    else:
        res_root_dir = res_root_dir.group(2)
        trigger_conf = confmgr.get('weapon_trigger_config', res_root_dir, default=None)
        if not trigger_conf or is_ignore_weapon(weapon_path, trigger_conf.get('ignore_list', [])):
            return ''
        return weapon_path.replace('h.gim', 'danjia.gim')


def get_pendant_show_data(item_no, is_get_player_data=False, rotate_pendant=False, is_in_battle_pass=False):
    skin_id = None
    role_id = item_utils.get_lobby_item_belong_no(item_no)
    role_data = global_data.player.get_item_by_no(role_id)
    if role_data:
        skin_id = role_data.get_fashion().get(FASHION_POS_SUIT)
        if not dress_utils.check_valid_decoration(skin_id, item_no):
            skin_id = None
    if not skin_id:
        skin_list = get_unfold_role_skin_list(role_id)
        for v_id in skin_list:
            if dress_utils.check_valid_decoration(v_id, item_no):
                skin_id = v_id
                break

    item_type = item_utils.get_lobby_item_type(item_no)
    head_id = None
    bag_id = None
    suit_id = None
    other_pendants = ()
    if item_type == L_ITEM_TYPE_HEAD:
        head_id = item_no
    elif item_type == L_ITEM_TYPE_BODY:
        bag_id = item_no
    elif item_type == L_ITEM_TYPE_SUIT:
        suit_id = item_no
    elif item_type in (L_ITEM_TYPE_FACE_DEC, L_ITEM_TYPE_ARM_DEC, L_ITEM_TYPE_HAIR_DEC, L_ITEM_TYPE_WAIST_DEC, L_ITEM_TYPE_LEG_DEC):
        other_pendants = (
         item_no,)
    model_data = get_lobby_model_data(skin_id, head_id=head_id, bag_id=bag_id, suit_id=suit_id, is_get_player_data=False, rotate_pendant=True, other_pendants=other_pendants, is_in_battlepass=is_in_battle_pass, consider_second_model=False)
    return model_data


def get_mecha_sfx_model_data--- This code section failed: ---

 515       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('get_mecha_model_h_path', 'get_mecha_model_path')
           6  IMPORT_NAME           0  'logic.gutils.dress_utils'
           9  IMPORT_FROM           1  'get_mecha_model_h_path'
          12  STORE_FAST            1  'get_mecha_model_h_path'
          15  IMPORT_FROM           2  'get_mecha_model_path'
          18  STORE_FAST            2  'get_mecha_model_path'
          21  POP_TOP          

 516      22  LOAD_GLOBAL           3  'confmgr'
          25  LOAD_ATTR             4  'get'
          28  LOAD_CONST            3  'display_enter_effect'
          31  LOAD_CONST            4  'Content'
          34  LOAD_GLOBAL           5  'str'
          37  LOAD_FAST             0  'item_no'
          40  CALL_FUNCTION_1       1 
          43  LOAD_CONST            5  'default'
          46  BUILD_MAP_0           0 
          49  CALL_FUNCTION_259   259 
          52  STORE_FAST            3  'item_display_data'

 517      55  LOAD_FAST             3  'item_display_data'
          58  LOAD_ATTR             4  'get'
          61  LOAD_CONST            6  'lobbyCallOutSfxPath'
          64  LOAD_CONST            7  ''
          67  CALL_FUNCTION_2       2 
          70  STORE_DEREF           0  'callOutSfxPath'

 518      73  LOAD_FAST             3  'item_display_data'
          76  LOAD_ATTR             4  'get'
          79  LOAD_CONST            8  'cSfxSoundName'
          82  LOAD_CONST            7  ''
          85  CALL_FUNCTION_2       2 
          88  STORE_DEREF           1  'cSfxSoundName'

 519      91  LOAD_CLOSURE          0  'callOutSfxPath'
          94  LOAD_CLOSURE          1  'cSfxSoundName'
         100  LOAD_CONST               '<code_object on_finish_create_model>'
         103  MAKE_CLOSURE_0        0 
         106  STORE_FAST            4  'on_finish_create_model'

 522     109  LOAD_GLOBAL           6  'global_data'
         112  LOAD_ATTR             7  'player'
         115  LOAD_ATTR             8  'get_lobby_selected_mecha_item_id'
         118  CALL_FUNCTION_0       0 
         121  STORE_FAST            0  'item_no'

 523     124  LOAD_GLOBAL           6  'global_data'
         127  LOAD_ATTR             7  'player'
         130  LOAD_ATTR             9  'get_mecha_fashion'
         133  LOAD_FAST             0  'item_no'
         136  CALL_FUNCTION_1       1 
         139  STORE_FAST            5  'clothing_id'

 524     142  LOAD_FAST             5  'clothing_id'
         145  POP_JUMP_IF_FALSE   157  'to 157'

 525     148  LOAD_FAST             5  'clothing_id'
         151  STORE_FAST            0  'item_no'
         154  JUMP_FORWARD          0  'to 157'
       157_0  COME_FROM                '154'

 526     157  LOAD_GLOBAL          10  'get_lobby_model_data'
         160  LOAD_GLOBAL          10  'get_lobby_model_data'
         163  LOAD_GLOBAL          11  'False'
         166  CALL_FUNCTION_257   257 
         169  STORE_FAST            6  'model_data'

 527     172  LOAD_FAST             5  'clothing_id'
         175  POP_JUMP_IF_FALSE   276  'to 276'

 528     178  LOAD_GLOBAL           6  'global_data'
         181  LOAD_ATTR             7  'player'
         184  LOAD_ATTR            12  'get_lobby_selected_mecha_id'
         187  CALL_FUNCTION_0       0 
         190  STORE_FAST            7  'mecha_id'

 529     193  LOAD_FAST             2  'get_mecha_model_path'
         196  LOAD_FAST             7  'mecha_id'
         199  LOAD_FAST             5  'clothing_id'
         202  CALL_FUNCTION_2       2 
         205  STORE_FAST            8  'mpath'

 530     208  LOAD_FAST             1  'get_mecha_model_h_path'
         211  LOAD_FAST             7  'mecha_id'
         214  LOAD_FAST             5  'clothing_id'
         217  CALL_FUNCTION_2       2 
         220  STORE_FAST            9  'submesh_path'

 531     223  SETUP_LOOP           50  'to 276'
         226  LOAD_FAST             6  'model_data'
         229  GET_ITER         
         230  FOR_ITER             39  'to 272'
         233  STORE_FAST           10  'data'

 532     236  LOAD_FAST             8  'mpath'
         239  LOAD_FAST            10  'data'
         242  LOAD_CONST           11  'mpath'
         245  STORE_SUBSCR     

 533     246  LOAD_FAST             9  'submesh_path'
         249  BUILD_LIST_1          1 
         252  LOAD_FAST            10  'data'
         255  LOAD_CONST           12  'sub_mesh_path_list'
         258  STORE_SUBSCR     

 534     259  LOAD_FAST             0  'item_no'
         262  LOAD_FAST            10  'data'
         265  LOAD_CONST           13  'skin_id'
         268  STORE_SUBSCR     
         269  JUMP_BACK           230  'to 230'
         272  POP_BLOCK        
       273_0  COME_FROM                '223'
         273  JUMP_FORWARD          0  'to 276'
       276_0  COME_FROM                '223'

 535     276  LOAD_FAST             6  'model_data'
         279  LOAD_FAST             4  'on_finish_create_model'
         282  BUILD_TUPLE_2         2 
         285  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 166


def gen_role_seq():
    if not global_data.player:
        return []
    return global_data.player.get_role_open_seq()


def get_role_seq_show():
    from logic.gutils import role_utils
    role_seq_show = []
    role_seq = gen_role_seq()
    for role_id in role_seq:
        if role_utils.check_show_role_panel(role_id):
            role_seq_show.append(role_id)

    return role_seq_show


def get_cam_matrix(scene_content_type, key):
    cam_hanger = None
    camera_info = confmgr.get('scene_content_config', str(scene_content_type), 'camera', key, default='')
    if camera_info:
        camera_trans = [ float(x) for x in camera_info.split(',') ]
        import math3d
        cam_hanger = math3d.matrix()
        cam_hanger.set_all(*camera_trans)
    if not cam_hanger:
        import world
        scene = world.get_active_scene()
        cam_hanger = scene.get_preset_camera(key)
    return cam_hanger


def get_cam_position(scene_content_type, display_type, default=None):
    scene_data = get_display_scene_data(display_type)
    cam_hanger = get_cam_matrix(scene_content_type, scene_data.get('cam_key'))
    if cam_hanger is None:
        return default
    else:
        return cam_hanger.translation


def get_cam_rot(display_type):
    import world
    scene = world.get_active_scene()
    cam_hanger = scene.get_preset_camera(display_type)
    if cam_hanger:
        return cam_hanger.rotation


def is_chuchang_scene():
    scene_type = global_data.game_mgr.get_cur_scene_type()
    return scene_type == scene_const.SCENE_MECHA_CHUCHANG


def print_cur_display_scene_cam_name():
    scene_content_type = global_data.ex_scene_mgr_agent.lobby_relatived_scene[global_data.game_mgr.scene.scene_type].scene_content_type
    if scene_content_type:
        cam_pos = global_data.game_mgr.scene.active_camera.world_position
        from common.cfg import confmgr
        cam_keys = six_ex.keys(confmgr.get('scene_content_config', str(scene_content_type), 'camera', default={}))
        min_weight = 99999
        weight2cam = {}
        for key in cam_keys:
            scene_pos = get_cam_matrix(scene_content_type, key).translation
            weight = abs(cam_pos.x - scene_pos.x) + abs(cam_pos.y - scene_pos.y) + abs(cam_pos.z - scene_pos.z)
            if weight not in weight2cam:
                weight2cam[weight] = []
            weight2cam[weight].append(key)
            min_weight = min(min_weight, weight)

        if min_weight < 99999:
            cams = weight2cam[min_weight]
            if cams:
                if len(cams) == 1:
                    print('cur_cam_name---------------', cams[0])
                else:
                    print('cur_cam_names---------------', cams)
            else:
                print('wait and try again!!!!!!!!!')
        else:
            print('no search cam!!!!!!!!!')
        scn_path = confmgr.get('scene_content_config', str(scene_content_type), 'scn_path')
        if scn_path:
            print('scene_path--------------', scn_path)
    else:
        display_type = global_data.emgr.get_lobby_display_type_event.emit()
        if display_type:
            from logic.gutils import lobby_model_display_utils
            print('cur_cam_name---------------', lobby_model_display_utils.get_display_scene_data(display_type[0]).get('cam_key'))
            print('scene_path--------------', global_data.game_mgr.scene.scene_data['scene_path'])