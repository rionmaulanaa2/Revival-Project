# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/PlatformAPI/SunshineEditor.py
from ..SunshineClient import SunshineClient
from .EditAPI import GetEngineEditAPI, SetEngineEditAPI
__all__ = [
 'SunshineEditor']

class SunshineEditor(object):

    def __init__(self, sunshineClient=None):
        self.sunshineClient = sunshineClient
        if sunshineClient is None:
            self._InitDefaultSunshineClient()
        self._loopTimer = -1
        self.looping = False
        return

    def _InitDefaultSunshineClient(self):
        self.sunshineClient = SunshineClient()
        self.sunshineClient.SetGameEncoding('utf-8')

    SetEngineEditAPI = staticmethod(SetEngineEditAPI)

    def RegisterPlugin(self, plugin):
        self.sunshineClient.RegisterPlugin(plugin)

    def GetPlugin(self, pluginName):
        return self.sunshineClient.GetPlugin(pluginName)

    def Connect(self, *args):
        ip, port = args[0], args[1]
        port = int(port)
        self.sunshineClient.Connect((ip, port))

    def StartHunter(self):
        plugin = self.sunshineClient.GetPlugin('Hunter')
        if plugin:
            plugin.StartHunter()

    def _StartLoop(self):

        def loop():
            try:
                self.sunshineClient.Update()
            except:
                import traceback
                traceback.print_exc()

        self._loopTimer = GetEngineEditAPI().AddRepeatTimer(0.01, loop)
        self.looping = True

    def Start(self):
        self._StartLoop()

    def Stop(self):
        if self.sunshineClient:
            self.sunshineClient.Close()
        if self._loopTimer != -1:
            GetEngineEditAPI().CancelTimer(self._loopTimer)
            self.looping = False