# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ResourceManager.py
from __future__ import absolute_import
from __future__ import print_function
import weakref
import game3d
import math3d
import common.utils.timer as timer
import math
import time
import six
RES_TYPE_MODEL = 0
RES_TYPE_SFX = 1
RES_TYPE_UNKNOWN = 2
from common.framework import Singleton
from common.utils.time_utils import get_time
from common.utils.pool_mgr import ResRefPoolMgr

class ResourceManager(Singleton):
    FRAME_SECOND = 1.0 / 30.0
    MIN_COMPLETE_NUM = 2
    MAX_UPDATE_DURATION = FRAME_SECOND

    def init(self):
        self.complete_list = []
        self._res_timer_id = 0
        self._wait_frame_count = 0
        self._is_log = False

    def add_complete_res(self, model, callback_info):
        path = None
        if model:
            path = model.filename
        self.complete_list.append((model, callback_info))
        if self._res_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._res_timer_id)
            self._res_timer_id = 0
        self._res_timer_id = global_data.game_mgr.register_logic_timer(self.post_logic_update, self.FRAME_SECOND, times=-1, mode=timer.CLOCK)
        return

    def post_logic_update(self, *arg):
        if self._is_log:
            print(('test--ResourceManager.post_logic_update--step1--len(complete_list) =', len(self.complete_list), '--_res_timer_id =', self._res_timer_id))
        if not self.complete_list:
            if self._res_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._res_timer_id)
                self._res_timer_id = 0
            if self._is_log:
                print('test--ResourceManager.post_logic_update--step2')
            return
        if self._wait_frame_count > 0:
            if self._is_log:
                print(('test--ResourceManager.post_logic_update--step3--_wait_frame_count =', self._wait_frame_count))
            self._wait_frame_count -= 1
            return
        leave_time = self.MAX_UPDATE_DURATION
        start_time = get_time()
        pass_time = 0
        while pass_time <= leave_time:
            if not self.complete_list:
                break
            if self._is_log:
                print(('test--ResourceManager.post_logic_update--step4--len(complete_list) =', len(self.complete_list), '--pass_time =', pass_time, '--leave_time =', leave_time))
            first_elem = self.complete_list.pop(0)
            model, callback_info = first_elem
            cb_func, cb_data = callback_info
            one_model_start_time = get_time()
            cb_func(model, cb_data)
            now_time = get_time()
            one_model_pass_time = now_time - one_model_start_time
            if one_model_pass_time > self.FRAME_SECOND:
                self._wait_frame_count = math.ceil(one_model_pass_time / self.FRAME_SECOND) + 2
            pass_time = now_time - start_time


class ResLoader(object):

    def __init__(self, mpath, callback, cb_data, res_type=RES_TYPE_MODEL, sync_priority=game3d.ASYNC_MID, merge_info=None, valid_checker=None):
        self.callback_info = (callback, cb_data)
        self.is_valid = True
        self.is_loaded = False
        self.load_task = None
        self.mpath = mpath
        self.res_type = res_type
        self.valid_checker = valid_checker
        self.load(sync_priority, merge_info)
        return

    def load(self, sync_priority, merge_info=None):
        import world
        if not self.is_loaded:
            if self.res_type == RES_TYPE_MODEL:
                self.load_task = world.create_model_async(self.mpath, self._load_complete, None, sync_priority, merge_info)
            elif self.res_type == RES_TYPE_UNKNOWN:
                self.load_task = world.create_res_object_async(self.mpath, self._load_complete, None, sync_priority)
            else:
                self.load_task = world.create_sfx_async(self.mpath, self._load_complete)
            self.is_loaded = True
        return

    def _load_complete(self, model, udata=None, current_task=None):
        if not self.is_valid:
            return
        else:
            if isinstance(self, ResLoader):
                self.load_task = None
                if global_data.enable_res_ref_cache and not global_data.is_low_mem_mode:
                    ResRefPoolMgr().add_item(self.mpath, model)
                if not self.is_valid:
                    if getattr(model, 'destroy', None):
                        model.destroy()
                    self.destroy()
                    return
                is_valid = True
                if self.valid_checker:
                    is_valid = self.valid_checker()
                if is_valid and self.callback_info:
                    if self.res_type == RES_TYPE_MODEL:
                        if hasattr(model, 'auto_cut_bones') and game3d.is_feature_ready('FixAllAutoCutBone'):
                            model.auto_cut_bones = True
                        self._setup_model_outline(model)
                        res_mgr = ResourceManager()
                        res_mgr.add_complete_res(model, self.callback_info)
                    else:
                        cb_func, cb_data = self.callback_info
                        cb_func(model, cb_data)
                else:
                    model.destroy()
                self.destroy()
            return

    def _setup_model_outline(self, model):
        pass

    def destroy(self):
        if self.load_task:
            if getattr(self.load_task, 'valid', None):
                self.load_task.cancel()
            if getattr(self.load_task, 'state', None):
                if self.load_task.state != game3d.STATE_FAILED:
                    self.load_task.cancel()
            self.load_task = None
        self.is_valid = False
        self.callback_info = None
        self.mpath = None
        return


class SimpleCall(object):

    def __init__(self, cb, cb_data):
        self.cb = cb
        self.cb_data = cb_data

    def __call__(self, model):
        self.cb(model, self.cb_data)
        self.cb, self.cb_data = (None, None)
        return None


class BindCall(object):

    def __init__(self, method, instance, cb_data):
        self.method = weakref.ref(method)
        self.inst = weakref.ref(instance)
        self.cb_data = cb_data

    def __call__(self, model):
        method = self.method()
        inst = self.inst()
        if method and inst:
            method(inst, model, self.cb_data)
        self.method, self.inst, self.cb_data = (None, None, None)
        return None


class ModelPool(Singleton):
    MAX_MODEL_KEEP_TIME = 60
    FIX_UPDATE_INTERVAL = 2

    def init(self):
        self._model_dict = {}
        self._update_timer_id = None
        return

    def add_free_model(self, model, animator=None, is_reset_material=True):
        if global_data.force_disable_model_cache:
            return
        if not model or not model.valid:
            return
        if not self._model_dict and not self._update_timer_id:
            self._update_timer_id = global_data.game_mgr.register_logic_timer(self.fixed_update, self.FIX_UPDATE_INTERVAL, times=-1, mode=timer.CLOCK)
        if animator:
            animator.reset()
        model_info = (model, animator, time.time())
        path = model.filename
        path = path.replace('\\', '/')
        model.visible = False
        model.unbind_all_col_obj()
        animator_dict = self._model_dict.setdefault(path, {})
        animator_path = ''
        if animator:
            animator_path = animator.GetXmlFile()
        animator_list = animator_dict.setdefault(animator_path, [])
        animator_list.append(model_info)
        if is_reset_material:
            model.all_materials.reset(True, True)

    def del_free_model(self, path):
        path = path.replace('\\', '/')
        animator_dict = self._model_dict.get(path, None)
        if not animator_dict:
            return
        else:
            for animator_list in six.itervalues(animator_dict):
                for index, model_info in enumerate(animator_list):
                    model, animator, start_time = model_info
                    if model.valid:
                        model.destroy()
                    if animator:
                        animator.destroy()

            del self._model_dict[path]
            return

    def get_free_model(self, path, animator_path=''):
        if not self._model_dict:
            return (None, None)
        else:
            path = path.replace('\\', '/')
            animator_dict = self._model_dict.get(path, None)
            if not animator_dict:
                return (None, None)
            animator_list = animator_dict.setdefault(animator_path, [])
            if not animator_list:
                return (None, None)
            model, animator, start_time = animator_list[0]
            animator_list.pop(0)
            if not model.valid:
                return (None, None)
            if path == 'model_new/niudan/6008_skate.gim':
                return (None, None)
            model.scale = math3d.vector(1, 1, 1)
            model.world_rotation_matrix.set_identity()
            model.position = math3d.vector(0, 0, 0)
            model.visible = True
            return (
             model, animator)

    def fixed_update(self, *args):
        if not self._model_dict:
            self._update_timer_id = None
            return timer.RELEASE
        else:
            now_time = time.time()
            for animator_dict in six.itervalues(self._model_dict):
                for animator_list in six.itervalues(animator_dict):
                    for index, model_info in enumerate(animator_list):
                        model, animator, start_time = model_info
                        pass_time = now_time - start_time
                        if pass_time > self.MAX_MODEL_KEEP_TIME:
                            if model.valid:
                                model.destroy()
                            if animator:
                                animator.destroy()
                            animator_list.pop(index)
                        break

            for path, animator_dict in six.iteritems(self._model_dict):
                if not animator_dict:
                    del self._model_dict[path]
                    break
                for animator_path, animator_list in six.iteritems(animator_dict):
                    if not animator_list:
                        del animator_dict[animator_path]
                        break

            return

    def clear(self):
        for animator_dict in six.itervalues(self._model_dict):
            for animator_list in six.itervalues(animator_dict):
                for index, model_info in enumerate(animator_list):
                    model, animator, start_time = model_info
                    if model.valid:
                        model.destroy()
                    if animator:
                        animator.destroy()

                del animator_list[:]

        self._model_dict.clear()


class ResLoaderMgr(object):

    def __init__(self):
        self.task = {}
        self.load_id = 0

    def add_load_task(self, mpath, callback, cb_data=None, res_type=RES_TYPE_MODEL, sync_priority=game3d.ASYNC_LOW, merge_info=None, valid_checker=None):
        self.load_id += 1
        im_func = getattr(callback, six._meth_func, None)
        im_self = getattr(callback, six._meth_self, None)
        if im_func and im_self:
            handler = BindCall(im_func, im_self, cb_data)
        else:
            handler = SimpleCall(callback, cb_data)
        tid = self.load_id
        self.task[tid] = (handler, ResLoader(mpath, self.load_complete, tid, res_type, sync_priority, merge_info, valid_checker))
        return self.load_id

    def cancel_task(self, tid):
        res_loader = self.task.get(tid, None)
        if res_loader and res_loader[1].is_loaded:
            res_loader[1].destroy()
            del self.task[tid]
        return

    def load_complete(self, model, task_id):
        cbinfo = self.task.get(task_id, None)
        if cbinfo is not None:
            cb, _ = cbinfo
            cb(model)
            del self.task[task_id]
        return

    def cancel_all(self):
        if self.task:
            for task_id, res_loader in six.iteritems(self.task):
                if res_loader[1].is_loaded:
                    res_loader[1].destroy()

            self.task = {}

    def destroy(self):
        self.cancel_all()