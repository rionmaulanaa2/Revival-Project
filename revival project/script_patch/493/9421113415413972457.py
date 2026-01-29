# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/RainbowPluginClientBase.py
try:
    from typing import Optional
except ImportError:
    pass

from ..RainbowPluginClient import RainbowPluginClient
from .EntityMgr import EntityMgr
__all__ = [
 'EDITOR_RAYCAST_DISTANCE', 'EDITOR_MODE_EDIT', 'EDITOR_MODE_GAME', 'RainbowPluginClientBase']
EDITOR_RAYCAST_DISTANCE = 9999
EDITOR_MODE_GAME = 0
EDITOR_MODE_EDIT = 1
EDITOR_MODE_COUNT = 2

class RainbowPluginClientBase(RainbowPluginClient):

    def __init__(self):
        self.entityMgr = None
        return

    def SetEntityMgr(self, entityMgr):
        self.entityMgr = entityMgr