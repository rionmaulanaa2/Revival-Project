# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/ComSystemMgr.py
from __future__ import absolute_import
import sys
g_com_sysmgr = None

class ComSystemMgr(object):

    def __new__(cls, *args, **kwargs):
        global g_com_sysmgr
        if g_com_sysmgr is None:
            g_com_sysmgr = object.__new__(cls, *args, **kwargs)
            g_com_sysmgr._do_init()
        return g_com_sysmgr

    def __init__(self):
        pass

    def _do_init(self):
        self._sys_map = {}
        self._handler_to_sys = {}
        self._element_set = set()
        self._mask_cache = {}
        self._sys_list = []
        global_data.g_com_sysmgr = g_com_sysmgr

    def get_mask(self, data_type):
        if data_type in self._mask_cache:
            return self._mask_cache[data_type]
        else:
            self._mask_cache[data_type] = 1 << len(self._mask_cache)
            return self._mask_cache[data_type]

    def add_system(self, system):
        system.on_add_sys()
        for interested_data_type in system.interested_type() + system.ignored_type():
            if interested_data_type not in self._sys_map:
                self._sys_map[interested_data_type] = []
            self._sys_map[interested_data_type].append(system)

        for handler_type in system.handler_types():
            if handler_type not in self._handler_to_sys:
                self._handler_to_sys[handler_type] = []
            self._handler_to_sys[handler_type].append(system)

        self._sys_list.append(system)

    def remove_system(self, system):
        system.on_remove_sys()
        for interested_data_type in system.interested_type() + system.ignored_type():
            if interested_data_type in self._sys_map:
                self._sys_map[interested_data_type].remove(system)

        for handler_type in system.handler_types():
            if handler_type in self._handler_to_sys:
                self._handler_to_sys[handler_type].remove(system)

        self._sys_list.remove(system)

    def add_data(self, data):
        type_of_data = type(data)
        data_mask = self.get_mask(type_of_data)
        unit_obj = data.unit_obj
        if unit_obj.sd.ecs_mask == 0:
            self._element_set.add(unit_obj)
        unit_obj.sd.ecs_mask |= data_mask
        for game_sys in self._sys_map.get(type_of_data, []):
            game_sys.mark_data_dirty()

    def remove_data(self, data):
        type_of_data = type(data)
        data_mask = self.get_mask(type_of_data)
        unit_obj = data.unit_obj
        unit_obj.sd.ecs_mask &= ~data_mask
        if unit_obj.sd.ecs_mask == 0:
            self._element_set.discard(unit_obj)
        for game_sys in self._sys_map.get(type_of_data, []):
            game_sys.mark_data_dirty()

    def get_elements(self, data_mask, ignored_mask):
        return [ unit_obj for unit_obj in self._element_set if unit_obj.sd.ecs_mask & data_mask == data_mask and not unit_obj.sd.ecs_mask & ignored_mask
               ]

    def tick(self, dt):
        for game_sys in self._sys_list:
            game_sys.tick_dt += dt
            if game_sys.tick_dt > game_sys.tick_step:
                game_sys.match_data_and_tick(game_sys.tick_dt)
                game_sys.tick_dt = 0

    def add_handler(self, handler):
        t = handler.HANDLER_TYPE
        handler_sys = self._handler_to_sys.get(t)
        if handler_sys:
            for game_sys in handler_sys:
                game_sys.add_handler(t, handler)

    def remove_handler(self, handler):
        t = handler.HANDLER_TYPE
        handler_sys = self._handler_to_sys.get(t)
        if handler_sys:
            for game_sys in handler_sys:
                game_sys.remove_handler(t, handler)

    def get_class(self, name):
        mpath = 'logic.gcommon.component.system.{}'.format(name).replace('FullFps', '')
        if '.' in name:
            name = name[name.rfind('.') + 1:]
        mod = sys.modules.get(mpath)
        if not mod:
            mod = __import__(mpath, globals(), locals(), [name])
        cls = getattr(mod, name, None)
        return cls

    def setup_all_system(self):
        sys_list = [
         'CommonMovementSystem',
         'CommonMovementSystemFullFps',
         'CommonMotorSystem',
         'CommonMotorSystemFullFps',
         'RotateSystem',
         'RotateSystemFullFps',
         'AnimatorSystem',
         'AnimatorSystemFullFps',
         'CameraRotateSystem',
         'CameraSystem',
         'AimIkSystem',
         'SenderSystem']
        for sys_name in sys_list:
            cls = self.get_class(sys_name)
            self.add_system(cls())


ComSystemMgr()