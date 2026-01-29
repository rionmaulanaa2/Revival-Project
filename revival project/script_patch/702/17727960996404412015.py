# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/algorithm/lrucache.py
from __future__ import generators
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import time
import sys
from heapq import heappush, heappop, heapify
__version__ = '1.0'
__all__ = ['CacheKeyError', 'LRUCache', 'DEFAULT_SIZE']
DEBUG = False
DEFAULT_SIZE = 16

class CacheKeyError(KeyError):
    pass


class LRUCache(object):

    class __Node(object):

        def __init__(self, key, obj, timestamp):
            object.__init__(self)
            self.key = key
            self.obj = obj
            self.atime = timestamp

        def __cmp__(self, other):
            return six_ex.compare(self.atime, other.atime)

        def __lt__(self, other):
            return self.atime < other.atime

        def __repr__(self):
            return '<%s %s => %s (accessed at %s)>' % (
             self.__class__, self.key, self.obj, self.atime)

    def __getseqn(self):
        seqn = self.__seqn_
        self.__seqn_ = seqn + 1
        return seqn

    __seqn = property(__getseqn)

    def __init__(self, size=DEFAULT_SIZE):
        if size <= 0:
            raise ValueError(size)
        elif type(size) is not type(DEFAULT_SIZE):
            raise TypeError(size)
        object.__init__(self)
        self.__heap = []
        self.__dict = {}
        self.__seqn_ = 0
        self.size = size

    def __len__(self):
        return len(self.__heap)

    def __contains__(self, key):
        return key in self.__dict

    def __setitem__(self, key, obj):
        if key in self.__dict:
            node = self.__dict[key]
            node.obj = obj
            node.atime = self.__seqn
            heapify(self.__heap)
        else:
            while len(self.__heap) >= self.size:
                lru = heappop(self.__heap)
                del self.__dict[lru.key]
                if DEBUG:
                    print('removing(setitem)-->', lru.obj)

            node = self.__Node(key, obj, self.__seqn)
            self.__dict[key] = node
            if DEBUG:
                print('inserting node-->', node.obj)
            heappush(self.__heap, node)

    def __getitem__(self, key):
        if key not in self.__dict:
            raise CacheKeyError(key)
        else:
            node = self.__dict[key]
            if DEBUG:
                print('retrieving-->', node.obj)
            node.atime = self.__seqn
            heapify(self.__heap)
            return node.obj

    def __delitem__(self, key):
        if key not in self.__dict:
            raise CacheKeyError(key)
        else:
            node = self.__dict[key]
            del self.__dict[key]
            if DEBUG:
                print('removing(delitem)-->', node.obj)
            self.__heap.remove(node)
            heapify(self.__heap)
            return node.obj

    def pop(self, key):
        if key not in self.__dict:
            raise CacheKeyError(key)
        else:
            node = self.__dict[key]
            del self.__dict[key]
            self.__heap.remove(node)
            heapify(self.__heap)
            return node.obj

    def __iter__(self):
        copy = self.__heap[:]
        while len(copy) > 0:
            node = heappop(copy)
            yield node.key

        if six.PY2:
            raise StopIteration
        else:
            return

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'size':
            while len(self.__heap) > value:
                lru = heappop(self.__heap)
                del self.__dict[lru.key]

    def __repr__(self):
        return '<%s (%d elements)>' % (str(self.__class__), len(self.__heap))

    def iterkeys(self):
        return self.__iter__()


if __name__ == '__main__':
    cache = LRUCache(25)
    print(cache)
    for i in range(50):
        cache[i] = str(i)

    print(cache)
    if 46 in cache:
        del cache[46]
    print(cache)
    cache.size = 10
    print(cache)
    cache[46] = '46'
    print(cache)
    print(len(cache))
    for c in cache:
        print(c)

    print(cache)
    for c in cache:
        print(c)