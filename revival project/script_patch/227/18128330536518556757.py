# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/appsflyer.py
from __future__ import absolute_import
import game3d
from . import appsflyer_const
from common.framework import Singleton
from common.platform.dctool import interface
from common.platform.AppsflyerData import AppsflyerData

class Appsflyer(Singleton):

    def advert_track_event(self, event_name, param='{}', suffix='', platform=None):
        if not hasattr(game3d, 'advert_track_event'):
            return
        else:
            if event_name not in appsflyer_const.event_day_dict:
                log_error('event_name is not defined in appsflyer_const.event_day_dict, event_name = %s' % event_name)
                return
            days = appsflyer_const.event_day_dict[event_name]
            if suffix:
                event_name = event_name + suffix
            can_send = AppsflyerData().is_enough_record_days(event_name, days)
            if can_send and game3d.get_platform() != game3d.PLATFORM_WIN32 and not interface.is_mainland_package():
                if platform is None:
                    game3d.advert_track_event(event_name, appsflyer_const.AF_PLATFORM, param)
                    game3d.advert_track_event(event_name, appsflyer_const.FB_PLATFORM, param)
                else:
                    game3d.advert_track_event(event_name, platform, param)
            return