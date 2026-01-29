# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/SortedDict.py
from __future__ import absolute_import
import six_ex
from six.moves import zip
import bisect
try:
    all
except NameError:

    def all(seq):
        for elem in seq:
            if not elem:
                return False
            return True


class SortedDict(dict):

    def __init__(self):
        super(SortedDict, self).__init__()
        self._sorted_key_list = []

    def __setitem__(self, key, value):
        if key not in self:
            bisect.insort(self._sorted_key_list, key)
        super(SortedDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        if key in self:
            self._sorted_key_list.remove(key)
        super(SortedDict, self).__delitem__(key)

    def __iter__(self):
        for key in self._sorted_key_list:
            yield key

    def __reversed__(self):
        self._sorted_key_list.reverse()

    def setdefault(self, key, value):
        if key in self:
            return
        self[key] = value

    def sorted_dict_items(self):
        return self._sorted_key_list

    def sorted_dict_values(self):
        return [ self[key] for key in self._sorted_key_list ]

    def sorted_dict_keys(self):
        return self._sorted_key_list

    def sorted_dict_iteritems(self):
        for key in self._sorted_key_list:
            yield (key, self[key])

    def reiteritems(self):
        for key in reversed(self._sorted_key_list):
            yield (
             key, self[key])

    def sorted_dict_iterkeys(self):
        return self.__iter__()

    def sorted_dict_itervalues(self):
        for key in self._sorted_key_list:
            yield self[key]

    def first(self):
        if len(self._sorted_key_list) <= 0:
            return None
        else:
            return self[self._sorted_key_list[0]]

    def last(self):
        if len(self._sorted_key_list) <= 0:
            return None
        else:
            return self[self._sorted_key_list[-1]]

    def __eq__(self, other):
        if isinstance(other, SortedDict):
            return len(self) == len(other) and all((p == q for p, q in zip(six_ex.keys(self), six_ex.keys(other))))
        return super(SortedDict, self).__eq__(self, other)