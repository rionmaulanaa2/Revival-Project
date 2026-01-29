# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/sfxmgr.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import world
import game3d
import math3d
import time
from common.framework import Singleton, Functor
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.pool_mgr import SfxPoolMgr, BulletSfxPoolMgr
from data.constant_break_data import data as constant_break_list
from logic.gutils.effect_utils import get_decal_tot_count, init_decal_attr, handle_sfx_differentiation_process
from logic.gcommon.common_const.collision_const import GLASS_GROUP
from common.utils.timer import Timer, LOGIC, CLOCK, RELEASE
from common.cfg import confmgr
CREATE_SRC_NORMAL = 1
CREATE_SRC_SIMPLE = 8
CREATE_SRC_ONE = 11
CREATE_SRC_OTHER_SYNC = 2
CREATE_SRC_OTHER_SYNC_FREQUENT = 9
CREATE_SRC_OTHER_SYNC_SHOTGUN = 3
CREATE_SRC_OTHER_HIT = 4
CREATE_SRC_MINE_HIT = 5
CREATE_SRC_OTHER_EXPLODE = 6
CREATE_SRC_MINE_EXPLODE = 7
CREATE_SRC_OTHER_EX_EXPLODE = 11
CREATE_SRC_MINE_EX_EXPLODE = 12
CREATE_SRC_MINE_RAY_GUN_CRATER = 10
MAX_LIMIT = 100000 * NEOX_UNIT_SCALE
CREATE_INTENSITY_INFO = {CREATE_SRC_NORMAL: (
                     (
                      MAX_LIMIT, 1 * NEOX_UNIT_SCALE, MAX_LIMIT),),
   CREATE_SRC_SIMPLE: (
                     (
                      30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 2), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 2)),
   CREATE_SRC_ONE: (
                  (
                   MAX_LIMIT, MAX_LIMIT, 1),),
   CREATE_SRC_OTHER_SYNC: (
                         (
                          30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 2), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 2)),
   CREATE_SRC_OTHER_SYNC_FREQUENT: (
                                  (
                                   30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 3), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 5)),
   CREATE_SRC_OTHER_SYNC_SHOTGUN: (
                                 (
                                  30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 5), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 5)),
   CREATE_SRC_MINE_HIT: (
                       (
                        MAX_LIMIT, 1 * NEOX_UNIT_SCALE, MAX_LIMIT),),
   CREATE_SRC_OTHER_HIT: (
                        (
                         30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 2), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 2)),
   CREATE_SRC_MINE_EXPLODE: (
                           (
                            MAX_LIMIT, 1 * NEOX_UNIT_SCALE, MAX_LIMIT),),
   CREATE_SRC_OTHER_EXPLODE: (
                            (
                             30 * NEOX_UNIT_SCALE, 2 * NEOX_UNIT_SCALE, 2), (MAX_LIMIT, 5 * NEOX_UNIT_SCALE, 2)),
   CREATE_SRC_MINE_EX_EXPLODE: (
                              (
                               MAX_LIMIT * NEOX_UNIT_SCALE, (NEOX_UNIT_SCALE, 3 * NEOX_UNIT_SCALE), (1, 2)),),
   CREATE_SRC_OTHER_EX_EXPLODE: (
                               (
                                MAX_LIMIT * NEOX_UNIT_SCALE, 3 * NEOX_UNIT_SCALE, 1),),
   CREATE_SRC_MINE_RAY_GUN_CRATER: (
                                  (
                                   MAX_LIMIT, NEOX_UNIT_SCALE, 6),)
   }
SfxSuffixDistortion = '_distortion.sfx'

class SfxMgr(Singleton):
    ALIAS_NAME = 'sfx_mgr'
    MAX_SFX_ID = 1000000000
    DECAL_Y_HEIGHT = 1.5 * NEOX_UNIT_SCALE
    POOL_MGR = SfxPoolMgr()

    def init(self):
        self._sfx_loading_cfgs = {}
        self._sfx_loaded_cfgs = {}
        self._sfx_ids = {}
        self._sfx_decal_ttl_timers = {}
        self._sfx_intensity_info = {}
        self._bug_sfx_paths_when_cached = set()
        self._enable_sfx_pool = not global_data.force_disable_sfx_cache
        self._cur_sfx_id = 0
        self._init_post_sfx_info()
        self._init_decal_sfx_info()

    def on_finalize(self):
        SfxMgr.POOL_MGR = None
        return

    def remove_all_sfx(self):
        keys = six_ex.keys(self._sfx_loading_cfgs)
        for sfx_id in keys:
            self.remove_sfx_by_id(sfx_id)

        keys = six_ex.keys(self._sfx_loaded_cfgs)
        for sfx_id in keys:
            self.remove_sfx_by_id(sfx_id)

    def clean_up_invalid(self):
        to_remove_id_list = []
        for sfx_id, (sfx, _, _, _, _, _) in six.iteritems(self._sfx_loaded_cfgs):
            if not (sfx and sfx.valid):
                to_remove_id_list.append(sfx_id)

        for sfx_id in to_remove_id_list:
            self.remove_sfx_by_id(sfx_id)

        self.clean_up_invalid_intensity_info()

    def clean_up_invalid_intensity_info(self):
        for sfx_info in six.itervalues(self._sfx_intensity_info):
            to_remove_ids = []
            for sfx_id in six.iterkeys(sfx_info):
                if sfx_id not in self._sfx_loaded_cfgs:
                    to_remove_ids.append(sfx_id)

            for sfx_id in to_remove_ids:
                sfx_info.pop(sfx_id, None)

        return

    def _on_add_intensity_info(self, sfx_path, sfx_id, sfx_world_pos):
        self._sfx_intensity_info.setdefault(sfx_path, {})
        self._sfx_intensity_info[sfx_path][sfx_id] = (sfx_world_pos, global_data.game_time)

    def _on_before_remove_intensity_info(self, sfx_path, sfx_id):
        item_info = self._sfx_intensity_info.get(sfx_path, None)
        if item_info is None:
            return
        else:
            item_info.pop(sfx_id, None)
            return

    def check_sfx_intensity(self, sfx_path, world_pos, int_check_type):
        if not global_data.cam_lplayer:
            return (True, 0)
        if sfx_path not in self._sfx_intensity_info:
            return (True, 0)
        player_pos = global_data.cam_lplayer.ev_g_position()
        dist_to_player = 0
        if player_pos:
            dist_to_player = (world_pos - player_pos).length
        intensity_check_info = CREATE_INTENSITY_INFO[int_check_type]
        for circle_limit, dist_limit, cnt_limit in intensity_check_info:
            if dist_to_player < circle_limit:
                check_dist = dist_limit
                check_limit = cnt_limit
                break
        else:
            return (
             True, 0)

        item_info = self._sfx_intensity_info[sfx_path]
        ret, oldest_sfx_id = True, 0
        if type(check_dist) is tuple:
            in_area_cnt = [ 0 for i in check_dist ]
            oldest_born_time = 0
            for sfx_id, (pos, born_time) in six.iteritems(item_info):
                if ret:
                    dist = (world_pos - pos).length
                    for index, _check_dist in enumerate(check_dist):
                        _check_limit = check_limit[index]
                        if dist < _check_dist:
                            in_area_cnt[index] += 1
                            if in_area_cnt[index] >= _check_limit:
                                ret = False
                                break

                if born_time > oldest_born_time:
                    oldest_born_time = born_time
                    oldest_sfx_id = sfx_id

        else:
            in_area_cnt = 0
            oldest_born_time = 0
            for sfx_id, (pos, born_time) in six.iteritems(item_info):
                if ret:
                    dist = (world_pos - pos).length
                    if dist < check_dist:
                        in_area_cnt += 1
                        if in_area_cnt >= check_limit:
                            ret = False
                if born_time > oldest_born_time:
                    oldest_born_time = born_time
                    oldest_sfx_id = sfx_id

        return (
         ret, oldest_sfx_id)

    @property
    def enable_sfx_pool--- This code section failed: ---

 208       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    @enable_sfx_pool.setter
    def enable_sfx_pool(self, value):
        self._enable_sfx_pool = value and not global_data.force_disable_sfx_cache

    def create_sfx_in_scene(self, sfx_path, pos=math3d.vector(0, 0, 0), duration=0, on_create_func=None, on_remove_func=None, ex_data={}, int_check_type=None, int_check_pos=None, create_scene=None):
        sfx_path = sfx_path.strip()
        if not create_scene:
            target_scene = global_data.game_mgr.scene if 1 else create_scene
            return target_scene or None
        else:
            if int_check_type and int_check_type != CREATE_SRC_NORMAL:
                if int_check_pos is not None:
                    my_pos = int_check_pos if 1 else pos
                    pass_flag, oldest_sfx_id = self.check_sfx_intensity(sfx_path, my_pos, int_check_type)
                    new_sfx_id = pass_flag or self._trans_sfx_by_id(sfx_path, oldest_sfx_id, target_scene, pos, duration, on_create_func, on_remove_func, ex_data)
                    if new_sfx_id != -1:
                        return new_sfx_id

            def on_create_sfx_in_scene(sfx, sfx_id, need_restart):
                if not create_scene:
                    cur_scene = global_data.game_mgr.scene if 1 else create_scene
                    if cur_scene and cur_scene.valid and cur_scene is target_scene:
                        cur_scene.add_object(sfx)
                        if need_restart:
                            sfx.restart()
                        sfx.world_position = pos
                        handle_sfx_differentiation_process(sfx, ex_data)
                        if on_create_func:
                            on_create_func(sfx)
                        self._on_after_create_decal_sfx(sfx, sfx_id, duration, ex_data) or self.remove_sfx(sfx)
                else:
                    self.remove_sfx(sfx)

            return self._create_sfx(sfx_path, duration, on_create_sfx_in_scene, on_remove_func, ex_data)

    def create_sfx_on_model(self, sfx_path, model, socket, type=world.BIND_TYPE_DEFAULT, duration=0, on_create_func=None, on_remove_func=None, ex_data={}, int_check_type=None, int_check_pos=None):
        sfx_path = sfx_path.strip()
        if not model or not model.valid:
            return
        if not model.has_socket(socket):
            log_error('model:[%s]\xe4\xb8\x8a\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9[%s]\xef\xbc\x8c\xe7\x89\xb9\xe6\x95\x88[%s]\xe6\x8c\x82\xe6\x8e\xa5\xe5\xa4\xb1\xe8\xb4\xa5\xe3\x80\x82' % (model.filename, socket, sfx_path))
            return

        def _on_create_sfx_on_model(sfx, sfx_id, need_restart):
            if model.valid:
                ret = model.bind(socket, sfx, type)
                if need_restart:
                    if not sfx.get_scene():
                        print('=======================================================================')
                        print('gzlaofeng@ [ERROR] \xe8\xbf\x99\xe4\xb8\xaa\xe6\x97\xb6\xe5\x80\x99\xef\xbc\x8c\xe7\x89\xb9\xe6\x95\x88\xe7\xab\x9f\xe7\x84\xb6\xe8\xbf\x98\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe8\xaf\xb4\xe6\x98\x8e\xe5\x8f\xaf\xe8\x83\xbdobject\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf')
                        print('\xe5\xa6\x82\xe6\x9e\x9c\xe7\x89\xb9\xe6\x95\x88\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe9\x82\xa3\xe4\xb9\x88\xe4\xbd\xa0\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\x8b\xe5\x8a\xa8restart\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe7\x89\xb9\xe6\x95\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe4\xbb\x8ecache\xe6\x8b\xbf\xe5\x87\xba\xe6\x9d\xa5\xe7\x9a\x84\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xe6\x89\x8d\xe8\x83\xbdrestart\xe6\x88\x90\xe5\x8a\x9f')
                        import traceback
                        traceback.print_stack()
                        print('bind result:', ret)
                        print('=======================================================================')
                    else:
                        sfx.restart()
                handle_sfx_differentiation_process(sfx, ex_data)
                if on_create_func:
                    on_create_func(sfx)
            else:
                self.remove_sfx(sfx)

        return self._create_sfx(sfx_path, duration, _on_create_sfx_on_model, on_remove_func, ex_data)

    def create_sfx_for_model(self, sfx_path, model, pos=math3d.vector(0, 0, 0), duration=0, on_create_func=None, on_remove_func=None, ex_data={}, int_check_type=None, int_check_pos=None):
        sfx_path = sfx_path.strip()
        if not (model and model.valid):
            return
        else:
            if int_check_type and int_check_type != CREATE_SRC_NORMAL:
                if int_check_pos is not None:
                    my_pos = int_check_pos if 1 else pos
                    pass_flag, oldest_sfx_id = self.check_sfx_intensity(sfx_path, my_pos, int_check_type)
                    pass_flag or self.remove_sfx_by_id(oldest_sfx_id)

            def _on_create_sfx_for_model(sfx, sfx_id, need_restart):
                if model.valid:
                    sfx.set_parent(model)
                    sfx.position = pos
                    if need_restart:
                        if not sfx.get_scene():
                            print('=======================================================================')
                            print('gzlaofeng@ [ERROR] \xe8\xbf\x99\xe4\xb8\xaa\xe6\x97\xb6\xe5\x80\x99\xef\xbc\x8c\xe7\x89\xb9\xe6\x95\x88\xe7\xab\x9f\xe7\x84\xb6\xe8\xbf\x98\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe8\xaf\xb4\xe6\x98\x8e\xe5\x8f\xaf\xe8\x83\xbdobject\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf')
                            print('\xe5\xa6\x82\xe6\x9e\x9c\xe7\x89\xb9\xe6\x95\x88\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe9\x82\xa3\xe4\xb9\x88\xe4\xbd\xa0\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\x8b\xe5\x8a\xa8restart\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe7\x89\xb9\xe6\x95\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe4\xbb\x8ecache\xe6\x8b\xbf\xe5\x87\xba\xe6\x9d\xa5\xe7\x9a\x84\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xaf\xe6\x89\x8d\xe8\x83\xbdrestart\xe6\x88\x90\xe5\x8a\x9f')
                            import traceback
                            traceback.print_stack()
                            print('=======================================================================')
                        else:
                            sfx.restart()
                    handle_sfx_differentiation_process(sfx, ex_data)
                    if on_create_func:
                        on_create_func(sfx)
                else:
                    self.remove_sfx(sfx)

            return self._create_sfx(sfx_path, duration, _on_create_sfx_for_model, on_remove_func, ex_data)

    def remove_sfx(self, sfx):
        sfx_id = self._sfx_ids.get(sfx, None)
        if sfx_id in self._sfx_loading_cfgs:
            del self._sfx_loading_cfgs[sfx_id]
        sfx = self._on_before_remove_sfx(sfx=sfx, sfx_id=sfx_id)
        if sfx and sfx.valid:
            sfx.destroy()
        return

    def remove_sfx_by_id(self, sfx_id):
        if sfx_id in self._sfx_loading_cfgs:
            del self._sfx_loading_cfgs[sfx_id]
        sfx = self._on_before_remove_sfx(sfx_id=sfx_id)
        if sfx and sfx.valid:
            sfx.destroy()

    def get_sfx_by_id(self, sfx_id):
        if sfx_id in self._sfx_loaded_cfgs:
            sfx, sfx_path, duration, on_remove_func, timer, ex_data = self._sfx_loaded_cfgs[sfx_id]
            if sfx and sfx.valid:
                return sfx

    def shutdown_sfx(self, sfx):

        def delay_shutdown():
            sfx_id = self._sfx_ids.get(sfx, None)
            if sfx_id in self._sfx_loading_cfgs:
                del self._sfx_loading_cfgs[sfx_id]
            if sfx and sfx.valid:
                sfx.shutdown(False)
            return

        global_data.game_mgr.sync_exec(delay_shutdown)

    def shutdown_sfx_by_id(self, sfx_id):
        if sfx_id in self._sfx_loading_cfgs:
            del self._sfx_loading_cfgs[sfx_id]
        sfx_cfg = self._sfx_loaded_cfgs.get(sfx_id)
        if sfx_cfg:
            sfx = sfx_cfg[0]
            if sfx and sfx.valid:
                sfx.shutdown(False)

    def restart_sfx_by_id(self, sfx_id):
        if sfx_id not in self._sfx_loaded_cfgs:
            return
        sfx_cfg = self._sfx_loaded_cfgs.get(sfx_id)
        if sfx_cfg:
            sfx = sfx_cfg[0]
            if sfx and sfx.valid:
                sfx.restart()

    @staticmethod
    def set_rotation_by_pivot(sfx, pivot, radius):
        transform_matrix = sfx.transformation
        rotation1 = math3d.matrix.make_rotation_between(math3d.vector(0, 1, 0), pivot)
        rotation2 = math3d.matrix.make_rotation(pivot, radius)
        transform_matrix.rotation = rotation1 * rotation2
        sfx.transformation = transform_matrix

    @staticmethod
    def set_rotation_by_normal(sfx, normal):
        if not normal or normal.is_zero:
            return
        transform_matrix = sfx.transformation
        rotation = math3d.matrix.make_rotation_between(math3d.vector(0, 1, 0), normal)
        transform_matrix.rotation = rotation
        sfx.transformation = transform_matrix

    @staticmethod
    def set_rotation_by_world_normal(sfx, normal):
        if not normal or normal.is_zero:
            return
        transform_matrix = sfx.world_transformation
        rotation = math3d.matrix.make_rotation_between(math3d.vector(0, 1, 0), normal)
        transform_matrix.rotation = rotation
        sfx.world_transformation = transform_matrix

    @staticmethod
    def set_rotation_by_world_normal_ex(sfx, normal):
        if not normal or normal.is_zero:
            return
        sfx.rotation_matrix = math3d.matrix.make_orient(normal, math3d.vector(0, 1, 0))

    @staticmethod
    def set_rotation(sfx, rotation):
        transform_matrix = sfx.transformation
        transform_matrix.rotation = rotation
        sfx.transformation = transform_matrix

    def _create_sfx(self, sfx_path, duration=0, on_create_func=None, on_remove_func=None, ex_data={}, sfx_instance=None):
        from logic.gutils import scene_utils
        sfx_path = scene_utils.scene_replace_res(sfx_path)
        sfx = sfx_instance
        if self._enable_sfx_pool and sfx is None:
            sfx = self.POOL_MGR.get_item(sfx_path)
        sfx_id = self._gen_sfx_id()
        if sfx and sfx.valid:
            self._sfx_loading_cfgs[sfx_id] = (
             sfx_path, duration, on_create_func, on_remove_func, ex_data)
            self._on_after_create_sfx(sfx, sfx_id, None)
        else:
            priority = ex_data.get('priority', game3d.ASYNC_MID) if ex_data else game3d.ASYNC_MID
            world.create_sfx_async(sfx_path, self._on_after_create_sfx, sfx_id, priority)
            self._sfx_loading_cfgs[sfx_id] = (sfx_path, duration, on_create_func, on_remove_func, ex_data)
        return sfx_id

    def _gen_sfx_id(self):
        self._cur_sfx_id = (self._cur_sfx_id + 1) % SfxMgr.MAX_SFX_ID
        return self._cur_sfx_id

    def _on_after_create_sfx(self, sfx, sfx_id, cur_task):
        if sfx_id not in self._sfx_loading_cfgs:
            self.remove_sfx(sfx)
            return
        else:
            if sfx is None:
                self.remove_sfx(sfx)
                return
            sfx_path, duration, on_create_func, on_remove_func, ex_data = self._sfx_loading_cfgs[sfx_id]
            del self._sfx_loading_cfgs[sfx_id]
            if duration > 0:
                timer = game3d.delay_exec(duration * 1000, Functor(self.shutdown_sfx, sfx=sfx))
            else:
                timer = None
            self._sfx_loaded_cfgs[sfx_id] = (
             sfx, sfx_path, duration, on_remove_func, timer, ex_data)
            self._sfx_ids[sfx] = sfx_id
            self._on_after_create_post_sfx(sfx_path)
            if not sfx.has_shutdown_event():
                sfx.register_shutdown_event(self.remove_sfx)
            if on_create_func:
                need_restart = True
                on_create_func(sfx, sfx_id, need_restart)
            if sfx and sfx.valid:
                self._on_add_intensity_info(sfx_path, sfx_id, sfx.world_position)
            return

    def _on_before_remove_sfx(self, sfx=None, sfx_id=None, use_now=False):
        if sfx in self._sfx_ids:
            sfx_id = self._sfx_ids[sfx]
            del self._sfx_ids[sfx]
        if sfx_id in self._sfx_loaded_cfgs:
            sfx, sfx_path, duration, on_remove_func, timer, ex_data = self._sfx_loaded_cfgs[sfx_id]
            del self._sfx_loaded_cfgs[sfx_id]
            self._on_before_remove_post_sfx(sfx_path)
            self._on_before_remove_intensity_info(sfx_path, sfx_id)
            if timer is not None:
                game3d.cancel_delay_exec(timer)
        else:
            sfx_path, on_remove_func = (None, None)
        if sfx and sfx.valid:
            self._on_before_remove_decal_sfx(sfx, sfx_id)
            if on_remove_func:
                if callable(on_remove_func):
                    on_remove_func(sfx)
                elif isinstance(on_remove_func, list):
                    on_remove_func[0](sfx, sfx_id)
            if self._enable_sfx_pool and sfx_path is not None and sfx.valid:
                can_cache = True
                if not global_data.feature_mgr.is_particlepolytube_node_count_fixed():
                    if sfx_path not in self._bug_sfx_paths_when_cached:
                        cached_sfx = self.POOL_MGR.get_item(sfx_path)
                        if cached_sfx is None:
                            if self._has_particle_polytube_sub_sfx(sfx):
                                self._bug_sfx_paths_when_cached.add(sfx_path)
                    can_cache = sfx_path not in self._bug_sfx_paths_when_cached
                if can_cache:
                    sfx.unregister_shutdown_event()
                    sfx.visible = True
                    sfx.scale = math3d.vector(1, 1, 1)
                    if use_now:
                        return sfx
                    if sfx.get_state() != world.FX_STATE_SHUTDOWN:
                        sfx.shutdown(True)
                    sfx.remove_from_parent()
                    sfx.world_position = math3d.vector(0, 0, 0)
                    if self.POOL_MGR.add_item(sfx_path, sfx):
                        sfx = None
        return sfx

    def _trans_sfx_by_id(self, sfx_path, sfx_id, scene, pos, duration, on_create_func, on_remove_func, ex_data):
        sfx = self._on_before_remove_sfx(sfx_id=sfx_id, use_now=True)
        if sfx is None or not sfx.valid:
            return -1
        else:
            if scene and scene.valid:

                def create_func_wrapper(sfx, sfx_id, need_restart):
                    if sfx.get_scene() != scene or sfx.get_parent():
                        sfx.remove_from_parent()
                        scene.add_object(sfx)
                    sfx.world_position = pos
                    sfx.restart()
                    handle_sfx_differentiation_process(sfx, ex_data)
                    if on_create_func:
                        on_create_func(sfx)
                    if not self._on_after_create_decal_sfx(sfx, sfx_id, duration, ex_data):
                        self.remove_sfx(sfx)

                return self._create_sfx(sfx_path, duration, create_func_wrapper, on_remove_func, ex_data, sfx)
            return -1

    def _init_post_sfx_info(self):
        self._post_process_sfx_info = {}

    def _on_after_create_post_sfx(self, sfx_path):
        if not sfx_path:
            return
        if sfx_path.endswith(SfxSuffixDistortion):
            self._post_process_sfx_info.setdefault('distortion', 0)
            self._post_process_sfx_info['distortion'] += 1
        self._check_trigger_post_process()

    def _on_before_remove_post_sfx(self, sfx_path):
        if not sfx_path:
            return
        if sfx_path.endswith(SfxSuffixDistortion):
            if self._post_process_sfx_info.get('distortion', 0) > 0:
                self._post_process_sfx_info['distortion'] -= 1
        self._check_trigger_post_process()

    def _check_trigger_post_process(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        for pp_name, cnt in six.iteritems(self._post_process_sfx_info):
            if pp_name == 'distortion':
                scene.enable_distortion(cnt > 0)

    def get_dynamic_decal_sfx_info(self):
        return self._dynamic_decal_sfx_info

    def _init_decal_sfx_info(self):
        self._dynamic_decal_sfx_info = {}
        self._static_decal_sfx_info = {}
        self._decal_count_unit_max = constant_break_list.get(1, {}).get('iLimitNum', 2)
        self._decal_count_check_radius = constant_break_list.get(1, {}).get('iLimitRange', 6.0) * NEOX_UNIT_SCALE
        self._decal_count_fade_radius_min = constant_break_list.get(1, {}).get('iLimitDistance', 4.0) * NEOX_UNIT_SCALE
        self._decal_over_count_time = constant_break_list.get(1, {}).get('fExistTime', 4.0)
        self._decal_fadeout_time = constant_break_list.get(1, {}).get('fClearTime', 2.0)

    def _on_after_create_decal_sfx(self, sfx, sfx_id, duration, ex_data={}):
        if not (sfx and sfx.valid):
            return
        else:
            max_life_time = 0
            decal_tex_size = ex_data.get('decal_tex_size', (0.0, 0.0))
            use_local_uv = ex_data.get('use_local_uv', True)
            intra_tex_path = ex_data.get('intra_tex_path', None)
            col_group = ex_data.get('col_group', None)
            allow_overlay = ex_data.get('allow_overlay', False)
            display_range_limit = ex_data.get('display_range_limit', 0)
            for sub_idx in range(sfx.get_subfx_count()):
                if not sfx.is_sub_decal(sub_idx):
                    continue
                sfx.set_sub_decal_height(sub_idx, SfxMgr.DECAL_Y_HEIGHT)
                self._dynamic_decal_sfx_info[sfx] = math3d.vector(sfx.world_position.x, sfx.world_position.y, sfx.world_position.z)
                fade_radius = display_range_limit if display_range_limit > 0 else self._decal_count_fade_radius_min
                check_radius = display_range_limit if display_range_limit > 0 else self._decal_count_check_radius
                intra_cnt, extra_cnt = get_decal_tot_count(sfx.world_position, self._dynamic_decal_sfx_info, fade_radius, check_radius)
                if intra_cnt > self._decal_count_unit_max:
                    max_life_time = -1
                elif extra_cnt > self._decal_count_unit_max:
                    max_life_time = self._decal_over_count_time
                if max_life_time > 0:
                    decal_life_time = max_life_time if 1 else duration
                    global_data.game_mgr.post_exec(init_decal_attr, sfx, sfx_id, sub_idx, ex_data, decal_tex_size, self._decal_fadeout_time, use_local_uv, intra_tex_path, decal_life_time * 1000, self._sfx_decal_ttl_timers)

            return max_life_time >= 0 or allow_overlay

    def _merge_static_decal_sfx(self, new_sfx, new_sfx_max_decal_radius):
        check_sfx = new_sfx
        to_del_sfx = set([])
        old_center_radius = (None, None)
        new_center_radius = (check_sfx.world_position, new_sfx_max_decal_radius)
        while new_center_radius != old_center_radius:
            old_center_radius = new_center_radius
            for sfx, (_, max_decal_radius) in six.iteritems(self._static_decal_sfx_info):
                if not (sfx and sfx.valid):
                    continue
                if sfx in to_del_sfx:
                    continue
                if sfx == check_sfx:
                    continue
                if (sfx.world_position - check_sfx.world_position).length < old_center_radius[1] + max_decal_radius:
                    to_del_sfx.add(sfx)
                    new_center = (sfx.world_position + check_sfx.world_position) * math3d.vector(0.5, 0.5, 0.5)
                    new_radius = old_center_radius[1] + max_decal_radius
                    new_center_radius = (new_center, new_radius)

        if new_center_radius:
            new_sfx.world_position = new_center_radius[0]
            for sub_idx in range(new_sfx.get_subfx_count()):
                if new_sfx.is_sub_decal(sub_idx):
                    new_sfx.set_sub_sprite_radius(sub_idx, new_center_radius[1])

        for sfx in to_del_sfx:
            self.remove_sfx(sfx)

        return None

    def _on_before_remove_decal_sfx(self, sfx, sfx_id):
        self._dynamic_decal_sfx_info.pop(sfx, None)
        self._static_decal_sfx_info.pop(sfx, None)
        sfx_ttl_timer_group = self._sfx_decal_ttl_timers.get(sfx_id, {})
        for timer_id in six.itervalues(sfx_ttl_timer_group):
            game3d.cancel_delay_exec(timer_id)

        self._sfx_decal_ttl_timers.pop(sfx_id, None)
        return

    def print_debug_info(self):
        print('=============================================')
        print('[INFO] mgr loaded sfx:', len(self._sfx_loaded_cfgs))
        for sfx_id, cfg in six.iteritems(self._sfx_loaded_cfgs):
            if cfg[0].valid:
                print('\t', sfx_id, cfg)
            else:
                print('\t', sfx_id, 'no_sfx', cfg[1])

        print('[INFO] mgr loading sfx', len(self._sfx_loading_cfgs))
        for sfx_id, cfg in six.iteritems(self._sfx_loading_cfgs):
            print('\t', sfx_id, cfg)

        print('[INFO] print_debug_info:')
        print('\tsfx count: {}'.format(world.get_active_scene().get_sfx_count()))
        print('\tcache sfx:')
        for k, v in six.iteritems(self.POOL_MGR.get_cached_sfx_map()):
            print('\t\t{}: {}'.format(k, v))

        print('=============================================')

    @staticmethod
    def _has_particle_polytube_sub_sfx(sfx):
        if sfx and sfx.valid:
            cnt = sfx.get_subfx_count()
            if cnt <= 0:
                return False
            types = [ sfx.get_sub_type(i) for i in range(cnt) ]
            for t in types:
                if t == world.FX_TYPE_PARTILCEPOLYTUBE:
                    return True

        return False


def _shutdown_callback(sfx):
    SfxMgr().remove_sfx(sfx)


class BulletSfxMgr(SfxMgr):
    ALIAS_NAME = 'bullet_sfx_mgr'
    POOL_MGR = BulletSfxPoolMgr()
    TRIGGER_RELEASE_INTERVAL = 60
    DEL_INTERVAL = 5

    def init(self):
        super(BulletSfxMgr, self).init()
        self.auto_release_timer = None
        return

    def on_finalize(self):
        BulletSfxMgr.POOL_MGR = None
        if self.auto_release_timer:
            global_data.game_mgr.unregister_logic_timer(self.auto_release_timer)
            self.auto_release_timer = None
        return

    def _auto_release(self, need_update_interval=False):
        if BulletSfxMgr.POOL_MGR.check_auto_release(BulletSfxMgr.DEL_INTERVAL):
            self.auto_release_timer = None
            return RELEASE
        else:
            if need_update_interval:
                timer = global_data.game_mgr.get_logic_timer()
                timer.set_interval(self.auto_release_timer, BulletSfxMgr.DEL_INTERVAL)
                timer.set_args(self.auto_release_timer, (False,))
            return

    def _create_sfx(self, *args, **kwargs):
        if self.auto_release_timer:
            global_data.game_mgr.get_logic_timer().set_interval(self.auto_release_timer, BulletSfxMgr.TRIGGER_RELEASE_INTERVAL)
        else:
            self.auto_release_timer = global_data.game_mgr.register_logic_timer(self._auto_release, interval=BulletSfxMgr.TRIGGER_RELEASE_INTERVAL, args=(True,), times=-1, mode=CLOCK)
        return super(BulletSfxMgr, self)._create_sfx(*args, **kwargs)

    def refresh_auto_release_timer(self):
        if self.auto_release_timer:
            self.auto_release_timer = global_data.game_mgr.register_logic_timer(self._auto_release, interval=BulletSfxMgr.TRIGGER_RELEASE_INTERVAL, args=(True,), times=-1, mode=CLOCK)