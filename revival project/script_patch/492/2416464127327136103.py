# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDetectScene.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from ..UnitCom import UnitCom
import os
import math3d
import C_file
import world
import collision
import math
import os
import logic.gcommon.common_const.collision_const as collision_const
from ...cdata import jump_physic_config
from logic.gcommon.const import NEOX_UNIT_SCALE
import tinyxml
import common.cinematic.datacommon as datacommon
import os.path
SCENE_INDEX_2_PATH = {1: 'scene/bw_fangwu01/bw_fangwu01_content/',
   2: 'scene/smqjiance_01/smqjiance_02_content/'
   }
PRIMITIVE_UNDEFINED = 0
PRIMITIVE_OUTSIDE_SURFACE = 1
PRIMITIVE_INSIDE_SURFACE = 2
PRIMITIVE_ON_SURFACE = 3
PRIMITIVE_INSIDE_SURFACE_HAS_COL = 4

class ComDetectScene(UnitCom):
    BIND_EVENT = {'E_DETECT_ONE_INNER_COL_MODEL': 'detect_one_inner_col_model',
       'E_DETECT_ALL_INNER_COL_MODEL': 'detect_all_inner_col_model',
       'E_REMOVE_INNER_COL_MODEL': 'remove_model'
       }

    def __init__(self):
        super(ComDetectScene, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComDetectScene, self).init_from_dict(unit_obj, bdict)
        self._cur_model = []
        self._model_info_list = []
        self._model_info_dict = {}
        self._scene_path = None
        return

    def get_chunk_name(self, x, z, lod):
        if lod == 0:
            return '%d_%d' % (x, z)
        else:
            return 'l%d_%d_%d' % (lod, x, z)

    def get_chunk_file_list(self):
        file_list = []
        for lod in range(3):
            for x in range(-50, 50):
                for z in range(-50, 50):
                    chunk_name = self.get_chunk_name(x, z, lod)
                    path = self._scene_path + chunk_name + '.scn'
                    if C_file.find_res_file(path, ''):
                        file_list.append(path)

        return file_list

    def init_model_list(self):
        self._model_info_list = []
        self._model_info_dict = {}
        if not self._model_info_list:
            chunk_files = self.get_chunk_file_list()
            for file in chunk_files:
                file_list = []
                cur_model_info_list = []
                doc = tinyxml.TiXmlDocument()
                buf = C_file.get_res_file(file, '')
                doc.Parse(buf)
                root = doc.RootElement()
                scene_obj_node = datacommon.get_child_doc(root, 'Scene')
                is_log = False
                if is_log:
                    print('test--chunk_files--step2--file = ', file, '--scene_obj_node =', scene_obj_node)
                if not scene_obj_node:
                    continue
                entities_obj_node = datacommon.get_child_doc(scene_obj_node, 'Entities')
                if is_log:
                    print('test--chunk_files--step3--entities_obj_node =', entities_obj_node)
                if not entities_obj_node:
                    continue
                models_obj_node = datacommon.get_child_doc(entities_obj_node, 'Models')
                if is_log:
                    print('test--chunk_files--step4--models_obj_node =', models_obj_node)
                if not models_obj_node:
                    continue
                all_files_obj_node = datacommon.get_child_doc(entities_obj_node, 'AllFiles')
                if is_log:
                    print('test--chunk_files--step5--all_files_obj_node =', all_files_obj_node)
                if not all_files_obj_node:
                    continue
                child = models_obj_node.FirstChild()
                while child:
                    one_model_attr = self.get_childe_attr_dict(child)
                    position_desc = one_model_attr.get('Position', '')
                    if position_desc:
                        coord_list = position_desc.split(',')
                        for index in range(len(coord_list)):
                            coord_list[index] = float(coord_list[index])

                        coord_list = tuple(coord_list)
                        one_model_attr['Position'] = math3d.vector(*coord_list)
                    else:
                        one_model_attr['Position'] = math3d.vector(0, 0, 0)
                    rotation_desc = one_model_attr.get('Rotation', '')
                    rot = math3d.matrix()
                    if rotation_desc:
                        value_list = rotation_desc.split(',')
                        for index in range(len(value_list)):
                            value_list[index] = float(value_list[index])

                        if value_list:
                            value_list = tuple(value_list)
                            rot.set_all(value_list)
                        else:
                            print('test--chunk_files--step6--file = ', file, '--rotation_desc =', rotation_desc)
                    one_model_attr['Rotation'] = rot
                    one_model_attr['FilePathIndex'] = int(one_model_attr['FilePathIndex'])
                    one_model_attr['ColGroup'] = int(one_model_attr['ColGroup'])
                    one_model_attr['ColMask'] = int(one_model_attr['ColMask'])
                    cur_model_info_list.append(one_model_attr)
                    child = child.NextSibling()

                child = all_files_obj_node.FirstChild()
                while child:
                    one_file_attr = self.get_childe_attr_dict(child)
                    file_list.append(one_file_attr)
                    child = child.NextSibling()

                for index in range(len(cur_model_info_list)):
                    one_model_attr = cur_model_info_list[index]
                    file_path_index = one_model_attr['FilePathIndex']
                    one_file_attr = file_list[file_path_index]
                    one_model_attr['Path'] = one_file_attr['Path']
                    if is_log:
                        print('test--chunk_files--step7--Path =', one_model_attr['Path'], '--one_model_attr =', one_model_attr)
                    self._model_info_dict[one_model_attr['Path']] = one_model_attr

                self._model_info_list.extend(cur_model_info_list)

    def detect_one_scene_inner_col_model(self, path, scene_index, callback=None):
        all_scene_path = list(six_ex.values(SCENE_INDEX_2_PATH))

        def finish_hit_test():
            if scene_index < len(all_scene_path):
                self.detect_one_scene_inner_col_model(path, scene_index + 1, callback)
            elif callback:
                callback()

        scene_path = all_scene_path[scene_index]
        self._scene_path = scene_path
        self.init_model_list()
        path = path.replace('/', '\\')
        one_model_info = self._model_info_dict.get(path, None)
        if not one_model_info:
            print(('test--detect_one_inner_col_model--step1--model path =', path, '--not exist in scene =', self._scene_path))
            return False
        else:
            self.remove_model()
            self.detect_one_model(one_model_info, finish_hit_test)
            print(('test--detect_one_inner_col_model--step2--model path =', path, '--exist in scene =', self._scene_path))
            return True

    def detect_one_inner_col_model(self, path, callback=None):
        self.detect_one_scene_inner_col_model(path, 0, callback)

    def detect_all_inner_col_model(self, scene_index=1):
        if isinstance(scene_index, str):
            self._scene_path = scene_index
        else:
            self._scene_path = SCENE_INDEX_2_PATH[scene_index]
        self.remove_model()
        self.init_model_list()
        print(('test--len(_model_info_list) =', len(self._model_info_list), '--type(_model_info_list) =', type(self._model_info_list), '--_scene_path =', self._scene_path))
        for one_model_info in self._model_info_list:
            self.detect_one_model(one_model_info)

    def get_childe_attr_dict(self, node):
        all_attr = {}
        attri = node.FirstAttribute()
        while attri:
            all_attr[attri.Name] = attri.Value
            attri = attri.Next()

        return all_attr

    def remove_model(self):
        print('test--remove_model--_cur_model =', self._cur_model)
        if self._cur_model:
            for one_model in self._cur_model:
                one_model.destroy()

            self._cur_model = []

    def detect_one_model(self, one_model_info, callback=None):
        import common.utils.timer as timer
        self.create_one_model(one_model_info)
        model = self._cur_model[0]
        global_data.game_mgr.register_logic_timer(self.hit_by_ray_test, 0.1, args=(
         model, callback), times=1, mode=timer.CLOCK)

    def hit_by_ray_test(self, model, callback, *args):
        character = self.sd.ref_character
        filename = model.filename
        g = globals()
        primitive_type_desc = 'PRIMITIVE_INSIDE_SURFACE'
        primitive_type = g[primitive_type_desc]
        filename = 'res/close_space_result/' + filename
        full_filename = os.path.abspath(filename)
        path_split = os.path.split(full_filename)
        obj_filename = full_filename.replace('gim', 'obj')
        center_filename = full_filename.replace('gim', 'txt')
        print(('test--hit_by_ray_test--obj_filename =', obj_filename))
        total_height = 120
        group = collision_const.GROUP_STATIC_SHOOTUNIT
        mask = character.mask
        duration = jump_physic_config.jump_speed / jump_physic_config.gravity
        jump_height = 0.5 * jump_physic_config.gravity * NEOX_UNIT_SCALE * duration ** 2
        result = model.voxelize(obj_filename, center_filename, total_height, group, mask, jump_height, primitive_type)
        is_has_close_space = result[0]
        if is_has_close_space:
            self.write_one_file(center_filename, result[1])
            self.write_one_file(obj_filename, result[2])
        print(('test--hit_by_ray_test--step2--is_has_close_space = ', is_has_close_space, '--total_height =', total_height, '--full_filename =', full_filename, '--jump_height =', jump_height / NEOX_UNIT_SCALE))
        if callback:
            callback()

    def write_one_file(self, new_path, text):
        new_path = os.path.abspath(new_path)
        dir_path = os.path.dirname(new_path)
        print('test--write_one_file--new_path =', new_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(new_path, 'w') as f:
            f.write(text)

    def create_one_model(self, one_model_info):
        self.load_one_model(one_model_info['Path'])
        merge_path = self.get_merge_model_path(one_model_info['Path'])
        if merge_path:
            print(('test--create_one_model--merge_path =', merge_path))
            self.load_one_model(merge_path)

    def load_one_model(self, path):
        print(('test--load_one_model--path =', path))
        MODEL_POSITION = math3d.vector(0, 60, 0)
        one_model = world.model(path, world.get_active_scene())
        self._cur_model.append(one_model)
        one_model.world_position = MODEL_POSITION
        lod_dist_list = (455, 910, 1105)
        one_model.lod_config = lod_dist_list
        one_model.active_collision = True

    def get_merge_model_path(self, path):
        basename = os.path.basename(path)
        split_path = os.path.split(path)
        split_filename = os.path.splitext(basename)
        filename_no_ext = split_filename[0]
        if not filename_no_ext.endswith('_a'):
            return
        else:
            part_filename = filename_no_ext[:-2]
            pair_filename = split_path[0] + '\\' + part_filename + '_b' + split_filename[1]
            pair_model_attr = self._model_info_dict.get(pair_filename, None)
            if not pair_model_attr:
                return
            cur_model_attr = self._model_info_dict.get(path, None)
            if not cur_model_attr:
                return
            pair_model_pos = pair_model_attr['Position']
            pair_model_pos = tuple([int(pair_model_pos.x), int(pair_model_pos.y), int(pair_model_pos.z)])
            cur_model_pos = cur_model_attr['Position']
            cur_model_pos = tuple([int(cur_model_pos.x), int(cur_model_pos.y), int(cur_model_pos.z)])
            if cur_model_pos != pair_model_pos:
                return
            return pair_filename