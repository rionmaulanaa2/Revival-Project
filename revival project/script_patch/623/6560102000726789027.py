# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/HunterPluginClient.py
from ..EditorPlugin import EditorPluginClient
from safaia import get_instance

class HunterPluginClient(EditorPluginClient):
    PLUGIN_NAME = 'Hunter'
    GAME_ID = ''
    CONNECT_ADDRESS = ('192.168.40.111', 29006)
    ENGINE_ENCODING = 'utf-8'
    SUNSHINE_UUID = '6665729f-8f19-44ee-8625-e6ab9f02dcdf'

    def __init__(self):
        super(HunterPluginClient, self).__init__()
        self.safaiaInstance = get_instance()
        if self.safaiaInstance.get_engine_name().lower() not in ('neox', 'messiah',
                                                                 'mobile server'):
            setattr(self.safaiaInstance, 'get_engine_name', self.GetEngineName)
            setattr(self.safaiaInstance, 'get_uid', self.GetUID)
            setattr(self.safaiaInstance, 'get_platform', self.GetPlatform)
            setattr(self.safaiaInstance, 'register_update', self.RegisterUpdate)
            setattr(self.safaiaInstance, 'unregister_update', self.UnregisterUpdate)
            setattr(self.safaiaInstance, 'get_base_dir', self.GetBaseDir)

    def GetEngineName(self):
        raise NotImplementedError

    def GetUID(self):
        return None

    def GetPlatform(self):
        raise NotImplementedError

    def RegisterUpdate(self, func):
        raise NotImplementedError

    def UnregisterUpdate(self):
        raise NotImplementedError

    def GetBaseDir(self):
        return '.'

    def ExecuteConsoleCommand(self, cmdStr):
        pass

    def StartHunter(self):
        safaiaClass = self.safaiaInstance.__class__

        class GMExtension(safaiaClass):

            def __init__(this):
                this.on_script(this.gmFuncSunshineDefined)

            def gmFuncSunshineDefined(this, lang, script):
                if lang == 'text':
                    self.ExecuteConsoleCommand(script.encode(self.ENGINE_ENCODING))

        self.safaiaInstance.install(GMExtension)
        self.safaiaInstance.start(self.GAME_ID, connect_addr=self.CONNECT_ADDRESS, encoding=self.ENGINE_ENCODING)
        print 'StartHunter'

    def StopHunter(self):
        self.safaiaInstance.stop()

    def Register(self):
        return {}