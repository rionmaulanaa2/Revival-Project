# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8034.py
from __future__ import absolute_import
import world
import weakref
from common.cfg import confmgr
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gutils.mecha_utils import get_fire_end_posiiton
from logic.gcommon.const import PART_WEAPON_POS_MAIN2
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
TRACK_WEAPON_POS = PART_WEAPON_POS_MAIN2
SEC_WP_ACC_SFX_ID = '101'
SEC_WP_ACC_STATE_ID = 'sec_wp_acc'
POISON_JUMP_PM_SFX_ID = '102'
POISON_JUMP_PM_STATE_ID = 'poison_jump_pm'
POISON_JUMP_SFX_ID = '103'
POISON_JUMP_STATE_ID = 'poison_jump'
STEAL_FUEL_SFX_DURATION = 1.5
UPDATE_REASON_WP_TRACK = 'weapon_track'
UPDATE_REASON_STEAL_FUEL = 'steal_fuel'

class ComMechaEffect8034(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_ACC_WP_TRACK': 'show_weapon_track',
       'E_STOP_ACC_WP_TRACK': 'stop_weapon_track',
       'E_SHOW_SEC_WP_ACC': 'show_sec_weapon_acc',
       'E_SHOW_POISON_JUMP_SFX': 'show_poison_jump_sfx'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8034, self).init_from_dict(unit_obj, bdict)
        self._model_ref = None
        self.need_update_reason = set()
        self.is_avatar = self.ev_g_is_avatar()
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8034, self).on_model_loaded(model)
        self._model_ref = weakref.ref(model)

    def show_weapon_track(self):
        if global_data.mecha and self.unit_obj != global_data.mecha.logic:
            return
        weapon = self.sd.ref_wp_bar_mp_weapons.get(TRACK_WEAPON_POS)
        if not weapon:
            return
        conf = confmgr.get('grenade_config', str(weapon.iType))
        self._speed = conf['fSpeed']
        self._g = self.scene.scene_col.gravity.y
        self._up_angle = conf.get('fUpAngle', 0)
        mass = conf.get('fMass', 1.0)
        linear_damp = conf.get('fLinearDamp', 0.0)
        conf = confmgr.get('firearm_res_config', str(weapon.iType))
        fire_sockets = conf.get('cBindPointEmission')
        if not fire_sockets:
            return
        self._fire_socket = fire_sockets[0]
        position = self.get_fire_pos()
        if not position:
            return
        direction = self.cal_direction(position)
        self.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, self._speed, self._g, self._up_angle, direction=direction, mass=mass, linear_damping=linear_damp)
        self.set_need_update(True, UPDATE_REASON_WP_TRACK)

    def stop_weapon_track(self):
        self.send_event('E_HIDE_PARABOLA_TRACK')
        self.set_need_update(False, UPDATE_REASON_WP_TRACK)

    def get_fire_pos(self):
        model = self._model_ref()
        if not model or not model.valid:
            return None
        else:
            socket_matrix = model.get_socket_matrix(self._fire_socket, world.SPACE_TYPE_WORLD)
            if not socket_matrix:
                return None
            return socket_matrix.translation

    def cal_direction(self, position):
        end_pos = get_fire_end_posiiton(self.unit_obj)
        direction = end_pos - position
        if not direction.is_zero:
            direction.normalize()
        return direction

    def tick(self, delta):
        if UPDATE_REASON_WP_TRACK in self.need_update_reason:
            position = self.get_fire_pos()
            if not position:
                return
            direction = self.cal_direction(position)
            self.send_event('E_UPDATE_PARABOLA_TRACK', position, direction)

    def set_need_update(self, need_update, reason=None):
        if need_update and reason not in self.need_update_reason:
            self.need_update_reason.add(reason)
        elif not need_update and reason in self.need_update_reason:
            self.need_update_reason.remove(reason)
        self.need_update = bool(self.need_update_reason)

    def show_sec_weapon_acc(self, show):
        self.on_trigger_state_effect(SEC_WP_ACC_STATE_ID, SEC_WP_ACC_SFX_ID if show else '', need_sync=True)

    def show_poison_jump_sfx(self, show):
        self.on_trigger_state_effect(POISON_JUMP_STATE_ID, POISON_JUMP_SFX_ID if show else '', need_sync=True)
        self.on_trigger_state_effect(POISON_JUMP_PM_STATE_ID, POISON_JUMP_PM_SFX_ID if self.is_avatar and show else '')