# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8024.py
from __future__ import absolute_import
import six
import math3d
from .ComGenericMechaEffect import ComGenericMechaEffect
from common.cfg import confmgr
import world
import weakref
from logic.gcommon.const import PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN2
from logic.gutils.mecha_utils import get_fire_end_posiiton
from logic.gcommon.common_const.mecha_const import MECHA_8023_FORM_PISTOL
from logic.gutils.screen_effect_utils import create_screen_effect_with_auto_refresh, remove_screen_effect_with_auto_refresh
from logic.gcommon.common_utils.bcast_utils import E_REFRESH_SUB_MODEL_ANIM
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
HIT_SFX = '100'
SUICIDE_SCREEN_STATE_ID = 'suicide_screen'
SUICIDE_SCREEN_EFFECT_ID = '101'
FOOTPRINT_SFX = '102'
FOOLS_JOJO_SUB_MODEL_KEY = 'mask_jojo'

class ComMechaEffect8024(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_ACC_WP_TRACK': 'show_weapon_track',
       'E_STOP_ACC_WP_TRACK': 'stop_weapon_track',
       'E_CREATE_HOLD_EFFECT': 'on_trigger_hold_effect',
       'E_SHOW_SUICIDE_DASH_EFFECT': 'on_show_suiside_dash_effect',
       'E_UPDATE_SUICIDE_SCREEN_SFX': 'on_update_suisice_screen_effect',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'E_REFRESH_SUB_MODEL_ANIM': 'set_sub_model_anim'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8024, self).init_from_dict(unit_obj, bdict)
        self.weapon_pos = PART_WEAPON_POS_MAIN2
        self._model_ref = None
        self.cur_sub_model_anim = 'idle'
        self.cur_weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        return

    def set_weapon_form(self, weapon_form):
        self.cur_weapon_form = weapon_form

    def on_model_loaded(self, model):
        super(ComMechaEffect8024, self).on_model_loaded(model)
        self._model_ref = weakref.ref(model)
        footprint_sfx_info = self.get_readonly_effect_info().get(FOOTPRINT_SFX, None)
        if footprint_sfx_info:
            self.footprint_sfx_info = {info['anim_event_name']:info for info in footprint_sfx_info}
            model.register_anim_key_event('run', 'step1', self.on_step)
            model.register_anim_key_event('run', 'step2', self.on_step)
        return

    def on_step(self, model, anim_name, anim_event_name):
        sfx_info = self.footprint_sfx_info.get(anim_event_name, None)
        if not sfx_info:
            return
        else:
            if sfx_info.get('level', 0) > self._cur_mecha_effect_level:
                return
            sfx_path = sfx_info.get('final_correspond_path', None)
            if not sfx_path:
                return
            socket_list = sfx_info.get('socket_list', None)
            if not socket_list:
                return

            def set_sfx_rot(sfx, rot_mat):
                sfx.rotation_matrix = rot_mat

            for socket in socket_list:
                socket_matrix = model.get_socket_matrix(socket, world.SPACE_TYPE_WORLD)
                if not socket_matrix:
                    continue
                pos = socket_matrix.translation
                pos.y = self.ev_g_position().y + 1
                forward = socket_matrix.forward
                forward.y = 0
                rot_mat = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=lambda sfx, rm=rot_mat: set_sfx_rot(sfx, rm), duration=2.8)

            return

    def show_weapon_track(self):
        if global_data.mecha and self.unit_obj != global_data.mecha.logic:
            return
        else:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
            if not weapon:
                return
            conf = confmgr.get('grenade_config', str(weapon.iType))
            self._speed = conf['fSpeed']
            self._g = -conf.get('fGravity', 98)
            self._up_angle = conf.get('fUpAngle', 0)
            mass = conf.get('fMass', 1)
            linear_damp = conf.get('fLinearDamp', 0)
            conf = confmgr.get('firearm_res_config', str(weapon.iType))
            self._fire_socket = conf.get('cBindPointEmission', None)
            if self._fire_socket:
                self._fire_socket = self._fire_socket[0]
            else:
                self._fire_socket = 'shoulei_fire'
            position = self.get_fire_pos()
            if not position:
                return
            self.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, self._speed, self._g, self._up_angle, mass=mass, linear_damping=linear_damp)
            self.need_update = True
            return

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

    def on_show_suiside_dash_effect(self):
        pos = self.ev_g_position()
        self.on_trigger_disposable_effect(HIT_SFX, (pos.x, pos.y, pos.z), need_sync=True)

    def on_update_suisice_screen_effect(self, show):
        effect_id = SUICIDE_SCREEN_EFFECT_ID if show else ''
        self.on_trigger_state_effect(SUICIDE_SCREEN_STATE_ID, effect_id, force=True, need_sync=True)

    def on_skin_sub_model_loaded(self):
        if self.ev_g_mecha_fashion_id() in (201802451, 201802452, 201802453):
            self.sd.ref_socket_res_agent.set_sfx_res_visible(False, 'h_only')
            self.sd.ref_socket_res_agent.set_model_res_visible(False, 'h_only')
            self.sd.ref_socket_res_agent.set_sfx_res_visible(True, 'l_only')
            self.sd.ref_socket_res_agent.set_model_res_visible(True, 'l_only')

    def set_sub_model_anim(self, anim):
        self.sd.ref_socket_res_agent.play_model_res_anim(anim, FOOLS_JOJO_SUB_MODEL_KEY)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_REFRESH_SUB_MODEL_ANIM, (anim,)], True)