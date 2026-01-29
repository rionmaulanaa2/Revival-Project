# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/interaction_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from logic.gcommon.common_const import scene_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const
from logic.gutils.items_book_utils import get_interaction_ui_icon
from logic.gutils.mecha_skin_utils import get_mecha_skin_no_by_item_no
from common.framework import Functor
import collision
import math
import math3d
from time import time
import world
from common.cfg import confmgr
import game3d
_HASH_scale = game3d.calc_string_hash('Scale')
MIN_VERTICAL_SIN = math.sin(math.pi / 3)
SPRAY_CHECK_DISTANCE = 50 * NEOX_UNIT_SCALE
OPEN_ANIM_NAME = 'open'
IDLE_ANIM_NAME = 'open_idle'
CLOSE_ANIM_NAME = 'close'
SPRAY_SFX_PATH = 'effect/fx/common/spray/spray_1.sfx'
DEFAULT_TEXTURE_PATH = 'effect/fx/common/spray/default.png'
SPRAY_SFX_PATTERN = 'effect/fx/spray/%d.sfx'
DEFAULT_DURATION = 10
DEFAULT_SPRAY_PATH = ''
EMOJ_DIR = 'model_new/others/emoji/'
SFX_DIR = 'effect/fx/niudan/'
AVATAR_SCALE = 2.0
PUPPET_SCALE = 2.0
GLOBAL_SPRAY_ID_DICT = {}
_HASH_TEX = '_Tex'
_HASH_TEX_ID = game3d.calc_string_hash(_HASH_TEX)
EMO_TEX_PATH = 'gui/emoji_tex/%s.tga'
EMO_MODEL_PATH = 'model_new/others/emoji/%s.gim'
MECHA_EX_ICON_PATH = 'gui/ui_res_2/item/ex_icon/'

def _do_generate_spray(spray_id, v3d_pos, v3d_elr_rot):
    lst_pos = (
     v3d_pos.x, v3d_pos.y, v3d_pos.z)
    lst_elr_rot = (v3d_elr_rot.x, v3d_elr_rot.y, v3d_elr_rot.z)
    return (
     lst_pos, lst_elr_rot, time())


def generate_lobby_spray_info--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'int'
           3  LOAD_FAST             0  'item_no'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            0  'item_no'

  51      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'scene'
          21  STORE_FAST            1  'cnt_scene'

  52      24  LOAD_FAST             1  'cnt_scene'
          27  POP_JUMP_IF_TRUE     34  'to 34'

  53      30  LOAD_CONST            0  ''
          33  RETURN_END_IF    
        34_0  COME_FROM                '27'

  54      34  LOAD_FAST             1  'cnt_scene'
          37  LOAD_ATTR             4  'get_type'
          40  CALL_FUNCTION_0       0 
          43  LOAD_GLOBAL           5  'scene_const'
          46  LOAD_ATTR             6  'SCENE_LOBBY'
          49  COMPARE_OP            3  '!='
          52  POP_JUMP_IF_FALSE    59  'to 59'

  55      55  LOAD_CONST            0  ''
          58  RETURN_END_IF    
        59_0  COME_FROM                '52'

  56      59  LOAD_GLOBAL           1  'global_data'
          62  LOAD_ATTR             7  'lobby_player'
          65  STORE_FAST            2  'lobby_player'

  57      68  LOAD_FAST             2  'lobby_player'
          71  POP_JUMP_IF_TRUE     78  'to 78'

  58      74  LOAD_CONST            0  ''
          77  RETURN_END_IF    
        78_0  COME_FROM                '71'

  59      78  LOAD_FAST             1  'cnt_scene'
          81  LOAD_ATTR             8  'active_camera'
          84  STORE_FAST            3  'camera'

  60      87  LOAD_FAST             3  'camera'
          90  POP_JUMP_IF_TRUE     97  'to 97'

  61      93  LOAD_CONST            0  ''
          96  RETURN_END_IF    
        97_0  COME_FROM                '90'

  62      97  LOAD_GLOBAL           1  'global_data'
         100  LOAD_ATTR             7  'lobby_player'
         103  LOAD_ATTR             9  'ev_g_model'
         106  CALL_FUNCTION_0       0 
         109  STORE_FAST            4  'model'

  63     112  LOAD_FAST             4  'model'
         115  POP_JUMP_IF_TRUE    122  'to 122'

  64     118  LOAD_CONST            0  ''
         121  RETURN_END_IF    
       122_0  COME_FROM                '115'

  66     122  LOAD_FAST             3  'camera'
         125  LOAD_ATTR            10  'world_position'
         128  STORE_FAST            5  'cam_pos'

  67     131  LOAD_FAST             3  'camera'
         134  LOAD_ATTR            11  'world_rotation_matrix'
         137  LOAD_ATTR            12  'forward'
         140  STORE_FAST            6  'cam_forward'

  68     143  LOAD_FAST             4  'model'
         146  LOAD_ATTR            11  'world_rotation_matrix'
         149  LOAD_ATTR            13  'right'
         152  STORE_FAST            7  'right'

  69     155  LOAD_FAST             6  'cam_forward'
         158  LOAD_GLOBAL          14  'SPRAY_CHECK_DISTANCE'
         161  BINARY_MULTIPLY  
         162  LOAD_FAST             5  'cam_pos'
         165  BINARY_ADD       
         166  STORE_FAST            8  'check_end'

  70     169  LOAD_FAST             1  'cnt_scene'
         172  LOAD_ATTR            15  'scene_col'
         175  LOAD_ATTR            16  'hit_by_ray'
         178  LOAD_FAST             5  'cam_pos'
         181  LOAD_FAST             8  'check_end'
         184  LOAD_CONST            1  ''
         187  LOAD_GLOBAL          17  'collision_const'
         190  LOAD_ATTR            18  'LAND_GROUP'
         193  LOAD_GLOBAL          17  'collision_const'
         196  LOAD_ATTR            18  'LAND_GROUP'
         199  LOAD_GLOBAL          19  'collision'
         202  LOAD_ATTR            20  'INCLUDE_FILTER'
         205  LOAD_GLOBAL          21  'False'
         208  CALL_FUNCTION_7       7 
         211  STORE_FAST            9  'result'

  71     214  LOAD_FAST             9  'result'
         217  LOAD_CONST            1  ''
         220  BINARY_SUBSCR    
         221  POP_JUMP_IF_FALSE   428  'to 428'

  72     224  LOAD_FAST             9  'result'
         227  LOAD_CONST            2  2
         230  BINARY_SUBSCR    
         231  STORE_FAST           10  'spray_normal'

  73     234  LOAD_FAST             9  'result'
         237  LOAD_CONST            3  1
         240  BINARY_SUBSCR    
         241  STORE_FAST           11  'spray_position'

  74     244  LOAD_FAST             7  'right'
         247  LOAD_ATTR            22  'cross'
         250  LOAD_FAST            10  'spray_normal'
         253  CALL_FUNCTION_1       1 
         256  STORE_FAST           12  'spray_forward'

  75     259  LOAD_GLOBAL          23  'abs'
         262  LOAD_FAST            10  'spray_normal'
         265  LOAD_ATTR            24  'y'
         268  CALL_FUNCTION_1       1 
         271  LOAD_GLOBAL          25  'MIN_VERTICAL_SIN'
         274  COMPARE_OP            0  '<'
         277  POP_JUMP_IF_FALSE   304  'to 304'

  76     280  LOAD_GLOBAL          26  'math3d'
         283  LOAD_ATTR            27  'vector'
         286  LOAD_CONST            1  ''
         289  LOAD_CONST            3  1
         292  LOAD_CONST            1  ''
         295  CALL_FUNCTION_3       3 
         298  STORE_FAST           12  'spray_forward'
         301  JUMP_FORWARD          0  'to 304'
       304_0  COME_FROM                '301'

  78     304  LOAD_FAST            10  'spray_normal'
         307  LOAD_ATTR            22  'cross'
         310  LOAD_FAST            12  'spray_forward'
         313  CALL_FUNCTION_1       1 
         316  STORE_FAST           12  'spray_forward'

  79     319  LOAD_GLOBAL          26  'math3d'
         322  LOAD_ATTR            28  'matrix'
         325  LOAD_ATTR            29  'make_orient'
         328  LOAD_FAST            12  'spray_forward'
         331  LOAD_FAST            10  'spray_normal'
         334  UNARY_NEGATIVE   
         335  CALL_FUNCTION_2       2 
         338  STORE_FAST           13  'spray_rotation'

  80     341  LOAD_GLOBAL          26  'math3d'
         344  LOAD_ATTR            30  'matrix_to_euler'
         347  LOAD_FAST            13  'spray_rotation'
         350  CALL_FUNCTION_1       1 
         353  STORE_FAST           14  'spray_euler'

  81     356  LOAD_GLOBAL          31  '_do_generate_spray'
         359  LOAD_FAST             0  'item_no'
         362  LOAD_FAST            11  'spray_position'
         365  LOAD_FAST            14  'spray_euler'
         368  CALL_FUNCTION_3       3 
         371  UNPACK_SEQUENCE_3     3 
         374  STORE_FAST           15  'pos'
         377  STORE_FAST           16  'euler_vec'
         380  STORE_FAST           17  'create_time'

  82     383  BUILD_MAP_4           4 

  83     386  LOAD_FAST            15  'pos'
         389  LOAD_CONST            4  'position'
         392  STORE_MAP        

  84     393  LOAD_FAST            16  'euler_vec'
         396  LOAD_CONST            5  'euler_rotation'
         399  STORE_MAP        

  85     400  LOAD_FAST            17  'create_time'
         403  LOAD_CONST            6  'create_time'
         406  STORE_MAP        

  86     407  STORE_MAP        
         408  STORE_MAP        
         409  STORE_MAP        
         410  STORE_MAP        
         411  STORE_FAST           18  'bdict'

  88     414  LOAD_GLOBAL          32  'create_spray_sfx'
         417  LOAD_FAST            18  'bdict'
         420  CALL_FUNCTION_1       1 
         423  POP_TOP          

  89     424  LOAD_FAST            18  'bdict'
         427  RETURN_END_IF    
       428_0  COME_FROM                '221'

Parse error at or near `STORE_MAP' instruction at offset 407


def get_sfx_path_by_spray_id(spray_idx):
    return SPRAY_SFX_PATTERN % spray_idx


def create_spray_sfx(bdict):
    pos_list = bdict.get('position', [0, 0, 0])
    euler_list = bdict.get('euler_rotation', [0, 0, 0])
    sfx_position = math3d.vector(*pos_list)
    sfx_rotation_euler = math3d.vector(*euler_list)
    sfx_rotation_matrix = math3d.euler_to_matrix(sfx_rotation_euler)
    spray_idx = bdict.get('spray_id', 0)
    create_timestamp = bdict.get('create_time', time())
    spray_items_conf = confmgr.get('spray_conf', 'SprayConfig', 'Content')
    spray_item = spray_items_conf.get(str(spray_idx), {})
    scale_num = spray_item.get('scale', 1.0)
    last_duration = spray_item.get('duration', DEFAULT_DURATION)
    rel_duration = last_duration - (time() - create_timestamp)
    scale = math3d.vector(scale_num, scale_num, scale_num)
    if rel_duration > 0:
        sfx_path = get_sfx_path_by_spray_id(spray_idx) or SPRAY_SFX_PATH
        sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_position, rel_duration, Functor(on_create_spray_complete, sfx_rotation_matrix, scale), on_remove_func=[on_remove_lobby_spray], ex_data={'allow_overlay': True})
        GLOBAL_SPRAY_ID_DICT[sfx_id] = 1


def clean_lobby_spray():
    keys = six_ex.keys(GLOBAL_SPRAY_ID_DICT)
    for key in keys:
        global_data.sfx_mgr.remove_sfx_by_id(key)


def on_remove_lobby_spray(sfx, sid):
    if sid in GLOBAL_SPRAY_ID_DICT:
        del GLOBAL_SPRAY_ID_DICT[sid]


def on_create_spray_complete(rotation, scale, sfx, *args):
    sfx.world_rotation_matrix = rotation
    sfx.scale = scale
    decal_sfx_info = global_data.sfx_mgr.get_dynamic_decal_sfx_info()
    MIN_DECAL_BIAS = 0
    cnt_max_decal_bias = MIN_DECAL_BIAS
    sprite_radius = sfx.get_sub_sprite_radius(0) * sfx.scale.x
    for k, v in six.iteritems(decal_sfx_info):
        if not k.valid:
            continue
        if not k.is_sub_decal(0):
            continue
        cmp_radius = k.get_sub_sprite_radius(0) * k.scale.x
        distance = (sfx.world_position - k.world_position).length
        if cmp_radius + sprite_radius >= distance:
            render_bias = k.render_bias
            cnt_max_decal_bias = max(cnt_max_decal_bias, render_bias)

    sfx.render_bias = min(31, cnt_max_decal_bias + 1)


def load_emoji(model_ref, item_no, cb, is_human=True, mecha_skin_no=None, mecha_skin_kill_cnt=None):
    emoji_path = get_emoj_path(is_human)
    if not emoji_path:
        return None
    else:
        return global_data.model_mgr.create_model(emoji_path, on_create_func=Functor(emoji_model_load_callback, model_ref, is_human, cb, item_no, mecha_skin_no=mecha_skin_no, mecha_skin_kill_cnt=mecha_skin_kill_cnt))


def remove_emoji(model_id, sfx_id, update_timer_id):
    global_data.sfx_mgr.shutdown_sfx_by_id(sfx_id)
    global_data.model_mgr.remove_model_by_id(model_id)
    global_data.game_mgr.unregister_logic_timer(update_timer_id)


def get_bind_point(is_human):
    if is_human:
        return 's_xuetiao'
    return 'xuetiao'


def play_emoji_sfx_open(bind_model, is_human, item_no, config_type):
    open_sfx_path = get_emoji_open_sfx_path(item_no, is_human)
    if not open_sfx_path:
        return None
    else:
        return global_data.sfx_mgr.create_sfx_on_model(open_sfx_path, bind_model, get_bind_point(is_human), on_create_func=Functor(on_emoji_sfx_loaded, config_type))


def play_emoji_sfx_idle(bind_model, is_human, item_no, config_type):
    sfx_path = get_emoji_idle_sfx_path(item_no, is_human)
    if not sfx_path:
        return None
    else:
        return global_data.sfx_mgr.create_sfx_on_model(sfx_path, bind_model, get_bind_point(is_human), on_create_func=Functor(on_emoji_sfx_loaded, config_type))


def on_emoji_sfx_loaded(config_type, emoji_sfx):
    emoj_config = confmgr.get('emoticon_conf', 'LobbyEmojiConf', 'Content', config_type)
    emoji_sfx.position = math3d.vector(0, emoj_config['offset_y'], 0)


def play_emoji_open(emoji_model, bind_model, is_human, item_no, cb):
    emoji_model.cache_animation(OPEN_ANIM_NAME, world.CACHE_ANIM_ALWAYS)
    emoji_model.play_animation(OPEN_ANIM_NAME)
    emoji_model.unregister_event(cb, 'end', OPEN_ANIM_NAME)
    emoji_model.register_anim_key_event(OPEN_ANIM_NAME, 'end', cb)


def play_emoji_idle(emoji_model, bind_model, is_human, item_no):
    emoji_model.play_animation(IDLE_ANIM_NAME)


def play_emoji_close(emoji_model, cb):
    emoji_model.play_animation(CLOSE_ANIM_NAME)
    emoji_model.unregister_event(cb, 'end', CLOSE_ANIM_NAME)
    emoji_model.register_anim_key_event(CLOSE_ANIM_NAME, 'end', cb)


def get_emoji_open_sfx_path(item_no, is_human):
    emoji_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no))
    if not emoji_config:
        return
    else:
        if is_human:
            path = emoji_config.get('human_open_effect_path', None) if 1 else emoji_config.get('mecha_open_effect_path', None)
            return path or None
        return '{0}{1}{2}'.format(SFX_DIR, path, '.sfx')


def get_emoji_idle_sfx_path(item_no, is_human):
    emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no))
    if is_human:
        path = emoj_config.get('human_idle_effect_path', None) if 1 else emoj_config.get('mecha_idle_effect_path', None)
        return path or None
    else:
        return '{0}{1}{2}'.format(SFX_DIR, path, '.sfx')


def set_material_type(emoji_model, conf_type):
    emoj_config = confmgr.get('emoticon_conf', 'LobbyEmojiConf', 'Content', conf_type)
    emoji_model.all_materials.set_var(_HASH_scale, 'Scale', emoj_config['scale'])
    emoji_model.position = math3d.vector(0, emoj_config['offset_y'], 0)


def get_emoji_duration(item_no):
    emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no))
    return emoj_config.get('keep_duration', 0.01)


def set_emoj_tex(emoji_model, item_no, item_dict=None):
    emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no))
    if not emoj_config:
        return
    UI_path = emoj_config.get('UI_path')
    sub_mat = emoji_model.get_sub_material(0)
    if UI_path:
        mecha_skin_no = str(item_dict.get('mecha_skin_no'))
        total_kill = str(item_dict.get('total_kill', 0))
        ui_rt_key = mecha_skin_no + '_' + total_kill
        ex_privilege_info = global_data.ui_rt_mgr.create_ui_rt(ui_rt_key, emoj_config)
        if ex_privilege_info:
            rt, tex, panel = ex_privilege_info
            panel.lab_value.SetString(total_kill)
            panel.bar.SetDisplayFrameByPath('', get_mecha_ex_icon_path(mecha_skin_no))
            emoji_model.visible = False

            def set_sub_mat():
                if sub_mat:
                    sub_mat.set_technique(1, 'shader/ui/blood_ui_digit.fx::UI_Blood')
                    sub_mat.set_texture(_HASH_TEX_ID, _HASH_TEX, tex)
                if emoji_model and emoji_model.valid:
                    emoji_model.visible = True

            game3d.delay_exec(100, set_sub_mat)
            game3d.delay_exec(200, lambda : global_data.ui_rt_mgr.update_ui_rt(ui_rt_key))
    else:
        sub_mat.set_texture(_HASH_TEX_ID, _HASH_TEX, EMO_TEX_PATH % str(item_no))


def emoji_model_load_callback(model_ref, is_human, cb, item_no, emoji_model, mecha_skin_no, mecha_skin_kill_cnt):
    model = model_ref()
    if not (model and model.valid):
        global_data.model_mgr.remove_model(emoji_model)
        return
    else:
        mecha_skin_no = mecha_skin_no or get_mecha_skin_no_by_item_no(item_no)
        if mecha_skin_no:
            belong_id = confmgr.get('lobby_item', str(item_no), 'belong_id')
            item_dict = global_data.player.get_mecha_skin_kill_cnt(belong_id)
            item_dict['mecha_skin_no'] = mecha_skin_no
            if mecha_skin_kill_cnt is not None:
                item_dict['total_kill'] = mecha_skin_kill_cnt
        else:
            item_dict = None
        set_emoj_tex(emoji_model, item_no, item_dict)
        bind_point = get_bind_point(is_human)
        emoji_model.remove_from_parent()
        model.bind(bind_point, emoji_model, world.BIND_TYPE_TRANSLATE)
        if cb:
            cb(emoji_model)
        return


def get_emoj_path(is_human):
    target = 'human' if is_human else 'mecha'
    return EMO_MODEL_PATH % target


def get_gesture_action_name(item_no):
    gesture_items_conf = confmgr.get('gesture_conf', 'GestureConfig', 'Content')
    item_no = str(item_no)
    if item_no not in gesture_items_conf:
        return None
    else:
        return gesture_items_conf[item_no]['action_name']


def get_mecha_ex_icon_path(mecha_skin_no=201802251):
    return '{}{}{}'.format(MECHA_EX_ICON_PATH, str(mecha_skin_no), '.png')


def set_emoji_icon(item, item_no):
    from logic.gutils import item_utils
    from logic.gcommon.item import lobby_item_type
    if item_utils.get_lobby_item_type(item_no) == lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE:
        path = item_utils.get_interact_mecha_img(item_no)
    else:
        mecha_skin_no = get_mecha_skin_no_by_item_no(item_no)
        path = get_mecha_ex_icon_path(mecha_skin_no) if mecha_skin_no else get_interaction_ui_icon(item_no)
    item.icon_action_spray.SetDisplayFrameByPath('', path)