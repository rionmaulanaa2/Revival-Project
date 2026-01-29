# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBaseModelAppearance.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from ..UnitCom import UnitCom
import game3d
import math3d
from common.cfg import confmgr
import math
import world
RES_TYPE_MODEL = 0
RES_TYPE_SFX = 1
RES_TYPE_UNKNOWN = 2
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import scene_const
from common.const.common_const import FORCE_DELTA_TIME_MS
import time
from common.utils.sfxmgr import CREATE_SRC_SIMPLE, CREATE_SRC_OTHER_HIT
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
from .ResourceManager import *
USELESS_CHAR = {
 'LMecha', ''}

class ComBaseModelAppearance(UnitCom):
    BIND_EVENT = {'G_MODEL': 'get_model',
       'G_TRANS': 'get_model_trans',
       'G_MAIN_AND_SUB_MODEL': 'get_main_and_sub_model',
       'S_ZHUJUE_MODEL': 'set_zhujue_model',
       'G_MODEL_POSITION': '_get_model_pos',
       'G_POSITION': '_get_model_pos',
       'E_POSITION': '_on_pos_changed',
       'G_LOAD_MODEL': 'load_model',
       'G_LOAD_MODEL_TASK_ID': 'load_model',
       'E_UNLOAD_MODEL': 'unload_model',
       'E_CANCEL_LOAD_TASK': 'cancel_task',
       'E_CLEAR_GIS_CACHE': 'clear_gis_cache',
       'G_IS_IN_MODEL': 'is_inner_model',
       'E_UNBIND_MODEL': 'unbind_model',
       'E_LOAD_MODEL_FROM_BDICT': 'force_load_model',
       'E_CANCEL_ALL_TASK': 'cancel_all_task',
       'E_ENABLE_RES_LOG': 'enable_res_log',
       'E_DELAY_DESTROY': 'delay_destroy',
       'E_DEBUG_POS': 'debug_pos'
       }
    BIND_LOAD_FINISH_EVENT = {'G_MODEL_FORWARD': '_get_forward_dir',
       'G_MODEL_UP': '_get_up_dir',
       'G_MODEL_ROTATION': '_get_rotation'
       }
    NEED_CACHE = False
    MAX_LOAD_MODEL_TIME = 6

    def __init__(self):
        super(ComBaseModelAppearance, self).__init__()
        self.res_loader_mgr = ResLoaderMgr()
        self._model = None
        self.is_zhujue = False
        self._position = math3d.vector(0, 0, 0)
        self._animator = None
        self._is_unbind_model_event = False
        self._save_unbind_model_event = []
        self._using_auto_move = False
        self.sd.ref_is_refreshing_whole_model = False
        self._cached_bdict = None
        self._start_load_model_time = 0
        self._sfx_ex_data = {}
        self.load_res_func = None
        return

    def reuse(self, share_data):
        super(ComBaseModelAppearance, self).reuse(share_data)
        self.sd.ref_is_refreshing_whole_model = False

    def cache(self):
        self.load_res_func = None
        self.on_model_destroy()
        if self.res_loader_mgr:
            self.res_loader_mgr.cancel_all()
        self.__destroy_base_model()
        super(ComBaseModelAppearance, self).cache()
        return

    @property
    def model(self):
        return self.get_model()

    def get_model_info(self, unit_obj, bdict):
        raise Exception('not implement get_model_info')

    def unbind_other_model(self, model):
        if not model:
            return
        socket_count = model.get_socket_count()
        bind_points = []
        for index in range(socket_count):
            all_bind_model = model.get_socket_objects(index)
            name = model.get_socket_name(index)
            bind_points.append(name)
            for bind_model in all_bind_model:
                model.unbind(bind_model)

    def get_xml_path(self):
        return ''

    def clear_gis_cache(self):
        model = self.get_model()
        if not model:
            return
        model.clear_gis_cache()
        if self.NEED_CACHE:
            model_pool = ModelPool()
            model_pool.del_free_model(model.filename)
        print(('test--clear_gis_cache--unit_obj =', self.unit_obj))
        if self.ev_g_is_avatar():
            global_data.emgr.cam_aim_clear_gis_cache.emit()

    def is_inner_model(self, outer_model):
        if not outer_model or not outer_model.valid:
            return False
        my_model = self.get_model()
        if not my_model:
            return False
        outer_center = outer_model.center_w
        outer_half_size = outer_model.bounding_box_w
        outer_min_point = outer_center - outer_half_size
        outer_max_point = outer_center + outer_half_size
        outer_radius = outer_model.bounding_radius_w
        my_center = my_model.center_w
        my_half_size = my_model.bounding_box_w
        my_min_point = my_center - my_half_size
        my_max_point = my_center + my_half_size
        my_radius = my_model.bounding_radius_w
        if my_radius >= outer_radius:
            return False
        sphere_diff = outer_center - my_center
        sphere_dist = sphere_diff.length
        min_radius = my_radius
        max_radius = outer_radius
        if sphere_dist > max_radius:
            return False
        is_max_greater = outer_max_point.x >= my_max_point.x and outer_max_point.y >= my_max_point.y and outer_max_point.z >= my_max_point.z
        is_min_less = outer_min_point.x <= my_min_point.x and outer_min_point.y <= my_min_point.y and outer_min_point.z <= my_min_point.z
        return is_max_greater and is_min_less

    def unload_model(self, model, animator=None, cached=True, is_reset_material=True):
        if self.NEED_CACHE and cached:
            model_pool = ModelPool()
            model_pool.add_free_model(model, animator, is_reset_material)
            if animator:
                animator.clear_anim_events()
        else:
            if model.valid:
                model.destroy()
            else:
                from exception_hook import post_stack
                post_stack('model has been destroyed before?')
            if animator:
                animator.destroy()

    def load_model(self, mpath, callback, cb_data=None, merge_info=None, sync_priority=game3d.ASYNC_MID, animator_path='', res_type=RES_TYPE_MODEL, use_cache_model=False, is_unbind_socket_obj=True):
        model = None
        animator = None
        if self.NEED_CACHE and not self.ev_g_is_avatar() or use_cache_model:
            model_pool = ModelPool()
            model, cache_animator = model_pool.get_free_model(mpath, animator_path)
            animator = cache_animator
        if model:
            if is_unbind_socket_obj:
                self.unbind_other_model(model)
            callback(model, cb_data, animator)
        elif self.res_loader_mgr:
            task_id = self.res_loader_mgr.add_load_task(mpath, callback, cb_data, res_type, sync_priority, merge_info=None, valid_checker=lambda use_idx=self.use_idx: self.is_enable(use_idx))
            return task_id
        return

    def load_sfx(self, mpath, callback, cb_data=None, merge_info=None, sync_priority=game3d.ASYNC_MID, *args):
        sfx_mgr = global_data.bullet_sfx_mgr

        def create_cb(sfx, use_idx):
            if not self.is_enable(use_idx):
                sfx_mgr.remove_sfx(sfx)
                return
            callback(sfx, cb_data)

        sfx_mgr.create_sfx_in_scene(mpath, on_create_func=lambda sfx, use_idx=self.use_idx: create_cb(sfx, use_idx), ex_data=self._sfx_ex_data)

    def cancel_task(self, tid):
        if self.res_loader_mgr:
            self.res_loader_mgr.cancel_task(tid)

    def cancel_all_task(self):
        if self.res_loader_mgr:
            self.res_loader_mgr.cancel_all()

    def enable_res_log(self, enable):
        res_mgr = ResourceManager()
        if res_mgr:
            res_mgr._is_log = enable
            print(('test--enable_res_log--res_mgr._is_log =', res_mgr._is_log, '--res_mgr =', res_mgr))

    def init_from_dict(self, unit_obj, bdict):
        super(ComBaseModelAppearance, self).init_from_dict(unit_obj, bdict)
        self.load_res_func = self.load_model
        position = bdict.get('position', (0, 0, 0)) or (0, 0, 0)
        self.send_event('S_ATTR_SET', 'entity_init_position', position)
        self._position = math3d.vector(*position)
        self.is_delay_destroy = False
        self.enable_debug_pos = False
        self.sd.ref_outblock_pos = bdict.get('outblock_pos')
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_changed)
        if not global_data.low_fps_switch_on:
            return
        is_agent = self.sd.ref_is_agent or self.ev_g_is_avatar()
        unit_name = self.unit_obj.__class__.__name__
        has_char = is_agent or self.unit_obj.get_com('ComCharacter') and unit_name not in USELESS_CHAR
        if not has_char and not self._using_auto_move:
            old_event = {'E_POSITION': '_on_pos_changed'
               }
            new_event = {'E_POSITION': '_set_position_auto_move'
               }
            self._unbind_event(old_event)
            self._bind_event(new_event)
            self.BIND_EVENT = {'G_MODEL': 'get_model',
               'G_MAIN_AND_SUB_MODEL': 'get_main_and_sub_model',
               'S_ZHUJUE_MODEL': 'set_zhujue_model',
               'G_MODEL_POSITION': '_get_model_pos',
               'G_POSITION': '_get_model_pos',
               'E_POSITION': '_set_position_auto_move',
               'G_LOAD_MODEL': 'load_model',
               'G_LOAD_MODEL_TASK_ID': 'load_model',
               'E_UNLOAD_MODEL': 'unload_model',
               'E_CANCEL_LOAD_TASK': 'cancel_task',
               'G_IS_IN_MODEL': 'is_inner_model'
               }
            self._using_auto_move = True

    def force_load_model(self):
        if not self._cached_bdict:
            return
        self.on_model_destroy()
        if self.res_loader_mgr:
            self.res_loader_mgr.cancel_all()
        self.__destroy_base_model()
        self.load_model_from_bdict(self._cached_bdict)

    def load_model_from_bdict(self, bdict, reload_model=False):
        ret = self.get_model_info(self.unit_obj, bdict)
        mpath, merge_info, udata = ret[0], ret[1], ret[2]
        from logic.gutils import scene_utils
        mpath = scene_utils.scene_replace_res(mpath)
        sync_priority = bdict.get('model_sync_priority', game3d.ASYNC_VERY_HIGH)
        if mpath:
            self._cached_bdict = bdict
            self._start_load_model_time = time.time()
            model = None
            animator_path = self.get_xml_path()
            if self.NEED_CACHE and not self.ev_g_is_avatar():
                model_pool = ModelPool()
                model, animator = model_pool.get_free_model(mpath, animator_path)
                self._animator = animator
                if animator:
                    animator.set_owner(self.unit_obj)
            if model:
                self.unbind_other_model(model)
                global_data.game_mgr.register_logic_timer(--- This code section failed: ---

 388       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_load_callback'
           6  LOAD_DEREF            1  'model'
           9  LOAD_DEREF            2  'udata'
          12  LOAD_DEREF            1  'model'
          15  LOAD_DEREF            3  'reload_model'
          18  CALL_FUNCTION_259   259 
          21  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18
, 1.0 / 33.0, times=1)
            else:
                callback = lambda model, udata, use_idx=self.use_idx: self._load_callback(model, udata, use_idx, reload_model=reload_model)
                self.load_res_func(mpath, callback, udata, merge_info, sync_priority, animator_path)
        return

    def on_post_init_complete(self, bdict):
        super(ComBaseModelAppearance, self).on_post_init_complete(bdict)
        self.load_model_from_bdict(bdict)

    def refresh_empty_model(self, path):
        self.sd.ref_is_refreshing_whole_model = True
        self._position = self._model.position
        model = world.model(path, None)
        self._load_callback(model, (math3d.vector(self._position), path), self.use_idx)
        return

    def get_main_and_sub_model(self, model):
        model_file_list = []
        model_file_list.append(model.filename)
        mesh_count = model.get_submesh_count()
        if hasattr(model, 'get_submesh_filename'):
            for mesh_idx in range(0, mesh_count):
                file_name = model.get_submesh_filename(mesh_idx)
                mesh_name = model.get_submesh_name(mesh_idx)
                model_file_list.append((mesh_name, file_name))

        return model_file_list

    def get_model(self):
        if self._model and self._model.valid:
            return self._model
        else:
            return None

    def get_model_trans(self):
        if self._model and self._model.valid:
            return self._model.world_transformation
        else:
            return None

    def _get_model_pos(self):
        try:
            return self._model.world_position
        except:
            return math3d.vector(self._position)

    def _get_forward_dir(self):
        model = self.get_model()
        if not model:
            return
        return model.world_rotation_matrix.forward

    def _get_up_dir(self):
        model = self.get_model()
        if not model:
            return
        return model.world_rotation_matrix.up

    def _get_rotation(self):
        if self.model:
            return self._model.world_rotation_matrix

    def unbind_model(self, bind_point):
        model = self.get_model()
        if model and model.has_socket(bind_point):
            for bind_model in model.get_socket_objects(bind_point):
                model.unbind(bind_model)

    def _on_pos_changed(self, position):
        if not position:
            from exception_hook import traceback_uploader
            traceback_uploader()
            return
        if math.isinf(position.x) or math.isinf(position.y) or math.isinf(position.y) or math.isnan(position.x) or math.isnan(position.y) or math.isnan(position.y):
            from exception_hook import traceback_uploader
            traceback_uploader()
            return
        self._position = position
        model = self.get_model()
        if model:
            model.position = position
        if self.enable_debug_pos:
            print(('test--_on_pos_changed--position =', position, '--unit_obj =', self.unit_obj))
            import traceback
            traceback.print_stack()

    def _set_position_auto_move(self, position):
        try:
            self._model.move_to_in_time(position, FORCE_DELTA_TIME_MS, None, None, None, False)
        except:
            self._position = position

        return

    def set_zhujue_model(self, flag):
        self.is_zhujue = flag
        if flag:
            if self.model:
                self.do_set_zhujue(self._model)
        else:
            self.do_set_zhujue(None)
        return

    def do_set_zhujue(self, model):
        world.get_active_scene().set_zhujue(model)

    def set_model_position(self, position):
        model = self.get_model()
        if not model:
            return
        model.position = position
        if self.enable_debug_pos:
            print(('test--set_model_position--position =', position, '--unit_obj =', self.unit_obj))
            import traceback
            traceback.print_stack()

    def _load_callback(self, model, user_data, use_idx, reload_model=False):
        if not self.is_enable(use_idx):
            try:
                if self.NEED_CACHE:
                    model_pool = ModelPool()
                    model_pool.add_free_model(model, self._animator)
                    if self._animator:
                        self._animator.clear_anim_events()
                else:
                    model.destroy()
            except Exception as e:
                print('[_load_callback] model has been remove form sceen %s' % self.__class__.__name__, '--error = ', str(e))
                import traceback
                traceback.print_stack()

            print(('test--_load_callback--step1--call_use_idx =', use_idx, '--cur_use_idx =', self.use_idx, '--is_active =', is_active, '--_is_valid =', _is_valid, '--unit_obj -', self.unit_obj))
            return
        else:
            if type(user_data) is dict:
                custom_model_name = user_data.get('custom_model_name', None)
                custom_model_name_prefix = user_data.get('custom_model_name_prefix', None)
                if custom_model_name:
                    model.name = custom_model_name
                    model.set_attr('model_name', custom_model_name_prefix)
            if self.sd.ref_is_refreshing_whole_model and self._model:
                self._model.destroy()
            self._model = model
            self._start_load_model_time = 0
            if not self.ev_g_is_avatar():
                self._cached_bdict = None
            if reload_model:
                print(('test--_load_callback--step3--model.filename =', model.filename, '--unit_obj =', self.unit_obj))
                return
            if model:
                if hasattr(model, 'enable_dynamic_culling') and self.ev_g_is_avatar():
                    model.enable_dynamic_culling(False)
                if global_data.enable_other_model_shadowmap or self.ev_g_is_avatar():
                    if hasattr(model, 'cast_shadow'):
                        model.cast_shadow = True
                    if hasattr(model, 'receive_shadow'):
                        model.receive_shadow = True
                    if global_data.debug_perf_switch_global:
                        avatar_visible = global_data.get_debug_perf_val('enable_avatar_model', True)
                        model.visible = avatar_visible
                if not model.get_scene():
                    scene = self.scene
                    if scene:
                        scene.add_object(model)
                self.set_model_position(self._position)
                if not self.sd.ref_is_refreshing_whole_model:
                    self._bind_event(self.BIND_LOAD_FINISH_EVENT)
                    if self._is_unbind_model_event:
                        self._unbind_event(self._save_unbind_model_event)
                        self._save_unbind_model_event = []
                        self._is_unbind_model_event = False
                self.on_load_model_complete(model, user_data)
                self.send_event('E_MODEL_LOADED', self._model)
                if self.is_zhujue:
                    self.do_set_zhujue(self._model)
                if hasattr(model, 'decal_recievable'):
                    self._model.decal_recievable = False
            return

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        import common.utilities
        col_type = kwargs.get('col_type', None)
        global_data.sound_mgr.play_sound_optimize('Play_bullet_hit', self.unit_obj, end_pos, ('bullet_hit_material',
                                                                                              'metal'))
        if check_need_ignore_effect_behind_camera(shot_type, end_pos):
            return
        else:
            if shot_type:
                res_conf = confmgr.get('firearm_res_config', str(shot_type), default={})
                sfx_path = res_conf.get('cSfxHit')
                if sfx_path:
                    ex_data = {}
                    camp_diff_param = res_conf.get('cExtraParam', {}).get('camp_diff', 0)
                    if camp_diff_param and 'trigger_camp_id' in kwargs.get('ext_dict', {}) and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != kwargs['ext_dict']['trigger_camp_id']:
                        if type(camp_diff_param) == str:
                            sfx_path = camp_diff_param
                        else:
                            ex_data['need_diff_process'] = True
                    global_data.sfx_mgr.create_sfx_in_scene(sfx_path, end_pos, duration=0.5, int_check_type=CREATE_SRC_SIMPLE, ex_data=ex_data)
                    return
            hit_sfx_path = ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx')
            if col_type:
                hit_sfx_path = scene_const.collision_sfx_map.get(col_type, hit_sfx_path)
            global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path[0], end_pos, int_check_type=CREATE_SRC_SIMPLE)
            if global_data.game_mgr.gds.get_actual_quality() > 1:
                hit_vect = end_pos - begin_pos
                if hit_vect.is_zero:
                    hit_vect = math3d.vector(0, 0, 1)
                else:
                    hit_vect.normalize()
                check_pos = end_pos - hit_vect * NEOX_UNIT_SCALE * 0.1
                check_dir = hit_vect * NEOX_UNIT_SCALE * 0.3
                if self.model and self.model.valid:
                    result = self.model.hit_by_ray(check_pos, check_dir)
                    if result[0]:
                        pos = check_pos + check_dir * result[1]
                        normal = self.model.get_triangle_normal(result[2], result[3])
                        pos = common.utilities.bullet_pos_offset(pos, normal)

                        def create_cb(sfx):
                            global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

                        global_data.sfx_mgr.create_sfx_for_model(hit_sfx_path[1], self.model, pos, duration=10, on_create_func=create_cb, int_check_type=CREATE_SRC_OTHER_HIT)
            return

    def delay_destroy(self):
        self.is_delay_destroy = True

    def debug_pos(self, enable):
        self.enable_debug_pos = enable

    def __destroy_base_model(self):
        if self.is_zhujue:
            self.do_set_zhujue(None)
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setRefModel(None)
        if self.model:
            self._unbind_event(self.BIND_LOAD_FINISH_EVENT)
            if not self.is_delay_destroy:
                try:
                    self.scene.remove_object(self.model)
                    if self.NEED_CACHE:
                        model_pool = ModelPool()
                        model_pool.add_free_model(self.model, self._animator)
                        if self._animator:
                            self._animator.clear_anim_events()
                    else:
                        self.model.destroy()
                except Exception as e:
                    print('model has been remove form sceen %s' % self.__class__.__name__, '--error = ', str(e))
                    import traceback
                    traceback.print_stack()

            self._model = None
        else:
            self._unbind_event(self.BIND_LOAD_FINISH_EVENT)
            self._model = None
        self.send_event('E_MODEL_DESTROY')
        return

    def destroy(self):
        self.load_res_func = None
        self.on_model_destroy()
        if self.res_loader_mgr:
            self.res_loader_mgr.destroy()
            self.res_loader_mgr = None
        self.__destroy_base_model()
        if self._using_auto_move:
            new_event = {'E_POSITION': '_set_position_auto_move'}
            self._unbind_event(new_event)
            self._using_auto_move = False
        super(ComBaseModelAppearance, self).destroy()
        return

    def on_model_destroy(self):
        pass

    def on_load_model_complete(self, model, user_data):
        pass

    def on_load_animator_complete(self, *args):
        pass

    def _enable_bind_event(self, flag, elist=None):
        super(ComBaseModelAppearance, self)._enable_bind_event(flag, elist)
        einfo = {}
        if elist is None:
            einfo = self.BIND_LOAD_FINISH_EVENT
        else:
            bind_events = self.BIND_LOAD_FINISH_EVENT
            for ename in elist:
                if ename in bind_events:
                    einfo[ename] = bind_events[ename]

        if self._model:
            if flag:
                self._bind_event(einfo)
            else:
                self._unbind_event(einfo)
        else:
            if flag:
                for key, value in six.iteritems(einfo):
                    if key in self._save_unbind_model_event:
                        del self._save_unbind_model_event[key]

            else:
                for key, value in six.iteritems(einfo):
                    if key not in self._save_unbind_model_event:
                        self._save_unbind_model_event[key] = value

            self._is_unbind_model_event = True if self._save_unbind_model_event else False
        return

    def rebind_event--- This code section failed: ---

 765       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'ComBaseModelAppearance'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'rebind_event'
          15  CALL_FUNCTION_0       0 
          18  POP_TOP          

 766      19  LOAD_GLOBAL           3  'getattr'
          22  LOAD_GLOBAL           1  'ComBaseModelAppearance'
          25  LOAD_GLOBAL           4  'False'
          28  CALL_FUNCTION_3       3 
          31  POP_JUMP_IF_FALSE    78  'to 78'
          34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             5  '_model'
        40_0  COME_FROM                '31'
          40  POP_JUMP_IF_FALSE    78  'to 78'

 767      43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             6  '_unbind_event'
          49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             7  'BIND_LOAD_FINISH_EVENT'
          55  CALL_FUNCTION_1       1 
          58  POP_TOP          

 768      59  LOAD_FAST             0  'self'
          62  LOAD_ATTR             8  '_bind_event'
          65  LOAD_FAST             0  'self'
          68  LOAD_ATTR             7  'BIND_LOAD_FINISH_EVENT'
          71  CALL_FUNCTION_1       1 
          74  POP_TOP          
          75  JUMP_FORWARD          0  'to 78'
        78_0  COME_FROM                '75'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 28