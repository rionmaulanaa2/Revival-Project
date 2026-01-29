# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/random_utils.py
from __future__ import absolute_import
import six
import six_ex
import random

def random_value_from_dict(random_dict):
    sum_rate = sum(six_ex.values(random_dict))
    rate = random.randint(1, sum_rate)
    for value, p in six.iteritems(random_dict):
        if p == 0:
            continue
        if rate <= p:
            return value
        rate -= p

    return random_dict.keys[0]