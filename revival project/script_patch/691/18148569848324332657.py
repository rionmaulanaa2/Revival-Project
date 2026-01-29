# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event_notifier.py
from __future__ import absolute_import
from __future__ import print_function
import cython
import weakref
from functools import partial
from copy import copy
from .framework import SingletonBase, Singleton
import six
REF_TYPE_NORMAL = cython.declare(cython.int, 1)
REF_TYPE_SINGLETON = cython.declare(cython.int, 2)
REF_TYPE_CC_NODE = cython.declare(cython.int, 3)

@cython.cclass
class WeakMethod2(object):
    method = cython.declare(object)
    instance = cython.declare(object)
    reference = cython.declare(object)
    deleted = cython.declare(cython.bint, visibility='public')
    ref_type = cython.declare(cython.int, visibility='public')

    @cython.locals(item=object, callback=object)
    def __init__(self, item, callback=None):
        self.method = None
        self.instance = None
        self.reference = None
        self.deleted = False
        self.hash_value = hash(item)
        im_func = getattr(item, six._meth_func, None)
        im_self = getattr(item, six._meth_self, None)
        if callback:
            release_callback = partial(callback, self)
        else:
            release_callback = None
        if im_func and im_self:
            from common.uisys.uielment.CCNode import CCNode
            import cc
            self.method = weakref.ref(im_func)
            self.instance = weakref.ref(im_self, release_callback)
            if isinstance(self.instance(), Singleton):
                self.ref_type = REF_TYPE_SINGLETON
            elif isinstance(self.instance(), (CCNode, cc.Node)):
                self.ref_type = REF_TYPE_CC_NODE
            else:
                self.ref_type = REF_TYPE_NORMAL
        else:
            self.reference = weakref.ref(item, release_callback)
        return

    @cython.ccall
    def release(self):
        self.deleted = True
        self.reference = None
        self.instance = None
        self.method = None
        return

    def __str__(self):
        if self.deleted:
            return 'deleted handler'
        else:
            if self.reference:
                return str(self.reference())
            return 'rinst:%s, func: %s' % (str(self.instance()), str(self.method()))

    @cython.cfunc
    def call(self, args, keywargs):
        if self.reference:
            func = self.reference()
            if not func:
                return None
            return func(*args, **keywargs)
        else:
            if not self.instance or not self.method:
                return None
            inst = self.instance()
            func = self.method()
            if not inst or not func:
                return None
            if self.ref_type == REF_TYPE_SINGLETON:
                robj = inst.get_instance()
                if robj is not inst:
                    return None
            elif self.ref_type == REF_TYPE_CC_NODE:
                if not inst.isValid():
                    return None
            return func(inst, *args, **keywargs)
            return None

    @cython.cfunc
    @cython.returns(cython.bint)
    def is_valid(self):
        if self.deleted:
            return False
        else:
            if self.reference:
                func = self.reference()
                if not func:
                    return False
                return True
            if not self.instance or not self.method:
                return False
            inst = self.instance()
            func = self.method()
            if not inst or not func:
                return False
            if self.ref_type == REF_TYPE_SINGLETON:
                robj = inst.get_instance()
                if robj is not inst:
                    return False
            elif self.ref_type == REF_TYPE_CC_NODE:
                if not inst.isValid():
                    return False
            return True

    @cython.ccall
    @cython.returns(cython.bint)
    @cython.locals(item=object)
    def equal(self, item):
        if item is None:
            return not self.is_valid()
        else:
            if self.reference:
                func = self.reference()
                if isinstance(item, WeakMethod2) and item.reference:
                    item_func = item.reference()
                    return item_func is func
                return func is item
            im_func = getattr(item, six._meth_func, None)
            im_self = getattr(item, six._meth_self, None)
            inst = self.instance()
            func = self.method()
            return im_func is func and inst is im_self
            return

    @cython.ccall
    @cython.returns(cython.bint)
    @cython.locals(item=object)
    def not_equal(self, item):
        return not self.equal(item)


WeakMethod2.__eq__ = WeakMethod2.equal
WeakMethod2.__ne__ = WeakMethod2.not_equal

@cython.cclass
class EventHook2(object):
    _list = cython.declare(list)
    _disable = cython.declare(cython.bint)
    _play_sound_enable = cython.declare(cython.bint)
    _node = cython.declare(object)
    _is_emitting = cython.declare(cython.bint)
    append = cython.declare(object, visibility='public')
    remove = cython.declare(object, visibility='public')
    index = cython.declare(object, visibility='public')

    @cython.locals(disable=cython.bint, play_sound_enable=cython.bint)
    def __init__(self, disable=False, play_sound_enable=False, node=None):
        super(EventHook2, self).__init__()
        self._list = []
        self._hash_list = []
        self._disable = disable
        self._play_sound_enable = play_sound_enable
        self._node = node
        self._is_emitting = False
        self.append = self._list.append
        self.remove = self._list.remove
        self.index = self._hash_list.index
        self.append_hash = self._hash_list.append

    @cython.locals(mobj=WeakMethod2)
    def __iadd__(self, handler_list):
        if not isinstance(handler_list, (list, tuple)):
            handler_list = [
             handler_list]
        for handler in handler_list:
            mobj = WeakMethod2(handler, self.remove_handler)
            if mobj.is_valid():
                h = hash(handler)
                if h not in self._hash_list:
                    self.append(mobj)
                    self.append_hash(h)

        return self

    def __isub__(self, handler_list):
        if handler_list is None:
            self.clear()
            return self
        else:
            if not isinstance(handler_list, (list, tuple)):
                handler_list = [
                 handler_list]
            for handler in handler_list:
                self.remove_handler(handler)

            return self

    @cython.locals(list_item=WeakMethod2)
    def remove_handler(self, handler, instance=None, force_remove=False):
        if instance and handler.deleted and not force_remove:
            return
        try:
            if instance:
                if self._is_emitting:
                    global_data.game_mgr.next_exec(self.remove_handler, handler, instance, True)
                else:
                    h = handler.hash_value
                    handler.release()
                    idx = self.index(h)
                    del self._list[idx]
                    del self._hash_list[idx]
                handler.deleted = True
            else:
                idx = -1
                idx = self.index(hash(handler))
                list_item = self._list[idx]
                list_item.deleted = True
                if self._is_emitting:
                    global_data.game_mgr.next_exec(self.remove_handler, handler, instance, True)
                else:
                    if isinstance(list_item, WeakMethod2):
                        list_item.release()
                    del self._list[idx]
                    del self._hash_list[idx]
        except ValueError:
            pass

    @cython.locals(handler=WeakMethod2)
    def flush_event_handler(self):
        valid_list = []
        valid_hash_list = []
        handler_list = self._list
        for i, handler in enumerate(handler_list):
            if handler.is_valid():
                valid_list.append(handler)
                valid_hash_list.append(self._hash_list[i])

        self._update_under_layer_list(valid_list, valid_hash_list)

    @cython.returns(list)
    @cython.locals(handler=WeakMethod2)
    def emit(self, *args, **keywargs):
        ret = []
        if not self._disable:
            self._is_emitting = True
            for handler in self._list:
                if handler.is_valid():
                    ret.append(handler.call(args, keywargs))

            self._is_emitting = False
        return ret

    @cython.locals(handler=WeakMethod2)
    def fire(self, *args, **keywargs):
        ret = []
        if not self._disable:
            handler_list = self._list
            for handler in handler_list:
                if handler.is_valid():
                    ret.append(handler.call(args, keywargs))

        self.clear()
        return ret

    def clear(self):
        self._update_under_layer_list([], [])

    def _update_under_layer_list(self, bind_list, bind_hash_list):
        self._list = bind_list
        self._hash_list = bind_hash_list
        self.append = self._list.append
        self.remove = self._list.remove
        self.index = self._hash_list.index
        self.append_hash = self._hash_list.append

    def disable(self, flag):
        self._disable = flag

    @cython.locals(h_ref=WeakMethod2)
    def _pop_handler(self, handler=None):
        if handler:
            for h_ref in self._list:
                if h_ref.equal(handler):
                    h_ref.deleted = True

        else:
            for h_ref in self._list:
                if not h_ref.is_valid():
                    h_ref.deleted = True if 1 else False

    @cython.locals(h_ref=WeakMethod2)
    def collect_handlers(self):
        valid_list = []
        valid_hash_list = []
        for i, h_ref in enumerate(self._list):
            if h_ref.deleted:
                continue
            if not h_ref.is_valid():
                log_error('find invalid handler', h_ref, h_ref.ref_type, 'consider leak posibility.')
                continue
            valid_list.append(h_ref)
            valid_hash_list.append(self._hash_list[i])

        self._update_under_layer_list(valid_list, valid_hash_list)

    def set_sound_enable(self, flag):
        self._play_sound_enable = flag


class EventNotifyer(SingletonBase):
    _KEEP_ALIVE_WHEN_RELOAD = 1
    ALIAS_NAME = 'emgr'
    ENABLE_OPTIMIZED_EVENT = True
    COLLECT_HANDLERS_INTERVAL = 2.0

    def init(self):
        self._event_map = {}
        self.hot_fix_mode = False
        self.time_collect_last = 0

    def on_finalize(self):
        self._event_map = {}
        self.hot_fix_mode = False
        self.time_collect_last = 0

    def create_event(self, event_list, flag=False):
        for ename in event_list:
            if ename not in self._event_map:
                self._event_map[ename] = EventHook2(flag)
            elif self.hot_fix_mode is False:
                raise Exception('event name dumplicate: %s' % ename)

    def flush_event_handler(self, name=None):
        if name is not None:
            evt = self._event_map.get(name, None)
            if evt:
                evt.flush_event_handler()
        else:
            for ename, evt in six.iteritems(self._event_map):
                if not hasattr(evt, 'flush_event_handler'):
                    print(evt)
                evt.flush_event_handler()

        return

    def collect_handlers(self):
        import time
        if time.time() - self.time_collect_last < self.COLLECT_HANDLERS_INTERVAL:
            return
        for evt in six.itervalues(self._event_map):
            evt.collect_handlers()

        self.time_collect_last = time.time()

    def add_event_notify(self, name, handler_list):
        if name not in self._event_map:
            self._event_map[name] = EventHook2()
        self._event_map[name] += handler_list

    def remove_event_notify(self, name, handler_list):
        if name is None:
            for val in six.itervalues(self._event_map):
                val -= handler_list

        else:
            val = self._event_map.get(name, None)
            if val:
                val -= handler_list
        return

    def clear(self, name):
        if name is None:
            for val in six.itervalues(self._event_map):
                val.clear()

        else:
            if not isinstance(name, (list, tuple)):
                name = [
                 name]
            for e in name:
                val = self._event_map.get(e, None)
                if val:
                    val.clear()

        return

    @cython.locals(val=EventHook2)
    def emit(self, name, *arg, **kwarg):
        if name is None:
            for val in six.itervalues(self._event_map):
                val.emit(*arg, **kwarg)

        else:
            val = self._event_map.get(name, None)
            if val:
                val.emit(*arg, **kwarg)
        return

    def bind_events(self, event_info):
        for ename, handlers in six.iteritems(event_info):
            evt = getattr(self, ename)
            if isinstance(handlers, (list, tuple)):
                for handler in handlers:
                    evt += handler

            else:
                evt += handlers

    def unbind_events(self, event_info):
        for ename, handlers in six.iteritems(event_info):
            evt = getattr(self, ename)
            if isinstance(handlers, (list, tuple)):
                for handler in handlers:
                    evt -= handler

            else:
                evt -= handlers

    fireEvent = emit

    def disable(self, name, flag):
        if name is None:
            for val in six.itervalues(self._event_map):
                val.disable(flag)

        else:
            val = self._event_map.get(name, None)
            if val:
                val.disable(flag)
        return

    def __iadd__(self, handler_info):
        event_name, handlers = handler_info
        self.add_event_notify(event_name, handlers)

    def __isub__(self, handler_info):
        event_name, handlers = handler_info
        self.remove_event_notify(event_name, handlers)

    def __getattr__(self, key):
        if key not in self._event_map:
            raise Exception('no event hook name %s' % key)
        return self._event_map.get(key, None)

    def __getitem__(self, key):
        if key not in self._event_map:
            raise Exception('no event hook name %s' % key)
        return self._event_map.get(key, None)