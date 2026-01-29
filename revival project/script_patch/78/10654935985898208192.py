# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMap.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import six
import six_ex
from . import ScenePart
from logic.gutils import map_utils
from logic.comsys.teammate.TeammateManager import TeammateManager
import time
from logic.gcommon.common_utils import parachute_utils
from logic.gutils import judge_utils
from logic.client.const import game_mode_const
from logic.gcommon.common_utils import local_text
from logic.gcommon.common_const.lang_data import code_2_shorthand
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL, BATTLE_SCENE_KONGDAO
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, GROUP_CHARACTER_INCLUDE
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from common.utils import timer
import math
import math3d
import game3d
import render
import world
import collision
_HASH_TEX = game3d.calc_string_hash('Tex0')
_HASH_COLOR = game3d.calc_string_hash('main_color')
_HASH_HALO_COLOR = game3d.calc_string_hash('haloColor')
MAP_NAME_COLOR = {BATTLE_SCENE_NORMAL: ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.0, 28.0 / 255.0, 1.0)),BATTLE_SCENE_KONGDAO: (
                        (0.0, 0.0, 0.0), (1.0, 220.0 / 255.0, 120.0 / 255.0), (160.0 / 255.0, 24.0 / 255.0, 0.0))
   }

class PartMap(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_show_big_map_event': 'show_big_map_ui',
       'scene_clear_player_map_marks': 'clear_player_marks',
       'scene_draw_line_event': 'draw_scene_line',
       'scene_clear_line_event': 'clear_scene_line',
       'scene_draw_wireframe_event': 'draw_trigger_wireframe',
       'scene_draw_wireframe_ball_event': 'draw_trigger_ball',
       'scene_observed_player_setted_event': 'on_enter_observe',
       'add_teammate_name_event': 'on_add_player',
       'scene_deep_mark': 'deep_mark',
       'scene_open_last_vehicle_flag_event': 'on_open_last_vehicle_flag',
       'scene_close_last_vehicle_flag_event': 'on_close_last_vehicle_flag',
       'scene_on_teammate_change': 'on_teammate_change',
       'scene_camera_player_setted_event': 'on_cam_lplayer_changed',
       'on_be_hit_event': 'on_fight_state',
       'on_observer_fire': 'on_fight_state',
       'scene_add_mark': 'add_common_mark',
       'scene_del_mark': 'del_common_mark',
       'scene_add_client_mark': 'add_client_mark',
       'scene_del_client_mark': 'del_client_mark',
       'scene_ai_mark': 'ai_common_mark',
       'scene_start_poison_circle_event': 'start_poison_circle',
       'scene_refresh_poison_circle_event': 'refresh_poison_circle',
       'scene_reduce_poison_circle_event': 'reduce_poison_circle',
       'scene_save_map_info_event': 'save_big_map_info',
       'settle_stage_event': 'on_create_settle_stage_ui',
       'mecha_8033_scan': 'scan_enemy_8033'
       }

    def __init__(self, scene, name):
        super(PartMap, self).__init__(scene, name)
        self._concerned_target_ids = []
        self._binded_target_ids = []
        self.map_marks = {}
        self.map_color_info = {}
        self.big_map_scale = None
        self.big_map_offset = None
        self._scene_timers = set()
        self._scene_timers_pri = {}
        self.map_config = map_utils.get_map_config()
        self.common_map_marks = {}
        self.ai_map_marks = {}
        self.client_map_marks = {}
        self.avatar_last_vehicle = None
        self._teammate_mgr = None
        self._map_area_name_bg_model_id = []
        self._map_area_name_model_id = []
        self._area_info_timer = None
        self._cur_area_id = None
        self._area_info_dic = {}
        self._in_fight_state = False
        self._fight_state_end_interval = 0
        self.check_height_timer = None
        self.mecha_8033_scan_enemy = []
        self.mecha_8033_enemy_timer = None
        return

    def add_sub_sys(self):
        self.register_sub_sys('SysMapQuickMark')
        self.register_sub_sys('SysMapAirlineMgr')
        self.register_sub_sys('SysMapEffectMgr')

    def on_enter(self):
        self.check_scene_custom_uv()
        self.add_sub_sys()
        self.init_poison_circle()
        self.map_config = map_utils.get_map_config()
        self.init_map_parameter()
        self.show_scale_plate_ui()
        global_data.cam_lplayer and self.on_player_setted(global_data.cam_lplayer)
        self.show_small_map_ui()
        self.show_map_mark_btn()
        if not self._teammate_mgr:
            self._teammate_mgr = TeammateManager()
            self._teammate_mgr.set_player(global_data.cam_lplayer)
        self._area_info_dic = {}
        self._area_info_timer = global_data.game_mgr.get_logic_timer().register(func=self.on_update_area_info, interval=10, mode=timer.CLOCK)
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            if judge_utils.is_ob():
                self._show_big_map_ui()
                global_data.ui_mgr.close_ui('JudgeLoadingUI')
        self.create_check_height_timer()

    def clear_check_height_timer(self):
        self.check_height_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_height_timer)
        self.check_height_timer = None
        return

    def is_show_map_name(self):
        if not global_data.cam_lplayer:
            return False
        position = global_data.cam_lplayer.ev_g_position()
        if not position:
            return False
        pos_y = position.y
        if math.isinf(pos_y) or math.isnan(pos_y):
            return False
        return pos_y > 1500

    def create_check_height_timer(self):

        def _check():
            if not self.is_show_map_name():
                self._del_map_name_model()
                if self.is_same_battle():
                    self.clear_check_height_timer()
            else:
                self.init_map_area_name()

        self.clear_check_height_timer()
        self.check_height_timer = global_data.game_mgr.get_logic_timer().register(func=_check, mode=timer.CLOCK, interval=1)

    def is_same_battle(self):
        battle_id = ''
        if global_data.battle:
            battle_id = str(global_data.battle.id)
        mark_battle_id = global_data.message_data.get_seting_inf('init_map_area_name')
        return mark_battle_id == battle_id

    def init_map_area_name(self):
        if self._map_area_name_model_id:
            return
        if self.is_same_battle():
            return
        if not global_data.battle:
            return
        scene_name = global_data.battle.get_scene_name()
        area_infos = confmgr.get('map_area_conf', scene_name, 'Content', default={})
        tv_e_conf = confmgr.get('tv_conf', 'cl_tv_entity', 'Content', default={})
        for index in six_ex.keys(area_infos):
            map_area_id = int(index)
            tv_id = 200000 + map_area_id
            scale_off = (1.0, 1.0)
            if str(tv_id) in tv_e_conf:
                self._create_map_name_model(tv_id, map_area_id, scale_off)

        if global_data.battle:
            global_data.message_data.set_seting_inf('init_map_area_name', str(global_data.battle.id))

    def _create_map_name_model(self, tv_id, map_area_id, scale_off):
        battle = global_data.battle
        forward_dir = 1
        if battle:
            plane = battle.get_entity(battle.plane_id)
            if plane and plane.logic:
                forward = plane.logic.ev_g_plane_direction()
                forward_dir = 1 if forward.cross(math3d.vector(1, 0, 0)).y <= 0 else -1
        lang = local_text.get_cur_text_lang()
        lang_str = code_2_shorthand.get(int(lang), 'en')
        path = 'model_new/scene/textures/map_name_sdf/%s/%d.png' % (lang_str, map_area_id)
        tv_e_conf = confmgr.get('tv_conf', 'cl_tv_entity', 'Content', default={})
        pos = tv_e_conf.get(str(tv_id), {}).get('pos', [0, 0, 0])
        scale = tv_e_conf.get(str(tv_id), {}).get('scale', [1, 1, 1])
        map_area_res_path = confmgr.get('script_gim_ref')['map_area_name']

        def bg_call_back(model, path=path, scale=scale, forward_dir=forward_dir):
            model.scale = math3d.vector(scale[0], scale[1], scale[2])
            mat = math3d.euler_to_matrix(math3d.vector(0, forward_dir * math.pi * 0.5, 0))
            model.rotation_matrix = mat
            tex = render.texture(path)
            model.all_materials.set_texture(_HASH_TEX, 'Tex0', tex)
            scene_name = global_data.battle and global_data.battle.get_scene_name() or BATTLE_SCENE_NORMAL
            main_color = MAP_NAME_COLOR.get(scene_name)[0]
            haloColor = MAP_NAME_COLOR.get(scene_name)[2]
            model.all_materials.set_var(_HASH_COLOR, 'main_color', main_color)
            model.all_materials.set_var(_HASH_HALO_COLOR, 'haloColor', haloColor)
            model.all_materials.set_macro('BACKGROUND_PATTERN', '0')
            model.all_materials.rebuild_tech()
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 11)

        model_id = global_data.model_mgr.create_model_in_scene(map_area_res_path, pos=math3d.vector(pos[0], pos[1] - 30, pos[2]), on_create_func=bg_call_back)
        self._map_area_name_bg_model_id.append(model_id)

        def call_back(model, path=path, scale=scale, forward_dir=forward_dir):
            model.scale = math3d.vector(scale[0], scale[1], scale[2])
            mat = math3d.euler_to_matrix(math3d.vector(0, forward_dir * math.pi * 0.5, 0))
            model.rotation_matrix = mat
            tex = render.texture(path)
            model.all_materials.set_texture(_HASH_TEX, 'Tex0', tex)
            scene_name = global_data.battle and global_data.battle.get_scene_name() or BATTLE_SCENE_NORMAL
            main_color = MAP_NAME_COLOR.get(scene_name)[1]
            haloColor = MAP_NAME_COLOR.get(scene_name)[2]
            model.all_materials.set_var(_HASH_COLOR, 'main_color', main_color)
            model.all_materials.set_var(_HASH_HALO_COLOR, 'haloColor', haloColor)
            model.all_materials.set_macro('BACKGROUND_PATTERN', '0')
            model.all_materials.rebuild_tech()
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 12)

        model_id = global_data.model_mgr.create_model_in_scene(map_area_res_path, pos=math3d.vector(pos[0], pos[1], pos[2]), on_create_func=call_back)
        self._map_area_name_model_id.append(model_id)

    def _del_map_name_model(self):
        for mode_id in self._map_area_name_bg_model_id:
            global_data.model_mgr.remove_model_by_id(mode_id)

        for mode_id in self._map_area_name_model_id:
            global_data.model_mgr.remove_model_by_id(mode_id)

        self._map_area_name_bg_model_id = []
        self._map_area_name_model_id = []

    def init_map_parameter(self):
        scn = self.scene()
        self.LEFT_TRK_IDX, self.RIGHT_TRK_IDX, self.BOTTOM_TRK_IDX, self.UP_TRK_IDX, self.TRUNK_SIZE = scn.get_safe_scene_map_uv_parameters()
        self.MAP_HEIGHT_DIST = self.TRUNK_SIZE * (self.UP_TRK_IDX - self.BOTTOM_TRK_IDX + 1)
        self.MAP_WIDTH_DIST = self.TRUNK_SIZE * (self.RIGHT_TRK_IDX - self.LEFT_TRK_IDX + 1)

    def on_update_area_info(self):
        if not (global_data.player and global_data.player.logic):
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if parachute_utils.is_parachuting(stage) or parachute_utils.is_preparing(stage):
            return
        battle = global_data.player.get_battle()
        if battle and battle.is_battle_prepare_stage():
            return
        logic = global_data.player.logic
        if logic.ev_g_in_mecha():
            logic = logic.ev_g_control_target().logic
        if logic:
            pos = logic.ev_g_model_position()
            if pos:
                area_id = self.scene().get_scene_area_info(pos.x, pos.z)
                if area_id != self._cur_area_id:
                    self._cur_area_id = area_id
                    if self._in_fight_state:
                        return
                    if area_id in self._area_info_dic:
                        if self._area_info_dic[area_id] > time.time():
                            return
                    self._area_info_dic[area_id] = time.time() + 30
                    from common.cfg import confmgr
                    from logic.gcommon.common_const import battle_const
                    scene_name = battle.get_scene_name()
                    area_info = confmgr.get('map_area_conf', scene_name, 'Content', str(area_id))
                    if area_info:
                        if not area_info.get('rich_id', 0):
                            return
                        global_data.emgr.battle_event_message.emit(area_info, message_type=battle_const.UP_NODE_AREA_INFO)

    def on_fight_state(self, *args):
        self.need_update = True
        self._in_fight_state = True
        self._fight_state_end_interval = 0

    def on_update(self, dt):
        if self._in_fight_state:
            self._fight_state_end_interval += dt
            if self._fight_state_end_interval > 2:
                self._in_fight_state = False
                self._fight_state_end_interval = 0

    def on_player_setted(self, player):
        if player is None:
            return
        else:
            self.update_team_member_info(player)
            return

    def update_team_member_info(self, player):
        self.on_update_team_member_info(player)
        self.update_map_players()

    def on_exit(self):
        self._cur_area_id = None
        global_data.ui_mgr.close_ui('SmallMapUI')
        global_data.ui_mgr.close_ui('BigMapUI')
        global_data.ui_mgr.close_ui('MidMapUI')
        global_data.ui_mgr.close_ui('ScalePlateUI')
        global_data.ui_mgr.close_ui('FightKillNumberUI')
        global_data.ui_mgr.close_ui('QuickMarkBtn')
        global_data.ui_mgr.close_ui('QuickMarkBtnMecha')
        global_data.ui_mgr.close_ui('QuickMarkBtnPC')
        global_data.ui_mgr.close_ui('PVEQuickMarkBtn')
        self.clear_timers()
        self.clear_all_info()
        if self._teammate_mgr:
            self._teammate_mgr.destroy()
        self._teammate_mgr = None
        if self._area_info_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._area_info_timer)
            self._area_info_timer = None
        self._del_map_name_model()
        self.clear_check_height_timer()
        self.unregister_timer()
        super(PartMap, self).on_exit()
        return

    def on_open_last_vehicle_flag(self, last_vehicle):
        import weakref
        self.avatar_last_vehicle = weakref.ref(last_vehicle)

    def on_close_last_vehicle_flag(self):
        self.avatar_last_vehicle = None
        return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_CONCERT, game_mode_const.GAME_MODE_HUNTING))
    def show_small_map_ui(self):
        from logic.comsys.map.SmallMapUINew import SmallMapUI, SmallMapUIPC
        global_data.ui_mgr.close_ui('SmallMapUI')
        if global_data.is_pc_mode:
            SmallMapUIPC(scale=1)
        else:
            SmallMapUI(scale=1)

    def show_map_mark_btn(self):
        from logic.gutils.judge_utils import is_ob
        if not is_ob():
            from logic.comsys.map.QuickMarkBtn import QuickMarkBtn, QuickMarkBtnMecha
            from logic.comsys.map.QuickMarkBtnPC import QuickMarkBtnPC
            from logic.comsys.map.PVEQuickMarkBtn import PVEQuickMarkBtn
            if global_data.is_pc_mode:
                QuickMarkBtnPC()
            elif global_data.game_mode and global_data.game_mode.is_pve():
                PVEQuickMarkBtn()
            else:
                QuickMarkBtn()
                QuickMarkBtnMecha()

    def update_map_players(self):
        scale_plate_ui = global_data.ui_mgr.get_ui('ScalePlateUI')
        if scale_plate_ui:
            scale_plate_ui.set_show_player_ids(six_ex.keys(self.map_color_info), self.map_color_info, self.map_marks)

    def show_big_map_ui(self):
        if not (global_data.player and global_data.player.logic):
            return
        self._show_big_map_ui()

    def _show_big_map_ui(self):
        if global_data.is_pc_mode:
            from logic.comsys.map.BigMapUINewPC import BigMapUIPC
            BigMapUIPC(scale=self.big_map_scale, center_pos=self.big_map_offset)
        else:
            from logic.comsys.map.BigMapUINew import BigMapUI
            BigMapUI(scale=self.big_map_scale, center_pos=self.big_map_offset)
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'map_zoom_out'))
        global_data.emgr.show_big_map_ui_event.emit()

    def on_show_map_mark(self, unit_id, mark_type, v3d_map_pos=None, extra_args=None):
        if mark_type is not None:
            if unit_id not in self.map_marks:
                self.map_marks[unit_id] = {}
            if mark_type not in self.map_marks[unit_id]:
                self.map_marks[unit_id][mark_type] = []
            self.map_marks[unit_id][mark_type].append({'pos': v3d_map_pos,'extra_args': extra_args})
            if not extra_args:
                extra_args = {}
            extra_args['is_init'] = True
            map_utils.add_scene_map_mark(unit_id, mark_type, v3d_map_pos, extra_args)
        else:
            self.clear_player_map_mark(unit_id)
        return

    def dist_map_col(self, ids):
        from logic.gutils.team_utils import get_teammate_colors
        player_col = get_teammate_colors(ids)
        return player_col

    def on_update_team_member_info(self, player):
        self.clear_all_info()
        player_ids = player.ev_g_groupmate()
        if player.id not in self.map_color_info:
            if not player_ids:
                player_ids = [
                 player.id]
            if player_ids:
                player_col_dic = self.dist_map_col(player_ids)
                self.map_color_info = player_col_dic
        self.bind_target_event(player_ids)
        self._concerned_target_ids = list(player_ids)
        self.collect_target_marks_and_route()

    def collect_target_marks_and_route(self):
        for tid in self._concerned_target_ids:
            self._collect_single_target_marks_and_route(tid)

    def _collect_single_target_marks_and_route(self, tid):
        target = EntityManager.getentity(tid)
        if not (target and target.logic and target.logic.is_valid()):
            return
        else:
            mark_dict = target.logic.ev_g_drawn_map_mark()
            if mark_dict is None:
                return
            global_data.emgr.remove_scene_mark.emit(tid)
            for mark_infos in six.itervalues(mark_dict):
                for mark_dict in mark_infos:
                    self.on_show_map_mark(tid, mark_dict.get('type'), mark_dict.get('v3d_map_pos'), mark_dict.get('extra_args'))

            return

    def bind_target_event(self, target_id_set):
        for tid in target_id_set:
            if tid not in self._binded_target_ids:
                self._bind_target_event_helper(tid, False)
                if self._bind_target_event_helper(tid, True):
                    self._binded_target_ids.append(tid)

    def unbind_target_event(self, target_id_set):
        for tid in target_id_set:
            if tid in self._binded_target_ids:
                self._bind_target_event_helper(tid, False)
                self._binded_target_ids.remove(tid)

    def _bind_target_event_helper(self, target_id, is_bind):
        target = EntityManager.getentity(target_id)
        if not (target and target.logic and target.logic.is_valid()):
            return False
        if is_bind:
            func = target.logic.regist_event
        else:
            func = target.logic.unregist_event
        func('E_DRAW_MAP_MARK', self.on_show_map_mark)
        func('E_CLEAR_SELF_MAP_MARK', self.clear_player_map_mark)
        return True

    def clear_all_info(self):
        if self._concerned_target_ids:
            self.unbind_target_event(self._binded_target_ids[:])
            self._concerned_target_ids = []
            self._binded_target_ids = []
            self.clear_records()

    def clear_player_map_mark(self, unit_id):
        global_data.emgr.scene_clear_player_map_marks.emit(unit_id)

    def clear_player_marks(self, unit_id):
        if unit_id in self.map_marks:
            del self.map_marks[unit_id]

    def clear_player_marks_by_type(self, unit_id, mark_type):
        if unit_id not in self.map_marks:
            return
        if mark_type in self.map_marks[unit_id] and self.map_marks[unit_id][mark_type]:
            self.map_marks[unit_id][mark_type].pop(0)
            if not self.map_marks[unit_id][mark_type]:
                del self.map_marks[unit_id][mark_type]
        if unit_id not in self.map_marks:
            del self.map_marks[unit_id]

    def clear_records(self):
        self.map_marks = {}
        self.map_color_info = {}

    def init_poison_circle(self):
        from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_NONE
        self.poison_circle_level = 0
        self.safe_circle_center = 0
        self.safe_circle_radius = 0
        self.poison_circle_center = 0
        self.poison_circle_radius = 0
        self.circle_refresh_time = 0
        self.circle_state = POISON_CIRCLE_STATE_NONE
        self.circle_state_last_time = 0

    def get_poison_circle_info(self):
        return {'state': self.circle_state,
           'safe_center': self.safe_circle_center,
           'safe_radius': self.safe_circle_radius,
           'poison_center': self.poison_circle_center,
           'poison_radius': self.poison_circle_radius,
           'start_time': self.circle_refresh_time,
           'last_time': self.circle_state_last_time,
           'level': self.poison_circle_level
           }

    def start_poison_circle(self, state, refresh_time, last_time):
        self.circle_state = state
        self.circle_refresh_time = refresh_time
        self.circle_state_last_time = last_time

    def _register_poison_circle_tips_timer(self, count_down_time, tips, timer_name):
        from common.utils.timer import CLOCK
        tm = global_data.game_mgr.get_logic_timer()
        from logic.gcommon.time_utility import time
        server_time = time()
        delay_time = self.circle_refresh_time + self.circle_state_last_time - count_down_time - server_time
        if delay_time <= 0:
            return

        def show_text():
            global_data.emgr.battle_show_message_event.emit(tips)
            setattr(self, timer_name, None)
            return

        self._cancel_timer(timer_name)
        t = tm.register(func=lambda : show_text(), interval=delay_time, times=1, mode=CLOCK)
        setattr(self, timer_name, t)

    def _cancel_timer(self, timer_name):
        tm = global_data.game_mgr.get_logic_timer()
        _timer = getattr(self, timer_name, None)
        if _timer is not None:
            if _timer:
                tm.unregister(_timer)
                setattr(self, timer_name, None)
        return

    def clear_timers(self):
        tm = global_data.game_mgr.get_logic_timer()
        for tid in self._scene_timers:
            if tid is not None:
                tm.unregister(tid)

        self._scene_timers.clear()
        self._cancel_timer('timer_10_count_down')
        return

    def refresh_poison_circle(self, state, refresh_time, last_time, level, poison_point, safe_point, reduce_type):
        import math3d
        self.circle_state = state
        self.circle_refresh_time = refresh_time
        self.circle_state_last_time = last_time
        self.safe_circle_center = math3d.vector(safe_point[0], 0, safe_point[1])
        self.safe_circle_radius = safe_point[2]
        self.poison_circle_center = math3d.vector(poison_point[0], 0, poison_point[1])
        self.poison_circle_radius = poison_point[2]
        self.poison_circle_level = level
        scale_plate_ui = global_data.ui_mgr.get_ui('ScalePlateUI')
        if scale_plate_ui:
            scale_plate_ui.set_safe_center(self.safe_circle_center)

    def reduce_poison_circle(self, state, refresh_time, last_time, reduce_type):
        self.circle_state = state
        self.circle_refresh_time = refresh_time
        self.circle_state_last_time = last_time

    def save_big_map_info(self, scale, offset):
        self.big_map_scale = scale
        self.big_map_offset = offset

    def draw_scene_line(self, pts, alive_time=5, color=16711680):
        colors = [16711680, 65280, 255]
        import world
        pri = world.primitives(world.get_active_scene())
        pts_list = []
        for idx, pt in enumerate(pts):
            _color = colors[idx % len(colors)]
            pts_list.append((pt.x, pt.y, pt.z, _color))

        pri.create_line_strip(pts_list)
        tm = global_data.game_mgr.get_logic_timer()
        from common.utils.timer import CLOCK
        if alive_time <= 0:
            log_error('You are creating an immortal line!!!')
        if alive_time > 0:
            _timer_id = tm.register(func=self._remove_scene_line, interval=alive_time, times=1, mode=CLOCK)
            tm.set_args(_timer_id, [pri, _timer_id])
            self._scene_timers.add(_timer_id)
            self._scene_timers_pri[_timer_id] = pri
        return pri

    def clear_scene_line(self):
        for timer_id in self._scene_timers_pri:
            pri = self._scene_timers_pri[timer_id]
            pri and pri.remove_from_parent()

        self._scene_timers_pri = {}
        tm = global_data.game_mgr.get_logic_timer()
        for timer_id in self._scene_timers:
            tm.unregister(timer_id)

        self._scene_timers.clear()

    def draw_trigger_wireframe(self, pos, rotation_mat, alive_time=10, length=(1, 1, 1), color=16711680):
        import world
        import math3d
        _points = [
         math3d.vector(-0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, -0.5), math3d.vector(-0.5, -0.5, -0.5)]
        pts = list(_points)
        pts.extend([ pt + math3d.vector(0, 1, 0) for pt in _points ])
        line_idx = [0, 1, 2, 0, 3, 2, 6, 3, 7, 6, 1, 5, 6, 4, 7, 0, 4, 5, 0]
        leng_vec = math3d.vector(*length)
        pts = [ i * leng_vec for i in pts ]
        pts_list = []
        for idx in line_idx:
            pts_list.append((pts[idx].x, pts[idx].y, pts[idx].z, color))

        tm = global_data.game_mgr.get_logic_timer()
        from common.utils.timer import CLOCK
        pri = world.primitives(world.get_active_scene())
        pri.create_line_strip(pts_list)
        pri.world_position = pos
        pri.world_rotation_matrix = rotation_mat

        def _remove_scene_pri():
            if pri:
                pri.remove_from_parent()

        if alive_time > 0:
            tm.register(func=_remove_scene_pri, interval=alive_time, times=1, mode=CLOCK)
        return pri

    def draw_trigger_ball(self, pos, rotation_mat=None, alive_time=10, length=(1, 1, 1), segments=4):
        import math3d

        def create_sphere_mesh(radius, num_segments):
            pts_list = []
            vertices = []
            indices = []
            for i in range(num_segments + 1):
                for j in range(num_segments + 1):
                    theta = i * math.pi / num_segments
                    phi = j * 2 * math.pi / num_segments
                    x = radius * math.sin(theta) * math.cos(phi)
                    y = radius * math.sin(theta) * math.sin(phi)
                    z = radius * math.cos(theta)
                    vertices.append((x, y, z))
                    if i < num_segments and j < num_segments:
                        a = i * (num_segments + 1) + j
                        b = i * (num_segments + 1) + j + 1
                        c = (i + 1) * (num_segments + 1) + j
                        d = (i + 1) * (num_segments + 1) + j + 1
                        indices.extend([a, b, c, b, d, c])

            for idx in indices:
                pts_list.append((vertices[idx][0], vertices[idx][1], vertices[idx][2], 16711680))

            return pts_list

        pts_list = create_sphere_mesh(length[0], segments)
        tm = global_data.game_mgr.get_logic_timer()
        from common.utils.timer import CLOCK
        pri = world.primitives(world.get_active_scene())
        pri.create_line_strip(pts_list)
        pri.world_position = pos
        if rotation_mat:
            pri.world_rotation_matrix = rotation_mat

        def _remove_scene_pri():
            if pri:
                pri.remove_from_parent()

        if alive_time > 0:
            tm.register(func=_remove_scene_pri, interval=alive_time, times=1, mode=CLOCK)
        return pri

    def _remove_scene_line(self, pri, timer_id):
        if timer_id in self._scene_timers:
            self._scene_timers.remove(timer_id)
        if pri:
            pri.remove_from_parent()

    def on_enter_observe(self, observe_targe):
        self.on_player_setted(observe_targe)

    def on_add_player(self, player, name):
        self.on_concerted_target_added(player)

    def on_concerted_target_added(self, player):
        if player.id in self._concerned_target_ids:
            if player.id not in self._binded_target_ids:
                self.bind_target_event([player.id])
                self._collect_single_target_marks_and_route(player.id)

    def add_common_mark(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        self.common_map_marks[mark_id] = {'mark_no': mark_no,'point': point,
           'is_deep': is_deep,
           'state': state,
           'create_timestamp': create_timestamp,
           'deep_timestamp': deep_timestamp
           }

    def add_client_mark(self, obj_id, mark_no, v3d_pos, require_follow_model=True, kwargs=None):
        self.client_map_marks[obj_id] = {'mark_no': mark_no,
           'v3d_pos': v3d_pos
           }

    def ai_common_mark(self, mark_id, point, state):
        if mark_id in self.ai_map_marks:
            self.ai_map_marks[mark_id]['point'] = point
            self.ai_map_marks[mark_id]['state'] = state
        else:
            self.ai_map_marks[mark_id] = {'point': point,
               'state': state
               }

    def del_common_mark(self, mark_id):
        if mark_id in self.common_map_marks:
            del self.common_map_marks[mark_id]
        if mark_id in self.ai_map_marks:
            del self.ai_map_marks[mark_id]

    def del_client_mark(self, mark_id):
        if mark_id in self.client_map_marks:
            del self.client_map_marks[mark_id]

    def deep_mark(self, mark_id, is_deep, state, deep_timestamp):
        if mark_id in self.common_map_marks:
            data = self.common_map_marks[mark_id]
            data['is_deep'] = is_deep
            data['state'] = state
            data['deep_timestamp'] = deep_timestamp

    def get_world_pos_in_map(self, world_pos):
        if not world_pos:
            return
        else:
            import world
            import cc
            scn = world.get_active_scene()
            res = scn.get_scene_map_uv_with_checking_script_logic(world_pos.x, world_pos.z)
            if res is not None:
                x, z = res
                size = self.map_config['arrMapResolution']
                return cc.Vec2(x * size[0], z * size[1])
            if global_data.use_sunshine:
                return cc.Vec2(0, 0)
            print('no get_world_pos_in_map ->get_scene_map_uv??? ')
            return
            return

    def get_map_pos_in_world(self, map_pos):
        import math3d
        final_left = (self.LEFT_TRK_IDX - 0.5) * self.TRUNK_SIZE
        final_bottom = (self.BOTTOM_TRK_IDX - 0.5) * self.TRUNK_SIZE
        size = self.map_config['arrMapResolution']
        u, v = float(map_pos.x) / size[0], float(map_pos.y) / size[1]
        return math3d.vector(u * self.MAP_WIDTH_DIST + final_left, 0, v * self.MAP_HEIGHT_DIST + final_bottom)

    def check_scene_custom_uv(self):
        if not global_data.battle:
            return
        map_data_conf = confmgr.get('map_config', str(global_data.battle.map_id), default={})
        scene = global_data.game_mgr.scene
        if scene:
            if 'cMapUVParas' in map_data_conf:
                paras = map_data_conf['cMapUVParas']
                print('map_data_conf  ', map_data_conf['cMapUVParas'])
                scene.enable_scene_custom_map_uv_parameters(*paras)

    def on_create_settle_stage_ui(self, *args):
        global_data.ui_mgr.close_ui('BigMapUI')
        global_data.ui_mgr.close_ui('MidMapUI')

    def show_scale_plate_ui(self):
        ui_inst = global_data.ui_mgr.show_ui('ScalePlateUI', 'logic.comsys.map')
        if ui_inst:
            ui_inst.set_show_player_ids(six_ex.keys(self.map_color_info), self.map_color_info, self.map_marks)
            ui_inst.set_safe_center(self.safe_circle_center)

    def on_teammate_change(self, unit_id):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == unit_id:
            self.on_player_setted(global_data.cam_lplayer)

    def on_cam_lplayer_changed(self):
        global_data.cam_lplayer and self.on_player_setted(global_data.cam_lplayer)
        if self._teammate_mgr:
            self._teammate_mgr.set_player(global_data.cam_lplayer)

    def unregister_timer(self):
        if self.mecha_8033_enemy_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.mecha_8033_enemy_timer)
        self.mecha_8033_enemy_timer = None
        return

    def scan_enemy_8033(self, mecha_eids):
        self.mecha_8033_scan_enemy = mecha_eids
        enemy_infos = []
        for eid in mecha_eids:
            mecha_entity = EntityManager.getentity(eid)
            if mecha_entity and mecha_entity.logic:
                pos = mecha_entity.logic.ev_g_position()
                enemy_infos.append((pos, False))

        self.mecha_8033_scan_enemy = enemy_infos
        global_data.emgr.mecha_8033_scan_info.emit()

    def get_mecha_8033_scan_enemy(self):
        return self.mecha_8033_scan_enemy