# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/LoginSetting.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.comsys.archive.archive_manager import ArchiveManager
from common.platform.channel import Channel
import logic.gcommon.time_utility as tutil
KEY_LAST_LOGINED_SERVER = 'last_logined_server'
KEY_FIRST_LOGIN_TIME_TODAY = 'first_login_time_today'
KEY_REGISTED_USERS = 'registed_users'
KEY_ACTIVATION = 'activation'
KEY_LOCAL_SERVER_LST = 'local_server_lst'
KEY_LAST_REMIND_TIME = 'last_remind_time'

class LoginSetting(Singleton):

    def init(self):
        self.read_setting()
        self.logined_user_name = ()

    def init_event(self):
        global_data.emgr.registed_account_updated_event += self.update_registed_users_by_user_name

    def read_setting(self):
        self.login_data_archive = ArchiveManager().get_archive_data('login')

    def on_finalize(self):
        self.save_setting()
        super(LoginSetting, self).on_finalize()

    def save_setting(self):
        self.login_data_archive.save(encrypt=True)

    @property
    def first_logined_server(self):
        return self.login_data_archive.get_field(KEY_ACTIVATION, False)

    @first_logined_server.setter
    def first_logined_server(self, flag):
        self.login_data_archive[KEY_ACTIVATION] = flag
        self.save_setting()

    @property
    def last_logined_server(self):
        return self.login_data_archive.get_field(KEY_LAST_LOGINED_SERVER, None)

    @last_logined_server.setter
    def last_logined_server(self, server_info):
        self.login_data_archive[KEY_LAST_LOGINED_SERVER] = server_info
        self.save_setting()

    def get_registed_users_by_user_name(self):
        logined_name = Channel().get_login_name()
        registed_users = self.login_data_archive.get_field(KEY_REGISTED_USERS, {})
        return registed_users.get(logined_name, None)

    def update_registed_users_by_user_name(self, data):
        logined_name = Channel().get_login_name()
        registed_users = self.login_data_archive.get_field(KEY_REGISTED_USERS, {})
        registed_users[logined_name] = data

    def get_server_num(self):
        server_info = self.last_logined_server or {}
        return server_info.get('svr_num', '0')

    def get_local_server_lst(self):
        return self.login_data_archive.get_field(KEY_LOCAL_SERVER_LST, [])

    def update_local_server_lst(self):
        if not self.last_logined_server:
            return
        else:
            host_num = self.last_logined_server.get('svr_num', None)
            now_server_lst = self.login_data_archive.get_field(KEY_LOCAL_SERVER_LST, [])
            if host_num and host_num not in now_server_lst:
                now_server_lst.append(host_num)
                self.login_data_archive[KEY_LOCAL_SERVER_LST] = now_server_lst
                self.save_setting()
            return

    @property
    def last_remind_timestamp(self):
        return self.login_data_archive.get_field(KEY_LAST_REMIND_TIME, 0)

    @last_remind_timestamp.setter
    def last_remind_timestamp(self, time_stamp):
        self.login_data_archive[KEY_LAST_REMIND_TIME] = time_stamp
        self.save_setting()