# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_messiah.py
__author__ = 'lxn3032'
import time
import traceback
import MEngine
import MConfig
from safaia_base import SafaiaBase

class FrameTimer(object):

    def __init__(self, func):
        self.canceled = False
        self.func = func
        self.loop()

    def loop(self):
        if self.canceled:
            return
        try:
            self.func()
        except:
            traceback.print_exc()

        MEngine.GetGameplay().Scenario.AddCallback(0.03, self.loop)

    def cancel(self):
        self.canceled = True


class SafaiaMessiah(SafaiaBase):

    def __init__(self):
        super(SafaiaMessiah, self).__init__()
        self.encoding = 'utf-8'
        self._timer = None
        return

    def get_uid(self):
        try:
            os_type = self.get_platform()
            if os_type == 'ios':
                import MPlatform
                adv_id = MPlatform.GetAdvertisingId().replace('-', '').lower()
                if '000000' not in adv_id:
                    return adv_id
            elif os_type == 'android':
                import MAccount
                MAccount.GetAccountManager().Initialize()
                time.sleep(0.5)
                adv_id = MAccount.GetAccountManager().GetPropStr('UDID').replace('-', '').lower()
                if '000000' not in adv_id:
                    return adv_id
            return super(SafaiaMessiah, self).get_uid()
        except:
            return super(SafaiaMessiah, self).get_uid()

    def get_platform(self):
        return MConfig.Platform.lower()

    def get_engine_name(self):
        return 'messiah'

    def register_update(self, update_func):
        self._timer = FrameTimer(update_func)

    def unregister_update(self):
        self._timer.cancel()

    def get_base_dir(self):
        return MEngine.GetFileSystemBasePath('LocalData')