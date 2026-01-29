# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/dev_tools.py
from __future__ import absolute_import
from six.moves import range
import time
import sys
import struct
import world
import math3d
import zlib
MIN_LEVEL = 0
SEA_LEVEL = 10
MAX_LEVEL = 255

def export_path_mesh--- This code section failed: ---

  25       0  LOAD_GLOBAL           0  'time'
           3  LOAD_ATTR             0  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            4  't1'

  27      12  LOAD_GLOBAL           1  'world'
          15  LOAD_ATTR             2  'get_active_scene'
          18  CALL_FUNCTION_0       0 
          21  STORE_FAST            5  'scn'

  29      24  LOAD_FAST             3  'grid_size'
          27  LOAD_CONST            1  2
          30  BINARY_DIVIDE    
          31  STORE_FAST            6  'half_grid_size'

  30      34  LOAD_FAST             1  'w'
          37  UNARY_NEGATIVE   
          38  LOAD_CONST            1  2
          41  BINARY_DIVIDE    
          42  LOAD_FAST             6  'half_grid_size'
          45  BINARY_ADD       
          46  STORE_FAST            7  'start_x'

  31      49  LOAD_FAST             1  'w'
          52  LOAD_CONST            1  2
          55  BINARY_DIVIDE    
          56  STORE_FAST            8  'end_x'

  32      59  LOAD_FAST             2  'h'
          62  UNARY_NEGATIVE   
          63  LOAD_CONST            1  2
          66  BINARY_DIVIDE    
          67  LOAD_FAST             6  'half_grid_size'
          70  BINARY_ADD       
          71  STORE_FAST            9  'start_z'

  33      74  LOAD_FAST             2  'h'
          77  LOAD_CONST            1  2
          80  BINARY_DIVIDE    
          81  STORE_FAST           10  'end_z'

  36      84  BUILD_LIST_0          0 
          87  STORE_FAST           11  'h_rows'

  38      90  SETUP_LOOP          297  'to 390'
          93  LOAD_GLOBAL           3  'range'
          96  LOAD_FAST             7  'start_x'
          99  LOAD_FAST             8  'end_x'
         102  LOAD_FAST             3  'grid_size'
         105  CALL_FUNCTION_3       3 
         108  GET_ITER         
         109  FOR_ITER            277  'to 389'
         112  STORE_FAST           12  'z'

  40     115  BUILD_LIST_0          0 
         118  STORE_FAST           13  'h_row'

  42     121  SETUP_LOOP          249  'to 373'
         124  LOAD_GLOBAL           3  'range'
         127  LOAD_FAST             9  'start_z'
         130  LOAD_FAST            10  'end_z'
         133  LOAD_FAST             3  'grid_size'
         136  CALL_FUNCTION_3       3 
         139  GET_ITER         
         140  FOR_ITER            229  'to 372'
         143  STORE_FAST           14  'x'

  44     146  LOAD_GLOBAL           4  'math3d'
         149  LOAD_ATTR             5  'vector'
         152  LOAD_FAST            14  'x'
         155  LOAD_CONST            2  2000
         158  LOAD_FAST            12  'z'
         161  CALL_FUNCTION_3       3 
         164  STORE_FAST           15  'p0'

  45     167  LOAD_GLOBAL           4  'math3d'
         170  LOAD_ATTR             5  'vector'
         173  LOAD_CONST            3  ''
         176  LOAD_CONST            4  -3000
         179  LOAD_CONST            3  ''
         182  CALL_FUNCTION_3       3 
         185  STORE_FAST           16  'p0_dir'

  46     188  LOAD_GLOBAL           6  'MIN_LEVEL'
         191  STORE_FAST            2  'h'

  49     194  LOAD_FAST             5  'scn'
         197  LOAD_ATTR             7  'hit_models_by_ray_ex'
         200  LOAD_FAST            15  'p0'
         203  LOAD_FAST            16  'p0_dir'
         206  LOAD_GLOBAL           8  'True'
         209  LOAD_CONST            0  ''
         212  LOAD_GLOBAL          10  'False'
         215  CALL_FUNCTION_5       5 
         218  STORE_FAST           17  'hits'

  50     221  LOAD_FAST            17  'hits'
         224  POP_JUMP_IF_FALSE   258  'to 258'

  51     227  LOAD_FAST            17  'hits'
         230  LOAD_CONST            3  ''
         233  BINARY_SUBSCR    
         234  STORE_FAST           18  'hit'

  52     237  LOAD_CONST            2  2000
         240  LOAD_CONST            5  3000
         243  LOAD_FAST            18  'hit'
         246  LOAD_CONST            6  1
         249  BINARY_SUBSCR    
         250  BINARY_MULTIPLY  
         251  BINARY_SUBTRACT  
         252  STORE_FAST            2  'h'
         255  JUMP_FORWARD          0  'to 258'
       258_0  COME_FROM                '255'

  55     258  LOAD_FAST             5  'scn'
         261  LOAD_ATTR            11  'terrain'
         264  LOAD_ATTR            12  'get_height'
         267  LOAD_FAST            15  'p0'
         270  CALL_FUNCTION_1       1 
         273  STORE_FAST           19  'height'

  56     276  LOAD_FAST            19  'height'
         279  POP_JUMP_IF_FALSE   314  'to 314'

  57     282  LOAD_FAST            19  'height'
         285  LOAD_CONST            3  ''
         288  BINARY_SUBSCR    
         289  LOAD_FAST             2  'h'
         292  COMPARE_OP            4  '>'
         295  POP_JUMP_IF_FALSE   314  'to 314'

  58     298  LOAD_FAST            19  'height'
         301  LOAD_CONST            3  ''
         304  BINARY_SUBSCR    
         305  STORE_FAST            2  'h'
         308  JUMP_ABSOLUTE       314  'to 314'
         311  JUMP_FORWARD          0  'to 314'
       314_0  COME_FROM                '311'

  61     314  LOAD_FAST             2  'h'
         317  LOAD_GLOBAL          13  'SEA_LEVEL'
         320  COMPARE_OP            0  '<'
         323  POP_JUMP_IF_FALSE   335  'to 335'

  62     326  LOAD_GLOBAL          13  'SEA_LEVEL'
         329  STORE_FAST            2  'h'
         332  JUMP_FORWARD          0  'to 335'
       335_0  COME_FROM                '332'

  63     335  LOAD_FAST             2  'h'
         338  LOAD_GLOBAL          14  'MAX_LEVEL'
         341  COMPARE_OP            4  '>'
         344  POP_JUMP_IF_FALSE   356  'to 356'

  64     347  LOAD_GLOBAL          14  'MAX_LEVEL'
         350  STORE_FAST            2  'h'
         353  JUMP_FORWARD          0  'to 356'
       356_0  COME_FROM                '353'

  66     356  LOAD_FAST            13  'h_row'
         359  LOAD_ATTR            15  'append'
         362  LOAD_FAST             2  'h'
         365  CALL_FUNCTION_1       1 
         368  POP_TOP          
         369  JUMP_BACK           140  'to 140'
         372  POP_BLOCK        
       373_0  COME_FROM                '121'

  68     373  LOAD_FAST            11  'h_rows'
         376  LOAD_ATTR            15  'append'
         379  LOAD_FAST            13  'h_row'
         382  CALL_FUNCTION_1       1 
         385  POP_TOP          
         386  JUMP_BACK           109  'to 109'
         389  POP_BLOCK        
       390_0  COME_FROM                '90'

  70     390  LOAD_GLOBAL           0  'time'
         393  LOAD_ATTR             0  'time'
         396  CALL_FUNCTION_0       0 
         399  STORE_FAST           20  't2'

  73     402  SETUP_LOOP           43  'to 448'
         405  LOAD_FAST            11  'h_rows'
         408  GET_ITER         
         409  FOR_ITER             35  'to 447'
         412  STORE_FAST           13  'h_row'

  74     415  SETUP_LOOP           26  'to 444'
         418  LOAD_GLOBAL          16  'enumerate'
         421  LOAD_FAST            13  'h_row'
         424  CALL_FUNCTION_1       1 
         427  GET_ITER         
         428  FOR_ITER             12  'to 443'
         431  UNPACK_SEQUENCE_2     2 
         434  STORE_FAST           21  'i'
         437  STORE_FAST            2  'h'

  75     440  JUMP_BACK           428  'to 428'
         443  POP_BLOCK        
       444_0  COME_FROM                '415'
         444  JUMP_BACK           409  'to 409'
         447  POP_BLOCK        
       448_0  COME_FROM                '402'

  78     448  LOAD_GLOBAL          17  'struct'
         451  LOAD_ATTR            18  'pack'
         454  LOAD_CONST            7  'ii'
         457  LOAD_GLOBAL          19  'len'
         460  LOAD_FAST            11  'h_rows'
         463  CALL_FUNCTION_1       1 
         466  LOAD_GLOBAL          19  'len'
         469  LOAD_FAST            11  'h_rows'
         472  LOAD_CONST            3  ''
         475  BINARY_SUBSCR    
         476  CALL_FUNCTION_1       1 
         479  CALL_FUNCTION_3       3 
         482  STORE_FAST           22  'data'

  79     485  SETUP_LOOP           69  'to 557'
         488  LOAD_FAST            11  'h_rows'
         491  GET_ITER         
         492  FOR_ITER             61  'to 556'
         495  STORE_FAST           13  'h_row'

  80     498  LOAD_CONST            8  ''
         501  STORE_FAST           23  'row_data'

  81     504  SETUP_LOOP           36  'to 543'
         507  LOAD_FAST            13  'h_row'
         510  GET_ITER         
         511  FOR_ITER             28  'to 542'
         514  STORE_FAST            2  'h'

  82     517  LOAD_FAST            23  'row_data'
         520  LOAD_GLOBAL          17  'struct'
         523  LOAD_ATTR            18  'pack'
         526  LOAD_CONST            9  'B'
         529  LOAD_FAST             2  'h'
         532  CALL_FUNCTION_2       2 
         535  INPLACE_ADD      
         536  STORE_FAST           23  'row_data'
         539  JUMP_BACK           511  'to 511'
         542  POP_BLOCK        
       543_0  COME_FROM                '504'

  83     543  LOAD_FAST            22  'data'
         546  LOAD_FAST            23  'row_data'
         549  INPLACE_ADD      
         550  STORE_FAST           22  'data'
         553  JUMP_BACK           492  'to 492'
         556  POP_BLOCK        
       557_0  COME_FROM                '485'

  86     557  LOAD_GLOBAL          20  'zlib'
         560  LOAD_ATTR            21  'compress'
         563  LOAD_FAST            22  'data'
         566  CALL_FUNCTION_1       1 
         569  STORE_FAST           24  'com_data'

  89     572  LOAD_GLOBAL          22  'open'
         575  LOAD_GLOBAL          10  'False'
         578  CALL_FUNCTION_2       2 
         581  STORE_FAST           25  'f'

  90     584  LOAD_FAST            25  'f'
         587  LOAD_ATTR            23  'write'
         590  LOAD_FAST            24  'com_data'
         593  CALL_FUNCTION_1       1 
         596  POP_TOP          

  91     597  LOAD_FAST            25  'f'
         600  LOAD_ATTR            24  'close'
         603  CALL_FUNCTION_0       0 
         606  POP_TOP          

  94     607  LOAD_GLOBAL           0  'time'
         610  LOAD_ATTR             0  'time'
         613  CALL_FUNCTION_0       0 
         616  STORE_FAST           26  't3'
         619  LOAD_CONST            0  ''
         622  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 578