# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/JsonConfig.py
from __future__ import absolute_import
import json

def parse(filename):
    configfile = open(filename)
    jsonconfig = json.load(configfile)
    configfile.close()
    return jsonconfig


def save--- This code section failed: ---

  15       0  LOAD_GLOBAL           0  'open'
           3  LOAD_GLOBAL           1  'json'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            2  'configFile'

  16      12  LOAD_GLOBAL           1  'json'
          15  LOAD_ATTR             2  'dump'
          18  LOAD_FAST             1  'jsonconfig'
          21  LOAD_FAST             2  'configFile'
          24  CALL_FUNCTION_2       2 
          27  POP_TOP          

  17      28  LOAD_FAST             2  'configFile'
          31  LOAD_ATTR             3  'close'
          34  CALL_FUNCTION_0       0 
          37  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6