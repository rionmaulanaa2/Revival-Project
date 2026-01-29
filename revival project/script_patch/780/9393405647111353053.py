# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoneyBoxAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
from logic.gutils.judge_utils import get_player_group_id
from logic.gcommon.common_const.battle_const import ADCRYSTAL_TIP_SEC_STAGE_ATK, ADCRYSTAL_TIP_SEC_STAGE_DEF, MAIN_NODE_COMMON_INFO, ADCRYSTAL_TIP_POS_CHANGE_ATK, ADCRYSTAL_TIP_POS_CHANGE_DEF
from logic.gcommon.common_utils.local_text import get_text_by_id

class ComMoneyboxAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CRYSTAL_LOW_HP': 'on_crystal_low_hp',
       'E_PLAYER_AROUND_CRYSTAL_CHANGE': 'on_player_around_crystal_change',
       'CRYSTAL_STAGE_CHANGE': 'on_crystal_stage_change'
       })

    def __init__(self):
        super(ComMoneyboxAppearance, self).__init__()
        self.faction_id = None
        self.npc_id = None
        self.crystal_data = None
        self.crystal_pos = None
        self.crystal_rot_mat = None
        self.crystal_scale = None
        self.valid_attack_dis = None
        self.guide_sfx_id = None
        self.damage_sfx_id = None
        self.crystal_stage = None
        self.route_sfx_list = []
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoneyboxAppearance, self).init_from_dict(unit_obj, bdict)
        self.faction_id = bdict.get('faction_id')
        self.npc_id = bdict.get('npc_id')
        self.crystal_stage = bdict.get('crystal_stage')
        self.init_crystal_data()

    def init_crystal_data(self):
        all_crystal = global_data.game_mode.get_cfg_data('moneybox_data')
        self.crystal_data = all_crystal.get(str(self.npc_id))
        scale = self.crystal_data.get('scale')
        self.crystal_scale = math3d.vector(*scale)
        if self.crystal_stage is None:
            self.init_crystal_data_without_stage()
        else:
            self.init_crystal_data_with_stage()
        return

    def init_crystal_data_without_stage(self):
        pos = self.crystal_data.get('pos')
        self.crystal_pos = math3d.vector(pos[0], pos[1], pos[2])
        rot = self.crystal_data.get('rot')
        self.crystal_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))

    def init_crystal_data_with_stage(self):
        pos_list = self.crystal_data.get('pos')
        pos = pos_list[self.crystal_stage]
        self.crystal_pos = math3d.vector(pos[0], pos[1], pos[2])
        rot_list = self.crystal_data.get('rot')
        rot = rot_list[self.crystal_stage]
        self.crystal_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))

    def get_model_info(self, unit_obj, bdict):
        all_model_path = self.crystal_data.get('model_path')
        if type(all_model_path) in (list, tuple) and len(all_model_path) > 1:
            model_path = all_model_path[0] if self.is_teammate() else all_model_path[1]
        else:
            model_path = 'model_new/items/items/crystall_blue.gim'
        return (
         model_path, None, None)

    def on_load_model_complete(self, model, user_data):
        model.world_position = self.crystal_pos
        model.rotation_matrix = self.crystal_rot_mat
        model.scale = self.crystal_scale
        self.create_guide_sfx()
        if self.crystal_stage is None:
            self.try_create_crystal_mark_widget(model)
        if not self.is_teammate():
            self.create_route_sfx()
        return

    def destroy(self):
        self.create_die_sfx()
        super(ComMoneyboxAppearance, self).destroy()
        self.remove_guide_sfx()
        self.remove_damage_sfx()
        self.remove_route_sfx()

    def on_crystal_stage_change(self, new_stage):
        self.crystal_stage = new_stage
        self.init_crystal_data_with_stage()
        self.model.world_position = self.crystal_pos
        self.model.rotation_matrix = self.crystal_rot_mat
        self.model.scale = self.crystal_scale
        self.send_event('CRYSTAL_STAGE_CHANGE_FOR_COL', new_stage)
        guide_sfx = global_data.sfx_mgr.get_sfx_by_id(self.guide_sfx_id)
        if guide_sfx:
            guide_sfx.position = math3d.vector(self.crystal_pos.x, self.crystal_pos.y, self.crystal_pos.z)
        if not self.is_teammate():
            self.remove_route_sfx()
            self.create_route_sfx()

    def on_crystal_low_hp(self, *args):
        if self.damage_sfx_id:
            return
        self.create_damage_sfx()

    def on_player_around_crystal_change(self, player_cnt):
        if self.crystal_stage is None:
            global_data.emgr.player_around_crystal_change_event.emit(self.faction_id, player_cnt)
        return

    def is_teammate(self):
        return get_player_group_id() == self.faction_id

    def create_guide_sfx(self):
        all_sfx_path = self.crystal_data.get('guide_sfx_path')
        sfx_scale = self.crystal_data.get('guide_sfx_scale')
        if type(all_sfx_path) in (list, tuple) and len(all_sfx_path) > 1:
            sfx_path = all_sfx_path[0] if self.is_teammate() else all_sfx_path[1]
        else:
            sfx_path = 'effect/fx/scenes/common/zhanqi/zq_guangzhu_blue_1.sfx'
        up_offset = 0
        guide_sfx_pos = math3d.vector(self.crystal_pos.x, self.crystal_pos.y + up_offset, self.crystal_pos.z)
        sfx_scale = math3d.vector(*sfx_scale)

        def create_cb(sfx):
            sfx.scale = sfx_scale

        self.guide_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, guide_sfx_pos, on_create_func=create_cb)

    def remove_guide_sfx(self):
        if self.guide_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.guide_sfx_id)

    def create_damage_sfx(self):
        sfx_path = 'effect/fx/robot/common/mecha_sunhuai.sfx'
        up_offset = 30
        damage_sfx_pos = math3d.vector(self.crystal_pos.x, self.crystal_pos.y + up_offset, self.crystal_pos.z)
        self.damage_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, damage_sfx_pos)

    def remove_damage_sfx(self):
        if self.damage_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.damage_sfx_id)

    def create_die_sfx(self):
        sfx_path = 'effect/fx/robot/robot_qishi/qishi_die.sfx'
        up_offset = 0
        die_sfx_pos = math3d.vector(self.crystal_pos.x, self.crystal_pos.y + up_offset, self.crystal_pos.z)
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, die_sfx_pos)

    def create_route_sfx(self):
        if self.crystal_stage is None:
            sfx_list = self.crystal_data.get('route_sfxs', [])
        else:
            sfx_list = self.crystal_data.get('route_sfxs', [])
            sfx_list = sfx_list[self.crystal_stage]
        scene_sfx_data = global_data.game_mode.get_cfg_data('scene_sfx_data')
        for sfx_id in sfx_list:
            sfx_data = scene_sfx_data.get(str(sfx_id))
            if not sfx_data:
                continue
            sfx_path = sfx_data.get('sfx_path')
            x, y, z = sfx_data.get('pos')
            position = math3d.vector(x, y, z)

            def create_cb(sfx, data=sfx_data):
                ex, ey, ez = data.get('end_pos')
                sfx.end_pos = math3d.vector(ex, ey, ez)

            sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, position, on_create_func=create_cb)
            sfx_id and self.route_sfx_list.append(sfx_id)

        return

    def remove_route_sfx(self):
        for sfx_id in self.route_sfx_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.route_sfx_list = []

    def try_create_crystal_mark_widget(self, model):
        ui = global_data.ui_mgr.show_ui('CrystalMarkUI', 'logic.comsys.battle.Crystal')
        if not ui:
            return
        if not self.unit_obj or not self.unit_obj.is_valid():
            return
        ui.add_mark_widget(self.faction_id, self.unit_obj.id, model)