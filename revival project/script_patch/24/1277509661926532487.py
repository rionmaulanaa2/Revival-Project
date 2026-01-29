# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/richtext.py
from __future__ import absolute_import
import six
from six.moves import range
import re
import random
from cocosui import cc, ccui, ccs
from common.cfg import confmgr
import common.input.touch
from common.uisys.font_utils import GetMultiLangFontName
ColorDict = {'w': '<color=0xf3fafeff>',
   'r': '<color=0xe0382fff>',
   'g': '<color=0x12ff00ff>',
   'zy': '<color=0x0bb103ff>',
   'bl': '<color=0x8da5c3ff>',
   'y': '<color=0xffea00ff>',
   'b': '<color=0x009cffff>',
   'p': '<color=0xf223ffff>',
   'c': '<color=0x03f0ffff>',
   'b2': '<color=0x85feffff>',
   'j': '<color=0xff4223ff>',
   'o': '<color=0xff9c00ff>',
   'a': '<color=0xce6912ff>',
   'd': '<color=0x10868aff>',
   'n': '</color>'
   }
from data import c_color_table
ColorDict.update([ (shorthand, '<color=0x%06xff>' % color_val) for shorthand, color_val in six.iteritems(c_color_table.data) ])

def richtext(rstr, fontSize, size, fontFile='gui/fonts/fzy4jw.ttf', callback=None):
    rstr = format_richtext(rstr)
    fontFile = GetMultiLangFontName(fontFile)
    rt = ccui.RichText.create(rstr, fontFile, fontSize, size)
    if callback:

        def testTouch(element, touch, eventTouch):
            if eventTouch.getEventCode() == common.input.touch.TOUCH_EVENT_ENDED:
                callback(element.getTouchString())

        rt.setTouchEnabled(True)
        rt.setSwallowTouches(False)
        rt.addElementTouchEventListener(testTouch)
    return rt


def get_color_text--- This code section failed: ---

  65       0  LOAD_GLOBAL           0  'min'
           3  LOAD_GLOBAL           1  'len'
           6  LOAD_FAST             0  'smsg'
           9  CALL_FUNCTION_1       1 
          12  LOAD_CONST            1  2
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'max_length'

  66      21  SETUP_LOOP           80  'to 104'
          24  LOAD_GLOBAL           2  'range'
          27  LOAD_FAST             1  'max_length'
          30  LOAD_CONST            2  ''
          33  LOAD_CONST            3  -1
          36  CALL_FUNCTION_3       3 
          39  GET_ITER         
          40  FOR_ITER             60  'to 103'
          43  STORE_FAST            2  'i'

  67      46  STORE_FAST            2  'i'
          49  LOAD_FAST             2  'i'
          52  SLICE+3          
          53  STORE_FAST            3  'key'

  68      56  LOAD_GLOBAL           3  'ColorDict'
          59  LOAD_ATTR             4  'get'
          62  LOAD_FAST             3  'key'
          65  LOAD_ATTR             5  'lower'
          68  CALL_FUNCTION_0       0 
          71  LOAD_CONST            0  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            4  'color'

  69      80  LOAD_FAST             4  'color'
          83  POP_JUMP_IF_FALSE    40  'to 40'

  70      86  LOAD_FAST             4  'color'
          89  LOAD_FAST             0  'smsg'
          92  LOAD_FAST             2  'i'
          95  SLICE+1          
          96  BUILD_TUPLE_2         2 
          99  RETURN_END_IF    
       100_0  COME_FROM                '83'
         100  JUMP_BACK            40  'to 40'
         103  POP_BLOCK        
       104_0  COME_FROM                '21'

  71     104  LOAD_CONST            0  ''
         107  LOAD_FAST             0  'smsg'
         110  BUILD_TUPLE_2         2 
         113  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 46


def get_emote_text--- This code section failed: ---

  74       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'emote'
           9  LOAD_CONST            1  'emote'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'emote_dict'

  75      18  LOAD_GLOBAL           2  'min'
          21  LOAD_GLOBAL           3  'len'
          24  LOAD_FAST             0  'smsg'
          27  CALL_FUNCTION_1       1 
          30  LOAD_CONST            2  3
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'max_length'

  76      39  SETUP_LOOP           74  'to 116'
          42  LOAD_GLOBAL           4  'range'
          45  LOAD_FAST             2  'max_length'
          48  LOAD_CONST            3  ''
          51  LOAD_CONST            4  -1
          54  CALL_FUNCTION_3       3 
          57  GET_ITER         
          58  FOR_ITER             54  'to 115'
          61  STORE_FAST            3  'i'

  77      64  STORE_FAST            3  'i'
          67  LOAD_FAST             3  'i'
          70  SLICE+3          
          71  STORE_FAST            4  'key'

  78      74  LOAD_FAST             1  'emote_dict'
          77  LOAD_ATTR             1  'get'
          80  LOAD_FAST             4  'key'
          83  LOAD_CONST            0  ''
          86  CALL_FUNCTION_2       2 
          89  STORE_FAST            5  'num'

  79      92  LOAD_FAST             5  'num'
          95  POP_JUMP_IF_FALSE    58  'to 58'

  80      98  LOAD_FAST             5  'num'
         101  LOAD_FAST             0  'smsg'
         104  LOAD_FAST             3  'i'
         107  SLICE+1          
         108  BUILD_TUPLE_2         2 
         111  RETURN_END_IF    
       112_0  COME_FROM                '95'
         112  JUMP_BACK            58  'to 58'
         115  POP_BLOCK        
       116_0  COME_FROM                '39'

  81     116  LOAD_CONST            0  ''
         119  LOAD_FAST             0  'smsg'
         122  BUILD_TUPLE_2         2 
         125  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 64


def format_richtext(mstr):
    textlist = mstr.split('#')
    str_list = []
    str_list.append(textlist[0])
    for smsg in textlist[1:]:
        if len(smsg) == 0:
            continue
        str1, str2 = get_color_text(smsg)
        if str1:
            str_list.append(str1)
        else:
            str1, str2 = get_emote_text(smsg)
            if str1:
                str_list.append(str1)
        str_list.append(str2)

    mstr = ''.join(str_list)
    return mstr


def richtext_to_str--- This code section failed: ---

 107       0  LOAD_FAST             0  'text'
           3  STORE_FAST            1  'rich_text'

 108       6  LOAD_CONST            1  '#g<touch=(.*?)>(.*?)</touch>#n'
           9  STORE_FAST            2  'relink'

 109      12  LOAD_GLOBAL           0  're'
          15  LOAD_ATTR             1  'findall'
          18  LOAD_FAST             2  'relink'
          21  LOAD_FAST             1  'rich_text'
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            3  'arg_list'

 110      30  SETUP_LOOP          144  'to 177'
          33  LOAD_FAST             3  'arg_list'
          36  GET_ITER         
          37  FOR_ITER            136  'to 176'
          40  STORE_FAST            4  'arg'

 111      43  LOAD_FAST             1  'rich_text'
          46  LOAD_ATTR             2  'replace'
          49  LOAD_CONST            2  '#g<touch=%s>'
          52  LOAD_FAST             4  'arg'
          55  LOAD_CONST            3  ''
          58  BINARY_SUBSCR    
          59  BINARY_MODULO    
          60  LOAD_CONST            4  '['
          63  CALL_FUNCTION_2       2 
          66  STORE_FAST            1  'rich_text'

 112      69  LOAD_FAST             1  'rich_text'
          72  LOAD_ATTR             2  'replace'
          75  LOAD_CONST            5  '</touch>#n'
          78  LOAD_CONST            6  ']'
          81  CALL_FUNCTION_2       2 
          84  STORE_FAST            1  'rich_text'

 113      87  LOAD_CONST            7  '<u=(.*?)>(.*?)</u>'
          90  STORE_FAST            2  'relink'

 114      93  LOAD_GLOBAL           0  're'
          96  LOAD_ATTR             1  'findall'
          99  LOAD_FAST             2  'relink'
         102  LOAD_FAST             4  'arg'
         105  LOAD_CONST            8  1
         108  BINARY_SUBSCR    
         109  CALL_FUNCTION_2       2 
         112  STORE_FAST            5  'text_list'

 115     115  SETUP_LOOP           55  'to 173'
         118  LOAD_FAST             5  'text_list'
         121  GET_ITER         
         122  FOR_ITER             47  'to 172'
         125  STORE_FAST            0  'text'

 116     128  LOAD_FAST             1  'rich_text'
         131  LOAD_ATTR             2  'replace'
         134  LOAD_CONST            9  '<u=%s>'
         137  LOAD_CONST            3  ''
         140  BINARY_SUBSCR    
         141  BINARY_MODULO    
         142  LOAD_CONST           10  ''
         145  CALL_FUNCTION_2       2 
         148  STORE_FAST            1  'rich_text'

 117     151  LOAD_FAST             1  'rich_text'
         154  LOAD_ATTR             2  'replace'
         157  LOAD_CONST           11  '</u>'
         160  LOAD_CONST           10  ''
         163  CALL_FUNCTION_2       2 
         166  STORE_FAST            1  'rich_text'
         169  JUMP_BACK           122  'to 122'
         172  POP_BLOCK        
       173_0  COME_FROM                '115'
         173  JUMP_BACK            37  'to 37'
         176  POP_BLOCK        
       177_0  COME_FROM                '30'

 118     177  LOAD_FAST             1  'rich_text'
         180  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 145


# global ColorDict ## Warning: Unused global