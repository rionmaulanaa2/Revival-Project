# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillWindRush.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.gcommon.common_const.skill_const import MP_SYNC_STAGE_BEGIN_DO_SKILL, MP_SYNC_STAGE_BEGIN_RECOVER

class SkillWindRush(SkillCd):
    MAX_ATTACK_STAGE = 3

    def __init__(self, skill_id, unit_obj, data):
        super(SkillWindRush, self).__init__(skill_id, unit_obj, data)
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self._max_stage = ext_info.get('continue_count', 3)
        self._max_duration = ext_info.get('continue_time', 5)
        self._disable_time = 0

    def on_add(self):
        if self._last_cast_time > 0 and 0 < self._left_count < self._max_stage:
            pass_time = tutil.time() - self._last_cast_time
            if self._max_duration > pass_time:
                leave_time = self._max_duration - pass_time
                self._disable_time = tutil.time() + leave_time + 0.1
        self._unit_obj.send_event('E_ADD_WIND_RUSH_SKILL')

    def check_skill(self):
        if tutil.time() < self._disable_time:
            return True
        return super(SkillWindRush, self).check_skill()

    def on_check_cast_skill(self):
        if tutil.time() < self._disable_time:
            return True
        return super(SkillWindRush, self).on_check_cast_skill()

    def do_skill(self, *args):
        stage, ignore_water = args
        if stage >= self._max_stage:
            self.end_skill()
        else:
            self._disable_time = tutil.time() + self._max_duration + 0.1
        self._last_cast_time = tutil.time()
        return (
         stage,)

    def mod_left_cnt(self, delta_cnt):
        super(SkillWindRush, self).mod_left_cnt(delta_cnt)

    def end_skill(self, *args):
        self._disable_time = 0
        self.begin_recover_mp()

    def can_do_skill_in_water(self, *args):
        if not args:
            return super(SkillWindRush, self).can_do_skill_in_water(args)
        else:
            stage, ignore_water = args
            if ignore_water:
                return True
            return super(SkillWindRush, self).can_do_skill_in_water(args)

    def update_skill(self, data, trigger_update_event=True):
        if not data:
            return
        super(SkillWindRush, self).update_skill(data, trigger_update_event)
        if 'continue_time' in data:
            self._max_duration = data.get('continue_time', 8.0)
        if 'continue_count' in data:
            self._max_stage = data.get('continue_count', 3)
            self._unit_obj.send_event('E_CHANGE_STAGE_COUNT', self._max_stage)
        last_cast_time = data.get('last_cast_time', -1)
        if last_cast_time != -1 and self._mp_stage == MP_SYNC_STAGE_BEGIN_DO_SKILL and self._mp < self._max_mp and self._left_count < self._max_stage:
            self.end_skill()
            self._left_count = self._max_stage
            self._unit_obj.send_event('E_ADD_WIND_RUSH_SKILL')