# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/algorithm/resloader.py
from __future__ import absolute_import
from __future__ import print_function
import six
import render
import world
import game3d
import threading
import os.path
from common.cfg import confmgr
__mutex = threading.RLock()

class ResCache(object):

    def __init__(self, max_size):
        super(ResCache, self).__init__()
        self.max_size = max_size
        self._cache = {}

    def clear(self):
        self._cache = {}

    def __getitem__(self, key):
        return self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def __delitem__(self, key):
        del self._cache[key]

    def __contains__(self, key):
        return key in self._cache

    def __iter__(self):
        return six.iterkeys(self._cache)

    def __len__(self):
        return len(self._cache)

    def __repr__(self):
        return str(self._cache)


class LruResCache(ResCache):

    def __init__(self, max_size):
        super(LruResCache, self).__init__(max_size)
        import common.algorithm.lrucache
        self._cache = common.algorithm.lrucache.LRUCache(max_size)

    def clear(self):
        keys = []
        if len(self._cache) > 0:
            for k in self._cache:
                keys.append(k)

            for k in keys:
                del self._cache[k]


__res_loading_cache = {}
__pre_load_list = [[], []]
__pre_load_list_fixed = confmgr.get('preload_list', 'permanent')
__pre_load_list_fixed = set(__pre_load_list_fixed) if __pre_load_list_fixed else set()
if game3d.get_platform() == game3d.PLATFORM_ANDROID:
    CACHE_MAX_SIZE = confmgr.get('setting', 'cache_size_android', default=50)
else:
    CACHE_MAX_SIZE = confmgr.get('setting', 'cache_size_ios', default=15)
CACHE_LRU = confmgr.get('setting', 'cache_lru', default=True)
cls = ResCache
if CACHE_LRU or game3d.get_platform() == game3d.PLATFORM_IOS:
    cls = LruResCache
__res_cache = cls(CACHE_MAX_SIZE)
__res_cache_fixed = {}
ASYNC_TEXURE = 1
ASYNC_RES = 2
TEX_EXT = set(('.png', '.bmp', '.tga', '.jpg', '.dds', '.ktx', '.pvr', '.spr'))

def reset_res_data_cache():
    global __res_cache
    retain_res_map = {}
    for path in __pre_load_list_fixed:
        if path in __res_cache:
            retain_res_map[path] = __res_cache[path]

    __res_cache.clear()
    for path, res in six.iteritems(retain_res_map):
        __res_cache[path] = res


def stop_async_res():
    __res_loading_cache.clear()


def sync_load_res_by_path(path, async_type=ASYNC_RES):
    path = path.replace('\\', '/')
    if path in __res_cache:
        return __res_cache[path]
    else:
        if path in __res_cache_fixed:
            return __res_cache_fixed[path]
        if async_type == ASYNC_RES:
            res_obj = world.create_res_object(path, world.RES_TYPE_UNKNOWN, game3d.ASYNC_NONE)
        elif async_type == ASYNC_TEXURE:
            res_obj = render.texture(path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
        else:
            print('[ERROR] sync_load_res_by_path failed. path:{0} type:{1}'.format(path, async_type))
            return None
        if path in __pre_load_list_fixed:
            __res_cache_fixed[path] = res_obj
        else:
            __res_cache[path] = res_obj
        return res_obj


def __load_res_by_path_finished(path, res):
    __mutex.acquire()
    if path in __pre_load_list_fixed:
        __res_cache_fixed[path] = res
    else:
        __res_cache[path] = res
    if path not in __res_loading_cache:
        return
    for callback_info in __res_loading_cache[path]:
        if callback_info[0]:
            callback_info[0](res, callback_info[1])

    if path in __res_loading_cache:
        del __res_loading_cache[path]
    __mutex.release()


def async_load_res_by_path(path, async_type=ASYNC_RES, async_callback=None, async_data=None, async_priority=None, async_create_obj=False):
    path = path.replace('\\', '/')
    if path in __res_cache_fixed:
        if async_callback:
            async_callback(__res_cache_fixed[path], async_data)
        return
    else:
        if path in __res_cache:
            if async_callback:
                async_callback(__res_cache[path], async_data)
            return
        if path in __res_loading_cache:
            __res_loading_cache[path].append((async_callback, async_data))
            return
        __res_loading_cache[path] = [
         (
          async_callback, async_data)]

        def load_callback(res, *args, **kargs):
            __load_res_by_path_finished(path, res)

        fn, fe = os.path.splitext(path)
        if fe in TEX_EXT:
            async_type = ASYNC_TEXURE
        if async_priority is None:
            priority = game3d.ASYNC_HIGH if async_type == ASYNC_RES else game3d.ASYNC_LOW
        else:
            priority = async_priority
        if async_type == ASYNC_RES:
            world.create_res_object(path, world.RES_TYPE_UNKNOWN, priority, load_callback)
        elif async_type == ASYNC_TEXURE:
            render.texture(path, False, False, render.TEXTURE_TYPE_UNKNOWN, priority, load_callback)
        else:
            print('[ERROR] async_load_res_by_path failed. path:{0} type:{1}'.format(path, async_type))
            return
        return


def async_load_res_list_by_path(pathlist, callback=None, priority=None):
    if not pathlist:
        if callback:
            callback()
        return
    count = [len(pathlist)]

    def async_callback(obj, data):
        count[0] -= 1
        if count[0] == 0 and callback:
            callback()

    for path in pathlist:
        async_load_res_by_path(path, async_callback=async_callback, async_priority=priority)


def load_sfx_by_path--- This code section failed: ---

 245       0  LOAD_GLOBAL           0  'sync_load_res_by_path'
           3  LOAD_GLOBAL           1  'ASYNC_RES'
           6  LOAD_GLOBAL           1  'ASYNC_RES'
           9  CALL_FUNCTION_257   257 
          12  STORE_FAST            3  'res'

 246      15  LOAD_GLOBAL           2  'world'
          18  LOAD_ATTR             3  'sfx'
          21  LOAD_FAST             3  'res'
          24  LOAD_FAST             1  'args'
          27  LOAD_FAST             2  'kargs'
          30  CALL_FUNCTION_VAR_KW_1     1 
          33  STORE_FAST            4  'sfx'

 247      36  LOAD_FAST             4  'sfx'
          39  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 9


def __async_load_sfx_by_path_callback(sfx, user_data, current_task):
    path, callback = user_data
    if sfx is None:
        sfx = world.sfx('fx/empty.sfx')
    __load_res_by_path_finished(path, sfx.get_res_object())
    callback(sfx)
    return


def async_load_sfx_by_path(path, callback):
    world.create_sfx_async(path, __async_load_sfx_by_path_callback, (
     path, callback))


def load_model_by_path--- This code section failed: ---

 267       0  LOAD_GLOBAL           0  'sync_load_res_by_path'
           3  LOAD_GLOBAL           1  'ASYNC_RES'
           6  LOAD_GLOBAL           1  'ASYNC_RES'
           9  CALL_FUNCTION_257   257 
          12  STORE_FAST            3  'res'

 268      15  LOAD_GLOBAL           2  'world'
          18  LOAD_ATTR             3  'model'
          21  LOAD_FAST             3  'res'
          24  LOAD_FAST             1  'args'
          27  LOAD_FAST             2  'kargs'
          30  CALL_FUNCTION_VAR_KW_1     1 
          33  STORE_FAST            4  'model'

 269      36  LOAD_FAST             4  'model'
          39  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 9


def load_texture_by_path--- This code section failed: ---

 273       0  LOAD_GLOBAL           0  'sync_load_res_by_path'
           3  LOAD_GLOBAL           1  'ASYNC_TEXURE'
           6  LOAD_GLOBAL           1  'ASYNC_TEXURE'
           9  CALL_FUNCTION_257   257 
          12  STORE_FAST            1  'res'

 274      15  LOAD_FAST             1  'res'
          18  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 9


def load_reslist(paths, callback, priority=None):
    if not paths:
        callback()
        return
    else:
        counter = [
         0]

        def load_cb(*args):
            counter[0] += 1
            if counter[0] >= len(paths):
                callback()

        for path in paths:
            async_load_res_by_path(path, async_type=ASYNC_RES, async_callback=load_cb, async_priority=priority, async_data=None)

        return


def get_modelpaths_by_name(name, model_confs=None):
    if model_confs is None:
        model_confs = confmgr.get('model').get_conf()
    model_conf = model_confs[name]
    modelpaths = []
    modelpaths.append(model_conf['model'])
    submodels = model_conf.get('submodels')
    if submodels:
        for submodel in submodels:
            subname = submodel['model']
            subpaths = get_modelpaths_by_name(subname, model_confs)
            modelpaths.extend(subpaths)

    return modelpaths


def get_modelpaths_by_type(conf_type, level):
    file_name = 'war_ship_data/' + conf_type
    check_level = level
    war_ship_data = confmgr.get(file_name, str(check_level), default=None)
    while not war_ship_data:
        check_level -= 1
        if check_level < 0:
            return
        war_ship_data = confmgr.get(file_name, str(check_level), default=None)

    model_name = confmgr.get('ship_model', str(war_ship_data['iType']))['cModel']
    return get_modelpaths_by_name(model_name, confmgr.get('model').get_conf())


def is_in_cache(path):
    path = path.replace('\\', '/')
    return path in __res_cache


def is_in_loading(path):
    path = path.replace('\\', '/')
    return path in __res_loading_cache


def clear_cache():
    reset_res_data_cache()


def add_preload_gim(path):
    if path not in __pre_load_list[0]:
        __pre_load_list[0].append(path)


def add_preload_sfx(path):
    if path not in __pre_load_list[1]:
        __pre_load_list[1].append(path)


def get_preload_gims():
    l = []
    l.extend(__pre_load_list[0])
    for gim in __pre_load_list_fixed:
        if gim.endswith('.gim'):
            l.append(gim)

    return l


def get_preload_sfxs():
    l = []
    l.extend(__pre_load_list[1])
    for gim in __pre_load_list_fixed:
        if gim.endswith('.sfx'):
            l.append(gim)

    return l


def clear_preload_list():
    __pre_load_list[0] = []
    __pre_load_list[1] = []


def preload_reslist(callback):
    res = []
    res.extend(__pre_load_list[0])
    res.extend(__pre_load_list[1])
    res.extend(__pre_load_list_fixed)
    async_load_res_list_by_path(res, callback)
    clear_preload_list()


def del_res_attr(obj, attr_name, task_only=False):
    task_name = '%s_task' % attr_name
    cnt_attr = getattr(obj, attr_name, None)
    cnt_attr_task = getattr(obj, task_name, None)
    if cnt_attr and not task_only:
        cnt_attr.destroy()
        setattr(obj, attr_name, None)
    if cnt_attr_task:
        cnt_attr_task.cancel()
        setattr(obj, task_name, None)
    return


def load_res_attr(obj, attr_name, res_path, callback, usr_data, res_type='MODEL', priority=game3d.ASYNC_MID):
    import world
    task_name = '%s_task' % attr_name
    cnt_attr = getattr(obj, attr_name, None)
    if cnt_attr:
        return
    else:
        cnt_attr_task = getattr(obj, task_name, None)
        if cnt_attr_task:
            return

        def res_callback(model, data, *args):
            if getattr(obj, task_name) != args[0]:
                model.destroy()
                return
            else:
                if not getattr(obj, task_name, None):
                    return
                setattr(obj, attr_name, model)
                callback(model, data, *args)
                setattr(obj, task_name, None)
                return

        res_task = None
        if res_type == 'MODEL':
            res_task = world.create_model_async(res_path, res_callback, usr_data, priority)
        else:
            res_task = world.create_sfx_async(res_path, res_callback, usr_data, priority)
        setattr(obj, task_name, res_task)
        return