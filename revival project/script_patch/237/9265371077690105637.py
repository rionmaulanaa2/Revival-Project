# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterEffect.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import collision
import logic.gcommon.common_utils.bcast_utils as bcast
from common.cfg import confmgr
FIRE_EFFECT_BIG = {'effect/fx/mecha/8012/8012_vice_ranshao_01.sfx': ['fx_buff']}
OIL_EFFECT = {'effect/fx/mecha/8012/8012_youwu.sfx': ['fx_buff']}
DIZZINESS_EFFECT = {'effect/fx/monster/pve/monster_stun.sfx': ['fx_buff']}
EMP_EFFECT = {'effect/fx/robot/autobot/dianliu_all.sfx': ['fx_buff']}
HIT_SFX = 'effect/fx/robot/common/shouji_fresnel.sfx'
HIT_SFX_PVE = 'effect/fx/robot/common/shouji_fresnel_pve.sfx'
HIT_SOCKET = 'fx_buff'

class ComMonsterEffect(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_CREATE_SCENE_EFFECT': 'on_create_scene_effect',
       'E_CREATE_MODEL_EFFECT': 'on_create_model_effects',
       'E_REMOVE_MODEL_EFFECT': 'on_remove_model_effects',
       'E_OIL_EFFECT': 'on_oil_effect',
       'E_FIRE_EFFECT': 'on_fire_effect',
       'E_ACTIVE_DIZZINESS': 'on_dizziness_effect',
       'E_SHOW_PART_HIGHLIGHT': '_on_show_highlight',
       'E_CHRACTER_INITED': 'on_character_init',
       'E_DO_OXRUSH_MONSTER': '_on_rush',
       'E_ACTIVE_EMP': 'on_emp_effect'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMonsterEffect, self).init_from_dict(unit_obj, bdict)
        self.hit_sfx_id = None
        self._model_sfx_ids = {}
        self.check_timer = None
        self.mask = None
        self.monster_id = bdict.get('npc_id')
        self.is_pve = global_data.game_mode.is_pve()
        self.is_firing = False
        self.is_dizziness = False
        self.is_emp = False
        return

    def destroy(self):
        self.clear_check_timer()
        super(ComMonsterEffect, self).destroy()
        self.clear_model_sfxs()
        self.is_firing = False
        self.is_dizziness = False
        self.is_emp = False

    def on_model_loaded(self, model):
        if self.ev_g_oil_debuff():
            self.on_oil_effect(True)
        if self.ev_g_fire_debuff():
            self.on_fire_effect(True)
        if self.ev_g_dizziness_debuff():
            self.on_dizziness_effect(True)
        if self.ev_g_emp_debuff():
            self.on_emp_effect(True)
        anim_conf = confmgr.get('monster_data', 'AnimShakeSfx', 'Content', str(self.monster_id), default=None)
        if anim_conf:
            conf = anim_conf.get('Triggers')
            for anim in conf:
                events = conf[anim]
                for event in events:
                    if model.has_anim_event(anim, event):
                        sfx_path = events[event]
                        self.send_event('E_REGISTER_ANIM_KEY_EVENT', anim, event, self.play_shake_sfx, sfx_path, True)

        return

    def play_shake_sfx(self, model, anim, event, sfx_path):
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path)

    def on_oil_effect(self, show):
        if show:
            if self.hit_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)
            self.on_create_model_effects(**OIL_EFFECT)
        else:
            self.on_remove_model_effects(**OIL_EFFECT)

    def on_fire_effect(self, show, big_fire=False):
        if self.is_firing ^ show:
            if show:
                self.on_create_model_effects(**FIRE_EFFECT_BIG)
            else:
                self.on_remove_model_effects(**FIRE_EFFECT_BIG)
            self.is_firing = show

    def on_dizziness_effect(self, show):
        if self.is_dizziness ^ show:
            if show:
                self.on_create_model_effects(**DIZZINESS_EFFECT)
            else:
                self.on_remove_model_effects(**DIZZINESS_EFFECT)
            self.is_dizziness = show

    def on_emp_effect(self, show):
        if self.is_emp ^ show:
            if show:
                self.on_create_model_effects(**EMP_EFFECT)
            else:
                self.on_remove_model_effects(**EMP_EFFECT)
            self.is_emp = show

    def _on_show_highlight(self, hit_parts, *args):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            shield = self.ev_g_shield()
            if shield is not None and shield > 0:
                return

            def on_remove_func(sfx):
                if not self or not self.is_valid():
                    return
                else:
                    self.hit_sfx_id = None
                    return

            if self.hit_sfx_id:
                return
            sfx_res = HIT_SFX_PVE if self.is_pve else HIT_SFX
            self.hit_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_res, model, HIT_SOCKET, on_remove_func=on_remove_func)
            return

    def on_create_model_effects(self, **info):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                self._model_sfx_ids[sfx_id_key] = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

    def on_remove_model_effects(self, **info):
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                    del self._model_sfx_ids[sfx_id_key]

    def clear_model_sfxs(self):
        for sfx_id in six.itervalues(self._model_sfx_ids):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._model_sfx_ids = {}

    def on_create_scene_effect(self, sfx, pos, duration):
        global_data.sfx_mgr.create_sfx_in_scene(sfx, math3d.vector(*pos), duration=duration)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx, pos, duration)], True)

    def on_character_init(self, character):
        self.mask = character.filter
        self.check_col()

    def _on_rush(self, is_rush):
        if is_rush:
            self.send_event('E_SET_CHAR_MASK', ~self.mask)
        else:
            self.start_check_dask()

    def _check_dask(self):
        if not self.mask:
            return
        is_hit = self.ev_g_static_test(mask=self.mask)
        if not is_hit:
            self.send_event('E_SET_CHAR_MASK', self.mask)
            self.clear_check_timer()

    def start_check_dask(self):
        self.clear_check_timer()
        self.check_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_dask, mode=2, interval=0.5)

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