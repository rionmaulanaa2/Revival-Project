# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/clan/ClanMember.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
from .ClanTitle import ClanTitle

class ClanMember(object):

    def __init__(self, bdict):
        super(ClanMember, self).__init__()
        self.title = bdict.get('title', ClanTitle.MASS)
        self.id = bdict.get('id', None)
        self.uid = bdict.get('uid', None)
        self.fashion_value = bdict.get('fashion_value', 0)
        self.active_ts = bdict.get('active_ts', int(tutil.time()))
        self.active_day = bdict.get('active_day', 0)
        self.history_point = bdict.get('history_point', 0)
        return

    def get_persistent_dict(self):
        return {'title': self.title,
           'id': self.id,
           'uid': self.uid,
           'history_point': self.history_point,
           'fashion_value': self.fashion_value,
           'active_ts': self.active_ts,
           'active_day': self.active_day
           }

    def get_client_dict(self, week_point, season_point):
        return {'title': self.title,
           'uid': self.uid,
           'week_point': week_point,
           'season_point': season_point
           }

    def get_id(self):
        return self.id

    def get_uid(self):
        return self.uid

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_history_point(self):
        return self.history_point

    def set_history_point(self, point):
        self.active_ts = int(tutil.time())
        self.history_point = point

    def update_active_day(self, day_no):
        if self.active_day != day_no:
            self.active_day = day_no
            return True
        return False

    def set_fashion_value(self, fashion_value):
        self.fashion_value = fashion_value

    def get_fashion_value(self):
        return self.fashion_value

    def get_active_timestamp(self):
        return self.active_ts