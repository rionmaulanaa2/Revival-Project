# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/ModelLibPlugin/ModelLibPluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = 'd671cd00-25ad-406a-9de5-596af90d853f'

class ModelLibPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def ShowRes(self, resPath):
        raise NotImplementedError

    def showMultiRes(self, resData):
        raise NotImplementedError