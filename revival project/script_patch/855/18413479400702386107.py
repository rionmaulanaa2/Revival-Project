# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/qa_test2.py
__author__ = 'lxn3032'
import traceback
from safaia_base import SafaiaBase
import C_app
import log
import utils

class SafaiaQATest2(SafaiaBase):

    def __init__(self):
        super(SafaiaQATest2, self).__init__()
        self._scope['log'] = log

    def get_engine_name(self):
        return 'fenghun'

    def get_platform(self):
        return C_app.user_os().lower()

    def get_uid(self):
        if self.get_platform().startswith('windows'):
            return super(SafaiaQATest2, self).get_uid()
        else:
            return utils.get_device_desc().replace('-', '').lower()

    def register_update(self, update_func):
        pass

    def unregister_update(self):
        pass

    def on_main_script(self, script):
        script = script.encode('gbk')
        exec compile(script, '<hunter script>', 'exec') in self._scope


delay_count = 0

def Init():
    pass


def Update(info):
    global delay_count
    if delay_count < 10:
        delay_count += 1
        if delay_count == 10:
            SafaiaQATest2().start('mh', connect_addr=('gate-gz.hunter.netease.com',
                                                      29001), encoding='gbk', default_name='XYQ', thread_safe=True)
        return
    try:
        SafaiaQATest2().update()
    except:
        tb = traceback.format_exc()
        SafaiaQATest2().send(24, {'type': 'tb','data': tb})


def End(*args, **kwargs):
    global delay_count
    delay_count = 0
    SafaiaQATest2().stop()