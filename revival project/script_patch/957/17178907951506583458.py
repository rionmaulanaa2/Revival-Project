# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/modelmgr.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import world
import game3d
import math3d
from common.framework import Singleton
from common.cfg import confmgr
from common.utils.pool_mgr import ModelPoolMgr, ResRefPoolMgr
from logic.manager_agents.manager_decorators import sync_exec
SPECIAL_MODEL_NOT_ADD_TO_POOL = ('8029', '8024_skin_s02')

class ModelConfig(object):

    def __init__(self, model_path, mesh_path_list=[]):
        self._model_path = model_path.replace('\\', '/')
        self._mesh_path_map = {}
        for mesh_path in mesh_path_list:
            self._mesh_path_map[mesh_path.replace('\\', '/')] = False

    def __str__(self):
        return self.get_key()

    def __repr__(self):
        return self.get_key()

    def get_key(self):
        mesh_path = ';'.join(six_ex.keys(self._mesh_path_map))
        return '{}|{}'.format(self._model_path, mesh_path)

    def get_model_path(self):
        return self._model_path

    def get_mesh_path_map(self):
        return self._mesh_path_map

    def set_mesh_loaded(self, mesh_path):
        if mesh_path in self._mesh_path_map:
            self._mesh_path_map[mesh_path] = True

    def set_all_mesh_loaded(self):
        for mesh_path in six.iterkeys(self._mesh_path_map):
            self._mesh_path_map[mesh_path] = True

    def is_all_mesh_loaded(self):
        for flag in six.itervalues(self._mesh_path_map):
            if not flag:
                return False

        return True


class ModelMgr(Singleton):
    ALIAS_NAME = 'model_mgr'
    MAX_MODEL_ID = 1000000000
    ENABLE_MESH_LOAD_ASYNC = True

    def init(self):
        self._model_loading_cfgs = {}
        self._model_loaded_cfgs = {}
        self._model_ids = {}
        self._cur_model_id = 0
        self._enable_model_pool = not global_data.force_disable_model_cache

    def on_finalize(self):
        pass

    def clean_up_invalid(self):
        to_remove_id_list = []
        for model_id, (model, _, _, _) in six.iteritems(self._model_loaded_cfgs):
            if model is None or not model.valid:
                to_remove_id_list.append(model_id)

        for model_id in to_remove_id_list:
            self.remove_model_by_id(model_id)

        return

    @property
    def enable_model_pool--- This code section failed: ---

  87       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    @enable_model_pool.setter
    def enable_model_pool(self, value):
        self._enable_model_pool = value and not global_data.force_disable_model_cache

    def create_model_in_scene(self, model_path, pos=math3d.vector(0, 0, 0), mesh_path_list=[], on_create_func=None, ex_data=None, create_scene=None):
        if not create_scene:
            scene = global_data.game_mgr.scene if 1 else create_scene
            return scene or None
        create_scene_type = scene.get_type()

        def on_create_model_in_scene(model):
            if model and model.valid is False:
                if model in self._model_ids:
                    import exception_hook
                    model_id = self._model_ids[model]
                    log_msg = 'model {} is not valid:'.format(model_id)
                    if model_id in self._model_loading_cfgs:
                        log_msg += '{}'.format(self._model_loading_cfgs[model_id])
                    if model_id in self._model_loaded_cfgs:
                        log_msg += '{}'.format(self._model_loaded_cfgs[model_id])
                    exception_hook.post_error(log_msg, 'DEBUG')
                self.remove_model(model)
                return
            scene = create_scene or global_data.game_mgr.scene if 1 else create_scene
            if scene and scene.valid and scene.get_type() == create_scene_type:
                scene.add_object(model)
                model.world_position = pos
            else:
                self.remove_model(model)
                return
            if on_create_func:
                on_create_func(model)

        return self.create_model(model_path, mesh_path_list, on_create_model_in_scene, ex_data)

    def create_model(self, model_path, mesh_path_list=[], on_create_func=None, ex_data=None):
        from logic.gutils import scene_utils
        model_path = scene_utils.scene_replace_res(model_path)
        model_cfg = ModelConfig(model_path, mesh_path_list)
        model = None
        if self._enable_model_pool:
            model = ModelPoolMgr().get_item(model_cfg.get_key())
        model_id = self._gen_model_id()
        ex_data = {} if ex_data is None else ex_data
        ex_data['model_id'] = model_id
        if model and model.valid:
            model.visible = True
            model_cfg.set_all_mesh_loaded()
            self._model_loading_cfgs[model_id] = (model_cfg, on_create_func, ex_data, None)
            self._on_after_create_model(model, model_id, None)
        else:
            task_handle = world.create_model_async(model_path, self._on_after_create_model, model_id, game3d.ASYNC_VERY_HIGH)
            self._model_loading_cfgs[model_id] = (model_cfg, on_create_func, ex_data, task_handle)
        return model_id

    def remove_model_socket(self, model, remove_socket_list):
        for socket_name in remove_socket_list:
            socket_object_count = model.get_socket_obj_count(socket_name)
            for index in range(socket_object_count):
                model.set_socket_bound_obj_active(socket_name, index, True, True)
                obj = model.get_socket_obj(socket_name, index)
                if obj:
                    obj.remove_from_parent()
                    obj.destroy()

    def remove_model(self, model, is_clear_socket_model=True):
        self._imp_remove_model(model=model, is_clear_socket_model=is_clear_socket_model)

    def remove_model_by_id(self, model_id):
        self._imp_remove_model(model_id=model_id)

    def create_mesh_async(self, task_handle, res_path, owner_model, on_load_callback=None, on_load_before_add=None, priority=game3d.ASYNC_VERY_HIGH):
        if self.ENABLE_MESH_LOAD_ASYNC:

            def on_load_mesh_cb(res_obj, udata=None, current_task=None):
                if res_obj is None or not (owner_model and owner_model.valid):
                    return
                else:
                    if global_data.enable_res_ref_cache and not global_data.is_low_mem_mode:
                        res_path, = udata
                        ResRefPoolMgr().add_item(res_path, res_obj)
                    if on_load_before_add:
                        on_load_before_add(owner_model)
                    owner_model.add_mesh(res_obj)
                    if on_load_callback:
                        on_load_callback(owner_model)
                    return

            if task_handle:
                task_handle.cancel()
            task_handle = world.create_res_object_async(res_path, on_load_mesh_cb, (res_path,), priority)
        elif not (owner_model and owner_model.valid):
            return
        if on_load_before_add:
            on_load_before_add(owner_model)
        owner_model.add_mesh(res_path)
        if on_load_callback:
            on_load_callback(owner_model)
        return task_handle

    def _on_create_callback(self, model_id):
        if model_id not in self._model_loaded_cfgs:
            return
        model, model_cfg, on_create_func, ex_data = self._model_loaded_cfgs[model_id]
        on_create_func(model)

    def _gen_model_id(self):
        self._cur_model_id = (self._cur_model_id + 1) % self.__class__.MAX_MODEL_ID
        return self._cur_model_id

    def _on_after_create_model(self, model, model_id, notused_cur_task):
        if model is None:
            if model_id in self._model_loading_cfgs:
                del self._model_loading_cfgs[model_id]
            return
        else:
            if model_id not in self._model_loading_cfgs:
                model.destroy()
                return
            model_cfg, on_create_func, ex_data, task_handle = self._model_loading_cfgs[model_id]
            if model_cfg.is_all_mesh_loaded():
                del self._model_loading_cfgs[model_id]
                self._model_loaded_cfgs[model_id] = (model, model_cfg, on_create_func, ex_data)
                self._model_ids[model] = model_id
                if on_create_func:
                    global_data.game_mgr.sync_exec(self._on_create_callback, model_id)
            else:
                for path in six.iterkeys(model_cfg.get_mesh_path_map()):
                    world.create_res_object_async(path, self._on_after_create_static_mesh, (model, model_id, path))

            return

    def _on_after_create_static_mesh(self, mesh, data, notused_cur_task):
        model, model_id, mesh_path = data
        if model_id not in self._model_loading_cfgs:
            if model and model.valid:
                model.destroy()
            return
        else:
            if mesh is None:
                return
            model.add_mesh(mesh)
            model_cfg, on_create_func, ex_data, task_handle = self._model_loading_cfgs[model_id]
            model_cfg.set_mesh_loaded(mesh_path)
            if model_cfg.is_all_mesh_loaded():
                del self._model_loading_cfgs[model_id]
                self._model_loaded_cfgs[model_id] = (model, model_cfg, on_create_func, ex_data)
                self._model_ids[model] = model_id
                if on_create_func:
                    global_data.game_mgr.sync_exec(self._on_create_callback, model_id)
            return

    def _imp_remove_model(self, model=None, model_id=None, is_clear_socket_model=True):
        if model is None and model_id is None:
            return
        else:
            if model in self._model_ids:
                model_id = self._model_ids[model]
            if model_id in self._model_loading_cfgs:
                model_cfg, on_create_func, ex_data, task_handle = self._model_loading_cfgs[model_id]
                if task_handle and task_handle.valid:
                    task_handle.cancel()
                del self._model_loading_cfgs[model_id]
            if model_id in self._model_loaded_cfgs:
                model, model_cfg, on_create_func, ex_data = self._model_loaded_cfgs[model_id]
                del self._model_loaded_cfgs[model_id]
            else:
                model_cfg = None
            if model in self._model_ids:
                del self._model_ids[model]
            if not (model and model.valid):
                return
            model.clear_events()
            model.clear_all_triggers()
            if is_clear_socket_model:
                socket_count = model.get_socket_count()
                for index in range(socket_count):
                    all_bind_model = model.get_socket_objects(index)
                    name = model.get_socket_name(index)
                    for bind_model in all_bind_model:
                        model.unbind(bind_model)

            if self._enable_model_pool and model_cfg is not None:
                mesh_path_map = model_cfg.get_mesh_path_map()
                is_not_add_to_pool = False
                for special_name in SPECIAL_MODEL_NOT_ADD_TO_POOL:
                    for path, _ in six.iteritems(mesh_path_map):
                        if special_name in path:
                            is_not_add_to_pool = True
                            break

                if model.get_segment_count() == len(mesh_path_map) + 1 and not is_not_add_to_pool:
                    model.remove_from_parent()
                    model.visible = False
                    model.position = math3d.vector(0, 0, 0)
                    model.scale = math3d.vector(1, 1, 1)
                    if ModelPoolMgr().add_item(model_cfg.get_key(), model):
                        model = None
            if model:
                model.destroy()
            return

    def get_model_by_id(self, model_id):
        if model_id in self._model_loaded_cfgs and self._model_loaded_cfgs[model_id]:
            return self._model_loaded_cfgs[model_id][0]

    def get_model_id(self, model):
        return self._model_ids.get(model, None)

    def print_debug_info(self):
        print('=============================================')
        print('[INFO] mgr loaded model:', len(self._model_loaded_cfgs))
        for model_id, cfg in six.iteritems(self._model_loaded_cfgs):
            if cfg[0].valid:
                print('\t', model_id, cfg)
            else:
                print('\t', model_id, 'no_model', cfg[1])

        print('[INFO] mgr loading model', len(self._model_loading_cfgs))
        for model_id, cfg in six.iteritems(self._model_loading_cfgs):
            print('\t', model_id, cfg)

        print('[INFO] print_debug_info:')
        print('\tcache model:')
        for k, v in six.iteritems(ModelPoolMgr().get_cached_model_map()):
            print('\t\t{}: {}'.format(k, v))

        print('=============================================')