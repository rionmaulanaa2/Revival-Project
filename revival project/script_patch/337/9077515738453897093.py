# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/meadow_quality_level.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game3d
HIGH_LEVEL = 3
MID_LEVEL = 2
LOW_LEVEL = 1
NONE_LEVEL = 0
Adreno = {HIGH_LEVEL: [
              '650',
              '640',
              '630',
              '620'],
   MID_LEVEL: [
             '540',
             '618',
             '619',
             '616'],
   LOW_LEVEL: [
             '430',
             '530',
             '512',
             '612',
             '610',
             '418',
             '510'],
   NONE_LEVEL: [
              '509',
              '508',
              '330',
              '506',
              '320',
              '505',
              '405']
   }
Mali = {HIGH_LEVEL: [
              'G78',
              'G77',
              'G76'],
   MID_LEVEL: [
             'G57',
             'G52',
             'G72',
             'G71'],
   LOW_LEVEL: [
             'G51',
             'T880',
             'T760'],
   NONE_LEVEL: [
              'T628',
              'T860',
              'T830',
              'T624',
              'T604',
              'T860',
              'T760',
              'T720']
   }
Apple = {HIGH_LEVEL: [
              'A14',
              'A13',
              'A12',
              'A11'],
   MID_LEVEL: [
             'A10',
             'A9'],
   LOW_LEVEL: [
             'A8'],
   NONE_LEVEL: [
              'A7']
   }

def get_quality_level--- This code section failed: ---

 107       0  SETUP_LOOP           79  'to 82'
           3  LOAD_GLOBAL           0  'six'
           6  LOAD_ATTR             1  'iteritems'
           9  LOAD_FAST             1  'levels'
          12  CALL_FUNCTION_1       1 
          15  GET_ITER         
          16  FOR_ITER             45  'to 64'
          19  UNPACK_SEQUENCE_2     2 
          22  STORE_FAST            2  'quality_level'
          25  STORE_FAST            3  'cards'

 108      28  SETUP_LOOP           30  'to 61'
          31  LOAD_FAST             3  'cards'
          34  GET_ITER         
          35  FOR_ITER             22  'to 60'
          38  STORE_FAST            4  'card_name'

 109      41  LOAD_FAST             4  'card_name'
          44  LOAD_FAST             0  'vedio_card_info'
          47  COMPARE_OP            6  'in'
          50  POP_JUMP_IF_FALSE    35  'to 35'

 110      53  LOAD_FAST             2  'quality_level'
          56  RETURN_END_IF    
        57_0  COME_FROM                '50'
          57  JUMP_BACK            35  'to 35'
          60  POP_BLOCK        
        61_0  COME_FROM                '28'
          61  JUMP_BACK            16  'to 16'
          64  POP_BLOCK        

 112      65  LOAD_GLOBAL           2  'print'
          68  LOAD_CONST            1  '!!![Unkown Vedio Card Name]:'
          71  LOAD_CONST            2  '!!!'
          74  CALL_FUNCTION_3       3 
          77  POP_TOP          

 113      78  LOAD_GLOBAL           3  'MID_LEVEL'
          81  RETURN_VALUE     
        82_0  COME_FROM                '0'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 74


def get_default_quality_by_vedio_card(vedio_card_info):
    plat_form = game3d.get_platform()
    if plat_form == game3d.PLATFORM_IOS:
        quality_levels = Apple
    elif 'Mali' in vedio_card_info:
        quality_levels = Mali
    elif 'Adreno' in vedio_card_info:
        quality_levels = Adreno
    else:
        quality_levels = {}
    return get_quality_level(vedio_card_info, quality_levels)