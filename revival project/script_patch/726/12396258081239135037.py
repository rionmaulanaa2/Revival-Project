# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/Statistics.py
from __future__ import absolute_import
import six

class Statistics(object):

    def __init__(self, logger):
        super(Statistics, self).__init__()
        self.logger = logger
        self._data = {}
        self._props = []
        self._methods = None
        self._init_method()
        return

    def destroy(self):
        self.logger = None
        self._data = None
        self._props = None
        self._methods = None
        return

    def init_from_dict(self, bdict):
        self._data = bdict.get('data', {})
        self._props = bdict.get('props', [])

    def get_persistent_dict(self):
        return {'data': self._data,
           'props': self._props
           }

    def update(self, stype, from_eid, to_eid, value):
        pass

    def clear(self):
        self._data = {}

    def is_dirty(self):
        return len(self._data) > 0

    def show(self):
        pass

    def get_props(self):
        return self._props

    def register_prop(self, prop):
        pass

    def _init_method(self):
        self._methods = {'add': self._m_add,
           'sub': self._m_sub,
           'mul': self._m_mul,
           'div': self._m_div,
           'max': self._m_max,
           'min': self._m_min,
           'set': self._m_set,
           'apd': self._m_apd,
           'uda': self._m_uda,
           'knt': self._m_knt,
           'udt': self._m_udt,
           'ududa': self._m_ududa,
           'udap': self._m_udap,
           'udas': self._m_udas
           }

    def _m_add(self, a, b, init):
        return a + b

    def _m_sub(self, a, b, init):
        return max(0, a - b)

    def _m_mul(self, a, b, init):
        return a * b

    def _m_div(self, a, b, init):
        try:
            return a / b
        except:
            return 0

    def _m_max(self, a, b, init):
        return max(a, b)

    def _m_min(self, a, b, init):
        if init and a <= 0:
            return b
        return min(a, b)

    def _m_set(self, a, b, init):
        return b

    def _m_apd(self, a, b, init):
        a.append(b)
        return a

    def _m_uda(self, a, b, init):
        if init:
            return b
        for key, value in six.iteritems(b):
            a.setdefault(key, 0)
            a[key] = a[key] + value

        return a

    def _m_knt(self, a, b, init):
        a.setdefault(b, 0)
        a[b] += 1
        return a

    def _m_udt(self, a, b, init):
        for key in six.iterkeys(b):
            a.setdefault(key, 0)
            a[key] = 1

        return a

    def _m_ududa(self, a, b, init):
        for key, data_dict in six.iteritems(b):
            a.setdefault(key, {})
            for sub_key, value in six.iteritems(data_dict):
                a[key].setdefault(sub_key, 0)
                a[key][sub_key] += value

        return a

    def _m_udap(self, a, b, init):
        for key, data in six.iteritems(b):
            a.setdefault(key, [])
            a[key].append(data)

        return a

    def _m_udas(self, a, b, init):
        for key, data in six.iteritems(b):
            a.setdefault(key, [])
            if data not in a[key]:
                a[key].append(data)

        return a