# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupySfxMgr.py
from __future__ import absolute_import
import six
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import math3d
import world

class MutiOccupySfxMgr(object):

    def __init__(self):
        self.init_parameters()
        self.process_event(True)

    def init_parameters(self):
        self.occupy_sfx_dict = {}
        self.occupy_sfx = confmgr.get('script_gim_ref')['muti_occupy_point_model']

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_occupy_point_state': self.update_occupy_point_state,
           'updata_occupy_sfx_size': self.update_occupy_sfx_size
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_occupy_point_state(self):
        if not global_data.death_battle_data:
            return
        if self.occupy_sfx_dict:
            return
        occupy_data = global_data.death_battle_data.occupy_data
        for part_id, occupy in six.iteritems(occupy_data):
            data = occupy.get_occupy_base_data()
            self.create_size_sfx(part_id, data)

    def create_size_sfx(self, part_id, data):
        pos = data.get('c_center', [0, 0, 0])
        yaw = data.get('yaw', 0)
        size = data.get('c_size', [1, 1, 1])
        scale = [size[0] / 347.462, 0.1, size[2] / 467.158]
        sfx = world.model(self.occupy_sfx, scene=self.get_scene())
        sfx.world_position = math3d.vector(*pos)
        sfx.scale = math3d.vector(*scale)
        sfx.rotation_matrix = math3d.matrix.make_rotation_y(yaw * 3.1415926 / 180)
        self.occupy_sfx_dict[part_id] = sfx

    def get_scene(self):
        return world.get_active_scene()

    def destroy(self):
        for key, sfx in six.iteritems(self.occupy_sfx_dict):
            sfx.destroy()

        self.occupy_sfx_dict = {}
        self.process_event(False)

    def update_occupy_sfx_size(self, idx, pos, scale, yaw):
        return
        sfx = self.occupy_sfx_dict.get(idx)
        if sfx:
            sfx.world_position = math3d.vector(*pos)
            sfx.scale = math3d.vector(scale[0] / 347.462, 0.1, scale[2] / 467.158)
            sfx.rotation_matrix = math3d.matrix.make_rotation_y(yaw * 3.1415926 / 180)