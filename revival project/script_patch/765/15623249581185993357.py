# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/Event.py
import sys
import weakref
import inspect
import collections
try:
    from weakref import WeakMethod
except ImportError:

    class WeakMethod(weakref.ref):
        __slots__ = ('_func_ref', '_meth_type', '_alive', '__weakref__')

        def __new__(cls, meth, callback=None):
            try:
                obj = meth.__self__
                func = meth.__func__
            except AttributeError:
                raise TypeError('argument should be a bound method, not {0}'.format(type(meth)))

            def _cb(arg):
                self = self_wr()
                if self._alive:
                    self._alive = False
                    if callback is not None:
                        callback(self)
                return

            self = weakref.ref.__new__(cls, obj, _cb)
            self._func_ref = weakref.ref(func, _cb)
            self._meth_type = type(meth)
            self._alive = True
            self_wr = weakref.ref(self)
            return self

        def __call__(self):
            obj = super(WeakMethod, self).__call__()
            func = self._func_ref()
            if obj is None or func is None:
                return
            else:
                return self._meth_type(func, obj)

        def __eq__(self, other):
            if isinstance(other, WeakMethod):
                if not self._alive or not other._alive:
                    return self is other
                return weakref.ref.__eq__(self, other) and self._func_ref == other._func_ref
            return False

        def __ne__(self, other):
            return not self.__eq__(other)

        __hash__ = weakref.ref.__hash__


CALL_EVENTS_EXCEPTION_THRESHOLD = 3
__call_events__ = collections.Counter()

class Event(object):

    def __init__(self):
        self._registerFuncs = {}

    @property
    def registerFuncs(self):
        return list(self._registerFuncs.keys())

    def _onFuncDie(self, wr):
        self._registerFuncs.pop(wr, None)
        return

    def _createWeakRef(self, func, listen=False):
        if inspect.ismethod(func):
            if listen:
                return WeakMethod(func, self._onFuncDie)
            return WeakMethod(func)
        return func

    def RegisterFunc(self, func, *args, **kwargs):
        ref = self._createWeakRef(func, True)
        if ref in self._registerFuncs:
            sys.stderr.write('[WARNING]Event handler %s is registered twice!' % func)
            return
        self._registerFuncs[ref] = (args, kwargs)

    def UnregisterFunc(self, func):
        ref = self._createWeakRef(func)
        self._registerFuncs.pop(ref, None)
        return

    def isRegistered(self, func):
        ref = self._createWeakRef(func)
        return ref in self._registerFuncs

    def Destroy(self):
        self._registerFuncs = {}

    def Activate(self, *args, **kwargs):
        if len(self._registerFuncs) == 0:
            return
        else:
            if __call_events__[self] + 1 >= CALL_EVENTS_EXCEPTION_THRESHOLD:
                print __call_events__
                raise Exception('The stack of event call has a ring! Depth: %d' % CALL_EVENTS_EXCEPTION_THRESHOLD)
            __call_events__[self] += 1
            ret = None
            for f, (_args, _kwargs) in list(self._registerFuncs.items()):
                try:
                    if isinstance(f, weakref.ref):
                        ret = f()(*(_args + args), **dict(_kwargs, **kwargs))
                    else:
                        ret = f(*(_args + args), **dict(_kwargs, **kwargs))
                except:
                    import traceback
                    traceback.print_exc()

            __call_events__[self] -= 1
            if __call_events__[self] == 0:
                __call_events__.__delitem__(self)
            return ret

    def __iadd__(self, func):
        self.RegisterFunc(func)
        return self

    def __isub__(self, func):
        self.UnregisterFunc(func)
        return self

    def __call__(self, *args, **kwargs):
        return self.Activate(*args, **kwargs)