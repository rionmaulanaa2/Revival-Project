# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHittableBoxAppearance.py
from __future__ import absolute_import
import math3d
from .ComBaseModelAppearance import ComBaseModelAppearance
from common.cfg import confmgr

class ComHittableBoxAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HEALTH_HP_CHANGE': '_on_hp_change',
       'E_HEALTH_HP_EMPTY': '_on_hp_empty'
       })

    def __init__(self):
        super(ComHittableBoxAppearance, self).__init__()
        self._box_id = None
        self._yaw = 0
        self._damage_sfx_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHittableBoxAppearance, self).init_from_dict(unit_obj, bdict)
        self._box_id = bdict['npc_id']
        self._yaw = bdict.get('yaw', 0)

    def destroy(self):
        self._remove_damage_sfx()
        super(ComHittableBoxAppearance, self).destroy()

    def get_model_info(self, unit_obj, bdict):
        conf = confmgr.get('box_res', str(self._box_id), default=None)
        rotation_matrix = math3d.matrix.make_rotation_y(self._yaw)
        model_scale = math3d.vector(*([conf.get('model_scale', 1)] * 3))
        return (
         conf['res'], None, (rotation_matrix, model_scale))

    def on_load_model_complete(self, model, user_data):
        super(ComHittableBoxAppearance, self).on_load_model_complete(model, user_data)
        model.rotation_matrix = user_data[0]
        model.scale = user_data[1]

    def cache(self):
        super(ComHittableBoxAppearance, self).cache()
        self._remove_damage_sfx()

    def _on_hp_empty(self):
        self._remove_damage_sfx()
        conf = confmgr.get('box_res', str(self._box_id), default=None)
        sfx_path, sfx_scale = conf.get('die_sfx', (None, None))
        if not sfx_path:
            return
        else:
            if sfx_scale != 1:

                def on_create_func(sfx):
                    sfx.scale = math3d.vector(*([sfx_scale] * 3))

            else:
                on_create_func = None
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self._position, duration=3, on_create_func=on_create_func)
            return

    def _create_damage_sfx(self):
        conf = confmgr.get('box_res', str(self._box_id), default=None)
        sfx_path, sfx_scale = conf.get('damage_sfx', (None, None))
        if not sfx_path:
            return
        else:
            if sfx_scale != 1:

                def on_create_func(sfx):
                    sfx.scale = math3d.vector(*([sfx_scale] * 3))

            else:
                on_create_func = None
            self._damage_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self._position, on_create_func=on_create_func)
            return

    def _remove_damage_sfx(self):
        if self._damage_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._damage_sfx_id)
            self._damage_sfx_id = None
        return

    def _on_hp_change(self, hp, mod):
        if self._damage_sfx_id:
            return
        if self.ev_g_health_percent() < 0.3:
            self._create_damage_sfx()