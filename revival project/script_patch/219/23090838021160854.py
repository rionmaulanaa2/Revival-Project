# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_ue4.py
import unreal_engine as ue
from safaia_base import SafaiaBase

class SafaiaUE4(SafaiaBase):

    def __init__(self):
        super(SafaiaUE4, self).__init__()
        self._update_func = None
        self._handle = None
        return

    def get_engine_name(self):
        return 'UE4-python'

    def register_update(self, update_func):
        self._update_func = update_func
        if not self._handle:
            self.handle = ue.add_ticker(self._on_tick)

    def unregister_update(self):
        self._update_func = None
        if self._handle:
            ue.remove_ticker(self._handle)
            self._handle = None
        return

    def _on_tick(self, dt):
        if self._update_func:
            self._update_func()
        return True

    def get_uid(self):
        return None

    def get_platform(self):
        return 'windows'