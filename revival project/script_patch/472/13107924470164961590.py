# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieObject.py
Moviecls = {'_root': {}}

def MovieGroupCls(grouptype):

    def wrapper--- This code section failed: ---

   8       0  LOAD_DEREF            0  'grouptype'
           3  LOAD_GLOBAL           0  'Moviecls'
           6  COMPARE_OP            7  'not-in'
           9  POP_JUMP_IF_FALSE    29  'to 29'

   9      12  BUILD_MAP_1           1 
          15  BUILD_MAP_1           1 
          18  STORE_MAP        
          19  LOAD_GLOBAL           0  'Moviecls'
          22  LOAD_DEREF            0  'grouptype'
          25  STORE_SUBSCR     
          26  JUMP_FORWARD          0  'to 29'
        29_0  COME_FROM                '26'

  10      29  LOAD_FAST             0  'cls'
          32  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_MAP' instruction at offset 18

    return wrapper


def MovieTrackCls(tracktype, grouptype='_root'):

    def wrapper--- This code section failed: ---

  16       0  LOAD_DEREF            0  'grouptype'
           3  LOAD_GLOBAL           0  'Moviecls'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    59  'to 59'

  17      12  LOAD_DEREF            1  'tracktype'
          15  LOAD_GLOBAL           0  'Moviecls'
          18  LOAD_DEREF            0  'grouptype'
          21  BINARY_SUBSCR    
          22  COMPARE_OP            7  'not-in'
          25  POP_JUMP_IF_FALSE    59  'to 59'

  18      28  BUILD_MAP_2           2 
          31  BUILD_MAP_1           1 
          34  STORE_MAP        
          35  LOAD_CONST            2  'Track'
          38  LOAD_CONST            3  '_type'
          41  STORE_MAP        
          42  LOAD_GLOBAL           0  'Moviecls'
          45  LOAD_DEREF            0  'grouptype'
          48  BINARY_SUBSCR    
          49  LOAD_DEREF            1  'tracktype'
          52  STORE_SUBSCR     
          53  JUMP_ABSOLUTE        59  'to 59'
          56  JUMP_FORWARD          0  'to 59'
        59_0  COME_FROM                '56'

  19      59  LOAD_FAST             0  'cls'
          62  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_MAP' instruction at offset 34

    return wrapper


def getMovieCls(typename, grouptype='_root'):
    if typename in Moviecls:
        return (
         Moviecls[typename]['_cls'], 'Group')
    else:
        if typename in Moviecls[grouptype]:
            return (
             Moviecls[grouptype][typename]['_cls'], 'Track')
        if typename in Moviecls['_root']:
            return (
             Moviecls['_root'][typename]['_cls'], 'Track')
        return (None, '')
        return None


class MovieObject(object):

    def __init__(self):
        super(MovieObject, self).__init__()
        self.properties = dict()