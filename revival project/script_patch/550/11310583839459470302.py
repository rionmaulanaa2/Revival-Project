# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8015.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from mobile.common.EntityManager import EntityManager
from common.utils import timer
import world
import math3d
import game3d
import render
import logic.gcommon.const as g_const
_HASH_Rim_intensity = game3d.calc_string_hash('Rim_intensity')
_HASH_AlphaFix = game3d.calc_string_hash('AlphaFix')
LIGHTNING_CHAIN_EFFECT_ID = '20'
LIGHTNING_SPHERE_EFFECT_ID = '21'

class ComMechaEffect8015(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_CHRACTER_INITED': 'on_character_init',
       'E_DO_OXRUSH_8015': '_on_rush',
       'E_OXRUSH_8015_LOCK_TARGET': '_on_lock_target',
       'E_CHANGE_ENHANCE_WEAPON_FIRE_8015': '_on_change_enhance_weapon_fire'
       })
    DASH_ANIM = {
     'dash_lod_f', 'dash_start_f', 'dash_stop_f'}

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8015, self).init_from_dict(unit_obj, bdict)
        self.check_timer = None
        self.mask = None
        self.last_anim_name = None
        self.enhance_sfx_id = None
        effect_infos = self.ev_g_mecha_readonly_effect_info()
        self._chain_sfx_path = effect_infos[LIGHTNING_CHAIN_EFFECT_ID][0]['final_correspond_path']
        self._sphere_sfx_path = effect_infos[LIGHTNING_SPHERE_EFFECT_ID][0]['final_correspond_path']
        return

    def destroy(self):
        self.clear_check_timer()
        self.enhance_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self.enhance_sfx_id)
        self.enhance_sfx_id = None
        super(ComMechaEffect8015, self).destroy()
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8015, self).on_model_loaded(model)

    def on_character_init(self, character):
        self.mask = character.filter
        self.check_col()

    def _check_dask(self):
        if not self.mask:
            return
        is_hit = self.ev_g_static_test(mask=self.mask)
        if not is_hit:
            self.send_event('E_SET_CHAR_MASK', self.mask)
            self.clear_check_timer()

    def _on_rush(self, is_rush):
        if is_rush:
            self.send_event('E_SET_CHAR_MASK', ~self.mask)
        else:
            self.start_check_dask()

    def start_check_dask(self):
        self.clear_check_timer()
        self.check_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_dask, mode=timer.CLOCK, interval=0.5)

    def clear_check_timer(self):
        self.check_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_timer)
        self.check_timer = None
        return

    def check_col(self):
        if not self.mask:
            return
        is_hit = self.ev_g_static_test(mask=self.mask)
        if is_hit:
            self.send_event('E_SET_CHAR_MASK', ~self.mask)
            self.start_check_dask()

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        if not global_data.feature_mgr.is_support_model_decal():
            if self.last_anim_name not in self.DASH_ANIM and anim_name in self.DASH_ANIM:
                self.send_event('E_PAUSE_OUTLINE', True)
        super(ComMechaEffect8015, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if not global_data.feature_mgr.is_support_model_decal():
            if self.last_anim_name in self.DASH_ANIM and anim_name not in self.DASH_ANIM:
                self.send_event('E_REFRESH_MODEL')
                self.send_event('E_PAUSE_OUTLINE', False)
        self.last_anim_name = anim_name

    def _on_lock_target(self, lock_target_ids):
        mecha_model = self.ev_g_model()
        for lock_target_id in lock_target_ids:
            entity = EntityManager.getentity(lock_target_id)
            if not (entity and entity.logic):
                return

            def create_cb(sfx):
                if entity and entity.logic and entity.logic.is_enable():
                    model = entity.logic.ev_g_model() if 1 else None
                    return model or None
                else:
                    if model and model.valid:
                        sfx.endpos_attach(model, 'fx_buff', True)
                    return

            if mecha_model:
                global_data.sfx_mgr.create_sfx_on_model(self._chain_sfx_path, mecha_model, 'fx_buff', on_create_func=create_cb)

    def _on_change_enhance_weapon_fire(self, is_switch):
        sockets = [
         'fx_1_kaihuo_r', 'fx_1_kaihuo_l']
        socket_index = self.ev_g_socket_index(g_const.PART_WEAPON_POS_MAIN1)
        mecha_model = self.ev_g_model()
        self.enhance_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self.enhance_sfx_id)
        self.enhance_sfx_id = None
        if is_switch:
            if mecha_model:
                self.enhance_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self._sphere_sfx_path, mecha_model, sockets[socket_index])
        return