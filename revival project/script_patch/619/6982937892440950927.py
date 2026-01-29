# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Sys3DParachuteRangeMgr.py
from __future__ import absolute_import
from __future__ import print_function
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
import world
import math3d
import logic.gutils.map_3d_utils as mutil
from logic.gcommon.common_utils import parachute_utils
from logic.gutils import map_utils
import common.utils.timer as timer
POISON_CIRCLE_RANGE_RES = 'effect/fx/scenes/common/biaozhi/3dmap_circle_duquan.sfx'
AIRLINE_PARACHUTE_RANGE_RES = 'effect/fx/scenes/common/biaozhi/3dmap_circle.sfx'
AIRLINE_PARACHUTE_RANGE_RES_KUOSAN = 'effect/fx/scenes/common/biaozhi/3dmap_circle_kuosan.sfx'
RANGE_RADIUS = 39
MAP_SIZE = 520

class Sys3DParachuteRangeMgr(ScenePartSysBase):

    def __init__(self):
        super(Sys3DParachuteRangeMgr, self).__init__()
        self._poison_circle_obj = None
        self._parachute_range_obj = None
        self._parachute_range_kuosan_obj = None
        self._gui_map_model_ref = None
        self.init_map_radius = float(RANGE_RADIUS) / MAP_SIZE * map_utils.get_map_dist()
        self.init_parachute_range()
        self.init_events()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)
        self.guide_timer = None
        self.poison_point = None
        return

    def init_events(self):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        global_data.emgr.map_3d_model_loaded_event += self.map_model_loaded
        global_data.emgr.map_model_transformation_changed_event += self.model_transform_changed
        global_data.emgr.click_3dmap_pos_valid_event += self.check_click_pos_valid
        global_data.emgr.show_parachture_range_guide_event += self.show_parachute_range_guide
        global_data.emgr.show_3dmap_poison_circle_event += self.show_poison_circle

    def show_poison_circle(self):
        if not global_data.enable_parachute_range_circle:
            return
        else:
            if self._poison_circle_obj:
                return
            battle = global_data.battle
            if not battle:
                return
            map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
            if not map_rt:
                print('map_rt is None in [Sys3DParachuteRangeMgr]')
                return
            final_mat = mutil.FINAL_WORLD_MAT
            map_model = self._gui_map_model_ref() if self._gui_map_model_ref else None
            if map_model and map_model.valid:
                final_mat = map_model.world_transformation
            if battle.poison_circle and 'poison_point' in battle.poison_circle:
                sfx = world.sfx(POISON_CIRCLE_RANGE_RES)
                map_rt.add_sfx(sfx)
                x, z, poison_range = battle.poison_circle.get('poison_point')
                poison_pos = math3d.vector(x, 0, z)
                poison_map_pos = mutil.trans_world_pos_to_3dmap_pos(poison_pos) * final_mat
                sfx.position = poison_map_pos
                scale = float(poison_range) / self.init_map_radius
                sfx.scale = math3d.vector(scale, scale, scale)
                sfx.rotation_matrix = final_mat
                self._poison_circle_obj = sfx
            return

    def init_parachute_range(self):
        if not global_data.enable_parachute_range_circle:
            return
        map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
        if not map_rt:
            print('map_rt is None in [Sys3DParachuteRangeMgr]')
            return
        sfx = world.sfx(AIRLINE_PARACHUTE_RANGE_RES)
        map_rt.add_sfx(sfx, pos=math3d.vector(0, 0, 0), rotation_matrix=mutil.END_ROT_MAT)
        sfx.visible = False
        self._parachute_range_obj = sfx
        sfx2 = world.sfx(AIRLINE_PARACHUTE_RANGE_RES_KUOSAN)
        map_rt.add_sfx(sfx2, pos=math3d.vector(0, 0, 0), rotation_matrix=mutil.END_ROT_MAT)
        sfx2.visible = False
        self._parachute_range_kuosan_obj = sfx2

    def show_parachute_range_guide(self):
        if not global_data.enable_parachute_range_circle:
            return
        sfx = self._parachute_range_kuosan_obj
        if sfx and sfx.valid:
            if not self.guide_timer:
                self.guide_timer = global_data.game_mgr.register_logic_timer(self.parachute_range_guide_callback, interval=sfx.life_span, times=-1, mode=timer.CLOCK)

    def parachute_range_guide_callback(self):
        if not global_data.enable_parachute_range_circle:
            return
        sfx = self._parachute_range_kuosan_obj
        if sfx and sfx.valid:
            sfx.visible = True
            sfx.restart()

    def map_model_loaded(self, model):
        import weakref
        self._gui_map_model_ref = weakref.ref(model)

    def on_login_reconnect(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        if self.guide_timer:
            global_data.game_mgr.unregister_logic_timer(self.guide_timer)
            self.guide_timer = None
            sfx = self._parachute_range_kuosan_obj
            if sfx and sfx.valid:
                self.guide_timer = global_data.game_mgr.register_logic_timer(self.parachute_range_guide_callback, interval=sfx.life_span, times=-1, mode=timer.CLOCK)
        return

    def update(self):
        if not global_data.enable_parachute_range_circle:
            return
        if not self._parachute_range_obj or not self._parachute_range_obj.valid:
            return
        self._parachute_range_obj.visible = self.on_update()

    def on_update(self):
        if not global_data.enable_parachute_range_circle:
            return
        else:
            battle = global_data.battle
            if not battle:
                return False
            plane = battle.get_entity(battle.plane_id)
            if not (plane and plane.logic):
                return False
            plane = plane.logic
            pos = plane.ev_g_position()
            if not pos:
                return False
            airline_start_pos = plane.ev_g_airline_start_pos()
            final_mat = mutil.FINAL_WORLD_MAT
            map_model = self._gui_map_model_ref() if self._gui_map_model_ref else None
            if map_model and map_model.valid:
                final_mat = map_model.world_transformation
            map_pos = mutil.trans_world_pos_to_3dmap_pos(pos) * final_mat
            self._parachute_range_obj.position = map_pos
            self._parachute_range_kuosan_obj.position = map_pos
            cnt_radius = plane.ev_g_cnt_plane_radius()
            scale = float(cnt_radius) / self.init_map_radius
            self._parachute_range_obj.scale = math3d.vector(scale, scale, scale)
            self._parachute_range_kuosan_obj.scale = math3d.vector(scale, scale, scale)
            return True

    def reset_3d_parachute_range(self):
        if not global_data.enable_parachute_range_circle:
            return
        else:
            if self._parachute_range_obj and self._parachute_range_obj.valid:
                self._parachute_range_obj.destroy()
                self._parachute_range_obj = None
            if self._parachute_range_kuosan_obj and self._parachute_range_kuosan_obj.valid:
                self._parachute_range_kuosan_obj.destroy()
                self._parachute_range_kuosan_obj = None
            if self._poison_circle_obj and self._poison_circle_obj.valid:
                self._poison_circle_obj.destroy()
                self._poison_circle_obj = None
            if self.update_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
                self.update_timer_id = None
            if self.guide_timer:
                global_data.game_mgr.unregister_logic_timer(self.guide_timer)
                self.guide_timer = None
            return

    def model_transform_changed(self):
        if not global_data.enable_parachute_range_circle:
            return
        else:
            m = self._gui_map_model_ref() if self._gui_map_model_ref else None
            if self._parachute_range_obj and self._parachute_range_obj.valid:
                self._parachute_range_obj.rotation_matrix = m.world_rotation_matrix
            if self._parachute_range_kuosan_obj and self._parachute_range_kuosan_obj.valid:
                self._parachute_range_kuosan_obj.rotation_matrix = m.world_rotation_matrix
            self.refresh_poison_circle_obj()
            return

    def refresh_poison_circle_obj(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            if not battle.poison_circle:
                poison_point = self.poison_point
            else:
                poison_point = battle.poison_circle.get('poison_point')
            if not poison_point:
                return
            if self._gui_map_model_ref:
                map_model = self._gui_map_model_ref() if 1 else None
                return map_model and map_model.valid or None
            final_mat = map_model.world_transformation
            if self._poison_circle_obj and self._poison_circle_obj.valid:
                self.poison_point = poison_point
                x, z, poison_range = poison_point
                poison_pos = math3d.vector(x, 0, z)
                poison_map_pos = mutil.trans_world_pos_to_3dmap_pos(poison_pos) * final_mat
                self._poison_circle_obj.position = poison_map_pos
                scale = float(poison_range) / self.init_map_radius
                self._poison_circle_obj.scale = math3d.vector(scale, scale, scale)
                self._poison_circle_obj.rotation_matrix = map_model.world_rotation_matrix
            return

    def check_click_pos_valid(self, is_valid):
        if not global_data.enable_parachute_range_circle:
            return
        if not is_valid and not self.guide_timer:
            obj = self._parachute_range_kuosan_obj
            if obj and obj.valid:
                obj.visible = True
                obj.restart()

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if stage not in (parachute_utils.STAGE_PLANE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_NONE):
            self.reset_3d_parachute_range()
        elif not self.update_timer_id:
            self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)

    def destroy(self):
        self.reset_3d_parachute_range()