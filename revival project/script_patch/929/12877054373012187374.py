# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComConsoleAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import math3d
import world

class ComConsoleAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HITED': '_on_hited',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'G_COLLISION_INFO': '_get_collision_info'
       })
    CONSOLE_PATH = 'model_new/niudan/6007_monitor.gim'

    def __init__(self):
        super(ComConsoleAppearance, self).__init__()
        self._trigger_size = math3d.vector(0, 0, 0)

    def init_from_dict(self, unit_obj, bdict):
        super(ComConsoleAppearance, self).init_from_dict(unit_obj, bdict)
        tsize = bdict.get('trigger_size', [15, 15, 20])
        self._trigger_size = math3d.vector(*tsize)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        return (
         ComConsoleAppearance.CONSOLE_PATH, None, math3d.vector(*pos))

    def _get_collision_info(self):
        return {'offset': 'half_y'
           }

    def on_load_model_complete(self, model, userdata):
        pos = userdata
        model.position = pos
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            size = self._trigger_size
            if size.z / 2.0 > lpos.z > -size.z / 2.0 and size.y > abs(lpos.y):
                if size.x / 2.0 > lpos.x > -size.x / 2.0:
                    return (True, lpos.length)
        return (
         False, None)

    def destroy(self):
        drone_id = self.ev_g_relevance_id()
        drone = EntityManager.getentity(drone_id)
        if self.model and self.model.valid:
            if self.ev_g_hp() <= 0:
                mat = self.model.get_socket_matrix('fx_boom', world.SPACE_TYPE_WORLD)
                scale, pos = mat.scale, mat.translation

                def create_cb(sfx):
                    sfx.scale = scale

                sfx_path = 'effect/fx/niudan/daojubeicuihui_baozha.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
            elif drone:
                mat = self.model.get_socket_matrix('fx_lighting', world.SPACE_TYPE_WORLD)
                scale, pos = mat.scale, mat.translation

                def create_cb(sfx):
                    sfx.scale = scale

                sfx_path = 'effect/fx/niudan/daojubeicuihui.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
        self._trigger_size = None
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        super(ComConsoleAppearance, self).destroy()
        return

    def _on_hited(self):
        pos = self.model.world_position
        global_data.sound_mgr.play_sound_optimize('Play_bullet_hit', self.unit_obj, pos, ('bullet_hit_material',
                                                                                          'metal'))

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        super(ComConsoleAppearance, self)._on_be_hited(begin_pos, end_pos, shot_type, is_self=kwargs.get('is_self', False), dmg_parts=kwargs.get('dmg_parts', False))