# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/cmd_benchmark.py
from __future__ import absolute_import
from six.moves import range

def start_benchmark--- This code section failed: ---

   9       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'math'
           9  STORE_DEREF           0  'math'

  10      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'math3d'
          21  STORE_DEREF           1  'math3d'

  13      24  LOAD_CONST            1  ''
          27  LOAD_CONST            2  ('Benchmarker',)
          30  IMPORT_NAME           2  'benchmarker'
          33  IMPORT_FROM           3  'Benchmarker'
          36  STORE_FAST            3  'Benchmarker'
          39  POP_TOP          

  15      40  LOAD_GLOBAL           4  'global_data'
          43  LOAD_ATTR             5  'game_mgr'
          46  LOAD_ATTR             6  'scene'
          49  LOAD_ATTR             7  'active_camera'
          52  STORE_DEREF           2  'cam'

  17      55  LOAD_FAST             3  'Benchmarker'
          58  LOAD_FAST             3  'Benchmarker'
          61  LOAD_CONST            4  30
          64  LOAD_CONST            5  'cycle'
          67  LOAD_FAST             1  'cycle'
          70  LOAD_CONST            6  'extra'
          73  LOAD_FAST             2  'extra'
          76  LOAD_CONST            7  'argv'
          79  LOAD_GLOBAL           8  'False'
          82  CALL_FUNCTION_1025  1025 
          85  SETUP_WITH          434  'to 522'
          88  STORE_FAST            4  'bench'

  18      91  LOAD_CONST           39  ('Haruhi', 'MikuruMikuru', 'Yuki', 'ItsukiItsukiItsukiItsukiItsuki', 'Kyon')
          94  UNPACK_SEQUENCE_5     5 
          97  STORE_DEREF           3  's1'
         100  STORE_DEREF           4  's2'
         103  STORE_DEREF           5  's3'
         106  STORE_DEREF           6  's4'
         109  STORE_DEREF           7  's5'

  21     112  LOAD_DEREF            2  'cam'
         115  LOAD_ATTR             9  'world_rotation_matrix'
         118  STORE_DEREF           8  'rot1'

  22     121  LOAD_DEREF            1  'math3d'
         124  LOAD_ATTR            10  'vector'
         127  LOAD_CONST           13  0.1
         130  LOAD_CONST           14  0.3
         133  LOAD_CONST           15  0.9
         136  CALL_FUNCTION_3       3 
         139  LOAD_DEREF            1  'math3d'
         142  LOAD_ATTR            10  'vector'
         145  LOAD_CONST           15  0.9
         148  LOAD_CONST           14  0.3
         151  LOAD_CONST           13  0.1
         154  CALL_FUNCTION_3       3 
         157  ROT_TWO          
         158  STORE_DEREF           9  'vec1'
         161  STORE_DEREF          10  'vec2'

  24     164  LOAD_FAST             4  'bench'
         167  LOAD_CONST            0  ''
         170  CALL_FUNCTION_1       1 
         173  LOAD_CONST               '<code_object _test1>'
         176  MAKE_FUNCTION_0       0 
         179  CALL_FUNCTION_1       1 
         182  STORE_FAST            5  '_test1'

  29     185  LOAD_FAST             4  'bench'
         188  LOAD_CONST           17  'str-join'
         191  CALL_FUNCTION_1       1 
         194  LOAD_CLOSURE          3  's1'
         197  LOAD_CLOSURE          4  's2'
         200  LOAD_CLOSURE          5  's3'
         203  LOAD_CLOSURE          6  's4'
         206  LOAD_CLOSURE          7  's5'
         212  LOAD_CONST               '<code_object _test2>'
         215  MAKE_CLOSURE_0        0 
         218  CALL_FUNCTION_1       1 
         221  STORE_FAST            6  '_test2'

  34     224  LOAD_FAST             4  'bench'
         227  LOAD_CONST           19  'str-concat'
         230  CALL_FUNCTION_1       1 
         233  LOAD_CLOSURE          3  's1'
         236  LOAD_CLOSURE          4  's2'
         239  LOAD_CLOSURE          5  's3'
         242  LOAD_CLOSURE          6  's4'
         245  LOAD_CLOSURE          7  's5'
         251  LOAD_CONST               '<code_object _test3>'
         254  MAKE_CLOSURE_0        0 
         257  CALL_FUNCTION_1       1 
         260  STORE_FAST            7  '_test3'

  39     263  LOAD_FAST             4  'bench'
         266  LOAD_CONST           21  'str-format'
         269  CALL_FUNCTION_1       1 
         272  LOAD_CLOSURE          3  's1'
         275  LOAD_CLOSURE          4  's2'
         278  LOAD_CLOSURE          5  's3'
         281  LOAD_CLOSURE          6  's4'
         284  LOAD_CLOSURE          7  's5'
         290  LOAD_CONST               '<code_object _test4>'
         293  MAKE_CLOSURE_0        0 
         296  CALL_FUNCTION_1       1 
         299  STORE_FAST            8  '_test4'

  59     302  LOAD_FAST             4  'bench'
         305  LOAD_CONST           23  'math_triangle'
         308  CALL_FUNCTION_1       1 
         311  LOAD_CLOSURE          0  'math'
         317  LOAD_CONST               '<code_object _test7>'
         320  MAKE_CLOSURE_0        0 
         323  CALL_FUNCTION_1       1 
         326  STORE_FAST            9  '_test7'

  64     329  LOAD_FAST             4  'bench'
         332  LOAD_CONST           25  'math_pow'
         335  CALL_FUNCTION_1       1 
         338  LOAD_CLOSURE          0  'math'
         344  LOAD_CONST               '<code_object _test8>'
         347  MAKE_CLOSURE_0        0 
         350  CALL_FUNCTION_1       1 
         353  STORE_FAST           10  '_test8'

  72     356  LOAD_FAST             4  'bench'
         359  LOAD_CONST           27  'math3d_vector'
         362  CALL_FUNCTION_1       1 
         365  LOAD_CLOSURE          1  'math3d'
         371  LOAD_CONST               '<code_object _test9>'
         374  MAKE_CLOSURE_0        0 
         377  CALL_FUNCTION_1       1 
         380  STORE_FAST           11  '_test9'

  81     383  LOAD_FAST             4  'bench'
         386  LOAD_CONST           29  'math3d_vector_transform'
         389  CALL_FUNCTION_1       1 
         392  LOAD_CLOSURE          1  'math3d'
         395  LOAD_CLOSURE          2  'cam'
         401  LOAD_CONST               '<code_object _test9_2>'
         404  MAKE_CLOSURE_0        0 
         407  CALL_FUNCTION_1       1 
         410  STORE_FAST           12  '_test9_2'

  88     413  LOAD_FAST             4  'bench'
         416  LOAD_CONST           31  'for'
         419  CALL_FUNCTION_1       1 
         422  LOAD_CONST               '<code_object _test10>'
         425  MAKE_FUNCTION_0       0 
         428  CALL_FUNCTION_1       1 
         431  STORE_FAST           13  '_test10'

  94     434  LOAD_FAST             4  'bench'
         437  LOAD_CONST           33  'rotation_matrix'
         440  CALL_FUNCTION_1       1 
         443  LOAD_CLOSURE          8  'rot1'
         446  LOAD_CLOSURE          2  'cam'
         452  LOAD_CONST               '<code_object _test11>'
         455  MAKE_CLOSURE_0        0 
         458  CALL_FUNCTION_1       1 
         461  STORE_FAST           14  '_test11'

  99     464  LOAD_FAST             4  'bench'
         467  LOAD_CONST           35  'matrix computation'
         470  CALL_FUNCTION_1       1 
         473  LOAD_CLOSURE          2  'cam'
         476  LOAD_CLOSURE          9  'vec1'
         479  LOAD_CLOSURE         10  'vec2'
         485  LOAD_CONST               '<code_object _test12>'
         488  MAKE_CLOSURE_0        0 
         491  CALL_FUNCTION_1       1 
         494  STORE_FAST           15  '_test12'

 107     497  LOAD_FAST             4  'bench'
         500  LOAD_CONST           37  'python computation'
         503  CALL_FUNCTION_1       1 
         506  LOAD_CONST               '<code_object _test13>'
         509  MAKE_FUNCTION_0       0 
         512  CALL_FUNCTION_1       1 
         515  STORE_FAST           16  '_test13'
         518  POP_BLOCK        
         519  LOAD_CONST            0  ''
       522_0  COME_FROM_WITH           '85'
         522  WITH_CLEANUP     
         523  END_FINALLY      
         524  LOAD_CONST            0  ''
         527  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1025' instruction at offset 82