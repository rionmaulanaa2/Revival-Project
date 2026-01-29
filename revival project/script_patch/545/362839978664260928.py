# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/VideoPlugin/VideoPluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = '24bd0bac-e646-11e7-8b2b-005056c00008'

class VideoPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def StartRecord(self, windowName):
        raise NotImplementedError

    def StopRecord(self):
        raise NotImplementedError

    def SetMarkPosition(self, positions, desc):
        raise NotImplementedError

    def StartPlay(self, position):
        raise NotImplementedError

    def StopPlay(self):
        raise NotImplementedError

    def PausePlay(self):
        raise NotImplementedError