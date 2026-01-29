# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/__init__.py
__author__ = 'lxn3032'
engine_cls = None

def detect_engine--- This code section failed: ---

   9       0  SETUP_EXCEPT         54  'to 57'

  10       3  LOAD_CONST            1  -1
           6  LOAD_CONST            0  ''
           9  IMPORT_NAME           0  'BigWorld'
          12  STORE_FAST            0  'BigWorld'

  11      15  LOAD_GLOBAL           1  'hasattr'
          18  LOAD_GLOBAL           2  'safaia_bigworld'
          21  CALL_FUNCTION_2       2 
          24  POP_JUMP_IF_FALSE    53  'to 53'

  12      27  LOAD_CONST            1  -1
          30  LOAD_CONST            3  ('SafaiaBigWorld',)
          33  IMPORT_NAME           2  'safaia_bigworld'
          36  IMPORT_FROM           3  'SafaiaBigWorld'
          39  STORE_FAST            1  'SafaiaBigWorld'
          42  POP_TOP          

  13      43  LOAD_FAST             1  'SafaiaBigWorld'
          46  STORE_FAST            2  'cls'

  14      49  LOAD_FAST             2  'cls'
          52  RETURN_END_IF    
        53_0  COME_FROM                '24'
          53  POP_BLOCK        
          54  JUMP_FORWARD         17  'to 74'
        57_0  COME_FROM                '0'

  15      57  DUP_TOP          
          58  LOAD_GLOBAL           4  'ImportError'
          61  COMPARE_OP           10  'exception-match'
          64  POP_JUMP_IF_FALSE    73  'to 73'
          67  POP_TOP          
          68  POP_TOP          
          69  POP_TOP          

  16      70  JUMP_FORWARD          1  'to 74'
          73  END_FINALLY      
        74_0  COME_FROM                '73'
        74_1  COME_FROM                '54'

  18      74  SETUP_EXCEPT         42  'to 119'

  19      77  LOAD_CONST            1  -1
          80  LOAD_CONST            0  ''
          83  IMPORT_NAME           5  'MEngine'
          86  STORE_FAST            3  'MEngine'

  20      89  LOAD_CONST            1  -1
          92  LOAD_CONST            4  ('SafaiaMessiah',)
          95  IMPORT_NAME           6  'safaia_messiah'
          98  IMPORT_FROM           7  'SafaiaMessiah'
         101  STORE_FAST            4  'SafaiaMessiah'
         104  POP_TOP          

  21     105  LOAD_FAST             4  'SafaiaMessiah'
         108  STORE_FAST            2  'cls'

  22     111  LOAD_FAST             2  'cls'
         114  RETURN_VALUE     
         115  POP_BLOCK        
         116  JUMP_FORWARD         17  'to 136'
       119_0  COME_FROM                '74'

  23     119  DUP_TOP          
         120  LOAD_GLOBAL           4  'ImportError'
         123  COMPARE_OP           10  'exception-match'
         126  POP_JUMP_IF_FALSE   135  'to 135'
         129  POP_TOP          
         130  POP_TOP          
         131  POP_TOP          

  24     132  JUMP_FORWARD          1  'to 136'
         135  END_FINALLY      
       136_0  COME_FROM                '135'
       136_1  COME_FROM                '116'

  26     136  SETUP_EXCEPT         42  'to 181'

  27     139  LOAD_CONST            1  -1
         142  LOAD_CONST            0  ''
         145  IMPORT_NAME           8  'game3d'
         148  STORE_FAST            5  'game3d'

  28     151  LOAD_CONST            1  -1
         154  LOAD_CONST            5  ('SafaiaNeoX',)
         157  IMPORT_NAME           9  'safaia_neox'
         160  IMPORT_FROM          10  'SafaiaNeoX'
         163  STORE_FAST            6  'SafaiaNeoX'
         166  POP_TOP          

  29     167  LOAD_FAST             6  'SafaiaNeoX'
         170  STORE_FAST            2  'cls'

  30     173  LOAD_FAST             2  'cls'
         176  RETURN_VALUE     
         177  POP_BLOCK        
         178  JUMP_FORWARD         17  'to 198'
       181_0  COME_FROM                '136'

  31     181  DUP_TOP          
         182  LOAD_GLOBAL           4  'ImportError'
         185  COMPARE_OP           10  'exception-match'
         188  POP_JUMP_IF_FALSE   197  'to 197'
         191  POP_TOP          
         192  POP_TOP          
         193  POP_TOP          

  32     194  JUMP_FORWARD          1  'to 198'
         197  END_FINALLY      
       198_0  COME_FROM                '197'
       198_1  COME_FROM                '178'

  34     198  SETUP_EXCEPT         42  'to 243'

  35     201  LOAD_CONST            1  -1
         204  LOAD_CONST            0  ''
         207  IMPORT_NAME          11  'unreal_engine'
         210  STORE_FAST            7  'unreal_engine'

  36     213  LOAD_CONST            1  -1
         216  LOAD_CONST            6  ('SafaiaUE4',)
         219  IMPORT_NAME          12  'safaia_ue4'
         222  IMPORT_FROM          13  'SafaiaUE4'
         225  STORE_FAST            8  'SafaiaUE4'
         228  POP_TOP          

  37     229  LOAD_FAST             8  'SafaiaUE4'
         232  STORE_FAST            2  'cls'

  38     235  LOAD_FAST             2  'cls'
         238  RETURN_VALUE     
         239  POP_BLOCK        
         240  JUMP_FORWARD         17  'to 260'
       243_0  COME_FROM                '198'

  39     243  DUP_TOP          
         244  LOAD_GLOBAL           4  'ImportError'
         247  COMPARE_OP           10  'exception-match'
         250  POP_JUMP_IF_FALSE   259  'to 259'
         253  POP_TOP          
         254  POP_TOP          
         255  POP_TOP          

  40     256  JUMP_FORWARD          1  'to 260'
         259  END_FINALLY      
       260_0  COME_FROM                '259'
       260_1  COME_FROM                '240'

  42     260  SETUP_EXCEPT         42  'to 305'

  43     263  LOAD_CONST            1  -1
         266  LOAD_CONST            0  ''
         269  IMPORT_NAME          14  'Timer'
         272  STORE_FAST            9  'Timer'

  44     275  LOAD_CONST            1  -1
         278  LOAD_CONST            7  ('SafaiaMobileServer',)
         281  IMPORT_NAME          15  'safaia_mobile_server'
         284  IMPORT_FROM          16  'SafaiaMobileServer'
         287  STORE_FAST           10  'SafaiaMobileServer'
         290  POP_TOP          

  45     291  LOAD_FAST            10  'SafaiaMobileServer'
         294  STORE_FAST            2  'cls'

  46     297  LOAD_FAST             2  'cls'
         300  RETURN_VALUE     
         301  POP_BLOCK        
         302  JUMP_FORWARD         17  'to 322'
       305_0  COME_FROM                '260'

  47     305  DUP_TOP          
         306  LOAD_GLOBAL           4  'ImportError'
         309  COMPARE_OP           10  'exception-match'
         312  POP_JUMP_IF_FALSE   321  'to 321'
         315  POP_TOP          
         316  POP_TOP          
         317  POP_TOP          

  48     318  JUMP_FORWARD          1  'to 322'
         321  END_FINALLY      
       322_0  COME_FROM                '321'
       322_1  COME_FROM                '302'

  52     322  SETUP_EXCEPT         20  'to 345'

  53     325  LOAD_CONST            1  -1
         328  LOAD_CONST            8  ('SafaiaThreading',)
         331  IMPORT_NAME          17  'safaia_threading'
         334  IMPORT_FROM          18  'SafaiaThreading'
         337  STORE_FAST           11  'SafaiaThreading'
         340  POP_TOP          
         341  POP_BLOCK        
         342  JUMP_FORWARD         33  'to 378'
       345_0  COME_FROM                '322'

  54     345  DUP_TOP          
         346  LOAD_GLOBAL          19  'ModuleNotFoundError'
         349  COMPARE_OP           10  'exception-match'
         352  POP_JUMP_IF_FALSE   377  'to 377'
         355  POP_TOP          
         356  POP_TOP          
         357  POP_TOP          

  55     358  LOAD_CONST            9  1
         361  LOAD_CONST            8  ('SafaiaThreading',)
         364  IMPORT_NAME          17  'safaia_threading'
         367  IMPORT_FROM          18  'SafaiaThreading'
         370  STORE_FAST           11  'SafaiaThreading'
         373  POP_TOP          
         374  JUMP_FORWARD          1  'to 378'
         377  END_FINALLY      
       378_0  COME_FROM                '377'
       378_1  COME_FROM                '342'

  57     378  LOAD_FAST            11  'SafaiaThreading'
         381  STORE_FAST            2  'cls'

  58     384  LOAD_FAST             2  'cls'
         387  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21


def get_instance():
    global engine_cls
    if not engine_cls:
        engine_cls = detect_engine()
        print 'Using {}'.format(engine_cls.__name__)
    return engine_cls()


if __name__ == '__main__':
    import sys
    import time
    process = sys.argv[1]
    kw = {}
    if len(sys.argv) >= 3:
        kw['connect_addr'] = sys.argv[2].split(':')
        kw['connect_addr'][1] = int(kw['connect_addr'][1])
        kw['connect_addr'] = tuple(kw['connect_addr'])
    instance = get_instance()
    print kw
    instance.start(process, **kw)
    while True:
        time.sleep(5)