# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/SysMapEffectMgr.py
from __future__ import absolute_import
import six
import six_ex
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import math3d
import world

class SysMapEffectMgr(ScenePartSysBase):

    def __init__(self):
        super(SysMapEffectMgr, self).__init__()
        self.init_parameters()
        self.process_event(True)
        self.on_update_control_point()

    def init_parameters(self):
        self.occupy_part_effect = {}
        self.occupy_part_sfx = confmgr.get('script_gim_ref')['occupy_part_sfx']
        self.occupy_part_size_sfx = confmgr.get('script_gim_ref')['occupy_part_size_sfx']

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_control_point': self.on_update_control_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_update_control_point(self):
        if not global_data.death_battle_data:
            return
        if not hasattr(global_data.death_battle_data, 'part_data'):
            return
        control_point_dict = global_data.death_battle_data.part_data
        new_controls = set(six_ex.keys(control_point_dict))
        cur_controls = set(six_ex.keys(self.occupy_part_effect))
        del_controls = cur_controls - new_controls
        for part_id in del_controls:
            data = self.occupy_part_effect[part_id]
            sfx = data.get('sfx')
            if sfx:
                sfx.destroy()
            size_sfx_id = data.get('size_sfx_id')
            if size_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(size_sfx_id)
            del self.occupy_part_effect[part_id]

        for part_id, data_obj in six.iteritems(control_point_dict):
            position = data_obj.data['position']
            range = data_obj.data['range']
            position = math3d.vector(*position)
            size_sfx_index = data_obj.control_side
            if part_id not in self.occupy_part_effect:
                self.occupy_part_effect[part_id] = {}
                self.create_sfx(part_id, position)
                self.create_size_sfx(part_id, range, position, size_sfx_index)
            elif self.occupy_part_effect[part_id]['pos'] != position:
                global_data.sfx_mgr.remove_sfx_by_id(self.occupy_part_effect[part_id]['sfx_id'])
                global_data.sfx_mgr.remove_sfx_by_id(self.occupy_part_effect[part_id]['size_sfx_id'])
                self.create_sfx(part_id, position)
                self.create_size_sfx(part_id, range, position, size_sfx_index)
            elif self.occupy_part_effect[part_id]['size_sfx_index'] != size_sfx_index:
                global_data.sfx_mgr.remove_sfx_by_id(self.occupy_part_effect[part_id]['size_sfx_id'])
                self.create_size_sfx(part_id, range, position, size_sfx_index)

    def create_sfx(self, part_id, position):
        sfx = world.sfx(self.occupy_part_sfx, scene=self.get_scene())
        sfx.world_position = position
        self.occupy_part_effect[part_id]['pos'] = position
        self.occupy_part_effect[part_id]['sfx'] = sfx

    def create_size_sfx(self, part_id, range, position, size_sfx_index):

        def create_cb(sfx):
            scale = range / (50.0 * NEOX_UNIT_SCALE)
            sfx.scale = math3d.vector(scale, 3.0, scale)

        size_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.occupy_part_size_sfx[size_sfx_index], position, on_create_func=create_cb)
        self.occupy_part_effect[part_id]['size_sfx_id'] = size_sfx_id
        self.occupy_part_effect[part_id]['size_sfx_index'] = size_sfx_index

    def destroy(self):
        for part_id, data in six.iteritems(self.occupy_part_effect):
            sfx = data.get('sfx')
            if sfx:
                sfx.destroy()
            size_sfx_id = data.get('size_sfx_id')
            if size_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(size_sfx_id)

        self.occupy_part_effect = {}
        self.process_event(False)