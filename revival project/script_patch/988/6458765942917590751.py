# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_neox.py
__author__ = 'lxn3032'
import game3d
from safaia_base import SafaiaBase

class SafaiaNeoX(SafaiaBase):

    def __init__(self):
        super(SafaiaNeoX, self).__init__()
        self._timer_id = None
        return

    def get_uid(self):
        udid = game3d.get_udid().replace('-', '').lower()
        if '000000' not in udid:
            return udid
        else:
            return None

    def get_engine_name(self):
        return 'NeoX'

    def get_platform(self):
        os_list = ('unknown', 'windows', 'mac', 'ios', 'android')
        platform_id = game3d.get_platform()
        try:
            return os_list[platform_id]
        except:
            return 'unknown'

    def register_update(self, update_func):
        self._timer_id = game3d.register_timer(40, update_func)
        game3d.activate_timer(self._timer_id, True)

    def unregister_update(self):
        game3d.activate_timer(self._timer_id, False)

    def get_base_dir(self):
        pf = game3d.get_platform()
        if pf == game3d.PLATFORM_IOS:
            return game3d.get_doc_dir()
        else:
            return '.'