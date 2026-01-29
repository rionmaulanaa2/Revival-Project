# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComOilBottle.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import building_const
from logic.gcommon import time_utility
import math3d
import render
import game3d
_HASH_u_fade_time = game3d.calc_string_hash('u_fade_time')
FIRE_WALL_EFFECT = 'effect/fx/mecha/8012/8012_vice_huoqiang.sfx'

class ComOilBottle(UnitCom):
    BIND_EVENT = {'E_OIL_BOTTLE_ON_FIRE': 'on_fire',
       'E_MODEL_LOADED': 'on_model_loaded'
       }

    def __init__(self):
        super(ComOilBottle, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComOilBottle, self).init_from_dict(unit_obj, bdict)
        self.state = bdict.get('building_state', building_const.B_OIL_BOTTLE_STATE_BOTTLE)
        pos = bdict.get('position', [0, 0, 0])
        self.fire_end_time = bdict['birthtime'] + bdict['fire_lifetime']
        self.firing = False
        self.model = None
        self.sid = None
        self.sfx = None
        self.pos = math3d.vector(*pos)
        self._oil_player_id = None
        return

    def cache(self):
        self.clear_fire_effect()
        super(ComOilBottle, self).cache()

    def on_model_loaded(self, model):
        if self.state == building_const.B_OIL_BOTTLE_STATE_FIRE:
            model.visible = False
            self.create_fire_effect()
        self.model = model
        if self.firing:
            model.visible = False
        global_data.sound_mgr.play_event('m_8012_weapon1_hit_3p', model.position)

    def on_fire(self, fighter_id):
        self.firing = True
        if self.model:
            self.model.visible = False
        self.create_fire_effect()
        self.state = building_const.B_OIL_BOTTLE_STATE_FIRE

    def create_fire_effect(self):

        def create_cb(sfx):
            self.sfx = sfx
            sfx.scale = math3d.vector(0.33, 0.33, 0.33)

        self.sid = global_data.sfx_mgr.create_sfx_in_scene(FIRE_WALL_EFFECT, self.pos, duration=-1, on_create_func=create_cb, ex_data={'allow_overlay': True})
        self._oil_player_id = global_data.sound_mgr.play_event('m_8012_weapon1_hit_loop_3p', self.pos)

    def clear_fire_effect(self):
        cur_time = time_utility.get_server_time()
        if cur_time < self.fire_end_time - 0.5:
            global_data.sfx_mgr.remove_sfx_by_id(self.sid)
        elif self.sfx and self.sfx.valid:
            self.fade_out_sfx(self.sfx, self.sid)
        self.sid = None
        self.sfx = None
        self.model = None
        if self._oil_player_id:
            global_data.sound_mgr.stop_playing_id(self._oil_player_id)
            self._oil_player_id = None
        return

    def destroy(self):
        self.clear_fire_effect()
        super(ComOilBottle, self).destroy()

    def fade_out_sfx(self, sfx, sfx_id):
        decal_fadeout_time = 1.0
        decal_life_time = decal_fadeout_time * 1000
        for sub_idx in range(sfx.get_subfx_count()):
            if not sfx.is_sub_decal(sub_idx):
                continue
            material = sfx.get_sub_decal_material(sub_idx)
            if not material:
                continue
            material.set_var(_HASH_u_fade_time, 'u_fade_time', decal_fadeout_time)
            ttl = (render.get_frametime() + decal_life_time) / 1000.0
            sfx.set_sub_decal_ttl(sub_idx, ttl)

        def delay_cb():
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        global_data.game_mgr.delay_exec(decal_fadeout_time, delay_cb)