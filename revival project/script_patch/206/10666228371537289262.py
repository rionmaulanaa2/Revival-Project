# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/SmallMapUINew.py
from __future__ import absolute_import
import six
from six.moves import range
import logic.gcommon.const as const
from common.const.uiconst import SMALL_MAP_ZORDER
from logic.comsys.map.MapBaseUINew import MapBaseUI
from logic.gutils import scene_utils
import cc
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from common.utils.ui_utils import get_scale
from logic.gcommon import time_utility
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.BattleInfo.FightKillNumberUI import FightKillNumberUI
from logic.client.const.game_mode_const import GAME_MODE_NIGHT_SURVIVAL
from logic.gcommon.common_const import attr_const
import game3d
import math
import world
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from common.cfg import confmgr
from collections import defaultdict
import common.utilities
from logic.gutils import bounty_mode_utils
from logic.gcommon.item.item_const import ITEM_GULOG_REVIVE_COIN
R_A_RATE = 180 / math.pi
MAX_SCALE_DISTANCE_SQR = (200 * const.NEOX_UNIT_SCALE) ** 2
MIN_SCALE_DISTANCE_SQR = (10 * const.NEOX_UNIT_SCALE) ** 2
SOUND_TYPE_FOOTSTEP = const.SOUND_TYPE_FOOTSTEP
SOUND_TYPE_FIRE = const.SOUND_TYPE_FIRE
SOUND_TYPE_CAR = const.SOUND_TYPE_CAR
SOUND_TYPE_SLOW_FOOTSTEP = const.SOUND_TYPE_SLOW_FOOTSTEP
SOUND_TYPE_SILENCER_FIRE = const.SOUND_TYPE_SILENCER_FIRE
SOUND_TYPE_MECHA_FIRE = const.SOUND_TYPE_MECHA_FIRE
SOUND_TYPE_MECHA_FOOTSTEP = const.SOUND_TYPE_MECHA_FOOTSTEP
SHOW_LAST_TIME = 1500
ITEM_CACHE_MAX_COUNT = 3
from logic.gcommon.common_const import ui_operation_const as uoc
DEATH_MODE_VIEW_RANGE = 300

class SmallMapBaseUI(MapBaseUI):
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_ACTION_EVENT = {'map_layer.OnClick': 'onclick_map_layer'
       }
    UI_CLICK_SALOG_DIC = {'map_layer.OnClick': '1'
       }
    GLOBAL_EVENT = {'battle_into_ace_stage_event': 'update_ace_state',
       'update_magic_region_timestamp': 'on_update_magic_region_timestamp',
       'update_rune_region_timestamp': 'on_update_rune_region_timestamp',
       'update_gravity_region_timestamp': 'on_update_gravity_region_timestamp',
       'update_bounty_region_timestamp': 'on_update_bounty_region_timestamp',
       'get_map_hint_wpos_event': 'on_get_hint_wpos',
       'update_map_test_touch_event': 'on_update_enable_touch',
       'hide_small_map_event': 'add_hide_count',
       'show_small_map_event': 'add_show_count',
       'get_small_map_show_count_event': 'get_show_count',
       'scene_observed_player_setted_event': '_on_enter_observe',
       'update_alive_player_num_event': '_update_alive_player_num',
       'judge_need_hide_details_event': '_update_judge_need_hide_details',
       'battle_into_ace_stage_event': 'change_visible_dis',
       'cam_lplayer_gulag_state_changed': 'on_update_can_revive'
       }
    HOT_KEY_FUNC_MAP = {'switch_big_map': 'keyboard_switch_big_map'}
    RECONNECT_CHECK_BATTLE = True

    def on_init_panel(self, *args, **kwargs):
        self.in_mecha_state = False
        super(SmallMapBaseUI, self).on_init_panel(*args, **kwargs)
        self._top_five_widget = None
        self.cur_survive_num = None
        self.cur_kill_mecha_num = None
        self._spectate_target = None
        self.init_widget()
        self.init_sound_visible_in_map()
        uoc.SMALL_MAP_ROTATE_ENABLE = global_data.player.get_setting(uoc.SMALL_MAP_ROTATE)
        self._tips_dict = {}
        return

    def init_sound_visible_in_map--- This code section failed: ---

 105       0  LOAD_GLOBAL           0  'True'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  '_is_run'

 106       9  LOAD_GLOBAL           2  'False'
          12  LOAD_FAST             0  'self'
          15  STORE_ATTR            3  '_is_in_mecha'

 107      18  LOAD_GLOBAL           2  'False'
          21  LOAD_FAST             0  'self'
          24  STORE_ATTR            4  '_is_ace_time'

 108      27  LOAD_CONST            0  ''
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            6  '_player'

 109      36  LOAD_CONST            0  ''
          39  LOAD_FAST             0  'self'
          42  STORE_ATTR            7  'enable_player_or_mecha'

 110      45  LOAD_GLOBAL           0  'True'
          48  LOAD_FAST             0  'self'
          51  STORE_ATTR            8  'sound_visible_enable'

 113      54  LOAD_GLOBAL           9  'global_data'
          57  LOAD_ATTR            10  'game_mode'
          60  LOAD_ATTR            11  'is_mode_type'
          63  LOAD_GLOBAL          12  'game_mode_const'
          66  LOAD_ATTR            13  'Close_VioceView'
          69  CALL_FUNCTION_1       1 
          72  UNARY_NOT        
          73  LOAD_FAST             0  'self'
          76  STORE_ATTR           14  'need_visible'

 115      79  BUILD_LIST_0          0 
          82  LOAD_FAST             0  'self'
          85  STORE_ATTR           15  'visible_opacity'

 116      88  BUILD_LIST_0          0 
          91  LOAD_FAST             0  'self'
          94  STORE_ATTR           16  'visible_dis'

 117      97  BUILD_LIST_0          0 
         100  LOAD_FAST             0  'self'
         103  STORE_ATTR           17  'visible_weight'

 118     106  BUILD_LIST_0          0 
         109  LOAD_FAST             0  'self'
         112  STORE_ATTR           18  'visible_pic'

 119     115  BUILD_LIST_0          0 
         118  LOAD_FAST             0  'self'
         121  STORE_ATTR           19  'human_visible_dis'

 120     124  BUILD_LIST_0          0 
         127  LOAD_FAST             0  'self'
         130  STORE_ATTR           20  'mecha_visible_dis'

 121     133  BUILD_LIST_0          0 
         136  LOAD_FAST             0  'self'
         139  STORE_ATTR           21  'ace_human_visible_dis'

 122     142  BUILD_LIST_0          0 
         145  LOAD_FAST             0  'self'
         148  STORE_ATTR           22  'ace_mecha_visible_dis'

 123     151  LOAD_GLOBAL          23  'CGameModeManager'
         154  CALL_FUNCTION_0       0 
         157  LOAD_ATTR            24  'get_mode_type'
         160  CALL_FUNCTION_0       0 
         163  LOAD_GLOBAL          25  'GAME_MODE_NIGHT_SURVIVAL'
         166  COMPARE_OP            2  '=='
         169  POP_JUMP_IF_FALSE   178  'to 178'
         172  LOAD_CONST            1  0.6
         175  JUMP_FORWARD          3  'to 181'
         178  LOAD_CONST            2  1
       181_0  COME_FROM                '175'
         181  STORE_FAST            1  'global_sound_visible_rate'

 125     184  LOAD_CONST            3  'human_visible_dis'
         187  LOAD_FAST             0  'self'
         190  LOAD_ATTR            19  'human_visible_dis'
         193  BUILD_TUPLE_2         2 
         196  LOAD_CONST            4  'mecha_visible_dis'
         199  LOAD_FAST             0  'self'
         202  LOAD_ATTR            20  'mecha_visible_dis'
         205  BUILD_TUPLE_2         2 
         208  LOAD_CONST            5  'ace_human_visible_dis'
         211  LOAD_FAST             0  'self'
         214  LOAD_ATTR            21  'ace_human_visible_dis'
         217  BUILD_TUPLE_2         2 
         220  LOAD_CONST            6  'ace_mecha_visible_dis'
         223  LOAD_FAST             0  'self'
         226  LOAD_ATTR            22  'ace_mecha_visible_dis'
         229  BUILD_TUPLE_2         2 
         232  BUILD_TUPLE_4         4 
         235  STORE_FAST            2  'dis_inf'

 127     238  SETUP_LOOP          198  'to 439'
         241  LOAD_GLOBAL          26  'range'
         244  LOAD_GLOBAL          27  'const'
         247  LOAD_ATTR            28  'SOUND_TYPE_MAX_COUNT'
         250  CALL_FUNCTION_1       1 
         253  GET_ITER         
         254  FOR_ITER            181  'to 438'
         257  STORE_FAST            3  'index'

 128     260  LOAD_GLOBAL          29  'confmgr'
         263  LOAD_ATTR            30  'get'
         266  LOAD_CONST            7  'sound_visible_conf'
         269  LOAD_GLOBAL          31  'str'
         272  LOAD_FAST             3  'index'
         275  CALL_FUNCTION_1       1 
         278  CALL_FUNCTION_2       2 
         281  STORE_FAST            4  'data'

 130     284  SETUP_LOOP           88  'to 375'
         287  LOAD_FAST             2  'dis_inf'
         290  GET_ITER         
         291  FOR_ITER             80  'to 374'
         294  UNPACK_SEQUENCE_2     2 
         297  STORE_FAST            5  'key'
         300  STORE_FAST            6  'visible_dis'

 131     303  BUILD_LIST_0          0 
         306  STORE_FAST            7  'dis_data'

 132     309  SETUP_LOOP           46  'to 358'
         312  LOAD_FAST             4  'data'
         315  LOAD_FAST             5  'key'
         318  BINARY_SUBSCR    
         319  GET_ITER         
         320  FOR_ITER             34  'to 357'
         323  STORE_FAST            8  'dis'

 133     326  LOAD_FAST             7  'dis_data'
         329  LOAD_ATTR            32  'append'
         332  LOAD_FAST             8  'dis'
         335  LOAD_GLOBAL          27  'const'
         338  LOAD_ATTR            33  'NEOX_UNIT_SCALE'
         341  BINARY_MULTIPLY  
         342  LOAD_FAST             1  'global_sound_visible_rate'
         345  BINARY_MULTIPLY  
         346  LOAD_CONST            8  2
         349  BINARY_POWER     
         350  CALL_FUNCTION_1       1 
         353  POP_TOP          
         354  JUMP_BACK           320  'to 320'
         357  POP_BLOCK        
       358_0  COME_FROM                '309'

 134     358  LOAD_FAST             6  'visible_dis'
         361  LOAD_ATTR            32  'append'
         364  LOAD_FAST             7  'dis_data'
         367  CALL_FUNCTION_1       1 
         370  POP_TOP          
         371  JUMP_BACK           291  'to 291'
         374  POP_BLOCK        
       375_0  COME_FROM                '284'

 136     375  LOAD_FAST             0  'self'
         378  LOAD_ATTR            15  'visible_opacity'
         381  LOAD_ATTR            32  'append'
         384  LOAD_FAST             4  'data'
         387  LOAD_CONST            9  'visible_opacity'
         390  BINARY_SUBSCR    
         391  CALL_FUNCTION_1       1 
         394  POP_TOP          

 137     395  LOAD_FAST             0  'self'
         398  LOAD_ATTR            17  'visible_weight'
         401  LOAD_ATTR            32  'append'
         404  LOAD_FAST             4  'data'
         407  LOAD_CONST           10  'visible_weight'
         410  BINARY_SUBSCR    
         411  CALL_FUNCTION_1       1 
         414  POP_TOP          

 138     415  LOAD_FAST             0  'self'
         418  LOAD_ATTR            18  'visible_pic'
         421  LOAD_ATTR            32  'append'
         424  LOAD_FAST             4  'data'
         427  LOAD_CONST           11  'visible_in_map_icon'
         430  BINARY_SUBSCR    
         431  CALL_FUNCTION_1       1 
         434  POP_TOP          
         435  JUMP_BACK           254  'to 254'
         438  POP_BLOCK        
       439_0  COME_FROM                '238'

 141     439  LOAD_FAST             0  'self'
         442  LOAD_ATTR            19  'human_visible_dis'
         445  LOAD_FAST             0  'self'
         448  STORE_ATTR           16  'visible_dis'

 143     451  BUILD_MAP_0           0 
         454  LOAD_FAST             0  'self'
         457  STORE_ATTR           34  '_show_entity'

 145     460  LOAD_GLOBAL          29  'confmgr'
         463  LOAD_ATTR            30  'get'
         466  LOAD_CONST           12  'sound_visible_const'
         469  CALL_FUNCTION_1       1 
         472  STORE_FAST            9  'conf'

 146     475  LOAD_CONST           13  3
         478  LOAD_FAST             0  'self'
         481  STORE_ATTR           35  'max_visible_item_count'

 148     484  BUILD_LIST_0          0 
         487  LOAD_FAST             0  'self'
         490  STORE_ATTR           36  '_panel_items'

 149     493  SETUP_LOOP           64  'to 560'
         496  LOAD_GLOBAL          26  'range'
         499  LOAD_FAST             0  'self'
         502  LOAD_ATTR            35  'max_visible_item_count'
         505  CALL_FUNCTION_1       1 
         508  GET_ITER         
         509  FOR_ITER             47  'to 559'
         512  STORE_FAST            3  'index'

 150     515  LOAD_GLOBAL          37  'getattr'
         518  LOAD_FAST             0  'self'
         521  LOAD_ATTR            38  'panel'
         524  LOAD_ATTR            39  'nd_sound'
         527  LOAD_CONST           14  'img_sound%d'
         530  LOAD_FAST             3  'index'
         533  BINARY_MODULO    
         534  CALL_FUNCTION_2       2 
         537  STORE_FAST           10  'item'

 151     540  LOAD_FAST             0  'self'
         543  LOAD_ATTR            36  '_panel_items'
         546  LOAD_ATTR            32  'append'
         549  LOAD_FAST            10  'item'
         552  CALL_FUNCTION_1       1 
         555  POP_TOP          
         556  JUMP_BACK           509  'to 509'
         559  POP_BLOCK        
       560_0  COME_FROM                '493'

 153     560  LOAD_FAST             9  'conf'
         563  LOAD_CONST           15  'visible_item_min_angle'
         566  BINARY_SUBSCR    
         567  LOAD_FAST             0  'self'
         570  STORE_ATTR           40  'visible_item_min_angle'

 154     573  BUILD_LIST_0          0 
         576  LOAD_FAST             0  'self'
         579  STORE_ATTR           41  '_add_entity'

 155     582  LOAD_GLOBAL           2  'False'
         585  LOAD_FAST             0  'self'
         588  STORE_ATTR           42  '_is_remove_old_entity'

 156     591  LOAD_CONST           16  ''
         594  LOAD_FAST             0  'self'
         597  STORE_ATTR           43  '_time_index'

 158     600  LOAD_CONST           16  ''
         603  LOAD_CONST           17  ('SOUND_VISIBLE_IN_MAP_KEY',)
         606  IMPORT_NAME          44  'logic.gcommon.common_const.ui_operation_const'
         609  IMPORT_FROM          45  'SOUND_VISIBLE_IN_MAP_KEY'
         612  STORE_FAST           11  'SOUND_VISIBLE_IN_MAP_KEY'
         615  POP_TOP          

 159     616  LOAD_GLOBAL           9  'global_data'
         619  LOAD_ATTR            46  'player'
         622  LOAD_ATTR            47  'get_setting'
         625  LOAD_FAST            11  'SOUND_VISIBLE_IN_MAP_KEY'
         628  CALL_FUNCTION_1       1 
         631  LOAD_FAST             0  'self'
         634  STORE_ATTR           48  'is_sound_visible_in_map'

 161     637  LOAD_GLOBAL          49  'world'
         640  LOAD_ATTR            50  'get_active_scene'
         643  CALL_FUNCTION_0       0 
         646  LOAD_FAST             0  'self'
         649  STORE_ATTR           51  '_scene'

 162     652  LOAD_FAST             0  'self'
         655  LOAD_ATTR            51  '_scene'
         658  POP_JUMP_IF_FALSE   686  'to 686'

 163     661  LOAD_FAST             0  'self'
         664  LOAD_ATTR            52  'player_change'
         667  LOAD_FAST             0  'self'
         670  LOAD_ATTR            51  '_scene'
         673  LOAD_ATTR            53  'get_player'
         676  CALL_FUNCTION_0       0 
         679  CALL_FUNCTION_1       1 
         682  POP_TOP          
         683  JUMP_FORWARD          0  'to 686'
       686_0  COME_FROM                '683'

 165     686  LOAD_GLOBAL          54  'hasattr'
         689  LOAD_GLOBAL          18  'visible_pic'
         692  CALL_FUNCTION_2       2 
         695  POP_JUMP_IF_FALSE   743  'to 743'

 166     698  LOAD_FAST             0  'self'
         701  LOAD_ATTR            48  'is_sound_visible_in_map'
         704  POP_JUMP_IF_FALSE   743  'to 743'
         707  LOAD_FAST             0  'self'
         710  LOAD_ATTR            14  'need_visible'
       713_0  COME_FROM                '704'
         713  POP_JUMP_IF_FALSE   743  'to 743'

 167     716  LOAD_GLOBAL           9  'global_data'
         719  LOAD_ATTR            55  'emgr'
         722  DUP_TOP          
         723  LOAD_ATTR            56  'sound_visible_add'
         726  LOAD_FAST             0  'self'
         729  LOAD_ATTR            57  'on_add_visible_elem'
         732  INPLACE_ADD      
         733  ROT_TWO          
         734  STORE_ATTR           56  'sound_visible_add'
         737  JUMP_ABSOLUTE       743  'to 743'
         740  JUMP_FORWARD          0  'to 743'
       743_0  COME_FROM                '740'

 169     743  LOAD_FAST             0  'self'
         746  LOAD_ATTR            14  'need_visible'
         749  POP_JUMP_IF_FALSE   776  'to 776'

 170     752  LOAD_GLOBAL           9  'global_data'
         755  LOAD_ATTR            55  'emgr'
         758  DUP_TOP          
         759  LOAD_ATTR            58  'player_open_sound_visible_in_map'
         762  LOAD_FAST             0  'self'
         765  LOAD_ATTR            59  'on_open_sound_visible_in_map'
         768  INPLACE_ADD      
         769  ROT_TWO          
         770  STORE_ATTR           58  'player_open_sound_visible_in_map'
         773  JUMP_FORWARD          0  'to 776'
       776_0  COME_FROM                '773'

 172     776  LOAD_GLOBAL           9  'global_data'
         779  LOAD_ATTR            55  'emgr'
         782  DUP_TOP          
         783  LOAD_ATTR            60  'scene_player_setted_event'
         786  LOAD_FAST             0  'self'
         789  LOAD_ATTR            61  'on_player_setted'
         792  INPLACE_ADD      
         793  ROT_TWO          
         794  STORE_ATTR           60  'scene_player_setted_event'

 173     797  LOAD_GLOBAL           9  'global_data'
         800  LOAD_ATTR            55  'emgr'
         803  DUP_TOP          
         804  LOAD_ATTR            62  'scene_observed_player_setted_event'
         807  LOAD_FAST             0  'self'
         810  LOAD_ATTR            63  'on_enter_observe'
         813  INPLACE_ADD      
         814  ROT_TWO          
         815  STORE_ATTR           62  'scene_observed_player_setted_event'

 174     818  LOAD_GLOBAL           9  'global_data'
         821  LOAD_ATTR            55  'emgr'
         824  DUP_TOP          
         825  LOAD_ATTR            64  'on_player_parachute_stage_changed'
         828  LOAD_FAST             0  'self'
         831  LOAD_ATTR            64  'on_player_parachute_stage_changed'
         834  INPLACE_ADD      
         835  ROT_TWO          
         836  STORE_ATTR           64  'on_player_parachute_stage_changed'

 175     839  LOAD_GLOBAL           9  'global_data'
         842  LOAD_ATTR            55  'emgr'
         845  DUP_TOP          
         846  LOAD_ATTR            65  'scene_sound_visible'
         849  LOAD_FAST             0  'self'
         852  LOAD_ATTR            66  'set_sound_visible_enable'
         855  INPLACE_ADD      
         856  ROT_TWO          
         857  STORE_ATTR           65  'scene_sound_visible'

 176     860  LOAD_GLOBAL           9  'global_data'
         863  LOAD_ATTR            55  'emgr'
         866  DUP_TOP          
         867  LOAD_ATTR            67  'cam_lplayer_gulag_state_changed'
         870  LOAD_FAST             0  'self'
         873  LOAD_ATTR            68  'on_player_gulag_state_changed'
         876  INPLACE_ADD      
         877  ROT_TWO          
         878  STORE_ATTR           67  'cam_lplayer_gulag_state_changed'
         881  LOAD_CONST            0  ''
         884  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 692

    def set_sound_visible_enable(self, flag):
        self.sound_visible_enable = flag

    def on_player_setted(self, player):
        self.player_change(player)

    def on_enter_observe(self, lplayer):
        self.player_change(lplayer)

    def on_player_parachute_stage_changed(self, stage):
        self.refresh_gulag_tip_vis(stage)

    def do_show_panel(self):
        super(SmallMapBaseUI, self).do_show_panel()
        if global_data.battle:
            self._update_alive_player_num(getattr(global_data.battle, 'alive_player_num', 0))

    def change_visible_dis(self):
        self._is_in_mecha = self._player and self._player.ev_g_in_mecha()
        self._is_ace_time = global_data.battle and global_data.battle.is_ace_time()
        if self._is_ace_time:
            self.visible_dis = self.ace_mecha_visible_dis if self._is_in_mecha else self.ace_human_visible_dis
        else:
            self.visible_dis = self.mecha_visible_dis if self._is_in_mecha else self.human_visible_dis

    def player_change(self, lplayer):
        if self._player:
            self._player.unregist_event('E_ON_JOIN_MECHA', self.on_control_target_change)
            self._player.unregist_event('E_ON_LEAVE_MECHA', self.on_control_target_change)
        if self._player != lplayer:
            for item in self._panel_items:
                item.setVisible(False)

        self._player = lplayer
        if not self._player:
            for item in self._panel_items:
                item.setVisible(False)

        else:
            self._player.regist_event('E_ON_JOIN_MECHA', self.on_control_target_change)
            self._player.regist_event('E_ON_LEAVE_MECHA', self.on_control_target_change)
            self.on_control_target_change()

    def on_control_target_change(self, *args):
        self._is_in_mecha = self._player.ev_g_in_mecha()
        self.change_visible_dis()
        self.enable_player_or_mecha = self._player.ev_g_control_target().logic if self._is_in_mecha else self._player

    def on_open_sound_visible_in_map(self, *args):
        from logic.gcommon.common_const.ui_operation_const import SOUND_VISIBLE_IN_MAP_KEY
        is_sound_visible_in_map = global_data.player.get_setting(SOUND_VISIBLE_IN_MAP_KEY)
        if self.is_sound_visible_in_map != is_sound_visible_in_map:
            if is_sound_visible_in_map:
                global_data.emgr.sound_visible_add += self.on_add_visible_elem
            else:
                global_data.emgr.sound_visible_add -= self.on_add_visible_elem
        self.is_sound_visible_in_map = is_sound_visible_in_map

    def on_add_visible_elem(self, entity, pos, sound_type, distance_sqr, driver_id=None):
        if not self.sound_visible_enable:
            return
        if not global_data.cam_lplayer:
            return
        listen_factor = global_data.cam_lplayer.ev_g_add_attr(attr_const.ATTR_LISTEN_RANGE_FACTOR)
        listen_dis = self.visible_dis[sound_type][-1] * (1 + listen_factor) ** 2
        if distance_sqr > listen_dis:
            return
        if global_data.cam_lplayer.ev_g_is_campmate(entity.ev_g_camp_id()):
            return
        if self._is_in_mecha and not self._is_ace_time and (sound_type == SOUND_TYPE_FOOTSTEP or sound_type == SOUND_TYPE_SLOW_FOOTSTEP):
            return
        if not self.enable_player_or_mecha:
            return
        is_refresh = False
        player_pos = self.enable_player_or_mecha.ev_g_model_position()
        if not player_pos:
            return
        if not self.visible_pic[sound_type]:
            return
        length_sqr = (pos - player_pos).length_sqr
        weight = self.get_weight(sound_type, length_sqr)
        if entity not in self._show_entity:
            if len(self._show_entity) > self.max_visible_item_count:
                min_entity, min_weight = self.get_min_weight_entity()
                if weight < min_weight:
                    return
                del self._show_entity[min_entity]
                self._is_remove_old_entity = True
            self._show_entity[entity] = {'pos': pos,'weight': weight,'length_sqr': length_sqr,'type_dic': defaultdict(int),'time_index': self._time_index}
            is_refresh = True
            self._add_entity.append(entity)
        entity_inf = self._show_entity[entity]
        if entity_inf['pos'] != pos:
            entity_inf['pos'] = pos
            is_refresh = True
        type_dic = entity_inf['type_dic']
        if type_dic[sound_type] == 0:
            is_refresh = True
        elif type_dic[sound_type] >= ITEM_CACHE_MAX_COUNT:
            return
        type_dic[sound_type] += 1
        if entity_inf['length_sqr'] != length_sqr:
            entity_inf['length_sqr'] = length_sqr
            is_refresh = True
        game3d.delay_exec(SHOW_LAST_TIME, self.del_visible_elem, (entity, sound_type, self._time_index))
        if is_refresh:
            self.refresh_visible()
        self._time_index += 1

    def del_visible_elem(self, entity, sound_type, time_index):
        if entity in self._show_entity:
            entity_inf = self._show_entity[entity]
            if entity_inf['time_index'] > time_index:
                return
            type_dic = entity_inf['type_dic']
            type_dic[sound_type] -= 1
            if not self.is_elment_enable(type_dic):
                del self._show_entity[entity]
                self._is_remove_old_entity = True
            if type_dic[sound_type] <= 0 and self._is_run:
                self.refresh_visible()

    def del_visible_elem_ex(self, entity):
        if entity in self._show_entity:
            del self._show_entity[entity]
            self._is_remove_old_entity = True

    def is_elment_enable(self, type_dic):
        for sound_type, value in six.iteritems(type_dic):
            if value > 0:
                return True

        return False

    def refresh_visible(self):
        if not self.enable_player_or_mecha:
            return
        else:
            if self._is_remove_old_entity:
                for item in self._panel_items:
                    if item.isVisible():
                        if item.entity not in self._show_entity:
                            item.setVisible(False)
                            item.entity = None

                self._is_remove_old_entity = False
            if self._add_entity:
                for entity in self._add_entity:
                    panel_item = self.get_disable_panel_item()
                    if panel_item:
                        panel_item.entity = entity
                        panel_item.setVisible(True)
                        entity_inf = self._show_entity[panel_item.entity]
                        sound_type = self.get_best_sound_type(entity_inf['type_dic'])
                        panel_item.SetDisplayFrameByPath('', self.visible_pic[sound_type])

                self._add_entity = []
            player_pos = self.enable_player_or_mecha.ev_g_model_position()
            if player_pos is None:
                return
            save_panel_item_dict = {}
            for panel_item in self._panel_items:
                if panel_item.isVisible():
                    entity = panel_item.entity
                    entity_inf = self._show_entity[entity]
                    vect = entity_inf['pos'] - player_pos
                    entity_length_sqr = vect.length_sqr
                    sound_type = self.get_best_sound_type(entity_inf['type_dic'])
                    angle = common.utilities.vector_radian(vect) * R_A_RATE
                    panel_item.setRotation(angle)
                    opacity_index = 0
                    distance_list = self.visible_dis[sound_type]
                    for i in range(len(distance_list)):
                        listen_factor = global_data.cam_lplayer.ev_g_add_attr(attr_const.ATTR_LISTEN_RANGE_FACTOR)
                        if entity_length_sqr < distance_list[i] * (1 + listen_factor) ** 2:
                            opacity_index = i
                            break
                    else:
                        opacity_index = len(distance_list) - 1

                    opacity = self.visible_opacity[sound_type][opacity_index] * 255 // 100
                    panel_item.setOpacity(opacity)
                    panel_item.SetDisplayFrameByPath('', self.visible_pic[sound_type])
                    del_flag = True
                    if save_panel_item_dict:
                        del_entity = []
                        del_save_panel_item = []
                        for save_panel_item, save_item_angle in six.iteritems(save_panel_item_dict):
                            if abs(angle - save_item_angle) < self.visible_item_min_angle:
                                if entity_inf['weight'] > self._show_entity[save_panel_item.entity]['weight']:
                                    save_panel_item.setOpacity(0)
                                    save_panel_item.setVisible(False)
                                    del_entity.append(save_panel_item.entity)
                                    del_save_panel_item.append(save_panel_item)
                                else:
                                    panel_item.setOpacity(0)
                                    panel_item.setVisible(False)
                                    del_entity.append(entity)
                                    del_flag = False

                        for entity in del_entity:
                            self.del_visible_elem_ex(entity)

                        for save_panel in del_save_panel_item:
                            if save_panel in save_panel_item_dict:
                                del save_panel_item_dict[save_panel]

                    if del_flag:
                        save_panel_item_dict[panel_item] = angle

            return

    def get_min_weight_entity(self):
        min_entity = None
        min_weight = 0
        for entity, entity_inf in six.iteritems(self._show_entity):
            if min_entity == None:
                min_entity = entity
                min_weight = entity_inf['weight']
            elif min_weight > entity_inf['weight']:
                min_entity = entity
                min_weight = entity_inf['weight']

        return (
         min_entity, min_weight)

    def get_disable_panel_item(self):
        for item in self._panel_items:
            if not item.isVisible():
                return item

        return None

    def get_best_sound_type(self, type_dic):
        best_weight = 0
        best_type = 0
        for sound_type, value in six.iteritems(type_dic):
            if value > 0:
                weight = self.visible_weight[sound_type]
                if best_weight == 0:
                    best_weight = weight
                    best_type = sound_type
                elif weight > best_weight:
                    best_weight = weight
                    best_type = sound_type

        return best_type

    def get_weight(self, sound_type, length_sqr):
        weight_rate = self.visible_weight[sound_type]
        if length_sqr == 0.0:
            weight = weight_rate
        else:
            weight = weight_rate / length_sqr
        return weight

    def init_widget(self):
        pass

    def init_br_circle_state(self):
        pass

    def init_player_widget(self):
        from logic.comsys.map.map_widget.MapPlayerInfoWidget import MapPlayerInfoWidget
        self.player_info_widget = MapPlayerInfoWidget(self, self.map_nd.nd_scale_up, inc_mini_map_mark=True)
        self.player_info_widget.set_follow_player_enable(True)
        self.player_info_widget.set_view_range((self.view_dist / 2.0, self.view_dist / 2.0))

    def init_parameters(self, **kwargs):
        if global_data.game_mode.is_mode_type(game_mode_const.Custom_MapViewRange):
            MAP_VIEW_RANGE = DEATH_MODE_VIEW_RANGE
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DEATH, game_mode_const.GAME_MODE_SNATCHEGG, game_mode_const.GAME_MODE_FLAG, game_mode_const.GAME_MODE_CROWN, game_mode_const.GAME_MODE_RANDOM_DEATH, game_mode_const.GAME_MODE_FLAG2)) and global_data.player.get_setting(uoc.SMALL_MAP_ROTATE):
                MAP_VIEW_RANGE = 200
            elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_MUTIOCCUPY,)):
                MAP_VIEW_RANGE = 200
            elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GOOSE_BEAR,)):
                MAP_VIEW_RANGE = 100
        else:
            MAP_VIEW_RANGE = 400
        dist = self.get_world_distance_in_map(MAP_VIEW_RANGE)
        self.view_dist = dist
        scale = self.calc_map_show_scale(dist, dist)
        kwargs['scale'] = scale
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})
        super(SmallMapBaseUI, self).init_parameters(**kwargs)
        self.map_nd.nd_name.setVisible(False)
        nd_name_json = None
        if getattr(self.map_nd.nd_scale_up_details, 'nd_name_json'):
            nd_name_json = self.map_nd.nd_scale_up_details.nd_name_json
            nd_name_json.setVisible(False)
        if global_data.ui_mgr.get_ui('BigMapUI'):
            self.add_hide_count('BigMapUI')
        return

    def init_paradrop_widget(self):
        from logic.comsys.map.map_widget.MapParadropMarkWidget import MapParadropMarkWidget
        self.paradrop_widget = MapParadropMarkWidget(self, self.map_nd.nd_scale_up_details, (self.map_nd.GetContentSize(), self.view_dist / 2))
        global_data.map = self.sv_map

    def _on_enter_observe(self, player):
        self._spectate_target = player

    def _update_alive_player_num(self, player_num):
        if not battle_utils.is_signal_logic():
            return
        is_in_spectate = False
        if global_data.player and global_data.player.logic:
            is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
        is_mode_survivals = global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS)
        if player_num == 5 and not is_in_spectate and is_mode_survivals:

            def close_cb(*args):
                self.destroy_widget('_top_five_widget')

            if not self._top_five_widget:
                from .map_widget.TopFiveWidget import TopFiveWidget
                nd = global_data.uisystem.load_template_create('battle_tips/common_tips/fight_top5_tips', self.panel.temp_top5)
                self._top_five_widget = TopFiveWidget(self, nd, close_cb)

    def init_enemy_widget(self):
        from logic.comsys.map.map_widget.MapEnemyInfoWidget import MapEnemyInfoWidget
        self.enemy_widget = MapEnemyInfoWidget(self, self.map_nd.nd_scale_up_details, (self.map_nd.GetContentSize(), self.view_dist / 2))

    def on_finalize_panel(self):
        self._is_run = False
        global_data.emgr.sound_visible_add -= self.on_add_visible_elem
        if self.need_visible:
            global_data.emgr.player_open_sound_visible_in_map -= self.on_open_sound_visible_in_map
        global_data.emgr.scene_player_setted_event -= self.on_player_setted
        global_data.emgr.scene_observed_player_setted_event -= self.on_enter_observe
        global_data.emgr.on_player_parachute_stage_changed -= self.on_player_parachute_stage_changed
        global_data.emgr.scene_sound_visible -= self.set_sound_visible_enable
        global_data.emgr.cam_lplayer_gulag_state_changed -= self.on_player_gulag_state_changed
        self.panel.stopAllActions()
        self.panel.poison.stopAllActions()
        self.panel.time.StopTimerAction()
        self.destroy_widget('circle_state_widget')
        self.destroy_widget('custom_ui_com')
        self.destroy_widget('paradrop_widget')
        self.destroy_widget('survive_widget')
        self.destroy_widget('beacon_tower_widget')
        self.destroy_widget('voice_tip_widget')
        self.destroy_widget('_top_five_widget')
        global_data.ui_mgr.close_ui('MapGuideUI')
        super(SmallMapBaseUI, self).on_finalize_panel()

    def init_event(self):
        super(SmallMapBaseUI, self).init_event()
        global_data.emgr.switch_control_target_event += self.on_ctrl_target_changed

    @execute_by_mode(False, game_mode_const.Cannot_ClickMapLayer)
    def onclick_map_layer(self, btn, touch):
        global_data.emgr.scene_show_big_map_event.emit()

    def on_enter_observe(self, target):
        super(SmallMapBaseUI, self).on_enter_observe(target)

    def update_alive_player_num(self, player_num):
        pass

    def check_hide_br_poison_progress(self):
        pass

    def on_camera_player_setted(self):
        pass

    def on_into_mecha_state(self):
        UIDistorterHelper().apply_ui_distort(self.__class__.__name__)
        self.in_mecha_state = True

    def on_into_human_state(self):
        UIDistorterHelper().cancel_ui_distort(self.__class__.__name__)
        self.in_mecha_state = False

    def on_switch_map_state(self, state):
        self.on_into_human_state() if state == const.MAP_STATE_HUMAN else self.on_into_mecha_state()

    def on_ctrl_target_changed(self, *args):
        if not global_data.cam_lplayer:
            return
        state = const.MAP_STATE_MECHA if global_data.cam_lplayer.ev_g_in_mecha('Mecha') else const.MAP_STATE_HUMAN
        self.on_switch_map_state(state)

    def on_change_ui_custom_data(self):
        if self.in_mecha_state:
            UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def init_voice_tip(self):
        battle = global_data.battle
        if not battle or not battle.is_single_person_battle():
            return
        from logic.comsys.common_ui.CommonTips import TipsManager
        from logic.comsys.chat.FightChatUI import FightChatTips
        self.voice_tip_widget = TipsManager(self.temp_teammate_message, FightChatTips, preload_tip_num=2)
        global_data.emgr.add_battle_group_msg_event += self.show_voice_tip

    def show_voice_tip(self, eid, name, tips_data):
        if 'msg' not in tips_data:
            return
        msg_dict = tips_data['msg']
        if not isinstance(msg_dict, dict):
            return
        if 'text' in msg_dict:
            self.voice_tip_widget.add_tips(msg_dict)
        voice_trigger_type = msg_dict.get('voice_trigger_type')
        if voice_trigger_type:
            global_data.game_voice_mgr.play_game_voice(voice_trigger_type)

    @execute_by_mode(True, game_mode_const.GAME_MODE_SURVIVALS)
    def update_ace_state(self):
        battle = global_data.battle
        if not battle:
            return
        self.panel.nd_ace_tiem.setVisible(battle.is_in_ace_state)

    def keyboard_switch_big_map(self, msg, keycode):
        if global_data.ui_mgr.get_ui('BigMapUI'):
            return
        else:
            self.onclick_map_layer(None, None)
            return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_MAGIC_SURVIVAL,))
    def on_update_magic_region_timestamp(self, timestamp):
        end_time = timestamp - time_utility.time()
        if end_time < 0:
            return
        left_time = int(end_time)
        content = get_text_by_id(17869, (str(left_time),))
        self.panel.nd_moon_tips.lab_tips.SetString(content)
        self.panel.nd_moon_tips.setVisible(True)
        global_data.emgr.move_survive_info_ui_event.emit(True, self.panel.nd_moon_tips.getContentSize().height)

        def update_time(pass_time):
            left_time = int(end_time - pass_time)
            content = get_text_by_id(17869, (str(left_time),))
            self.panel.nd_moon_tips.lab_tips.SetString(content)

        def timer_end():
            self.panel.nd_moon_tips.setVisible(False)
            global_data.emgr.move_survive_info_ui_event.emit(False, self.panel.nd_moon_tips.getContentSize().height)

        self.panel.nd_moon_tips.StopTimerAction()
        self.panel.nd_moon_tips.TimerAction(update_time, end_time, callback=timer_end, interval=1.0)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GRANBELM_SURVIVAL, game_mode_const.GAME_MODE_GRANHACK_SURVIVAL))
    def on_update_rune_region_timestamp(self, timestamp, show_tip):
        end_time = timestamp - time_utility.time()
        if end_time < 0:
            return
        left_time = int(end_time)
        if global_data.gran_sur_battle_mgr.is_sub_mode:
            content = get_text_by_id(19807).format(n=str(left_time))
        else:
            content = get_text_by_id(19709).format(n=str(left_time))
        self.panel.nd_moon_tips.lab_tips.SetString(content)
        self.panel.nd_moon_tips.setVisible(True)
        global_data.emgr.move_survive_info_ui_event.emit(True, self.panel.nd_moon_tips.getContentSize().height)

        def update_time(pass_time):
            left_time = int(end_time - pass_time)
            if global_data.gran_sur_battle_mgr.is_sub_mode:
                content = get_text_by_id(19807).format(n=str(left_time))
            else:
                content = get_text_by_id(19709).format(n=str(left_time))
            self.panel.nd_moon_tips.lab_tips.SetString(content)

        def timer_end():
            self.panel.nd_moon_tips.setVisible(False)
            global_data.emgr.move_survive_info_ui_event.emit(False, self.panel.nd_moon_tips.getContentSize().height)
            if show_tip:
                global_data.emgr.on_region_show_tips.emit()

        self.panel.nd_moon_tips.StopTimerAction()
        self.panel.nd_moon_tips.TimerAction(update_time, end_time, callback=timer_end, interval=1.0)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GRAVITY_SURVIVAL, game_mode_const.GAME_MODE_GOOSE_BEAR))
    def on_update_gravity_region_timestamp(self, timestamp, show_tip):
        end_time = timestamp - time_utility.time()
        if end_time < 0:
            return
        left_time = int(end_time)
        content = get_text_by_id(19880).format(n=str(left_time))
        self.panel.nd_moon_tips.lab_tips.SetString(content)
        self.panel.nd_moon_tips.setVisible(True)
        global_data.emgr.move_survive_info_ui_event.emit(True, self.panel.nd_moon_tips.getContentSize().height)

        def update_time(pass_time):
            left_time = int(end_time - pass_time)
            content = get_text_by_id(19880).format(n=str(left_time))
            self.panel.nd_moon_tips.lab_tips.SetString(content)

        def timer_end--- This code section failed: ---

 789       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'nd_moon_tips'
           9  LOAD_ATTR             2  'setVisible'
          12  LOAD_GLOBAL           3  'False'
          15  CALL_FUNCTION_1       1 
          18  POP_TOP          

 790      19  LOAD_GLOBAL           4  'global_data'
          22  LOAD_ATTR             5  'emgr'
          25  LOAD_ATTR             6  'move_survive_info_ui_event'
          28  LOAD_ATTR             7  'emit'
          31  LOAD_GLOBAL           3  'False'
          34  LOAD_DEREF            0  'self'
          37  LOAD_ATTR             0  'panel'
          40  LOAD_ATTR             1  'nd_moon_tips'
          43  LOAD_ATTR             8  'getContentSize'
          46  CALL_FUNCTION_0       0 
          49  LOAD_ATTR             9  'height'
          52  CALL_FUNCTION_2       2 
          55  POP_TOP          

 791      56  LOAD_DEREF            1  'show_tip'
          59  POP_JUMP_IF_FALSE   138  'to 138'

 792      62  LOAD_CONST            1  ''
          65  LOAD_CONST            2  ('GRANBELM_PORTAL_REFRESH_TIPS', 'MAIN_NODE_COMMON_INFO')
          68  IMPORT_NAME          10  'logic.gcommon.common_const.battle_const'
          71  IMPORT_FROM          11  'GRANBELM_PORTAL_REFRESH_TIPS'
          74  STORE_FAST            0  'GRANBELM_PORTAL_REFRESH_TIPS'
          77  IMPORT_FROM          12  'MAIN_NODE_COMMON_INFO'
          80  STORE_FAST            1  'MAIN_NODE_COMMON_INFO'
          83  POP_TOP          

 793      84  BUILD_MAP_2           2 
          87  BUILD_MAP_3           3 
          90  STORE_MAP        
          91  LOAD_CONST            4  19882
          94  LOAD_CONST            5  'content_txt'
          97  STORE_MAP        
          98  STORE_FAST            2  'message'

 794     101  LOAD_FAST             1  'MAIN_NODE_COMMON_INFO'
         104  STORE_FAST            3  'message_type'

 795     107  LOAD_GLOBAL           4  'global_data'
         110  LOAD_ATTR             5  'emgr'
         113  LOAD_ATTR            13  'show_battle_main_message'
         116  LOAD_ATTR             7  'emit'
         119  LOAD_FAST             2  'message'
         122  LOAD_FAST             3  'message_type'
         125  LOAD_GLOBAL          14  'True'
         128  LOAD_GLOBAL           3  'False'
         131  CALL_FUNCTION_4       4 
         134  POP_TOP          
         135  JUMP_FORWARD          0  'to 138'
       138_0  COME_FROM                '135'

Parse error at or near `STORE_MAP' instruction at offset 90

        self.panel.nd_moon_tips.StopTimerAction()
        self.panel.nd_moon_tips.TimerAction(update_time, end_time, callback=timer_end, interval=1.0)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GULAG_SURVIVAL,))
    def on_update_can_revive(self, can_revive, is_canceled, **kwargs):
        from logic.gcommon.common_const.battle_const import ST_IDLE
        item = self._tips_dict.get('gulag_can_revive', None)
        if not item:
            item = global_data.uisystem.load_template_create('battle_gulade/i_gulag_revive_times', parent=self.panel.nd_mode_tip, name='gulag_revive_times')
            if global_data.is_pc_mode:
                si_ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
                if si_ui and si_ui.panel.list_pc:
                    now_pos = si_ui.panel.list_pc.getPosition()
                    si_ui.panel.list_pc.SetPosition(now_pos.x, now_pos.y - item.getContentSize().height)
            else:
                global_data.emgr.move_survive_info_ui_event.emit(True, item.getContentSize().height)
            self._tips_dict['gulag_can_revive'] = item
            self.panel.nd_mode_tip.setVisible(True)
        revive_coin = 0
        if global_data.cam_lplayer:
            revive_coin = global_data.cam_lplayer.ev_g_item_count(ITEM_GULOG_REVIVE_COIN)
            is_canceled = global_data.battle and getattr(global_data.battle, 'gulag_canceled', False) or is_canceled
        free_revive = 1 if can_revive else 0
        revive_count = 0 if is_canceled else revive_coin + free_revive
        item.lab_times.SetString(get_text_by_id(17980, (revive_count,)))
        return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GULAG_SURVIVAL,))
    def refresh_gulag_tip_vis(self, stage):
        from logic.gcommon.common_utils.parachute_utils import STAGE_LAND
        self.panel.nd_mode_tip.setVisible(stage == STAGE_LAND)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_BOUNTY_SURVIVAL,))
    def on_update_bounty_region_timestamp(self, timestamp, show_type):
        item = self._tips_dict.get(show_type, None)
        if not item:
            item = self.panel.list_tips.AddTemplateItem()
            global_data.emgr.move_survive_info_ui_event.emit(True, item.getContentSize().height)
            self._tips_dict[show_type] = item

        def timer_end(item=item):
            global_data.emgr.move_survive_info_ui_event.emit(False, item.getContentSize().height)
            self._tips_dict[show_type] = None
            self.panel.list_tips.DeleteItem(item)
            if self.panel.list_tips.GetItemCount() == 0:
                self.panel.list_tips.setVisible(False)
            return

        end_time = int(timestamp - time_utility.time())
        if timestamp <= 0 or end_time < 0:
            timer_end()
            return
        else:
            if show_type == bounty_mode_utils.PREY_TYPE:
                text_1 = get_text_by_id(19895)
                text_2 = get_text_by_id(19896)
            else:
                text_1 = get_text_by_id(19893)
                text_2 = get_text_by_id(19894)
                item.pnl_bounty.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/bounty/pnl_battle_tips_bounty2.png')
            self.panel.list_tips.setVisible(True)

            def update_time(pass_time, item=item):
                left_second = int(end_time - pass_time) % 60
                left_min = int(end_time - pass_time) // 60
                if left_min == 0:
                    content = text_2.format(left_second)
                else:
                    content = text_1.format(left_min, left_second)
                item.lab_time.SetString(content)

            update_time(0)
            item.StopTimerAction()
            item.TimerAction(update_time, end_time, callback=timer_end, interval=1.0)
            return

    def on_get_hint_wpos(self):
        pass

    def on_update_enable_touch(self):
        pass

    def _update_judge_need_hide_details(self):
        if global_data.judge_need_hide_details:
            self.add_hide_count('JUDEG_DETAIL')
        else:
            self.add_show_count('JUDEG_DETAIL')

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def init_widget_scale_btns(self):
        dist = self.view_dist
        scale = self.calc_map_show_scale(dist, dist)
        self._show_big_scale = scale
        self._show_small_scale = scale / 2.0
        self.set_map_scale(self._show_big_scale)
        self.map_info_widget.lab_switch.SetString(8104)

        @self.map_info_widget.btn_switch.callback()
        def OnClick(btn, touch):
            self.switch_map_mode()

        @self.panel.layer_swipe.callback()
        def OnEnd(btn, touch):
            self.on_swipe(btn, touch)

        @self.panel.layer_swipe.callback()
        def OnBegin(btn, touch):
            return True

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def switch_map_mode(self):
        if abs(self.cur_map_scale - self._show_big_scale) < 0.01:
            self.set_map_scale(self._show_small_scale)
            self.map_info_widget.lab_switch.SetString(8103)
            self.map_nd.nd_scale_up_details.setVisible(False)
        else:
            self.set_map_scale(self._show_big_scale)
            self.map_info_widget.lab_switch.SetString(8104)
            self.map_nd.nd_scale_up_details.setVisible(True)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def init_guide_ui(self):
        from .MapGuideUI import MapGuideUI
        MapGuideUI()
        self.panel.SetTimeOut(10.0, lambda : global_data.ui_mgr.close_ui('MapGuideUI'))

    def on_swipe(self, btn, touch):
        if btn.GetMovedDistance() > get_scale('30w'):
            self.switch_map_mode()
            global_data.ui_mgr.close_ui('MapGuideUI')

    def get_player_info_widget(self):
        return self.player_info_widget

    def on_player_gulag_state_changed(self, gulag_state, **kwargs):
        from logic.gcommon.common_const.battle_const import ST_IDLE
        if gulag_state == ST_IDLE:
            self.add_show_count('gulag')
        else:
            self.add_hide_count('gulag')


class SmallMapUI(SmallMapBaseUI):
    PANEL_CONFIG_NAME = 'map/map_small'

    def init_widget(self):
        super(SmallMapUI, self).init_widget()
        if scene_utils.is_circle_poison():
            self.init_br_circle_state()
        self.init_map_info_widget()
        self.init_survive_widget()
        self.init_paradrop_widget()
        self.panel.map_layer.set_sound_enable(False)
        self.init_guide_ui()
        self.init_voice_tip()
        self.check_hide_br_poison_progress()
        self.update_ace_state()

    def init_br_circle_state(self):
        from logic.comsys.map.map_widget.SmallMapCircleStateWidget import SmallMapCircleStateWidget
        self.circle_state_widget = SmallMapCircleStateWidget(self)

    def init_map_info_widget(self):
        template_path = 'map/i_map_info_nml'
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_KING):
            template_path = 'map/i_map_info_koth'
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_MUTIOCCUPY, game_mode_const.GAME_MODE_FLAG,
         game_mode_const.GAME_MODE_DEATH, game_mode_const.GAME_MODE_SNIPE,
         game_mode_const.GAME_MODE_CLONE,
         game_mode_const.GAME_MODE_RANDOM_DEATH,
         game_mode_const.GAME_MODE_CONTROL, game_mode_const.GAME_MODE_CROWN,
         game_mode_const.GAME_MODE_CRYSTAL, game_mode_const.GAME_MODE_ADCRYSTAL,
         game_mode_const.GAME_MODE_TRAIN, game_mode_const.GAME_MODE_FLAG2,
         game_mode_const.GAME_MODE_SNATCHEGG, game_mode_const.GAME_MODE_IMPROVISE,
         game_mode_const.GAME_MODE_ARMRACE, game_mode_const.GAME_MODE_ASSAULT)):
            template_path = 'map/i_map_info_tdm'
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_FFA, game_mode_const.GAME_MODE_ZOMBIE_FFA)):
            template_path = 'map/i_map_info_ffa'
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_DUEL, game_mode_const.GAME_MODE_GOOSE_BEAR)):
            template_path = 'map/i_map_info_gvg'
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_HUMAN_DEATH, game_mode_const.GAME_MODE_SCAVENGE)):
            template_path = 'map/i_map_info_htdm'
        self.map_info_widget = global_data.uisystem.load_template_create(template_path, self.panel.nd_info_1)
        self.init_widget_scale_btns()

    def init_survive_widget(self):
        global_data.emgr.update_map_info_widget_event += self.update_alive_player_num
        global_data.emgr.scene_camera_player_setted_event += self.on_camera_player_setted
        from logic.comsys.battle.BattleInfo.SurviveWidget import SurviveWidget
        self.on_camera_player_setted()
        self.survive_widget = SurviveWidget(self.on_kill_num_change, self.on_kill_mecha_num_change, self.assist_mecha_num_change, self.assist_human_num_change)

    def on_kill_num_change(self, my_kill_num):
        if not self.map_info_widget.my_kill_num:
            return
        self.map_info_widget.my_kill_num.SetString(str(my_kill_num))

    def on_kill_mecha_num_change(self, kill_mecha_num):
        if not self.map_info_widget.my_mech_num:
            return
        else:
            self.map_info_widget.my_mech_num.SetString(str(kill_mecha_num))
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                kill_mecha_voice = {5: '101_star_01',10: '101_star_02'}
                for num, voice in six.iteritems(kill_mecha_voice):
                    if (self.cur_kill_mecha_num is None or self.cur_kill_mecha_num < num) and kill_mecha_num == num:
                        global_data.emgr.play_anchor_voice.emit(voice)
                        break

            self.cur_kill_mecha_num = kill_mecha_num
            return

    def assist_mecha_num_change(self, assist_mecha_num):
        if not self.map_info_widget.my_assist_num:
            return
        self.map_info_widget.my_assist_num.SetString(str(assist_mecha_num))

    def assist_human_num_change(self, assist_human_num):
        if not self.map_info_widget.my_assist_human_num:
            return
        self.map_info_widget.my_assist_human_num.SetString(str(assist_human_num))

    @execute_by_mode(False, game_mode_const.Hide_AlivePlayerNum)
    def update_alive_player_num(self, player_num):
        WARNING_ALIVE_NUM = 5
        WARNING_ALINE_NUM_BIG = 20
        if self.panel:
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                if player_num > 100:
                    player_num = 100
                survive_num_voice = {50: '101_remain_01',20: '101_remain_02',10: '101_remain_03',3: '101_remain_04',2: '101_remain_05'}
                for num, voice in six.iteritems(survive_num_voice):
                    if player_num == num and self.cur_survive_num and player_num < self.cur_survive_num:
                        global_data.emgr.play_anchor_voice.emit(voice)
                        break

            self.cur_survive_num = player_num
            self.map_info_widget.survive_num.setString(str(player_num))
            if not global_data.player:
                return
            battle = global_data.player.get_battle()
            if battle and not battle.is_battle_prepare_stage():
                if player_num < WARNING_ALIVE_NUM:
                    self.map_info_widget.survive_num.SetColor('#SR')
                    self.panel.StopAnimation('survive_change')
                    self.panel.PlayAnimation('survive_change')
                elif player_num <= WARNING_ALINE_NUM_BIG:
                    self.map_info_widget.survive_num.SetColor('#SR')
                else:
                    self.map_info_widget.survive_num.SetColor('#SK')

    @execute_by_mode(True, game_mode_const.Hide_MapPoisonProgress)
    def check_hide_br_poison_progress(self):
        old_size = self.panel.img_frame.GetContentSize()
        self.panel.img_frame.SetContentSize(old_size[0], 218)
        self.panel.poison.setVisible(False)

    def on_camera_player_setted(self):
        if global_data.player and global_data.player.get_battle():
            self.update_alive_player_num(global_data.player.get_battle().alive_player_num)
        self.on_ctrl_target_changed()

    def on_get_hint_wpos(self):
        return self.panel.temp_hint.ConvertToWorldSpacePercentage(0, 100)

    def on_update_enable_touch(self):
        self.panel.nd_test.SetEnableTouch(not self.panel.nd_test.GetEnableTouch())

    def change_ui_data(self):
        nd = getattr(self.panel, 'nd_custom')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, scale, 'temp_map_tips')


class SmallMapUIPC(SmallMapBaseUI):
    PANEL_CONFIG_NAME = 'map/map_small_pc'

    def init_widget(self):
        super(SmallMapUIPC, self).init_widget()
        if scene_utils.is_circle_poison():
            self.init_br_circle_state()
        self.init_survive_widget()
        self.on_camera_player_setted()
        self.init_paradrop_widget()
        self.panel.map_layer.set_sound_enable(False)
        self.init_voice_tip()
        self.check_hide_br_poison_progress()
        self.update_ace_state()

    @execute_by_mode(False, (game_mode_const.GAME_MODE_SNATCHEGG,))
    def init_survive_widget(self):
        FightKillNumberUI()

    def init_br_circle_state(self):
        from logic.comsys.map.map_widget.SmallMapCircleStateWidget import SmallMapCircleStateWidgetPC
        self.circle_state_widget = SmallMapCircleStateWidgetPC(self)

    @execute_by_mode(True, game_mode_const.Hide_MapPoisonProgress)
    def check_hide_br_poison_progress(self):
        old_size = self.panel.img_frame.GetContentSize()
        self.panel.img_frame.SetContentSize(old_size[0], 185)
        self.panel.poison.setVisible(False)
        self.panel.nd_time.setVisible(False)

    def on_camera_player_setted(self):
        self.on_ctrl_target_changed()

    def on_get_hint_wpos(self):
        return self.panel.temp_hint.ConvertToWorldSpacePercentage(0, 100)

    def on_update_enable_touch(self):
        self.panel.nd_test.SetEnableTouch(not self.panel.nd_test.GetEnableTouch())

    def init_voice_tip(self):
        battle = global_data.battle
        if not battle or not battle.is_single_person_battle():
            return
        from logic.comsys.common_ui.CommonTips import TipsManager
        from logic.comsys.chat.FightChatUI import FightChatTipsPC
        self.voice_tip_widget = TipsManager(self.temp_teammate_message, FightChatTipsPC, preload_tip_num=2)
        global_data.emgr.add_battle_group_msg_event += self.show_voice_tip