# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCrystalCoverAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
from logic.comsys.battle import BattleUtils

class ComCrystalCoverAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'CRYSTAL_STAGE_CHANGE': 'on_crystal_stage_change'
       })

    def __init__(self):
        super(ComCrystalCoverAppearance, self).__init__()
        self.npc_id = None
        self.cover_data = None
        self.cover_pos = None
        self.cover_rot_mat = None
        self.cover_scale = None
        self.cover_birthtime = 0
        self.crystal_stage = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComCrystalCoverAppearance, self).init_from_dict(unit_obj, bdict)
        self.npc_id = bdict.get('npc_id')
        self.faction_id = bdict.get('faction_id')
        self.crystal_stage = bdict.get('crystal_stage')
        self.init_crystal_cover_data()
        self.cover_birthtime = bdict.get('cover_birthtime', 0)

    def init_crystal_cover_data(self):
        all_cover = global_data.game_mode.get_cfg_data('crystal_cover_data')
        self.cover_data = all_cover.get(str(self.npc_id))
        scale = self.cover_data.get('scale')
        self.cover_scale = math3d.vector(*scale)
        if self.crystal_stage is None:
            self.init_crystal_cover_data_without_stage()
        else:
            self.init_crystal_cover_data_with_stage()
        return

    def init_crystal_cover_data_without_stage(self):
        pos = self.cover_data.get('pos')
        self.cover_pos = math3d.vector(pos[0], pos[1], pos[2])
        rot = self.cover_data.get('rot')
        self.cover_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))

    def init_crystal_cover_data_with_stage(self):
        pos_list = self.cover_data.get('pos')
        pos = pos_list[self.crystal_stage]
        self.cover_pos = math3d.vector(pos[0], pos[1], pos[2])
        rot_list = self.cover_data.get('rot')
        rot = rot_list[self.crystal_stage]
        self.cover_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))

    def get_model_info(self, unit_obj, bdict):
        model_path = self.cover_data.get('model_path')
        return (
         model_path, None, None)

    def on_load_model_complete(self, model, user_data):
        model.world_position = self.cover_pos
        model.rotation_matrix = self.cover_rot_mat
        model.scale = self.cover_scale

    def on_crystal_stage_change(self, new_stage):
        self.crystal_stage = new_stage
        self.init_crystal_cover_data_with_stage()
        if self.model:
            self.model.world_position = self.cover_pos
            self.model.rotation_matrix = self.cover_rot_mat
            self.model.scale = self.cover_scale
            self.send_event('CRYSTAL_STAGE_CHANGE_FOR_COL', new_stage)

    def try_bind_crystal_mark_widget(self, model):
        ui = global_data.ui_mgr.get_ui('CrystalMarkUI')
        if not ui:
            return
        mark_widget = ui.get_mark_widget(self.faction_id)
        if not mark_widget or mark_widget.is_bind:
            return
        mark_widget.try_bind_model(model)