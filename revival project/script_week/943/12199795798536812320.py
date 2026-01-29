# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/map_utils.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.common_utils.local_text import get_text_by_id
import world
import math3d
import cc
MAP_PARAMETERS = {}

def get_map_uv(pos):
    default_pos = (-1.0, -1.0)
    if not pos:
        return default_pos
    scn = world.get_active_scene()
    res = scn.get_scene_map_uv_with_checking_script_logic(pos.x, pos.z)
    return res or default_pos


def get_map_uv_ex(tuple_pos):
    scn = world.get_active_scene()
    default_pos = (-1.0, -1.0)
    if not tuple_pos:
        return default_pos
    x, y, z = tuple_pos
    res = scn.get_scene_map_uv_with_checking_script_logic(x, z)
    return res or default_pos


def get_map_dist():
    l_idx, r_idx, btm_idx, up_idx, trunk_size = world.get_active_scene().get_safe_scene_map_uv_parameters()
    return (r_idx - l_idx + 1) * trunk_size


def get_map_dist_vertical():
    l_idx, r_idx, btm_idx, up_idx, trunk_size = world.get_active_scene().get_safe_scene_map_uv_parameters()
    return (up_idx - btm_idx + 1) * trunk_size


def get_world_pos_from_map(map_pos, content_size):
    l_idx, r_idx, btm_idx, up_idx, trunk_size = world.get_active_scene().get_safe_scene_map_uv_parameters()
    pos_left = trunk_size * (l_idx - 0.5)
    pos_btm = trunk_size * (btm_idx - 0.5)
    height_map_dist = (up_idx - btm_idx + 1) * trunk_size
    width_map_dist = (r_idx - l_idx + 1) * trunk_size
    u, v = float(map_pos.x) / content_size[0], float(map_pos.y) / content_size[1]
    return math3d.vector(u * width_map_dist + pos_left, 0, v * height_map_dist + pos_btm)


def get_map_pos_from_world(world_pos):
    part_map = global_data.game_mgr.scene.get_com('PartMap')
    if part_map:
        return part_map.get_world_pos_in_map(world_pos)
    else:
        return None


def get_map_config():
    if not global_data.battle:
        return {}
    from common.cfg import confmgr
    map_id = str(global_data.battle.map_id)
    map_data_conf = confmgr.get('map_config', str(map_id), default={})
    map_conf = {}
    map_keys = ['cMapFolder', 'arrMapResolution', 'arrMapScaleRange']
    for key in map_keys:
        map_conf[key] = map_data_conf[key]

    optional_keys = [
     'cMapUVParas', 'cMapCutEdge']
    for key in optional_keys:
        if key in map_data_conf:
            map_conf[key] = map_data_conf[key]

    cMapCutEdge = map_conf.get('cMapCutEdge')
    if cMapCutEdge:
        map_conf['mapShowSize'] = [
         map_conf['arrMapResolution'][0] - (cMapCutEdge[0] + cMapCutEdge[1]),
         map_conf['arrMapResolution'][1] - (cMapCutEdge[2] + cMapCutEdge[3])]
    else:
        map_conf['mapShowSize'] = map_conf['arrMapResolution']
    return map_conf


def add_scene_map_mark(unit_id, mark_type, v3d_map_pos, extra_args):
    from logic.gutils import judge_utils
    if judge_utils.is_ob():
        return
    else:
        if not (global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(unit_id)):
            return
        from logic.comsys.map.FightLocateUI import FightLocateUI
        ui = global_data.ui_mgr.get_ui('FightLocateUI')
        if ui or global_data.cam_lplayer:
            player = global_data.cam_lplayer if 1 else None
            FightLocateUI(None, player)
        global_data.emgr.add_scene_mark.emit(unit_id, mark_type, v3d_map_pos, extra_args)
        return


def send_mark_group_msg(mark_type, extra_args=None):
    from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_GATHER
    from common.cfg import confmgr
    if not global_data.cam_lplayer:
        return
    else:
        battle = global_data.battle
        if battle and battle.is_single_person_battle() and mark_type == MARK_GOTO:
            return
        role_id = str(global_data.player.get_role())
        mark_chat_conf = confmgr.get('quick_mark_chat')
        default_cfg = mark_chat_conf.get('0')
        role_cfg = mark_chat_conf.get(role_id, default=default_cfg)
        mark_type_str = str(mark_type)
        if mark_type_str not in role_cfg and mark_type_str not in default_cfg:
            return
        mark_type_cfg = role_cfg.get(mark_type_str) or default_cfg.get(mark_type_str)
        txt_id = mark_type_cfg['text_id']
        msg = {'text': txt_id}
        voice_trigger_type = mark_type_cfg.get('trigger_type')
        if voice_trigger_type:
            msg['voice_trigger_type'] = voice_trigger_type
        if extra_args and mark_type == MARK_RES:
            item_id = extra_args.get('item_id')
            text_id = extra_args.get('text_id')
            if item_id is not None:
                msg = {'text': text_id or 16039,'mark_item_id': item_id}
        global_data.cam_lplayer.send_event('E_SEND_BATTLE_GROUP_MSG', msg, True)
        return


def check_can_draw_mark_or_route():
    if global_data.player and global_data.player.logic:
        is_die = global_data.player.logic.ev_g_death()
        if is_die:
            return False
    return True


def trans_to_map_idx--- This code section failed: ---

 134       0  LOAD_GLOBAL           0  'world'
           3  LOAD_ATTR             1  'get_active_scene'
           6  CALL_FUNCTION_0       0 
           9  LOAD_ATTR             2  'get_safe_scene_map_uv_parameters'
          12  CALL_FUNCTION_0       0 
          15  UNPACK_SEQUENCE_5     5 
          18  STORE_FAST            2  'l_idx'
          21  STORE_FAST            3  'r_idx'
          24  STORE_FAST            4  'btm_idx'
          27  STORE_FAST            5  'up_idx'
          30  STORE_FAST            6  'trunk_size'

 135      33  STORE_FAST            1  'right_top_pos'
          36  BINARY_SUBSCR    
          37  LOAD_GLOBAL           3  'float'
          40  LOAD_FAST             6  'trunk_size'
          43  CALL_FUNCTION_1       1 
          46  BINARY_DIVIDE    
          47  LOAD_CONST            2  0.5
          50  BINARY_ADD       
          51  STORE_FAST            7  'l_x_idx'

 136      54  STORE_FAST            3  'r_idx'
          57  BINARY_SUBSCR    
          58  LOAD_GLOBAL           3  'float'
          61  LOAD_FAST             6  'trunk_size'
          64  CALL_FUNCTION_1       1 
          67  BINARY_DIVIDE    
          68  LOAD_CONST            2  0.5
          71  BINARY_ADD       
          72  STORE_FAST            8  'l_y_idx'

 138      75  LOAD_FAST             1  'right_top_pos'
          78  LOAD_CONST            1  ''
          81  BINARY_SUBSCR    
          82  LOAD_GLOBAL           3  'float'
          85  LOAD_FAST             6  'trunk_size'
          88  CALL_FUNCTION_1       1 
          91  BINARY_DIVIDE    
          92  LOAD_CONST            2  0.5
          95  BINARY_SUBTRACT  
          96  STORE_FAST            9  'r_x_idx'

 139      99  LOAD_FAST             1  'right_top_pos'
         102  LOAD_CONST            3  1
         105  BINARY_SUBSCR    
         106  LOAD_GLOBAL           3  'float'
         109  LOAD_FAST             6  'trunk_size'
         112  CALL_FUNCTION_1       1 
         115  BINARY_DIVIDE    
         116  LOAD_CONST            2  0.5
         119  BINARY_SUBTRACT  
         120  STORE_FAST           10  'r_y_idx'

 140     123  LOAD_GLOBAL           4  'print'
         126  LOAD_CONST            4  'area_map_rect'
         129  LOAD_FAST             7  'l_x_idx'
         132  LOAD_FAST             8  'l_y_idx'
         135  LOAD_FAST             9  'r_x_idx'
         138  LOAD_FAST            10  'r_y_idx'
         141  BUILD_LIST_4          4 
         144  CALL_FUNCTION_2       2 
         147  POP_TOP          

Parse error at or near `STORE_FAST' instruction at offset 33