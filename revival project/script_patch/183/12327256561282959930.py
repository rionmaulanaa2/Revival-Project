# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/archive/archive_manager.py
from __future__ import absolute_import
from logic.comsys.archive.archivedata import ArchiveData
from logic.comsys.archive import archive_key_const
from common.framework import Singleton

class ArchiveManager(Singleton):
    ALIAS_NAME = 'achi_mgr'

    def init(self):
        self._archive_data = {}

    def get_archive_data(self, archive_name):
        if archive_name not in self._archive_data:
            self._archive_data[archive_name] = ArchiveData(archive_name)
        return self._archive_data[archive_name]

    def del_archive_data(self, archive_name):
        if archive_name not in self._archive_data:
            return
        self._archive_data[archive_name].del_data()
        del self._archive_data[archive_name]

    def get_general_archive_data(self):
        return self.get_archive_data('data_general')

    def get_login_account_data(self):
        return self.get_archive_data('data_login')

    def get_user_archive_data(self, usernum):
        return self.get_archive_data('data_%s' % usernum)

    def get_cur_user_archive_data(self, field, default=None):
        if not global_data.player or not global_data.player.uid:
            return default
        user_arch = self.get_user_archive_data(global_data.player.uid)
        return user_arch.get_field(field, default)

    def set_cur_user_archive_data(self, field, val):
        if not global_data.player or not global_data.player.uid:
            return False
        user_arch = self.get_user_archive_data(global_data.player.uid)
        user_arch.set_field(field, val)
        return True

    def is_show_netease_daren_red_point(self, sdk_uid):
        return self.get_general_archive_data().get_field('netease_red_point', {}).get(sdk_uid, 1)

    def save_netease_daren_red_point(self, sdk_uid, flag):
        general_data = self.get_general_archive_data()
        red_point = general_data.get_field('netease_red_point', {})
        if red_point.get(sdk_uid) == flag:
            return
        red_point[sdk_uid] = flag
        general_data.set_field('netease_red_point', red_point)

    def get_general_archive_data_value(self, key, default=None):
        data_general = self.get_general_archive_data()
        return data_general.get_field(key, default)

    def save_general_archive_data_value(self, key, value):
        data_general = self.get_general_archive_data()
        data_general.set_field(key, value)

    def save_custom_bit_mode(self, value):
        data_general = self.get_general_archive_data()
        data_general.set_field('custom_bit', value)

    def get_custom_bit_mode(self, default='noset'):
        data_general = self.get_general_archive_data()
        return data_general.get_field('custom_bit', default)

    def get_login_account_data_value(self, key, default=None):
        data_general = self.get_login_account_data()
        return data_general.get_field(key, default)

    def save_login_account_data_value(self, key, value):
        data_general = self.get_login_account_data()
        data_general.set_field(key, value)