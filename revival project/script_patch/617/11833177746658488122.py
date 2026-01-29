# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/dress_utils.py
from __future__ import absolute_import
import six_ex
import six
import math3d
import world
import game3d
import logic.gcommon.common_const.animation_const as animation_const
import C_file
from common.cfg import confmgr
from logic.gcommon.item import item_const as iconst
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import SEX_MALE, SEX_FEMALE
from logic.gcommon.component.client.ResourceManager import ResLoaderMgr, RES_TYPE_UNKNOWN
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_SUIT_2, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_OTHER_PENDANT_LIST, FASHION_POS_WEAPON_SFX
from logic.gcommon.common_const import character_anim_const
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.gutils import role_utils
from logic.gutils.role_skin_utils import get_improve_skin_head_id, get_improve_skin_pendants_id
HEAD_PENDANT_TYPE = {'NEW_HEAD': 1,
   'NEW_HEAD_WITH_SOCKET_RES': 2,
   'OLD_HEAD_WITH_SOCKET_RES': 3
   }
ANIM_ASSEMBLE_PATHS = frozenset([
 '16/1.0/16_2007/parts/l_head.gim'])
DressLoader = ResLoaderMgr()
SEX_CONF = {SEX_MALE: 'm',
   SEX_FEMALE: 'f'
   }
DEFAULT_CLOTHING_ID = -1

def get_suit_clothing(role_id, suit_id, lod_level=iconst.LOD_L):
    clothing_copy = confmgr.get('dress_suit', str(suit_id), 'suit_clothing', default={}).copy()
    if clothing_copy:
        for pos, path in six.iteritems(clothing_copy):
            clothing_copy[pos] = 'character/{}'.format(path.format(role_id, lod_level))

    return clothing_copy


def get_suit_wgg(role_id, suit_id, lod_level=iconst.LOD_L):
    return {}


def get_suit_id_by_clothing(dress_dict, role_id):
    if iconst.DRESS_POS_BODICE in dress_dict:
        clothing_data = dress_dict[iconst.DRESS_POS_BODICE]
        if isinstance(clothing_data, int):
            return get_suid_id(clothing_data)
        if isinstance(clothing_data, dict):
            item_id = clothing_data.get('item_id', None)
            if item_id:
                return get_suid_id(item_id)
    role_deault_item = confmgr.get('role_config', str(role_id), 'default_item')
    if role_deault_item:
        return get_suid_id(role_deault_item[iconst.DRESS_POS_BODICE])
    else:
        return


def get_default_dress(role_id, part_id=None):
    default_dress = confmgr.get('role_config', str(role_id), 'default_dress')
    if part_id:
        return default_dress.get(part_id)
    return default_dress


def get_default_dress_item_by_part(role_id, part_id):
    default_item = confmgr.get('role_config', str(role_id), 'default_item')
    if part_id:
        return default_item.get(str(part_id))
    else:
        return None


def get_dress_path--- This code section failed: ---

  94       0  LOAD_FAST             0  'dress_conf'
           3  POP_JUMP_IF_TRUE     71  'to 71'

  95       6  LOAD_FAST             4  'default_part_id'
           9  LOAD_CONST            0  ''
          12  COMPARE_OP            8  'is'
          15  POP_JUMP_IF_FALSE    22  'to 22'

  96      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

  97      22  LOAD_GLOBAL           1  'get_default_dress'
          25  LOAD_FAST             1  'role_id'
          28  LOAD_FAST             4  'default_part_id'
          31  CALL_FUNCTION_2       2 
          34  STORE_FAST            6  'dress_id'

  98      37  LOAD_GLOBAL           2  'get_dress_conf'
          40  LOAD_CONST            0  ''
          43  LOAD_FAST             6  'dress_id'
          46  CALL_FUNCTION_2       2 
          49  STORE_FAST            0  'dress_conf'

  99      52  LOAD_FAST             0  'dress_conf'
          55  LOAD_CONST            0  ''
          58  COMPARE_OP            8  'is'
          61  POP_JUMP_IF_FALSE    71  'to 71'

 100      64  LOAD_CONST            0  ''
          67  RETURN_END_IF    
        68_0  COME_FROM                '61'
          68  JUMP_FORWARD          0  'to 71'
        71_0  COME_FROM                '68'

 101      71  JUMP_FORWARD          1  'to 75'
          74  BINARY_SUBSCR    
        75_0  COME_FROM                '71'
          75  STORE_FAST            7  'res'

 102      78  LOAD_GLOBAL           3  'confmgr'
          81  LOAD_ATTR             4  'get'
          84  LOAD_CONST            2  'role_config'
          87  LOAD_GLOBAL           5  'str'
          90  LOAD_FAST             1  'role_id'
          93  CALL_FUNCTION_1       1 
          96  LOAD_CONST            3  'sex'
          99  CALL_FUNCTION_3       3 
         102  STORE_FAST            8  'sex'

 103     105  LOAD_CONST            4  'character/{}'
         108  LOAD_ATTR             6  'format'
         111  LOAD_FAST             7  'res'
         114  LOAD_ATTR             6  'format'
         117  LOAD_FAST             1  'role_id'
         120  LOAD_GLOBAL           7  'SEX_CONF'
         123  LOAD_FAST             8  'sex'
         126  BINARY_SUBSCR    
         127  LOAD_FAST             2  'lod'
         130  LOAD_FAST             3  'style'
         133  LOAD_FAST             5  'suit_id'
         136  CALL_FUNCTION_5       5 
         139  CALL_FUNCTION_1       1 
         142  RETURN_VALUE     

Parse error at or near `BINARY_SUBSCR' instruction at offset 74


def get_dress_res_by_item_no(item_no, default_dress_id=None):
    conf = get_dress_conf(item_no, default_dress_id)
    if conf is None:
        return
    else:
        return conf.get('res', None)


def get_dress_path_by_item_no_and_part_id(item_no, part_id, role_id, lod=iconst.LOD_H, style=None):
    default_dress_id = confmgr.get('role_config', str(role_id), 'default_dress', str(part_id))
    return get_dress_path_by_item_no(item_no, default_dress_id, role_id, lod, style)


def get_dress_path_by_item_no(item_no, default_dress_id, role_id, lod=iconst.LOD_H, style=None):
    res = get_dress_res_by_item_no(item_no, default_dress_id)
    if res is None:
        return
    else:
        sex = confmgr.get('role_config', str(role_id), 'sex')
        return 'character/{}'.format(res.format(role_id, SEX_CONF[sex], lod, style))


def get_dress_path_by_part_id(part_id, role_id, lod=iconst.LOD_H, style=None):
    sex = confmgr.get('role_config', str(role_id), 'sex')
    default_dress_id = confmgr.get('role_config', str(role_id), 'default_dress', str(part_id))
    item_no = global_data.player.get_clothing_by_part_id(part_id)
    res = get_dress_res_by_item_no(item_no, default_dress_id)
    if not res:
        return None
    else:
        return 'character/{}'.format(res.format(role_id, SEX_CONF[role_id], lod, style))


def get_dress_items(dress_items, parts=[iconst.DRESS_POS_HEAD, iconst.DRESS_POS_BODICE, iconst.DRESS_POS_BOTTOMS]):
    items = {}
    for part_id in parts:
        items[part_id] = dress_items.get(part_id, None)

    return items


def check_default_dress(clothing_dict, role_id, check_face=False):
    dress_dict = {}
    dress_dict.update(clothing_dict)
    default_dress = confmgr.get('role_config', str(role_id), 'default_dress')
    default_item = confmgr.get('role_config', str(role_id), 'default_item')
    for part_id in six.iterkeys(default_dress):
        if not check_face and part_id == iconst.DRESS_POS_FACE:
            continue
        if part_id not in clothing_dict:
            dress_dict[part_id] = {'item_id': default_item[part_id]}

    return dress_dict


def get_merge_info(dress_dict, role_id, lod, style):
    import world
    merge_info = None
    dress_conf_dict = {}
    default_dress = get_default_dress(role_id)
    for part_id in sorted(six_ex.keys(dress_dict)):
        item_data = dress_dict[part_id]
        dress_conf = get_dress_conf(item_data['item_id'], default_dress.get(part_id))
        dress_path = get_dress_path(dress_conf, role_id, lod, style, part_id)
        dress_conf_dict[part_id] = dress_conf

    return (dress_conf_dict, merge_info)


def default_shadow_path(role_id):
    return 'character/{0}/shadow/{0}_shadow.gim'.format(role_id)


def xray_model_path(role_id):
    return 'character/{0}/xray/{0}_xray.gim'.format(role_id)


class DresserModel(object):

    def __init__(self, model, role_id, lod=iconst.LOD_H, style=iconst.DEFAULT_STYLE, dress_dict={}, suit_id=None):
        import weakref
        self._model = weakref.ref(model)
        self._role_id = role_id
        self._lod = lod
        self._suit_id = suit_id
        self._init_dress_dict = dress_dict if dress_dict else {}
        self._dress_dict = self._init_dress_dict.copy()
        self._multi_task_id = 0
        self._multi_2_single_task_map = {}
        self._single_2_multi_task_map = {}

    def destroy(self):
        for pos in six_ex.keys(self._dress_dict):
            self.delete_clothing(pos)

    def _get_multi_task_id(self):
        self._multi_task_id += 1
        return self._multi_task_id

    def get_model(self):
        return self._model()

    def set_suit_id(self, suit_id):
        if suit_id == self._suit_id:
            return
        self._suit_id = suit_id
        cur_clothing = get_suit_clothing(self._role_id, self._suit_id, self._lod)
        for pos in six_ex.keys(cur_clothing):
            can_delete = pos not in self._init_dress_dict
            if can_delete:
                self.delete_clothing(pos)

        self._dress_dict = self._init_dress_dict.copy()

    def get_suit_id(self):
        return self._suit_id

    def _do_callback(self, res, userdata, *pass_args):
        callback, args = userdata
        if callback:
            return callback(res, *args)

    def async_load_res(self, path, callback, *args):
        import world
        import game3d
        world.create_res_object_async(path, self._do_callback, (callback, args), game3d.ASYNC_HIGH)

    def get_other_clothing(self, cur_clothing, ohter_clothing):
        if not ohter_clothing:
            return
        else:
            cur_suit_wgg_conf = get_suit_wgg(self._role_id, self._suit_id, self._lod)
            cur_suit_wgg_exclude = confmgr.get('dress_wgg', str(self._suit_id), 'wgg_exclude')
            for pos, _ in six.iteritems(ohter_clothing):
                if str(pos) in cur_clothing:
                    continue
                wgg_path = cur_suit_wgg_conf.get(str(pos), None)
                wgg_exclude = cur_suit_wgg_exclude.get(str(pos), [])
                if wgg_path is None:
                    continue
                cur_clothing[str(pos)] = wgg_path
                for ex_pos in wgg_exclude:
                    if str(ex_pos) in cur_clothing:
                        del cur_clothing[str(ex_pos)]

            return

    def dress(self, ohter_clothing=None, callback=None, valid_checker=None):
        suit_clothing = confmgr.get('dress_suit', str(self._suit_id), 'suit_clothing', default={})
        if not suit_clothing:
            return
        cur_clothing = get_suit_clothing(self._role_id, self._suit_id, self._lod)
        self.get_other_clothing(cur_clothing, ohter_clothing)
        for pos in six_ex.keys(self._dress_dict):
            can_delete = pos not in cur_clothing
            if can_delete:
                self.delete_clothing(pos)

        multi_task_id = self._get_multi_task_id()
        for pos, cpath in six.iteritems(cur_clothing):
            if pos in self._dress_dict:
                continue
            signle_task_id = DressLoader.add_load_task(cpath, self._load_dress_callback, [pos, cpath, callback, multi_task_id, valid_checker], res_type=RES_TYPE_UNKNOWN, sync_priority=game3d.ASYNC_HIGH)
            self._dress_dict[pos] = signle_task_id
            if multi_task_id:
                if multi_task_id not in self._multi_2_single_task_map:
                    self._multi_2_single_task_map[multi_task_id] = {}
                self._multi_2_single_task_map[multi_task_id][signle_task_id] = pos
                self._single_2_multi_task_map[signle_task_id] = multi_task_id

    def _load_dress_callback(self, res, cb_data):
        pos, cpath, cb, multi_task_id, valid_checker = cb_data
        is_valid = True
        if valid_checker:
            is_valid = valid_checker()
        if not is_valid:
            return
        else:
            model = self._model()
            if not model or not model.valid:
                return
            if multi_task_id is None:
                model.add_mesh(res)
                self._dress_dict[pos] = cpath
                self._set_submesh_hitskip(pos)
                if callable(cb):
                    cb()
            elif multi_task_id in self._multi_2_single_task_map:
                m2smap = self._multi_2_single_task_map[multi_task_id]
                for single_task_id, item in six.iteritems(m2smap):
                    if isinstance(item, str) and item == pos:
                        m2smap[single_task_id] = [
                         res, pos, cpath]

                is_all_complete = True
                for item in six.itervalues(m2smap):
                    if isinstance(item, str):
                        is_all_complete = False

                if is_all_complete:
                    for single_task_id, item in six.iteritems(m2smap):
                        if single_task_id in self._single_2_multi_task_map:
                            del self._single_2_multi_task_map[single_task_id]
                        res, pos, cpath = item
                        model.add_mesh(res)
                        self._dress_dict[pos] = cpath
                        self._set_submesh_hitskip(pos)

                    if callable(cb):
                        cb()
                    del self._multi_2_single_task_map[multi_task_id]
            return

    def _set_submesh_hitskip(self, pos):
        model = self._model()
        if model and model.valid:
            if pos in iconst.MESH_CONF:
                mesh_name = iconst.MESH_CONF[pos]
                model.set_submesh_hitmask(mesh_name, world.HIT_SKIP)
            else:
                import traceback
                traceback.print_stack()

    def delete_clothing(self, pos):
        if pos not in self._dress_dict:
            return
        cur_dress = self._dress_dict[pos]
        if isinstance(cur_dress, int):
            if cur_dress in self._single_2_multi_task_map:
                single_id = cur_dress
                multi_id = self._single_2_multi_task_map[single_id]
                del self._single_2_multi_task_map[single_id]
                if multi_id in self._multi_2_single_task_map:
                    m2smap = self._multi_2_single_task_map[multi_id]
                    if single_id in m2smap:
                        item_data = m2smap[single_id]
                        del m2smap[single_id]
            DressLoader.cancel_task(cur_dress)
            del self._dress_dict[pos]
        elif isinstance(cur_dress, str):
            model = self._model()
            if model and model.valid:
                model.remove_mesh(cur_dress)
            del self._dress_dict[pos]

    def _change_lod_callback(self, res_list, pos_list, dress_list):
        pass

    def set_lod(self, lod):
        pass


def init_dress_merge_sys--- This code section failed: ---

 406       0  SETUP_EXCEPT        142  'to 145'

 407       3  LOAD_CONST            1  ''
           6  LOAD_CONST            0  ''
           9  IMPORT_NAME           0  'render'
          12  STORE_FAST            0  'render'

 408      15  LOAD_GLOBAL           1  'hasattr'
          18  LOAD_GLOBAL           2  'confmgr'
          21  CALL_FUNCTION_2       2 
          24  POP_JUMP_IF_TRUE     31  'to 31'

 409      27  LOAD_CONST            0  ''
          30  RETURN_END_IF    
        31_0  COME_FROM                '24'

 411      31  LOAD_GLOBAL           2  'confmgr'
          34  LOAD_ATTR             3  'get_raw'
          37  LOAD_CONST            3  'dress_part_uv'
          40  LOAD_CONST            4  'content'
          43  CALL_FUNCTION_2       2 
          46  STORE_FAST            1  'conf'

 412      49  SETUP_LOOP           89  'to 141'
          52  LOAD_GLOBAL           4  'six'
          55  LOAD_ATTR             5  'iteritems'
          58  LOAD_FAST             1  'conf'
          61  CALL_FUNCTION_1       1 
          64  GET_ITER         
          65  FOR_ITER             72  'to 140'
          68  UNPACK_SEQUENCE_2     2 
          71  STORE_FAST            2  'k'
          74  STORE_FAST            3  'v'

 413      77  LOAD_FAST             3  'v'
          80  LOAD_CONST            1  ''
          83  BINARY_SUBSCR    
          84  POP_JUMP_IF_FALSE    65  'to 65'

 415      87  LOAD_FAST             0  'render'
          90  LOAD_ATTR             6  'set_part_uv'
          93  LOAD_GLOBAL           7  'int'
          96  LOAD_FAST             2  'k'
          99  CALL_FUNCTION_1       1 
         102  LOAD_FAST             3  'v'
         105  LOAD_CONST            5  1
         108  BINARY_SUBSCR    
         109  LOAD_FAST             3  'v'
         112  LOAD_CONST            6  2
         115  BINARY_SUBSCR    
         116  LOAD_FAST             3  'v'
         119  LOAD_CONST            7  3
         122  BINARY_SUBSCR    
         123  LOAD_FAST             3  'v'
         126  LOAD_CONST            8  4
         129  BINARY_SUBSCR    
         130  CALL_FUNCTION_5       5 
         133  POP_TOP          
         134  JUMP_BACK            65  'to 65'
         137  JUMP_BACK            65  'to 65'
         140  POP_BLOCK        
       141_0  COME_FROM                '49'
         141  POP_BLOCK        
         142  JUMP_FORWARD         47  'to 192'
       145_0  COME_FROM                '0'

 416     145  DUP_TOP          
         146  LOAD_GLOBAL           8  'Exception'
         149  COMPARE_OP           10  'exception-match'
         152  POP_JUMP_IF_FALSE   191  'to 191'
         155  POP_TOP          
         156  STORE_FAST            4  'e'
         159  POP_TOP          

 417     160  LOAD_CONST            1  ''
         163  LOAD_CONST            0  ''
         166  IMPORT_NAME           9  'traceback'
         169  STORE_FAST            5  'traceback'

 418     172  LOAD_FAST             5  'traceback'
         175  LOAD_ATTR            10  'print_exc'
         178  CALL_FUNCTION_0       0 
         181  POP_TOP          

 419     182  LOAD_FAST             4  'e'
         185  RAISE_VARARGS_1       1 
         188  JUMP_FORWARD          1  'to 192'
         191  END_FINALLY      
       192_0  COME_FROM                '191'
       192_1  COME_FROM                '142'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21


def mecha_lobby_id_2_battle_id(mecha_lobby_id):
    mecha_dict = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
    return mecha_dict.get(str(mecha_lobby_id), {}).get('battle_mecha_id', mecha_lobby_id)


def battle_id_to_mecha_lobby_id(mecha_id):
    mecha_dict = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
    for lobby_item_id, info in six.iteritems(mecha_dict):
        if info.get('battle_mecha_id') == mecha_id:
            return int(lobby_item_id)


def get_role_item_no(role_id, clothing_id):
    if clothing_id is not None:
        return clothing_id
    else:
        return role_id


def get_mecha_default_fashion(mecha_id):
    mecha_item_no = battle_id_to_mecha_lobby_id(int(mecha_id))
    return confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')[0]


def get_mecha_item_default_fashion(mecha_item_no):
    return confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_no), 'default_fashion')[0]


def get_role_model_path(role_id, clothing_id):
    path = None
    if clothing_id is not None:
        path = confmgr.get('role_info', 'RoleSkin', 'Content', str(clothing_id), 'model_path')
    if path is None and role_id is None:
        return
    else:
        if path is None and role_utils.is_role_publish(role_id):
            path = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'model_path')
        return path


def get_role_model_h_path_after_create(role_id):
    item_data = global_data.player.get_item_by_no(role_id)
    fashion_data = item_data.get_fashion()
    dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
    return get_role_model_path_by_lod(role_id, dressed_clothing_id, 'h')


def get_role_model_path_by_lod(role_id, clothing_id, lod_level='h'):
    path = get_role_model_path(role_id, clothing_id)
    if path:
        index = path.find('empty.gim')
        if index != -1:
            dir_path = path[0:index]
            path = dir_path + '{}.gim'.format(lod_level)
    return path


def get_mecha_skin_item_no(mecha_id, clothing_id):
    if clothing_id and clothing_id != DEFAULT_CLOTHING_ID:
        return clothing_id
    mecha_dict = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
    for lobby_item_id, info in six.iteritems(mecha_dict):
        if info.get('battle_mecha_id') == mecha_id:
            return info.get('default_fashion')[0]


def get_mecha_model_offset_y(clothing_id):
    if clothing_id == DEFAULT_CLOTHING_ID:
        return 0
    mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
    skin_data = mecha_skin_conf.get(str(clothing_id))
    return skin_data.get('model_offset_y', 0) * NEOX_UNIT_SCALE


def get_mecha_model_path(mecha_id, clothing_id, shiny_weapon_id=None):
    path = None
    if clothing_id != DEFAULT_CLOTHING_ID:
        mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        skin_data = mecha_skin_conf.get(str(clothing_id))
        if skin_data is not None:
            model_path = None
            if shiny_weapon_id:
                model_path = skin_data.get('shiny_weapon_model_path', None)
                if model_path and type(model_path) is dict:
                    model_path = model_path.get(str(shiny_weapon_id), None)
            model_path = model_path or skin_data.get('model_path', None)
            if model_path is not None:
                path = model_path
    if path is None and mecha_id is None:
        return
    else:
        if path is None:
            mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
            mechainfo = mecha_conf[str(mecha_id)]
            path = mechainfo['model_path']
        return path


def get_mecha_weapon_model_path(mecha_id, clothing_id):
    path = None
    if clothing_id != DEFAULT_CLOTHING_ID:
        mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        skin_data = mecha_skin_conf.get(str(clothing_id))
        if skin_data is not None:
            model_path = skin_data.get('weapon_model_path', None)
            if model_path is not None:
                path = model_path
    return path


def get_mecha_model_h_path(mecha_id, clothing_id, auto_use_low_model=True, shiny_weapon_id=None):
    path = get_mecha_model_path(mecha_id, clothing_id, shiny_weapon_id)
    h_name = global_data.gsetting.mapping_mecha_lod_name('h') + '.gim' if auto_use_low_model else 'h.gim'
    if path:
        index = path.find('empty.gim')
        if index != -1:
            path = path[0:index] + h_name
    return path


def get_pet_model_path(clothing_id):
    return confmgr.get('c_pet_info', str(clothing_id), 'model_path', default='')


def get_pet_model_h_path(clothing_id):
    path = get_pet_model_path(clothing_id)
    if path:
        index = path.find('empty.gim')
        if index != -1:
            path = path[0:index] + 'h.gim'
    return path


FORCE_USE_H_MECHA = (8029, 201802451, 201802452, 201802453)

def get_mecha_model_lod_path(mecha_id, clothing_id, lod_level, auto_use_low_model=True, shiny_weapon_id=None):
    path = get_mecha_model_path(mecha_id, clothing_id, shiny_weapon_id)
    lod_name = ['l', 'l1', 'l2', 'l3', 'h']
    if path:
        index = path.find('empty.gim')
        if index != -1:
            real_lod_name = lod_name[lod_level]
            if auto_use_low_model:
                real_lod_name = global_data.gsetting.mapping_mecha_lod_name(real_lod_name)
            if mecha_id in FORCE_USE_H_MECHA or clothing_id in FORCE_USE_H_MECHA:
                real_lod_name = 'h'
            path = '{}{}{}'.format(path[0:index], real_lod_name, '.gim')
    return path


def get_mecha_model_hit_path(mecha_id, clothing_id):
    path = None
    if clothing_id != DEFAULT_CLOTHING_ID:
        mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        skin_data = mecha_skin_conf.get(str(clothing_id))
        if skin_data is not None:
            model_path = skin_data.get('hit_path', None)
            if model_path is not None:
                path = model_path
    if path is None:
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        mechainfo = mecha_conf[str(mecha_id)]
        path = mechainfo['hit_path']
    return path


def get_mecha_dress_clothing_id(mecha_id=None, mecha_item_id=None):
    if mecha_id:
        mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
    if not global_data.player:
        return
    else:
        mecha_item_data = global_data.player.get_item_by_no(mecha_item_id)
        if mecha_item_data is not None:
            fashion_data = mecha_item_data.get_fashion()
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            if dressed_clothing_id is not None:
                clothing_data = global_data.player.get_item_by_no(dressed_clothing_id)
                if clothing_data is not None:
                    return dressed_clothing_id
        return


def get_ob_mecha_dress_clothing_id(mecha_id, mecha_dict):
    dressed_clothing_id = mecha_dict.get(mecha_id, {}).get('fashion', {}).get(FASHION_POS_SUIT)
    return dressed_clothing_id


def get_mecha_dress_shiny_weapon_id(mecha_id):
    mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
    mecha_item_data = global_data.player.get_item_by_no(mecha_item_id)
    if not mecha_item_data:
        return None
    else:
        fashion_data = mecha_item_data.get_fashion()
        return fashion_data.get(FASHION_POS_WEAPON_SFX)


def get_role_dress_clothing_id(role_id, check_default=False):
    if global_data.player:
        item_data = global_data.player.get_item_by_no(role_id)
    else:
        item_data = None
    default_val = None
    if check_default:
        default_val = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
    if item_data is not None:
        fashion_data = item_data.get_fashion()
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        if dressed_clothing_id is not None:
            clothing_data = global_data.player.get_item_by_no(dressed_clothing_id)
            if clothing_data is not None:
                return dressed_clothing_id
            if check_default:
                return default_val
    return default_val


def get_role_decroation_id(role_id, skin_id, decroation_type):
    item_data = global_data.player.get_item_by_no(role_id)
    if item_data is not None:
        fashion_data = item_data.get_fashion()
        dressed_headwear_id = fashion_data.get(decroation_type)
        if dressed_headwear_id is not None:
            clothing_data = global_data.player.get_item_by_no(dressed_headwear_id)
            if clothing_data is not None and check_valid_decoration(skin_id, dressed_headwear_id):
                return dressed_headwear_id
    return


def get_role_fashion_data(role_id, skin_id, decroation_type_list):
    item_data = global_data.player.get_item_by_no(role_id)
    dec_dict = {}
    if item_data is not None:
        fashion_data = item_data.get_fashion()
        for decroation_type in decroation_type_list:
            dressed_headwear_id = fashion_data.get(decroation_type)
            if dressed_headwear_id is not None:
                clothing_data = global_data.player.get_item_by_no(dressed_headwear_id)
                if clothing_data is not None and check_valid_decoration(skin_id, dressed_headwear_id):
                    dec_dict[decroation_type] = dressed_headwear_id

        return dec_dict
    else:
        return


def get_skin_default_show_decoration_dict(skin_id):
    from logic.gutils.item_utils import get_lobby_item_type
    cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), default={})
    default_show_dec_id_list = cur_skin_cnf.get('default_show_dec_id_list', [])
    default_show_dict = {}
    for dec_id in default_show_dec_id_list:
        lobby_type = get_lobby_item_type(dec_id)
        fashion_pos = get_lobby_type_fashion_pos(lobby_type)
        if fashion_pos:
            default_show_dict[fashion_pos] = dec_id

    return default_show_dict


def get_skin_default_wear_decoration_list(skin_id, real_skin_id=None):
    top_skin_id = get_top_skin_id_by_skin_id(skin_id) or skin_id
    skin_valid_pendant_conf = confmgr.get('top_role_skin_pendant_conf', str(top_skin_id), default={})
    DefaultDecList = skin_valid_pendant_conf.get('DefaultDecList', [])
    if real_skin_id:
        return [ d_id for d_id in DefaultDecList if check_valid_decoration(real_skin_id, d_id) ]
    else:
        return DefaultDecList


def get_skin_default_wear_decoration_dict(skin_id, real_skin_id):
    if type(skin_id) == str and skin_id.isdigit():
        skin_id = int(skin_id)
    if type(real_skin_id) == str and real_skin_id.isdigit():
        real_skin_id = int(real_skin_id)
    DefaultDecList = get_skin_default_wear_decoration_list(skin_id, real_skin_id)
    if DefaultDecList:
        default_pos_dec_dict = decoration_list_to_fashion_dict(DefaultDecList)
        return default_pos_dec_dict
    return {}


def get_top_skin_need_completion_dec_dict(role_id, top_skin_id, current_wear_dict, real_skin_id=None):
    dec_dict = get_skin_default_wear_decoration_dict(top_skin_id, real_skin_id)
    if not dec_dict:
        return {}
    completion_dec_dict = {}
    for pos, dec_id in six.iteritems(dec_dict):
        if not current_wear_dict.get(pos) or not check_valid_decoration(real_skin_id if real_skin_id else top_skin_id, current_wear_dict[pos]):
            completion_dec_dict[pos] = dec_id

    return completion_dec_dict


def get_real_dec_dict_with_check_completion_and_replacement(skin_id, head_id=None, bag_id=None, suit_id=None, other_pendants=None, improved_skin_id=None):
    top_skin_id = get_top_skin_id_by_skin_id(skin_id)
    cur_wear_dict = {}
    if head_id:
        cur_wear_dict[FASHION_POS_HEADWEAR] = head_id
    if bag_id:
        cur_wear_dict[FASHION_POS_BACK] = bag_id
    if suit_id:
        cur_wear_dict[FASHION_POS_SUIT_2] = suit_id
    if other_pendants:
        cur_wear_dict[FASHION_OTHER_PENDANT_LIST] = other_pendants
    comp_dict = get_top_skin_need_completion_dec_dict(None, top_skin_id, cur_wear_dict, skin_id)
    head_id = comp_dict.get(FASHION_POS_HEADWEAR) or head_id
    bag_id = comp_dict.get(FASHION_POS_BACK) or bag_id
    suit_id = comp_dict.get(FASHION_POS_SUIT_2) or suit_id
    if not other_pendants:
        other_pendants = []
    for pos in FASHION_OTHER_PENDANT_LIST:
        dec_item_id = comp_dict.get(pos)
        if dec_item_id and dec_item_id not in other_pendants:
            other_pendants = list(other_pendants)
            other_pendants.append(dec_item_id)

    force_default_head_dec = check_force_default_head_dec(skin_id)
    if force_default_head_dec:
        head_id = force_default_head_dec
    force_default_bag_dec = check_force_default_bag_dec(skin_id)
    if force_default_bag_dec:
        bag_id = force_default_bag_dec
    if improved_skin_id:

        def try_get_improve_pendant_id(s_id, p_id):
            return get_improve_pendant_id(s_id, p_id) or p_id

        head_id = try_get_improve_pendant_id(skin_id, head_id)
        bag_id = try_get_improve_pendant_id(skin_id, bag_id)
        suit_id = try_get_improve_pendant_id(skin_id, suit_id)
        new_other_pendants = []
        for pendant_id in other_pendants:
            new_pid = try_get_improve_pendant_id(skin_id, pendant_id)
            new_other_pendants.append(new_pid)

        other_pendants = new_other_pendants
        change_head = get_improve_skin_head_id(improved_skin_id)
        if change_head:
            head_id = change_head
    return (head_id, bag_id, suit_id, other_pendants)


def get_role_fashion_decoration_dict(role_id, top_skin_id, decoration_type_list=None):
    role_top_skin_scheme = global_data.player.get_or_request_role_top_skin_scheme(role_id)
    if role_top_skin_scheme is None:
        log_error('role fashion decoration data should fetch in advance!')
        return {}
    else:
        if not decoration_type_list:
            from logic.gcommon.item.item_const import FASHION_DECORATION_TYPE_LIST
            decoration_type_list = FASHION_DECORATION_TYPE_LIST
        top_skin_scheme = role_top_skin_scheme.get(str(top_skin_id), {})
        decoration_dict = {}
        for d_type in decoration_type_list:
            if d_type in top_skin_scheme:
                decoration_dict[d_type] = top_skin_scheme[d_type]

        return decoration_dict


def get_role_top_skin_owned_second_skin_list(top_skin_id):
    top_skin_second_skin_list = confmgr.get('top_role_skin_conf', str(top_skin_id), default=[])
    return top_skin_second_skin_list


def get_top_skin_clothing_id(role_id, top_skin_id, role_skin_id=None):
    top_skin_second_skin_list = confmgr.get('top_role_skin_conf', str(top_skin_id), default={})
    if not role_skin_id:
        role_skin_id = get_role_dress_clothing_id(role_id)
    if role_skin_id in top_skin_second_skin_list:
        return role_skin_id
    else:
        if global_data.player.check_need_request_role_top_skin_scheme(role_id):
            log_error('need_ request role fashion scheme in advance')
        else:
            top_skin_scheme = global_data.player.get_role_top_skin_scheme_br_role_and_skin(role_id, top_skin_id)
            top_skin_suit = top_skin_scheme.get(FASHION_POS_SUIT, None)
            if top_skin_suit in top_skin_second_skin_list:
                return top_skin_suit
        own_skin_list = []
        own_func = global_data.player.has_item_by_no if global_data.player else (lambda : False)
        for skin_id in top_skin_second_skin_list:
            own = own_func(skin_id)
            if own:
                own_skin_list.append(skin_id)

        own_skin_list = sorted(own_skin_list)
        if own_skin_list:
            return own_skin_list[0]
        return top_skin_id
        return


def get_top_skin_clothing_id_list(role_id, top_skin_list):
    role_skin_id = get_role_dress_clothing_id(role_id)
    show_skin_list = []
    for top_skin_id in top_skin_list:
        show_skin_id = get_top_skin_clothing_id(role_id, top_skin_id, role_skin_id)
        if not show_skin_id:
            show_skin_list.append(top_skin_id)
        else:
            show_skin_list.append(show_skin_id)

    return show_skin_list


def get_top_skin_id_by_skin_id(skin_id):
    cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), default={})
    belonging_top_skin_id = cur_skin_cnf.get('belonging_top_skin_id')
    if not belonging_top_skin_id:
        log_error('get_top_skin_id_by_skin_id is not a valid second skin!!!!', skin_id)
        return skin_id
    return belonging_top_skin_id


def skin_plan_to_fashion_dict(plan_data):
    from logic.gcommon.item.item_const import FASHION_PLAN_POS_NAME, PLAN_POS_LIST, PLAN_POS_TO_TAG
    fashion_dict = {}
    other_dict = {}
    if plan_data:
        pos_list = PLAN_POS_LIST
        for pos in pos_list:
            if pos < len(plan_data):
                if pos == FASHION_PLAN_POS_NAME:
                    other_dict['name'] = plan_data[pos]
                else:
                    pos_data = plan_data[pos]
                    if pos_data != -1 and pos_data:
                        if pos in PLAN_POS_TO_TAG:
                            TAG = PLAN_POS_TO_TAG[pos]
                            fashion_dict[TAG] = pos_data

    return (
     fashion_dict, other_dict)


def fashion_dict_to_skin_plan(fashion_dict, name=''):
    from logic.gcommon.item.item_const import FASHION_PLAN_POS_NAME, PLAN_POS_LIST, PLAN_POS_TO_TAG
    plan_list = []
    for pos in PLAN_POS_LIST:
        if pos == FASHION_PLAN_POS_NAME:
            plan_list.append(name)
        else:
            plan_list.append(fashion_dict.get(PLAN_POS_TO_TAG[pos], 0))

    return plan_list


def get_lobby_type_fashion_pos(lobby_type):
    from logic.gcommon.item import lobby_item_type
    from logic.gcommon.item import item_const
    lobby_type_2_fashion_pos = {lobby_item_type.L_ITEM_TYPE_HEAD: item_const.FASHION_POS_HEADWEAR,
       lobby_item_type.L_ITEM_TYPE_BODY: item_const.FASHION_POS_BACK,
       lobby_item_type.L_ITEM_TYPE_LEG_DEC: item_const.FASHION_POS_LEG,
       lobby_item_type.L_ITEM_TYPE_FACE_DEC: item_const.FASHION_POS_FACE,
       lobby_item_type.L_ITEM_TYPE_WAIST_DEC: item_const.FASHION_POS_WAIST,
       lobby_item_type.L_ITEM_TYPE_HAIR_DEC: item_const.FASHION_POS_HAIR,
       lobby_item_type.L_ITEM_TYPE_SUIT: item_const.FASHION_POS_SUIT_2,
       lobby_item_type.L_ITEM_TYPE_ARM_DEC: item_const.FASHION_POS_ARM
       }
    return lobby_type_2_fashion_pos.get(lobby_type, None)


def decoration_list_to_fashion_dict(preview_decoration_list):
    from logic.gutils import item_utils
    from logic.gcommon.item.lobby_item_type import ITEM_TYPE_DEC
    preview_decoration = {}
    for item_no in preview_decoration_list:
        l_item_type = item_utils.get_lobby_item_type(item_no)
        if l_item_type in ITEM_TYPE_DEC:
            fashion_pos = get_lobby_type_fashion_pos(l_item_type)
            if fashion_pos is not None:
                preview_decoration[fashion_pos] = item_no

    return preview_decoration


def collocation_list_to_fashion_dict(collocation_list):
    from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN
    from logic.gutils import item_utils
    from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR
    fashion_dict = {}
    decoration_list = list(collocation_list)
    for item_no in collocation_list:
        l_item_type = item_utils.get_lobby_item_type(item_no)
        if l_item_type == L_ITEM_TYPE_ROLE_SKIN:
            fashion_dict[FASHION_POS_SUIT] = item_no
            decoration_list.remove(item_no)

    decoration_dict = decoration_list_to_fashion_dict(collocation_list)
    fashion_dict.update(decoration_dict)
    return fashion_dict


def check_valid_decoration(skin_id, decoration_id):
    if not skin_id:
        return False
    skin_id = int(skin_id)
    restrict_info = confmgr.get('pendant', 'SkinRestrict', str(decoration_id), default={})
    unusable_skin_list = restrict_info.get('unusable_skin_list', [])
    usable_skin_list = restrict_info.get('usable_skin_list', [])
    if skin_id in unusable_skin_list:
        return False
    if skin_id not in usable_skin_list:
        return False
    return True


def get_decoration_id_skin_list(decoration_id, top_skin_only=False):
    from logic.gutils import item_utils
    if not top_skin_only:
        _skin_list = confmgr.get('pendant_skin_list_conf', str(decoration_id), 'SecSkinList', default=[])
    else:
        _skin_list = confmgr.get('pendant_skin_list_conf', str(decoration_id), 'TopSkinList', default=[])
    skin_list = []
    for deco_type in _skin_list:
        if item_utils.can_open_show(deco_type):
            skin_list.append(deco_type)

    return skin_list


def get_invisible_decoration_id_list():
    invisible_decoration_id_list = []
    from logic.gutils import item_utils
    restrict_info = confmgr.get('pendant', 'SkinRestrict', default={})
    role_info = confmgr.get('role_info', 'RoleInfo', 'Content', default={})
    role_skins = confmgr.get('role_info', 'RoleSkin', 'Content', default={})
    skin_set = set()
    for info in six.itervalues(role_info):
        skin_set.update(info.get('skin_list', []))

    for dec_id, dec_conf in six.iteritems(restrict_info):
        if type(dec_conf) != dict:
            continue
        if dec_conf.get('is_invisible_in_list', False) or not item_utils.can_open_show(dec_id):
            invisible_decoration_id_list.append(int(dec_id))
        else:
            cur_usable_set = set(dec_conf.get('usable_skin_list', []))
            cur_unusable_set = set(dec_conf.get('unusable_skin_list', []))
            cur_usable_set -= cur_unusable_set
            for skin_id in cur_usable_set:
                if skin_id in skin_set or role_skins.get(str(skin_id), {}).get('belonging_top_skin_id', None) in skin_set:
                    break
            else:
                invisible_decoration_id_list.append(int(dec_id))

    return invisible_decoration_id_list


def get_valid_deco_list_for_skin_id(role_id, skin_id, pendant_ty_list=None):
    top_skin_id = get_top_skin_id_by_skin_id(skin_id) or skin_id
    skin_valid_pendant_conf = confmgr.get('top_role_skin_pendant_conf', str(top_skin_id), default={})
    ret_list = []
    if not pendant_ty_list:
        ret_list = skin_valid_pendant_conf.get('AllValidDec', [])
    else:
        deco_list = []
        for deco_type in pendant_ty_list:
            deco_list.extend(skin_valid_pendant_conf.get('ValidDecDict', {}).get(deco_type, []))

        ret_list = deco_list
    final_ret_list = []
    from logic.gutils import item_utils
    for item in ret_list:
        if item_utils.can_open_show(item):
            final_ret_list.append(item)

    return final_ret_list


def check_dec_hide_rp(item_no):
    dec_conf = confmgr.get('pendant', 'SkinRestrict', default={})
    if dec_conf:
        conf = dec_conf.get(str(item_no), {})
        if conf:
            return conf.get('is_invisible_in_list', 0)


def get_goods_id_of_role_dress_related_item_no(item_no):
    from logic.gutils.item_utils import get_lobby_item_type
    from logic.gcommon.item.lobby_item_type import ROLE_SKIN_TYPE, L_ITEM_TYPE_ROLE_SKIN
    lobby_type = get_lobby_item_type(item_no)
    if lobby_type not in ROLE_SKIN_TYPE:
        log_error('get_dress_related_item_goods_id failed', item_no)
        return None
    else:
        if lobby_type == L_ITEM_TYPE_ROLE_SKIN:
            return confmgr.get('role_info', 'RoleSkin', 'Content', str(item_no), 'goods_id', default=None)
        return confmgr.get('pendant', 'SkinRestrict', str(item_no), 'goods_id', default=None)
        return None


def get_vehicle_res(item_id):
    res_path = confmgr.get('items_skin_conf', 'VehicleSkinConfig', 'Content', str(item_id), default={}).get('cRes')
    return res_path


def get_head_model_path(head_id):
    pendant_cnf = confmgr.get('pendant', 'ItemData', str(head_id), default={})
    head_res_path = None
    for belong_skin_id in pendant_cnf:
        head_res_path = pendant_cnf[belong_skin_id].get('pendant_socket_res_path', None)
        if head_res_path:
            break

    return head_res_path


def get_weapon_skin_res(item_id):
    conf = confmgr.get('items_skin_conf', 'WeaponSkinConfig', 'Content', str(item_id), default={})
    return (
     conf.get('cRes'), conf.get('cResLeft'))


def get_weapon_default_fashion(weapon_id):
    weapon_id = int(weapon_id)
    weapon_conf = confmgr.get('items_book_conf', 'WeaponConfig', 'Content')
    for cKey, conf in six.iteritems(weapon_conf):
        if weapon_id in conf['battle_item_no']:
            return conf['default_fashion']

    return None


def get_weapon_skin_channel_list(item_id):
    conf = confmgr.get('items_skin_conf', 'WeaponSkinConfig', 'Content', str(item_id), default={})
    return conf.get('cOpenPackage', [])


def get_weapon_sfx_skin_show_mount_item_no(item_id):
    weapon_sfx_show_data = confmgr.get('lobby_model_display_conf', 'WeaponSfx', 'Content').get(str(item_id))
    if weapon_sfx_show_data:
        return weapon_sfx_show_data.get('mount_item_no', None)
    else:
        return None


def get_file_name(model):
    if not model:
        return ''
    path = model.get_file_path().split('\\')
    if len(path) < 3:
        return ''
    name_suffix = path[-1]
    if name_suffix in ('empty.gim', 'h.gim', 'l.gim', 'l1.gim'):
        name_suffix = path[-2]
    name = name_suffix.split('.')[0]
    if name_suffix.startswith('80'):
        name = name.split('_')[-1]
        if name[0] in ('a', 'b', 'c'):
            name = path[-3]
    elif name_suffix.startswith('60'):
        name = path[-2]
    elif 'character' == path[0]:
        if 'a' in name:
            name = name.split('_')[0]
        else:
            file_name = 'soft_bone_param_%s_%s' % (path[-3], name)
            if C_file.find_res_file('confs/{}.json'.format(file_name), ''):
                return file_name
            name = name.split('_')[0]
    else:
        name = name.split('_')[0]
    file_name = 'soft_bone_param_%s_%s' % (path[-3], name)
    return file_name


def clear_spring_anim(model, param):
    if not model or not model.valid or not param:
        return
    else:
        bone_chains = param['bone_chains']
        if not bone_chains:
            return []
        for part, _ in six.iteritems(bone_chains):
            part = str(part)
            part_model = None
            if part == 'body':
                part_model = model
            elif model.has_socket(part):
                model_list = model.get_socket_objects(part)
                if len(model_list) > 0:
                    part_model = model_list[0]
            if not part_model:
                continue
            if part_model.get_bone_count() > 0:
                part_model.get_spring_anim(True).clear_spring_anim()

        return


def init_spring_anim(model, param):
    if not model or not model.valid or not param:
        return {}
    else:
        part_models = []
        simulation_steps = param.get('simulation_steps', character_anim_const.k_simulation_steps)
        air_friction_idle = param.get('air_friction_idle', character_anim_const.k_air_friction_idle)
        bone_chains = param['bone_chains']
        if not bone_chains:
            return {}
        part_models_wind_param = {}
        for part, chains in six.iteritems(bone_chains):
            part = str(part)
            part_model = None
            if part == 'body':
                part_model = model
            elif model.has_socket(part):
                model_list = model.get_socket_objects(part)
                if len(model_list) > 0:
                    part_model = model_list[0]
            if not part_model or type(part_model) != world.model:
                continue
            anim = part_model.get_spring_anim(True)
            part_models_wind_param[part_model] = part_wind_param = []
            for bone in chains:
                name = bone['name']
                air_friction = bone.get('air_friction', character_anim_const.k_air_friction)
                linear_damping = bone.get('linear_damping', character_anim_const.k_linear_damping)
                mix_ratio = bone.get('mix_ratio', character_anim_const.k_mix_ratio)
                stiffness = bone.get('stiffness', character_anim_const.k_stiffness)
                horizion_rate = bone.get('horizon_rate', 0.0)
                vertical_rate = bone.get('vertical_rate', 0.0)
                anim.set_physx_constants(air_friction, linear_damping, int(simulation_steps), air_friction_idle)
                anim.add_spring_anim(name, mix_ratio, stiffness, 0, horizion_rate, vertical_rate)
                if 'wind_param' in bone:
                    wind_param = {'root_name': name}
                    wind_param.update(bone['wind_param'])
                    part_wind_param.append(wind_param)
                if hasattr(anim, 'apply_clamp_plane'):
                    anim.apply_clamp_plane(name, *bone.get('clamp_plane', [0, 0, 0]))

        anim = model.get_spring_anim(True)
        if hasattr(anim, 'enable_collision'):
            bone_cols = param.get('bone_cols', {})
            part_cols = []
            for col_bone, col_info in six.iteritems(bone_cols):
                if not col_info:
                    continue
                if isinstance(col_info[0], str):
                    target_bones = col_info
                    info = [1, 0]
                elif global_data.feature_mgr.is_support_precise_spring_anim_col() and global_data.is_ue_model:
                    target_bones, info = col_info
                else:
                    target_bones = []
                target_bones_idices = {}
                for bone_name in target_bones:
                    part_name, bone_idx = bone_name.split('-')
                    if part_name not in six.iterkeys(target_bones_idices):
                        target_bones_idices[part_name] = []
                    target_bones_idices[part_name].append(int(bone_idx))

                for part_name, target_bone_list in six.iteritems(target_bones_idices):
                    col_anim = anim
                    if part_name != 'body':
                        if not hasattr(anim, 'set_as_child_spring_anim'):
                            continue
                        if not model.has_socket(part_name):
                            continue
                        model_list = model.get_socket_objects(part_name)
                        if len(model_list) <= 0:
                            continue
                        part_model = model_list[0]
                        if not part_model or type(part_model) != world.model:
                            continue
                        col_anim = part_model.get_spring_anim(True)
                        col_anim.set_as_child_spring_anim(True)
                    if global_data.feature_mgr.is_support_precise_spring_anim_col():
                        col_anim.add_spring_anim_col_obj(col_bone, target_bone_list, 0, info[0], info[1])
                    else:
                        col_anim.add_spring_anim_col_obj(col_bone, target_bone_list, 0)
                    part_cols.append(col_anim)

            for anim in part_cols:
                col_anim.enable_collision()

        if part_models_wind_param:
            for part_model in six.iterkeys(part_models_wind_param):
                if not part_model or not part_model.valid:
                    continue
                part_model.get_spring_anim(True).enable_physx()

        return part_models_wind_param


def get_pendant_conf(skin_id, pendant_id):
    res_cnf = None
    if skin_id is not None and pendant_id is not None:
        if check_valid_decoration(skin_id, pendant_id):
            pendant_cnf = confmgr.get('pendant', 'ItemData', str(pendant_id))
            if pendant_cnf is not None:
                res_cnf = pendant_cnf.get(str(skin_id))
                if res_cnf is None:
                    res_cnf = pendant_cnf.get(str(1))
    return res_cnf


def get_improve_pendant_id(skin_id, pendant_id):
    _conf = get_pendant_conf(skin_id, pendant_id) or {}
    return _conf.get('improved_pendant_id', None)


def get_pendant_head_path(head_id, skin_id):
    head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list = (None,
                                                                                                                None,
                                                                                                                None,
                                                                                                                None,
                                                                                                                None)
    res_cnf = get_pendant_conf(skin_id, head_id)
    if res_cnf is not None:
        head_pendant_type = res_cnf.get('head_pendant_type')
        head_res_path = res_cnf.get('head_res_path')
        pendant_socket_name = res_cnf.get('pendant_socket_name')
        pendant_socket_res_path = res_cnf.get('pendant_socket_res_path')
        pendant_random_anim_list = res_cnf.get('pendant_random_anim_list')
    return (
     head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list)


def get_pendant_bag_path(bag_id, skin_id):
    socket_name = None
    bag_model_path = None
    anim_data = None
    res_cnf = get_pendant_conf(skin_id, bag_id)
    if res_cnf is not None:
        bag_model_path = res_cnf.get('bag_res_path')
        socket_name = res_cnf.get('bag_socket_name')
        anim_data = {}
        anim_data['use_skin_show_anim'] = res_cnf.get('use_skin_show_anim')
        anim_data['use_skin_end_anim'] = res_cnf.get('use_skin_end_anim')
        anim_data['show_anim'] = res_cnf.get('show_anim')
        anim_data['end_anim'] = res_cnf.get('end_anim')
    return (
     bag_model_path, socket_name, anim_data)


def get_pendant_suit_path(suit_id, skin_id):
    head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path = (None,
                                                                                      None,
                                                                                      None,
                                                                                      None)
    bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2 = (None, None,
                                                                          None, None)
    anim_data = None
    res_cnf = get_pendant_conf(skin_id, suit_id)
    if res_cnf is not None:
        head_pendant_type = res_cnf.get('head_pendant_type')
        head_res_path = res_cnf.get('head_res_path')
        pendant_socket_name = res_cnf.get('pendant_socket_name')
        pendant_socket_res_path = res_cnf.get('pendant_socket_res_path')
        bag_socket_name = res_cnf.get('bag_socket_name')
        bag_model_path = res_cnf.get('bag_res_path')
        bag_socket_name2 = res_cnf.get('bag_socket_name2')
        bag_model_path2 = res_cnf.get('bag_res_path2')
        anim_data = {}
        anim_data['use_skin_show_anim'] = res_cnf.get('use_skin_show_anim')
        anim_data['use_skin_end_anim'] = res_cnf.get('use_skin_end_anim')
        anim_data['show_anim'] = res_cnf.get('show_anim')
        anim_data['end_anim'] = res_cnf.get('end_anim')
    return (
     head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2, anim_data)


def get_pendant_other_path(other_id, skin_id):
    head_pendant_type, head_res_path = (None, None)
    res_path, socket_name = (None, None)
    pendant_type = None
    anim_data = None
    res_cnf = get_pendant_conf(skin_id, other_id)
    head_pendant_l_same_gis = False
    bag_pendant_l_same_gis = False
    pendant_l_same_gis = False
    pendant_l_anim = None
    if res_cnf is not None:
        head_pendant_type = res_cnf.get('head_pendant_type')
        head_res_path = res_cnf.get('head_res_path')
        pendant_socket_name = res_cnf.get('pendant_socket_name')
        pendant_socket_res_path = res_cnf.get('pendant_socket_res_path')
        head_pendant_l_same_gis = res_cnf.get('head_pendant_l_same_gis')
        pendant_type = res_cnf.get('pendant_type')
        if pendant_socket_res_path:
            res_path = pendant_socket_res_path
            socket_name = pendant_socket_name
        bag_socket_name = res_cnf.get('bag_socket_name')
        bag_model_path = res_cnf.get('bag_res_path')
        bag_pendant_l_same_gis = res_cnf.get('bag_pendant_l_same_gis')
        pendant_l_same_gis = res_cnf.get('pendant_l_same_gis')
        pendant_l_anim = res_cnf.get('pendant_l_anim')
        if bag_model_path:
            res_path = bag_model_path
            socket_name = bag_socket_name
        table_socket_name = res_cnf.get('socket_name')
        table_res_path = res_cnf.get('res_path')
        if table_res_path:
            res_path = table_res_path
            socket_name = table_socket_name
        anim_data = {}
        anim_data['use_skin_show_anim'] = res_cnf.get('use_skin_show_anim')
        anim_data['use_skin_end_anim'] = res_cnf.get('use_skin_end_anim')
        anim_data['show_anim'] = res_cnf.get('show_anim')
        anim_data['end_anim'] = res_cnf.get('end_anim')
    data_dict = {'head_pendant_type': head_pendant_type,
       'head_res_path': head_res_path,
       'head_pendant_l_same_gis': head_pendant_l_same_gis or pendant_l_same_gis or bag_pendant_l_same_gis,
       'pendant_type': pendant_type,
       'res_path': res_path,
       'socket_name': socket_name,
       'anim_data': anim_data,
       'pendant_l_anim': pendant_l_anim
       }
    return data_dict


def get_pendant_other_list_path(other_id_list, skin_id):
    pendant_data_list = [ get_pendant_other_path(other_id, skin_id) for other_id in other_id_list if other_id ]
    pendant_data_list = [ x for x in pendant_data_list if bool(x.get('res_path')) ]
    head_pendant_type, head_res_path = (None, None)
    for pendant_data in pendant_data_list:
        temp_head_pendant_type = pendant_data['head_pendant_type']
        temp_head_res_path = pendant_data['head_res_path']
        if temp_head_res_path:
            if head_res_path and head_res_path != temp_head_res_path:
                log_error('Mutliple pendant have head specification!', other_id_list, skin_id)
            head_pendant_type = temp_head_pendant_type
            head_res_path = temp_head_res_path

    if head_res_path:
        global_data.game_mgr.show_tip('\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81\xe6\x8c\x82\xe9\xa5\xb0\xe6\x8d\xa2\xe5\xa4\xb4\xef\xbc\x81')
    return (head_pendant_type, head_res_path, pendant_data_list)


def get_pendant_other_list_anim(other_id_list, skin_id):
    pendant_data_list = [ get_pendant_other_path(other_id, skin_id) for other_id in other_id_list ]
    pendant_data_list = [ x for x in pendant_data_list if bool(x.get('res_path')) ]
    anim_data = {}
    anim_data['use_skin_show_anim'] = None
    anim_data['use_skin_end_anim'] = None
    anim_data['show_anim'] = None
    anim_data['end_anim'] = None
    for pendant_data in pendant_data_list:
        temp_anim_data = pendant_data['anim_data']
        if temp_anim_data:
            use_skin_show_anim = temp_anim_data.get('use_skin_show_anim')
            use_skin_end_anim = temp_anim_data.get('use_skin_end_anim')
            show_anim = temp_anim_data.get('show_anim')
            end_anim = temp_anim_data.get('end_anim')
            anim_data['use_skin_show_anim'] = anim_data['use_skin_show_anim'] or use_skin_show_anim
            anim_data['use_skin_end_anim'] = anim_data['use_skin_end_anim'] or use_skin_end_anim
            if show_anim:
                if anim_data['show_anim'] and anim_data['show_anim'] != show_anim:
                    log_error('Mutliple pendant have different show_anim')
                anim_data['show_anim'] = anim_data['show_anim'] or show_anim
            if end_anim:
                anim_data['end_anim'] = anim_data['end_anim'] or end_anim

    if not anim_data['show_anim'] and not anim_data['use_skin_show_anim']:
        for other_id in other_id_list:
            item_data = confmgr.get('lobby_item', str(other_id), default={})
            item_show_ani = item_data.get('first_ani_name')
            if item_show_ani and not anim_data['show_anim']:
                anim_data['show_anim'] = item_show_ani
            elif item_show_ani and anim_data['show_anim'] and item_show_ani != anim_data['show_anim']:
                log_error('There are multiple show anims!!!', other_id_list)

    if not anim_data['end_anim'] and not anim_data['use_skin_end_anim']:
        for other_id in other_id_list:
            item_data = confmgr.get('lobby_item', str(other_id), default={})
            item_show_ani = item_data.get('end_ani_name')
            if item_show_ani and not anim_data['end_anim']:
                anim_data['end_anim'] = item_show_ani
            elif item_show_ani and anim_data['end_anim'] and item_show_ani != anim_data['end_anim']:
                log_error('There are multiple end anims!!!', other_id_list)

    return anim_data


def get_pendant_res_lod_conf--- This code section failed: ---

1423       0  LOAD_CONST           23  (None, None, None, None, None, None)
           3  UNPACK_SEQUENCE_6     6 
           6  STORE_FAST            7  'head_pendant_type'
           9  STORE_FAST            8  'head_res_path'
          12  STORE_FAST            9  'pendant_socket_name'
          15  STORE_FAST           10  'pendant_socket_res_path'
          18  STORE_FAST           11  'head_pendant_l_same_gis'
          21  STORE_FAST           12  'pendant_random_anim_list'

1424      24  LOAD_CONST           24  (None, None, None, None, None)
          27  UNPACK_SEQUENCE_5     5 
          30  STORE_FAST           13  'bag_socket_name'
          33  STORE_FAST           14  'bag_model_path'
          36  STORE_FAST           15  'bag_socket_name2'
          39  STORE_FAST           16  'bag_model_path2'
          42  STORE_FAST           17  'bag_pendant_l_same_gis'

1425      45  LOAD_CONST           25  (None, None)
          48  UNPACK_SEQUENCE_2     2 
          51  STORE_FAST           18  'res_cnf'
          54  STORE_FAST           19  'bag_cnf'

1426      57  LOAD_CONST            0  ''
          60  STORE_FAST           20  'pendant_data_list'

1427      63  LOAD_FAST             2  'skin_id'
          66  LOAD_CONST            0  ''
          69  COMPARE_OP            9  'is-not'
          72  POP_JUMP_IF_FALSE   536  'to 536'

1428      75  LOAD_FAST             5  'suit_id'
          78  LOAD_CONST            0  ''
          81  COMPARE_OP            9  'is-not'
          84  POP_JUMP_IF_FALSE   105  'to 105'

1429      87  LOAD_GLOBAL           1  'get_pendant_conf'
          90  LOAD_FAST             2  'skin_id'
          93  LOAD_FAST             5  'suit_id'
          96  CALL_FUNCTION_2       2 
          99  STORE_FAST           18  'res_cnf'
         102  JUMP_FORWARD         60  'to 165'

1431     105  LOAD_FAST             3  'head_id'
         108  LOAD_CONST            0  ''
         111  COMPARE_OP            9  'is-not'
         114  POP_JUMP_IF_FALSE   135  'to 135'

1432     117  LOAD_GLOBAL           1  'get_pendant_conf'
         120  LOAD_FAST             2  'skin_id'
         123  LOAD_FAST             3  'head_id'
         126  CALL_FUNCTION_2       2 
         129  STORE_FAST           18  'res_cnf'
         132  JUMP_FORWARD          0  'to 135'
       135_0  COME_FROM                '132'

1433     135  LOAD_FAST             4  'bag_id'
         138  LOAD_CONST            0  ''
         141  COMPARE_OP            9  'is-not'
         144  POP_JUMP_IF_FALSE   165  'to 165'

1434     147  LOAD_GLOBAL           1  'get_pendant_conf'
         150  LOAD_FAST             2  'skin_id'
         153  LOAD_FAST             4  'bag_id'
         156  CALL_FUNCTION_2       2 
         159  STORE_FAST           19  'bag_cnf'
         162  JUMP_FORWARD          0  'to 165'
       165_0  COME_FROM                '162'
       165_1  COME_FROM                '102'

1436     165  LOAD_FAST            18  'res_cnf'
         168  LOAD_CONST            0  ''
         171  COMPARE_OP            9  'is-not'
         174  POP_JUMP_IF_FALSE   358  'to 358'
         177  POP_JUMP_IF_FALSE     1  'to 1'
         180  COMPARE_OP            2  '=='
         183  POP_JUMP_IF_TRUE    205  'to 205'
         186  LOAD_FAST            18  'res_cnf'
         189  LOAD_ATTR             2  'get'
         192  LOAD_CONST            2  'only_use_in_h'
         195  LOAD_GLOBAL           3  'False'
         198  CALL_FUNCTION_2       2 
         201  UNARY_NOT        
       202_0  COME_FROM                '183'
       202_1  COME_FROM                '174'
         202  POP_JUMP_IF_FALSE   358  'to 358'

1437     205  LOAD_FAST            18  'res_cnf'
         208  LOAD_ATTR             2  'get'
         211  LOAD_CONST            3  'head_pendant_type'
         214  CALL_FUNCTION_1       1 
         217  STORE_FAST            7  'head_pendant_type'

1438     220  LOAD_FAST            18  'res_cnf'
         223  LOAD_ATTR             2  'get'
         226  LOAD_CONST            4  'head_res_path'
         229  CALL_FUNCTION_1       1 
         232  STORE_FAST            8  'head_res_path'

1439     235  LOAD_FAST            18  'res_cnf'
         238  LOAD_ATTR             2  'get'
         241  LOAD_CONST            5  'pendant_socket_name'
         244  CALL_FUNCTION_1       1 
         247  STORE_FAST            9  'pendant_socket_name'

1440     250  LOAD_FAST            18  'res_cnf'
         253  LOAD_ATTR             2  'get'
         256  LOAD_CONST            6  'pendant_socket_res_path'
         259  CALL_FUNCTION_1       1 
         262  STORE_FAST           10  'pendant_socket_res_path'

1441     265  LOAD_FAST            18  'res_cnf'
         268  LOAD_ATTR             2  'get'
         271  LOAD_CONST            7  'head_pendant_l_same_gis'
         274  CALL_FUNCTION_1       1 
         277  STORE_FAST           11  'head_pendant_l_same_gis'

1442     280  LOAD_FAST            18  'res_cnf'
         283  LOAD_ATTR             2  'get'
         286  LOAD_CONST            8  'pendant_random_anim_list'
         289  CALL_FUNCTION_1       1 
         292  STORE_FAST           12  'pendant_random_anim_list'

1443     295  LOAD_FAST            18  'res_cnf'
         298  LOAD_ATTR             2  'get'
         301  LOAD_CONST            9  'bag_socket_name'
         304  CALL_FUNCTION_1       1 
         307  STORE_FAST           13  'bag_socket_name'

1444     310  LOAD_FAST            18  'res_cnf'
         313  LOAD_ATTR             2  'get'
         316  LOAD_CONST           10  'bag_res_path'
         319  CALL_FUNCTION_1       1 
         322  STORE_FAST           14  'bag_model_path'

1445     325  LOAD_FAST            18  'res_cnf'
         328  LOAD_ATTR             2  'get'
         331  LOAD_CONST           11  'bag_socket_name2'
         334  CALL_FUNCTION_1       1 
         337  STORE_FAST           15  'bag_socket_name2'

1446     340  LOAD_FAST            18  'res_cnf'
         343  LOAD_ATTR             2  'get'
         346  LOAD_CONST           12  'bag_res_path2'
         349  CALL_FUNCTION_1       1 
         352  STORE_FAST           16  'bag_model_path2'
         355  JUMP_FORWARD          0  'to 358'
       358_0  COME_FROM                '355'

1448     358  LOAD_FAST            19  'bag_cnf'
         361  LOAD_CONST            0  ''
         364  COMPARE_OP            9  'is-not'
         367  POP_JUMP_IF_FALSE   448  'to 448'

1449     370  LOAD_FAST            19  'bag_cnf'
         373  LOAD_ATTR             2  'get'
         376  LOAD_CONST            9  'bag_socket_name'
         379  CALL_FUNCTION_1       1 
         382  STORE_FAST           13  'bag_socket_name'

1450     385  LOAD_FAST            19  'bag_cnf'
         388  LOAD_ATTR             2  'get'
         391  LOAD_CONST           10  'bag_res_path'
         394  CALL_FUNCTION_1       1 
         397  STORE_FAST           14  'bag_model_path'

1451     400  LOAD_FAST            19  'bag_cnf'
         403  LOAD_ATTR             2  'get'
         406  LOAD_CONST           11  'bag_socket_name2'
         409  CALL_FUNCTION_1       1 
         412  STORE_FAST           15  'bag_socket_name2'

1452     415  LOAD_FAST            19  'bag_cnf'
         418  LOAD_ATTR             2  'get'
         421  LOAD_CONST           12  'bag_res_path2'
         424  CALL_FUNCTION_1       1 
         427  STORE_FAST           16  'bag_model_path2'

1453     430  LOAD_FAST            19  'bag_cnf'
         433  LOAD_ATTR             2  'get'
         436  LOAD_CONST           13  'bag_pendant_l_same_gis'
         439  CALL_FUNCTION_1       1 
         442  STORE_FAST           17  'bag_pendant_l_same_gis'
         445  JUMP_FORWARD          0  'to 448'
       448_0  COME_FROM                '445'

1455     448  LOAD_FAST             6  'other_pendants'
         451  POP_JUMP_IF_FALSE   536  'to 536'

1456     454  LOAD_GLOBAL           4  'get_pendant_other_list_path'
         457  LOAD_FAST             6  'other_pendants'
         460  LOAD_FAST             2  'skin_id'
         463  CALL_FUNCTION_2       2 
         466  UNPACK_SEQUENCE_3     3 
         469  STORE_FAST           21  'ops_head_pendant_type'
         472  STORE_FAST           22  'ops_head_res_path'
         475  STORE_FAST           20  'pendant_data_list'

1457     478  LOAD_FAST             8  'head_res_path'
         481  POP_JUMP_IF_FALSE   533  'to 533'
         484  LOAD_FAST            22  'ops_head_res_path'
         487  POP_JUMP_IF_FALSE   533  'to 533'
         490  LOAD_FAST             8  'head_res_path'
         493  LOAD_FAST            22  'ops_head_res_path'
         496  COMPARE_OP            3  '!='
       499_0  COME_FROM                '487'
       499_1  COME_FROM                '481'
         499  POP_JUMP_IF_FALSE   533  'to 533'

1458     502  LOAD_GLOBAL           5  'log_error'
         505  LOAD_CONST           14  'There are two pendants need to change head!'
         508  LOAD_FAST             2  'skin_id'
         511  LOAD_FAST             3  'head_id'
         514  LOAD_FAST             4  'bag_id'
         517  LOAD_FAST             5  'suit_id'
         520  LOAD_FAST             6  'other_pendants'
         523  CALL_FUNCTION_6       6 
         526  POP_TOP          
         527  JUMP_ABSOLUTE       533  'to 533'
         530  JUMP_ABSOLUTE       536  'to 536'
         533  JUMP_FORWARD          0  'to 536'
       536_0  COME_FROM                '533'

1461     536  LOAD_FAST             8  'head_res_path'
         539  LOAD_CONST            0  ''
         542  COMPARE_OP            2  '=='
         545  POP_JUMP_IF_FALSE   582  'to 582'

1462     548  LOAD_FAST             1  'empty_res_path'
         551  POP_JUMP_IF_FALSE   604  'to 604'

1463     554  LOAD_FAST             1  'empty_res_path'
         557  LOAD_ATTR             6  'replace'
         560  LOAD_CONST           15  'empty.gim'
         563  LOAD_CONST           16  'parts/%s_head.gim'
         566  LOAD_FAST             0  'lod_level'
         569  BINARY_MODULO    
         570  CALL_FUNCTION_2       2 
         573  STORE_FAST            8  'head_res_path'
         576  JUMP_ABSOLUTE       604  'to 604'
         579  JUMP_FORWARD         22  'to 604'

1465     582  LOAD_FAST             8  'head_res_path'
         585  LOAD_ATTR             6  'replace'
         588  LOAD_CONST           17  'h.gim'
         591  LOAD_CONST           18  '%s.gim'
         594  LOAD_FAST             0  'lod_level'
         597  BINARY_MODULO    
         598  CALL_FUNCTION_2       2 
         601  STORE_FAST            8  'head_res_path'
       604_0  COME_FROM                '579'

1467     604  LOAD_FAST            10  'pendant_socket_res_path'
         607  POP_JUMP_IF_FALSE   675  'to 675'

1468     610  LOAD_FAST            10  'pendant_socket_res_path'
         613  LOAD_ATTR             7  'endswith'
         616  LOAD_CONST           17  'h.gim'
         619  CALL_FUNCTION_1       1 
         622  POP_JUMP_IF_FALSE   650  'to 650'

1469     625  LOAD_FAST            10  'pendant_socket_res_path'
         628  LOAD_ATTR             6  'replace'
         631  LOAD_CONST           17  'h.gim'
         634  LOAD_CONST           18  '%s.gim'
         637  LOAD_FAST             0  'lod_level'
         640  BINARY_MODULO    
         641  CALL_FUNCTION_2       2 
         644  STORE_FAST           10  'pendant_socket_res_path'
         647  JUMP_ABSOLUTE       675  'to 675'

1471     650  LOAD_FAST            10  'pendant_socket_res_path'
         653  LOAD_ATTR             6  'replace'
         656  LOAD_CONST           19  'h_'
         659  LOAD_CONST           20  '%s_'
         662  LOAD_FAST             0  'lod_level'
         665  BINARY_MODULO    
         666  CALL_FUNCTION_2       2 
         669  STORE_FAST           10  'pendant_socket_res_path'
         672  JUMP_FORWARD          0  'to 675'
       675_0  COME_FROM                '672'

1473     675  LOAD_FAST            14  'bag_model_path'
         678  POP_JUMP_IF_FALSE   746  'to 746'

1474     681  LOAD_FAST            14  'bag_model_path'
         684  LOAD_ATTR             7  'endswith'
         687  LOAD_CONST           17  'h.gim'
         690  CALL_FUNCTION_1       1 
         693  POP_JUMP_IF_FALSE   721  'to 721'

1475     696  LOAD_FAST            14  'bag_model_path'
         699  LOAD_ATTR             6  'replace'
         702  LOAD_CONST           17  'h.gim'
         705  LOAD_CONST           18  '%s.gim'
         708  LOAD_FAST             0  'lod_level'
         711  BINARY_MODULO    
         712  CALL_FUNCTION_2       2 
         715  STORE_FAST           14  'bag_model_path'
         718  JUMP_ABSOLUTE       746  'to 746'

1477     721  LOAD_FAST            14  'bag_model_path'
         724  LOAD_ATTR             6  'replace'
         727  LOAD_CONST           19  'h_'
         730  LOAD_CONST           20  '%s_'
         733  LOAD_FAST             0  'lod_level'
         736  BINARY_MODULO    
         737  CALL_FUNCTION_2       2 
         740  STORE_FAST           14  'bag_model_path'
         743  JUMP_FORWARD          0  'to 746'
       746_0  COME_FROM                '743'

1479     746  LOAD_FAST            16  'bag_model_path2'
         749  POP_JUMP_IF_FALSE   817  'to 817'

1480     752  LOAD_FAST            16  'bag_model_path2'
         755  LOAD_ATTR             7  'endswith'
         758  LOAD_CONST           17  'h.gim'
         761  CALL_FUNCTION_1       1 
         764  POP_JUMP_IF_FALSE   792  'to 792'

1481     767  LOAD_FAST            16  'bag_model_path2'
         770  LOAD_ATTR             6  'replace'
         773  LOAD_CONST           17  'h.gim'
         776  LOAD_CONST           18  '%s.gim'
         779  LOAD_FAST             0  'lod_level'
         782  BINARY_MODULO    
         783  CALL_FUNCTION_2       2 
         786  STORE_FAST           16  'bag_model_path2'
         789  JUMP_ABSOLUTE       817  'to 817'

1483     792  LOAD_FAST            16  'bag_model_path2'
         795  LOAD_ATTR             6  'replace'
         798  LOAD_CONST           19  'h_'
         801  LOAD_CONST           20  '%s_'
         804  LOAD_FAST             0  'lod_level'
         807  BINARY_MODULO    
         808  CALL_FUNCTION_2       2 
         811  STORE_FAST           16  'bag_model_path2'
         814  JUMP_FORWARD          0  'to 817'
       817_0  COME_FROM                '814'

1485     817  LOAD_FAST            20  'pendant_data_list'
         820  POP_JUMP_IF_FALSE   957  'to 957'

1486     823  SETUP_LOOP          131  'to 957'
         826  LOAD_FAST            20  'pendant_data_list'
         829  GET_ITER         
         830  FOR_ITER            120  'to 953'
         833  STORE_FAST           23  'pendant_data'

1487     836  LOAD_FAST            23  'pendant_data'
         839  LOAD_CONST           21  'res_path'
         842  BINARY_SUBSCR    
         843  POP_JUMP_IF_TRUE    868  'to 868'

1488     846  LOAD_GLOBAL           5  'log_error'
         849  LOAD_CONST           22  'There are error in pendant_data'
         852  LOAD_FAST             6  'other_pendants'
         855  LOAD_FAST             2  'skin_id'
         858  CALL_FUNCTION_3       3 
         861  POP_TOP          

1489     862  CONTINUE            830  'to 830'
         865  JUMP_FORWARD          0  'to 868'
       868_0  COME_FROM                '865'

1490     868  LOAD_FAST            23  'pendant_data'
         871  LOAD_CONST           21  'res_path'
         874  BINARY_SUBSCR    
         875  LOAD_ATTR             7  'endswith'
         878  LOAD_CONST           17  'h.gim'
         881  CALL_FUNCTION_1       1 
         884  POP_JUMP_IF_FALSE   920  'to 920'

1491     887  LOAD_FAST            23  'pendant_data'
         890  LOAD_CONST           21  'res_path'
         893  BINARY_SUBSCR    
         894  LOAD_ATTR             6  'replace'
         897  LOAD_CONST           17  'h.gim'
         900  LOAD_CONST           18  '%s.gim'
         903  LOAD_FAST             0  'lod_level'
         906  BINARY_MODULO    
         907  CALL_FUNCTION_2       2 
         910  LOAD_FAST            23  'pendant_data'
         913  LOAD_CONST           21  'res_path'
         916  STORE_SUBSCR     
         917  JUMP_BACK           830  'to 830'

1493     920  LOAD_FAST            23  'pendant_data'
         923  LOAD_CONST           21  'res_path'
         926  BINARY_SUBSCR    
         927  LOAD_ATTR             6  'replace'
         930  LOAD_CONST           19  'h_'
         933  LOAD_CONST           20  '%s_'
         936  LOAD_FAST             0  'lod_level'
         939  BINARY_MODULO    
         940  CALL_FUNCTION_2       2 
         943  LOAD_FAST            23  'pendant_data'
         946  LOAD_CONST           21  'res_path'
         949  STORE_SUBSCR     
         950  JUMP_BACK           830  'to 830'
         953  POP_BLOCK        
       954_0  COME_FROM                '823'
         954  JUMP_FORWARD          0  'to 957'
       957_0  COME_FROM                '823'

1496     957  LOAD_FAST             7  'head_pendant_type'
         960  LOAD_FAST             8  'head_res_path'
         963  LOAD_FAST             9  'pendant_socket_name'
         966  LOAD_FAST            10  'pendant_socket_res_path'
         969  LOAD_FAST            11  'head_pendant_l_same_gis'
         972  LOAD_FAST            12  'pendant_random_anim_list'
         975  LOAD_FAST            13  'bag_socket_name'
         978  LOAD_FAST            14  'bag_model_path'
         981  LOAD_FAST            15  'bag_socket_name2'
         984  LOAD_FAST            16  'bag_model_path2'
         987  LOAD_FAST            17  'bag_pendant_l_same_gis'
         990  LOAD_FAST            20  'pendant_data_list'
         993  BUILD_TUPLE_12       12 
         996  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 177


def get_pendant_anim(skin_id=None, bag_id=None, suit_id=None, other_pendants=()):
    use_skin_show_anim, show_anim, use_skin_end_anim, end_anim = (None, None, None,
                                                                  None)
    if skin_id is not None:
        ops_anim_data = get_pendant_other_list_anim(other_pendants, skin_id)
        if ops_anim_data:
            use_skin_show_anim = ops_anim_data.get('use_skin_show_anim')
            use_skin_end_anim = ops_anim_data.get('use_skin_end_anim')
            show_anim = ops_anim_data.get('show_anim')
            end_anim = ops_anim_data.get('end_anim')
        res_cnf = None
        if suit_id is not None:
            res_cnf = get_pendant_conf(skin_id, suit_id)
        elif bag_id is not None:
            res_cnf = get_pendant_conf(skin_id, bag_id)
        if res_cnf is not None:
            use_skin_show_anim = res_cnf.get('use_skin_show_anim')
            use_skin_end_anim = res_cnf.get('use_skin_end_anim')
            show_anim = res_cnf.get('show_anim')
            end_anim = res_cnf.get('end_anim')
    return (use_skin_show_anim, show_anim, use_skin_end_anim, end_anim)


def get_lobby_model_scale(role_id, dressed_clothing_id):
    scale = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'lobby_model_scale', default=None)
    if not scale:
        scale = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'lobby_model_scale')
    return scale or 1


def create_lobby_model(role_id, dressed_clothing_id, head_id=None, bag_id=None, suit_id=None):
    res_path = get_role_model_path_by_lod(role_id, dressed_clothing_id, lod_level='l')
    role_model = world.model(res_path, None)
    head_res_path = res_path.replace('l.gim', 'parts/l_head.gim')
    head_model = world.model(head_res_path, None)
    role_model.add_mesh(head_res_path)
    scale = get_lobby_model_scale(role_id, dressed_clothing_id)
    scale = scale or 1
    role_model.scale = math3d.vector(scale, scale, scale)
    return role_model


DRIVER_CONFIG = {animation_const.ROLE_ID_MI_LA: '_driver'
   }

def create_lobby_driver_model--- This code section failed: ---

1546       0  LOAD_GLOBAL           0  'get_role_model_path_by_lod'
           3  LOAD_FAST             0  'role_id'
           6  LOAD_FAST             1  'dressed_clothing_id'
           9  LOAD_CONST            1  'lod_level'
          12  LOAD_CONST            2  'l'
          15  CALL_FUNCTION_258   258 
          18  STORE_FAST            5  'res_path'

1547      21  LOAD_GLOBAL           1  'DRIVER_CONFIG'
          24  LOAD_ATTR             2  'get'
          27  LOAD_ATTR             3  'replace'
          30  CALL_FUNCTION_2       2 
          33  STORE_FAST            6  'post_fix'

1548      36  LOAD_FAST             5  'res_path'
          39  LOAD_ATTR             3  'replace'
          42  LOAD_CONST            4  'l.gim'
          45  LOAD_CONST            2  'l'
          48  LOAD_FAST             6  'post_fix'
          51  BINARY_ADD       
          52  LOAD_CONST            5  '.gim'
          55  BINARY_ADD       
          56  CALL_FUNCTION_2       2 
          59  STORE_FAST            7  'driver_res_path'

1549      62  LOAD_GLOBAL           4  'world'
          65  LOAD_ATTR             5  'model'
          68  LOAD_FAST             7  'driver_res_path'
          71  LOAD_CONST            0  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            8  'role_model'

1550      80  LOAD_FAST             5  'res_path'
          83  LOAD_ATTR             3  'replace'
          86  LOAD_CONST            4  'l.gim'
          89  LOAD_CONST            6  'parts/l_head'
          92  LOAD_FAST             6  'post_fix'
          95  BINARY_ADD       
          96  LOAD_CONST            5  '.gim'
          99  BINARY_ADD       
         100  CALL_FUNCTION_2       2 
         103  STORE_FAST            9  'head_res_path'

1551     106  LOAD_GLOBAL           4  'world'
         109  LOAD_ATTR             5  'model'
         112  LOAD_FAST             9  'head_res_path'
         115  LOAD_CONST            0  ''
         118  CALL_FUNCTION_2       2 
         121  STORE_FAST           10  'head_model'

1552     124  LOAD_FAST             8  'role_model'
         127  LOAD_ATTR             7  'add_mesh'
         130  LOAD_FAST             9  'head_res_path'
         133  CALL_FUNCTION_1       1 
         136  POP_TOP          

1556     137  LOAD_FAST             8  'role_model'
         140  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 30


def role_skin_should_show_custom(role_id, skin_id):
    role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'goods_id')
    top_skin_id = get_top_skin_id_by_skin_id(skin_id)
    skin_list = get_role_top_skin_owned_second_skin_list(top_skin_id)
    has_content = len(skin_list) > 1 or get_valid_deco_list_for_skin_id(role_id, skin_id)
    return bool(role_goods_id) and has_content


def is_role_usable(role_id):
    role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'goods_id')
    return role_goods_id is not None


def get_fashion_unowned_money_type(all_item_no):
    from logic.gutils import mall_utils
    price_list = []
    for item_no in all_item_no:
        item_data = global_data.player.get_item_by_no(item_no)
        has_item = item_data is not None
        if not has_item:
            goods_id = get_goods_id_of_role_dress_related_item_no(item_no)
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                price_list.append(price)

    payment_list = []
    for prices in price_list:
        for p in prices:
            goods_payment = p.get('goods_payment')
            if goods_payment is not None:
                payment_list.append(goods_payment)

    new_money_types_list = []
    for p in payment_list:
        if p not in new_money_types_list:
            new_money_types_list.append(p)

    return new_money_types_list


def get_item_no_list_buy_info(item_no_list):
    own_list = []
    no_own_list = []
    can_buy_list = []
    no_can_buy_list = []
    from logic.gutils import mall_utils
    for item_no in item_no_list:
        if not item_no:
            continue
        own = global_data.player.has_item_by_no(item_no) if global_data.player else False
        if own:
            own_list.append(item_no)
        else:
            no_own_list.append(item_no)

    for item_no in no_own_list:
        goods_id = get_goods_id_of_role_dress_related_item_no(item_no)
        price = mall_utils.get_mall_item_price(goods_id)
        if price:
            can_buy_list.append(item_no)
        else:
            no_can_buy_list.append(item_no)

    return (own_list, no_own_list, can_buy_list, no_can_buy_list)


def play_anim_screen_sfx(sfx_list):
    ret_list = []
    for sfx in sfx_list:
        ret_list.append(create_screen_effect_directly(sfx))

    return ret_list


def play_chuchang_sfx(sfx_list, pos):

    def call_back(sfx, *args):
        pass

    ret_list = []
    for sfx in sfx_list:
        ret_list.append(global_data.sfx_mgr.create_sfx_in_scene(sfx, pos=pos, on_create_func=call_back))

    return ret_list


def check_force_default_head_dec(skin_id):
    conf = confmgr.get('pendant', 'SolidDec').get(str(skin_id), {})
    dec_id = conf.get('default_solid_dec', None)
    if dec_id:
        dec_conf = confmgr.get('pendant', 'ItemData').get(str(dec_id), {})
        dec_type = dec_conf.get(str(skin_id), {}).get('pendant_type', None)
        if not dec_type:
            dec_type = dec_conf.get('1').get('pendant_type', None)
        if dec_type == 'Head':
            return dec_id
    return


def check_force_default_bag_dec(skin_id):
    conf = confmgr.get('pendant', 'SolidDec').get(str(skin_id), {})
    dec_id = conf.get('default_solid_dec', None)
    if dec_id:
        dec_conf = confmgr.get('pendant', 'ItemData').get(str(dec_id), {})
        dec_type = dec_conf.get(str(skin_id), {}).get('pendant_type', None)
        if not dec_type:
            dec_type = dec_conf.get('1').get('pendant_type', None)
        if dec_type in ('Bag', 'Waist'):
            return dec_id
    return


def handle_unusable_dec(dec_list, skin_id):
    usable_list = []
    unusable_list = []
    for dec_id in dec_list:
        conf = confmgr.get('pendant', 'SkinRestrict').get(str(dec_id), {})
        cur_usable_list = conf.get('usable_skin_list', [])
        cur_unusable_list = conf.get('unusable_skin_list', [])
        if cur_usable_list:
            if skin_id in cur_usable_list:
                usable_list.append(dec_id)
        if cur_unusable_list:
            if skin_id in cur_unusable_list:
                unusable_list.append(dec_id)

    return list(set(dec_list) - set(unusable_list) & set(usable_list))


def handle_usable_skin_list(dec_id):
    from logic.gutils.item_utils import get_lobby_item_belong_no
    from logic.gutils.role_skin_utils import filter_publish_role_skins
    conf = confmgr.get('pendant', 'SkinRestrict').get(str(dec_id), {})
    cur_usable_list = conf.get('usable_skin_list', [])
    cur_unusable_list = conf.get('unusable_skin_list', [])
    usable_set = set(cur_usable_list) - set(cur_unusable_list)
    belong_id = get_lobby_item_belong_no(dec_id)
    return filter_publish_role_skins(belong_id, usable_set)


SP_PHOTO_SKIP = (201001942, 201001943, 201001251)

def check_quick_msg_photo_skip(skin_id):
    return skin_id in SP_PHOTO_SKIP


def show_change_fashion_tips(fashion_data, cur_clothing_id):
    from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, RARE_DEGREE_5, RARE_DEGREE_4, RARE_DEGREE_7
    from logic.gutils import item_utils
    dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
    text = None
    if cur_clothing_id == dressed_clothing_id and FASHION_POS_WEAPON_SFX in fashion_data:
        rare_degree = item_utils.get_item_rare_degree(dressed_clothing_id, ignore_imporve=True)
        if rare_degree in {RARE_DEGREE_5, RARE_DEGREE_7}:
            from logic.gutils.mecha_skin_utils import get_mecha_shiny_weapon_info
            if len(get_mecha_shiny_weapon_info(cur_clothing_id)) > 1:
                text = get_text_by_id(635625)
            else:
                text = get_text_by_id(611402)
        elif rare_degree == RARE_DEGREE_4:
            text = get_text_by_id(611406)
    if not text:
        name_text = item_utils.get_lobby_item_name(dressed_clothing_id)
        text = get_text_by_id(14002, {'name': name_text})
    global_data.game_mgr.show_tip(text)
    return


def is_assemble_style(res_path):
    if not global_data.enable_assemble_model_style:
        return False
    if not global_data.feature_mgr.is_support_anim_assemble():
        return False
    for path_item in ANIM_ASSEMBLE_PATHS:
        if path_item in res_path:
            return True

    return False