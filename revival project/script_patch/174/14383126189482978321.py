# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillThrowable8024.py
from __future__ import absolute_import
import world
import collision
import math3d
import time
from common.cfg import confmgr
from .SkillThrowable import SkillThrowable
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
from logic.gcommon.common_const.skill_const import MP_SYNC_STAGE_BEGIN_RECOVER, MP_SYNC_STAGE_IDLE

class SkillThrowable8024(SkillThrowable):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillThrowable8024, self).__init__(skill_id, unit_obj, data)
        self.trigger_c4 = None
        self.flying_grenade_explode_id = None
        self.force_visible = True
        return

    def do_skill(self, stage, position, forward):
        throw_item, stage = super(SkillThrowable8024, self).do_skill(stage, position, forward)
        self.flying_grenade_explode_id = throw_item['uniq_key']
        return (
         throw_item, stage)

    def update_skill(self, data, trigger_update_event=True):
        super(SkillThrowable8024, self).update_skill(data, trigger_update_event)
        is_exploder = data.get('is_exploder', False)
        trigger_c4 = data.get('trigger_c4', None)
        if is_exploder:
            self.flying_grenade_explode_id = trigger_c4
            self.force_visible = False
            self.begin_recover_mp()
        else:
            if not trigger_c4:
                self.force_visible = True
                self.begin_recover_mp()
            else:
                self.force_visible = False
                self.begin_recover_mp()
            self._unit_obj.send_event('E_UPDATE_IGNITE_STATE', trigger_c4)
            self.trigger_c4 = trigger_c4
        return

    def end_skill(self, *args):
        super(SkillThrowable8024, self).end_skill(*args)
        self.boom_time = time.time()
        c4_entity = global_data.battle.get_entity(self.trigger_c4)
        if c4_entity and c4_entity.logic:
            model = c4_entity.logic.ev_g_model()
            if model:
                pos = model.world_position
                return (
                 (
                  pos.x, pos.y, pos.z),)
        flying_grenade_entity, _ = global_data.emgr.scene_find_throw_item_event.emit(self.flying_grenade_explode_id)[0]
        if flying_grenade_entity and flying_grenade_entity.logic:
            model = flying_grenade_entity.logic.ev_g_model()
            if model:
                pos = model.world_position
                return (
                 (
                  pos.x, pos.y, pos.z),)

    def tick(self, delta):
        if self._mp_stage == MP_SYNC_STAGE_BEGIN_RECOVER:
            self._mp += delta * self._inc_mp
            if self._mp > self._max_mp:
                self._mp = self._max_mp
                self._mp_stage = MP_SYNC_STAGE_IDLE
                self.need_tick = False
                self._unit_obj.send_event('E_ENERGY_FULL', self._skill_id)
            self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp, self.force_visible)