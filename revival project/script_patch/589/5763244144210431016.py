# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8008.py
from __future__ import absolute_import
import world
import weakref
from common.cfg import confmgr
import logic.gcommon.const as g_const
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gutils.mecha_utils import get_fire_end_posiiton
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'

class ComMechaEffect8008(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_ACC_WP_TRACK': 'show_weapon_track',
       'E_STOP_ACC_WP_TRACK': 'stop_weapon_track'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8008, self).init_from_dict(unit_obj, bdict)
        self.weapon_pos = g_const.PART_WEAPON_POS_MAIN2
        self._model_ref = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8008, self).on_model_loaded(model)
        self._model_ref = weakref.ref(model)

    def show_weapon_track(self):
        if global_data.mecha and self.unit_obj != global_data.mecha.logic:
            return
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
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
        if fire_sockets:
            self._fire_socket = fire_sockets[0] if 1 else 'missile00'
            position = self.get_fire_pos()
            return position or None
        direction = self.cal_direction(position)
        self.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, self._speed, self._g, self._up_angle, direction=direction, mass=mass, linear_damping=linear_damp)
        self.need_update = True

    def stop_weapon_track(self):
        self.need_update = False
        self.send_event('E_HIDE_PARABOLA_TRACK')

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
        position = self.get_fire_pos()
        if not position:
            return
        direction = self.cal_direction(position)
        self.send_event('E_UPDATE_PARABOLA_TRACK', position, direction)