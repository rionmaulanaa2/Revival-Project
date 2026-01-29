# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComIcewallAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import world
import math3d
import weakref
import game3d
from common.cfg import confmgr
from logic.client.path_utils import ICW_WALL_EXPLODE
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComIcewallAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BUILDING_EXPLODE': '_on_explode',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_COLLISION_INFO': '_get_collision_info'
       })

    def __init__(self):
        super(ComIcewallAppearance, self).__init__()
        self.source_custom_box = (4.3, 2.7, 1.5)
        self.custom_box = (4.3, 2.7, 1.5)
        self.model_scale = (1.0, 1.0, 1.0)
        self.offset = (0.0, 2.7, 0.0)

    def init_from_dict(self, unit_obj, bdict):
        super(ComIcewallAppearance, self).init_from_dict(unit_obj, bdict)
        col_size = bdict['col_size']
        if col_size:
            src_col = self.source_custom_box
            self.model_scale = (1.0 * col_size[0] / src_col[0], 1.0 * col_size[1] / src_col[1], 1.0 * col_size[2] / src_col[2])
            self.custom_box = (col_size[0], col_size[1], col_size[2])
            self.offset = (0, col_size[1], 0)

    def _on_explode(self, *args):
        if self._model and self._model.valid:
            self._model.visible = False
            self._model.play_animation('stand', -1.0, 0, 0, 2)
            global_data.sfx_mgr.create_sfx_in_scene(ICW_WALL_EXPLODE, self._model.position)
            global_data.sound_mgr.play_event('Play_useitem_ice_wall_end', self._model.position)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('rot', [0])[0]
        data = {'position': math3d.vector(*pos),'rotation': rotation}
        ice_wall_path = confmgr.get('script_gim_ref')['ice_wall_model']
        return (
         ice_wall_path, None, data)

    def on_load_model_complete(self, model, userdata):
        pos = userdata['position']
        model.position = pos
        model.world_scale = math3d.vector(*self.model_scale)
        m = math3d.matrix.make_rotation_y(userdata['rotation'])
        model.rotation_matrix = m
        model.play_animation('open', -1.0, 0, 0, 2)
        model.lod_config = (1280, 10000)
        global_data.sound_mgr.play_event('Play_useitem_ice_wall', pos)

    def _get_collision_info(self):
        return {'custom_box': self.custom_box,'offset': math3d.vector(*self.offset)}