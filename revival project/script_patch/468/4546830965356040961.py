# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/JudgeRoomCard.py
from __future__ import absolute_import
from .Item import Item

class JudgeRoomCard(Item):
    __slots__ = ('competition_region', )

    def __init__(self, item_id=None, create_time=None):
        super(JudgeRoomCard, self).__init__(item_id, create_time)
        self.competition_region = None
        return

    def get_persistent_dict(self):
        data = super(JudgeRoomCard, self).get_persistent_dict()
        data.update({'competition_region': self.competition_region
           })
        return data

    def get_client_dict(self):
        data = super(JudgeRoomCard, self).get_client_dict()
        data.update({'competition_region': self.competition_region
           })
        return data

    def get_competition_region(self):
        return self.competition_region

    def set_competition_region(self, region):
        self.competition_region = region