# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/LaunchBoostAppearance.py
from __future__ import absolute_import
import six
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_PLANE, STAGE_PRE_PARACHUTE, STAGE_ISLAND, PARACHUTE_ANIM_TIME
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_skin_item_no, get_mecha_model_h_path
from logic.gcommon.common_utils.decal_utils import decode_decal_list, decode_color
from logic.gutils.mecha_skin_utils import get_mecha_skin_shiny_id, MechaSocketResAgent
from logic.gcommon.common_utils.bcast_utils import E_SYNC_LAUNCH_BOOST_MECHA_POSITION_OFFSET, E_SYNC_LAUNCH_BOOST_MECHA_MOVE_DIR
from logic.client.path_utils import MECHA_READY_TRK_PATH
from .temp_boost_tail_sfx_info import TAIL_SFX_INFO
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK, RELEASE
from common.framework import Functor
from common.cfg import confmgr
from math import radians, fabs, acos, pi
import math3d
import world
import time
EMPTY_SUBMESH_NAME = 'empty'
EPSILON = 0.01
UP_VECTOR = math3d.vector(0, 1, 0)
MECHA_READY_ANIM_DURATION = PARACHUTE_ANIM_TIME * 1000
DEFAULT_CAM_PITCH = 0.5
INTRP_NONE = 0
INTRP_ENTER = 1
INTRP_LOOP = 2
INTRP_EXIT = 3
INTRP_STATE_COUNT = 4
SYNC_INTERVAL = 0.2
MECHA_OUTER_RADIUS = 6 * NEOX_UNIT_SCALE
MECHA_INNER_RADIUS = 5 * NEOX_UNIT_SCALE
MECHA_PUSH_SPEED = NEOX_UNIT_SCALE
MAX_INTRP_ANGLE = pi / 3.0

def float_equal(x, y):
    return fabs(x - y) < EPSILON


def clamp(x, min_val, max_val):
    if x > max_val:
        return max_val
    if x < min_val:
        return min_val
    return x


def get_intrp_duration(cur_value, target_value, delta_value):
    return (max(cur_value, target_value) - min(cur_value, target_value)) / delta_value


def get_intrp_result(cur_value, target_value, add_value):
    if target_value > cur_value:
        return cur_value + add_value
    else:
        if target_value < cur_value:
            return cur_value - add_value
        return cur_value


class LaunchBoostAppearance(object):

    def __init__(self, parent, load_model_callback):
        self.parent = parent
        self.load_model_callback = load_model_callback
        self.init_parameters()
        self.ready_anim_track = world.track(MECHA_READY_TRK_PATH)
        self.load_mecha_model()
        self.load_groupmate_mecha_model()

    def init_parameters(self):
        self.avatar_eid = global_data.player.id
        self.eid_list = []
        self.groupmate_eid_list = []
        self.specific_parameters_valid = {}
        self.cur_avatar_move_dir = math3d.vector(0, 0, 0)
        self.last_move_dir_x = {}
        self.last_move_dir_z = {}
        self.groupmate_lent = {}
        self.last_sync_time_stamp = 0.0
        self.mecha_position_offset = {}
        self.groupmate_mecha_last_target_position_offset = {}
        self.groupmate_mecha_move_dir = {}
        self.mecha_models = {}
        self.socket_res_agents = {}
        self.ready_anim_name = ''
        self.ready_anim_timer = -1
        self.ready_anim_initial_position = math3d.vector(0, 0, 0)
        conf = confmgr.get('launch_boost_conf')
        self.fly_zone_front_width = conf.get('FLY_ZONE_FRONT_WIDTH') * NEOX_UNIT_SCALE
        self.fly_zone_back_width = conf.get('FLY_ZONE_BACK_WIDTH') * NEOX_UNIT_SCALE
        self.fly_zone_front_dist = conf.get('FLY_ZONE_FRONT_DIST') * NEOX_UNIT_SCALE
        self.fly_zone_back_dist = conf.get('FLY_ZONE_BACK_DIST') * NEOX_UNIT_SCALE
        self.delta_fly_zone_width = (self.fly_zone_front_width - self.fly_zone_back_width) / (self.fly_zone_front_dist + self.fly_zone_back_dist)
        self.max_fly_speed = conf.get('FLY_SPEED') * NEOX_UNIT_SCALE
        self.fly_speed = {}
        self.max_mecha_roll_value_info = conf.get('MAX_ROLL_VALUE')
        self.max_mecha_yaw_value_info = conf.get('MAX_YAW_VALUE')
        self.max_mecha_pitch_value_info = conf.get('MAX_PITCH_VALUE')
        self.max_mecha_roll_value = {}
        self.max_mecha_yaw_value = {}
        self.max_mecha_pitch_value = {}
        self.mecha_rot_intrp_duration_info = conf.get('MECHA_ROT_INTRP_DURATION')
        self.mecha_rot_intrp_duration = {}
        self.mecha_rot_intrp_left_time = {}
        self.cur_mecha_roll = {}
        self.max_delta_mecha_roll = {}
        self.delta_mecha_roll = {}
        self.target_mecha_roll = {}
        self.cur_mecha_yaw = {}
        self.max_delta_mecha_yaw = {}
        self.delta_mecha_yaw = {}
        self.target_mecha_yaw = {}
        self.cur_mecha_pitch = {}
        self.max_delta_mecha_pitch = {}
        self.delta_mecha_pitch = {}
        self.target_mecha_pitch = {}
        self.initial_position_offset_dist = (
         math3d.vector(0, 0, 0),
         math3d.vector(-conf.get('INITIAL_SIDE_OFFSET_DIST') * NEOX_UNIT_SCALE, 0, -conf.get('INITIAL_FORWARD_OFFSET_DIST') * NEOX_UNIT_SCALE),
         math3d.vector(conf.get('INITIAL_SIDE_OFFSET_DIST') * NEOX_UNIT_SCALE, 0, -conf.get('INITIAL_FORWARD_OFFSET_DIST') * NEOX_UNIT_SCALE))
        self.plane_forward_dir = None
        self.cur_cam_yaw_offset = 0.0
        self.cur_cam_pitch = DEFAULT_CAM_PITCH
        self.max_cam_pitch_value = radians(conf.get('MAX_CAM_PITCH_VALUE'))
        self.min_cam_pitch_value = -radians(conf.get('MIN_CAM_PITCH_VALUE'))
        self.enter_hor_offset_dist = conf.get('ENTER_HOR_OFFSET_DIST') * NEOX_UNIT_SCALE
        self.enter_ver_offset_dist = conf.get('ENTER_VER_OFFSET_DIST') * NEOX_UNIT_SCALE
        enter_intrp_duration = conf.get('ENTER_INTRP_DURATION')
        loop_hor_offset_dist = conf.get('LOOP_HOR_OFFSET_DIST') * NEOX_UNIT_SCALE
        loop_ver_offset_dist = conf.get('LOOP_VER_OFFSET_DIST') * NEOX_UNIT_SCALE
        exit_hor_offset_dist = conf.get('EXIT_HOR_OFFSET_DIST') * NEOX_UNIT_SCALE
        exit_ver_offset_dist = conf.get('EXIT_VER_OFFSET_DIST') * NEOX_UNIT_SCALE
        exit_intrp_duration = conf.get('EXIT_INTRP_DURATION')
        self.end_offset_dist_info = {INTRP_ENTER: (
                       loop_hor_offset_dist, loop_ver_offset_dist),
           INTRP_EXIT: (
                      exit_hor_offset_dist, exit_ver_offset_dist)
           }
        self.cam_intrp_duration_info = {INTRP_ENTER: enter_intrp_duration,
           INTRP_EXIT: exit_intrp_duration
           }
        self.end_hor_offset_dist = 0.0
        self.end_ver_offset_dist = 0.0
        self.delta_hor_offset_dist = 0.0
        self.delta_ver_offset_dist = 0.0
        self.cam_intrp_state = INTRP_NONE
        self.cur_hor_offset_dist = self.enter_hor_offset_dist
        self.cur_ver_offset_dist = self.enter_ver_offset_dist
        self.cam_intrp_duration = 0.0
        self.cam_intrp_left_time = 0.0
        self.tail_sfx_info = {}
        self.tail_sfx_id_list = {}
        self.mecha_anim_func = {}
        self._space_node_dict = {}
        return

    def destroy(self):
        self.load_model_callback = None
        self.stop_mecha_ready_anim()
        self.ready_anim_track = None
        self.clear_all_space_node()
        for socket_res_agent in six.itervalues(self.socket_res_agents):
            socket_res_agent.destroy()

        for eid, mecha_model in six.iteritems(self.mecha_models):
            for anim_name, func in six.iteritems(self.mecha_anim_func.get(eid, {})):
                mecha_model.unregister_event(func, 'end', anim_name)

            mecha_model and mecha_model.destroy()

        self.mecha_anim_func.clear()
        self.eid_list = []
        self.groupmate_eid_list = []
        self.mecha_models = {}
        self.tail_sfx_info.clear()
        self.tail_sfx_id_list.clear()
        return

    def get_scene(self):
        return self.parent.get_scene()

    def on_load_empty_model_complete(self, data, model, *args):
        scene = self.get_scene()
        if not (scene and scene.valid):
            return
        if not global_data.battle:
            return
        self.mecha_models[self.avatar_eid] = model
        skin_id = data['skin_id']
        shiny_weapon_id = data['shiny_weapon_id']
        scene.add_object(model)
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        if hasattr(model, 'unlimit_socket_obj'):
            model.unlimit_socket_obj(True)
        self.socket_res_agents[self.avatar_eid] = MechaSocketResAgent()
        self.socket_res_agents[self.avatar_eid].load_skin_model_and_effect(model, skin_id, shiny_weapon_id, use_editor_socket_res_data=False)
        decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), [])
        load_model_decal_data(model, skin_id, decal_list, lod_level=data['lod_level'], create_high_quality_decal=True)
        color_dict = global_data.player.get_mecha_color().get(str(skin_id), {})
        load_model_color_data(model, skin_id, color_dict)
        self.check_mecha_model_state()
        self.load_model_callback()

    def _init_specific_parameters_with_mecha_id(self, eid, mecha_id):
        if eid in self.max_mecha_roll_value:
            return
        else:
            mecha_id = str(mecha_id)
            self.fly_speed[eid] = self.max_fly_speed
            self.last_move_dir_x[eid], self.last_move_dir_z[eid] = (0.0, 0.0)
            self.max_mecha_roll_value[eid] = radians(self.max_mecha_roll_value_info.get(mecha_id, self.max_mecha_roll_value_info['default']))
            self.max_mecha_yaw_value[eid] = radians(self.max_mecha_roll_value_info.get(mecha_id, self.max_mecha_roll_value_info['default']))
            self.max_mecha_pitch_value[eid] = radians(self.max_mecha_pitch_value_info.get(mecha_id, self.max_mecha_pitch_value_info['default']))
            self.mecha_rot_intrp_duration[eid] = self.mecha_rot_intrp_duration_info.get(mecha_id, self.mecha_rot_intrp_duration_info['default'])
            self.mecha_rot_intrp_left_time[eid] = [0.0, 0.0]
            self.cur_mecha_roll[eid] = 0.0
            self.max_delta_mecha_roll[eid] = self.delta_mecha_roll[eid] = self.max_mecha_roll_value[eid] / self.mecha_rot_intrp_duration[eid]
            self.target_mecha_roll[eid] = 0.0
            self.cur_mecha_yaw[eid] = 0.0
            self.max_delta_mecha_yaw[eid] = self.delta_mecha_yaw[eid] = self.max_mecha_yaw_value[eid] / self.mecha_rot_intrp_duration[eid]
            self.target_mecha_yaw[eid] = 0.0
            self.cur_mecha_pitch[eid] = 0.0
            self.max_delta_mecha_pitch[eid] = self.delta_mecha_pitch[eid] = self.max_mecha_pitch_value[eid] / self.mecha_rot_intrp_duration[eid]
            self.target_mecha_pitch[eid] = 0.0
            self.specific_parameters_valid[eid] = True
            if global_data.test_launch_boost_tail_sfx is None:
                global_data.test_launch_boost_tail_sfx = ''
            key = global_data.test_launch_boost_tail_sfx
            self.tail_sfx_info[eid] = TAIL_SFX_INFO.get(key, {}).get(mecha_id, {})
            return

    def load_mecha_model(self):
        mecha_id = global_data.player.get_lobby_selected_mecha_id()
        self.ready_anim_name = 'fashe_xin_' + str(mecha_id)
        self._init_specific_parameters_with_mecha_id(self.avatar_eid, mecha_id)
        mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        clothing_id = global_data.player.get_mecha_fashion(mecha_item_id)
        res_path = get_mecha_model_path(mecha_id, clothing_id)
        item_id = get_mecha_skin_item_no(mecha_id, clothing_id)
        shiny_id = get_mecha_skin_shiny_id(item_id)
        mesh_path = get_mecha_model_h_path(mecha_id, clothing_id, shiny_weapon_id=shiny_id)
        data = {'skin_id': clothing_id,'shiny_weapon_id': shiny_id,'lod_level': -1}
        global_data.model_mgr.create_model(res_path, mesh_path_list=[mesh_path], on_create_func=Functor(self.on_load_empty_model_complete, data))

    def on_load_groupmate_empty_model_complete(self, data, model, *args):
        if global_data.cam_lplayer and global_data.cam_lplayer.share_data.ref_parachute_stage not in (STAGE_ISLAND, STAGE_NONE, STAGE_PLANE):
            return
        scene = self.get_scene()
        if not (scene and scene.valid):
            return
        if not global_data.battle:
            return
        eid = data['eid']
        groupmate = EntityManager.getentity(eid)
        if groupmate and groupmate.logic and groupmate.logic.share_data.ref_parachute_stage in (STAGE_ISLAND, STAGE_PLANE):
            self.mecha_models[eid] = model
            skin_id = data['skin_id']
            shiny_weapon_id = data['shiny_weapon_id']
            custom_skin_data = data['custom_skin_data']
            scene.add_object(model)
            model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
            if hasattr(model, 'unlimit_socket_obj'):
                model.unlimit_socket_obj(True)
            socket_res_agent = MechaSocketResAgent()
            self.socket_res_agents[eid] = socket_res_agent
            socket_res_agent.load_skin_model_and_effect(model, skin_id, shiny_weapon_id, use_editor_socket_res_data=False)
            decal_list = custom_skin_data.get('decal', [])
            if decal_list and len(decal_list[0]) < 9:
                decal_list = decode_decal_list(decal_list)
            load_model_decal_data(model, skin_id, decal_list, lod_level=data['lod_level'], create_high_quality_decal=True)
            color_dict = custom_skin_data.get('color', {})
            if color_dict and isinstance(color_dict, dict):
                color_dict = decode_color(color_dict)
            load_model_color_data(model, skin_id, color_dict)
            socket_res_agent.play_animation('fly', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP, 1.0)
            self.tail_sfx_id_list[eid] = []
            for path, sockets in six.iteritems(self.tail_sfx_info[eid]):
                for socket in sockets:
                    self.tail_sfx_id_list[eid].append(global_data.sfx_mgr.create_sfx_on_model(path, model, socket))

            self.check_mecha_model_state()

    def load_groupmate_mecha_model(self):
        from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, get_mecha_model_path, get_mecha_model_lod_path
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
        if global_data.cam_lplayer:
            groupmate_list = global_data.cam_lplayer.ev_g_groupmate()
            for eid in groupmate_list:
                if eid == self.avatar_eid:
                    continue
                if eid in self.mecha_models:
                    if self.mecha_models[eid]:
                        continue
                    if self.mecha_models[eid] is None:
                        continue
                self.mecha_models[eid] = None
                groupmate = EntityManager.getentity(eid)
                if groupmate:
                    self.groupmate_lent[eid] = groupmate.logic
                    if groupmate.logic.share_data.ref_parachute_stage not in (STAGE_ISLAND, STAGE_PLANE):
                        self.mecha_models[eid] = False
                        continue
                    lobby_mecha_id, lobby_mecha_fashion = groupmate.get_lobby_mecha_info()
                    mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_id)
                    self._init_specific_parameters_with_mecha_id(eid, mecha_id)
                    self.groupmate_mecha_last_target_position_offset[eid] = groupmate.share_data.ref_mecha_target_position_offset
                    skin_id = lobby_mecha_fashion['fashion'][FASHION_POS_SUIT]
                    shiny_weapon_id = lobby_mecha_fashion['fashion'].get(FASHION_POS_WEAPON_SFX, -1)
                    data = {'eid': eid,
                       'mecha_id': mecha_id,'skin_id': skin_id,
                       'shiny_weapon_id': shiny_weapon_id,
                       'custom_skin_data': lobby_mecha_fashion.get('custom_skin', {}),
                       'lod_level': 0
                       }
                    res_path = get_mecha_model_path(mecha_id, skin_id)
                    mesh_path = get_mecha_model_lod_path(mecha_id, skin_id, 0, shiny_weapon_id=shiny_weapon_id)
                    global_data.model_mgr.create_model(res_path, mesh_path_list=[mesh_path], on_create_func=Functor(self.on_load_groupmate_empty_model_complete, data))
                else:
                    self.mecha_models[eid] = False

        return

    def check_mecha_model_state(self):
        if self.avatar_eid not in self.mecha_models:
            return
        if not global_data.cam_lplayer:
            return
        player_stage = global_data.cam_lplayer.share_data.ref_parachute_stage
        mecha_visible = player_stage in (STAGE_NONE, STAGE_PLANE, STAGE_PRE_PARACHUTE)
        for eid, mecha_model in six.iteritems(self.mecha_models):
            if mecha_model:
                mecha_model.visible = mecha_visible
                self.socket_res_agents[eid].refresh_res_visible()

        if player_stage in (STAGE_NONE, STAGE_PLANE):
            self.show_rank_on_model()

    def groupmate_mecha_disappear(self, eid):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.share_data.ref_parachute_stage != STAGE_PLANE:
            return
        if eid in self.mecha_models:
            self.clear_eid_space_node(eid)
            if self.mecha_models[eid]:
                self.tail_sfx_id_list[eid] = []

                def delay_hide_model():
                    if eid in self.mecha_models and self.mecha_models[eid] and self.mecha_models[eid].valid:
                        self.mecha_models[eid].visible = False
                        socket_res_agent = self.socket_res_agents.pop(eid)
                        socket_res_agent.destroy()
                        self.mecha_models[eid].destroy()
                        self.mecha_models[eid] = None
                    return

                global_data.sfx_mgr.create_sfx_on_model('effect/fx/robot/robot_01/robot01_call_up.sfx', self.mecha_models[eid], 'fx_zhaohuan')
                global_data.game_mgr.register_logic_timer(delay_hide_model, interval=1.5, times=1, mode=CLOCK)

    def own_mecha_model_loaded(self):
        return self.avatar_eid in self.mecha_models

    def own_mecha_play_fly_animation(self):
        if self.avatar_eid in self.mecha_models:
            own_mecha = self.mecha_models[self.avatar_eid]
            self.socket_res_agents[self.avatar_eid].play_animation('fly', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP, 1.0)
            self.tail_sfx_id_list[self.avatar_eid] = []
            for path, sockets in six.iteritems(self.tail_sfx_info[self.avatar_eid]):
                for socket in sockets:
                    self.tail_sfx_id_list[self.avatar_eid].append(global_data.sfx_mgr.create_sfx_on_model(path, own_mecha, socket))

    def _mecha_ready_ready_anim_tick(self):
        if self.avatar_eid not in self.mecha_models:
            self.ready_anim_timer = -1
            return RELEASE
        anim_ctrl = self.mecha_models[self.avatar_eid].get_anim_ctrl(world.ANIM_TYPE_SKELETAL)
        cur_time = anim_ctrl.get_anim_time(self.ready_anim_name)
        if cur_time >= MECHA_READY_ANIM_DURATION or not anim_ctrl.get_playing(self.ready_anim_name):
            self.ready_anim_timer = -1
            return RELEASE
        cur_trans = self.ready_anim_track.get_transform(cur_time)
        pos = cur_trans.translation
        rot = cur_trans.rotation
        forward = rot.forward
        up = forward.cross(-rot.right)
        cur_trans = math3d.matrix.make_orient(up, rot.forward)
        cur_trans.do_translate(pos)
        cam = world.get_active_scene().active_camera
        cam.world_rotation_matrix = cur_trans.rotation
        cam.world_position = cur_trans.translation + self.ready_anim_initial_position

    def begin_mecha_ready_anim(self, initial_position, rotation_matrix):
        self.ready_anim_initial_position = initial_position
        self.mecha_models[self.avatar_eid].world_position = initial_position
        if rotation_matrix:
            self.mecha_models[self.avatar_eid].world_rotation_matrix = rotation_matrix
        self.socket_res_agents[self.avatar_eid].play_animation(self.ready_anim_name, -1.0, world.TRANSIT_TYPE_DEFAULT, 0.0, world.PLAY_FLAG_DEF_LOOP, 1.0)
        self.stop_mecha_ready_anim()
        self.ready_anim_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self._mecha_ready_ready_anim_tick, interval=1, times=-1)
        self._mecha_ready_ready_anim_tick()

    def stop_mecha_ready_anim(self):
        if self.ready_anim_timer > -1:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.ready_anim_timer)
            self.ready_anim_timer = -1

    def set_cam_delta_yaw_and_pitch(self, delta_yaw, delta_pitch):
        self.cur_cam_yaw_offset += delta_yaw
        self.cur_cam_pitch = clamp(self.cur_cam_pitch + delta_pitch, self.min_cam_pitch_value, self.max_cam_pitch_value)

    def _get_start_offset_dist(self, intrp_state):
        if intrp_state == INTRP_ENTER:
            return (self.enter_hor_offset_dist, self.enter_ver_offset_dist)
        else:
            return (
             self.cur_hor_offset_dist, self.cur_ver_offset_dist)

    def set_cam_intrp_state(self, intrp_state):
        if self.cam_intrp_state == intrp_state:
            return
        if self.cam_intrp_state == INTRP_LOOP and intrp_state == INTRP_ENTER:
            return
        self.cam_intrp_state = intrp_state
        start_hor_offset_dist, start_ver_offset_dist = self._get_start_offset_dist(intrp_state)
        self.end_hor_offset_dist, self.end_ver_offset_dist = self.end_offset_dist_info[intrp_state]
        self.cam_intrp_left_time = self.cam_intrp_duration = self.cam_intrp_duration_info[intrp_state]
        self.delta_hor_offset_dist = (self.end_hor_offset_dist - start_hor_offset_dist) / self.cam_intrp_duration
        self.delta_ver_offset_dist = (self.end_ver_offset_dist - start_ver_offset_dist) / self.cam_intrp_duration

    def on_reconnect(self):
        cam = self.get_scene().active_camera
        if self.plane_forward_dir is not None:
            self.cur_cam_yaw_offset = cam.world_rotation_matrix.yaw - self.plane_forward_dir.yaw
        else:
            self.cur_cam_yaw_offset = 0.0
        self.plane_forward_dir = None
        return

    def _update_avatar_move_dir(self):
        if not global_data.cam_lplayer:
            return
        else:
            share_data = global_data.cam_lplayer.share_data
            move_dir = share_data.ref_rocker_dir
            if move_dir is None:
                move_dir = math3d.vector(0, 0, 0)
            else:
                move_dir *= share_data.ref_rocker_move_dist / share_data.ref_rocker_radius
            self.cur_avatar_move_dir = move_dir
            return

    def _update_avatar_mecha_position_offset(self, dt):
        if not self.specific_parameters_valid.get(self.avatar_eid, False):
            return
        eid = self.avatar_eid
        if eid not in self.mecha_position_offset:
            return
        fly_dist = self.max_fly_speed * dt
        move_dir = self.cur_avatar_move_dir
        self.mecha_position_offset[eid] += move_dir * fly_dist
        mecha_position_offset = self.mecha_position_offset[eid]
        push_move_dir = math3d.vector(0, 0, 0)
        for other_eid in self.groupmate_eid_list:
            if not self.specific_parameters_valid.get(other_eid, False):
                continue
            other_mecha_position_offset = self.mecha_position_offset[other_eid]
            pos_vec = mecha_position_offset - other_mecha_position_offset
            pos_dist = pos_vec.length
            if 0.0 < pos_dist < MECHA_OUTER_RADIUS:
                push_dir = math3d.vector(pos_vec)
                push_dir.normalize()
                if pos_dist < MECHA_INNER_RADIUS:
                    move_dist = MECHA_INNER_RADIUS - pos_dist
                    push_move_dir += push_dir * move_dist
                else:
                    move_dist = MECHA_OUTER_RADIUS - pos_dist
                    push_dist = MECHA_PUSH_SPEED * dt
                    if push_dist <= move_dist:
                        push_move_dir += push_dir * push_dist
                    else:
                        push_move_dir += push_dir * move_dist

        mecha_position_offset.x += push_move_dir.x
        mecha_position_offset.z += push_move_dir.z
        mecha_position_offset.z = clamp(mecha_position_offset.z, -self.fly_zone_back_dist, self.fly_zone_front_dist)
        correspond_zone_width = self.fly_zone_back_width + self.delta_fly_zone_width * (self.fly_zone_back_dist + mecha_position_offset.z)
        mecha_position_offset.x = clamp(mecha_position_offset.x, -correspond_zone_width, correspond_zone_width)
        cur_time_stamp = time.time()
        if cur_time_stamp - self.last_sync_time_stamp >= SYNC_INTERVAL:
            global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (E_SYNC_LAUNCH_BOOST_MECHA_MOVE_DIR, (move_dir.x, move_dir.z)), True)
            global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (E_SYNC_LAUNCH_BOOST_MECHA_POSITION_OFFSET, (mecha_position_offset.x, mecha_position_offset.z)), True)
            self.last_sync_time_stamp = cur_time_stamp
        else:
            need_sync_x, need_sync_z, need_sync_position_offset = False, False, False
            move_dir_x, move_dir_z = move_dir.x, move_dir.z
            last_move_dir_x, last_move_dir_z = self.last_move_dir_x[self.avatar_eid], self.last_move_dir_z[self.avatar_eid]
            if last_move_dir_x != move_dir_x and last_move_dir_x * move_dir_x <= 0.0:
                need_sync_x = True
                if fabs(move_dir_x) < EPSILON:
                    need_sync_position_offset = True
            if last_move_dir_z != move_dir_z and last_move_dir_z * move_dir_z <= 0.0:
                need_sync_z = True
                if fabs(move_dir_z) < EPSILON:
                    need_sync_position_offset = True
            if need_sync_x or need_sync_z or need_sync_position_offset:
                if need_sync_x or need_sync_z:
                    global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (E_SYNC_LAUNCH_BOOST_MECHA_MOVE_DIR, (move_dir.x, move_dir.z)), True)
                if need_sync_position_offset:
                    global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (E_SYNC_LAUNCH_BOOST_MECHA_POSITION_OFFSET, (mecha_position_offset.x, mecha_position_offset.z)), True)
                self.last_sync_time_stamp = cur_time_stamp

    def _update_groupmate_mecha_position_offset(self, dt):
        for index, eid in enumerate(self.groupmate_eid_list):
            if not self.specific_parameters_valid.get(eid, False):
                continue
            groupmate_lent = self.groupmate_lent[eid]
            if not groupmate_lent.is_valid():
                ent = global_data.battle.get_entity(eid)
                if ent and ent.logic and ent.logic.is_valid():
                    groupmate_lent = self.groupmate_lent[eid] = ent.logic
                else:
                    continue
            target_position_offset = groupmate_lent.share_data.ref_mecha_target_position_offset
            if target_position_offset is None:
                target_position_offset = self.initial_position_offset_dist[index]
                groupmate_lent.share_data.ref_mecha_target_position_offset = target_position_offset
                self.groupmate_mecha_last_target_position_offset[eid] = target_position_offset
            move_dir = target_position_offset - self.mecha_position_offset[eid]
            cur_dist = move_dir.length
            if not move_dir.is_zero:
                move_dir.normalize()
            last_target_position_offset = self.groupmate_mecha_last_target_position_offset[eid]
            if last_target_position_offset != target_position_offset:
                self.fly_speed[eid] = min(cur_dist / SYNC_INTERVAL, self.max_fly_speed)
                self.groupmate_mecha_last_target_position_offset[eid] = target_position_offset
            fly_dist = self.fly_speed[eid] * dt
            if cur_dist <= fly_dist:
                self.mecha_position_offset[eid] = target_position_offset
            else:
                self.mecha_position_offset[eid] += move_dir * fly_dist
            self.groupmate_mecha_move_dir[eid] = groupmate_lent.share_data.ref_mecha_move_dir

        return

    def _update_mecha_position_offset(self, dt):
        if not global_data.cam_lplayer:
            return
        if self.cam_intrp_state != INTRP_LOOP:
            return
        self._update_avatar_mecha_position_offset(dt)
        self._update_groupmate_mecha_position_offset(dt)

    def _get_new_target_rot_values(self, eid):
        if eid == self.avatar_eid:
            move_dir = self.cur_avatar_move_dir
            move_dir_x, move_dir_z = move_dir.x, move_dir.z
        else:
            move_dir_x, move_dir_z = self.groupmate_mecha_move_dir.get(eid, (0.0, 0.0))
        if float_equal(move_dir_x, self.last_move_dir_x[eid]) and float_equal(move_dir_z, self.last_move_dir_z[eid]):
            return (self.target_mecha_roll[eid], self.target_mecha_yaw[eid], self.target_mecha_pitch[eid])
        else:
            max_mecha_roll_value = self.max_mecha_roll_value[eid]
            max_mecha_yaw_value = self.max_mecha_yaw_value[eid]
            max_mecha_pitch_value = self.max_mecha_pitch_value[eid]
            if global_data.debug_launch_boost_param:
                if global_data.max_mecha_roll_value is not None:
                    max_mecha_roll_value = radians(global_data.max_mecha_roll_value)
                if global_data.max_mecha_yaw_value is not None:
                    max_mecha_yaw_value = radians(global_data.max_mecha_yaw_value)
                if global_data.max_mecha_pitch_value is not None:
                    max_mecha_pitch_value = radians(global_data.max_mecha_pitch_value)
            if fabs(move_dir_x) < EPSILON or global_data.cam_lplayer.share_data.ref_parachute_stage != STAGE_PLANE:
                new_mecha_target_roll = 0.0
                new_mecha_target_yaw = 0.0
            else:
                new_mecha_target_roll = -max_mecha_roll_value * move_dir_x
                new_mecha_target_yaw = max_mecha_yaw_value * move_dir_x
            if fabs(move_dir_z) < EPSILON or global_data.cam_lplayer.share_data.ref_parachute_stage != STAGE_PLANE:
                new_mecha_target_pitch = 0.0
            else:
                new_mecha_target_pitch = max_mecha_pitch_value * move_dir_z
            return (new_mecha_target_roll, new_mecha_target_yaw, new_mecha_target_pitch)

    def _get_delta_rotation_values(self, eid):
        if global_data.debug_launch_boost_param:
            if global_data.max_mecha_roll_value is not None:
                max_mecha_roll_value = radians(global_data.max_mecha_roll_value)
            else:
                max_mecha_roll_value = self.max_mecha_roll_value[eid]
            if global_data.max_mecha_yaw_value is not None:
                max_mecha_yaw_value = radians(global_data.max_mecha_yaw_value)
            else:
                max_mecha_yaw_value = self.max_mecha_yaw_value[eid]
            if global_data.max_mecha_pitch_value is not None:
                max_mecha_pitch_value = radians(global_data.max_mecha_pitch_value)
            else:
                max_mecha_pitch_value = self.max_mecha_pitch_value[eid]
            if global_data.mecha_rot_intrp_duration is not None:
                mecha_rot_intrp_duration = global_data.mecha_rot_intrp_duration
            else:
                mecha_rot_intrp_duration = self.mecha_rot_intrp_duration[eid]
            return (max_mecha_roll_value / mecha_rot_intrp_duration, max_mecha_yaw_value / mecha_rot_intrp_duration, max_mecha_pitch_value / mecha_rot_intrp_duration)
        else:
            return (
             self.delta_mecha_roll[eid], self.delta_mecha_yaw[eid], self.delta_mecha_pitch[eid])
            return

    def _interpolate_mecha_rotation(self, dt, eid, delta_mecha_roll, delta_mecha_yaw, delta_mecha_pitch):
        if self.mecha_rot_intrp_left_time[eid][0] > 0.0:
            if self.mecha_rot_intrp_left_time[eid][0] > dt:
                self.mecha_rot_intrp_left_time[eid][0] -= dt
                self.cur_mecha_roll[eid] = get_intrp_result(self.cur_mecha_roll[eid], self.target_mecha_roll[eid], delta_mecha_roll * dt)
                self.cur_mecha_yaw[eid] = get_intrp_result(self.cur_mecha_yaw[eid], self.target_mecha_yaw[eid], delta_mecha_yaw * dt)
            else:
                self.mecha_rot_intrp_left_time[eid][0] = 0.0
                self.cur_mecha_roll[eid] = self.target_mecha_roll[eid]
                self.cur_mecha_yaw[eid] = self.target_mecha_yaw[eid]
        if self.mecha_rot_intrp_left_time[eid][1] > 0.0:
            if self.mecha_rot_intrp_left_time[eid][1] > dt:
                self.mecha_rot_intrp_left_time[eid][1] -= dt
                self.cur_mecha_pitch[eid] = get_intrp_result(self.cur_mecha_pitch[eid], self.target_mecha_pitch[eid], delta_mecha_pitch * dt)
            else:
                self.mecha_rot_intrp_left_time[eid][1] = 0.0
                self.cur_mecha_pitch[eid] = self.target_mecha_pitch[eid]

    def _update_avatar_mecha_rotation_offset(self, dt):
        eid = self.avatar_eid
        if not self.specific_parameters_valid.get(eid, False):
            return
        new_mecha_target_roll, new_mecha_target_yaw, new_mecha_target_pitch = self._get_new_target_rot_values(eid)
        delta_mecha_roll, delta_mecha_yaw, delta_mecha_pitch = self._get_delta_rotation_values(eid)
        if new_mecha_target_roll != self.target_mecha_roll[eid]:
            self.mecha_rot_intrp_left_time[eid][0] = get_intrp_duration(self.cur_mecha_roll[eid], new_mecha_target_roll, delta_mecha_roll)
            self.target_mecha_roll[eid] = new_mecha_target_roll
        if new_mecha_target_yaw != self.target_mecha_yaw[eid]:
            self.mecha_rot_intrp_left_time[eid][0] = get_intrp_duration(self.cur_mecha_yaw[eid], new_mecha_target_yaw, delta_mecha_yaw)
            self.target_mecha_yaw[eid] = new_mecha_target_yaw
        if new_mecha_target_pitch != self.target_mecha_pitch[eid]:
            self.mecha_rot_intrp_left_time[eid][1] = get_intrp_duration(self.cur_mecha_pitch[eid], new_mecha_target_pitch, delta_mecha_pitch)
            self.target_mecha_pitch[eid] = new_mecha_target_pitch
        self._interpolate_mecha_rotation(dt, eid, delta_mecha_roll, delta_mecha_yaw, delta_mecha_pitch)

    def _update_groupmate_mecha_rotation_offset(self, dt):
        for eid in self.groupmate_eid_list:
            if not self.specific_parameters_valid.get(eid, False):
                continue
            new_mecha_target_roll, new_mecha_target_yaw, new_mecha_target_pitch = self._get_new_target_rot_values(eid)
            delta_mecha_roll, delta_mecha_yaw, delta_mecha_pitch = self._get_delta_rotation_values(eid)
            if new_mecha_target_roll != self.target_mecha_roll[eid]:
                delta_mecha_roll = min(fabs(new_mecha_target_roll - self.cur_mecha_roll[eid]) / SYNC_INTERVAL, self.max_delta_mecha_roll[eid])
                self.delta_mecha_roll[eid] = delta_mecha_roll
                self.mecha_rot_intrp_left_time[eid][0] = get_intrp_duration(self.cur_mecha_roll[eid], new_mecha_target_roll, delta_mecha_roll)
                self.target_mecha_roll[eid] = new_mecha_target_roll
            if new_mecha_target_yaw != self.target_mecha_yaw[eid]:
                delta_mecha_yaw = min(fabs(new_mecha_target_yaw - self.cur_mecha_yaw[eid]) / SYNC_INTERVAL, self.max_delta_mecha_yaw[eid])
                self.delta_mecha_yaw[eid] = delta_mecha_yaw
                self.mecha_rot_intrp_left_time[eid][0] = get_intrp_duration(self.cur_mecha_yaw[eid], new_mecha_target_yaw, delta_mecha_yaw)
                self.target_mecha_yaw[eid] = new_mecha_target_yaw
            if new_mecha_target_pitch != self.target_mecha_pitch[eid]:
                delta_mecha_pitch = min(fabs(new_mecha_target_pitch - self.cur_mecha_pitch[eid]) / SYNC_INTERVAL, self.max_delta_mecha_pitch[eid])
                self.delta_mecha_pitch[eid] = delta_mecha_pitch
                self.mecha_rot_intrp_left_time[eid][1] = get_intrp_duration(self.cur_mecha_pitch[eid], new_mecha_target_pitch, delta_mecha_pitch)
                self.target_mecha_pitch[eid] = new_mecha_target_pitch
            self._interpolate_mecha_rotation(dt, eid, delta_mecha_roll, delta_mecha_yaw, delta_mecha_pitch)

    def _update_mecha_rotation_offset(self, dt):
        self._update_avatar_mecha_rotation_offset(dt)
        self._update_groupmate_mecha_rotation_offset(dt)

    def _update_last_move_dir(self):
        self.last_move_dir_x[self.avatar_eid], self.last_move_dir_z[self.avatar_eid] = self.cur_avatar_move_dir.x, self.cur_avatar_move_dir.z
        for eid in self.groupmate_eid_list:
            self.last_move_dir_x[eid], self.last_move_dir_z[eid] = self.groupmate_mecha_move_dir.get(eid, (0.0,
                                                                                                           0.0))

    def _update_cam_position_offset(self, dt):
        if self.cam_intrp_left_time > 0.0:
            if self.cam_intrp_left_time > dt:
                self.cam_intrp_left_time -= dt
                self.cur_hor_offset_dist += self.delta_hor_offset_dist * dt
                self.cur_ver_offset_dist += self.delta_ver_offset_dist * dt
            else:
                self.cam_intrp_left_time = 0.0
                self.cur_hor_offset_dist = self.end_hor_offset_dist
                self.cur_ver_offset_dist = self.end_ver_offset_dist
                self.cam_intrp_state = (self.cam_intrp_state + 1) % INTRP_STATE_COUNT

    def update(self, camera, forward, position, dt):
        plane_forward_refreshed = False
        if self.plane_forward_dir != forward:
            if not self.eid_list:
                eid_list = global_data.cam_lplayer.ev_g_groupmate()
                if len(eid_list) > 3:
                    import exception_hook
                    err_msg = 'groupmate_data length larger than 3 !!!' + str(eid_list)
                    exception_hook.post_error(err_msg)
                    return (
                     position, camera.world_rotation_matrix, camera.world_position)
                self.eid_list = eid_list
                self.groupmate_eid_list = list(self.eid_list)
                if self.avatar_eid in self.groupmate_eid_list:
                    self.groupmate_eid_list.remove(self.avatar_eid)
                global_data.cam_lplayer.send_event('E_TRY_CANCEL_RUN_LOCK')
                global_data.cam_lplayer.send_event('E_FORBID_RUN_LOCK', True)
                for index, eid in enumerate(self.eid_list):
                    self.mecha_position_offset[eid] = math3d.vector(self.initial_position_offset_dist[index])

                avatar_mecha_position_offset = self.mecha_position_offset[self.avatar_eid]
                global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (E_SYNC_LAUNCH_BOOST_MECHA_POSITION_OFFSET, (avatar_mecha_position_offset.x, avatar_mecha_position_offset.z)), True)
            plane_forward_refreshed = True
            self.plane_forward_dir = forward
        mat = math3d.matrix.make_orient(forward, UP_VECTOR)
        right = mat.right
        self._update_avatar_move_dir()
        self._update_mecha_position_offset(dt)
        self._update_mecha_rotation_offset(dt)
        self._update_last_move_dir()
        need_load_groupmate_mecha_models = False
        avatar_mecha_position = None
        for eid in self.eid_list:
            if not self.mecha_models[eid]:
                if self.mecha_models[eid] is not None and eid != self.avatar_eid:
                    need_load_groupmate_mecha_models = True
                continue
            mecha_position = position + forward * self.mecha_position_offset[eid].z + right * self.mecha_position_offset[eid].x
            self.mecha_models[eid].world_position = mecha_position
            if eid == self.avatar_eid:
                avatar_mecha_position = mecha_position
            mecha_rotation_matrix = mat
            rot_yaw = math3d.rotation(0, 0, 0, 1)
            rot_yaw.set_axis_angle(UP_VECTOR, self.cur_mecha_yaw[eid])
            mecha_rotation_matrix *= math3d.rotation_to_matrix(rot_yaw)
            rot_roll = math3d.rotation(0, 0, 0, 1)
            rot_roll.set_axis_angle(mecha_rotation_matrix.forward, self.cur_mecha_roll[eid])
            mecha_rotation_matrix *= math3d.rotation_to_matrix(rot_roll)
            rot_roll = math3d.rotation(0, 0, 0, 1)
            rot_roll.set_axis_angle(right, self.cur_mecha_pitch[eid])
            mecha_rotation_matrix *= math3d.rotation_to_matrix(rot_roll)
            self.mecha_models[eid].world_rotation_matrix = mecha_rotation_matrix

        if need_load_groupmate_mecha_models:
            self.load_groupmate_mecha_model()
        cur_mat = camera.world_rotation_matrix
        if plane_forward_refreshed:
            yaw_mat = mat
            right = mat.right
        else:
            yaw_mat = math3d.matrix.make_rotation_y(self.cur_cam_yaw_offset + cur_mat.yaw)
            right = yaw_mat.right
            self.cur_cam_yaw_offset = 0
        pitch_mat = math3d.matrix.make_rotation(right, self.cur_cam_pitch)
        new_mat = yaw_mat * pitch_mat
        camera.world_rotation_matrix = new_mat
        cam_pos = position
        self._update_cam_position_offset(dt)
        new_forward = new_mat.forward
        cam_pos += math3d.vector(0, self.cur_ver_offset_dist, 0) - new_forward * self.cur_hor_offset_dist
        if self.cam_intrp_state == INTRP_EXIT:
            cam_pos += (avatar_mecha_position - position) * (1.0 - self.cam_intrp_left_time / self.cam_intrp_duration)
        camera.world_position = cam_pos
        return (
         avatar_mecha_position, new_mat, cam_pos)

    def play_fly_animation(self, model, eid):
        self.socket_res_agents[eid].play_animation('fly', -1, world.TRANSIT_TYPE_DELAY, 0, world.PLAY_FLAG_LOOP, 1.0)
        self.tail_sfx_id_list[eid] = []
        for path, sockets in six.iteritems(self.tail_sfx_info[eid]):
            for socket in sockets:
                self.tail_sfx_id_list[eid].append(global_data.sfx_mgr.create_sfx_on_model(path, model, socket))

    def _register_end_anim_event(self, model, eid, anim_name):
        if eid not in self.mecha_anim_func:
            self.mecha_anim_func[eid] = {}
        if anim_name not in self.mecha_anim_func[eid]:
            func = lambda *args: self.play_fly_animation(model, eid)
            model.register_anim_key_event(anim_name, 'end', func)
            self.mecha_anim_func[eid][anim_name] = func

    def test_fly_emote(self, emote_anim_name):
        mecha_model = self.mecha_models.get(self.avatar_eid)
        if mecha_model:
            if mecha_model.cur_anim_name != 'fly':
                return
            for sfx_id in self.tail_sfx_id_list.get(self.avatar_eid, []):
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

            self.tail_sfx_id_list[self.avatar_eid] = []
            self.socket_res_agents[self.avatar_eid].play_animation(emote_anim_name, -1.0, world.TRANSIT_TYPE_DELAY, 0, world.PLAY_FLAG_NO_LOOP, 1.0)
            self._register_end_anim_event(mecha_model, self.avatar_eid, emote_anim_name)

    def show_rank_on_model(self):
        mecha_model_dict = self.mecha_models
        for eid, model in six.iteritems(mecha_model_dict):
            if not model:
                continue
            if eid not in self._space_node_dict:
                self.check_show_rank_title_on_model(eid, model)

    def check_show_rank_title_on_model(self, eid, model):
        rank_use_title_dict = {}
        if str(eid) == str(global_data.player.id):
            rank_use_title_dict = global_data.player.rank_use_title_dict
        elif global_data.cam_lplayer:
            infos = global_data.cam_lplayer.ev_g_teammate_infos()
            rank_use_title_dict = infos.get(eid, {}).get('rank_use_title_dict', {})
        if rank_use_title_dict:
            from logic.gutils.template_utils import init_rank_title
            from logic.gcommon.common_const import rank_const
            from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
            space_node = CCUISpaceNode.Create()
            space_node.set_enable_limit_in_screen(False, 0, 0, 0, 0)
            nd_title = global_data.uisystem.load_template_create('title/i_title_normal_2', parent=space_node, name='nd_title')
            nd_title.img_icon.setScale(0.85)
            rank_title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
            rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
            init_rank_title(nd_title, rank_title_type, rank_info)
            xuetiao_pos = model.get_socket_matrix('xuetiao', world.SPACE_TYPE_WORLD)
            if xuetiao_pos:
                space_node.set_assigned_world_pos(xuetiao_pos.translation)
                space_node.bind_model(model, 'xuetiao')

            def vis_callback(last_need_draw, cur_need_draw):
                if nd_title and nd_title.isValid():
                    nd_title.setVisible(True if cur_need_draw else False)

            space_node.set_visible_callback(vis_callback)
            self._space_node_dict[eid] = space_node
        else:
            self._space_node_dict[eid] = None
        return

    def clear_all_space_node(self):
        for space_node in six.itervalues(self._space_node_dict):
            if space_node:
                space_node.Destroy()

        self._space_node_dict = {}

    def clear_eid_space_node(self, eid):
        if eid in self._space_node_dict:
            nd = self._space_node_dict.get(eid, None)
            if nd:
                nd.Destroy()
            del self._space_node_dict[eid]
        return