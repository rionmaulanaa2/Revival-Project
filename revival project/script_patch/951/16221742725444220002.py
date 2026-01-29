# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillBeacon8031Client.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from logic.gcommon.time_utility import get_server_time

class SkillBeacon8031Client(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillBeacon8031Client, self).__init__(skill_id, unit_obj, data)
        self.last_cast_time = 0
        self.max_duration = 10
        self.beacon_eid = None
        return

    def do_skill(self, *args):
        super(SkillBeacon8031Client, self).do_skill(*args)
        return args

    def end_skill(self, *args):
        super(SkillBeacon8031Client, self).do_skill(*args)
        return args

    def update_skill(self, data, trigger_update_event=True):
        if not data:
            return
        super(SkillBeacon8031Client, self).update_skill(data, trigger_update_event)
        if 'max_duration' in data:
            self.max_duration = data['max_duration']
            self._unit_obj.send_event('E_NOTIFY_REAPER_SHAPE_MAX_DURATION', self.max_duration)
        if 'last_cast_time' in data:
            self.last_cast_time = data['last_cast_time']
            self.beacon_eid = data['beacon_eid']
            if self.beacon_eid:
                interval = get_server_time() - self.last_cast_time
                if interval < self.max_duration:
                    self._unit_obj.send_event('E_TRANS_TO_REAPER', self.max_duration - interval, self.beacon_eid)
            else:
                self._unit_obj.send_event('E_TRANS_TO_REAPER', 0)
        if 'expected_end_time' in data:
            self._unit_obj.send_event('E_TRANS_TO_REAPER', data['expected_end_time'] - get_server_time(), self.beacon_eid)