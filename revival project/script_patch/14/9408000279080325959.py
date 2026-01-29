# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/color_table.py
from __future__ import absolute_import
import six
import re
from common.cfg import confmgr
from data import c_color_table
FTLabelColorDict = {}
from data import c_color_table
FTLabelColorDict.update([ (shorthand, '%06x' % color_val) for shorthand, color_val in six.iteritems(c_color_table.data) ])
import re
pattern = '#(?P<color_code>[a-zA-Z]{2})'
hex_color = re.compile('0[xX]([\\w][\\w])([\\w][\\w])([\\w][\\w])')
hex_color2 = re.compile('0[xX]([\\w]+)')
hex_color_sim = re.compile('([\\w][\\w])([\\w][\\w])([\\w][\\w])')
hex_color_sim2 = re.compile('([\\w]+)')

def _get_table_color_val(color_code):
    color_code = color_code.upper()
    if color_code in c_color_table.data:
        return c_color_table.data[color_code]
    else:
        log_error("Can't find color %s in color table" % color_code)
        return 16711680


def get_color_val--- This code section failed: ---

  28       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_FAST             0  'color_str'
           6  LOAD_GLOBAL           1  'str'
           9  LOAD_GLOBAL           2  'six'
          12  LOAD_ATTR             3  'text_type'
          15  BUILD_TUPLE_2         2 
          18  CALL_FUNCTION_2       2 
          21  POP_JUMP_IF_TRUE     28  'to 28'

  29      24  LOAD_FAST             0  'color_str'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

  31      28  LOAD_FAST             0  'color_str'
          31  LOAD_ATTR             4  'startswith'
          34  LOAD_CONST            1  '#'
          37  CALL_FUNCTION_1       1 
          40  POP_JUMP_IF_TRUE     47  'to 47'

  32      43  LOAD_CONST            2  16711680
          46  RETURN_END_IF    
        47_0  COME_FROM                '40'

  33      47  RETURN_VALUE     
          48  PRINT_ITEM_TO    
          49  PRINT_ITEM_TO    
          50  SLICE+1          
          51  STORE_FAST            1  'color_code'

  34      54  LOAD_GLOBAL           5  '_get_table_color_val'
          57  LOAD_FAST             1  'color_code'
          60  CALL_FUNCTION_1       1 
          63  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 47


def format_color_replace(mstr):

    def _color_replace_check(matched):
        color_code = matched.group('color_code')
        color_code_upper = color_code.upper()
        if color_code_upper in FTLabelColorDict:
            return '#c' + FTLabelColorDict[color_code_upper]
        return '#' + color_code

    return re.sub(pattern, _color_replace_check, mstr)


def get_color_rgb(hex_str):
    if hex_str.startswith('0x') or hex_str.startswith('0X'):
        m = re.match(hex_color, hex_str)
    else:
        m = re.match(hex_color_sim, hex_str)
    if not m:
        return (255, 0, 0)
    return (
     int(m.group(1), 16), int(m.group(2), 16), int(m.group(3), 16))


def get_color_rgb_hex(hex_str):
    if hex_str.startswith('0x') or hex_str.startswith('0X'):
        m = re.match(hex_color2, hex_str)
    else:
        m = re.match(hex_color_sim2, hex_str)
    if not m:
        return 16711680
    return int(m.group(1), 16)