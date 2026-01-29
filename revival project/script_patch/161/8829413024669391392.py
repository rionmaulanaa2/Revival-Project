# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/ui_proxy.py
from __future__ import absolute_import
from __future__ import print_function
import six
from cocosui import cc
import weakref

def SetClassInstanceMethod(cls, name=None):

    def decorator(f):
        setattr(cls, name or f.__name__, f)

    return decorator


def SetClassClassMethod(cls, name=None):

    def decorator(f):
        setattr(cls, name or f.__name__, classmethod(f))

    return decorator


def SetClassStaticMethod(cls, name=None):

    def decorator(f):
        setattr(cls, name or f.__name__, staticmethod(f))

    return decorator


_rawClass2ProxyClass = {}
_rawClasses = set()
_create_raw_instances = weakref.WeakValueDictionary()
_static_method_type = type(cc.Node.create)
_instance_method_type = type(cc.Node.setPosition)
_attr_type = type(cc.Node.data)

def trans2ProxyObj(rawInstance):
    if rawInstance is None:
        return
    else:
        rawCls = rawInstance.__class__
        if rawCls not in _rawClasses:
            print('class not valid:', rawCls)
        ret = _create_raw_instances.get(id(rawInstance))
        if ret is None:
            return _rawClass2ProxyClass[rawCls](rawInstance)
        return ret or _rawClass2ProxyClass[rawCls](rawInstance)
        return


def getProxyObj(rawInstance):
    if rawInstance is None:
        return
    else:
        rawCls = rawInstance.__class__
        if rawCls not in _rawClasses:
            print('class not valid:', rawCls)
        ret = _create_raw_instances.get(id(rawInstance))
        return ret


def _setClassStaticMethod(cls, attr, f):

    @SetClassStaticMethod(cls, attr)
    def function(*arg, **argw):
        return f(*arg, **argw)


def _setClassInstanceMethod(cls, attr, f):

    @SetClassInstanceMethod(cls, attr)
    def function(self, *arg, **argw):
        return f(self._obj, *arg, **argw)


def ProxyClass(rawType=None):

    def decorator(cls):

        @SetClassClassMethod(cls)
        def getRawType(cls):
            return rawType or cls.__base__.getRawType()

        @SetClassInstanceMethod(cls)
        def __getattr__(self, name):
            if name in _get_set_attr:
                return getattr(self._obj, name)

        @SetClassInstanceMethod(cls)
        def __setattr__(self, name, value):
            if name in _get_set_attr:
                return setattr(self._obj, name, value)
            self.__dict__[name] = value

        @SetClassInstanceMethod(cls)
        def get(self):
            return self._obj

        @SetClassInstanceMethod(cls)
        def _on_create(self, rawObj):
            _create_raw_instances[id(rawObj)] = self
            self._obj = rawObj
            return self

        @SetClassInstanceMethod(cls)
        def _on_destroy(self):
            if id(self._obj) in _create_raw_instances:
                del _create_raw_instances[id(self._obj)]

        @SetClassInstanceMethod(cls)
        def _on_release(self):
            if id(self._obj) in _create_raw_instances:
                del _create_raw_instances[id(self._obj)]

        _get_set_attr = set()
        if rawType:
            for attr in dir(rawType):
                if attr.find('__') == 0:
                    continue
                var = getattr(rawType, attr)
                tvar = type(var)
                if tvar is _static_method_type:
                    _setClassStaticMethod(cls, attr, var)
                elif tvar is _instance_method_type:
                    _setClassInstanceMethod(cls, attr, var)
                elif tvar is _attr_type:
                    _get_set_attr.add(attr)

        clsBase = cls.__base__
        if clsBase is not object:
            for attr, var in six.iteritems(clsBase.__dict__):
                if attr not in cls.__dict__:
                    if callable(var):
                        setattr(cls, attr, var)

        if rawType and rawType not in _rawClass2ProxyClass:
            _rawClass2ProxyClass[rawType] = cls
            _rawClasses.add(rawType)
        return cls

    return decorator