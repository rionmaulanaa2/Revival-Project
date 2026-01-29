# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/RainbowEntity.py


class RainbowEntityWrapper(object):

    def __init__(self, uuid, entity):
        self._uuid = uuid
        self._entity = entity

    @property
    def uuid(self):
        return self._uuid

    @property
    def entity(self):
        return self._entity

    @property
    def Edit(self):
        pass