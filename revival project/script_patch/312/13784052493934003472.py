# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMiaoMiaoDating.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from . import ScenePart
import world
from logic.gutils.scene_utils import UI_SCENE_BOX_PREFIX
from logic.gcommon.const import DEFAULT_ROLE_ID
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.item import item_const as iconst
from logic.gutils.ConnectHelper import ConnectHelper
import render
from common.cfg import confmgr
import game3d
from logic.gcommon.const import LOBBY_TV_TOUCH_MAX_DISTANCE
from common.platform.dctool import interface
import C_file
import math3d
from logic.gcommon.common_const import collision_const
import collision
from logic.gcommon.common_const import lobby_const
_HASH_Tex0 = game3d.calc_string_hash('Tex0')
_HASH_Tex12 = game3d.calc_string_hash('Tex12')
_HASH_NormalMap = game3d.calc_string_hash('NormalMap')
_HASH_LightMap = game3d.calc_string_hash('LightMap')
_HASH_LightMapSep = game3d.calc_string_hash('LightMapSep')
_HASH_u_lightmap_scale = game3d.calc_string_hash('u_lightmap_scale')
_HASH_u_lightmap_add = game3d.calc_string_hash('u_lightmap_add')
_HASH_u_texture_trans1 = game3d.calc_string_hash('u_texture_trans1')
VAR_NAME = ('Tex0', 'Tex12', 'NormalMap')
VAR_NAME_HASH = (_HASH_Tex0, _HASH_Tex12, _HASH_NormalMap)
TEXTURE_MAP = {'dt_building_diji_01': [
                         ('dt_building_diji_01_4', '01_b', '01_m', '01_n')],
   'dt_prop_zhuzi_01': [
                      ('dt_prop_zhuzi_01_0', '02_b', '02_m', '02_n')],
   'dt_building_diji_02': [
                         ('dt_building_diji_020', '03_b')],
   'dt_building_diji_03': [
                         ('dt_building_diji_030', '04_b')],
   'dt_prop_zhanshitai_01': [
                           ('dt_prop_zhanshitai_01', '05_b')],
   'dt_prop_zhanshitai_03': [
                           ('dt_prop_zhanshitai_030', '06_b')],
   'dt_prop_toutie_01': [
                       ('dt_prop_toutie_01', '07_b')]
   }
LOBBY_SKIN_TYPE_DEFAULT = 0
LOBBY_SKIN_TYPE_REPLACE_TEX = 1
LOBBY_SKIN_TYPE_REPLACE_MODEL = 3
LOBBY_SKIN_TYPE_SPRING_FESTIVAL = 4
LOBBY_SCENE_REPLAY_MODEL_FILE = {lobby_const.LOBBY_SCENE_TYPE_WSJ: 'lobby_models_wsj',
   lobby_const.LOBBY_SCENE_TYPE_SDJ: 'lobby_models_sdj'
   }
ITEM_NO_TO_STYLE_MAP = {'0': (
       LOBBY_SKIN_TYPE_DEFAULT, None, 'dating'),
   '210010000': (
               LOBBY_SKIN_TYPE_DEFAULT, None, 'dating'),
   '210010001': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_haibian', 'dating'),
   '210010002': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_huoyan', 'dating'),
   '210010003': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_huoyan_a', 'dating'),
   '210010004': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_keai', 'dating'),
   '210010005': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_kehuan', 'dating'),
   '210010006': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_qipao', 'dating'),
   '210010007': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_qipao_a', 'dating'),
   '210010008': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_rixi', 'dating'),
   '210010009': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_yinyue', 'dating'),
   '210010010': (
               LOBBY_SKIN_TYPE_REPLACE_TEX, 'dating_yinyue_a', 'dating'),
   '210010011': (
               LOBBY_SKIN_TYPE_SPRING_FESTIVAL, 'dating_chunjie', 'dating'),
   '210010012': (
               LOBBY_SKIN_TYPE_REPLACE_MODEL, lobby_const.LOBBY_SCENE_TYPE_SDJ, 'dating_sdj'),
   '210010013': (
               LOBBY_SKIN_TYPE_REPLACE_MODEL, lobby_const.LOBBY_SCENE_TYPE_WSJ, 'dating_wsj')
   }
PIC_HEAD = 'model_new/miaomiaoxitong/%s/%s_%s.tga'
EXTRA_MODELS = ('model_new\\xuanjue\\new_dating_cj\\zhujiemian_cj_denglong01.gim',
                'model_new\\xuanjue\\new_dating_cj\\zhujiemian_cj_tiehua01.gim')
S_CHARACTER_RESET_POSITION = math3d.vector(22.4853, 16.891581, -9.516837)
BOX_COMPUTER_POSITION = {'210010013': {'box_computer_2': math3d.vector(-137.82, 16.34, -213.99),'box_computer_4': math3d.vector(147.33, 15.32, -239.09),'box_computer_3': math3d.vector(-144.99, 24, -210.78),'box_computer_5': math3d.vector(150.92, 21.32, -233.89)}}
DEFAULT_BOX_COMPUTER_POSITION = {'box_computer_2': math3d.vector(-172.89, 20.39, -230.1),'box_computer_4': math3d.vector(175.1, 20.39, -230.1),'box_computer_3': math3d.vector(-172.89, 27.53, -227.69),'box_computer_5': math3d.vector(175.1, 27.53, -227.69)}
DEFAULT_SFX_NAMES = [
 'dating_dengguang_13_108',
 'dating_dengguang_12_105',
 'dating_pingmu_hengxian_03_57',
 'dating_pingmu_hengxian_03_46',
 'dating_dengguang_02_128',
 'dating_pingmu_hengxian_03_52',
 'dating_dengguang_05_105',
 'dating_dengguang_11_102',
 'dating_dengguang_09_100',
 'dating_dengguang_07_31',
 'dating_dengguang_04_distortion_122',
 'dating_dengguang_06_74',
 'dating_dengguang_06_71',
 'dating_pingmu_hengxian_04_103',
 'dating_dianzi_32',
 'dating_dengguang_02_12',
 'dating_dengguang_06_68',
 'dating_dengguang_06_108',
 'dating_stopsign_57']
IGNORE_MODELS = [
 'lobby_mirror',
 'box_mecha_02',
 'box_mecha_01',
 'box_mecha',
 'box_mecha_04',
 'box_mecha_03',
 'box_mecha_hologram']

class PartMiaoMiaoDating(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartMiaoMiaoDating, self).__init__(scene, name)
        self.cur_use_item_no = -1
        self.mianmiao_style_name = ''
        self.is_load = False
        self.cur_scene_type = lobby_const.LOBBY_SCENE_TYPE_DEFAULT
        self.load_downcount = {}
        self.skin_lobby_models = {}
        self.skin_lobby_sfxs = {}
        self.skin_lobby_cols = {}
        self.default_lobby_models = []
        self.default_lobby_sfxs = []
        self.spring_festival_extra_models = []
        self.spring_festival_extra_cols = []
        self.need_reset_character_position = True
        self.save_default_texture_maps = {}
        self.replace_tex_of_model_map = {}
        self.model_name_map = confmgr.get('miaomiao_model_map', default={})
        for model_name, scene_model_names in six.iteritems(self.model_name_map):
            for scene_model_name in scene_model_names:
                self.replace_tex_of_model_map[scene_model_name] = TEXTURE_MAP.get(model_name)

        self.check_shoot_func_map = {LOBBY_SKIN_TYPE_DEFAULT: self.reset_lobby_skin,
           LOBBY_SKIN_TYPE_REPLACE_TEX: self.process_scene_texture,
           LOBBY_SKIN_TYPE_REPLACE_MODEL: self.process_scene_models,
           LOBBY_SKIN_TYPE_SPRING_FESTIVAL: self.process_spring_festival
           }

    def on_enter(self):
        global_data.emgr.miaomiao_lobby_skin_change += self.reset_style
        global_data.emgr.miaomiao_lobby_skin_change_force += self.reset_style_force
        global_data.emgr.player_leave_visit_scene_event += self.on_leave_scene
        global_data.emgr.player_enter_visit_scene_event += self.on_enter_scene

    def reset_style_force(self, item_no=-1):
        self.reset_style(item_no, True)

    def reset_style(self, item_no=-1, force=False):
        if not global_data.player:
            return
        if item_no == -1:
            is_in_visit_mode = global_data.player.is_in_visit_mode()
            if is_in_visit_mode:
                cur_miaomiao_item_no = global_data.player.get_visit_lobby_skin_id()
            else:
                cur_miaomiao_item_no = global_data.player.get_lobby_skin()
            self.change_style_by_item_no(cur_miaomiao_item_no)
        else:
            self.change_style_by_item_no(item_no)

    def on_load(self):
        self.is_load = True
        for model in self.scene().get_models():
            if model.name in IGNORE_MODELS:
                continue
            self.default_lobby_models.append(model)

        for sfx_name in DEFAULT_SFX_NAMES:
            sfx = self.scene().get_sfx(sfx_name)
            if sfx:
                self.default_lobby_sfxs.append(sfx)

        self.need_reset_character_position = False
        self.reset_style(-1)
        self.need_reset_character_position = True

    def on_enter_scene(self, *args):
        self.reset_style(-1)

    def on_leave_scene(self, *args):
        self.reset_style(-1)

    def create_model_simple(self, model_path, model_list, col_list, use_item_no):
        scn = self.scene()

        def callback(model):
            model_list.append(model)
            col = collision.col_object(collision.MESH, model, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_DEFAULT_VISIBLE, 0, True)
            scn.scene_col.add_object(col)
            col.position = model.world_position
            col.rotation_matrix = model.rotation_matrix
            col_list.append(col)
            if self.cur_use_item_no != use_item_no:
                model.visible = False
                col.mask = 0
                col.group = collision_const.GROUP_DEFAULT_VISIBLE

        global_data.model_mgr.create_model_in_scene(model_path, pos=math3d.vector(0, 0, 0), on_create_func=callback, create_scene=scn)

    def process_spring_festival(self, mianmiao_style_name, use_item_no):
        self.replace_texture(mianmiao_style_name)
        if self.spring_festival_extra_models:
            for model in self.spring_festival_extra_models:
                model.visible = True

            for col in self.spring_festival_extra_cols:
                col.mask = collision_const.GROUP_CHARACTER_INCLUDE
                col.group = collision_const.GROUP_DEFAULT_VISIBLE

        else:
            for model_path in EXTRA_MODELS:
                self.create_model_simple(model_path, self.spring_festival_extra_models, self.spring_festival_extra_cols, use_item_no)

        self.replace_scene_models(lobby_const.LOBBY_SCENE_TYPE_DEFAULT)
        self.reset_lobby_player_position()

    def hide_spring_festival_extra_model(self):
        if self.spring_festival_extra_models:
            for model in self.spring_festival_extra_models:
                model.visible = False

            for col in self.spring_festival_extra_cols:
                col.mask = 0
                col.group = collision_const.GROUP_DEFAULT_VISIBLE

    def reset_lobby_skin(self, _, use_item_no):
        self.reset_texture()
        self.replace_scene_models(lobby_const.LOBBY_SCENE_TYPE_DEFAULT)
        self.hide_spring_festival_extra_model()

    def reset_lobby_player_position(self):
        if global_data.lobby_player and self.need_reset_character_position:
            global_data.lobby_player.send_event('E_FOOT_POSITION', S_CHARACTER_RESET_POSITION)

    def process_scene_models(self, lobby_scene_type, use_item_no):
        self.replace_scene_models(lobby_scene_type)
        self.hide_spring_festival_extra_model()
        self.reset_lobby_player_position()

    def change_style_by_item_no(self, item_no):
        if not self.is_load:
            return
        else:
            if self.cur_use_item_no == item_no:
                return
            self.cur_use_item_no = item_no
            style_inf = ITEM_NO_TO_STYLE_MAP.get(str(item_no), None)
            if style_inf != None:
                style = style_inf[0]
                self.check_shoot_func_map[style](style_inf[1], self.cur_use_item_no)
                self.setup_env_light_info(style_inf[2])
                self.fix_lobby_scene_computer_box_position(str(item_no))
            return

    def fix_lobby_scene_computer_box_position(self, item_no):
        scn = self.scene()
        computer_box_positions = BOX_COMPUTER_POSITION.get(item_no, DEFAULT_BOX_COMPUTER_POSITION)
        for box_name, pos in computer_box_positions.items():
            model = scn.get_model(box_name)
            if model:
                model.position = pos

    def setup_env_light_info(self, env_conf_name):
        scn = self.scene()
        scn.setup_env_light_info(env_conf_name, 'on_ground')

    def process_scene_texture(self, mianmiao_style_name, use_item_no):
        self.replace_scene_models(lobby_const.LOBBY_SCENE_TYPE_DEFAULT)
        self.replace_texture(mianmiao_style_name)
        self.hide_spring_festival_extra_model()

    def replace_texture(self, mianmiao_style_name):
        if self.mianmiao_style_name == mianmiao_style_name:
            return
        self.mianmiao_style_name = mianmiao_style_name
        self.need_replace_models = self.replace_tex_of_model_map.keys()
        need_save_default_map = not self.save_default_texture_maps
        scn = self.scene()
        save_model_names = []
        for model_name in self.need_replace_models:
            datas = self.replace_tex_of_model_map.get(model_name)
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

        scn = self.scene()
        teihua_model = scn.get_model('tiehua_162')
        if teihua_model:
            teihua_model.visible = False

    def create_model_async(self, model_info, model_list, col_list, scene_type, old_models):
        scn = self.scene()
        position = model_info['Position']

        def callback(model):
            model.position = math3d.vector(*position)
            rotation = model_info.get('Rotation')
            if rotation:
                rot = math3d.matrix()
                rot.set_all(rotation)
                model.rotation_matrix = rot.rotation
            scale = model_info.get('Scale')
            if scale:
                model.scale = math3d.vector(*scale)
            lightmap_info = model_info.get('Lightmap')
            if lightmap_info:
                path = lightmap_info['LightmapPath']
                uv_ofs = lightmap_info['uv_ofs']
                uv_scale = lightmap_info['uv_scale']
                lightmap_scale = lightmap_info['lightmap_scale']
                lightmap_add = lightmap_info['lightmap_add']
                model.manual_apply_lightmap_ue(path, 2, uv_scale[0], uv_scale[1], uv_ofs[0], uv_ofs[1], lightmap_scale[0], lightmap_scale[1], lightmap_scale[2], lightmap_add[0], lightmap_add[1], lightmap_add[2], lightmap_add[3], True, '_sep_rgb')
            if model_info.get('is_collision'):
                col = collision.col_object(collision.MESH, model, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_DEFAULT_VISIBLE, 0, True)
                col.position = model.world_position
                col.rotation_matrix = model.rotation_matrix
                scn.scene_col.add_object(col)
                col_list.append(col)
                if self.cur_scene_type != scene_type:
                    col.mask = 0
                    col.group = collision_const.GROUP_DEFAULT_VISIBLE
            if model_info.get('is_hide'):
                model.visible = False
            else:
                model.visible = False
                model_list.append(model)
            self.load_downcount[scene_type] -= 1
            if self.load_downcount[scene_type] == 0 and self.cur_scene_type == scene_type:
                self.change_model_show(old_models, model_list)

        position = model_info['Position']
        global_data.model_mgr.create_model_in_scene(model_info['FilePath'], pos=math3d.vector(*position), on_create_func=callback, create_scene=scn)

    def replace_scene_models(self, new_scene_type):
        if self.cur_scene_type == new_scene_type:
            return
        old_scene_type = self.cur_scene_type
        self.cur_scene_type = new_scene_type
        if old_scene_type == lobby_const.LOBBY_SCENE_TYPE_DEFAULT:
            old_models = self.default_lobby_models
            old_cols = []
        else:
            old_models = self.skin_lobby_models.get(old_scene_type, [])
            old_cols = self.skin_lobby_cols.get(old_scene_type, [])
        if new_scene_type == lobby_const.LOBBY_SCENE_TYPE_DEFAULT:
            new_models = self.default_lobby_models
            new_cols = []
            self.change_model_show(old_models, new_models)
        else:
            new_models = self.skin_lobby_models.get(new_scene_type, [])
            new_cols = self.skin_lobby_cols.get(new_scene_type, [])
            if not new_models:
                replace_model_infos = confmgr.get(LOBBY_SCENE_REPLAY_MODEL_FILE.get(new_scene_type), 'models', default={})
                self.load_downcount[new_scene_type] = len(replace_model_infos)
                for model_info in replace_model_infos:
                    self.create_model_async(model_info, new_models, new_cols, new_scene_type, old_models)

                self.skin_lobby_models[new_scene_type] = new_models
                self.skin_lobby_cols[new_scene_type] = new_cols
            else:
                self.change_model_show(old_models, new_models)
        for col in old_cols:
            col.mask = 0
            col.group = collision_const.GROUP_DEFAULT_VISIBLE

        for col in new_cols:
            col.mask = collision_const.GROUP_CHARACTER_INCLUDE
            col.group = collision_const.GROUP_DEFAULT_VISIBLE

        old_sfxs = self.default_lobby_sfxs if old_scene_type == LOBBY_SKIN_TYPE_DEFAULT else self.skin_lobby_sfxs.get(old_scene_type, [])
        if new_scene_type == LOBBY_SKIN_TYPE_DEFAULT:
            new_sfxs = self.default_lobby_sfxs if 1 else self.skin_lobby_sfxs.get(new_scene_type, [])
            replace_sfx_infos = new_sfxs or confmgr.get(LOBBY_SCENE_REPLAY_MODEL_FILE.get(new_scene_type), 'sfxs', default=[])
            for sfx_info in replace_sfx_infos:
                position = model_info['Position']
                sfx = world.sfx(model_info['FilePath'], scene=scn)
                sfx.position = math3d.vector(*position)
                new_sfxs.append(model)

            self.skin_lobby_sfxs[new_scene_type] = new_sfxs
        for sfx in old_sfxs:
            sfx.visible = False

        for sfx in new_sfxs:
            sfx.visible = True

        PartMirror = self.get_scene().get_com('PartMirror')
        PartMirror.replace_scene_models(new_scene_type)

    def change_model_show(self, old_models, new_models):
        for model in old_models:
            if model.valid:
                model.visible = False

        for model in new_models:
            if model.valid:
                model.visible = True

    def reset_texture(self, *args):
        self.need_replace_models = self.replace_tex_of_model_map.keys()
        if not self.save_default_texture_maps:
            return
        scn = self.scene()
        save_model_names = []
        for model_name in self.need_replace_models:
            datas = self.replace_tex_of_model_map.get(model_name)
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
        self.mianmiao_style_name = ''
        scn = self.scene()
        teihua_model = scn.get_model('tiehua_162')
        if teihua_model:
            teihua_model.visible = True

    def check_res_file(self, texture_name):
        if C_file.find_res_file(texture_name, '') == 1:
            return True
        if C_file.find_res_file(texture_name.replace('.tga', '.ktx'), '') == 1:
            return True
        if C_file.find_res_file(texture_name.replace('.tga', '.dds'), '') == 1:
            return True
        return False

    def on_exit(self):
        global_data.emgr.miaomiao_lobby_skin_change -= self.reset_style
        global_data.emgr.miaomiao_lobby_skin_change_force -= self.reset_style_force
        global_data.emgr.player_leave_visit_scene_event -= self.on_leave_scene
        global_data.emgr.player_enter_visit_scene_event -= self.on_enter_scene