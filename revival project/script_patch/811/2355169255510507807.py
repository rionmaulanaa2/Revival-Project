# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/LocalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from mobile.common.EntityManager import Dynamic
from logic.gutils.EntityPool import EntityPool
from mobile.common.IdManager import IdManager
from mobile.common.EntityManager import EntityManager
from data.newbie_stage_config import GetBarrierConfig, GetDoorConfig, GetViewRangeConfig
from logic.gutils import scene_utils
import world
import math3d
from logic.gcommon.const import NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE
from common.cfg import confmgr

@Dynamic
class LocalBattle(Battle):
    TICK_INTERVAL = 1
    BARRIER_CHECK_ERROR = 6

    def __init__(self, entityid):
        super(LocalBattle, self).__init__(entityid)
        self._mecha_charger = None
        self._tick_total = 0
        self.barriers_col_model = None
        self.barrier_sfx_main = None
        self.barrier_sfx_main_id = None
        self.barrier_min_x = None
        self.barrier_max_x = None
        self.barrier_min_z = None
        self.barrier_max_z = None
        self.area_id = 1
        return

    def init_from_dict(self, bdict):
        self.init_from_dict_base(bdict)
        self.init_event(True)

    def destroy(self, clear_cache=True):
        self.init_event(False)
        self.clear_barriers()
        super(LocalBattle, self).destroy()

    def load_finish(self):
        scene = self.get_scene()
        view_range = GetViewRangeConfig().get(self.battle_tid, {}).get('view_range', 500)
        scene.scene_data.update({'view_range': view_range})
        scene.modify_view_range(view_range)
        self.play_localbattle_bgm()
        self.create_barriers()
        super(LocalBattle, self).load_finish()

    def init_battle_scene(self, scene_data):
        self.load_scene(scene_data)

    def init_event(self, bind=False):
        if bind:
            global_data.emgr.camera_lctarget_open_prez += self.on_open_prez
        else:
            global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez

    def tick(self, dt):
        super(LocalBattle, self).tick(dt)
        self._tick_total += dt
        if self._tick_total < LocalBattle.TICK_INTERVAL:
            return
        self._tick_total -= LocalBattle.TICK_INTERVAL
        self.mecha_charger_check()

    def record_mecha_charger(self, charger_id):
        self._mecha_charger = charger_id

    def mecha_charger_check(self):
        if self._mecha_charger is None:
            return
        else:
            charger = EntityManager.getentity(self._mecha_charger)
            if not (charger and charger.logic):
                return
            charger.logic.send_event('E_LBS_CHARGER_CHECK')
            return

    def play_localbattle_bgm(self):
        if self.battle_tid == NEWBIE_STAGE_HUMAN_BATTLE:
            global_data.sound_mgr.play_music('Custom1')
        elif self.battle_tid == NEWBIE_STAGE_MECHA_BATTLE:
            global_data.sound_mgr.play_music('Custom2')

    def create_barriers(self):
        barrier_conf = GetBarrierConfig().get(int(self.battle_tid), {})
        if not barrier_conf:
            return
        barrier_min_x, _, barrier_min_z = barrier_conf['barrier_left_bottom']
        barrier_max_x, _, barrier_max_z = barrier_conf['barrier_right_top']
        barrier_height = barrier_conf['barrier_height']
        barrier_center_x, barrier_center_z = (barrier_min_x + barrier_max_x) * 0.5, (barrier_min_z + barrier_max_z) * 0.5
        self.barriers_col_model = scene_utils.add_region_scene_collision_box((barrier_center_x, barrier_height, barrier_center_z), (barrier_max_x - barrier_min_x) * 0.5, (barrier_max_z - barrier_min_z) * 0.5)
        self.set_barrier_range(barrier_min_x, barrier_max_x, barrier_min_z, barrier_max_z)
        barrier_center = math3d.vector(barrier_center_x, barrier_height, barrier_center_z)
        self.create_barrier_sfx(barrier_min_x, barrier_min_z, barrier_max_x, barrier_max_z, barrier_center)

    def create_barrier_sfx(self, min_x, min_z, max_x, max_z, center):

        def on_create_func(model):
            scale_x = (max_x - min_x) / (model.bounding_box.x * 2)
            scale_y = 4.0
            scale_z = (max_z - min_z) / (model.bounding_box.z * 2)
            model.world_scale = math3d.vector(scale_x, scale_y, scale_z)
            self.barrier_sfx_main = model
            self.barrier_sfx_main_id = None
            self.barrier_sfx_main.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
            return

        barrier_model_path = confmgr.get('script_gim_ref')['region_range_blue']
        self.barrier_sfx_main_id = global_data.model_mgr.create_model_in_scene(barrier_model_path, center, on_create_func=on_create_func)

    def on_open_prez(self, enable):
        if self.barrier_sfx_main:
            if enable:
                self.barrier_sfx_main.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self.barrier_sfx_main.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self.barrier_sfx_main.all_materials.rebuild_tech()

    def clear_barriers(self):
        if self.barriers_col_model:
            global_data.model_mgr.remove_model_by_id(self.barriers_col_model)
        self.barriers_col_model = None
        if self.barrier_sfx_main_id:
            global_data.model_mgr.remove_model_by_id(self.barrier_sfx_main_id)
            self.barrier_sfx_main_id = None
        if self.barrier_sfx_main:
            global_data.model_mgr.remove_model(self.barrier_sfx_main)
            self.barrier_sfx_main = None
        return

    def get_barrier_range(self):
        return (
         self.barrier_min_x, self.barrier_max_x, self.barrier_min_z, self.barrier_max_z)

    def set_barrier_range(self, min_x, max_x, min_z, max_z):
        self.barrier_min_x = min_x + self.BARRIER_CHECK_ERROR
        self.barrier_max_x = max_x - self.BARRIER_CHECK_ERROR
        self.barrier_min_z = min_z + self.BARRIER_CHECK_ERROR
        self.barrier_max_z = max_z - self.BARRIER_CHECK_ERROR

    def get_settle_point(self):
        return None

    def set_combat_weapons(self, weapon_dict):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            global_data.player.logic.send_event('E_GUIDE_INIT_WEAPONS', None, weapon_dict)
            return