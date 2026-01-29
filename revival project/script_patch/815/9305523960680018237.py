# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NewbieFourLocalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from mobile.common.EntityManager import Dynamic
from data.newbie_stage_config import GetBarrierConfig, GetViewRangeConfig
from logic.gutils import scene_utils
import world
import math3d
from logic.gcommon.common_const import collision_const
from common.cfg import confmgr
BARRIER_MODEL_RADIUS = 100

@Dynamic
class NewbieFourLocalBattle(Battle):

    def __init__(self, entityid):
        super(NewbieFourLocalBattle, self).__init__(entityid)
        self.barrier_model = None
        self.barrier_center = None
        self.barrier_radius = None
        self.area_id = None
        return

    def init_from_dict(self, bdict):
        self.init_from_dict_base(bdict)
        self.init_event(True)

    def init_event(self, bind=False):
        if bind:
            global_data.emgr.camera_lctarget_open_prez += self.on_open_prez
        else:
            global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez

    def load_finish(self):
        scene = self.get_scene()
        view_range = GetViewRangeConfig().get(self.battle_tid, {}).get('view_range', 500)
        scene.scene_data.update({'view_range': view_range})
        scene.modify_view_range(view_range)
        global_data.sound_mgr.play_music('Custom4')
        self.create_barriers()
        super(NewbieFourLocalBattle, self).load_finish()

    def destroy(self, clear_cache=True):
        self.remove_barriers()
        super(NewbieFourLocalBattle, self).destroy()

    def init_battle_scene(self, scene_data):
        from logic.gcommon.common_utils import parachute_utils
        parachute_stage = self._save_init_bdict.get('parachute_stage', None)
        preload_cockpit = parachute_utils.is_flying(parachute_stage)
        scene_data.update({'preload_cockpit': preload_cockpit})
        self.load_scene(scene_data)
        return

    def create_barriers(self):
        global_data.emgr.camera_lctarget_open_prez += self.on_open_prez

        def create_cb(model, *args):
            if model and model.valid:
                model.visible = True
                model.set_col_group_mask(collision_const.REGION_BOUNDARY_SCENE_GROUP, collision_const.REGION_BOUNDARY_SCENE_MASK)
                model.active_collision = True
                model.scale = math3d.vector(*barrier_scale)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                self.barrier_model = model

        barrier_conf = GetBarrierConfig().get(int(self.battle_tid), {})
        barrier_center = barrier_conf.get('barrier_center', [4641, 290, -130])
        barrier_scale = barrier_conf.get('barrier_scale', [10, 10, 10])
        self.barrier_radius = barrier_scale[0] * BARRIER_MODEL_RADIUS
        center_vec = math3d.vector(*barrier_center)
        self.barrier_center = center_vec
        barrier_model_path = confmgr.get('script_gim_ref')['manyue_region_range']
        global_data.model_mgr.create_model_in_scene(barrier_model_path, pos=center_vec, on_create_func=create_cb)

    def remove_barriers(self):
        if self.barrier_model:
            global_data.model_mgr.remove_model(self.barrier_model)
            global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez
            self.barrier_model = None
        return

    def on_open_prez(self, enable):
        if self.barrier_model and self.barrier_model.valid:
            if enable:
                self.barrier_model.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self.barrier_model.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self.barrier_model.all_materials.rebuild_tech()

    def get_barrier_range(self):
        return (
         self.barrier_center, self.barrier_radius)