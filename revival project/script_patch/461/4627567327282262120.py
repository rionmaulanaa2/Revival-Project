# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComMechaBackWeapon8027.py
from __future__ import absolute_import
import weakref
import world
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import PART_WEAPON_POS_MAIN2
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils.mecha_skin_utils import DEFAULT_RES_KEY
from common.utils import timer
from logic.gcommon.const import SOUND_TYPE_MECHA_FOOTSTEP
MODEL_SHADER_CTRL_SET_ENABLE = hasattr(world.model, 'set_inherit_parent_shaderctrl')

class ComMechaBackWeapon8027(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'E_ENERGY_CHANGE': '_on_energy_change',
       'E_CONTINUOUSSHOOT8027_ANIM_START': '_on_anim_start',
       'E_CONTINUOUSSHOOT8027_FIRE': '_on_fire',
       'E_SHOW_WEAPON8027': '_show_weapon'
       }
    WEAPON_KEYS = [
     'back_c', 'back_b', 'back_a']
    HAND_WEAPON_KEY = 'hand'

    def __init__(self):
        super(ComMechaBackWeapon8027, self).__init__()
        self.weapon_pos = PART_WEAPON_POS_MAIN2
        self.skill_id = 802751
        self.weapon_models = []
        self.show_num = 0
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'set_observe_target_id_event': self.on_observe_target_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaBackWeapon8027, self).init_from_dict(unit_obj, bdict)
        self.weapon_models = []
        self.mecha_id = bdict['mecha_id']

    def on_observe_target_changed(self, *args, **kargs):
        self._show_weapon(self.show_num)

    def refresh_weapon_num(self, percent=None):
        skill_cost = self.ev_g_energy_cost(self.skill_id) or 1.0 / 3
        if percent is None:
            percent = self.ev_g_energy(self.skill_id) or 1.0
        percent += 0.05
        show_num = int(percent / skill_cost)
        if show_num == self.show_num:
            return
        else:
            self.show_num = show_num
            self._show_weapon(show_num)
            return

    def _show_weapon(self, show_num):
        for index, key in enumerate(self.WEAPON_KEYS):
            weapon_models = self.sd.ref_socket_res_agent.model_res_map.get(key)
            if weapon_models:
                o_visible = weapon_models[0].visible
                n_visible = show_num > index
                if n_visible:
                    if o_visible != n_visible:
                        for weapon_model in weapon_models:
                            weapon_model.play_animation('vice_end1' if index % 2 else 'vice_end2')
                            sound_name = ('m_8027_darts_return', 'nf')
                            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, None, None)

                    else:
                        for weapon_model in weapon_models:
                            weapon_model.play_animation('idle')

                self.sd.ref_socket_res_agent.set_model_res_visible(n_visible, key)

        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_WEAPON8027, (show_num,)], True)
        return

    def _on_model_loaded(self, model):
        pass

    def on_skin_sub_model_loaded(self):
        for key in self.WEAPON_KEYS:
            self.sd.ref_socket_res_agent.set_model_res_visible(False, key)

        self.refresh_weapon_num()

    def _on_energy_change(self, key, percent):
        if key == self.skill_id:
            self.refresh_weapon_num(percent)

    def _on_anim_start(self, sid):
        if self.show_num > 0:
            self.sd.ref_socket_res_agent.set_model_res_visible(False, self.WEAPON_KEYS[self.show_num - 1])
        self.sd.ref_socket_res_agent.set_model_res_visible(True, self.HAND_WEAPON_KEY)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CONTINUOUSSHOOT8027_ANIM_START, (sid,)], True)

    def _on_fire(self, sid):
        self.sd.ref_socket_res_agent.set_model_res_visible(False, self.HAND_WEAPON_KEY)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CONTINUOUSSHOOT8027_FIRE, (sid,)], True)
        sound_name = ('m_8027_darts_fire', 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)

    def destroy(self):
        super(ComMechaBackWeapon8027, self).destroy()
        self.process_event(False)
        self.weapon_models = []