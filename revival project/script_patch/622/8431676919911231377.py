# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/firearm_sfx_mapping_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
SFX_PATH_LIST = []
SFX_PATH_MAP = {}
SFX_PATH_COUNT = 0
SCALE_DECIMAL_PLACE_COUNT = 2
SCALE_TO_INT_VALUE = int(pow(10, SCALE_DECIMAL_PLACE_COUNT))
SFX_PATH_ROUND_COUNT = 1
SCALE_BASE = 1
INVALID_SFX_INDEX = 1

def check_sfx_mapping_initialized--- This code section failed: ---

  23       0  LOAD_GLOBAL           0  'SFX_PATH_LIST'
           3  POP_JUMP_IF_FALSE    10  'to 10'

  24       6  LOAD_CONST            0  ''
           9  RETURN_END_IF    
        10_0  COME_FROM                '3'

  25      10  LOAD_GLOBAL           1  'confmgr'
          13  LOAD_ATTR             2  'get'
          16  LOAD_CONST            1  'firearm_res_mapping'
          19  CALL_FUNCTION_1       1 
          22  STORE_FAST            0  'normal_sfx_mapping'

  26      25  LOAD_GLOBAL           1  'confmgr'
          28  LOAD_ATTR             2  'get'
          31  LOAD_CONST            2  'mecha_skin_firearm_res_mapping'
          34  CALL_FUNCTION_1       1 
          37  STORE_FAST            1  'skin_sfx_mapping'

  27      40  LOAD_GLOBAL           0  'SFX_PATH_LIST'
          43  LOAD_ATTR             3  'extend'
          46  LOAD_ATTR             3  'extend'
          49  BINARY_SUBSCR    
          50  CALL_FUNCTION_1       1 
          53  POP_TOP          

  28      54  LOAD_GLOBAL           4  'SFX_PATH_MAP'
          57  LOAD_ATTR             5  'update'
          60  LOAD_ATTR             4  'SFX_PATH_MAP'
          63  BINARY_SUBSCR    
          64  CALL_FUNCTION_1       1 
          67  POP_TOP          

  29      68  LOAD_GLOBAL           6  'len'
          71  LOAD_GLOBAL           0  'SFX_PATH_LIST'
          74  CALL_FUNCTION_1       1 
          77  STORE_FAST            2  'normal_sfx_count'

  30      80  LOAD_GLOBAL           0  'SFX_PATH_LIST'
          83  LOAD_ATTR             3  'extend'
          86  LOAD_FAST             1  'skin_sfx_mapping'
          89  LOAD_CONST            3  'sfx_path_list'
          92  BINARY_SUBSCR    
          93  CALL_FUNCTION_1       1 
          96  POP_TOP          

  31      97  SETUP_LOOP           47  'to 147'
         100  LOAD_GLOBAL           7  'six'
         103  LOAD_ATTR             8  'iteritems'
         106  LOAD_FAST             1  'skin_sfx_mapping'
         109  LOAD_CONST            4  'sfx_path_map'
         112  BINARY_SUBSCR    
         113  CALL_FUNCTION_1       1 
         116  GET_ITER         
         117  FOR_ITER             26  'to 146'
         120  UNPACK_SEQUENCE_2     2 
         123  STORE_FAST            3  'key'
         126  STORE_FAST            4  'value'

  32     129  LOAD_FAST             4  'value'
         132  LOAD_FAST             2  'normal_sfx_count'
         135  BINARY_ADD       
         136  LOAD_GLOBAL           4  'SFX_PATH_MAP'
         139  LOAD_FAST             3  'key'
         142  STORE_SUBSCR     
         143  JUMP_BACK           117  'to 117'
         146  POP_BLOCK        
       147_0  COME_FROM                '97'

  33     147  LOAD_CONST            5  10
         150  STORE_FAST            5  'tmp_value'

  34     153  LOAD_GLOBAL           6  'len'
         156  LOAD_GLOBAL           0  'SFX_PATH_LIST'
         159  CALL_FUNCTION_1       1 
         162  STORE_GLOBAL          9  'SFX_PATH_COUNT'

  36     165  SETUP_LOOP           46  'to 214'
         168  LOAD_GLOBAL           9  'SFX_PATH_COUNT'
         171  LOAD_FAST             5  'tmp_value'
         174  BINARY_MODULO    
         175  LOAD_GLOBAL           9  'SFX_PATH_COUNT'
         178  COMPARE_OP            3  '!='
         181  POP_JUMP_IF_TRUE    200  'to 200'
         184  LOAD_FAST             5  'tmp_value'
         187  LOAD_CONST            6  1
         190  BINARY_SUBTRACT  
         191  LOAD_GLOBAL           9  'SFX_PATH_COUNT'
         194  COMPARE_OP            2  '=='
       197_0  COME_FROM                '181'
         197  POP_JUMP_IF_FALSE   213  'to 213'

  37     200  LOAD_FAST             5  'tmp_value'
         203  LOAD_CONST            5  10
         206  INPLACE_MULTIPLY 
         207  STORE_FAST            5  'tmp_value'
         210  JUMP_BACK           168  'to 168'
         213  POP_BLOCK        
       214_0  COME_FROM                '165'

  38     214  LOAD_FAST             5  'tmp_value'
         217  STORE_GLOBAL         10  'SFX_PATH_ROUND_COUNT'

  39     220  LOAD_CONST            7  1.0
         223  LOAD_GLOBAL          11  'SCALE_TO_INT_VALUE'
         226  BINARY_MULTIPLY  
         227  LOAD_GLOBAL          10  'SFX_PATH_ROUND_COUNT'
         230  BINARY_MULTIPLY  
         231  STORE_GLOBAL         12  'SCALE_BASE'

  40     234  LOAD_FAST             5  'tmp_value'
         237  LOAD_CONST            6  1
         240  BINARY_SUBTRACT  
         241  STORE_GLOBAL         13  'INVALID_SFX_INDEX'

Parse error at or near `BINARY_SUBSCR' instruction at offset 49


def encode_sfx_info(sfx_path, sfx_scale):
    global SFX_PATH_ROUND_COUNT
    global INVALID_SFX_INDEX
    sfx_scale_code = int(sfx_scale * SCALE_TO_INT_VALUE) * SFX_PATH_ROUND_COUNT
    sfx_path_code = SFX_PATH_MAP.get(sfx_path, INVALID_SFX_INDEX)
    return sfx_scale_code + sfx_path_code


def decode_sfx_info--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'type'
           3  LOAD_FAST             0  'code'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'str'
          12  COMPARE_OP            8  'is'
          15  POP_JUMP_IF_FALSE    55  'to 55'
          18  LOAD_FAST             0  'code'
          21  LOAD_ATTR             2  'endswith'
          24  LOAD_CONST            1  'L'
          27  CALL_FUNCTION_1       1 
        30_0  COME_FROM                '15'
          30  POP_JUMP_IF_FALSE    55  'to 55'

  51      33  POP_JUMP_IF_FALSE     2  'to 2'
          36  SLICE+2          
          37  STORE_FAST            0  'code'

  52      40  LOAD_GLOBAL           3  'int'
          43  LOAD_FAST             0  'code'
          46  CALL_FUNCTION_1       1 
          49  STORE_FAST            0  'code'
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

  54      55  LOAD_FAST             0  'code'
          58  LOAD_GLOBAL           4  'SFX_PATH_ROUND_COUNT'
          61  BINARY_MODULO    
          62  STORE_FAST            1  'sfx_path_code'

  55      65  LOAD_FAST             0  'code'
          68  LOAD_FAST             1  'sfx_path_code'
          71  BINARY_SUBTRACT  
          72  LOAD_GLOBAL           5  'SCALE_BASE'
          75  BINARY_DIVIDE    
          76  STORE_FAST            2  'sfx_scale_code'

  56      79  LOAD_FAST             1  'sfx_path_code'
          82  LOAD_GLOBAL           6  'SFX_PATH_COUNT'
          85  COMPARE_OP            5  '>='
          88  POP_JUMP_IF_FALSE    97  'to 97'
          91  LOAD_CONST            0  ''
          94  JUMP_FORWARD          7  'to 104'
          97  LOAD_GLOBAL           8  'SFX_PATH_LIST'
         100  LOAD_FAST             1  'sfx_path_code'
         103  BINARY_SUBSCR    
       104_0  COME_FROM                '94'
         104  LOAD_FAST             2  'sfx_scale_code'
         107  BUILD_TUPLE_2         2 
         110  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 33


def get_correspond_sfx_info_for_ai(wp_type, socket_name=None, acc_level=0):
    res_conf = confmgr.get('firearm_res_config', str(wp_type), default={})
    if not res_conf:
        return None
    else:
        sfx_path = res_conf['cSfxBulletFlying']
        sync_sfx_path = res_conf.get('cSfxBulletFlyingOther', sfx_path)
        if not sync_sfx_path:
            sync_sfx_path = sfx_path
        sfx_scale = 1.0
        if isinstance(sfx_path, (list, tuple)):
            sfx_path = sfx_path[acc_level]
            sync_sfx_path = sync_sfx_path[acc_level]
        elif isinstance(sfx_path, dict):
            sfx_path = sfx_path[socket_name]
            sync_sfx_path = sync_sfx_path[socket_name]
        return (sfx_path, sync_sfx_path, sfx_scale)


# global SFX_PATH_COUNT ## Warning: Unused global# global SCALE_BASE ## Warning: Unused global