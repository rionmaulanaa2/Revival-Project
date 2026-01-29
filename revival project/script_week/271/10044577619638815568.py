# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/detection_utils.py
from __future__ import absolute_import
from six.moves import range
import math
import math3d
import world
import collision
import game3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.scene_const import MTL_HOUSE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_EXCLUDE, WATER_GROUP, WATER_MASK, REGION_SCENE_GROUP, REGION_BOUNDARY_SCENE_GROUP, TERRAIN_MASK, GROUP_SHOOTUNIT, SLOPE_GROUP
from common.cfg import confmgr
MAX_DETECT_DIST = 50 * NEOX_UNIT_SCALE
VALID_POS = [None, None]
DETECT_COL = None
DETECT_TIMES = 0
DETECT_CALLBACK = None
RESULT_NOT_NONE = True
CAMERA_OFFSET = 3
UP_VECTOR = math3d.vector(0, 1, 0)
DEFAULT_UP_ROTATE_ANGLE = math.radians(40)

def get_valid_jump_pos():
    global VALID_POS
    if not VALID_POS[0] and not VALID_POS[1]:
        return None
    else:
        if not VALID_POS[0]:
            return VALID_POS[1]
        if not VALID_POS[1]:
            return VALID_POS[0]
        camera = global_data.game_mgr.scene.active_camera
        start = camera.position
        dir_cam = camera.rotation_matrix.forward
        dir0 = VALID_POS[0] - start
        dir0.normalize()
        dir1 = VALID_POS[1] - start
        dir1.normalize()
        if dir_cam.dot(dir0) >= dir_cam.dot(dir1):
            return VALID_POS[0]
        return VALID_POS[1]
        return None


def get_no_obstacle(scene, hit_pos, camera_pos):
    global DETECT_TIMES
    direction = camera_pos - hit_pos
    direction.y = 0
    direction.normalize()
    group = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
    mask = GROUP_CHARACTER_INCLUDE & ~WATER_MASK
    for i in range(50):
        t_s_pos = hit_pos + direction * NEOX_UNIT_SCALE * i
        t_e_pos = t_s_pos + math3d.vector(0, -10000, 0)
        ret = scene.scene_col.hit_by_ray(t_s_pos, t_e_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
        DETECT_TIMES += 1
        if not ret[0]:
            continue
        point = ret[1]
        valid_start = math3d.vector(point.x, point.y + NEOX_UNIT_SCALE, point.z)
        valid_ret = scene.scene_col.hit_by_ray(valid_start, camera_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
        DETECT_TIMES += 1
        if not valid_ret[0]:
            return point


def get_no_obstacle_new(scene, top_point_pos, camera_pos):
    global DETECT_TIMES
    cam_dir = top_point_pos - camera_pos
    hypotenuse = cam_dir.length
    if hypotenuse == 0.0:
        return None
    else:
        cam_dir.y = 0
        cos_value = cam_dir.length / hypotenuse
        delta_hypotenuse = NEOX_UNIT_SCALE / cos_value
        cam_dir = top_point_pos - camera_pos
        cam_dir.normalize()
        cam_dir *= delta_hypotenuse
        group = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
        mask = GROUP_CHARACTER_INCLUDE & ~WATER_MASK
        for i in range(1, 50):
            t_s_pos = top_point_pos - cam_dir * i
            t_e_pos = t_s_pos + math3d.vector(0, -10000, 0)
            ret = scene.scene_col.hit_by_ray(t_s_pos, t_e_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
            DETECT_TIMES += 1
            if not ret[0]:
                continue
            point = ret[1]
            valid_start = math3d.vector(point.x, point.y + NEOX_UNIT_SCALE, point.z)
            valid_ret = scene.scene_col.hit_by_ray(valid_start, camera_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
            DETECT_TIMES += 1
            if not valid_ret[0]:
                return point

        return None


def check_target_pos_behind_mecha(target_pos, mecha_pos, camera):
    if mecha_pos is not None:
        target_dir = target_pos - mecha_pos
        target_dir.y = 0
        if target_dir.is_zero:
            return True
        target_dir.normalize()
        forward = camera.rotation_matrix.forward
        forward.y = 0
        if forward.is_zero:
            return True
        forward.normalize()
        return target_dir.dot(forward) < 0
    else:
        return False


def detect_jump_pos--- This code section failed: ---

 119       0  LOAD_GLOBAL           0  'DETECT_COL'
           3  POP_JUMP_IF_TRUE     10  'to 10'

 120       6  LOAD_CONST            0  ''
           9  RETURN_END_IF    
        10_0  COME_FROM                '3'

 122      10  LOAD_GLOBAL           1  'world'
          13  LOAD_ATTR             2  'get_active_scene'
          16  CALL_FUNCTION_0       0 
          19  STORE_FAST            1  'scene'

 123      22  LOAD_FAST             1  'scene'
          25  LOAD_ATTR             3  'active_camera'
          28  STORE_FAST            2  'camera'

 124      31  LOAD_FAST             2  'camera'
          34  LOAD_ATTR             4  'rotation_matrix'
          37  LOAD_ATTR             5  'forward'
          40  STORE_FAST            3  'ori_forward'

 125      43  LOAD_FAST             2  'camera'
          46  LOAD_ATTR             4  'rotation_matrix'
          49  LOAD_ATTR             6  'right'
          52  STORE_FAST            4  'right'

 127      55  STORE_FAST            1  'scene'
          58  COMPARE_OP            2  '=='
          61  POP_JUMP_IF_FALSE   160  'to 160'

 128      64  LOAD_GLOBAL           7  'math3d'
          67  LOAD_ATTR             8  'rotation'
          70  LOAD_CONST            2  ''
          73  LOAD_CONST            2  ''
          76  LOAD_CONST            2  ''
          79  LOAD_CONST            3  1
          82  CALL_FUNCTION_4       4 
          85  STORE_FAST            5  'rot'

 130      88  LOAD_GLOBAL           9  'min'
          91  LOAD_GLOBAL          10  'math'
          94  LOAD_ATTR            11  'acos'
          97  LOAD_FAST             3  'ori_forward'
         100  LOAD_ATTR            12  'dot'
         103  LOAD_GLOBAL          13  'UP_VECTOR'
         106  CALL_FUNCTION_1       1 
         109  CALL_FUNCTION_1       1 
         112  LOAD_CONST            4  0.1
         115  BINARY_SUBTRACT  
         116  LOAD_GLOBAL          14  'DEFAULT_UP_ROTATE_ANGLE'
         119  CALL_FUNCTION_2       2 
         122  STORE_FAST            6  'rotate_angle'

 131     125  LOAD_FAST             5  'rot'
         128  LOAD_ATTR            15  'set_axis_angle'
         131  LOAD_FAST             4  'right'
         134  LOAD_FAST             6  'rotate_angle'
         137  UNARY_NEGATIVE   
         138  CALL_FUNCTION_2       2 
         141  POP_TOP          

 132     142  LOAD_FAST             5  'rot'
         145  LOAD_ATTR            16  'rotate_vector'
         148  LOAD_FAST             3  'ori_forward'
         151  CALL_FUNCTION_1       1 
         154  STORE_FAST            3  'ori_forward'
         157  JUMP_FORWARD          0  'to 160'
       160_0  COME_FROM                '157'

 134     160  LOAD_FAST             2  'camera'
         163  LOAD_ATTR            17  'position'
         166  LOAD_FAST             3  'ori_forward'
         169  LOAD_GLOBAL          18  'CAMERA_OFFSET'
         172  BINARY_MULTIPLY  
         173  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
         176  BINARY_MULTIPLY  
         177  BINARY_ADD       
         178  STORE_FAST            7  'start_pos'

 135     181  LOAD_FAST             7  'start_pos'
         184  LOAD_FAST             3  'ori_forward'
         187  LOAD_GLOBAL          20  'MAX_DETECT_DIST'
         190  BINARY_MULTIPLY  
         191  BINARY_ADD       
         192  STORE_FAST            8  'end_pos'

 137     195  LOAD_GLOBAL          21  'global_data'
         198  LOAD_ATTR            22  'mecha'
         201  POP_JUMP_IF_FALSE   234  'to 234'
         204  LOAD_GLOBAL          21  'global_data'
         207  LOAD_ATTR            22  'mecha'
         210  LOAD_ATTR            23  'logic'
       213_0  COME_FROM                '201'
         213  POP_JUMP_IF_FALSE   234  'to 234'
         216  LOAD_GLOBAL          21  'global_data'
         219  LOAD_ATTR            22  'mecha'
         222  LOAD_ATTR            23  'logic'
         225  LOAD_ATTR            24  'ev_g_position'
         228  CALL_FUNCTION_0       0 
         231  JUMP_FORWARD          3  'to 237'
         234  LOAD_CONST            0  ''
       237_0  COME_FROM                '231'
         237  STORE_FAST            9  'mecha_pos'

 139     240  LOAD_CONST            5  50
         243  STORE_FAST           10  'max_search'

 140     246  LOAD_GLOBAL          26  'False'
         249  STORE_FAST           11  'last_detect_block_area'

 141     252  LOAD_CONST            2  ''
         255  STORE_FAST           12  'detect_block_area_pass_count'

 142     258  LOAD_CONST            2  ''
         261  STORE_GLOBAL         27  'DETECT_TIMES'

 143     264  LOAD_GLOBAL          28  'GROUP_CHARACTER_INCLUDE'
         267  LOAD_GLOBAL          29  'WATER_GROUP'
         270  UNARY_INVERT     
         271  BINARY_AND       
         272  STORE_FAST           13  'group'

 144     275  LOAD_GLOBAL          28  'GROUP_CHARACTER_INCLUDE'
         278  LOAD_GLOBAL          30  'WATER_MASK'
         281  UNARY_INVERT     
         282  BINARY_AND       
         283  STORE_FAST           14  'mask'

 148     286  SETUP_LOOP         1197  'to 1486'
         289  LOAD_GLOBAL          31  'range'
         292  LOAD_FAST            10  'max_search'
         295  CALL_FUNCTION_1       1 
         298  GET_ITER         
         299  FOR_ITER           1051  'to 1353'
         302  STORE_FAST           15  'i'

 150     305  LOAD_FAST             3  'ori_forward'
         308  STORE_FAST           16  'forward'

 151     311  LOAD_FAST            15  'i'
         314  LOAD_CONST            2  ''
         317  COMPARE_OP            4  '>'
         320  POP_JUMP_IF_FALSE   400  'to 400'

 152     323  LOAD_GLOBAL           7  'math3d'
         326  LOAD_ATTR             8  'rotation'
         329  LOAD_CONST            2  ''
         332  LOAD_CONST            2  ''
         335  LOAD_CONST            2  ''
         338  LOAD_CONST            3  1
         341  CALL_FUNCTION_4       4 
         344  STORE_FAST            5  'rot'

 153     347  LOAD_FAST             5  'rot'
         350  LOAD_ATTR            15  'set_axis_angle'
         353  LOAD_FAST             4  'right'
         356  LOAD_FAST            15  'i'
         359  LOAD_CONST            6  0.5
         362  BINARY_MULTIPLY  
         363  LOAD_FAST             0  'detect_stage'
         366  BINARY_MULTIPLY  
         367  LOAD_GLOBAL          10  'math'
         370  LOAD_ATTR            32  'pi'
         373  BINARY_MULTIPLY  
         374  LOAD_CONST            7  180
         377  BINARY_DIVIDE    
         378  CALL_FUNCTION_2       2 
         381  POP_TOP          

 154     382  LOAD_FAST             5  'rot'
         385  LOAD_ATTR            16  'rotate_vector'
         388  LOAD_FAST             3  'ori_forward'
         391  CALL_FUNCTION_1       1 
         394  STORE_FAST           16  'forward'
         397  JUMP_FORWARD          0  'to 400'
       400_0  COME_FROM                '397'

 155     400  LOAD_FAST             7  'start_pos'
         403  LOAD_FAST            16  'forward'
         406  LOAD_GLOBAL          20  'MAX_DETECT_DIST'
         409  BINARY_MULTIPLY  
         410  BINARY_ADD       
         411  STORE_FAST           17  'new_end_pos'

 156     414  LOAD_FAST             1  'scene'
         417  LOAD_ATTR            33  'scene_col'
         420  LOAD_ATTR            34  'hit_by_ray'
         423  LOAD_FAST             7  'start_pos'
         426  LOAD_FAST            17  'new_end_pos'
         429  LOAD_CONST            2  ''
         432  LOAD_FAST            13  'group'
         435  LOAD_FAST            14  'mask'
         438  LOAD_GLOBAL          35  'collision'
         441  LOAD_ATTR            36  'INCLUDE_FILTER'
         444  LOAD_GLOBAL          26  'False'
         447  CALL_FUNCTION_7       7 
         450  STORE_FAST           18  'result'

 158     453  LOAD_GLOBAL          27  'DETECT_TIMES'
         456  LOAD_CONST            3  1
         459  INPLACE_ADD      
         460  STORE_GLOBAL         27  'DETECT_TIMES'

 159     463  LOAD_FAST            18  'result'
         466  LOAD_CONST            2  ''
         469  BINARY_SUBSCR    
         470  POP_JUMP_IF_FALSE   299  'to 299'

 160     473  LOAD_FAST            18  'result'
         476  LOAD_CONST            3  1
         479  BINARY_SUBSCR    
         480  LOAD_FAST            18  'result'
         483  LOAD_CONST            1  2
         486  BINARY_SUBSCR    
         487  LOAD_FAST            18  'result'
         490  LOAD_CONST            8  5
         493  BINARY_SUBSCR    
         494  ROT_THREE        
         495  ROT_TWO          
         496  STORE_FAST           19  'point'
         499  STORE_FAST           20  'normal'
         502  STORE_FAST           21  'col_object'

 161     505  LOAD_FAST            21  'col_object'
         508  LOAD_ATTR            37  'group'
         511  LOAD_GLOBAL          38  'REGION_BOUNDARY_SCENE_GROUP'
         514  COMPARE_OP            2  '=='
         517  POP_JUMP_IF_FALSE   526  'to 526'

 162     520  CONTINUE            299  'to 299'
         523  JUMP_FORWARD          0  'to 526'
       526_0  COME_FROM                '523'

 163     526  LOAD_FAST            21  'col_object'
         529  LOAD_ATTR            37  'group'
         532  LOAD_GLOBAL          39  'REGION_SCENE_GROUP'
         535  COMPARE_OP            2  '=='
         538  POP_JUMP_IF_FALSE   568  'to 568'
         541  LOAD_FAST            21  'col_object'
         544  LOAD_ATTR            40  'mask'
         547  LOAD_GLOBAL          41  'TERRAIN_MASK'
         550  COMPARE_OP            2  '=='
       553_0  COME_FROM                '538'
         553  POP_JUMP_IF_FALSE   568  'to 568'

 164     556  LOAD_GLOBAL          42  'True'
         559  STORE_FAST           11  'last_detect_block_area'

 166     562  CONTINUE            299  'to 299'
         565  JUMP_FORWARD          0  'to 568'
       568_0  COME_FROM                '565'

 167     568  LOAD_FAST            15  'i'
         571  LOAD_CONST            2  ''
         574  COMPARE_OP            2  '=='
         577  POP_JUMP_IF_TRUE    586  'to 586'
         580  LOAD_FAST            11  'last_detect_block_area'
       583_0  COME_FROM                '577'
         583  POP_JUMP_IF_FALSE   993  'to 993'

 168     586  LOAD_CONST            2  ''
         589  LOAD_FAST            20  'normal'
         592  STORE_ATTR           43  'y'

 169     595  LOAD_FAST            19  'point'
         598  STORE_FAST           22  'top_point_pos'

 170     601  LOAD_FAST            19  'point'
         604  LOAD_FAST            20  'normal'
         607  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
         610  BINARY_MULTIPLY  
         611  BINARY_ADD       
         612  STORE_FAST           23  't_s_pos'

 171     615  LOAD_FAST            23  't_s_pos'
         618  LOAD_GLOBAL           7  'math3d'
         621  LOAD_ATTR            44  'vector'
         624  LOAD_CONST            2  ''
         627  LOAD_CONST            9  -10000
         630  LOAD_CONST            2  ''
         633  CALL_FUNCTION_3       3 
         636  BINARY_ADD       
         637  STORE_FAST           24  't_e_pos'

 172     640  LOAD_FAST             1  'scene'
         643  LOAD_ATTR            33  'scene_col'
         646  LOAD_ATTR            34  'hit_by_ray'
         649  LOAD_FAST            23  't_s_pos'
         652  LOAD_FAST            24  't_e_pos'
         655  LOAD_CONST            2  ''
         658  LOAD_FAST            13  'group'
         661  LOAD_FAST            14  'mask'
         664  LOAD_GLOBAL          35  'collision'
         667  LOAD_ATTR            36  'INCLUDE_FILTER'
         670  LOAD_GLOBAL          26  'False'
         673  CALL_FUNCTION_7       7 
         676  STORE_FAST           25  'ret'

 173     679  LOAD_GLOBAL          27  'DETECT_TIMES'
         682  LOAD_CONST            3  1
         685  INPLACE_ADD      
         686  STORE_GLOBAL         27  'DETECT_TIMES'

 174     689  LOAD_FAST            25  'ret'
         692  LOAD_CONST            2  ''
         695  BINARY_SUBSCR    
         696  POP_JUMP_IF_FALSE  1347  'to 1347'

 175     699  LOAD_FAST            25  'ret'
         702  LOAD_CONST            3  1
         705  BINARY_SUBSCR    
         706  LOAD_FAST            18  'result'
         709  LOAD_CONST            1  2
         712  BINARY_SUBSCR    
         713  ROT_TWO          
         714  STORE_FAST           19  'point'
         717  STORE_FAST           20  'normal'

 176     720  LOAD_GLOBAL           7  'math3d'
         723  LOAD_ATTR            44  'vector'
         726  LOAD_FAST            19  'point'
         729  LOAD_ATTR            45  'x'
         732  LOAD_FAST            19  'point'
         735  LOAD_ATTR            43  'y'
         738  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
         741  BINARY_ADD       
         742  LOAD_FAST            19  'point'
         745  LOAD_ATTR            46  'z'
         748  CALL_FUNCTION_3       3 
         751  STORE_FAST           26  'valid_start'

 177     754  LOAD_FAST             1  'scene'
         757  LOAD_ATTR            33  'scene_col'
         760  LOAD_ATTR            34  'hit_by_ray'
         763  LOAD_FAST            26  'valid_start'
         766  LOAD_FAST             7  'start_pos'
         769  LOAD_CONST            2  ''
         772  LOAD_FAST            13  'group'
         775  LOAD_FAST            14  'mask'
         778  LOAD_GLOBAL          35  'collision'
         781  LOAD_ATTR            36  'INCLUDE_FILTER'
         784  LOAD_GLOBAL          26  'False'
         787  CALL_FUNCTION_7       7 
         790  STORE_FAST           27  'valid_ret'

 178     793  LOAD_GLOBAL          27  'DETECT_TIMES'
         796  LOAD_CONST            3  1
         799  INPLACE_ADD      
         800  STORE_GLOBAL         27  'DETECT_TIMES'

 179     803  LOAD_FAST            27  'valid_ret'
         806  LOAD_CONST            2  ''
         809  BINARY_SUBSCR    
         810  POP_JUMP_IF_TRUE    822  'to 822'

 180     813  LOAD_FAST            19  'point'
         816  STORE_FAST           28  'final_pos'
         819  JUMP_FORWARD         24  'to 846'

 183     822  LOAD_GLOBAL          47  'get_no_obstacle_new'
         825  LOAD_FAST             1  'scene'
         828  LOAD_FAST            22  'top_point_pos'
         831  LOAD_FAST             7  'start_pos'
         834  CALL_FUNCTION_3       3 
         837  JUMP_IF_TRUE_OR_POP   843  'to 843'
         840  LOAD_FAST            19  'point'
       843_0  COME_FROM                '837'
         843  STORE_FAST           28  'final_pos'
       846_0  COME_FROM                '819'

 185     846  LOAD_CONST            2  ''
         849  LOAD_FAST            20  'normal'
         852  STORE_ATTR           43  'y'

 186     855  LOAD_FAST            28  'final_pos'
         858  LOAD_FAST            20  'normal'
         861  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
         864  BINARY_MULTIPLY  
         865  LOAD_CONST           10  1.7
         868  BINARY_MULTIPLY  
         869  INPLACE_ADD      
         870  STORE_FAST           28  'final_pos'

 189     873  LOAD_GLOBAL          48  'check_target_pos_behind_mecha'
         876  LOAD_FAST            28  'final_pos'
         879  LOAD_FAST             9  'mecha_pos'
         882  LOAD_FAST             2  'camera'
         885  CALL_FUNCTION_3       3 
         888  POP_JUMP_IF_FALSE   897  'to 897'

 190     891  CONTINUE            299  'to 299'
         894  JUMP_FORWARD          0  'to 897'
       897_0  COME_FROM                '894'

 192     897  LOAD_FAST            28  'final_pos'
         900  LOAD_GLOBAL          49  'VALID_POS'
         903  LOAD_GLOBAL           3  'active_camera'
         906  BINARY_SUBTRACT  
         907  STORE_SUBSCR     

 194     908  LOAD_FAST            11  'last_detect_block_area'
         911  POP_JUMP_IF_FALSE   986  'to 986'
         914  LOAD_FAST             9  'mecha_pos'
         917  LOAD_CONST            0  ''
         920  COMPARE_OP            9  'is-not'
       923_0  COME_FROM                '911'
         923  POP_JUMP_IF_FALSE   986  'to 986'

 195     926  LOAD_FAST            12  'detect_block_area_pass_count'
         929  LOAD_CONST            3  1
         932  INPLACE_ADD      
         933  STORE_FAST           12  'detect_block_area_pass_count'

 196     936  LOAD_GLOBAL          50  'can_teleport'
         939  LOAD_GLOBAL          49  'VALID_POS'
         942  LOAD_GLOBAL           3  'active_camera'
         945  BINARY_SUBTRACT  
         946  BINARY_SUBSCR    
         947  LOAD_FAST             9  'mecha_pos'
         950  CALL_FUNCTION_2       2 
         953  POP_JUMP_IF_TRUE    986  'to 986'

 198     956  LOAD_FAST            12  'detect_block_area_pass_count'
         959  LOAD_CONST            3  1
         962  COMPARE_OP            4  '>'
         965  POP_JUMP_IF_FALSE   299  'to 299'

 199     968  LOAD_GLOBAL          26  'False'
         971  STORE_FAST           11  'last_detect_block_area'
         974  JUMP_BACK           299  'to 299'

 200     977  CONTINUE            299  'to 299'
         980  JUMP_ABSOLUTE       986  'to 986'
         983  JUMP_FORWARD          0  'to 986'
       986_0  COME_FROM                '983'

 201     986  BREAK_LOOP       
         987  JUMP_ABSOLUTE      1347  'to 1347'
         990  JUMP_ABSOLUTE      1350  'to 1350'

 203     993  LOAD_FAST            19  'point'
         996  LOAD_GLOBAL           7  'math3d'
         999  LOAD_ATTR            44  'vector'
        1002  LOAD_CONST            2  ''
        1005  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
        1008  LOAD_CONST           11  3
        1011  BINARY_MULTIPLY  
        1012  LOAD_CONST            2  ''
        1015  CALL_FUNCTION_3       3 
        1018  BINARY_ADD       
        1019  STORE_FAST           23  't_s_pos'

 204    1022  LOAD_FAST            19  'point'
        1025  STORE_FAST           24  't_e_pos'

 205    1028  LOAD_FAST             1  'scene'
        1031  LOAD_ATTR            33  'scene_col'
        1034  LOAD_ATTR            51  'sweep_test'
        1037  LOAD_GLOBAL           0  'DETECT_COL'
        1040  LOAD_FAST            23  't_s_pos'
        1043  LOAD_FAST            24  't_e_pos'
        1046  LOAD_FAST            13  'group'
        1049  LOAD_FAST            14  'mask'
        1052  LOAD_CONST            2  ''
        1055  LOAD_GLOBAL          35  'collision'
        1058  LOAD_ATTR            36  'INCLUDE_FILTER'
        1061  CALL_FUNCTION_7       7 
        1064  STORE_FAST           25  'ret'

 206    1067  LOAD_FAST            25  'ret'
        1070  LOAD_CONST            2  ''
        1073  BINARY_SUBSCR    
        1074  POP_JUMP_IF_FALSE  1350  'to 1350'

 207    1077  LOAD_FAST            25  'ret'
        1080  LOAD_CONST            3  1
        1083  BINARY_SUBSCR    
        1084  LOAD_ATTR            52  'is_zero'
        1087  POP_JUMP_IF_FALSE  1096  'to 1096'
        1090  LOAD_FAST            19  'point'
        1093  JUMP_FORWARD          7  'to 1103'
        1096  LOAD_FAST            25  'ret'
        1099  LOAD_CONST            3  1
        1102  BINARY_SUBSCR    
      1103_0  COME_FROM                '1093'
        1103  STORE_FAST           29  'valid_pos'

 208    1106  LOAD_GLOBAL           7  'math3d'
        1109  LOAD_ATTR            44  'vector'
        1112  LOAD_FAST            16  'forward'
        1115  LOAD_ATTR            45  'x'
        1118  LOAD_CONST            2  ''
        1121  LOAD_FAST            16  'forward'
        1124  LOAD_ATTR            46  'z'
        1127  CALL_FUNCTION_3       3 
        1130  STORE_FAST           30  'hori_forward'

 209    1133  LOAD_FAST            30  'hori_forward'
        1136  LOAD_ATTR            52  'is_zero'
        1139  POP_JUMP_IF_TRUE   1165  'to 1165'

 210    1142  LOAD_FAST            30  'hori_forward'
        1145  LOAD_ATTR            53  'normalize'
        1148  CALL_FUNCTION_0       0 
        1151  POP_TOP          

 211    1152  LOAD_FAST            29  'valid_pos'
        1155  LOAD_FAST            30  'hori_forward'
        1158  INPLACE_ADD      
        1159  STORE_FAST           29  'valid_pos'
        1162  JUMP_FORWARD          0  'to 1165'
      1165_0  COME_FROM                '1162'

 214    1165  LOAD_FAST             9  'mecha_pos'
        1168  LOAD_CONST            0  ''
        1171  COMPARE_OP            9  'is-not'
        1174  POP_JUMP_IF_FALSE  1206  'to 1206'
        1177  LOAD_FAST            29  'valid_pos'
        1180  LOAD_FAST             9  'mecha_pos'
        1183  BINARY_SUBTRACT  
        1184  LOAD_ATTR            54  'length'
        1187  LOAD_CONST            8  5
        1190  LOAD_GLOBAL          19  'NEOX_UNIT_SCALE'
        1193  BINARY_MULTIPLY  
        1194  COMPARE_OP            0  '<'
      1197_0  COME_FROM                '1174'
        1197  POP_JUMP_IF_FALSE  1206  'to 1206'

 215    1200  CONTINUE            299  'to 299'
        1203  JUMP_FORWARD          0  'to 1206'
      1206_0  COME_FROM                '1203'

 217    1206  LOAD_GLOBAL          48  'check_target_pos_behind_mecha'
        1209  LOAD_FAST            29  'valid_pos'
        1212  LOAD_FAST             9  'mecha_pos'
        1215  LOAD_FAST             2  'camera'
        1218  CALL_FUNCTION_3       3 
        1221  POP_JUMP_IF_FALSE  1230  'to 1230'

 218    1224  CONTINUE            299  'to 299'
        1227  JUMP_FORWARD          0  'to 1230'
      1230_0  COME_FROM                '1227'

 220    1230  LOAD_FAST            29  'valid_pos'
        1233  LOAD_GLOBAL           7  'math3d'
        1236  LOAD_ATTR            44  'vector'
        1239  LOAD_CONST            2  ''
        1242  LOAD_CONST            1  2
        1245  LOAD_CONST            2  ''
        1248  CALL_FUNCTION_3       3 
        1251  BINARY_ADD       
        1252  STORE_FAST           31  'check_valid_pos_s'

 221    1255  LOAD_FAST            29  'valid_pos'
        1258  LOAD_GLOBAL           7  'math3d'
        1261  LOAD_ATTR            44  'vector'
        1264  LOAD_CONST            2  ''
        1267  LOAD_CONST            3  1
        1270  LOAD_CONST            2  ''
        1273  CALL_FUNCTION_3       3 
        1276  BINARY_SUBTRACT  
        1277  STORE_FAST           32  'check_valid_pos_e'

 223    1280  LOAD_FAST             1  'scene'
        1283  LOAD_ATTR            33  'scene_col'
        1286  LOAD_ATTR            34  'hit_by_ray'
        1289  LOAD_FAST            31  'check_valid_pos_s'
        1292  LOAD_FAST            32  'check_valid_pos_e'
        1295  LOAD_CONST            2  ''
        1298  LOAD_FAST            13  'group'
        1301  LOAD_FAST            14  'mask'
        1304  LOAD_GLOBAL          35  'collision'
        1307  LOAD_ATTR            36  'INCLUDE_FILTER'
        1310  LOAD_GLOBAL          26  'False'
        1313  CALL_FUNCTION_7       7 
        1316  STORE_FAST           33  'valid_plane'

 224    1319  LOAD_FAST            33  'valid_plane'
        1322  LOAD_CONST            2  ''
        1325  BINARY_SUBSCR    
        1326  POP_JUMP_IF_FALSE  1343  'to 1343'

 225    1329  LOAD_FAST            29  'valid_pos'
        1332  LOAD_GLOBAL          49  'VALID_POS'
        1335  LOAD_GLOBAL           3  'active_camera'
        1338  BINARY_SUBTRACT  
        1339  STORE_SUBSCR     
        1340  JUMP_FORWARD          0  'to 1343'
      1343_0  COME_FROM                '1340'

 227    1343  BREAK_LOOP       
        1344  JUMP_ABSOLUTE      1350  'to 1350'
        1347  JUMP_BACK           299  'to 299'
        1350  JUMP_BACK           299  'to 299'
        1353  POP_BLOCK        

 229    1354  LOAD_FAST             8  'end_pos'
        1357  STORE_FAST           23  't_s_pos'

 230    1360  LOAD_FAST             8  'end_pos'
        1363  LOAD_GLOBAL           7  'math3d'
        1366  LOAD_ATTR            44  'vector'
        1369  LOAD_CONST            2  ''
        1372  LOAD_CONST            9  -10000
        1375  LOAD_CONST            2  ''
        1378  CALL_FUNCTION_3       3 
        1381  BINARY_ADD       
        1382  STORE_FAST           24  't_e_pos'

 231    1385  LOAD_FAST             1  'scene'
        1388  LOAD_ATTR            33  'scene_col'
        1391  LOAD_ATTR            34  'hit_by_ray'
        1394  LOAD_FAST            23  't_s_pos'
        1397  LOAD_FAST            24  't_e_pos'
        1400  LOAD_CONST            2  ''
        1403  LOAD_FAST            13  'group'
        1406  LOAD_FAST            14  'mask'
        1409  LOAD_GLOBAL          35  'collision'
        1412  LOAD_ATTR            36  'INCLUDE_FILTER'
        1415  LOAD_GLOBAL          26  'False'
        1418  CALL_FUNCTION_7       7 
        1421  STORE_FAST           25  'ret'

 232    1424  LOAD_FAST            25  'ret'
        1427  LOAD_CONST            2  ''
        1430  BINARY_SUBSCR    
        1431  POP_JUMP_IF_FALSE  1475  'to 1475'
        1434  LOAD_GLOBAL          48  'check_target_pos_behind_mecha'
        1437  LOAD_FAST            25  'ret'
        1440  LOAD_CONST            3  1
        1443  BINARY_SUBSCR    
        1444  LOAD_FAST             9  'mecha_pos'
        1447  LOAD_FAST             2  'camera'
        1450  CALL_FUNCTION_3       3 
        1453  UNARY_NOT        
      1454_0  COME_FROM                '1431'
        1454  POP_JUMP_IF_FALSE  1475  'to 1475'

 233    1457  LOAD_FAST            25  'ret'
        1460  LOAD_CONST            3  1
        1463  BINARY_SUBSCR    
        1464  LOAD_GLOBAL          49  'VALID_POS'
        1467  LOAD_GLOBAL           3  'active_camera'
        1470  BINARY_SUBTRACT  
        1471  STORE_SUBSCR     
        1472  JUMP_FORWARD         11  'to 1486'

 235    1475  LOAD_CONST            0  ''
        1478  LOAD_GLOBAL          49  'VALID_POS'
        1481  LOAD_GLOBAL           3  'active_camera'
        1484  BINARY_SUBTRACT  
        1485  STORE_SUBSCR     
      1486_0  COME_FROM                '286'
      1486_1  COME_FROM                '286'

 237    1486  LOAD_GLOBAL          55  'get_valid_jump_pos'
        1489  CALL_FUNCTION_0       0 
        1492  STORE_FAST           29  'valid_pos'

 239    1495  LOAD_GLOBAL          56  'DETECT_CALLBACK'
        1498  POP_JUMP_IF_FALSE  1520  'to 1520'
        1501  LOAD_FAST            29  'valid_pos'
      1504_0  COME_FROM                '1498'
        1504  POP_JUMP_IF_FALSE  1520  'to 1520'

 240    1507  LOAD_GLOBAL          56  'DETECT_CALLBACK'
        1510  LOAD_FAST            29  'valid_pos'
        1513  CALL_FUNCTION_1       1 
        1516  POP_TOP          
        1517  JUMP_FORWARD          0  'to 1520'
      1520_0  COME_FROM                '1517'
        1520  LOAD_CONST            0  ''
        1523  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 55


def detect_jump_pos_wrapper(*args):
    detect_jump_pos(1)
    detect_jump_pos(2)


def start_jump_pos_detect(unit, max_detect_dist, detect_callback=None):
    global DETECT_COL
    global DETECT_TIMES
    global DETECT_CALLBACK
    global MAX_DETECT_DIST
    DETECT_TIMES = 0
    MAX_DETECT_DIST = max_detect_dist
    if not DETECT_COL:
        DETECT_COL = collision.col_object(collision.SPHERE, math3d.vector(13, 13, 13), GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE)
    DETECT_CALLBACK = detect_callback
    unit.regist_event('E_DELTA_YAW', detect_jump_pos_wrapper)
    unit.regist_event('E_DELTA_PITCH', detect_jump_pos_wrapper)
    if G_POS_CHANGE_MGR:
        unit.regist_pos_change(detect_jump_pos_wrapper)
    else:
        unit.regist_event('E_POSITION', detect_jump_pos_wrapper)


def stop_jump_pos_detect(unit):
    global VALID_POS
    global DETECT_CALLBACK
    DETECT_CALLBACK = None
    VALID_POS = [None, None]
    unit.unregist_event('E_DELTA_YAW', detect_jump_pos_wrapper)
    unit.unregist_event('E_DELTA_PITCH', detect_jump_pos_wrapper)
    if G_POS_CHANGE_MGR:
        unit.unregist_pos_change(detect_jump_pos_wrapper)
    else:
        unit.unregist_event('E_POSITION', detect_jump_pos_wrapper)
    return


def check_in_house(pos):
    scn = world.get_active_scene()
    if scn.get_scene_info_2d(pos.x, pos.z) == MTL_HOUSE:
        s_pos = pos + math3d.vector(0, 1, 0) * 0.2 * NEOX_UNIT_SCALE
        e_pos = s_pos + math3d.vector(0, 1000, 0)
        ret = scn.scene_col.hit_by_ray(s_pos, e_pos, 0, 15, 15, collision.INCLUDE_FILTER, False)
        return ret[0]
    return False


def need_add_boost_dist_offset(pos, boost_dir, offset):
    scn = world.get_active_scene()
    b_dir = math3d.vector(boost_dir)
    ret = scn.scene_col.hit_by_ray(pos + UP_VECTOR, pos + UP_VECTOR + b_dir * offset, 0, 15, 15, collision.INCLUDE_FILTER, False)
    return not ret[0]


CONTAIN_MECHA_GROUP = GROUP_CHARACTER_INCLUDE | SLOPE_GROUP & ~WATER_GROUP
CONTAIN_MECHA_MASK = GROUP_CHARACTER_INCLUDE | SLOPE_GROUP & ~WATER_MASK

class CanContainMechaChecker(object):
    CHARACTER_SIZE_MAP = {}
    STATIC_TEST_COL_MAP = {}
    SWEEP_TEST_COL_MAP = {}

    def __init__(self, mecha_id):
        if mecha_id in CanContainMechaChecker.CHARACTER_SIZE_MAP:
            radius, half_height = CanContainMechaChecker.CHARACTER_SIZE_MAP[mecha_id]
        else:
            physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content', str(mecha_id))
            radius = physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2.0
            half_height = physic_conf['character_size'][1] * NEOX_UNIT_SCALE / 2.0 - radius + 1.0
            CanContainMechaChecker.CHARACTER_SIZE_MAP[mecha_id] = (radius, half_height)
        if (radius, half_height) in CanContainMechaChecker.STATIC_TEST_COL_MAP:
            self.static_test_col = CanContainMechaChecker.STATIC_TEST_COL_MAP[radius, half_height]
            self.sweep_test_col = CanContainMechaChecker.SWEEP_TEST_COL_MAP[radius]
        else:
            self.static_test_col = collision.col_object(collision.BOX, math3d.vector(radius, half_height + radius, radius), CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK)
            CanContainMechaChecker.STATIC_TEST_COL_MAP[radius, half_height] = self.static_test_col
            self.sweep_test_col = collision.col_object(collision.SPHERE, math3d.vector(radius, 0, 0), CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK)
            CanContainMechaChecker.SWEEP_TEST_COL_MAP[radius] = self.sweep_test_col
        self.static_col_center_offset = math3d.vector(0, radius + half_height, 0)
        self.sweep_test_offset = math3d.vector(0, half_height * 2, 0)
        self.get_unit_by_cid_func = None
        return

    def destroy(self):
        self.static_test_col = None
        self.sweep_test_col = None
        self.get_unit_by_cid_func = None
        return

    def check(self, pos, is_center_pos=False):
        if self.get_unit_by_cid_func is None:
            func = global_data.emgr.get_scene_find_unit_func.emit()
            if func:
                self.get_unit_by_cid_func = func[0]
            else:
                return False
        if is_center_pos:
            self.static_test_col.position = pos
        else:
            self.static_test_col.position = pos + self.static_col_center_offset
        ret = global_data.game_mgr.scene.scene_col.static_test(self.static_test_col, CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK, collision.INCLUDE_FILTER)
        if ret:
            for hit_col in ret:
                if hit_col.cid == self.static_test_col.cid:
                    continue
                if hasattr(hit_col, 'is_character') and hit_col.is_character:
                    continue
                hit_unit = self.get_unit_by_cid_func(hit_col.cid)
                if not hit_unit:
                    return False

        return True

    def check_with_sweep_test(self, pos):
        if self.get_unit_by_cid_func is None:
            func = global_data.emgr.get_scene_find_unit_func.emit()
            if func:
                self.get_unit_by_cid_func = func[0]
            else:
                return
        if self.check(pos):
            return pos
        else:
            center_pos = pos + self.static_col_center_offset
            ret = global_data.game_mgr.scene.scene_col.sweep_test(self.sweep_test_col, center_pos, center_pos + self.sweep_test_offset, CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK, 0, collision.INCLUDE_FILTER)
            if ret[0]:
                up_ratio = ret[3]
            else:
                up_ratio = 1.0
            ret = global_data.game_mgr.scene.scene_col.sweep_test(self.sweep_test_col, center_pos, center_pos - self.sweep_test_offset, CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK, 0, collision.INCLUDE_FILTER)
            if ret[0]:
                down_ratio = ret[3]
            else:
                down_ratio = 1.0
            if up_ratio + down_ratio < 1.0:
                return
            if up_ratio < down_ratio:
                return pos + self.sweep_test_offset * (up_ratio - 0.5)
            return pos - self.sweep_test_offset * (down_ratio - 0.5)
            return

    def check_with_sweep_test_by_center_pos(self, pos):
        if self.get_unit_by_cid_func is None:
            func = global_data.emgr.get_scene_find_unit_func.emit()
            if func:
                self.get_unit_by_cid_func = func[0]
            else:
                return
        if self.check(pos, is_center_pos=True):
            return pos - self.static_col_center_offset
        else:
            ret = global_data.game_mgr.scene.scene_col.sweep_test(self.sweep_test_col, pos, pos + self.sweep_test_offset, CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK, 0, collision.INCLUDE_FILTER)
            if ret and ret[0]:
                up_ratio = ret[3]
            else:
                up_ratio = 1.0
            ret = global_data.game_mgr.scene.scene_col.sweep_test(self.sweep_test_col, pos, pos - self.sweep_test_offset, CONTAIN_MECHA_GROUP, CONTAIN_MECHA_MASK, 0, collision.INCLUDE_FILTER)
            if ret and ret[0]:
                down_ratio = ret[3]
            else:
                down_ratio = 1.0
            if up_ratio + down_ratio < 1.0:
                return
            if up_ratio < down_ratio:
                return pos + self.sweep_test_offset * (up_ratio - 0.5) - self.static_col_center_offset
            return pos - self.sweep_test_offset * (down_ratio - 0.5) - self.static_col_center_offset
            return


TMP_DETECT_COL = None
POS_OFFSET = 0

def get_tmp_detect_col():
    global TMP_DETECT_COL
    global POS_OFFSET
    if not TMP_DETECT_COL or not TMP_DETECT_COL.valid:
        width = NEOX_UNIT_SCALE * 1.6
        height = 4 * NEOX_UNIT_SCALE
        bounding_box = math3d.vector(width, height, width)
        TMP_DETECT_COL = collision.col_object(collision.BOX, bounding_box, 0, 0)
        POS_OFFSET = height + NEOX_UNIT_SCALE
        scn = world.get_active_scene()
    return TMP_DETECT_COL


def clear_tmp_col():
    global TMP_DETECT_COL
    scn = world.get_active_scene()
    if TMP_DETECT_COL and TMP_DETECT_COL.valid:
        scn.scene_col.remove_object(TMP_DETECT_COL)
    TMP_DETECT_COL = None
    return


def can_teleport(pos, from_pos):
    scn = world.get_active_scene()
    camera = scn.active_camera
    _, y = camera.world_to_screen(pos)
    size = game3d.get_window_size()
    y = y * 1.0 / size[1]
    if y < 0.1 or y > 0.9:
        return False
    return True


def can_contain_mecha(pos):
    tmp_col = get_tmp_detect_col()
    tmp_col.position = pos + math3d.vector(0, POS_OFFSET, 0)
    scn = world.get_active_scene()
    result = scn.scene_col.static_test(tmp_col, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER) or []
    block_col_objs = []
    for col_obj in result:
        unit = global_data.emgr.scene_find_unit_event.emit(col_obj.cid)[0]
        if not unit:
            block_col_objs.append(col_obj)

    return len(block_col_objs) == 0


def _hit_by_ray(scn, start, end, add=True):
    ret = scn.scene_col.hit_by_ray(start, end, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
    return ret


UP_OFFSET_DIST = 6 * NEOX_UNIT_SCALE
MID_OFFSET_DIST = 3.5 * NEOX_UNIT_SCALE
DOWN_OFFSET_DIST = 1 * NEOX_UNIT_SCALE
LEFT_RIGHT_OFFSET_DIST = 1.5 * NEOX_UNIT_SCALE
MIN_VALID_DIST = 12 * NEOX_UNIT_SCALE

def can_teleport_8013_part_1(scn, pos, from_pos):
    vec = from_pos - pos
    if vec.is_zero:
        return False
    if vec.length < 0.5 * NEOX_UNIT_SCALE:
        return False
    vec.normalize()
    pos = pos + vec * 0.5 * NEOX_UNIT_SCALE
    ret = _hit_by_ray(scn, from_pos + UP_VECTOR * UP_OFFSET_DIST, pos + UP_VECTOR * UP_OFFSET_DIST, False)
    if ret and ret[0]:
        return False
    ret = _hit_by_ray(scn, from_pos + UP_VECTOR * DOWN_OFFSET_DIST, pos + UP_VECTOR * DOWN_OFFSET_DIST)
    if ret and ret[0]:
        return False
    right = UP_VECTOR.cross(-vec)
    ret = _hit_by_ray(scn, from_pos + UP_VECTOR * MID_OFFSET_DIST + right * LEFT_RIGHT_OFFSET_DIST, pos + UP_VECTOR * MID_OFFSET_DIST + right * LEFT_RIGHT_OFFSET_DIST)
    if ret and ret[0]:
        return False
    ret = _hit_by_ray(scn, from_pos + UP_VECTOR * MID_OFFSET_DIST - right * LEFT_RIGHT_OFFSET_DIST, pos + UP_VECTOR * MID_OFFSET_DIST - right * LEFT_RIGHT_OFFSET_DIST)
    if ret and ret[0]:
        return False
    ret = scn.scene_col.hit_by_ray(pos, pos + UP_VECTOR * MIN_VALID_DIST, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
    if ret and ret[0]:
        up_valid_dist = ret[1].y - pos.y
    else:
        return True
    ret = scn.scene_col.hit_by_ray(pos, pos - UP_VECTOR * MIN_VALID_DIST, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
    if ret and ret[1]:
        down_valid_dist = pos.y - ret[1].y
    else:
        return True
    if up_valid_dist + down_valid_dist >= MIN_VALID_DIST:
        return True
    return False


def can_teleport_8013_part_2(scn, pos, from_pos):
    camera = scn.active_camera
    offset_h = math3d.vector(0, 3 * NEOX_UNIT_SCALE, 0)
    start_pos = from_pos + offset_h * 2 + camera.rotation_matrix.right * NEOX_UNIT_SCALE * 1.2 - camera.rotation_matrix.forward * NEOX_UNIT_SCALE
    direct = start_pos - pos
    if not direct.is_zero:
        direct.normalize()
    end_pos = pos + direct * 1 + offset_h
    ret = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
    if ret and ret[0]:
        return False
    return can_contain_mecha(pos)


def can_teleport_8013(pos, from_pos):
    scn = world.get_active_scene()
    camera = scn.active_camera
    _, y = camera.world_to_screen(pos)
    size = game3d.get_window_size()
    y = y * 1.0 / size[1]
    if y < 0.1 or y > 0.9:
        return False
    if can_teleport_8013_part_1(scn, pos, from_pos):
        return True
    return can_teleport_8013_part_2(scn, pos, from_pos)


class DetectByRay(object):

    def __init__(self):
        self.max_detect_dist = 100 * NEOX_UNIT_SCALE
        self.max_search = 10
        self.detect_callback = None
        self.detect_times = 0
        self.detect_interval = 0.03
        self.last_detect_time = 0
        self.listen_unit = None
        self.detect_point_list = []
        self.miss_point_list = []
        return

    def destroy(self):
        self.listen_unit = None
        return

    def set_max_search_times(self, max_search):
        self.max_search = max_search

    def start_dir_detect(self, unit, dist, callback):
        self.listen_unit = unit
        self.max_detect_dist = dist
        self.detect_callback = callback
        self.detect_point_list = []
        self.miss_point_list = []
        self.listen_unit.regist_event('E_DELTA_YAW', self.do_hook_direct)
        self.listen_unit.regist_event('E_DELTA_PITCH', self.do_hook_direct)
        if G_POS_CHANGE_MGR:
            self.listen_unit.regist_pos_change(self.do_hook_direct)
        else:
            self.listen_unit.regist_event('E_POSITION', self.do_hook_direct)
        self.do_hook_direct()

    def stop_dir_detect(self):
        if self.listen_unit:
            self.listen_unit.unregist_event('E_DELTA_YAW', self.do_hook_direct)
            self.listen_unit.unregist_event('E_DELTA_PITCH', self.do_hook_direct)
            if G_POS_CHANGE_MGR:
                self.listen_unit.unregist_pos_change(self.do_hook_direct)
            else:
                self.listen_unit.unregist_event('E_POSITION', self.do_hook_direct)
            self.listen_unit = None
        return

    def do_hook_direct(self, *args):
        global DETECT_COL
        import time
        if not DETECT_COL:
            DETECT_COL = collision.col_object(collision.SPHERE, math3d.vector(13, 13, 13), GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE)
        now = time.time()
        if now - self.last_detect_time < self.detect_interval:
            return
        else:
            self.last_detect_time = now - self.detect_interval * 0.5
            scene = world.get_active_scene()
            camera = scene.active_camera
            ori_forward = camera.rotation_matrix.forward
            right = camera.rotation_matrix.right
            start_pos = camera.position + ori_forward * CAMERA_OFFSET * NEOX_UNIT_SCALE
            group = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
            mask = GROUP_CHARACTER_INCLUDE & ~WATER_MASK
            for i in range(self.max_search):
                forward = ori_forward
                if i > 0:
                    rot = math3d.rotation(0, 0, 0, 1)
                    rot.set_axis_angle(right, i * 1.0 / 2 * math.pi / 180)
                    forward = rot.rotate_vector(ori_forward)
                new_end_pos = start_pos + forward * self.max_detect_dist
                result = scene.scene_col.hit_by_ray(start_pos, new_end_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
                self.detect_times += 1
                if result[0]:
                    pos, normal = result[1], result[2]
                    self.detect_callback(pos, normal)
                    self.last_detect_time = now
                    break
            else:
                self.detect_callback(None, None)

            return