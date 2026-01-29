# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8004.py
from __future__ import absolute_import
import math3d
import game3d
from .ComGenericMechaEffect import ComGenericMechaEffect
_HASH_emissive_intensity = game3d.calc_string_hash('emissive_intensity')
HEAT_BRIGHT_TIME = 0.8
ACTION_INCREASE = 1
ACTION_DECREASE = 2
MAX_HEAT_STATE_ID = 'max_heat'
MAX_HEAT_EFFECT_ID = '20'
PVE_ALL_DIR_DASH_DMG_EFFECT_ID = '21'

class ComMechaEffect8004(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_DEATH': '_on_died',
       'E_TRY_IN_MAX_HEAT': '_in_max_heat',
       'E_TRY_OUT_MAX_HEAT': '_out_max_heat',
       'E_ON_LEAVE_MECHA': '_leave_mecha',
       'E_MECHA_LOD_LOADED_FIRST': ('initialize_emissive', 10),
       'E_CREATE_ALL_DIR_DASH_DMG_EFFECT': 'on_create_all_dir_dash_dmg_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8004, self).init_from_dict(unit_obj, bdict)
        self._cur_bright_time = 0
        self._cur_bright_action = ACTION_INCREASE
        self._is_in_heat = False
        self.ori_intensity = {}
        self.max_intensity = {}
        self.min_intensity = {}

    def tick(self, dt):
        if not self.ev_g_in_max_heat():
            self._out_max_heat()
            return
        model = self.ev_g_model()
        if model:
            if not self.max_intensity or not self.min_intensity:
                return
            if self._cur_bright_action == ACTION_INCREASE:
                self._cur_bright_time += dt
                if self._cur_bright_time >= HEAT_BRIGHT_TIME:
                    self._cur_bright_time = HEAT_BRIGHT_TIME
                    self._cur_bright_action = ACTION_DECREASE
                for index, max_intensity in self.max_intensity.items():
                    min_intensity = self.min_intensity[index]
                    cur_bright = min_intensity + (max_intensity - min_intensity) * (self._cur_bright_time / HEAT_BRIGHT_TIME)
                    sub_material = model.get_sub_material(index)
                    if sub_material:
                        sub_material.set_var(_HASH_emissive_intensity, 'emissive_intensity', cur_bright)

            else:
                self._cur_bright_time -= dt
                if self._cur_bright_time <= 0:
                    self._cur_bright_time = 0
                    self._cur_bright_action = ACTION_INCREASE
                for index, max_intensity in self.max_intensity.items():
                    min_intensity = self.min_intensity[index]
                    cur_bright = max_intensity - (max_intensity - min_intensity) * ((HEAT_BRIGHT_TIME - self._cur_bright_time) / HEAT_BRIGHT_TIME)
                    sub_material = model.get_sub_material(index)
                    if sub_material:
                        sub_material.set_var(_HASH_emissive_intensity, 'emissive_intensity', cur_bright)

    def destroy(self):
        self.clear_heat_sfx()
        super(ComMechaEffect8004, self).destroy()

    def initialize_emissive(self):
        model = self.ev_g_model()
        for index in range(model.get_submesh_count()):
            if index not in self.ori_intensity:
                sub_material = model.get_sub_material(index)
                if not sub_material:
                    continue
                var = sub_material.get_var(_HASH_emissive_intensity, 'emissive_intensity')
                if var is None:
                    continue
                self.ori_intensity[index] = var
                self.max_intensity[index] = var * 1.5
                self.min_intensity[index] = var * 3.5

        return

    def clear_heat_sfx(self):
        self.on_trigger_state_effect(MAX_HEAT_STATE_ID, '')

    def _in_max_heat(self):
        if self._is_in_heat:
            return
        self._is_in_heat = True
        self.on_trigger_state_effect(MAX_HEAT_STATE_ID, MAX_HEAT_EFFECT_ID)
        global_data.emgr.play_game_voice.emit('rage')
        self.need_update = True
        self._cur_bright_time = 0
        self._cur_bright_action = ACTION_INCREASE

    def _leave_mecha(self, *args):
        self.clear_heat_sfx()

    def _out_max_heat(self):
        self.clear_heat_sfx()
        self._is_in_heat = False
        self.need_update = False
        model = self.ev_g_model()
        if model:
            for index, var in self.ori_intensity.items():
                sub_material = model.get_sub_material(index)
                if sub_material:
                    sub_material.set_var(_HASH_emissive_intensity, 'emissive_intensity', var)

    def on_create_all_dir_dash_dmg_effect(self, pos, dir):
        self.on_trigger_disposable_effect(PVE_ALL_DIR_DASH_DMG_EFFECT_ID, pos, dir, need_sync=True)

    def _on_died(self):
        self._out_max_heat()