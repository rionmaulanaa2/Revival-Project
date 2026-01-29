# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideSetting.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.comsys.login.LoginSetting import LoginSetting
from logic.comsys.archive.archive_manager import ArchiveManager

class GuideSetting(Singleton):

    def init(self):
        self.read_setting()
        self.init_host_num()
        self._create_login = False

    def on_finalize(self):
        self.save_setting()
        super(GuideSetting, self).on_finalize()

    def init_host_num(self):
        last_login_data = LoginSetting().last_logined_server
        if last_login_data:
            self.host_num = str(last_login_data['svr_num'])
        else:
            self.host_num = str(0)

    def read_setting(self):
        self.guide_data_archive = ArchiveManager().get_archive_data('guide')

    def save_setting(self):
        self.guide_data_archive.save(encrypt=True)

    @property
    def local_battle_data(self):
        return self.guide_data_archive.get_field(self.host_num, {})

    @local_battle_data.setter
    def local_battle_data(self, info):
        self.guide_data_archive[self.host_num] = info
        self.save_setting()