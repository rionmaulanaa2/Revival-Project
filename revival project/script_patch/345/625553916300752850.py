# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/Unit.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
import cython
from collections import defaultdict
from logic.gcommon.utility import dummy_cb
from logic.gcommon.component.SimpleEventManager import SimpleEventManager
from . import com_factory
from .IUnit import IUnit
from .UnitShareData import UnitShareData, DUMMY_SHARE_DATA
from logic.gcommon.common_utils import pos_change_mgr

class Unit(IUnit):

    def __init__(self, entity, battle, is_cacheable=False):
        super(Unit, self).__init__()
        self.id = entity.id
        self._is_valid = True
        self._is_player = False
        self._has_dynamic_com = False
        self._owner = entity
        self._battle = battle
        self._pos_change_mgr = pos_change_mgr.PosChangeMgr()
        self._event_mgr = SimpleEventManager()
        self._event_mgr.unit_obj = self
        self._bind_event_interface()
        self._is_ticking = False
        self._update_coms = set()
        self._stop_update_coms = set()
        self._start_update_coms = set()
        self._com_extend_func_names = defaultdict(set)
        self.fast_acc_dict = defaultdict(set)
        self._coms = {}
        self._add_com_order = []
        self._add_com_order_origin = []
        self.lg_mask = 0
        self._is_cacheable = is_cacheable
        self.is_cached = False
        self._lock_com = False
        self.__bind_share_data()

    def __getattr__(self, key):
        if key.startswith('ev_g_'):
            if not self._event_mgr:
                return dummy_cb
            rawkey = key[3:].upper()
            event_info = self._event_mgr._event_dict.get(rawkey, None)
            if event_info:
                func = event_info[0][1]
                self.__dict__[key] = func
                self.fast_acc_dict[key].add(self)
            else:
                func = dummy_cb
            return func
        else:
            name = self.__class__.__name__
            raise AttributeError("'%s' object has no attribute '%s'" % (name, key))
            return

    def update_from_dict(self, bdict):
        for com in six_ex.values(self._coms):
            com.update_from_dict(self, bdict)

    def on_init_complete(self):
        for com in six_ex.values(self._coms):
            if com.is_valid():
                com.on_init_complete()

    def on_post_init_complete(self, bdict):
        for com in six.itervalues(self._coms):
            if com.is_valid():
                com.on_post_init_complete(bdict)

    def reset(self):
        for com in six_ex.values(self._coms):
            com.reset()

    def get_client_dict(self):
        cdict = {}
        for com in six.itervalues(self._coms):
            d = com.get_client_dict()
            if d:
                cdict.update(d)

        return cdict

    def get_settle_dict(self):
        cdict = {}
        for com in six.itervalues(self._coms):
            d = com.get_settle_dict()
            if d:
                cdict.update(d)

        return cdict

    def reuse(self, entity, battle):
        self.id = entity.id
        self._owner = entity
        self._battle = battle
        self._add_com_order = self._add_com_order_origin
        self.__bind_share_data()
        for com in six.itervalues(self._coms):
            com.reuse(self.sd)

    def cache(self):
        for com in six.itervalues(self._coms):
            com.cache()

        self.__unbind_share_data()
        self.id = None
        self._owner = None
        self._battle = None
        self.is_cached = True
        self._scene_cache = None
        return

    def get_owner(self):
        return self._owner

    def get_battle(self):
        return self._battle

    def get_scene(self):
        if self._scene_cache and self._scene_cache.valid:
            return self._scene_cache
        if self._battle:
            self._scene_cache = self._battle.get_scene()
            return self._scene_cache

    def is_valid(self):
        return self._is_valid

    def is_enable(self):
        return self._is_valid and self.id is not None

    def is_dead(self):
        return False

    def is_defeated(self):
        return False

    def is_player(self):
        return self._is_player

    def set_player(self):
        self._is_player = True

    def get_logic_mask(self):
        return self.lg_mask

    def is_robot(self):
        return False

    def is_monster(self):
        return False

    def is_mecha(self):
        return False

    def is_pet(self):
        return False

    def _bind_event_interface(self):
        self.send_event = self._event_mgr.emit
        self.regist_event = self._event_mgr.regist_event
        self.unregist_event = self._event_mgr.unregist_event
        self.get_value = self._event_mgr.value
        self.regist_pos_change = self._pos_change_mgr.add_pos_listener
        self.unregist_pos_change = self._pos_change_mgr.del_pos_listener
        self.notify_pos_change = self._pos_change_mgr.notify_pos_change

    def _unbind_event_interface(self):
        self.send_event = dummy_cb
        self.regist_event = dummy_cb
        self.unregist_event = dummy_cb
        self.get_value = dummy_cb
        self.regist_pos_change = dummy_cb
        self.unregist_pos_change = dummy_cb
        self.notify_pos_change = dummy_cb

    def _init_coms(self, bdict):
        pass

    def _post_init_coms(self, bdict):
        pass

    def del_from_update_list(self, com):
        if self._is_ticking:
            self._stop_update_coms.add(com)
            if com in self._start_update_coms:
                self._start_update_coms.remove(com)
        elif com in self._update_coms:
            self._update_coms.remove(com)

    def add_to_update_list(self, com):
        if com.__class__.__name__ not in self._coms:
            return
        if self._is_ticking:
            self._start_update_coms.add(com)
            if com in self._stop_update_coms:
                self._stop_update_coms.remove(com)
        else:
            self._update_coms.add(com)
        self._has_dynamic_com = True

    def add_com(self, com_name, com_type):
        if com_name in self._coms:
            log_error('Com %s already exist!' % com_name)
            return None
        else:
            c = com_factory.load_com(com_name, com_type)
            if not c:
                return None
            self._coms[com_name] = c

            def _set_method(c, name):
                method = getattr(c, name)
                setattr(self, name, method)

            for name in c.ExtendFuncNames:
                if not hasattr(self, name):
                    _set_method(c, name)
                    self._com_extend_func_names[com_name].add(name)

            if c.need_update:
                self.add_to_update_list(c)
            self._add_com_order.append(com_name)
            return c

    def del_com(self, com_name):
        if not self._coms:
            return
        else:
            com = self._coms.pop(com_name, None)
            if not com:
                return
            if com_name in self._com_extend_func_names:
                for name in self._com_extend_func_names[com_name]:
                    del self.__dict__[name]

                del self._com_extend_func_names[com_name]
            self.del_from_update_list(com)
            com.destroy()
            return

    def get_com(self, com_name):
        if not self._coms:
            return None
        else:
            return self._coms.get(com_name, None)

    def reload_com(self):
        for com in six_ex.values(self._coms):
            com.rebind_event()

    def remove_coms_event_func(self, key):
        raise Exception('Obsolete Interface')

    def test_coms(self):
        for com in six.itervalues(self._coms):
            for k, v in six.iteritems(com.BIND_EVENT):
                v1 = self._event_mgr.get_event_func(k)
                kk = 'ev_' + k.lower()
                v2 = com.__dict__.get(kk)
                if v2 is not None and v1 != v2:
                    print('[ERROR] ev_func error:', k, com.__class__.__name__, v2)
                v3 = self.__dict__.get(kk)
                if v3 is not None and v1 != v3:
                    print('[ERROR] ev_func error:', k, com.__class__.__name__, v3)

        return

    def tick(self, dt):
        self._is_ticking = True
        for com in self._update_coms:
            if com.is_active:
                com.tick(dt)

        self._is_ticking = False
        if self._start_update_coms:
            for com in self._start_update_coms:
                self.add_to_update_list(com)

            self._start_update_coms = set()
        if self._stop_update_coms:
            for com in self._stop_update_coms:
                self.del_from_update_list(com)

            self._stop_update_coms = set()

    def init_from_dict(self, bdict):
        if not self.is_cached:
            self._init_coms(bdict)
        ordered_com_name = self._add_com_order
        self._add_com_order_origin = ordered_com_name
        self._add_com_order = []
        for com_name in ordered_com_name:
            com = self._coms.get(com_name)
            if com:
                com.init_from_dict(self, bdict)

        self.on_init_complete()
        self.on_post_init_complete(bdict)

    def destroy(self):
        if not self._is_valid:
            return
        else:
            self._is_valid = False
            for com in six.itervalues(self._coms):
                com._unbind_event_interface()

            for com in six_ex.values(self._coms):
                com.destroy()

            self._unbind_event_interface()
            self._event_mgr.destroy()
            self._event_mgr = None
            self._coms = None
            self._update_coms = None
            self._stop_update_coms = None
            self._start_update_coms = None
            self.__unbind_share_data()
            self.fast_acc_dict.clear()
            self._owner = None
            self._battle = None
            self._scene_cache = None
            self._pos_change_mgr.destroy()
            self._pos_change_mgr = None
            return

    def _report_warning(self):
        import game3d
        self.__life_end = global_data.game_time
        life_time = self.__life_end - self.__life_begin + 0.001
        life_circle = life_time * game3d.get_frame_rate()
        thread_hold = 0.5
        for key, hit_times in six.iteritems(self.__hit_attrs):
            if hit_times / life_circle >= thread_hold:
                pass
            self.__dict__.pop(key, None)

        for key, miss_times in six.iteritems(self.__miss_attrs):
            if miss_times > 2:
                continue

        self.__miss_attrs = {}
        self.__hit_attrs = {}
        self.__life_begin = global_data.game_time
        return

    def lock_event(self, value):
        self._event_mgr.lock(value)

    def __bind_share_data(self):
        self.sd = self.share_data = UnitShareData()
        self.sd.ref_is_mecha = False
        self._owner.sd = self._owner.share_data = self.sd

    def __unbind_share_data(self):
        self.sd = self.share_data = DUMMY_SHARE_DATA
        if self._owner:
            self._owner.sd = self._owner.share_data = DUMMY_SHARE_DATA

    def has_dynamic_com(self):
        return self._has_dynamic_com