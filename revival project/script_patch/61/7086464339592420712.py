# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/time_utils.py
from __future__ import absolute_import
from __future__ import print_function
import time
from datetime import tzinfo, datetime, timedelta
import six
ONE_WEEK_DAYS = 7
ONE_MINUTE_SECONDS = 60
ONE_HOUR_SECONS = 3600
ONE_DAY_SECONDS = 86400
ONE_DAY_HOURS = 24
ONE_WEEK_SECONDS = ONE_WEEK_DAYS * ONE_DAY_SECONDS

def get_clock():
    return time.clock()


def get_time():
    return time.time()


def get_cur_time_str():
    now = datetime.now()
    return now.strftime('[%Y %m-%d %H:%M:%S]')


def get_readable_time(delta_time):
    day, hour, minute, second = get_readable_time_value(delta_time)
    if day:
        return '%s\xe5\xa4\xa9%s\xe5\xb0\x8f\xe6\x97\xb6%s\xe5\x88\x86\xe9\x92\x9f%s\xe7\xa7\x92' % (day, hour, minute, second)
    if hour:
        return '%s\xe5\xb0\x8f\xe6\x97\xb6%s\xe5\x88\x86\xe9\x92\x9f%s\xe7\xa7\x92' % (hour, minute, second)
    return '%s\xe5\x88\x86\xe9\x92\x9f%s\xe7\xa7\x92' % (minute, second)


def get_readable_time_value(delta_time):
    t = int(delta_time)
    if t <= 0:
        return (0, 0, 0, 0)
    day = t // ONE_DAY_SECONDS
    t -= ONE_DAY_SECONDS * day
    hour = t // ONE_HOUR_SECONS
    t -= ONE_HOUR_SECONS * hour
    minute = t // ONE_MINUTE_SECONDS
    t -= ONE_MINUTE_SECONDS * minute
    second = t
    return (
     day, hour, minute, second)


class UTC(tzinfo):

    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return 'UTC +%s' % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def set_timezone(tz):
    import game3d
    if game3d.get_platform() != game3d.PLATFORM_WIN32:
        return
    else:
        TIMEZONE_DATA = {-12: 'Dateline Standard Time',
           -11: 'UTC-11',
           -10: 'Hawaiian Standard Time',
           -8: 'Pacific Standard Time',
           -7: 'Mountain Standard Time',
           -6: 'Central Standard Time',
           -5: 'Eastern Standard Time',
           -4: 'Atlantic Standard Time',
           -3: 'Newfoundland Standard Time',
           -2: 'UTC-02',
           -1: 'Azores Standard Time',
           0: 'GMT Standard Time',
           1: 'W. Central Africa Standard Time',
           2: 'Egypt Standard Time',
           3: 'Russian Standard Time',
           4: 'Arabian Standard Time',
           5: 'Pakistan Standard Time',
           6: 'Myanmar Standard Time',
           7: 'SE Asia Standard Time',
           8: 'China Standard Time',
           9: 'Tokyo Standard Time',
           10: 'Lord Howe Standard Time',
           11: 'Central Pacific Standard Time',
           12: 'UTC+12',
           13: 'Samoa Standard Time',
           13: 'UTC+13',
           14: 'Line Islands Standard Time'
           }
        timezone = TIMEZONE_DATA.get(tz, None)
        if timezone:
            import os
            os.system('tzutil /s "%s"' % timezone)
            game3d.restart()
        return


def get_timezone():
    import time
    import game3d
    tzname = time.tzname[1]
    if game3d.get_platform() == game3d.PLATFORM_WIN32:
        try:
            tzname = six.ensure_text(tzname, 'gbk', 'ignore')
        except Exception as e:
            print('tzname decode except:', str(e))
            tzname = ''

    return '(UTC%+2d) %s' % (-time.timezone // 3600, tzname)