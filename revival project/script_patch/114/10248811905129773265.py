# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/package_type.py
from __future__ import absolute_import
import C_file
import six.moves.builtins
TEST_PACKAGE_DESC = 'TEST_PACKAGE'
APPLE_JUDGE_PACKAGE_DESC = 'APPLE_JUDGE_PACKAGE'
ANDROID_JUDGE_PACKAGE_DESC = 'ANDROID_JUDGE_PACKAGE'
GOV_JUDGE_PACKAGE_DESC = 'GOV_JUDGE_PACKAGE_DESC'
RECOMMEND_PACKAGE_DESC = 'RECOMMEND_PACKAGE'
NORMAL_PACKAGE_DESC = 'normal'
TF_PACKAGE_DESC = 'TF'
PACKAGE_LIMIT_PREFIX = 'PACKAGE_LIMIT_'
PACKAGE_LIMIT_DICT = {'\xe5\x86\x85\xe6\xb5\x8b': TEST_PACKAGE_DESC,
   '\xe8\x8b\xb9\xe6\x9e\x9c\xe5\xae\xa1\xe6\xa0\xb8': APPLE_JUDGE_PACKAGE_DESC,
   '\xe5\xae\x89\xe5\x8d\x93\xe5\xae\xa1\xe6\xa0\xb8': ANDROID_JUDGE_PACKAGE_DESC,
   '\xe7\x89\x88\xe7\xbd\xb2\xe5\xae\xa1\xe6\xa0\xb8': GOV_JUDGE_PACKAGE_DESC,
   '\xe6\x8e\xa8\xe8\x8d\x90\xe5\xae\xa1\xe6\xa0\xb8': RECOMMEND_PACKAGE_DESC
   }

def get_package_desc():
    return six.moves.builtins.__dict__.get('ACE_PACKAGE_TYPE', NORMAL_PACKAGE_DESC)


def is_inner_package():
    return six.moves.builtins.__dict__.get('ACE_PACKAGE_INNER', 0)


def is_normal_package():
    return get_package_desc() == 'normal'


def is_dev_package():
    return bool(__debug__)


def is_android_dds_package--- This code section failed: ---

  46       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('patch_utils',)
           6  IMPORT_NAME           0  'patch'
           9  IMPORT_FROM           1  'patch_utils'
          12  STORE_FAST            0  'patch_utils'
          15  POP_TOP          

  47      16  LOAD_GLOBAL           2  'hasattr'
          19  LOAD_GLOBAL           3  'is_android_dds_package'
          22  CALL_FUNCTION_2       2 
          25  POP_JUMP_IF_FALSE    38  'to 38'

  48      28  LOAD_FAST             0  'patch_utils'
          31  LOAD_ATTR             3  'is_android_dds_package'
          34  CALL_FUNCTION_0       0 
          37  RETURN_END_IF    
        38_0  COME_FROM                '25'

  50      38  LOAD_GLOBAL           4  'bool'
          41  LOAD_GLOBAL           5  'C_file'
          44  LOAD_ATTR             6  'find_res_file'
          47  LOAD_CONST            4  'android_dds_package.flag'
          50  LOAD_CONST            5  ''
          53  CALL_FUNCTION_2       2 
          56  CALL_FUNCTION_1       1 
          59  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 22