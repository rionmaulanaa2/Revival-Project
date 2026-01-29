# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWeaponAimTarget.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import common.utils.timer as timer
import logic.gcommon.const as const
from mobile.common.EntityManager import EntityManager

class ComWeaponAimTarget(UnitCom):
    BIND_EVENT = {'E_AIM_LOCK_TARGET': 'on_aim_lock'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComWeaponAimTarget, self).init_from_dict(unit_obj, bdict)
        self._lock_target_id = None
        self._sound_timer = None
        return

    def cache(self):
        self.on_aim_lock(None)
        super(ComWeaponAimTarget, self).cache()
        return

    def on_aim_lock(self, target_id):
        if not target_id:
            self.on_target_locked(False)
        self._lock_target_id = target_id
        self.check_sound()
        if self._lock_target_id:
            self.on_target_locked(True)

    def check_sound(self):
        if self._lock_target_id:
            self.clear_sound_timer()
            self.add_sound_visible()
            self._sound_timer = global_data.game_mgr.register_logic_timer(self.add_sound_visible, interval=10, times=60, mode=timer.LOGIC)
        else:
            self.clear_sound_timer()

    def clear_sound_timer(self):
        if self._sound_timer:
            global_data.game_mgr.unregister_logic_timer(self._sound_timer)
            self._sound_timer = None
        return

    def add_sound_visible(self):
        if not self._lock_target_id:
            return
        lock_target = EntityManager.getentity(self._lock_target_id)
        if not (lock_target and lock_target.logic):
            return
        if not lock_target.logic.ev_g_is_cam_target():
            return
        model = self.ev_g_model()
        if model:
            pos = model.world_position
            lock_target.logic.send_event('E_HITED_SHOW_LOCK_DIR', self.unit_obj, pos)

    def destroy(self):
        self.on_aim_lock(None)
        super(ComWeaponAimTarget, self).destroy()
        return

    def on_target_locked(self, is_lock):
        if self._lock_target_id:
            lock_target = EntityManager.getentity(self._lock_target_id)
            if lock_target and lock_target.logic:
                lock_target.logic.send_event('E_BEING_LOCK_TARGET', self.unit_obj.id, is_lock)