# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/algorithm/traversal.py
from __future__ import absolute_import
import six

def traversal_dict(src_dict, prefix='', result=None):
    if result is None:
        result = {}
    for key, val in six.iteritems(src_dict):
        if isinstance(val, str):
            if prefix:
                skey = '%s.%s' % (prefix, key)
            else:
                skey = key
            result[skey] = val
        elif isinstance(val, dict):
            if prefix:
                next_prfix = '%s.%s' % (prefix, key)
            else:
                next_prfix = key
            traversal_dict(val, next_prfix, result)
        else:
            raise Exception('un known type for val %s' % type(val))

    return result