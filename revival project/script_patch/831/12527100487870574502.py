# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/gen_pro_info.py
from __future__ import absolute_import
from __future__ import print_function
import six
HEADER = "# -*- coding=utf-8 -*-\n# proto_info.py\n\n'''\n@Auto-Generated\nidx-salt\xe5\x9c\xa8\xe8\xbf\x99\xe9\x87\x8c\xef\xbc\x8c\xe6\x96\xb9\xe4\xbe\xbf\xe7\x94\x9f\xe6\x88\x90\n'''\n\n"
import os
import re
DIRS = [
 'client', 'server']
FILE_NAME = 'proto_info.py'
FILE_NAME_SALT = 'proto_salt.py'

def write_file--- This code section failed: ---

  31       0  LOAD_GLOBAL           0  'open'
           3  LOAD_GLOBAL           1  'write'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            2  'f'

  32      12  LOAD_FAST             2  'f'
          15  LOAD_ATTR             1  'write'
          18  LOAD_GLOBAL           2  'HEADER'
          21  CALL_FUNCTION_1       1 
          24  POP_TOP          

  34      25  SETUP_LOOP           80  'to 108'
          28  LOAD_GLOBAL           3  'six'
          31  LOAD_ATTR             4  'iteritems'
          34  LOAD_FAST             1  'mp_proto'
          37  CALL_FUNCTION_1       1 
          40  GET_ITER         
          41  FOR_ITER             63  'to 107'
          44  UNPACK_SEQUENCE_2     2 
          47  STORE_FAST            3  'k'
          50  STORE_FAST            4  'v'

  35      53  LOAD_FAST             2  'f'
          56  LOAD_ATTR             1  'write'
          59  LOAD_CONST            2  '\n'
          62  CALL_FUNCTION_1       1 
          65  POP_TOP          

  36      66  LOAD_FAST             2  'f'
          69  LOAD_ATTR             1  'write'
          72  LOAD_CONST            3  '{} = {}'
          75  LOAD_ATTR             5  'format'
          78  LOAD_FAST             3  'k'
          81  LOAD_FAST             4  'v'
          84  CALL_FUNCTION_2       2 
          87  CALL_FUNCTION_1       1 
          90  POP_TOP          

  37      91  LOAD_FAST             2  'f'
          94  LOAD_ATTR             1  'write'
          97  LOAD_CONST            2  '\n'
         100  CALL_FUNCTION_1       1 
         103  POP_TOP          
         104  JUMP_BACK            41  'to 41'
         107  POP_BLOCK        
       108_0  COME_FROM                '25'

  43     108  LOAD_FAST             2  'f'
         111  LOAD_ATTR             6  'close'
         114  CALL_FUNCTION_0       0 
         117  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def walk_files(s_path, d_type):
    arr = []
    for root, dirs, files in os.walk('{}/{}/'.format(s_path, d_type), topdown=False):
        for name in files:
            if not name.endswith('proto.py'):
                continue
            p = os.path.join(root, name)
            lst = find_func(p)
            arr.extend(lst)

    return arr


def find_func--- This code section failed: ---

  59       0  LOAD_GLOBAL           0  'open'
           3  LOAD_GLOBAL           1  'read'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            1  'f'

  60      12  LOAD_FAST             1  'f'
          15  LOAD_ATTR             1  'read'
          18  CALL_FUNCTION_0       0 
          21  STORE_FAST            2  'content'

  61      24  LOAD_FAST             1  'f'
          27  LOAD_ATTR             2  'close'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

  62      34  LOAD_GLOBAL           3  're'
          37  LOAD_ATTR             4  'findall'
          40  LOAD_CONST            2  '(?<!# )def (\\w+)\\('
          43  LOAD_FAST             2  'content'
          46  CALL_FUNCTION_2       2 
          49  STORE_FAST            3  'res'

  63      52  LOAD_FAST             3  'res'
          55  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def get_proto(s_path='./'):
    mp_proto = {}
    for d_type in DIRS:
        key = '{}_proto'.format(d_type)
        mp_proto[key] = walk_files(s_path, d_type)

    total = 0
    for d_type, info in six.iteritems(mp_proto):
        l = len(info)
        print('{}: {}'.format(d_type, l))
        total += l

    print('Done.! total = {}'.format(total))
    return mp_proto


def gen_proto():
    mp_proto = get_proto()
    write_file(FILE_NAME, mp_proto)


def get_salt():
    mp_proto = get_proto()
    import sys
    sys.path.append('../../')
    from common_utils.idx_utils import IdxReflect
    mp_salt = {}
    for d_type, names in six.iteritems(mp_proto):
        mp_salt[d_type] = IdxReflect(d_type, names).salt

    return mp_salt


def gen_salt():
    mp_salt = get_salt()
    write_file(FILE_NAME_SALT, mp_salt)
    print('gen_salt OK! mp_salt = {}'.format(mp_salt))


if __name__ == '__main__':
    gen_salt()