# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEDynamicDoorAppearance.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from math import pi
import world
from .ComBaseModelAppearance import ComBaseModelAppearance

class ComPVEDynamicDoorAppearance(ComBaseModelAppearance):
    BIND_EVENT = {}
    RES_PATH = {'01': 'effect/mesh/scenes/quyutexiao/pve_battalion_blue.gim',
       '02': 'effect/mesh/scenes/quyutexiao/pve_battalion_blue_80.gim'
       }
    UP = math3d.vector(0, 1, 0)
    SCALE_Z = 0.02

    def __init__(self):
        super(ComPVEDynamicDoorAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEDynamicDoorAppearance, self).init_from_dict(unit_obj, bdict)
        self.pos_left = math3d.vector(*bdict.get('pos_left'))
        self.pos_right = math3d.vector(*bdict.get('pos_right'))
        self.scale = bdict.get('scale')
        self.offset = bdict.get('offset')

    def get_model_info(self, unit_obj, bdict):
        env_key = global_data.battle or '01' if 1 else global_data.battle.get_env_key()
        return (
         self.RES_PATH.get(env_key, 'effect/mesh/scenes/quyutexiao/pve_battalion_blue.gim'), None, None)

    def on_load_model_complete(self, model, user_data):
        pos = (self.pos_left + self.pos_right) * 0.5
        pos.y += self.offset
        diff = self.pos_left - self.pos_right
        diff.y = 0
        diff.normalize()
        r = diff.cross(self.UP)
        r.normalize()
        r_matrix = math3d.matrix.make_orient(r, self.UP)
        scale_x = (self.pos_left - self.pos_right).length / (model.bounding_box.x * 2.0)
        scale_x *= self.scale
        scale_z = self.SCALE_Z
        model.world_scale = math3d.vector(scale_x, 1.0, scale_z)
        model.rotation_matrix = r_matrix
        model.world_position = pos
        model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)

    def destroy(self):
        super(ComPVEDynamicDoorAppearance, self).destroy()