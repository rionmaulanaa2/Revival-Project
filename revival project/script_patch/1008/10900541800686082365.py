# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/identification.py
from __future__ import absolute_import
import script

class IdCalculater(object):

    def __init__(self):
        self.idmap_server = {}
        self.idmap_client = {}

    def calc(self, idtype):
        if script.is_client():
            return self.calc_client(idtype)
        else:
            return self.calc_server(idtype)

    def calc_server(self, idtype):
        i = self.idmap_server.get(idtype, 0) + 1
        if i > 2147483646:
            i = 1
        self.idmap_server[idtype] = i
        return i

    def calc_client(self, idtype):
        i = self.idmap_client.get(idtype, 0) - 1
        if i < -2147483647:
            i = -1
        self.idmap_client[idtype] = i
        return i