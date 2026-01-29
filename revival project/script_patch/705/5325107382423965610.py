# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Sys3DAirLineMgr.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
import world
import math3d
import logic.gutils.map_3d_utils as mutil
from logic.gcommon.common_utils import parachute_utils
import weakref
import common.utils.timer as timer
import time
AIRLINE_ID = 0
AIRLINE_PREVIEW_LINE1_ID = 1
AIRLINE_PREVIEW_LINE2_ID = 2
AIRLINE_PREVIEW_WARNING_LINE1_ID = 3
AIRLINE_PREVIEW_WARNING_LINE2_ID = 4
AIRLINE_RES = 'effect/fx/scenes/common/map/map_xian_01.sfx'
AIRLINE_JIANTOU_RES = 'effect/fx/scenes/common/map/map_xian_end.sfx'
PREVIEW_LINE_RES = 'effect/fx/scenes/common/map/map_xian_02.sfx'
PREVIEW_LINE_RES_WARNING = 'effect/fx/scenes/common/map/map_xian_02_01.sfx'

class Sys3DAirLineMgr(ScenePartSysBase):

    def __init__(self):
        super(Sys3DAirLineMgr, self).__init__()
        self.gui_map_model_ref = None
        self.airline_jiantou = None
        self.warning_timer = None
        self.is_first = True
        self.update_timer_id = None
        self.is_show_airline_ani = False
        self.is_reconnect = False
        self.airline_map = {}
        self.init_events()
        return

    def init_events(self):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.map_model_transformation_changed_event += self.reset_airlines
        global_data.emgr.map_3d_model_loaded_event += self.map_model_loaded
        global_data.emgr.draw_preview_line_event += self.draw_preview_lines
        global_data.emgr.draw_airline_event += self.draw_airline
        global_data.emgr.click_3dmap_pos_valid_event += self.check_click_pos_valid
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        global_data.emgr.show_airline_ani_event += self.show_airline_ani
        global_data.emgr.on_battle_status_changed += self.on_battle_status_changed

    def on_login_reconnect(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        self.is_reconnect = True
        return

    def map_model_loaded(self, model):
        self.gui_map_model_ref = weakref.ref(model)

    def show_airline_ani(self):
        if not self.is_first:
            return
        self.is_first = False
        battle = global_data.battle
        flight_dict = battle.flight_dict
        if not flight_dict:
            return
        st_pos = math3d.vector(*flight_dict['start_pos'])
        end_pos = math3d.vector(*flight_dict['end_pos'])
        self.draw_airline(st_pos, st_pos + (end_pos - st_pos) * 0.05)
        self.start_time = time.time()

        def update_airline_ani(*args):
            flight_dict = global_data.battle.flight_dict
            if not flight_dict:
                return
            if not self.start_time:
                return
            start_pos = flight_dict['start_pos']
            end_pos = flight_dict['end_pos']
            now = time.time()
            percent = (now - self.start_time) / 2.0
            percent = 1 if percent >= 1 else percent
            if AIRLINE_ID in self.airline_map:
                v3d_end_pos = math3d.vector(*end_pos)
                v3d_start_pos = math3d.vector(*start_pos)
                target_pos = v3d_start_pos + (v3d_end_pos - v3d_start_pos) * percent
                self.airline_map[AIRLINE_ID][2] = target_pos
                self.reset_airlines()
            if percent >= 1:
                return timer.RELEASE

        self.update_timer_id = global_data.game_mgr.register_logic_timer(update_airline_ani, interval=1, times=-1, mode=timer.LOGIC)

    def draw_airlines(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            flight_dict = battle.flight_dict
            if not flight_dict:
                return
            if self.update_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
                self.update_timer_id = None
            self.clear_airlines()
            self.add_airline(AIRLINE_ID, math3d.vector(*flight_dict['start_pos']), math3d.vector(*flight_dict['end_pos']))
            self.draw_jiantou(math3d.vector(*flight_dict['start_pos']), math3d.vector(*flight_dict['end_pos']))
            return

    def draw_preview_lines(self, tangent_points):
        if not global_data.enable_parachute_range_circle:
            return
        s1, e1, s2, e2 = tangent_points
        self.add_airline(AIRLINE_PREVIEW_LINE1_ID, s1, e1, PREVIEW_LINE_RES)
        self.add_airline(AIRLINE_PREVIEW_LINE2_ID, s2, e2, PREVIEW_LINE_RES)
        self.add_airline(AIRLINE_PREVIEW_WARNING_LINE1_ID, s1, e1, PREVIEW_LINE_RES_WARNING)
        self.add_airline(AIRLINE_PREVIEW_WARNING_LINE2_ID, s2, e2, PREVIEW_LINE_RES_WARNING)
        if AIRLINE_PREVIEW_WARNING_LINE1_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_WARNING_LINE1_ID][0].visible = False
        if AIRLINE_PREVIEW_WARNING_LINE2_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_WARNING_LINE2_ID][0].visible = False

    def draw_airline(self, st_pos, end_pos):
        self.add_airline(AIRLINE_ID, st_pos, end_pos)
        self.draw_jiantou(st_pos, end_pos)
        global_data.emgr.show_3dmap_poison_circle_event.emit()

    def draw_jiantou(self, st_pos, end_pos):
        if self.airline_jiantou:
            return
        else:
            map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
            if not map_rt:
                print('map_rt is None in [Sys3DAirLineMgr]')
                return
            final_world_mat = mutil.FINAL_WORLD_MAT
            gui_map_model = self.gui_map_model_ref() if self.gui_map_model_ref else None
            if gui_map_model and gui_map_model.valid:
                final_world_mat = gui_map_model.world_transformation
            airline_forward = end_pos - st_pos
            if airline_forward.is_zero:
                return
            yaw = airline_forward.yaw
            sfx = world.sfx(AIRLINE_JIANTOU_RES)
            self.airline_jiantou = sfx
            end_pos = mutil.trans_world_pos_to_3dmap_pos(end_pos)
            end_pos = end_pos * final_world_mat
            map_rt.add_sfx(sfx, pos=end_pos, rotation_matrix=mutil.END_ROT_MAT)
            local_mat = math3d.matrix.make_rotation_y(yaw)
            sfx.world_rotation_matrix = local_mat * final_world_mat.rotation
            return

    def add_airline(self, al_id, start_pos, end_pos, sfx_path=None):
        if not sfx_path:
            sfx_path = AIRLINE_RES if 1 else sfx_path
            map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
            map_rt or print('map_rt is None in [Sys3DAirLineMgr]')
            return
        else:
            final_world_mat = mutil.FINAL_WORLD_MAT
            gui_map_model = self.gui_map_model_ref() if self.gui_map_model_ref else None
            if gui_map_model and gui_map_model.valid:
                final_world_mat = gui_map_model.world_transformation
            if al_id in self.airline_map:
                airline_obj, sp, ep = self.airline_map[al_id]
                if airline_obj and airline_obj.valid:
                    airline_obj.destroy()
                    del self.airline_map[al_id]
            sfx = world.sfx(sfx_path)
            if hasattr(sfx, 'enable_lod'):
                sfx.enable_lod = False
            self.airline_map[al_id] = [sfx, start_pos, end_pos]
            st_pos = mutil.trans_world_pos_to_3dmap_pos(start_pos)
            end_pos = mutil.trans_world_pos_to_3dmap_pos(end_pos)
            st_pos = st_pos * final_world_mat
            end_pos = end_pos * final_world_mat
            map_rt.add_sfx(sfx, pos=st_pos, rotation_matrix=mutil.END_ROT_MAT)
            sfx.end_pos = end_pos
            return

    def reset_airlines(self):
        gui_map_model = self.gui_map_model_ref() if self.gui_map_model_ref else None
        if gui_map_model and gui_map_model.valid:
            mat = gui_map_model.world_transformation
            for al_obj, st_pos, end_pos in six.itervalues(self.airline_map):
                st_pos = mutil.trans_world_pos_to_3dmap_pos(st_pos)
                end_pos = mutil.trans_world_pos_to_3dmap_pos(end_pos)
                st_pos = st_pos * mat
                end_pos = end_pos * mat
                al_obj.world_position = st_pos
                al_obj.end_pos = end_pos

            if self.airline_jiantou and self.airline_jiantou.valid:
                if AIRLINE_ID in self.airline_map:
                    _, st_pos, end_pos = self.airline_map[AIRLINE_ID]
                    forward = end_pos - st_pos
                    forward.normalize()
                    end_pos = mutil.trans_world_pos_to_3dmap_pos(end_pos)
                    end_pos = end_pos * mat
                    self.airline_jiantou.world_position = end_pos
                    local_mat = math3d.matrix.make_rotation_y(forward.yaw)
                    self.airline_jiantou.world_rotation_matrix = local_mat * mat.rotation
        return

    def del_airline(self, al_id):
        if al_id not in self.airline_map:
            return
        airline_obj, start_pos, end_pos = self.airline_map[al_id]
        if airline_obj and airline_obj.valid:
            airline_obj.destroy()
        del self.airline_map[al_id]

    def clear_airlines(self):
        for al_info in six.itervalues(self.airline_map):
            al_obj = al_info[0]
            if al_obj and al_obj.valid:
                al_obj.destroy()

        self.airline_map.clear()
        if self.airline_jiantou and self.airline_jiantou.valid:
            self.airline_jiantou.destroy()
            self.airline_jiantou = None
        return

    def check_click_pos_valid(self, is_valid):
        if not global_data.enable_parachute_range_circle:
            return
        if not is_valid:
            if self.warning_timer:
                return

            def warning_end_callback(*args):
                self.show_airline_warning(False)
                self.warning_timer = None
                return

            self.show_airline_warning(True)
            self.warning_timer = global_data.game_mgr.register_logic_timer(warning_end_callback, 0.3, times=1, mode=timer.CLOCK)

    def show_airline_warning(self, is_warning):
        if AIRLINE_PREVIEW_LINE1_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_LINE1_ID][0].visible = not is_warning
        if AIRLINE_PREVIEW_LINE2_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_LINE2_ID][0].visible = not is_warning
        if AIRLINE_PREVIEW_WARNING_LINE1_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_WARNING_LINE1_ID][0].visible = is_warning
        if AIRLINE_PREVIEW_WARNING_LINE2_ID in self.airline_map:
            self.airline_map[AIRLINE_PREVIEW_WARNING_LINE2_ID][0].visible = is_warning

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if stage == parachute_utils.STAGE_PLANE:
            self.draw_airlines()
        else:
            self.clear_airlines()

    def on_battle_status_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if self.is_reconnect:
            self.is_reconnect = False
            if stage == parachute_utils.STAGE_MECHA_READY:
                self.draw_airlines()

    def destroy(self):
        self.clear_airlines()
        if self.warning_timer:
            global_data.game_mgr.unregister_logic_timer(self.warning_timer)
            self.warning_timer = None
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        return