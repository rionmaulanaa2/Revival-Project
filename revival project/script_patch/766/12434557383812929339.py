# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWater.py
from __future__ import absolute_import
from __future__ import print_function
from functools import cmp_to_key
from ..UnitCom import UnitCom
import math3d
import collision
from logic.gcommon.common_const import water_const, scene_const
import time
import world
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK, TERRAIN_GROUP, GROUP_CHARACTER_INCLUDE, STONE_GROUP, ROAD_GROUP, GROUP_STATIC_SHOOTUNIT, GROUP_DYNAMIC_SHOOTUNIT
import weakref
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComWater(UnitCom):
    BIND_EVENT = {'G_WATER_HEIGHT': '_get_water_height',
       'G_WATER_DIFF_HEIGHT': '_get_water_diff_height',
       'E_ENABLE_WATER_UPDATE': '_enable_update',
       'G_IS_WATER_DEPTH_OVER': '_is_water_depth_over',
       'G_LAST_MATERIAL': 'get_last_material_index',
       'E_FORCE_CHECK_WATER': 'force_check_water',
       'E_REFRESH_CUR_WATER_STATUS': '_refresh_cur_water_status',
       'G_IS_IN_WATER_AREA': '_is_in_water'
       }
    MIN_CHECK_TIME = 0.1
    MIN_CHANGE_STATUS_TIME = 0.2
    DEFAULT_WATER_HEIGHT = -99999

    def __init__(self):
        super(ComWater, self).__init__()
        self.need_update = False
        self.sd.ref_water_status = None
        self.is_first = True
        self.last_check = 0
        self.last_water_height = self.DEFAULT_WATER_HEIGHT
        self.last_status_check = 0
        self.last_diff_height = 0
        self.water_diff = 0
        self.last_material = None
        self._is_in_water_area = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComWater, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        if not self.need_update and self.ev_g_model():
            self.need_update = True

    def _enable_update(self, value):
        self.need_update = value

    def _is_in_water(self):
        return self._is_in_water_area

    def get_last_material_index(self):
        return self.last_material

    def _get_water_height(self):
        return self.last_water_height

    def _get_water_diff_height(self):
        return self.water_diff

    def _is_water_depth_over(self, depth):
        return depth < self.water_diff

    def _set_water_diff_height(self, diff_height):
        change = diff_height != self.water_diff
        self.water_diff = diff_height
        if change:
            self.on_water_depth_change(diff_height)

    def get_pos(self):
        return self.ev_g_position()

    def check_material_index(self, material):
        return material

    def change_status(self, last_status, water_height=None, water_depth=0):
        self.last_water_height = water_height or self.DEFAULT_WATER_HEIGHT

    def on_water_depth_change(self, diff_height):
        pass

    def on_check_fly_failed(self, pos_y, water_y):
        return False

    def force_check_water(self):
        self.tick(0)

    def tick--- This code section failed: ---

 107       0  LOAD_GLOBAL           0  'time'
           3  LOAD_ATTR             0  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  'now'

 108      12  LOAD_FAST             2  'now'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'last_check'
          21  BINARY_SUBTRACT  
          22  STORE_FAST            3  'diff_time'

 109      25  LOAD_FAST             2  'now'
          28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             2  'last_status_check'
          34  BINARY_SUBTRACT  
          35  STORE_FAST            4  'diff_status_time'

 110      38  LOAD_GLOBAL           3  'True'
          41  STORE_FAST            5  'can_change_status'

 111      44  LOAD_FAST             3  'diff_time'
          47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             4  'MIN_CHECK_TIME'
          53  COMPARE_OP            1  '<='
          56  POP_JUMP_IF_FALSE    63  'to 63'

 112      59  LOAD_CONST            0  ''
          62  RETURN_END_IF    
        63_0  COME_FROM                '56'

 113      63  LOAD_FAST             4  'diff_status_time'
          66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             5  'MIN_CHANGE_STATUS_TIME'
          72  COMPARE_OP            1  '<='
          75  POP_JUMP_IF_FALSE    87  'to 87'

 114      78  LOAD_GLOBAL           6  'False'
          81  STORE_FAST            5  'can_change_status'
          84  JUMP_FORWARD          9  'to 96'

 116      87  LOAD_FAST             2  'now'
          90  LOAD_FAST             0  'self'
          93  STORE_ATTR            2  'last_status_check'
        96_0  COME_FROM                '84'

 118      96  LOAD_FAST             2  'now'
          99  LOAD_FAST             0  'self'
         102  STORE_ATTR            1  'last_check'

 119     105  LOAD_FAST             0  'self'
         108  LOAD_ATTR             7  'scene'
         111  STORE_FAST            6  'scn'

 121     114  LOAD_FAST             6  'scn'
         117  POP_JUMP_IF_TRUE    124  'to 124'

 122     120  LOAD_CONST            0  ''
         123  RETURN_END_IF    
       124_0  COME_FROM                '117'

 124     124  LOAD_FAST             0  'self'
         127  LOAD_ATTR             8  'get_pos'
         130  CALL_FUNCTION_0       0 
         133  STORE_FAST            7  'pos'

 125     136  LOAD_FAST             7  'pos'
         139  POP_JUMP_IF_FALSE  1381  'to 1381'

 126     142  LOAD_FAST             6  'scn'
         145  LOAD_ATTR             9  'get_scene_info_2d'
         148  LOAD_FAST             7  'pos'
         151  LOAD_ATTR            10  'x'
         154  LOAD_FAST             7  'pos'
         157  LOAD_ATTR            11  'z'
         160  CALL_FUNCTION_2       2 
         163  STORE_FAST            8  'material_index'

 127     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR            12  'check_material_index'
         172  LOAD_FAST             8  'material_index'
         175  CALL_FUNCTION_1       1 
         178  STORE_FAST            8  'material_index'

 128     181  LOAD_FAST             0  'self'
         184  LOAD_ATTR            13  'last_material'
         187  LOAD_FAST             8  'material_index'
         190  COMPARE_OP            3  '!='
         193  POP_JUMP_IF_FALSE   279  'to 279'

 129     196  LOAD_GLOBAL          14  'global_data'
         199  LOAD_ATTR            15  'debug_water_motorcycle'
         202  POP_JUMP_IF_FALSE   257  'to 257'
         205  LOAD_FAST             0  'self'
         208  LOAD_ATTR            16  'ev_g_is_avatar'
         211  CALL_FUNCTION_0       0 
       214_0  COME_FROM                '202'
         214  POP_JUMP_IF_FALSE   257  'to 257'

 130     217  LOAD_GLOBAL          17  'print'
         220  LOAD_CONST            1  'test--ComWater.tick--material_index ='
         223  LOAD_FAST             8  'material_index'
         226  LOAD_CONST            2  '--last_material ='
         229  LOAD_FAST             0  'self'
         232  LOAD_ATTR            13  'last_material'
         235  LOAD_CONST            3  '--self ='
         238  LOAD_CONST            4  '--unit_obj ='
         241  LOAD_FAST             0  'self'
         244  LOAD_ATTR            18  'unit_obj'
         247  BUILD_TUPLE_8         8 
         250  CALL_FUNCTION_1       1 
         253  POP_TOP          
         254  JUMP_FORWARD          0  'to 257'
       257_0  COME_FROM                '254'

 132     257  LOAD_FAST             0  'self'
         260  LOAD_ATTR            19  'send_event'
         263  LOAD_CONST            5  'E_LAST_MATERIAL_CHANGE'
         266  LOAD_CONST            6  'last_material_index'
         269  LOAD_FAST             8  'material_index'
         272  CALL_FUNCTION_257   257 
         275  POP_TOP          
         276  JUMP_FORWARD          0  'to 279'
       279_0  COME_FROM                '276'

 134     279  LOAD_FAST             8  'material_index'
         282  LOAD_FAST             0  'self'
         285  STORE_ATTR           13  'last_material'

 136     288  LOAD_FAST             8  'material_index'
         291  LOAD_GLOBAL          20  'scene_const'
         294  LOAD_ATTR            21  'MTL_WATER'
         297  COMPARE_OP            2  '=='
         300  POP_JUMP_IF_TRUE    318  'to 318'
         303  LOAD_FAST             8  'material_index'
         306  LOAD_GLOBAL          20  'scene_const'
         309  LOAD_ATTR            22  'MTL_DEEP_WATER'
         312  COMPARE_OP            2  '=='
       315_0  COME_FROM                '300'
         315  POP_JUMP_IF_FALSE  1307  'to 1307'

 137     318  LOAD_FAST             6  'scn'
         321  LOAD_ATTR            23  'scene_col'
         324  LOAD_ATTR            24  'hit_by_ray'
         327  LOAD_GLOBAL          25  'math3d'
         330  LOAD_ATTR            26  'vector'
         333  LOAD_FAST             7  'pos'
         336  LOAD_ATTR            10  'x'
         339  LOAD_CONST            7  99999
         342  LOAD_FAST             7  'pos'
         345  LOAD_ATTR            11  'z'
         348  CALL_FUNCTION_3       3 
         351  LOAD_GLOBAL          25  'math3d'
         354  LOAD_ATTR            26  'vector'
         357  LOAD_FAST             7  'pos'
         360  LOAD_ATTR            10  'x'
         363  LOAD_CONST            8  -99999
         366  LOAD_FAST             7  'pos'
         369  LOAD_ATTR            11  'z'
         372  CALL_FUNCTION_3       3 
         375  LOAD_CONST            9  ''
         378  LOAD_CONST           10  -1

 138     381  LOAD_GLOBAL          27  'WATER_GROUP'
         384  LOAD_GLOBAL          28  'TERRAIN_GROUP'
         387  BINARY_OR        

 139     388  LOAD_GLOBAL          29  'collision'
         391  LOAD_ATTR            30  'INCLUDE_FILTER'
         394  LOAD_GLOBAL           3  'True'
         397  LOAD_GLOBAL           6  'False'
         400  CALL_FUNCTION_8       8 
         403  STORE_FAST            9  'result'

 140     406  LOAD_FAST             9  'result'
         409  LOAD_CONST            9  ''
         412  BINARY_SUBSCR    
         413  POP_JUMP_IF_FALSE  1378  'to 1378'

 141     416  LOAD_GLOBAL          31  'sorted'
         419  LOAD_FAST             9  'result'
         422  LOAD_CONST           11  1
         425  BINARY_SUBSCR    
         426  LOAD_CONST           12  'key'
         429  LOAD_GLOBAL          32  'cmp_to_key'
         432  LOAD_FAST             0  'self'
         435  LOAD_ATTR            33  'sort_cmp'
         438  CALL_FUNCTION_1       1 
         441  LOAD_CONST           13  'reverse'
         444  LOAD_GLOBAL           3  'True'
         447  CALL_FUNCTION_513   513 
         450  STORE_FAST           10  'new_result'

 145     453  LOAD_FAST             0  'self'
         456  LOAD_ATTR            34  'check_water_collisions'
         459  LOAD_FAST            10  'new_result'
         462  CALL_FUNCTION_1       1 
         465  STORE_FAST           10  'new_result'

 147     468  LOAD_FAST            10  'new_result'
         471  POP_JUMP_IF_TRUE    552  'to 552'

 148     474  LOAD_FAST             0  'self'
         477  LOAD_ATTR            35  '_set_water_diff_height'
         480  LOAD_CONST            9  ''
         483  CALL_FUNCTION_1       1 
         486  POP_TOP          

 149     487  LOAD_FAST             0  'self'
         490  LOAD_ATTR            36  'sd'
         493  LOAD_ATTR            37  'ref_water_status'
         496  LOAD_GLOBAL          38  'water_const'
         499  LOAD_ATTR            39  'WATER_NONE'
         502  COMPARE_OP            3  '!='
         505  POP_JUMP_IF_FALSE   548  'to 548'

 150     508  LOAD_GLOBAL          38  'water_const'
         511  LOAD_ATTR            39  'WATER_NONE'
         514  LOAD_FAST             0  'self'
         517  LOAD_ATTR            36  'sd'
         520  STORE_ATTR           37  'ref_water_status'

 151     523  LOAD_FAST             0  'self'
         526  LOAD_ATTR            40  'change_status'
         529  LOAD_FAST             0  'self'
         532  LOAD_ATTR            36  'sd'
         535  LOAD_ATTR            37  'ref_water_status'
         538  LOAD_CONST            9  ''
         541  CALL_FUNCTION_2       2 
         544  POP_TOP          
         545  JUMP_FORWARD          0  'to 548'
       548_0  COME_FROM                '545'

 152     548  LOAD_CONST            0  ''
         551  RETURN_END_IF    
       552_0  COME_FROM                '471'

 154     552  LOAD_GLOBAL           6  'False'
         555  STORE_FAST           11  'is_in_water'

 155     558  LOAD_FAST             0  'self'
         561  LOAD_ATTR            41  'DEFAULT_WATER_HEIGHT'
         564  STORE_FAST           12  'water_height'

 156     567  LOAD_CONST            0  ''
         570  STORE_FAST           13  'diff_height'

 157     573  SETUP_LOOP          140  'to 716'
         576  LOAD_FAST            10  'new_result'
         579  GET_ITER         
         580  FOR_ITER            132  'to 715'
         583  STORE_FAST           14  'water_infos'

 158     586  LOAD_FAST             7  'pos'
         589  LOAD_ATTR            43  'y'
         592  LOAD_FAST            14  'water_infos'
         595  LOAD_CONST            9  ''
         598  BINARY_SUBSCR    
         599  LOAD_CONST            9  ''
         602  BINARY_SUBSCR    
         603  LOAD_ATTR            43  'y'
         606  COMPARE_OP            1  '<='
         609  POP_JUMP_IF_FALSE   580  'to 580'

 159     612  LOAD_GLOBAL           3  'True'
         615  STORE_FAST           11  'is_in_water'

 160     618  LOAD_FAST            14  'water_infos'
         621  LOAD_CONST            9  ''
         624  BINARY_SUBSCR    
         625  LOAD_CONST            9  ''
         628  BINARY_SUBSCR    
         629  LOAD_ATTR            43  'y'
         632  STORE_FAST           12  'water_height'

 161     635  LOAD_GLOBAL          44  'len'
         638  LOAD_FAST            14  'water_infos'
         641  CALL_FUNCTION_1       1 
         644  LOAD_CONST           11  1
         647  COMPARE_OP            2  '=='
         650  POP_JUMP_IF_FALSE   677  'to 677'

 162     653  LOAD_FAST            14  'water_infos'
         656  LOAD_CONST            9  ''
         659  BINARY_SUBSCR    
         660  LOAD_CONST            9  ''
         663  BINARY_SUBSCR    
         664  LOAD_ATTR            43  'y'
         667  LOAD_CONST           14  999999
         670  BINARY_ADD       
         671  STORE_FAST           13  'diff_height'
         674  JUMP_ABSOLUTE       712  'to 712'

 164     677  LOAD_FAST            14  'water_infos'
         680  LOAD_CONST            9  ''
         683  BINARY_SUBSCR    
         684  LOAD_CONST            9  ''
         687  BINARY_SUBSCR    
         688  LOAD_ATTR            43  'y'
         691  LOAD_FAST            14  'water_infos'
         694  LOAD_CONST           11  1
         697  BINARY_SUBSCR    
         698  LOAD_CONST            9  ''
         701  BINARY_SUBSCR    
         702  LOAD_ATTR            43  'y'
         705  BINARY_SUBTRACT  
         706  STORE_FAST           13  'diff_height'
         709  JUMP_BACK           580  'to 580'
         712  JUMP_BACK           580  'to 580'
         715  POP_BLOCK        
       716_0  COME_FROM                '573'

 166     716  LOAD_FAST            11  'is_in_water'
         719  POP_JUMP_IF_TRUE    806  'to 806'

 169     722  LOAD_GLOBAL          38  'water_const'
         725  LOAD_ATTR            39  'WATER_NONE'
         728  LOAD_FAST             0  'self'
         731  LOAD_ATTR            36  'sd'
         734  LOAD_ATTR            37  'ref_water_status'
         737  COMPARE_OP            3  '!='
         740  POP_JUMP_IF_FALSE   802  'to 802'

 170     743  LOAD_GLOBAL          38  'water_const'
         746  LOAD_ATTR            39  'WATER_NONE'
         749  LOAD_FAST             0  'self'
         752  LOAD_ATTR            36  'sd'
         755  STORE_ATTR           37  'ref_water_status'

 172     758  LOAD_FAST             0  'self'
         761  LOAD_ATTR            40  'change_status'
         764  LOAD_FAST             0  'self'
         767  LOAD_ATTR            36  'sd'
         770  LOAD_ATTR            37  'ref_water_status'
         773  LOAD_FAST            12  'water_height'
         776  CALL_FUNCTION_2       2 
         779  POP_TOP          

 173     780  LOAD_FAST             0  'self'
         783  LOAD_ATTR            35  '_set_water_diff_height'
         786  LOAD_FAST            13  'diff_height'
         789  JUMP_IF_TRUE_OR_POP   795  'to 795'
         792  LOAD_CONST            9  ''
       795_0  COME_FROM                '789'
         795  CALL_FUNCTION_1       1 
         798  POP_TOP          
         799  JUMP_FORWARD          0  'to 802'
       802_0  COME_FROM                '799'

 174     802  LOAD_CONST            0  ''
         805  RETURN_END_IF    
       806_0  COME_FROM                '719'

 188     806  LOAD_FAST             0  'self'
         809  LOAD_ATTR            45  'on_check_fly_failed'
         812  LOAD_FAST             7  'pos'
         815  LOAD_ATTR            43  'y'
         818  LOAD_FAST            12  'water_height'
         821  CALL_FUNCTION_2       2 
         824  POP_JUMP_IF_FALSE   917  'to 917'

 189     827  LOAD_FAST             0  'self'
         830  LOAD_ATTR            35  '_set_water_diff_height'
         833  LOAD_CONST            9  ''
         836  CALL_FUNCTION_1       1 
         839  POP_TOP          

 194     840  LOAD_FAST             0  'self'
         843  LOAD_ATTR            46  'get_status_by_height'
         846  LOAD_FAST            13  'diff_height'
         849  CALL_FUNCTION_1       1 
         852  STORE_FAST           15  'status'

 195     855  LOAD_FAST            15  'status'
         858  LOAD_FAST             0  'self'
         861  LOAD_ATTR            36  'sd'
         864  LOAD_ATTR            37  'ref_water_status'
         867  COMPARE_OP            3  '!='
         870  POP_JUMP_IF_FALSE   913  'to 913'

 197     873  LOAD_FAST            15  'status'
         876  LOAD_FAST             0  'self'
         879  LOAD_ATTR            36  'sd'
         882  STORE_ATTR           37  'ref_water_status'

 198     885  LOAD_FAST             0  'self'
         888  LOAD_ATTR            40  'change_status'
         891  LOAD_FAST             0  'self'
         894  LOAD_ATTR            36  'sd'
         897  LOAD_ATTR            37  'ref_water_status'
         900  LOAD_FAST            12  'water_height'
         903  LOAD_FAST            13  'diff_height'
         906  CALL_FUNCTION_3       3 
         909  POP_TOP          
         910  JUMP_FORWARD          0  'to 913'
       913_0  COME_FROM                '910'

 199     913  LOAD_CONST            0  ''
         916  RETURN_END_IF    
       917_0  COME_FROM                '824'

 201     917  LOAD_FAST             0  'self'
         920  LOAD_ATTR            35  '_set_water_diff_height'
         923  LOAD_FAST            13  'diff_height'
         926  CALL_FUNCTION_1       1 
         929  POP_TOP          

 203     930  LOAD_FAST             5  'can_change_status'
         933  POP_JUMP_IF_TRUE    940  'to 940'

 205     936  LOAD_CONST            0  ''
         939  RETURN_END_IF    
       940_0  COME_FROM                '933'

 216     940  LOAD_FAST            10  'new_result'
         943  LOAD_CONST            9  ''
         946  BINARY_SUBSCR    
         947  LOAD_CONST            9  ''
         950  BINARY_SUBSCR    
         951  STORE_FAST           16  'water_result'

 217     954  LOAD_GLOBAL          47  'getattr'
         957  LOAD_FAST            16  'water_result'
         960  LOAD_CONST           15  4
         963  BINARY_SUBSCR    
         964  LOAD_CONST           16  'model_col_name'
         967  LOAD_CONST            0  ''
         970  CALL_FUNCTION_3       3 
         973  STORE_FAST           17  'model_name'

 218     976  LOAD_GLOBAL           6  'False'
         979  STORE_FAST           18  'chang_status'

 219     982  LOAD_FAST            17  'model_name'
         985  POP_JUMP_IF_FALSE  1152  'to 1152'

 220     988  LOAD_GLOBAL          14  'global_data'
         991  LOAD_ATTR            48  'game_mgr'
         994  LOAD_ATTR             7  'scene'
         997  LOAD_ATTR            49  'get_model'
        1000  LOAD_FAST            17  'model_name'
        1003  CALL_FUNCTION_1       1 
        1006  STORE_FAST           19  'model'

 221    1009  LOAD_FAST            19  'model'
        1012  POP_JUMP_IF_FALSE  1152  'to 1152'

 222    1015  LOAD_FAST            16  'water_result'
        1018  LOAD_CONST           11  1
        1021  BINARY_SUBSCR    
        1022  STORE_FAST           20  'normal'

 224    1025  LOAD_GLOBAL          25  'math3d'
        1028  LOAD_ATTR            26  'vector'
        1031  LOAD_CONST            9  ''
        1034  LOAD_CONST           11  1
        1037  LOAD_CONST            9  ''
        1040  CALL_FUNCTION_3       3 
        1043  LOAD_ATTR            50  'dot'
        1046  LOAD_FAST            20  'normal'
        1049  CALL_FUNCTION_1       1 
        1052  LOAD_FAST            20  'normal'
        1055  LOAD_ATTR            51  'length'
        1058  BINARY_DIVIDE    
        1059  LOAD_CONST           17  0.85
        1062  COMPARE_OP            0  '<'
        1065  POP_JUMP_IF_FALSE  1149  'to 1149'

 225    1068  LOAD_FAST             0  'self'
        1071  LOAD_ATTR            35  '_set_water_diff_height'
        1074  LOAD_CONST            9  ''
        1077  CALL_FUNCTION_1       1 
        1080  POP_TOP          

 226    1081  LOAD_FAST             0  'self'
        1084  LOAD_ATTR            36  'sd'
        1087  LOAD_ATTR            37  'ref_water_status'
        1090  LOAD_GLOBAL          38  'water_const'
        1093  LOAD_ATTR            39  'WATER_NONE'
        1096  COMPARE_OP            3  '!='
        1099  POP_JUMP_IF_FALSE  1142  'to 1142'

 227    1102  LOAD_GLOBAL          38  'water_const'
        1105  LOAD_ATTR            39  'WATER_NONE'
        1108  LOAD_FAST             0  'self'
        1111  LOAD_ATTR            36  'sd'
        1114  STORE_ATTR           37  'ref_water_status'

 228    1117  LOAD_FAST             0  'self'
        1120  LOAD_ATTR            40  'change_status'
        1123  LOAD_FAST             0  'self'
        1126  LOAD_ATTR            36  'sd'
        1129  LOAD_ATTR            37  'ref_water_status'
        1132  LOAD_CONST            9  ''
        1135  CALL_FUNCTION_2       2 
        1138  POP_TOP          
        1139  JUMP_FORWARD          0  'to 1142'
      1142_0  COME_FROM                '1139'

 229    1142  LOAD_CONST            0  ''
        1145  RETURN_END_IF    
      1146_0  COME_FROM                '1065'
        1146  JUMP_ABSOLUTE      1152  'to 1152'
        1149  JUMP_FORWARD          0  'to 1152'
      1152_0  COME_FROM                '1149'

 230    1152  LOAD_FAST             0  'self'
        1155  LOAD_ATTR            52  'last_water_height'
        1158  LOAD_FAST            12  'water_height'
        1161  COMPARE_OP            3  '!='
        1164  POP_JUMP_IF_FALSE  1176  'to 1176'

 231    1167  LOAD_GLOBAL           3  'True'
        1170  STORE_FAST           18  'chang_status'
        1173  JUMP_FORWARD          0  'to 1176'
      1176_0  COME_FROM                '1173'

 234    1176  LOAD_FAST             0  'self'
        1179  LOAD_ATTR            46  'get_status_by_height'
        1182  LOAD_FAST            13  'diff_height'
        1185  CALL_FUNCTION_1       1 
        1188  STORE_FAST           15  'status'

 235    1191  LOAD_FAST            15  'status'
        1194  LOAD_FAST             0  'self'
        1197  LOAD_ATTR            36  'sd'
        1200  LOAD_ATTR            37  'ref_water_status'
        1203  COMPARE_OP            3  '!='
        1206  POP_JUMP_IF_FALSE  1230  'to 1230'

 236    1209  LOAD_GLOBAL           3  'True'
        1212  STORE_FAST           18  'chang_status'

 237    1215  LOAD_FAST            15  'status'
        1218  LOAD_FAST             0  'self'
        1221  LOAD_ATTR            36  'sd'
        1224  STORE_ATTR           37  'ref_water_status'
        1227  JUMP_FORWARD          0  'to 1230'
      1230_0  COME_FROM                '1227'

 239    1230  LOAD_FAST            18  'chang_status'
        1233  POP_JUMP_IF_FALSE  1304  'to 1304'

 240    1236  LOAD_FAST             0  'self'
        1239  LOAD_ATTR            40  'change_status'
        1242  LOAD_FAST             0  'self'
        1245  LOAD_ATTR            36  'sd'
        1248  LOAD_ATTR            37  'ref_water_status'
        1251  LOAD_FAST            12  'water_height'
        1254  LOAD_FAST            13  'diff_height'
        1257  CALL_FUNCTION_3       3 
        1260  POP_TOP          

 242    1261  LOAD_FAST             0  'self'
        1264  LOAD_ATTR            36  'sd'
        1267  LOAD_ATTR            37  'ref_water_status'
        1270  LOAD_GLOBAL          38  'water_const'
        1273  LOAD_ATTR            53  'WATER_DEEP_LEVEL'
        1276  COMPARE_OP            2  '=='
        1279  POP_JUMP_IF_FALSE  1301  'to 1301'

 243    1282  LOAD_FAST             0  'self'
        1285  LOAD_ATTR            19  'send_event'
        1288  LOAD_CONST           18  'E_CHANGE_WATER_LIMIT'
        1291  CALL_FUNCTION_1       1 
        1294  POP_TOP          
        1295  JUMP_ABSOLUTE      1301  'to 1301'
        1298  JUMP_ABSOLUTE      1304  'to 1304'
        1301  JUMP_ABSOLUTE      1378  'to 1378'
        1304  JUMP_ABSOLUTE      1381  'to 1381'

 254    1307  LOAD_FAST             0  'self'
        1310  LOAD_ATTR            35  '_set_water_diff_height'
        1313  LOAD_CONST            9  ''
        1316  CALL_FUNCTION_1       1 
        1319  POP_TOP          

 255    1320  LOAD_FAST             0  'self'
        1323  LOAD_ATTR            36  'sd'
        1326  LOAD_ATTR            37  'ref_water_status'
        1329  LOAD_GLOBAL          38  'water_const'
        1332  LOAD_ATTR            39  'WATER_NONE'
        1335  COMPARE_OP            3  '!='
        1338  POP_JUMP_IF_FALSE  1381  'to 1381'

 256    1341  LOAD_GLOBAL          38  'water_const'
        1344  LOAD_ATTR            39  'WATER_NONE'
        1347  LOAD_FAST             0  'self'
        1350  LOAD_ATTR            36  'sd'
        1353  STORE_ATTR           37  'ref_water_status'

 258    1356  LOAD_FAST             0  'self'
        1359  LOAD_ATTR            40  'change_status'
        1362  LOAD_FAST             0  'self'
        1365  LOAD_ATTR            36  'sd'
        1368  LOAD_ATTR            37  'ref_water_status'
        1371  CALL_FUNCTION_1       1 
        1374  POP_TOP          
        1375  JUMP_ABSOLUTE      1381  'to 1381'
        1378  JUMP_FORWARD          0  'to 1381'
      1381_0  COME_FROM                '1378'
        1381  LOAD_CONST            0  ''
        1384  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 250

    def get_status_by_height(self, diff_height):
        from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL
        scene_name = global_data.battle.get_scene_name() or BATTLE_SCENE_NORMAL
        heights = water_const.WATER_HEIGHT.get(scene_name)
        if diff_height <= heights[0]:
            return water_const.WATER_NONE
        else:
            if diff_height <= heights[1] * NEOX_UNIT_SCALE:
                return water_const.WATER_SHALLOW_LEVEL
            if diff_height <= heights[2] * NEOX_UNIT_SCALE:
                return water_const.WATER_SHWLLOW_LEVEL2
            if diff_height <= heights[3] * NEOX_UNIT_SCALE:
                return water_const.WATER_MID_LEVEL
            return water_const.WATER_DEEP_LEVEL

        return water_const.WATER_NONE

    def check_water_collisions(self, new_results):
        filter_list = []
        flag = False
        for result in new_results:
            rgroup = result[4].group
            if rgroup == WATER_GROUP and not flag:
                flag = True
                filter_list.append([result])
            elif rgroup == 65535 and flag:
                flag = False
                filter_list[-1].append(result)
            elif rgroup & GROUP_STATIC_SHOOTUNIT and not rgroup & GROUP_DYNAMIC_SHOOTUNIT and flag:
                flag = False
                filter_list[-1].append(result)

        col_results = []
        for cols in filter_list:
            if len(cols) == 2 or len(cols) == len(new_results) == 1:
                col_results.append(cols)

        return col_results

    def remove_same_water_obj(self, new_results):
        has_water = False
        delete_list = []
        water_height = self.DEFAULT_WATER_HEIGHT
        for result in new_results:
            if result[4].mask == WATER_MASK and result[4].group == WATER_GROUP:
                if not has_water:
                    has_water = True
                    water_height = result[0].y
                    continue
                delete_list.append(result)
            elif result[4].mask == 31 and result[4].group == 31:
                delete_list.append(result)
            elif result[4].group not in (WATER_GROUP, TERRAIN_GROUP, 65535, STONE_GROUP, ROAD_GROUP):
                delete_list.append(result)

        for del_r in delete_list:
            new_results.remove(del_r)

        low_than_water_height = []
        for result in new_results:
            if result[0].y <= water_height:
                low_than_water_height.append(result)

        return low_than_water_height

    def sort_cmp(self, c1, c2):
        if c1[0].y > c2[0].y:
            return 1
        else:
            if c1[0].y < c2[0].y:
                return -1
            return 0

    def is_water_obj(self, obj):
        return obj.mask == WATER_MASK and obj.group == WATER_GROUP

    def destroy(self):
        self.sd.ref_water_status = None
        self.is_first = True
        self.last_check = 0
        self.last_status_check = 0
        self.last_diff_height = 0
        super(ComWater, self).destroy()
        return

    def _refresh_cur_water_status(self):
        if self.sd.ref_water_status is not None and self.last_water_height is not None:
            self.change_status(self.sd.ref_water_status, self.last_water_height)
        return