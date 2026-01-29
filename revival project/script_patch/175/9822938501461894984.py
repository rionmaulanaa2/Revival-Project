# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Model/ModelBase.py
import weakref
from ..utils.ShortUUID import uuid
TIMETICK_PER_SEC = 24000

class MontageModelBase(object):

    def __init__(self, uid=None):
        super(MontageModelBase, self).__init__()
        self.uuid = uid if uid is not None else uuid()
        self.properties = dict()
        self.parent = None
        self.meta = None
        return

    def serialize(self):
        return {'uuid': self.uuid,'properties': self.properties}

    def deserialize(self, data):
        self.uuid = data.get('uuid')
        self.properties = data.get('properties')

    def clear(self):
        self.properties.clear()
        self.parent = None
        self.meta = None
        return