# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPhantom8029.py
from __future__ import absolute_import
import math3d
from .SkillWindRush import SkillWindRush
from logic.gcommon import time_utility as tutil
from logic.gutils.mecha_utils import get_mecha_call_pos

class SkillPhantom8029(SkillWindRush):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPhantom8029, self).__init__(skill_id, unit_obj, data)
        self._left_count = 0
        self._phantom_id = None
        return

    def do_skill(self, *args):
        stage, ignore_water, position = args
        if stage >= self._max_stage:
            self.end_skill()
        elif stage == 1:
            self._disable_time = tutil.time() + self._max_duration
        self._last_cast_time = tutil.time()
        if position:
            return (stage, position.x, position.y, position.z)
        else:
            return (
             stage, None, None, None)

    def on_check_cast_skill(self):
        if tutil.time() < self._disable_time:
            return True
        return super(SkillWindRush, self).on_check_cast_skill()

    def update_skill(self, data, trigger_update_event=True):
        super(SkillPhantom8029, self).update_skill(data, trigger_update_event)
        phantom_id = data.get('phantom_eid', None)
        left_count = data.get('left_count', None)
        continue_count = data.get('continue_count', None)
        last_cast_time = data.get('last_cast_time', None)
        if continue_count and self._unit_obj:
            self._max_stage = continue_count
            self._unit_obj.send_event('E_UPDATE_CORE_STATE', self._max_stage)
        if left_count and self._unit_obj:
            self._left_count = left_count
            self._unit_obj.send_event('E_UPDATE_USE_STATE', self._left_count, last_cast_time)
        if phantom_id and self._unit_obj:
            self._unit_obj.send_event('E_UPDATE_PHANTOM_STATE', phantom_id)
        return

    def can_do_skill_in_water(self, *args):
        if not args:
            return super(SkillWindRush, self).can_do_skill_in_water(args)
        else:
            stage, ignore_water, _ = args
            if ignore_water:
                return True
            return super(SkillWindRush, self).can_do_skill_in_water(args)