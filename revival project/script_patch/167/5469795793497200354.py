# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/AntiCheatSDKMgr.py
from __future__ import absolute_import
import six
from common.framework import Singleton
import game3d
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import time
import json
PC_ANTICHEAT_FAIL_CODE = 100
PC_ANTICHEAT_SUCCESS_CODE = 200
IS_OPEN_ACSDK_PC = True and hasattr(game3d, 'anticheatsdk_init_sdk')

class AntiCheatSDKMgr(Singleton):
    ALIAS_NAME = 'anticheatsdk_mgr'
    MAX_TRY_TIME = 5
    CHECK_INTERVAL = 900
    FRAME_CUT_CHECK_INTERVAL = 60

    def init(self):
        self.is_acskd_inited = False
        self._cheat_check_tid = None
        self._cheat_check_tid_dict = {}
        self._init_try_time = 0
        self.is_up_role_info_acsdk = False
        self._last_check_time = 0
        self._last_check_time_dict = {}
        self._queues = []
        self.cur_callback = None
        self._frame_cut_interval = self.FRAME_CUT_CHECK_INTERVAL
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_login_reconnect_event': self.on_login_reconnect
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_acsdk(self):
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return
        if IS_OPEN_ACSDK_PC and not self.is_acskd_inited:
            from common.platform.dctool import interface
            if interface.is_mainland_package():
                gameID = 'g93'
                secretKey = 'l7wizsdohe71l38f'
                host = 'acsdk.gameyw.netease.com'
            else:
                gameID = 'g93na'
                secretKey = 'd0mbdasaigsm0wrc'
                host = 'acsdk.gameyw.easebar.com'
            game3d.anticheatsdk_init_sdk(True, gameID, secretKey, host, self.init_anticheat_sdk_callback)
            log_error('init_acsdk')

    def init_anticheat_sdk_callback(self, code, msg_list):
        if code == PC_ANTICHEAT_FAIL_CODE:
            log_error('init_anticheat_sdk_callback fail', msg_list)
            self._init_try_time += 1
            if self._init_try_time <= self.MAX_TRY_TIME:
                self.start_pc_anticheat_init_timer()
        elif code == PC_ANTICHEAT_SUCCESS_CODE:
            self.is_acskd_inited = True
            if self._queues:
                script_id, self.cur_callback = self._queues.pop(0)
                game3d.anticheatsdk_anticheat_check(True, script_id, self.anticheat_check_callback)
            self._init_tid = None
            game3d.delay_exec(1, lambda : self.init_callback())
        self.upload_sa_log(msg_list)
        return

    def init_callback(self):
        self.start_pc_anticheat_check_timer()
        self.start_anticheat_check_timer('1', self._frame_cut_interval)

    def set_acsdk_roleinfo(self):
        if IS_OPEN_ACSDK_PC and game3d.get_platform() == game3d.PLATFORM_WIN32 and not self.is_up_role_info_acsdk and global_data.player:
            from logic.comsys.login.LoginSetting import LoginSetting
            userId = str(global_data.player.uid)
            server_info = LoginSetting().last_logined_server or {}
            userServer = server_info.get('svr_name', '0')
            server_num = str(server_info.get('svr_num', 0))
            userName = global_data.player.get_name()
            game3d.anticheatsdk_set_extra_param('role_id', userId)
            game3d.anticheatsdk_set_extra_param('user_name', userName)
            game3d.anticheatsdk_set_extra_param('svr_name', userServer)
            game3d.anticheatsdk_set_extra_param('svr_num', server_num)
            self.is_up_role_info_acsdk = True

    def upload_sa_log(self, msg_list):
        player = global_data.player
        if not player:
            log_error('AntiCheatSDKMgr:try upload Log but not player', msg_list)
            return
        for json_msg in msg_list:
            msg = json.loads(json_msg)
            if type(msg) != dict:
                player.call_server_method('client_sa_log', ('acsdk_cheat_check_v2', {'report': msg}))
            else:
                player.call_server_method('client_sa_log', ('acsdk_cheat_check_v2', msg))

    def start_pc_anticheat_init_timer(self):
        self._init_tid = global_data.game_mgr.register_logic_timer(self.init_acsdk, interval=5, times=1, mode=CLOCK)

    def anticheatsdk_anticheat_check(self):
        self._last_check_time = time()
        if not IS_OPEN_ACSDK_PC:
            return
        self.anticheat_check('0', self.anticheat_sdk_check_callback)

    def run_anticheat_by_script_id(self, script_id):
        if not IS_OPEN_ACSDK_PC:
            return
        self.anticheat_check(script_id, self.anticheat_sdk_check_callback)

    def start_pc_anticheat_check_timer(self):
        if not self.is_acskd_inited:
            return
        if self._cheat_check_tid:
            return

        def check_func():
            self.anticheatsdk_anticheat_check()
            self._cheat_check_tid = global_data.game_mgr.register_logic_timer(check_func, interval=self.CHECK_INTERVAL, times=1, mode=CLOCK)

        cur_time = time()
        nex_time = min(int(self._last_check_time + self.CHECK_INTERVAL - cur_time), self.CHECK_INTERVAL)
        nex_time = max(1, nex_time)
        self._cheat_check_tid = global_data.game_mgr.register_logic_timer(check_func, interval=nex_time, times=1, mode=CLOCK)

    def on_login_reconnect(self, *args):
        self._cheat_check_tid = None
        self._init_tid = None
        if self.is_acskd_inited:
            self.start_pc_anticheat_check_timer()
            self.start_anticheat_check_timer('1', self._frame_cut_interval)
        elif self._init_try_time <= self.MAX_TRY_TIME:
            self.start_pc_anticheat_init_timer()
        return

    def on_finalize(self):
        self.process_event(False)
        if self._cheat_check_tid:
            global_data.game_mgr.unregister_logic_timer(self._cheat_check_tid)
            self._cheat_check_tid = None
        if self._init_tid:
            global_data.game_mgr.unregister_logic_timer(self._init_tid)
            self._init_tid = None
        if self._cheat_check_tid_dict:
            for script_id, tid in six.iteritems(self._cheat_check_tid_dict):
                if tid:
                    global_data.game_mgr.unregister_logic_timer(tid)

        self._cheat_check_tid_dict = {}
        if self.is_acskd_inited:
            game3d.anticheatsdk_clearsdk()
        super(AntiCheatSDKMgr, self).on_finalize()
        return

    def anticheat_sdk_check_callback(self, code, msg_list):
        if code == PC_ANTICHEAT_FAIL_CODE:
            log_error('anticheat_sdk_check_callback fail', msg_list)
        elif code == PC_ANTICHEAT_SUCCESS_CODE:
            pass
        self.upload_sa_log(msg_list)

    def upload_screenshot(self):
        self.anticheat_check('ss', self.anticheat_sdk_check_callback)

    def start_anticheat_check_timer(self, script_id, interval):
        if not self.is_acskd_inited:
            return
        if self._cheat_check_tid_dict.get(script_id):
            return

        def check_func():
            self._last_check_time_dict[script_id] = time()
            if not IS_OPEN_ACSDK_PC:
                return
            self.anticheat_check(script_id, self.anticheat_sdk_check_callback)
            self._cheat_check_tid_dict[script_id] = global_data.game_mgr.register_logic_timer(check_func, interval=interval, times=1, mode=CLOCK)

        _last_check_time = self._last_check_time_dict.get(script_id, 0)
        cur_time = time()
        nex_time = min(int(self._last_check_time + interval - cur_time), interval)
        nex_time = max(1, nex_time)
        self._cheat_check_tid_dict[script_id] = global_data.game_mgr.register_logic_timer(check_func, interval=nex_time, times=1, mode=CLOCK)

    def anticheat_check(self, script_id, callback):
        if self.cur_callback or not self.is_acskd_inited:
            self._queues.append((script_id, callback))
            return
        self.cur_callback = callback
        game3d.anticheatsdk_anticheat_check(True, script_id, self.anticheat_check_callback)

    def anticheat_check_callback(self, code, msg_list):
        self.cur_callback(code, msg_list)
        if self._queues:
            script_id, self.cur_callback = self._queues.pop(0)
            game3d.anticheatsdk_anticheat_check(True, script_id, self.anticheat_check_callback)
        else:
            self.cur_callback = None
        return