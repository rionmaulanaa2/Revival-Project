# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/Part3DMap.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import math3d
import game3d
import world
import math
import render
import cc
import collision
import time
from common.cfg import confmgr
from common.uisys.render_target import RenderTargetHolder, RenderTarget
from logic.gcommon.common_utils import parachute_utils
import logic.gutils.map_3d_utils as mutil
import weakref
from common.utils import timer
_HASH_TEX = game3d.calc_string_hash('Tex0')
_HASH_RT_OR_COLOR = game3d.calc_string_hash('rt_or_color')
_HASH_BASE_COLOR = game3d.calc_string_hash('Base_Color')
_HASH_ALPHAMTL = game3d.calc_string_hash('AlphaMtl')
_HASH_Y_Flip = game3d.calc_string_hash('Y_Flip')
GUI_MAP_RES = 'scene/xuanjue/xuanjue_06_content/gui_map.gim'
MAP_START_SFX02 = 'effect/fx/scenes/common/map/start_02.sfx'
MAP_END_SFX = 'effect/fx/scenes/common/map/map_end.sfx'
AIRLINE_RES = 'effect/fx/scenes/common/map/map_xian_01.sfx'
PARACHUTE_RANGE_RES = 'effect/fx/scenes/common/biaozhi/3dmap_circle.sfx'
from common.uisys.font_utils import GetMultiLangFontFaceName
MAP_RT_CONF = {'scn_bg_color': 332855,
   'cam_fov': 60.0,
   'rt_width': 1757.0,
   'rt_height': 1024.0,
   'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
   'cam_pos': math3d.vector(0, 300, 0)
   }
COCKPIT_BOLI_WIDTH = 26.9
COCKPIT_BOLI_HEIGHT = 15.7

class Part3DMap(ScenePart.ScenePart):
    INIT_EVENT = {'on_player_parachute_stage_changed': 'on_player_parachute_stage_changed',
       'save_3d_map_event': 'save_render_target',
       'add_rt_tex_to_cockpit': 'set_render_target_to_model',
       'get_3d_map_rt_event': 'get_3d_map_rt',
       'choose_parachute_point_event': 'choose_parachute_point',
       'calc_map_cam_move_pos': 'calc_map_can_move_pos',
       'move_map_pos_event': 'move_map_pos',
       'scale_map_3d_event': 'scale_map_model',
       'rotate_map_3d_event': 'rotate_map_model'
       }

    def __init__(self, scene, name):
        super(Part3DMap, self).__init__(scene, name, need_update=True)
        self.gui_map_target = None
        self.gui_map_model = None
        self.gui_map_task = None
        self.gui_ani_timer = None
        self.stop_ani_timer = None
        self.is_playing_animation = False
        self.is_first = True
        self.is_operational = False
        self.cockipt_model_ref = None
        self.start_sfx_id = None
        self.has_play_start02 = False
        self.airline_map = {}
        return

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        prepare_timestamp = 0
        battle = global_data.battle
        if battle:
            prepare_timestamp = getattr(battle, 'prepare_timestamp', 0)
        m = {0: '\xe5\x88\x9d\xe5\xa7\x8b\xe7\x8a\xb6\xe6\x80\x81',
           1: '\xe7\x99\xbb\xe6\x9c\xba',
           2: '\xe8\x87\xaa\xe7\x94\xb1\xe8\x90\xbd\xe4\xbd\x93',
           3: '\xe6\x89\x93\xe5\xbc\x80\xe9\x99\x8d\xe8\x90\xbd\xe4\xbc\x9e',
           4: '\xe8\x90\xbd\xe5\x9c\xb0',
           5: '\xe9\xa3\x9e\xe8\xa1\x8c\xe8\xbd\xbd\xe5\x85\xb7',
           6: '\xe8\xb6\x85\xe7\xba\xa7\xe8\xb7\xb3',
           7: '\xe5\x8f\x91\xe5\xb0\x84\xe8\xa3\x85\xe5\xa4\x87\xe9\x98\xb6\xe6\xae\xb5',
           8: '\xe5\x87\xba\xe5\x87\xbb\xe9\x98\xb6\xe6\xae\xb5',
           9: '\xe9\xa2\x84\xe5\xa4\x87\xe5\x87\xba\xe5\x87\xbb\xe9\x98\xb6\xe6\xae\xb5',
           10: '\xe5\x87\xba\xe5\x87\xbb\xe9\x98\xb6\xe6\xae\xb5'
           }
        if stage == parachute_utils.STAGE_MECHA_READY:
            if self.is_first:
                self.is_first = False
                now = time.time()
                if prepare_timestamp - now > 4:
                    self.is_playing_animation = True
                    self.show_3d_map_with_animation()
                else:
                    self.show_3d_map_instant()
            else:
                self.show_3d_map_instant()
        elif stage == parachute_utils.STAGE_PLANE:
            global_data.emgr.set_3d_map_camera_event.emit(True)
            if not self.is_operational:
                self.is_operational = True
                self.show_3d_map_instant()
        elif stage in (parachute_utils.STAGE_LAUNCH_PREPARE, parachute_utils.STAGE_FREE_DROP):
            if stage == parachute_utils.STAGE_LAUNCH_PREPARE:
                global_data.emgr.show_screen_effect.emit('ScreenMapEnd', {})
            global_data.emgr.set_3d_map_camera_event.emit(False)
            self.reset_3d_map()
        elif stage == parachute_utils.STAGE_LAND:
            global_data.emgr.hide_screen_effect.emit('ScreenMapEnd')
            global_data.emgr.hide_screen_effect.emit('ScreenMapStart')
            self.reset_3d_map()
        elif stage != parachute_utils.STAGE_NONE:
            self.reset_3d_map()

    def on_enter(self):
        self.load_gui_map_model()
        self.init_render_target()
        self.add_sub_sys()

    def add_sub_sys(self):
        self.register_sub_sys('Sys3DAirLineMgr')
        self.register_sub_sys('Sys3DPlayerInfoMgr')
        self.register_sub_sys('Sys3DParachuteRangeMgr')
        self.register_sub_sys('Sys3DMapInfoMgr')
        player = global_data.player
        if player:
            cnt = player.get_total_cnt()
            if cnt <= 5:
                self.register_sub_sys('Sys3DGuide')

    def on_exit(self):
        super(Part3DMap, self).on_exit()
        self.reset_3d_map()

    def on_update(self, dt):
        pass

    def save_render_target(self):
        self.show_3d_map_with_animation()

    def init_render_target(self):
        if self.gui_map_target:
            self.gui_map_target.stop_render_target()
        self.gui_map_target = RenderTargetHolder(None, None, MAP_RT_CONF)
        self.gui_map_target.start_render_target()
        render.enable_dynamic_culling(False)
        return

    def get_3d_map_rt(self):
        return self.gui_map_target

    def load_gui_map_model(self):
        self.gui_map_task = world.create_model_async(GUI_MAP_RES, self.on_gui_map_loaded, None, game3d.ASYNC_HIGH)
        return

    def choose_parachute_point(self, x, y):
        if not self.is_operational:
            self.check_is_playing_animation()
            return None
        else:
            uv = self.trans_ui_pos_to_rt_uv(x, y)
            if not uv:
                return None
            scn_pos = self.trans_uv_to_rt_scene_pos(*uv)
            if not scn_pos:
                return None
            return mutil.trans_3dmap_pos_to_world_pos(scn_pos)

    def init_map_names(self):
        import render
        render.create_font('name_txt', GetMultiLangFontFaceName('FZLanTingHei'), 20, True)
        ui_empty = render.texture('gui/ui_res_2/battle/panel/pnl_item_empty.png')
        self.name_simui = world.simuiobject(ui_empty)
        name_simui_id = self.name_simui.add_text_ui('\xe5\x93\xbc\xe6\x80\xbb\xe6\x98\xaf\xe4\xb8\x8d\xe6\x98\xaf\xe8\xbf\x99\xe4\xb8\xaa\xe5\xad\x97\xe4\xbd\x93', 'name_txt', 0, 0)
        color = (255, 254, 255, 255)
        self.name_simui.set_ui_color(name_simui_id, color)
        self.name_simui.set_ui_align(name_simui_id, 0.5, 0.5)
        self.name_simui.set_ui_skew(name_simui_id, 0, 0)
        self.name_simui.set_ui_fill_z(name_simui_id, False)
        if self.gui_map_model:
            self.name_simui.set_parent(self.gui_map_model)
            local_pos = self.gui_map_model.get_socket_matrix('name', world.SPACE_TYPE_LOCAL)
            self.name_simui.position = local_pos.translation

    def trans_ui_pos_to_rt_uv(self, x, y):
        scn = self.scene()
        if not scn:
            return
        else:
            if self.cockipt_model_ref:
                cockpit_model = self.cockipt_model_ref() if 1 else None
                return cockpit_model or None
            cam = scn.active_camera
            p0 = cam.screen_to_world(x, y)[0]
            cam_pos = cam.world_position
            ray_dir = p0 - cam_pos
            if ray_dir.is_zero:
                return
            ray_dir.normalize()
            pstart = cam_pos
            pend = pstart + ray_dir * 1000
            rres = cockpit_model.hit_by_ray(pstart, pend - pstart)
            if rres[0]:
                pos = pstart + (pend - pstart) * rres[1]
                pm_mat = cockpit_model.get_socket_matrix('juli', world.SPACE_TYPE_LOCAL)
                cockpit_mat = cockpit_model.world_transformation
                cockpit_mat.inverse()
                pos = pos * cockpit_mat
                dis_diff = pos - pm_mat.translation
                u = dis_diff.x / COCKPIT_BOLI_WIDTH
                v = dis_diff.y / COCKPIT_BOLI_HEIGHT
                return (
                 u, v)
            return
            return

    def trans_uv_to_rt_scene_pos(self, u, v):
        if not self.gui_map_target:
            return None
        else:
            if not self.gui_map_model:
                return None
            rt_x = MAP_RT_CONF['rt_width'] * u
            rt_y = MAP_RT_CONF['rt_height'] * (1 - v)
            rt_cam = self.gui_map_target.camera
            rt_scn = self.gui_map_target.scn
            p0, p0dir = rt_cam.screen_to_world(rt_x, rt_y, self.gui_map_target.rt)
            p0dir.normalize()
            pstart = rt_cam.world_position
            pend = pstart + p0dir * 1000
            final_mat = mutil.FINAL_WORLD_INVERSE_MAT
            if self.gui_map_model and self.gui_map_model.valid:
                world_mat = self.gui_map_model.world_transformation
                world_mat.inverse()
                final_mat = world_mat
            result = rt_scn.scene_col.hit_by_ray(pstart, pend, 0, -1, -1, collision.INCLUDE_FILTER)
            if result[0]:
                return result[1] * final_mat
            return None
            return None

    def calc_map_can_move_pos(self, z, i=0):
        import math
        cam = self.gui_map_target.camera
        pos = self.gui_map_model.world_position
        pos.x += 350
        pos.y += 350
        cam_dir = pos - cam.world_position
        new_pos = cam_dir * ((pos.z - 100.0) / pos.z) + cam.world_position
        diff_pos = new_pos - pos
        z = new_pos.z
        cam_fov = MAP_RT_CONF['cam_fov']
        rt_width = MAP_RT_CONF['rt_width']
        rt_height = MAP_RT_CONF['rt_height']
        base_x = mutil.BASE_X
        base_y = mutil.BASE_Y
        base_z = mutil.BASE_Z
        base_height = base_z * math.tan(cam_fov / 2.0 / 180.0 * math.pi) * 2
        base_width = base_height * (rt_width / rt_height)
        cur_height = z / base_z * base_height
        cur_width = z / base_z * base_width
        width = (base_width - cur_width) / 2.0
        height = (base_height - cur_height) / 2.0
        print(width)
        print(height)

    def rotate_map_model(self, rtype, value):
        if not self.is_operational:
            self.check_is_playing_animation()
            return
        map_model = self.gui_map_model
        if not map_model or not map_model.valid:
            return
        cur_rot_mat = map_model.world_rotation_matrix
        v = math3d.matrix_to_euler(cur_rot_mat)
        x_d = v.x / math.pi * 180
        y_d = v.y / math.pi * 180
        if rtype == mutil.MAP_3D_ROTATE_X:
            x_d += value
            x_d = min(max(mutil.MIN_X_DEGREE, x_d), mutil.MAX_X_DEGREE)
        elif rtype == mutil.MAP_3D_ROTATE_Z:
            y_d += value
        x_dr = x_d / 180.0 * math.pi
        y_dr = y_d / 180.0 * math.pi
        new_vr = math3d.vector(x_dr, y_dr, v.z)
        map_model.world_rotation_matrix = math3d.euler_to_matrix(new_vr)
        global_data.emgr.map_model_transformation_changed_event.emit()

    def scale_map_model(self, dist, anchor_pos):
        if not self.is_operational:
            self.check_is_playing_animation()
            return
        map_model = self.gui_map_model
        if not map_model or not map_model.valid:
            return
        if not self.gui_map_target:
            return
        cur_z = map_model.world_position.z
        new_z = cur_z + dist
        new_z = min(max(mutil.MIN_MAP_AND_CAM_DISTANCE, new_z), mutil.MAX_MAP_AND_CAM_DISTANCE)
        world_pos = self.gui_map_model.world_position
        world_pos.z = new_z
        self.gui_map_model.world_position = world_pos
        global_data.emgr.map_model_transformation_changed_event.emit()

    def calc_can_move_range(self, z):
        cam_fov = MAP_RT_CONF['cam_fov']
        rt_width = MAP_RT_CONF['rt_width']
        rt_height = MAP_RT_CONF['rt_height']
        base_z = mutil.BASE_Z
        base_height = base_z * math.tan(cam_fov / 2.0 / 180.0 * math.pi) * 2
        base_width = base_height * (rt_width / rt_height)
        cur_height = z / base_z * base_height
        cur_width = z / base_z * base_width
        width = (base_width - cur_width) / 2.0
        height = (base_height - cur_height) / 2.0
        return (
         width, height)

    def move_map_pos(self, x, y):
        move_range = self.calc_can_move_range(self.gui_map_model.world_position.z)
        if not move_range:
            return
        width, height = move_range
        base_x = mutil.BASE_X
        base_y = mutil.BASE_Y
        pos = self.gui_map_model.world_position + math3d.vector(x, y, 0)
        pos.x = min(max(pos.x, base_x - width), base_x + width)
        pos.y = min(max(pos.y, base_y - width), base_y + width)
        self.gui_map_model.world_position = pos
        global_data.emgr.map_model_transformation_changed_event.emit()

    def on_gui_map_loaded(self, model, data, task, *args):
        if self.gui_map_model:
            model.destroy()
            return
        else:
            if not self.gui_map_target:
                model.destroy()
                return
            self.gui_map_model = model
            global_data.gui_map_model = model
            self.gui_map_task = None
            self.gui_map_target.add_model(model, pos=mutil.ANI_START_POS, rotation_matrix=mutil.START_ROT_MAT, scale=mutil.START_SCALE)
            self.gui_map_target.scn.scene_col.hit_by_ray(math3d.vector(0, 0, 0), math3d.vector(0, 0, 0), 0, -1, -1, collision.INCLUDE_FILTER)
            model.active_collision = True
            if self.is_playing_animation:
                self.show_3d_map_with_animation()
            else:
                self.show_3d_map_instant()
            global_data.emgr.map_3d_model_loaded_event.emit(model)
            return

    def show_3d_map_with_animation(self):
        if not self.gui_map_target:
            return
        if not self.gui_map_model:
            return
        import time
        from common.utils import timer
        st = time.time()
        sflag = [
         0, 0]

        def on_update_ani(*args):
            scn = self.scene()
            now = time.time()
            diff_time = now - st
            if diff_time <= 4:
                if not sflag[0]:
                    sflag[0] = 1
                    self.gui_map_model.world_rotation_matrix = mutil.ANI_START_ROT
                    self.gui_map_model.scale = mutil.START_SCALE
                else:
                    cur_rot = self.gui_map_model.world_rotation_matrix
                    cur_rot = cur_rot * mutil.ROT1
                    self.gui_map_model.world_rotation_matrix = cur_rot
            else:
                if diff_time > 4 and diff_time <= 4.2:
                    self.gui_map_model.world_rotation_matrix = sflag[1] or mutil.START_ROT_MAT
                sflag[1] += 0.033
                if sflag[1] > 1:
                    sflag[1] = 1 if 1 else sflag[1]
                    pos = self.gui_map_model.position
                    pos.intrp(pos, mutil.ANI_END_POS, sflag[1])
                    self.gui_map_model.position = pos
                    cur_rot = math3d.matrix_to_rotation(self.gui_map_model.world_rotation_matrix)
                    cur_rot.slerp(cur_rot, mutil.END_ROT, sflag[1])
                    self.gui_map_model.world_rotation_matrix = math3d.rotation_to_matrix(cur_rot)
                    scale = self.gui_map_model.scale
                    scale.intrp(scale, mutil.END_SCALE, sflag[1])
                    self.gui_map_model.scale = scale
                else:
                    self.show_3d_map_instant()
                    if self.start_sfx_id:
                        global_data.sfx_mgr.remove_sfx_by_id(self.start_sfx_id)
                        self.start_sfx_id = None
                    if not self.has_play_start02:
                        global_data.emgr.show_screen_effect.emit('ScreenMapStart', {})
                        self.has_play_start02 = True
                    global_data.emgr.show_airline_ani_event.emit()
                    global_data.emgr.set_3d_map_camera_event.emit(True)
                    self.gui_ani_timer = None
                    return timer.RELEASE
            return

        self.gui_ani_timer = global_data.game_mgr.register_logic_timer(on_update_ani, interval=1, times=-1, mode=timer.LOGIC)

    def check_is_playing_animation(self):
        if not self.gui_map_model:
            return
        else:
            if self.gui_ani_timer:
                global_data.game_mgr.unregister_logic_timer(self.gui_ani_timer)
                self.gui_ani_timer = None
            if not self.stop_ani_timer:
                sflag = [
                 0]

                def on_update_stop_ani(*args):
                    if sflag[0] < 0.2:
                        sflag[0] += 0.033
                        sflag[0] = 1 if sflag[0] >= 1 else sflag[0]
                        map_model = self.gui_map_model
                        pos = self.gui_map_model.position
                        pos.intrp(pos, mutil.ANI_END_POS, sflag[0])
                        map_model.world_position = pos
                        cur_rot = math3d.matrix_to_rotation(map_model.world_rotation_matrix)
                        cur_rot.slerp(cur_rot, mutil.END_ROT, sflag[0])
                        map_model.world_rotation_matrix = math3d.rotation_to_matrix(cur_rot)
                        scale = map_model.scale
                        scale.intrp(scale, mutil.END_SCALE, sflag[0])
                        map_model.scale = scale
                    else:
                        self.show_3d_map_instant()
                        self.stop_ani_timer = None
                        self.is_operational = True
                        global_data.emgr.set_3d_map_camera_event.emit(True)
                        global_data.emgr.show_airline_ani_event.emit()
                        if not self.has_play_start02:
                            global_data.emgr.show_screen_effect.emit('ScreenMapStart', {})
                            self.has_play_start02 = True
                        return timer.RELEASE
                    return

                self.stop_ani_timer = global_data.game_mgr.register_logic_timer(on_update_stop_ani, interval=1, times=-1, mode=timer.LOGIC)
            return

    def show_3d_map_instant(self):
        gui_map_model = self.gui_map_model
        if not gui_map_model or not gui_map_model.valid:
            return
        else:
            if self.gui_ani_timer:
                global_data.game_mgr.unregister_logic_timer(self.gui_ani_timer)
                self.gui_ani_timer = None
            if self.start_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self.start_sfx_id)
                self.start_sfx_id = None
            gui_map_model.play_animation('rotate', 0, 0, 0, 0, 0)
            gui_map_model.scale = mutil.END_SCALE
            gui_map_model.world_rotation_matrix = mutil.END_ROT_MAT
            gui_map_model.world_position = mutil.END_POS
            global_data.emgr.show_map_info_event.emit()
            return

    def set_render_target_to_model(self, model, tex_name, tex_index=1):
        if not model or not model.valid:
            return
        if not self.gui_map_target:
            log_error('[Part3DMap] gui_map_target is None!!!')
            return
        import game3d
        hash_tex = game3d.calc_string_hash(tex_name)
        model.get_sub_material(tex_index).set_texture(hash_tex, tex_name, self.gui_map_target.tex)
        model.get_sub_material(tex_index).set_var(_HASH_RT_OR_COLOR, 'rt_or_color', 0.0)
        model.get_sub_material(tex_index).set_var(_HASH_ALPHAMTL, 'AlphaMtl', 0.95)
        import device_compatibility
        if not device_compatibility.is_sys_uv_left_bottom():
            model.get_sub_material(tex_index).set_var(_HASH_Y_Flip, 'Y_Flip', 1.0)
        self.cockipt_model_ref = weakref.ref(model)

    def reset_3d_map(self):
        if self.gui_ani_timer:
            global_data.game_mgr.unregister_logic_timer(self.gui_ani_timer)
            self.gui_ani_timer = None
        if self.stop_ani_timer:
            global_data.game_mgr.unregister_logic_timer(self.stop_ani_timer)
            self.stop_ani_timer = None
        if self.gui_map_model:
            self.gui_map_model.destroy()
            self.gui_map_model = None
        if self.gui_map_target:
            self.gui_map_target.stop_render_target()
            self.gui_map_target.destroy()
            self.gui_map_target = None
            render.enable_dynamic_culling(global_data.feature_mgr.is_support_dyculling())
        if self.gui_map_task:
            self.gui_map_task.cancel()
            self.gui_map_task = None
        if self.start_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.start_sfx_id)
            self.start_sfx_id = None
        cockpit_model = self.cockipt_model_ref() if self.cockipt_model_ref else None
        if cockpit_model and cockpit_model.valid:
            cockpit_model.get_sub_material(1).set_var(_HASH_RT_OR_COLOR, 'rt_or_color', 1.0)
            cockpit_model.get_sub_material(1).set_var(_HASH_ALPHAMTL, 'AlphaMtl', 0.078)
        return