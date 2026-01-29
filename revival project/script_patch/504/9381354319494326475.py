# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPhantomAppearance.py
from __future__ import absolute_import
from six import iteritems
from six.moves import range
import math3d
import world
import random
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID, get_mecha_model_path, battle_id_to_mecha_lobby_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, MECHA_FASHION_KEY
from logic.gutils.mecha_utils import check_need_flip, check_need_scale
from logic.gcommon.const import NEOX_UNIT_SCALE, CHARACTER_LERP_DIR_YAWS
from common.cfg import confmgr
from logic.gcommon.component.client.com_mecha_appearance.ComPhantomCtrl import STATE_IDLE, STATE_RUN, STATE_NONE
from logic.client.const.game_mode_const import GAME_MODE_SURVIVALS
from logic.gutils.mecha_skin_utils import get_mecha_skin_res_readonly_info, MechaSocketResAgent, get_accurate_mecha_skin_info_from_fasion_data
from logic.gcommon.common_const.mecha_const import STATE_VISIBLE, STATE_SHOTGUN_RELOAD, STATE_RIFLE, STATE_SHOTGUN, STATE_RIFLE_VICE, STATE_SHOTGUN_VICE
from logic.gutils.dress_utils import get_mecha_default_fashion
from ext_package.ext_decorator import has_skin_ext
from common.utils.timer import CLOCK
ANIM_TO_STATE = {'run': STATE_RIFLE,
   'rifle_vice_start': STATE_RIFLE_VICE,
   'shotgun_vice_start': STATE_SHOTGUN_VICE,
   'rifle_idle': STATE_RIFLE,
   'rifle_aim': STATE_RIFLE,
   'run_stop': STATE_RIFLE
   }
PHANTOM_SHOW_EFFECT_ID = {8029: '100',8023: '104'}
PHANTOM_DISAPPEAR_EFFECT_ID = {8029: '101',8023: '105'}
PHANTOM_TAIL_EFFECT_ID = {8029: '102'}
PHANTOM_HIT_EFFECT_ID = {8029: '103',8023: '106'}
PHANTOM_GROUPMATE_TAG_EFFECT_ID = {8029: '106',8023: ['107', '109']}
SOUND_NAME = {8029: 'm_8029_ray_loop_3p'}

class ComPhantomAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_MECHA_FASHION_ID': 'get_mecha_fashion_id',
       'E_MECHA_LOD_LOADED_FIRST': ('on_load_lod_complete_first', 10),
       'E_UPDATE_PHANTOM_STATE': '_update_phantom_state',
       'E_8029_PHANTOM_START_DESTROY': '_update_destroy_state',
       'E_PLAY_HIT_SFX': '_play_hit_sfx',
       'E_MECHA_LOD_LOADED': 'on_load_lod_complete',
       'G_MECHA_SKIN_AND_SHINY_WEAPON_ID': 'get_mecha_skin_and_shiny_weapon_id'
       })
    MODEL_PATH = 'model_new/mecha/8029/8029/empty.gim'
    HIT_SFX = 'effect/fx/mecha/8029/8029_hit.sfx'

    def __init__(self):
        super(ComPhantomAppearance, self).__init__()
        self._mecha_fashion_id = None
        self._born_pos = [0, 0, 0]
        self._yaw = 0
        self._state = STATE_NONE
        self._is_play_hit_sfx = False
        self._extra_info = {}
        self._random_anim_timer = None
        self._play_anim = None
        self._sfx_dict = {}
        self._shiny_weapon_id = 0
        self._skin_model_and_effect_loaded = False
        self.sd.ref_socket_res_agent = None
        self._sound_id = None
        self._end_sound = None
        self._loop_sound = None
        self._first_load = False
        self._sfx_idle = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self.sd.ref_mecha_id = bdict.get('mecha_id', 8029)
        self.sd.ref_owner_id = bdict.get('owner_eid', None)
        self.sd.ref_camp_id = bdict.get('faction_id', 0)
        self.sd.ref_socket_res_agent = MechaSocketResAgent()
        self._mecha_fashion_id, self._shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(self.sd.ref_mecha_id, bdict.get(MECHA_FASHION_KEY, {}))
        self._born_pos = bdict.get('position', [0, 0, 0])
        self._yaw = bdict.get('yaw', 0)
        self._state = bdict.get('state', STATE_RUN)
        self._is_play_hit_sfx = False
        self._extra_info = bdict.get('extra_info', {})
        self._random_anim_list = self._extra_info.get('random_anim_list', [])
        self._sfx_dict = get_mecha_skin_res_readonly_info(self.sd.ref_mecha_id, self._mecha_fashion_id, self._shiny_weapon_id)
        super(ComPhantomAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def on_load_model_complete(self, model, user_data):
        model.world_position = math3d.vector(*self._born_pos)
        model.rotation_matrix = math3d.matrix.make_rotation_y(self._yaw)
        self._update_model_attributes(model)
        self.send_event('E_HUMAN_MODEL_LOADED', model, user_data)
        self._set_model_visible(False)
        self._init_voice()

    def on_load_lod_complete_first(self):
        self._load_skin_model_and_effect()
        self._update_phantom_state(self._state)

    def create_model_sfx(self, effect_id, duration_scale=1.0, create_cb=None, remove_cb=None, need_return_sfx_id=False):
        effect_list = self._sfx_dict.get(effect_id, [])
        sfx_id = None
        for effect_info in effect_list:
            sfx_path = effect_info['final_correspond_path']
            duration = effect_info.get('duration', 0)
            for socket in effect_info.get('socket_list', []):
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self._model, socket, duration=duration * duration_scale, on_create_func=create_cb, on_remove_func=remove_cb)

        if need_return_sfx_id:
            return sfx_id
        else:
            return

    def _init_voice(self):
        if self._loop_sound:
            global_data.sound_mgr.stop_playing_id(self._loop_sound)
        sound_name = SOUND_NAME.get(self.sd.ref_mecha_id)
        if not sound_name:
            return
        self._sound_id = global_data.sound_mgr.register_game_obj(sound_name + str(self.unit_obj.id))
        global_data.sound_mgr.set_position(self._sound_id, self.model.position)
        self._loop_sound = global_data.sound_mgr.post_event(sound_name, self._sound_id)

    def _init_outline(self):
        if not global_data.cam_lctarget or not global_data.battle:
            return
        param = {'status_type': 'XRAY_ONLY','u_color': (0.0625, 0.3359, 1.0, 1.0),
           'outline_alpha': 0.0,
           'update_interval': 5.0
           }
        if self.sd.ref_owner_id == global_data.cam_lplayer.id:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray')
            param['u_color'] = tuple(self._extra_info.get('xray_self', (0.0625, 0.3359,
                                                                        1.0, 1.0)))
            self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_xray', param, prority=0)
            sfx_path = PHANTOM_GROUPMATE_TAG_EFFECT_ID[self.sd.ref_mecha_id]
            if isinstance(sfx_path, list):
                sfx_path = sfx_path[0]
            self._sfx_idle = self.create_model_sfx(sfx_path, need_return_sfx_id=True)
        elif global_data.cam_lctarget.ev_g_is_campmate(self.sd.ref_camp_id):
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray')
            param['u_color'] = tuple(self._extra_info.get('xray_teammate', (0.0625,
                                                                            0.3359,
                                                                            1.0,
                                                                            1.0)))
            self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_xray', param, prority=0)
            sfx_path = PHANTOM_GROUPMATE_TAG_EFFECT_ID[self.sd.ref_mecha_id]
            if isinstance(sfx_path, list):
                sfx_path = sfx_path[1]
            self._sfx_idle = self.create_model_sfx(sfx_path, need_return_sfx_id=True)
        elif global_data.game_mode and not global_data.game_mode.is_mode_type(GAME_MODE_SURVIVALS):
            param['status_type'] = 'OUTLINE_ONLY'
            param['outline_alpha'] = 0.333
            param['u_color'] = tuple(self._extra_info.get('xray_enemy', (0.0625, 0.3359,
                                                                         1.0, 1.0)))
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_outline')
            self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_outline', param, prority=0)
        self.send_event('E_UPDATE_CURRENT_MATERIAL_STATUS')

    def _set_model_visible(self, visible):
        model = self.model
        if not model:
            return
        model.visible = visible

    def on_load_lod_complete(self, *args):
        if not self._first_load:
            self._first_load = True
            return
        else:
            if self._sfx_idle:
                global_data.sfx_mgr.remove_sfx_by_id(self._sfx_idle)
                self._sfx_idle = None
            self._init_outline()
            return

    def _update_phantom_state(self, state):
        if not self.model:
            return
        if state == STATE_RUN:
            self._play_animation('run', -1, world.TRANSIT_TYPE_DELAY, 0, world.PLAY_FLAG_LOOP)
        elif state == STATE_IDLE:
            if self._state == STATE_RUN:
                self._model.register_anim_key_event('run_stop', 'end', lambda *args: self._update_phantom_state(STATE_IDLE))
                self._play_animation('run_stop', 300, world.TRANSIT_TYPE_DELAY, 0, world.PLAY_FLAG_NO_LOOP)
            else:
                self._play_random_anim()
        self._state = state

    def _update_destroy_state(self):
        self.create_model_sfx(PHANTOM_DISAPPEAR_EFFECT_ID[self.sd.ref_mecha_id])
        if self.model:
            global_data.sound_mgr.play_event('m_8029_ray_end_3p', self.model.position)

    def _update_model_attributes(self, model):
        model.set_enable_lerp_dir_light(True)
        model.set_lerp_dir_light_yaws(CHARACTER_LERP_DIR_YAWS)
        model.shader_lod_type = world.SHADER_LOD_TYPE_CHAR
        if hasattr(model, 'can_skip_update'):
            model.can_skip_update = False
        if global_data.enable_other_model_shadowmap:
            model.cast_shadow = True
            model.receive_shadow = True
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            model.set_submesh_hitmask(i, world.HIT_SKIP)

        check_need_scale(model, self.sd.ref_mecha_id, self._mecha_fashion_id, False)
        check_need_flip(model)

    def _play_hit_sfx(self):
        if self._is_play_hit_sfx:
            return

        def remove_sfx(sfx):
            self._is_play_hit_sfx = False
            self._init_outline()

        self._is_play_hit_sfx = True
        self.create_model_sfx(PHANTOM_HIT_EFFECT_ID[self.sd.ref_mecha_id], remove_cb=remove_sfx)

    def _play_animation(self, *args):
        anim_name, trans_time, trans_type, start_time, is_loop = args
        self._play_anim = anim_name
        state_list = STATE_VISIBLE[ANIM_TO_STATE.get(anim_name, STATE_RIFLE)]
        socket_res_agent = self.sd.ref_socket_res_agent
        for vis_state in state_list[0]:
            socket_res_agent.set_model_res_visible(True, vis_state)

        for invis_state in state_list[1]:
            socket_res_agent.set_model_res_visible(False, invis_state)

        self._model.play_animation(*args)

    def _play_random_anim--- This code section failed: ---

 245       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_is_valid'
           6  UNARY_NOT        
           7  POP_JUMP_IF_TRUE     20  'to 20'
          10  LOAD_FAST             0  'self'
          13  LOAD_ATTR             1  'model'
          16  UNARY_NOT        
        17_0  COME_FROM                '7'
          17  POP_JUMP_IF_FALSE    24  'to 24'

 246      20  LOAD_CONST            0  ''
          23  RETURN_END_IF    
        24_0  COME_FROM                '17'

 247      24  LOAD_GLOBAL           2  'True'
          27  STORE_FAST            1  'play_idle_anim'

 248      30  LOAD_GLOBAL           3  'getattr'
          33  LOAD_GLOBAL           1  'model'
          36  LOAD_GLOBAL           4  'False'
          39  CALL_FUNCTION_3       3 
          42  POP_JUMP_IF_FALSE    78  'to 78'

 249      45  LOAD_GLOBAL           5  'random'
          48  LOAD_ATTR             6  'Random'
          51  CALL_FUNCTION_0       0 
          54  STORE_FAST            2  'rand'

 250      57  LOAD_FAST             2  'rand'
          60  LOAD_ATTR             5  'random'
          63  CALL_FUNCTION_0       0 
          66  LOAD_CONST            2  0.5
          69  COMPARE_OP            1  '<='
          72  STORE_FAST            1  'play_idle_anim'
          75  JUMP_FORWARD          0  'to 78'
        78_0  COME_FROM                '75'

 251      78  LOAD_FAST             1  'play_idle_anim'
          81  POP_JUMP_IF_FALSE   109  'to 109'

 252      84  LOAD_FAST             0  'self'
          87  LOAD_ATTR             7  '_random_anim_list'
          90  LOAD_CONST            3  ''
          93  BINARY_SUBSCR    
          94  STORE_FAST            3  'anim'

 253      97  LOAD_GLOBAL           2  'True'
         100  LOAD_FAST             0  'self'
         103  STORE_ATTR            8  '_cur_playing_idle'
         106  JUMP_FORWARD         53  'to 162'

 255     109  LOAD_FAST             2  'rand'
         112  LOAD_ATTR             9  'randint'
         115  LOAD_CONST            4  1
         118  LOAD_GLOBAL          10  'len'
         121  LOAD_FAST             0  'self'
         124  LOAD_ATTR             7  '_random_anim_list'
         127  CALL_FUNCTION_1       1 
         130  LOAD_CONST            4  1
         133  BINARY_SUBTRACT  
         134  CALL_FUNCTION_2       2 
         137  STORE_FAST            4  'idx'

 256     140  LOAD_FAST             0  'self'
         143  LOAD_ATTR             7  '_random_anim_list'
         146  LOAD_FAST             4  'idx'
         149  BINARY_SUBSCR    
         150  STORE_FAST            3  'anim'

 257     153  LOAD_GLOBAL           4  'False'
         156  LOAD_FAST             0  'self'
         159  STORE_ATTR            8  '_cur_playing_idle'
       162_0  COME_FROM                '106'

 258     162  LOAD_FAST             0  'self'
         165  LOAD_ATTR            11  '_play_animation'
         168  LOAD_FAST             3  'anim'
         171  LOAD_CONST            5  300
         174  LOAD_GLOBAL          12  'world'
         177  LOAD_ATTR            13  'TRANSIT_TYPE_DELAY'
         180  LOAD_CONST            3  ''
         183  LOAD_FAST             0  'self'
         186  LOAD_ATTR             8  '_cur_playing_idle'
         189  POP_JUMP_IF_FALSE   201  'to 201'
         192  LOAD_GLOBAL          12  'world'
         195  LOAD_ATTR            14  'PLAY_FLAG_LOOP'
         198  JUMP_FORWARD          6  'to 207'
         201  LOAD_GLOBAL          12  'world'
         204  LOAD_ATTR            15  'PLAY_FLAG_NO_LOOP'
       207_0  COME_FROM                '198'
         207  CALL_FUNCTION_5       5 
         210  POP_TOP          

 259     211  LOAD_FAST             0  'self'
         214  LOAD_ATTR             1  'model'
         217  LOAD_ATTR            16  'get_anim_length'
         220  LOAD_FAST             3  'anim'
         223  CALL_FUNCTION_1       1 
         226  LOAD_CONST            6  1000.0
         229  BINARY_DIVIDE    
         230  STORE_FAST            5  'anim_length'

 260     233  LOAD_FAST             0  'self'
         236  LOAD_ATTR            17  'clear_ramdom_timer'
         239  CALL_FUNCTION_0       0 
         242  POP_TOP          

 261     243  LOAD_GLOBAL          18  'global_data'
         246  LOAD_ATTR            19  'game_mgr'
         249  LOAD_ATTR            20  'register_logic_timer'
         252  LOAD_FAST             0  'self'
         255  LOAD_ATTR            21  '_play_random_anim'
         258  LOAD_CONST            7  'interval'
         261  LOAD_FAST             5  'anim_length'
         264  LOAD_CONST            8  'mode'
         267  LOAD_GLOBAL          22  'CLOCK'
         270  CALL_FUNCTION_513   513 
         273  LOAD_FAST             0  'self'
         276  STORE_ATTR           23  '_random_anim_timer'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 39

    def _load_skin_model_and_effect(self):
        if self._skin_model_and_effect_loaded:
            return
        self.sd.ref_socket_res_agent.load_skin_model_and_effect(self.model, self._mecha_fashion_id, self._shiny_weapon_id, is_phantom=True, need_listen_anim_enter_leave=False)
        self._skin_model_and_effect_loaded = True
        if global_data.cam_lplayer and global_data.cam_lctarget.ev_g_is_campmate(self.sd.ref_camp_id):
            duration_scale = 0.1
        else:
            duration_scale = 1.0
        self.create_model_sfx(PHANTOM_SHOW_EFFECT_ID[self.sd.ref_mecha_id], duration_scale=duration_scale, create_cb=self._on_create_show_sfx, remove_cb=self._on_remove_show_sfx)

    def _on_create_show_sfx(self, *args):

        def do_set_model_visible():
            self._set_model_visible(True)
            self._update_phantom_state(self._state)
            tail_effect = PHANTOM_TAIL_EFFECT_ID.get(self.sd.ref_mecha_id)
            if tail_effect:
                self.create_model_sfx(tail_effect)
            if 'set_socket_res_vis' in self._extra_info:
                for key, vis in iteritems(self._extra_info['set_socket_res_vis']):
                    if self.sd.ref_socket_res_agent:
                        self.sd.ref_socket_res_agent.set_model_res_visible(bool(vis), key)

        global_data.game_mgr.post_exec(do_set_model_visible)

    def _on_remove_show_sfx(self, *args):
        self._init_outline()

    def _on_pos_changed(self, position):
        super(ComPhantomAppearance, self)._on_pos_changed(position)
        if not self._sound_id:
            return
        global_data.sound_mgr.set_position(self._sound_id, position)

    def get_mecha_fashion_id(self):
        return self._mecha_fashion_id

    def get_mecha_skin_and_shiny_weapon_id(self):
        return (
         self._mecha_fashion_id, None)

    def get_model_info(self, unit, bdict):
        model_path = get_mecha_model_path(self.sd.ref_mecha_id, self._mecha_fashion_id) or self.MODEL_PATH
        return (
         model_path, None, None)

    def clear_ramdom_timer(self):
        if self._random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self._random_anim_timer)
        self._random_anim_timer = None
        return

    def on_model_destroy(self):
        self._clear_skin_model_and_effect()

    def _clear_skin_model_and_effect(self):
        if self.sd.ref_socket_res_agent:
            self.sd.ref_socket_res_agent.destroy()
            self.sd.ref_socket_res_agent = None
        self._skin_model_and_effect_loaded = False
        return

    def destroy(self):
        self._first_load = False
        self.clear_ramdom_timer()
        if self._sound_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_id)
        if self._loop_sound:
            global_data.sound_mgr.stop_playing_id(self._loop_sound)
        if self._sfx_idle:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_idle)
            self._sfx_idle = None
        super(ComPhantomAppearance, self).destroy()
        return