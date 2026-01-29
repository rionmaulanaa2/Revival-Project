# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/dctool/mgr.py
from __future__ import absolute_import
from __future__ import print_function
from common.framework import Singleton
from common.platform.dctool import scenetypecfg as cfg
from common.cfg import confmgr
from dctool3 import DCTool
import json
import time
LOGIN_FAILED_CODES_NO_CHECK = (110, )

class DctoolMgr(Singleton):
    ALIAS_NAME = 'dctool'
    CD_TIME = 1

    def init(self):
        self.last_time = {}
        self.login_start_time = 0
        self._normal_timer = None
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.on_request_login_event += self.on_request_login
        global_data.emgr.on_login_success_event += self.on_login_success
        global_data.emgr.on_login_failed_event += self.on_login_fail
        global_data.emgr.net_disconnect_event += self.on_disconnect
        global_data.emgr.net_reconnect_event += self.on_reconnect
        global_data.emgr.net_login_reconnect_event += self.on_reconnect
        global_data.emgr.on_server_list_refresh_event += self.on_server_list_refresh

    def get_enable(self):
        return confmgr.get('setting', 'dctool', default=False)

    def start_check(self, scene_type, **kwargs):
        if not self.get_enable():
            return
        else:
            if scene_type not in cfg.SCENE_INFO:
                return
            scene_type, func_name = cfg.SCENE_INFO[scene_type]
            res_dict = cfg.get_default_dict(scene_type)
            res_dict.update(getattr(cfg, func_name)(**kwargs))
            if not res_dict:
                return
            if scene_type not in self.last_time:
                self.last_time[scene_type] = 0
            now_time = time.time()
            if now_time - self.last_time[scene_type] < self.CD_TIME:
                return
            self.last_time[scene_type] = now_time
            encoded_json = json.dumps(res_dict)
            print('@@@@@@@@@@ data-detect', res_dict['Scene'], res_dict.get('region', None))
            DCTool.lazy_diagnose(encoded_json)
            return

    def on_request_login(self):
        self.login_start_time = time.time()

    def on_login_success(self):
        time_cost = (time.time() - self.login_start_time) * 1000
        self.start_check('LoginSuccess', time_cost=time_cost)
        self.start_normal_check()

    def on_login_fail(self, err_code=None, error_log=None, *args, **kwargs):
        if err_code in LOGIN_FAILED_CODES_NO_CHECK:
            return
        self.start_check('LoginFailed', err_code=err_code, error_log=error_log)
        self.stop_normal_check()

    def on_disconnect(self, *args, **kwargs):
        if global_data.connect_helper.is_disconnected():
            return
        self.start_check('Disconnect')
        self.stop_normal_check()

    def on_reconnect(self, *args, **kwargs):
        self.start_check('Reconnect')
        self.start_normal_check()

    def on_server_list_refresh(self, *args, **kwargs):
        from logic.comsys.login.LoginHelper import LoginHelper
        if LoginHelper().server_list:
            self.start_check('DownloadServerListSuccess')
        else:
            self.start_check('DownloadServerListFailed')

    def start_normal_check(self, interval=-1):
        if not self.get_enable():
            return
        self.stop_normal_check()
        from common.utils import timer
        import random
        if interval == -1:
            interval = confmgr.get('setting', 'dc_time', default=1800)

        def on_check():
            self.start_check('Normal')

        def first_check():
            self.start_check('Normal')
            global_data.game_mgr.get_logic_timer().unregister(self._normal_timer)
            self._normal_timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=timer.CLOCK, interval=interval)

        self._normal_timer = global_data.game_mgr.get_logic_timer().register(func=first_check, mode=timer.CLOCK, interval=int(interval * random.random() + 1), times=1)

    def stop_normal_check(self):
        if self._normal_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._normal_timer)
            self._normal_timer = None
        return