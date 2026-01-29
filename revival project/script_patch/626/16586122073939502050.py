# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Singleton.py


def with_metaclass(meta, *bases):

    class metaclass(type):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

        @classmethod
        def __prepare__(cls, name, this_bases):
            return meta.__prepare__(name, bases)

    return type.__new__(metaclass, 'temporary_class', (), {})


class MetaSingleton(type):

    def __call__(cls, *args, **kwargs):
        if not cls.__dict__.get('_instance'):
            cls._instance = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Singleton(with_metaclass(MetaSingleton)):

    @classmethod
    def instance(cls):
        return cls()