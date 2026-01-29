# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyEffect.py
from __future__ import absolute_import
import six
import math
import math3d
from . import ScenePart
from common.cfg import confmgr
from random import randint

class PartLobbyEffect(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLobbyEffect, self).__init__(scene, name, True)

    def on_enter(self):
        effect_classify = confmgr.get('lobby_effect_conf', 'EffectClassify', 'Content')
        classify_count = len(effect_classify)
        cur_type = randint(1, classify_count)
        type_key = 'Type_%d' % cur_type
        effect_dic = confmgr.get('lobby_effect_conf', type_key, 'Content')
        for effect_info in six.itervalues(effect_dic):
            position = effect_info.get('position')
            position = math3d.vector(position[0], position[1], position[2])
            rotation = effect_info.get('rotation')
            rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rotation[0] / 180, math.pi * rotation[1] / 180, math.pi * rotation[2] / 180))
            scale = effect_info.get('scale')
            scale = math3d.vector(scale[0], scale[1], scale[2])
            res_path = effect_info.get('res_path')

            def on_create_func(sfx, world_scale=scale, world_rotation_matrix=rotation_matrix):
                sfx.world_scale = world_scale
                sfx.world_rotation_matrix = world_rotation_matrix

            global_data.sfx_mgr.create_sfx_in_scene(res_path, position, on_create_func=on_create_func)