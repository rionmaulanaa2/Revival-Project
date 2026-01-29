# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPrivilegeLobby.py
from __future__ import absolute_import
import six
from six.moves import range
import math
from . import ScenePart
from logic.gcommon.item import item_const as iconst
from logic.gutils.ConnectHelper import ConnectHelper
from common.cfg import confmgr
import math3d
import game3d
import world
from ext_package.ext_decorator import has_skin_ext
from logic.manager_agents.manager_decorators import sync_exec
import random
import common.utils.timer as timer
VAR_HASH_NAME = game3d.calc_string_hash('Tex0')
VAR_NAME = 'Tex0'
ENV_DICT = {'-1': 'dating',
   '208000001': 'dating_privilege'
   }
spring_festival_sky_box = '208000003'
FIREWORKS_CN = [
 'effect/fx/scenes/common/dating/dt_firework_happynewyear.sfx',
 'effect/fx/scenes/common/dating/dt_firework_happysmc.sfx',
 'effect/fx/scenes/common/dating/dt_firework_logo.sfx']
FIREWORKS_NA = [
 'effect/fx/scenes/common/dating/dt_firework_happysmc.sfx',
 'effect/fx/scenes/common/dating/dt_firework_logo.sfx']
COMMON_FIREWORK = 'effect/fx/scenes/common/chunjie/chunjie_yanhua_beijing_short.sfx'
FIREWORKS_INTERVAL = (0.7, 3)
FIREWORKS_DISTANCE = (1000, 3000)
FIREWORKS_RADIAN = 0.7 * math.pi
FIREWORKS_HEIGHT = (-200, 1300)

class PartPrivilegeLobby(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartPrivilegeLobby, self).__init__(scene, name)
        self.is_load = False
        self.data = confmgr.get('privilege_scene_data', default={})
        self.model_list = {}
        self.sfx_list = {}
        self.sfx_id_list = {}
        self.lobby_style = -1
        self.is_show_suneffect = True
        self.fireworks_timer = None
        return

    def on_enter(self):
        self.set_privilege_lobby_state(0)
        global_data.emgr.privilege_lobby_skin_change += self.set_privilege_lobby_state
        global_data.emgr.privilege_lobby_skin_change_force += self.set_privilege_lobby_state_force
        global_data.emgr.player_leave_visit_scene_event += self.on_leave_scene
        global_data.emgr.player_enter_visit_scene_event += self.on_enter_scene
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def on_load(self):
        self.is_load = True

    def set_privilege_lobby_state(self, item_no=0):
        if not global_data.player:
            return
        if item_no == 0:
            is_in_visit_mode = global_data.player.is_in_visit_mode()
            if is_in_visit_mode:
                cur_lobby_style = global_data.player.get_visit_lobby_skybox_id()
            else:
                cur_lobby_style = global_data.player.get_lobby_skybox_id()
            self.change_scenes(cur_lobby_style)
        else:
            self.change_scenes(item_no)

    def set_privilege_lobby_state_force(self, item_no):
        if not global_data.player or item_no is None:
            return
        else:
            self.change_scenes(item_no, True)
            return

    def on_enter_scene(self, *args):
        self.set_privilege_lobby_state(0)

    def on_leave_scene(self, *args):
        self.set_privilege_lobby_state(0)

    def change_scenes(self, style_idx, is_force=False):
        if style_idx == 0:
            style_idx = -1
        if self.lobby_style == style_idx:
            return
        self.change_scenes_model(style_idx)
        self.change_scenes_sfx(style_idx)
        self.change_scenes_skybox(style_idx)
        if str(style_idx) == spring_festival_sky_box:
            self.play_fireworks()
        else:
            self.stop_fireworks()
        self.lobby_style = style_idx

    def change_scenes_model(self, style_idx):
        mirror = self.get_scene().get_com('PartMirror')
        old_style_model = self.model_list.get(str(self.lobby_style), [])
        for model in old_style_model:
            if model and model.valid:
                model.visible = False
                if mirror:
                    mirror.set_model_visible_from_mirror(model, False)

        new_style_model = self.model_list.get(str(style_idx), [])
        if not new_style_model:
            self.model_list[str(style_idx)] = []
            new_style_model_infos = self.data.get('model', {}).get(str(style_idx), [])
            for idx in range(len(new_style_model_infos)):
                model_info = new_style_model_infos[idx]
                if model_info.get('not_show', None) and not has_skin_ext():
                    continue

                def create_cb(model, model_info=model_info, lobby_style=style_idx, *args):
                    model.scale = math3d.vector(*model_info.get('scale', [1, 1, 1]))
                    rot = model_info.get('rot', [0.0, 0.0, 0.0])
                    model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(rot[0] / 180.0 * math.pi, rot[1] / 180.0 * math.pi, rot[2] / 180.0 * math.pi))
                    self.model_list[str(lobby_style)].append(model)
                    if mirror:
                        mirror.add_model_to_mirror(model)

                model_path = model_info.get('src_path', '')
                model_pos = math3d.vector(*model_info.get('pos', [0, 0, 0]))
                global_data.model_mgr.create_model_in_scene(model_path, model_pos, on_create_func=create_cb, create_scene=self.get_scene())

        else:
            for model in new_style_model:
                if model and model.valid:
                    model.visible = True
                    if mirror:
                        mirror.set_model_visible_from_mirror(model, True)

        return

    def change_scenes_sfx(self, style_idx):
        mirror = self.get_scene().get_com('PartMirror')
        old_style_sfx = self.sfx_list.get(str(self.lobby_style), [])
        for sfx in old_style_sfx:
            if mirror:
                mirror.remove_sfx_from_mirror(sfx)
            global_data.sfx_mgr.remove_sfx(sfx)

        self.sfx_list[str(self.lobby_style)] = []
        self.sfx_id_list[str(self.lobby_style)] = []
        new_style_sfx = self.sfx_list.get(str(style_idx), [])
        if not new_style_sfx:
            self.sfx_list[str(style_idx)] = []
            self.sfx_id_list[str(style_idx)] = []
            new_style_sfx_infos = self.data.get('sfx', {}).get(str(style_idx), [])
            for idx in range(len(new_style_sfx_infos)):
                sfx_info = new_style_sfx_infos[idx]
                if sfx_info.get('not_show', None) and not has_skin_ext():
                    continue

                def create_cb(sfx, sfx_info=sfx_info, lobby_style=style_idx):
                    sfx.scale = math3d.vector(*sfx_info.get('scale', [1, 1, 1]))
                    rot = sfx_info.get('rot', [0, 0, 0])
                    sfx.rotation_matrix = math3d.euler_to_matrix(math3d.vector(rot[0] / 180 * math.pi, rot[1] / 180 * math.pi, rot[2] / 180 * math.pi))
                    mirror.add_sfx_from_mirror(sfx)
                    self.sfx_list[str(style_idx)].append(sfx)

                sfx_path = sfx_info.get('src_path', '')
                sfx_pos = math3d.vector(*sfx_info.get('pos', [0, 0, 0]))
                sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_pos, on_create_func=create_cb, create_scene=self.get_scene())
                self.sfx_id_list[str(style_idx)].append(sfx_id)

        return

    @sync_exec
    def change_scenes_skybox(self, style_idx):
        sky_box_xml = self.data.get('skybox', {}).get(str(style_idx), '')
        if not sky_box_xml:
            log_error('has no skybox xml')
            return
        scn = self.get_scene()
        if not scn or not scn.valid:
            log_error('scene is not exist')
            return
        env_path = sky_box_xml[0]['src_path']
        scn.load_env_new(env_path)
        conf_name = scn._get_scene_data('light_config')
        scn.setup_env_light_info(conf_name, 'on_ground', True)
        mirror = scn.get_com('PartMirror')
        if mirror:
            mirror.update_mirror_env(env_path, 'dating')
        if str(style_idx) != '-1':
            self.is_show_suneffect = False
            global_data.emgr.update_suneffect_state.emit(False)
        else:
            self.is_show_suneffect = True
            global_data.emgr.update_suneffect_state.emit(True)

    def get_suneffect_state(self):
        return self.is_show_suneffect

    def get_model_list(self):
        return self.model_list

    def get_lobby_style(self):
        return str(self.lobby_style)

    def remove_sfx(self):
        if self.sfx_id_list:
            for lobby_style, sfx_info in six.iteritems(self.sfx_id_list):
                for sfx_id in sfx_info:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_id_list = {}
        self.sfx_list = {}

    def on_exit(self):
        self.stop_fireworks()
        self.remove_sfx()
        global_data.emgr.privilege_lobby_skin_change_force -= self.set_privilege_lobby_state_force
        global_data.emgr.privilege_lobby_skin_change -= self.set_privilege_lobby_state
        global_data.emgr.player_leave_visit_scene_event -= self.on_leave_scene
        global_data.emgr.player_enter_visit_scene_event -= self.on_enter_scene
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect

    def play_sfx(self):
        lplayer = global_data.lobby_player
        if not lplayer:
            return
        lobby_player_pos = lplayer.ev_g_position()
        if not lobby_player_pos:
            lobby_player_pos = math3d.vector(0.0, 0.0, 0.0)
        if G_IS_NA_PROJECT:
            fireworks = FIREWORKS_NA
        else:
            fireworks = FIREWORKS_CN
        distance = FIREWORKS_DISTANCE[0] + random.random() * FIREWORKS_DISTANCE[1]
        scn = self.scene()
        camera_yaw = scn.active_camera.world_rotation_matrix.yaw
        r = camera_yaw + (random.random() - 0.5) * FIREWORKS_RADIAN
        height = FIREWORKS_HEIGHT[0] + random.random() * FIREWORKS_HEIGHT[1]
        x_offset = math.sin(r) * distance
        y_offset = math.cos(r) * distance
        pos = lobby_player_pos + math3d.vector(x_offset, height, y_offset)
        sfx_index = random.randint(0, len(fireworks) - 1)

        def create_cb(sfx):
            sfx.world_rotation_matrix = math3d.matrix.make_rotation_y(r)
            sfx.scale = math3d.vector(1.0, 1.0, 1.0)

        global_data.sfx_mgr.create_sfx_in_scene(fireworks[sfx_index], pos, on_create_func=create_cb, create_scene=scn)
        pos1 = lobby_player_pos + math3d.vector(x_offset, height - 800, y_offset)

        def create_cb1(sfx):
            sfx.scale = math3d.vector(10.0, 10.0, 10.0)
            sfx.world_rotation_matrix = math3d.matrix.make_rotation_y(r)

        global_data.sfx_mgr.create_sfx_in_scene(COMMON_FIREWORK, pos1, on_create_func=create_cb1, create_scene=scn)

    def delay_random_lobby_fireworks(self):

        def callback():
            self.delay_random_lobby_fireworks()
            self.play_sfx()

        interval = FIREWORKS_INTERVAL[0] + random.random() * FIREWORKS_INTERVAL[1]
        self.fireworks_timer = global_data.game_mgr.register_logic_timer(callback, interval=interval, times=1, mode=timer.CLOCK)

    def on_login_reconnect(self):
        if self.lobby_style == spring_festival_sky_box:
            self.play_fireworks()

    def play_fireworks(self):
        if self.fireworks_timer:
            global_data.game_mgr.unregister_logic_timer(self.fireworks_timer)
            self.fireworks_timer = None
        self.delay_random_lobby_fireworks()
        return

    def stop_fireworks(self):
        if self.fireworks_timer:
            global_data.game_mgr.unregister_logic_timer(self.fireworks_timer)
            self.fireworks_timer = None
        return