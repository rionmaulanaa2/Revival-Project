# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillCd.py
from __future__ import absolute_import
from .SkillBase import SkillBase
from logic.gcommon.common_const.skill_const import MP_SYNC_STAGE_IDLE, MP_SYNC_STAGE_BEGIN_DO_SKILL, MP_SYNC_STAGE_END_DO_SKILL, MP_SYNC_STAGE_BEGIN_RECOVER
from logic.gcommon.time_utility import get_server_time
from common.cfg import confmgr

class SkillCd(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillCd, self).__init__(skill_id, unit_obj, data)
        self._last_cast_ts = data.get('last_cast_ts', 0)
        self.__left_cast_cnt = [0]
        self._tell_ui_at_once = False

    @property
    def _left_cast_cnt(self):
        return self.__left_cast_cnt[0]

    @_left_cast_cnt.setter
    def _left_cast_cnt(self, v):
        self.__left_cast_cnt[0] = 0
        self.__left_cast_cnt = [v]

    def on_add(self):
        if self._mp < self._max_mp and self._auto_recover:
            self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
        self.refresh_interval_cd()

    def check_skill(self):
        if self._unit_obj.ev_g_add_attr('skill_not_cost_{}'.format(self._category)):
            return True
        if self._mp < self._cost_mp + self._cost_mp_pre:
            return False
        if self._left_cast_cnt <= 0:
            return False
        if self.check_in_interval_cd():
            return False
        self._do_cost()
        return True

    def check_in_interval_cd(self):
        if self._last_cast_ts:
            return self._last_cast_ts - get_server_time() > 0
        return False

    def do_skill(self, *args):
        super(SkillCd, self).do_skill(*args)
        self.refresh_interval_cd()

    def refresh_interval_cd(self):
        cur_conf = confmgr.get('skill_conf', str(self._skill_id))
        cast_intv = cur_conf.get('cast_intv')
        if cast_intv is None:
            return
        else:
            if self._last_cast_ts:
                interval = self._last_cast_ts - get_server_time()
                if interval > 0:
                    cast_intv = interval
                else:
                    self._last_cast_ts = get_server_time()
            else:
                self._last_cast_ts = get_server_time()
            action_parts = cur_conf.get('ext_info', {}).get('action_parts')
            if self._left_cast_cnt > 0 and cast_intv > 0 and action_parts:
                for action in action_parts:
                    self._unit_obj.send_event('E_SET_ACTION_FORBIDDEN', action, True)

                def _recover():
                    if not self._unit_obj:
                        return
                    for action in action_parts:
                        self._unit_obj.send_event('E_SET_ACTION_FORBIDDEN', action, False)

                from common.utils.timer import CLOCK
                global_data.game_mgr.register_logic_timer(_recover, interval=cast_intv, times=1, mode=CLOCK)
            return

    def _do_cost(self):
        self._mp -= self._cost_mp + self._cost_mp_pre
        self.need_tick = True
        self.mod_left_cnt(-1)
        self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER if self._auto_recover else MP_SYNC_STAGE_BEGIN_DO_SKILL
        if self._tell_ui_at_once:
            self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)

    def tick(self, delta):
        if self._mp_stage == MP_SYNC_STAGE_BEGIN_RECOVER:
            self._mp += delta * self._inc_mp
            if self._mp > self._max_mp:
                self._mp = self._max_mp
                self._mp_stage = MP_SYNC_STAGE_IDLE
                self.need_tick = False
                self._unit_obj.send_event('E_ENERGY_FULL', self._skill_id)
            self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)

    def mod_left_cnt(self, delta_cnt):
        self._left_cast_cnt += delta_cnt

    def set_left_cnt(self, cnt):
        self._left_cast_cnt = cnt

    def on_check_cast_skill(self):
        if not super(SkillCd, self).on_check_cast_skill():
            return False
        if self.check_in_interval_cd():
            return False
        return self._left_cast_cnt > 0

    def update_skill(self, data, trigger_update_event=True):
        if not data:
            return
        super(SkillCd, self).update_skill(data, trigger_update_event)
        if self._auto_recover and self._mp < self._max_mp:
            self.begin_recover_mp()