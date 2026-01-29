# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSpringFestival.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from . import ScenePart
from common.cfg import confmgr
import game3d
import C_file
import math
import random
import common.utils.timer as timer
import math3d
from logic.gcommon.common_const import collision_const
import collision
_HASH_Tex0 = game3d.calc_string_hash('Tex0')
_HASH_Tex12 = game3d.calc_string_hash('Tex12')
_HASH_NormalMap = game3d.calc_string_hash('NormalMap')
VAR_NAME = ('Tex0', 'Tex12', 'NormalMap')
VAR_NAME_HASH = (_HASH_Tex0, _HASH_Tex12, _HASH_NormalMap)
TEXTURE_MAP = {'dt_building_diji_01': [
                         ('dt_building_diji_01_4', '01_b', '01_m', '01_n'),
                         ('dt_building_diji_01_1', '08_b')],
   'dt_prop_zhuzi_01': [
                      ('dt_prop_zhuzi_01_0', '02_b', '02_m', '02_n')],
   'dt_building_diji_02': [
                         ('dt_building_diji_020', '03_b', '03_m', '03_n')],
   'dt_prop_zhanshitai_03': [
                           ('dt_prop_zhanshitai_030', '06_b')]
   }
MODEL_NAME_MAP = {'dt_prop_zhanshitai_03': [
                           'dt_prop_zhanshitai_03_03',
                           'dt_prop_zhanshitai_03_01',
                           'dt_prop_zhanshitai_03',
                           'dt_prop_zhanshitai_03_02'],
   'dt_prop_zhuzi_01': [
                      'dt_prop_zhuzi_01',
                      'dt_prop_zhuzi_01_01'],
   'dt_building_diji_01': [
                         'dt_building_diji_01'],
   'dt_building_diji_02': [
                         'dt_building_diji_02']
   }
EXTRA_MODELS = ('model_new\\xuanjue\\new_dating_cj\\zhujiemian_cj_denglong01.gim',
                'model_new\\xuanjue\\new_dating_cj\\zhujiemian_cj_tiehua01.gim')
PIC_HEAD = 'model_new/miaomiaoxitong/%s/%s_%s.tga'
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

class PartSpringFestival(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartSpringFestival, self).__init__(scene, name)
        self.mianmiao_style_index = 0
        self.mianmiao_style_name = 'dating_chunjie'
        self.replace_texture_delay_exec = None
        self.replace_model_map = {}
        self.need_replace_models = []
        self.is_load = False
        self.save_default_texture_maps = {}
        for model_name, scene_model_names in six.iteritems(MODEL_NAME_MAP):
            for scene_model_name in scene_model_names:
                self.replace_model_map[scene_model_name] = TEXTURE_MAP.get(model_name)

        self.fireworks_timer = None
        self.camera_yaw = 0.0
        self.extra_models = []
        self.extra_model_cols = []
        self.inside_enable = False
        self.outside_enable = False
        return

    def on_enter(self):
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.spring_festival_inside_skin_enable += self.set_spring_festival_inside_skin_enable
        global_data.emgr.spring_festival_outside_skin_enable += self.set_spring_festival_outside_skin_enable

    def on_pause(self, flag):
        if self.outside_enable:
            if flag:
                self.stop_fireworks()
            else:
                self.play_fireworks()

    def on_load(self):
        self.is_load = True
        part_privilege_lobby = self.scene().get_com('PartPrivilegeLobby')
        if part_privilege_lobby and part_privilege_lobby.get_lobby_style() == '-1':
            self.set_spring_festival_outside_skin_enable(True)
        part_miaomiao_dating = self.scene().get_com('PartMiaoMiaoDating')
        if part_miaomiao_dating and part_miaomiao_dating.get_mianmiao_style_index() == 0:
            self.set_spring_festival_inside_skin_enable(True)

    def set_spring_festival_inside_skin_enable(self, enable):
        if enable:
            self.replace_texture()
        else:
            self.reset_texture()
        if enable and not self.inside_enable:
            self.add_extra_model()
            self.inside_enable = True
        elif not enable and self.inside_enable:
            self.clear_extra_model()
            self.inside_enable = False

    def set_spring_festival_outside_skin_enable(self, enable):
        if enable:
            self.replace_skybox()
        if enable and not self.outside_enable:
            self.play_fireworks()
            self.outside_enable = True
        elif not enable and self.outside_enable:
            self.stop_fireworks()
            self.outside_enable = False

    def on_enter_scene(self, *args):
        pass

    def on_leave_scene(self, *args):
        pass

    def replace_texture(self):
        self.need_replace_models = six_ex.keys(self.replace_model_map)
        need_save_default_map = not self.save_default_texture_maps
        scn = self.scene()
        save_model_names = []
        for model_name in self.need_replace_models:
            datas = self.replace_model_map.get(model_name)
            for data in datas:
                model = scn.get_model(model_name)
                if model:
                    material = model.get_sub_material(data[0])
                    for index in range(len(data) - 1):
                        texture_name = PIC_HEAD % (self.mianmiao_style_name, self.mianmiao_style_name, data[index + 1])
                        if need_save_default_map:
                            key = model_name + data[0] + str(index)
                            self.save_default_texture_maps[key] = material.get_texture(VAR_NAME_HASH[index], VAR_NAME[index])
                        if not self.check_res_file(texture_name):
                            key = model_name + data[0] + str(index)
                            texture_name = self.save_default_texture_maps[key]
                        if texture_name:
                            material.set_texture(VAR_NAME_HASH[index], VAR_NAME[index], texture_name)

                else:
                    save_model_names.append(model_name)

    def reset_texture(self):
        if not self.save_default_texture_maps:
            return
        scn = self.scene()
        save_model_names = []
        for model_name in self.need_replace_models:
            datas = self.replace_model_map.get(model_name)
            for data in datas:
                model = scn.get_model(model_name)
                if model:
                    material = model.get_sub_material(data[0])
                    for index in range(len(data) - 1):
                        key = model_name + data[0] + str(index)
                        texture_name = self.save_default_texture_maps[key]
                        if texture_name:
                            material.set_texture(VAR_NAME_HASH[index], VAR_NAME[index], texture_name)

                else:
                    save_model_names.append(model_name)

        self.need_replace_models = save_model_names

    def add_extra_model(self):
        for model_path in EXTRA_MODELS:

            def callback(model):
                model.receive_shadow = True
                model.cast_shadow = True
                scn = self.scene()
                mask = collision_const.TERRAIN_MASK
                group = collision_const.TERRAIN_GROUP
                col = collision.col_object(collision.MESH, model, mask, group, 0, True)
                col.position = model.position
                col.rotation_matrix = model.rotation_matrix
                scn.scene_col.add_object(col)
                self.extra_model_cols.append(col)

            model_id = global_data.model_mgr.create_model_in_scene(model_path, math3d.vector(0, 0, 0), on_create_func=callback, create_scene=self.get_scene())
            if model_id:
                self.extra_models.append(model_id)

    def clear_extra_model(self):
        for model_id in self.extra_models:
            if model_id:
                global_data.model_mgr.remove_model_by_id(model_id)

        self.extra_models = []
        scn = self.scene()
        for col in self.extra_model_cols:
            scn.scene_col.remove_object(col)

        self.extra_model_cols = []

    def check_res_file(self, texture_name):
        if C_file.find_res_file(texture_name, '') == 1:
            return True
        if C_file.find_res_file(texture_name.replace('.tga', '.ktx'), '') == 1:
            return True
        if C_file.find_res_file(texture_name.replace('.tga', '.dds'), '') == 1:
            return True
        return False

    def replace_skybox(self):
        return
        sky_box_xml = 'scene/scene_env_confs/lobby_spring_festival.xml'
        scn = self.get_scene()
        if not scn:
            log_error('scene is not exist')
            return
        scn.load_env_new(sky_box_xml)
        scn.setup_env_light_info('dating', 'on_ground')

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
        if self.outside_enable:
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

    def on_exit(self):
        if self.fireworks_timer:
            global_data.game_mgr.unregister_logic_timer(self.fireworks_timer)
            self.fireworks_timer = None
        if self.replace_texture_delay_exec:
            game3d.cancel_delay_exec(self.replace_texture_delay_exec)
            self.replace_texture_delay_exec = None
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect
        global_data.emgr.spring_festival_inside_skin_enable -= self.set_spring_festival_inside_skin_enable
        global_data.emgr.spring_festival_outside_skin_enable -= self.set_spring_festival_outside_skin_enable
        return