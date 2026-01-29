# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSnowmanAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
from common.cfg import confmgr
from logic.gutils.scene_utils import SNOW_SCENE_BOX_MODEL_ENT_MAP

class ComSnowmanAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HEALTH_HP_EMPTY': '_on_explode',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_COLLISION_INFO': '_get_collision_info',
       'E_SCENE_BOX_STAT_CHANGE': 'on_box_state_change'
       })

    def __init__(self):
        super(ComSnowmanAppearance, self).__init__()
        self.custom_model_name = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSnowmanAppearance, self).init_from_dict(unit_obj, bdict)
        self.snowman_state = bdict.get('state', None)
        return

    def _on_explode(self, *args):
        pass

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('yaw', 0)
        snowman_index = bdict.get('appearance', 0)
        self.custom_model_name = 'snowman_0%s_%s' % (snowman_index + 1, str(self.unit_obj.id))
        data = {'position': math3d.vector(*pos),
           'rotation': rotation,
           'custom_model_name': self.custom_model_name,
           'custom_model_name_prefix': 'snowman_0%s' % (snowman_index + 1,)
           }
        SNOW_SCENE_BOX_MODEL_ENT_MAP[self.custom_model_name] = self.unit_obj.id
        snowman_path = confmgr.get('script_gim_ref')['snowman_res']
        model_path = snowman_path.get(str(snowman_index), snowman_path['0'])
        return (
         model_path, None, data)

    def on_load_model_complete(self, model, userdata):
        model.position = userdata['position']
        m = math3d.matrix.make_rotation_y(userdata['rotation'])
        model.rotation_matrix = m
        model.lod_config = (1280, 10000)

    def _get_collision_info(self):
        return {'custom_box': (0.5, 0.8, 0.5),'offset': math3d.vector(0.0, 0.8, 0.0)}

    def on_box_state_change(self, *args):
        pass

    def destroy(self):
        SNOW_SCENE_BOX_MODEL_ENT_MAP.pop(self.custom_model_name, None)
        super(ComSnowmanAppearance, self).destroy()
        return