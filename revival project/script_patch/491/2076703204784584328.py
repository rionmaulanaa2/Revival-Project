# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/AtmospherePlugin/AtmospherePluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = 'dfdd1bae-ccd7-11e6-b8b4-14dda9de0dd8'

class AtmospherePluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    @classmethod
    def UpdateGameInfo(cls, gameInfo, newKey):
        raise NotImplementedError

    @classmethod
    def GetPluginsInfo(cls):
        raise NotImplementedError