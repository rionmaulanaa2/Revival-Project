# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/UnitCom.py
from __future__ import absolute_import
from __future__ import print_function
import six
import cython
from logic.gcommon.utility import dummy_cb
import logic.gcommon.common_utils.bcast_utils as bcast
from .com_factory import UnitComMetaclass
from .IUnitCom import IUnitCom
from .UnitShareData import UnitShareData, DUMMY_SHARE_DATA
from logic.gcommon.component import SimpleEventManager
from logic.gcommon.component.SimpleEventManager import com_bind_event, com_unbind_event

def raise_exception(error):
    raise Exception(error)


class UnitCom(IUnitCom):
    BIND_EVENT = {}
    BIND_ATTR_CHANGE = {}
    SHARE_DATA_REF = {}
    ExtendFuncNames = []

    def __init__(self, need_update=False):
        self._is_valid = True
        self.__raw_need_update = need_update
        self._need_update = need_update
        self.is_active = False
        self.unit_obj = None
        self.battle = None
        self.use_idx = 0
        self.sd = UnitShareData()
        self._fast_acc_attrs = set()
        return

    def __getattr__(self, key):
        if key.startswith('ev_g_'):
            if self.unit_obj:
                rawkey = key[3:].upper()
                event_info = self.unit_obj._event_mgr._event_dict.get(rawkey, None)
                if event_info:
                    func = event_info[0][1]
                    self.__dict__[key] = func
                    self._fast_acc_attrs.add(key)
                    self.unit_obj.fast_acc_dict[key].add(self)
                else:
                    func = dummy_cb
            else:
                func = dummy_cb
            return func
        else:
            name = self.__class__.__name__
            raise AttributeError("'%s' object has no attribute '%s'" % (name, key))
            return

    def init_from_dict(self, unit_obj, bdict):
        self.unit_obj = unit_obj
        self.battle = unit_obj.get_battle()
        self._bind_event_interface()
        self.is_active = True
        if not unit_obj.is_cached:
            unit_obj.sd.merge(self.sd)
            self.sd = unit_obj.sd
            for attr, handler_name in six.iteritems(self.BIND_ATTR_CHANGE):
                self.BIND_EVENT['E_ADD_ATTR_CHANGED_%s' % attr] = handler_name

            self.init_event()
        self.need_update = self._need_update

    def destroy(self):
        if not self._is_valid:
            return
        else:
            self._is_valid = False
            self._unbind_event_interface()
            if self.unit_obj and self.unit_obj._is_valid:
                self.destroy_event()
                fast_acc_dict = self.unit_obj.fast_acc_dict
                for key in self._fast_acc_attrs:
                    if key in self.__dict__:
                        delattr(self, key)
                    if key in fast_acc_dict and self in fast_acc_dict[key]:
                        fast_acc_dict[key].remove(self)

                self._fast_acc_attrs.clear()
            self.is_active = False
            self.unit_obj = None
            self.battle = None
            self.sd = DUMMY_SHARE_DATA
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

    def get_client_dict(self):
        return {}

    def get_settle_dict(self):
        return {}

    def reset(self):
        pass

    @property
    def need_update(self):
        return self._need_update

    @property
    def logger(self):
        return self.unit_obj.get_owner().logger

    @property
    def scene(self):
        return global_data.game_mgr.scene

    @property
    def statistics(self):
        return self.battle.get_battle_statistics()

    @need_update.setter
    def need_update(self, val):
        self._need_update = val
        if self.unit_obj:
            if val:
                self.unit_obj.add_to_update_list(self)
            else:
                self.unit_obj.del_from_update_list(self)

    def is_unit_obj_type(self, type_name):
        if self.unit_obj and self.unit_obj.__class__.__name__ == type_name:
            return True
        return False

    def update_from_dict(self, unit_obj, bdict):
        pass

    def on_init_complete(self):
        pass

    def on_post_init_complete(self, bdict):
        pass

    def reuse(self, share_data):
        self.use_idx += 1
        self._need_update = self.__raw_need_update
        self.sd = share_data

    def cache(self):
        self.is_active = False
        self.battle = None
        self.need_update = False
        self.sd = DUMMY_SHARE_DATA
        return

    def _send_and_bcast_event(self, event_name, *args):
        self.send_event(bcast.idx_2_event_name(event_name), *args)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [event_name, args], True)

    def _bind_event_interface(self):
        self.send_event = self.unit_obj.send_event
        self.regist_event = self.unit_obj.regist_event
        self.unregist_event = self.unit_obj.unregist_event
        self.get_value = self.unit_obj.get_value
        self.send_and_bcast_event = self._send_and_bcast_event
        self.regist_pos_change = self.unit_obj.regist_pos_change
        self.unregist_pos_change = self.unit_obj.unregist_pos_change
        self.notify_pos_change = self.unit_obj.notify_pos_change

    def _unbind_event_interface(self):
        self.send_event = dummy_cb
        self.regist_event = dummy_cb
        self.unregist_event = dummy_cb
        self.get_value = dummy_cb
        self.send_and_bcast_event = dummy_cb
        self.regist_pos_change = dummy_cb
        self.unregist_pos_change = dummy_cb
        self.notify_pos_change = dummy_cb

    def _bind_event(self, einfo):
        com_bind_event(self, einfo)

    def _unbind_event(self, einfo):
        com_unbind_event(self, einfo)

    def _enable_bind_event(self, flag, elist=None):
        einfo = {}
        if elist is None:
            einfo = self.BIND_EVENT
        else:
            bind_events = self.BIND_EVENT
            for ename in elist:
                if ename in bind_events:
                    einfo[ename] = bind_events[ename]

        if flag:
            self._bind_event(einfo)
        else:
            self._unbind_event(einfo)
        return

    def init_event(self):
        self._bind_event(self.BIND_EVENT)

    def is_valid(self):
        return self._is_valid

    def is_enable(self, use_idx=None):
        if use_idx is None:
            return self._is_valid and self.is_active
        else:
            return self._is_valid and self.is_active and use_idx == self.use_idx
            return

    def tick(self, delta):
        pass

    def destroy_event(self):
        self._unbind_event(self.BIND_EVENT)

    def rebind_event--- This code section failed: ---

 386       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'False'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    38  'to 38'

 387      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'destroy_event'
          21  CALL_FUNCTION_0       0 
          24  POP_TOP          

 388      25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             3  'init_event'
          31  CALL_FUNCTION_0       0 
          34  POP_TOP          
          35  JUMP_FORWARD          0  'to 38'
        38_0  COME_FROM                '35'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def destroy_from_unit(self):
        if self.unit_obj is None:
            return
        else:
            self.unit_obj.del_com(self.__class__.__name__)
            return

    def on_destroy(self):
        raise Exception('PLEASE USE destroy() INSTEAD !!!!!!!!!!!!!!!!!!')