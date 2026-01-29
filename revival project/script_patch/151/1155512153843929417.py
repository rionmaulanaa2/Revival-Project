# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/etree/SimpleXMLTreeBuilder.py
from __future__ import absolute_import
from .. import xmllib
import string
from . import ElementTree

class TreeBuilder(xmllib.XMLParser):

    def __init__--- This code section failed: ---

  74       0  LOAD_GLOBAL           0  'ElementTree'
           3  LOAD_ATTR             1  'TreeBuilder'
           6  CALL_FUNCTION_0       0 
           9  LOAD_FAST             0  'self'
          12  STORE_ATTR            2  '__builder'

  75      15  LOAD_FAST             1  'html'
          18  POP_JUMP_IF_FALSE    61  'to 61'

  76      21  LOAD_CONST            1  ''
          24  LOAD_CONST            0  ''
          27  IMPORT_NAME           3  'six.moves.html_entities'
          30  STORE_FAST            2  'six'

  77      33  LOAD_FAST             0  'self'
          36  LOAD_ATTR             4  'entitydefs'
          39  LOAD_ATTR             5  'update'
          42  LOAD_FAST             2  'six'
          45  LOAD_ATTR             6  'moves'
          48  LOAD_ATTR             7  'html_entities'
          51  LOAD_ATTR             4  'entitydefs'
          54  CALL_FUNCTION_1       1 
          57  POP_TOP          
          58  JUMP_FORWARD          0  'to 61'
        61_0  COME_FROM                '58'

  78      61  LOAD_GLOBAL           8  'xmllib'
          64  LOAD_ATTR             9  'XMLParser'
          67  LOAD_ATTR            10  '__init__'
          70  LOAD_ATTR             2  '__builder'
          73  LOAD_GLOBAL          11  'True'
          76  CALL_FUNCTION_257   257 
          79  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 76

    def feed(self, data):
        xmllib.XMLParser.feed(self, data)

    def close(self):
        xmllib.XMLParser.close(self)
        return self.__builder.close()

    def handle_data(self, data):
        self.__builder.data(data)

    handle_cdata = handle_data

    def unknown_starttag(self, tag, attrs):
        attrib = {}
        for key, value in attrs.items():
            attrib[fixname(key)] = value

        self.__builder.start(fixname(tag), attrib)

    def unknown_endtag(self, tag):
        self.__builder.end(fixname(tag))


def fixname--- This code section failed: ---

 116       0  LOAD_CONST            1  ' '
           3  LOAD_FAST             0  'name'
           6  COMPARE_OP            7  'not-in'
           9  POP_JUMP_IF_FALSE    16  'to 16'

 117      12  LOAD_FAST             0  'name'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 118      16  LOAD_CONST            2  '{%s}%s'
          19  LOAD_GLOBAL           0  'tuple'
          22  LOAD_FAST             1  'split'
          25  LOAD_FAST             1  'split'
          28  LOAD_CONST            3  1
          31  CALL_FUNCTION_3       3 
          34  CALL_FUNCTION_1       1 
          37  BINARY_MODULO    
          38  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_MODULO' instruction at offset 37


if __name__ == '__main__':
    import sys
    p = TreeBuilder()
    text = "    <root xmlns='default'>\n       <tag attribute='value' />\n    </root>\n    "
    p.feed(text)
    tree = p.close()
    status = []
    tag = tree.find('{default}tag')
    if tag is None:
        status.append('namespaces not supported')
    if tag is not None and tag.get('{default}attribute'):
        status.append('default namespace applied to unqualified attribute')
    if status:
        print "xmllib doesn't work properly in this Python version:"
        for bug in status:
            print (
             '-', bug)

    else:
        print 'congratulations; no problems found in xmllib'