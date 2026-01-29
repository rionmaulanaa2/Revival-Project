# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/AppsflyerData.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.time_utility import time, timestamp_to_datetime

class AppsflyerData(Singleton):

    def init(self):
        self.read_setting()

    def read_setting(self):
        self.ad_data = ArchiveManager().get_archive_data('appsflyer_data')

    def is_enough_record_days(self, event_name, days):
        if days == -1:
            event_season = self.ad_data.get_field(event_name, 0)
            if global_data.player and global_data.player.get_battle_season() > event_season:
                self.ad_data[event_name] = global_data.player.get_battle_season()
                self.save_setting()
                return True
            return False
        else:
            event_time = self.ad_data.get_field(event_name, 0)
            now_time = time()
            if event_time == 0:
                self.ad_data[event_name] = now_time
                self.save_setting()
                return True
            today_date = timestamp_to_datetime(now_time).date()
            event_date = timestamp_to_datetime(event_time).date()
            delta_days = (today_date - event_date).days
            if delta_days >= days or delta_days < 0:
                self.ad_data[event_name] = now_time
                self.save_setting()
                return True
            return False

    def save_setting(self):
        self.ad_data.save(encrypt=True)

    def on_finalize(self):
        self.save_setting()
        super(AppsflyerData, self).on_finalize()