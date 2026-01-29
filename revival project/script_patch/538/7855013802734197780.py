# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPuzzleAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
import math3d
from common.cfg import confmgr
from logic.gcommon.common_const import pve_const

class ComPuzzleAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HEALTH_HP_EMPTY': '_on_explode',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_COLLISION_INFO': '_get_collision_info',
       'E_SCENE_BOX_STAT_CHANGE': 'on_box_state_change'
       })

    def __init__(self):
        super(ComPuzzleAppearance, self).__init__()
        self.custom_model_name = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPuzzleAppearance, self).init_from_dict(unit_obj, bdict)
        self.puzzle_type = bdict.get('puzzle_type', pve_const.PUZZLE_TYPE_BOMB)
        self.npc_id = bdict.get('npc_id', 0)

    def _on_explode(self, *args):
        pass

    def get_puzzle_config(self):
        conf_key = None
        if self.puzzle_type == pve_const.PUZZLE_TYPE_BOMB:
            conf_key = 'BombConf'
        if not conf_key:
            return {}
        else:
            return confmgr.get('pve/puzzle_data', conf_key, 'Content', default={})

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('yaw', 0)
        data = {'position': math3d.vector(*pos),
           'rotation': rotation
           }
        print (
         'gggggggggggggggg', data)
        puzzle_config = self.get_puzzle_config()
        model_path = puzzle_config.get(str(self.npc_id), {}).get('model_res', '')
        return (
         model_path, None, data)

    def on_load_model_complete(self, model, userdata):
        model.position = userdata['position']
        print ('pppppppppppppp', userdata)
        m = math3d.matrix.make_rotation_y(userdata['rotation'])
        model.rotation_matrix = m
        model.lod_config = (1280, 10000)

    def _get_collision_info(self):
        return {'custom_box': (0.5, 0.8, 0.5),'offset': math3d.vector(0.0, 0.8, 0.0)}

    def on_box_state_change(self, *args):
        pass

    def destroy(self):
        super(ComPuzzleAppearance, self).destroy()