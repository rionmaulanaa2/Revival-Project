# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8023.py
from __future__ import absolute_import
from six.moves import range
import render
import world
import weakref
from .ComGenericMechaEffect import ComGenericMechaEffect
from common.cfg import confmgr
from logic.gcommon.const import PART_WEAPON_POS_MAIN3
from logic.gutils.mecha_utils import get_fire_end_posiiton
from logic.gcommon.common_const.mecha_const import MECHA_8023_FORM_PISTOL
from logic.gutils.screen_effect_utils import create_screen_effect_with_auto_refresh, remove_screen_effect_with_auto_refresh
import logic.gcommon.common_utils.bcast_utils as bcast
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
EFFECT_TYPE_INVIS = 0
EFFECT_TYPE_DASH = 1
SCREEN_EFFECT = {EFFECT_TYPE_INVIS: '100',EFFECT_TYPE_DASH: '110'}

class ComMechaEffect8023(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_ACC_WP_TRACK': 'show_weapon_track',
       'E_STOP_ACC_WP_TRACK': 'stop_weapon_track',
       'E_CREATE_HOLD_EFFECT': 'on_trigger_hold_effect',
       'E_REFRESH_AKIMBO_MODEL': 'refresh_akimbo_model',
       'E_8023_SWITCH_WEAPON_FORM': 'set_weapon_form',
       'E_BLOCK_ANIM_EFFECT': 'block_anim_effect',
       'E_BLOCK_LC_EFFECT': 'block_lc_effect',
       'E_HIDE_EFFECT_WHEN_INVISIBLE': 'hide_effect_when_invisible',
       'E_SHOW_SCREEN_EFFECT': 'show_screen_effect',
       'E_SET_MODEL_OPACITY': 'on_enter_opacity',
       'E_LEAVE_MODEL_OPACITY': 'on_leave_opacity'
       })
    HAND_SOCKET = 'akimbo_hand'
    LEG_SOCKET = 'akimbo_leg'
    RIGHT = '_r'
    LEFT = '_l'
    INVISIBLE_SKILL_ID = 802354

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8023, self).init_from_dict(unit_obj, bdict)
        self.weapon_pos = PART_WEAPON_POS_MAIN3
        self._model_ref = None
        self._block_anim_effect = False
        self._block_lc_effect = False
        self.cur_weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        self.being_invisible = False
        return

    def show_screen_effect(self, show, effect_type):
        screen_effect_id = SCREEN_EFFECT.get(effect_type)
        if not screen_effect_id:
            return
        screen_sfx = self._readonly_effect_conf[screen_effect_id][0]['final_correspond_path']
        if show:
            create_screen_effect_with_auto_refresh(self._driver_id, screen_sfx)
        else:
            remove_screen_effect_with_auto_refresh(self._driver_id, screen_sfx)

    def on_post_init_complete(self, bdict):
        from logic.gcommon.time_utility import get_server_time
        super(ComMechaEffect8023, self).on_post_init_complete(bdict)
        invisible_skill_conf = bdict.get('skills', {}).get(self.INVISIBLE_SKILL_ID, {})
        is_invisible = invisible_skill_conf.get('is_invisible', False)
        left_time = invisible_skill_conf.get('invisible_end_timestamp', 0) - get_server_time()
        self.send_event('E_8023_SWITCH_VISIBLE', is_invisible, left_time)
        self.need_hide_submesh = self.ev_g_mecha_shiny_weapon_id() in (201802361, 201802362,
                                                                       201802363)

    def block_anim_effect(self, block):
        self._block_anim_effect = block
        if block:
            self.clear_triggered_anim_effect()

    def block_lc_effect(self, block):
        if block:
            self.inc_disable_self_only_counter()
            self.clear_triggered_anim_effect()
        else:
            self.dec_disable_self_only_counter()

    def hide_effect_when_invisible(self, hide):
        self.being_invisible = hide
        self.sd.ref_socket_res_agent.set_sfx_res_visible(not hide, 'hide_when_invis')
        self.sd.ref_socket_res_agent.set_model_res_visible(not hide, 'hide_when_invis')

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        if self._block_anim_effect:
            return
        super(ComMechaEffect8023, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)

    def set_weapon_form(self, weapon_form):
        self.cur_weapon_form = weapon_form

    def on_model_loaded(self, model):
        super(ComMechaEffect8023, self).on_model_loaded(model)
        self._model_ref = weakref.ref(model)

    def refresh_akimbo_model(self, side=None, show_hand=None, need_sync=False):
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_REFRESH_AKIMBO_MODEL, (side, show_hand)], True)
        if show_hand is None:
            show_hand = self.cur_weapon_form == MECHA_8023_FORM_PISTOL
        if side is None:
            side = (
             self.RIGHT, self.LEFT)
        else:
            side = (
             side,)
        for s in side:
            self.sd.ref_socket_res_agent.set_model_res_visible(show_hand, self.HAND_SOCKET + s)
            self.sd.ref_socket_res_agent.set_model_res_visible(not show_hand, self.LEG_SOCKET + s)

        return

    def show_weapon_track(self, extra_speed=0, extra_g=0, extra_up=0):
        if global_data.mecha and self.unit_obj != global_data.mecha.logic:
            return
        else:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
            if not weapon:
                return
            conf = confmgr.get('grenade_config', str(weapon.iType))
            self._speed = conf['fSpeed'] + extra_speed
            self._g = -conf.get('fGravity', 98)
            self._up_angle = conf.get('fUpAngle', 0)
            mass = conf.get('fMass', 1)
            linear_damp = conf.get('fLinearDamp', 0)
            conf = confmgr.get('firearm_res_config', str(weapon.iType))
            self._fire_socket = conf.get('cBindPointEmission', None)
            if self._fire_socket:
                self._fire_socket = self._fire_socket[0]
            else:
                self._fire_socket = 'shoulei_fire'
            position = self.get_fire_pos()
            if not position:
                return
            self.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, self._speed, self._g, self._up_angle, direction=self.cal_direction(position), mass=mass, linear_damping=linear_damp)
            self.need_update = True
            return

    def stop_weapon_track(self):
        self.need_update = False
        self.send_event('E_HIDE_PARABOLA_TRACK')

    def get_fire_pos(self):
        model = self._model_ref()
        if not model or not model.valid:
            return None
        else:
            socket_matrix = model.get_socket_matrix(self._fire_socket, world.SPACE_TYPE_WORLD)
            if not socket_matrix:
                return None
            return socket_matrix.translation

    def cal_direction(self, position):
        end_pos = get_fire_end_posiiton(self.unit_obj)
        direction = end_pos - position
        if not direction.is_zero:
            direction.normalize()
        return direction

    def tick(self, delta):
        position = self.get_fire_pos()
        if not position:
            return
        direction = self.cal_direction(position)
        self.send_event('E_UPDATE_PARABOLA_TRACK', position, direction)

    def on_enter_opacity--- This code section failed: ---

 178       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'need_hide_submesh'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 179       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 180      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'ev_g_model'
          19  CALL_FUNCTION_0       0 
          22  STORE_FAST            2  'model'

 181      25  LOAD_FAST             2  'model'
          28  UNARY_NOT        
          29  POP_JUMP_IF_TRUE     42  'to 42'
          32  LOAD_FAST             2  'model'
          35  LOAD_ATTR             2  'valid'
          38  UNARY_NOT        
        39_0  COME_FROM                '29'
          39  POP_JUMP_IF_FALSE    46  'to 46'

 182      42  LOAD_CONST            0  ''
          45  RETURN_END_IF    
        46_0  COME_FROM                '39'

 184      46  LOAD_GLOBAL           3  'getattr'
          49  LOAD_GLOBAL           1  'ev_g_model'
          52  LOAD_CONST            0  ''
          55  CALL_FUNCTION_3       3 
          58  LOAD_CONST            0  ''
          61  COMPARE_OP            8  'is'
          64  POP_JUMP_IF_FALSE    80  'to 80'
          67  LOAD_FAST             0  'self'
          70  LOAD_ATTR             5  'being_invisible'
        73_0  COME_FROM                '64'
          73  POP_JUMP_IF_FALSE    80  'to 80'

 185      76  LOAD_CONST            0  ''
          79  RETURN_END_IF    
        80_0  COME_FROM                '73'

 187      80  LOAD_GLOBAL           3  'getattr'
          83  LOAD_GLOBAL           1  'ev_g_model'
          86  LOAD_CONST            0  ''
          89  CALL_FUNCTION_3       3 
          92  LOAD_CONST            0  ''
          95  COMPARE_OP            8  'is'
          98  POP_JUMP_IF_FALSE   239  'to 239'

 188     101  BUILD_LIST_0          0 
         104  LOAD_FAST             0  'self'
         107  STORE_ATTR            6  'need_hide_submesh_idx'

 189     110  SETUP_LOOP          126  'to 239'
         113  LOAD_GLOBAL           7  'range'
         116  LOAD_FAST             2  'model'
         119  LOAD_ATTR             8  'get_submesh_count'
         122  CALL_FUNCTION_0       0 
         125  CALL_FUNCTION_1       1 
         128  GET_ITER         
         129  FOR_ITER            103  'to 235'
         132  STORE_FAST            3  'i'

 190     135  LOAD_FAST             2  'model'
         138  LOAD_ATTR             9  'get_submesh_name'
         141  LOAD_FAST             3  'i'
         144  CALL_FUNCTION_1       1 
         147  LOAD_CONST            2  'hit'
         150  COMPARE_OP            2  '=='
         153  POP_JUMP_IF_FALSE   162  'to 162'

 191     156  CONTINUE            129  'to 129'
         159  JUMP_FORWARD          0  'to 162'
       162_0  COME_FROM                '159'

 193     162  LOAD_FAST             2  'model'
         165  LOAD_ATTR            10  'get_submesh_visible'
         168  LOAD_FAST             3  'i'
         171  CALL_FUNCTION_1       1 
         174  POP_JUMP_IF_TRUE    183  'to 183'

 194     177  CONTINUE            129  'to 129'
         180  JUMP_FORWARD          0  'to 183'
       183_0  COME_FROM                '180'

 195     183  LOAD_FAST             2  'model'
         186  LOAD_ATTR            11  'get_sub_material'
         189  LOAD_FAST             3  'i'
         192  CALL_FUNCTION_1       1 
         195  LOAD_ATTR            12  'transparent_mode'
         198  LOAD_GLOBAL          13  'render'
         201  LOAD_ATTR            14  'TRANSPARENT_MODE_OPAQUE'
         204  COMPARE_OP            2  '=='
         207  POP_JUMP_IF_FALSE   216  'to 216'

 196     210  CONTINUE            129  'to 129'
         213  JUMP_FORWARD          0  'to 216'
       216_0  COME_FROM                '213'

 197     216  LOAD_FAST             0  'self'
         219  LOAD_ATTR             6  'need_hide_submesh_idx'
         222  LOAD_ATTR            15  'append'
         225  LOAD_FAST             3  'i'
         228  CALL_FUNCTION_1       1 
         231  POP_TOP          
         232  JUMP_BACK           129  'to 129'
         235  POP_BLOCK        
       236_0  COME_FROM                '110'
         236  JUMP_FORWARD          0  'to 239'
       239_0  COME_FROM                '110'

 199     239  SETUP_LOOP           33  'to 275'
         242  LOAD_FAST             0  'self'
         245  LOAD_ATTR             6  'need_hide_submesh_idx'
         248  GET_ITER         
         249  FOR_ITER             22  'to 274'
         252  STORE_FAST            3  'i'

 200     255  LOAD_FAST             2  'model'
         258  LOAD_ATTR            16  'set_submesh_visible'
         261  LOAD_FAST             3  'i'
         264  LOAD_GLOBAL          17  'False'
         267  CALL_FUNCTION_2       2 
         270  POP_TOP          
         271  JUMP_BACK           249  'to 249'
         274  POP_BLOCK        
       275_0  COME_FROM                '239'
         275  LOAD_CONST            0  ''
         278  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 55

    def on_leave_opacity--- This code section failed: ---

 203       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'need_hide_submesh'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 204       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 205      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'ev_g_model'
          19  CALL_FUNCTION_0       0 
          22  STORE_FAST            2  'model'

 206      25  LOAD_FAST             2  'model'
          28  UNARY_NOT        
          29  POP_JUMP_IF_TRUE     42  'to 42'
          32  LOAD_FAST             2  'model'
          35  LOAD_ATTR             2  'valid'
          38  UNARY_NOT        
        39_0  COME_FROM                '29'
          39  POP_JUMP_IF_FALSE    46  'to 46'

 207      42  LOAD_CONST            0  ''
          45  RETURN_END_IF    
        46_0  COME_FROM                '39'

 208      46  LOAD_GLOBAL           3  'getattr'
          49  LOAD_GLOBAL           1  'ev_g_model'
          52  LOAD_CONST            0  ''
          55  CALL_FUNCTION_3       3 
          58  POP_JUMP_IF_TRUE     65  'to 65'

 209      61  LOAD_CONST            0  ''
          64  RETURN_END_IF    
        65_0  COME_FROM                '58'

 210      65  SETUP_LOOP           33  'to 101'
          68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             5  'need_hide_submesh_idx'
          74  GET_ITER         
          75  FOR_ITER             22  'to 100'
          78  STORE_FAST            3  'i'

 211      81  LOAD_FAST             2  'model'
          84  LOAD_ATTR             6  'set_submesh_visible'
          87  LOAD_FAST             3  'i'
          90  LOAD_GLOBAL           7  'True'
          93  CALL_FUNCTION_2       2 
          96  POP_TOP          
          97  JUMP_BACK            75  'to 75'
         100  POP_BLOCK        
       101_0  COME_FROM                '65'
         101  LOAD_CONST            0  ''
         104  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 55