# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/etree/TidyTools.py
from __future__ import absolute_import
from __future__ import print_function
import glob
import string
import os
import sys
from .ElementTree import ElementTree, Element
NS_XHTML = '{http://www.w3.org/1999/xhtml}'

def tidy--- This code section failed: ---

  41       0  LOAD_CONST            1  'tidy'
           3  LOAD_CONST            2  '-qn'
           6  LOAD_CONST            3  '-asxml'
           9  BUILD_LIST_3          3 
          12  STORE_FAST            2  'command'

  43      15  LOAD_FAST             1  'new_inline_tags'
          18  POP_JUMP_IF_FALSE    62  'to 62'

  44      21  LOAD_FAST             2  'command'
          24  LOAD_ATTR             0  'append'
          27  LOAD_CONST            4  '--new-inline-tags'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          

  45      34  LOAD_FAST             2  'command'
          37  LOAD_ATTR             0  'append'
          40  LOAD_GLOBAL           1  'string'
          43  LOAD_ATTR             2  'join'
          46  LOAD_FAST             1  'new_inline_tags'
          49  LOAD_CONST            5  ','
          52  CALL_FUNCTION_2       2 
          55  CALL_FUNCTION_1       1 
          58  POP_TOP          
          59  JUMP_FORWARD          0  'to 62'
        62_0  COME_FROM                '59'

  50      62  LOAD_GLOBAL           3  'os'
          65  LOAD_ATTR             4  'system'

  51      68  LOAD_CONST            6  '%s %s >%s.out 2>%s.err'
          71  LOAD_GLOBAL           1  'string'
          74  LOAD_ATTR             2  'join'
          77  LOAD_FAST             2  'command'
          80  CALL_FUNCTION_1       1 
          83  LOAD_FAST             0  'file'
          86  LOAD_FAST             0  'file'
          89  LOAD_FAST             0  'file'
          92  BUILD_TUPLE_4         4 
          95  BINARY_MODULO    
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          

  54     100  SETUP_EXCEPT         27  'to 130'

  55     103  LOAD_GLOBAL           5  'ElementTree'
         106  CALL_FUNCTION_0       0 
         109  STORE_FAST            3  'tree'

  56     112  LOAD_FAST             3  'tree'
         115  LOAD_ATTR             6  'parse'
         118  LOAD_ATTR             7  'print'
         121  BINARY_ADD       
         122  CALL_FUNCTION_1       1 
         125  POP_TOP          
         126  POP_BLOCK        
         127  JUMP_FORWARD         57  'to 187'
       130_0  COME_FROM                '100'

  57     130  POP_TOP          
         131  POP_TOP          
         132  POP_TOP          

  58     133  LOAD_GLOBAL           7  'print'
         136  LOAD_CONST            8  '*** %s:%s'
         139  LOAD_GLOBAL           8  'sys'
         142  LOAD_ATTR             9  'exc_info'
         145  CALL_FUNCTION_0       0 
         148  LOAD_CONST            9  2
         151  SLICE+2          
         152  BINARY_MODULO    
         153  CALL_FUNCTION_1       1 
         156  POP_TOP          

  59     157  LOAD_GLOBAL           7  'print'
         160  LOAD_CONST           10  '*** %s is not valid XML (check %s.err for info)'

  60     163  LOAD_FAST             0  'file'
         166  LOAD_FAST             0  'file'
         169  BUILD_TUPLE_2         2 
         172  BINARY_MODULO    
         173  CALL_FUNCTION_1       1 
         176  POP_TOP          

  61     177  LOAD_CONST            0  ''
         180  STORE_FAST            3  'tree'
         183  JUMP_FORWARD         73  'to 259'
         186  END_FINALLY      
       187_0  COME_FROM                '127'

  63     187  LOAD_GLOBAL           3  'os'
         190  LOAD_ATTR            11  'path'
         193  LOAD_ATTR            12  'isfile'
         196  LOAD_ATTR             7  'print'
         199  BINARY_ADD       
         200  CALL_FUNCTION_1       1 
         203  POP_JUMP_IF_FALSE   223  'to 223'

  64     206  LOAD_GLOBAL           3  'os'
         209  LOAD_ATTR            13  'remove'
         212  LOAD_ATTR             7  'print'
         215  BINARY_ADD       
         216  CALL_FUNCTION_1       1 
         219  POP_TOP          
         220  JUMP_FORWARD          0  'to 223'
       223_0  COME_FROM                '220'

  65     223  LOAD_GLOBAL           3  'os'
         226  LOAD_ATTR            11  'path'
         229  LOAD_ATTR            12  'isfile'
         232  LOAD_ATTR            11  'path'
         235  BINARY_ADD       
         236  CALL_FUNCTION_1       1 
         239  POP_JUMP_IF_FALSE   259  'to 259'

  66     242  LOAD_GLOBAL           3  'os'
         245  LOAD_ATTR            13  'remove'
         248  LOAD_ATTR            11  'path'
         251  BINARY_ADD       
         252  CALL_FUNCTION_1       1 
         255  POP_TOP          
         256  JUMP_FORWARD          0  'to 259'
       259_0  COME_FROM                '256'
       259_1  COME_FROM                '186'

  68     259  LOAD_FAST             3  'tree'
         262  RETURN_VALUE     

Parse error at or near `BINARY_ADD' instruction at offset 121


def getbody(file, **options):
    try:
        tree = tidy(*(file,), **options)
        if tree is None:
            return
    except IOError as v:
        print('***', v)
        return

    NS = NS_XHTML
    for node in tree.getiterator():
        if node.tag.startswith(NS):
            node.tag = node.tag[len(NS):]

    body = tree.getroot().find('body')
    return body


def getzonebody(file, **options):
    body = getbody(file, **options)
    if body is None:
        return
    else:
        if body.text and string.strip(body.text):
            title = Element('h1')
            title.text = string.strip(body.text)
            title.tail = '\n\n'
            body.insert(0, title)
        body.text = None
        return body


if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        for file in glob.glob(arg):
            print(file, '...', tidy(file))