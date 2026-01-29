# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontPath/Manager/ModelProxy.py
from __future__ import absolute_import
import world

class Wrapper(object):

    def __init__(self, item):
        self.item = item
        self.type = 0

    def __set__(self, instance, value):
        self.type = 2
        self.value = value

    def __call__(self, *args, **kwargs):
        self.type = 1
        self.args = args
        self.kwargs = kwargs

    def handle(self, model):
        if self.type == 1:
            getattr(model, self.item)(*self.args, **self.kwargs)
        elif self.type == 2:
            setattr(model, self.item, self.value)


class ModelProxy(object):

    def __init__(self, model, callback=None):
        self.callback = callback
        self.model = None
        self.todoList = []
        world.create_model_async(model, self._load_model_callback)
        return

    def loaded(self):
        return self.model is not None

    def _load_model_callback(self, obj, *args):
        if self.callback:
            self.callback(obj, *args)
        self.model = obj
        for proxy in self.todoList:
            proxy.handle(self.model)

        self.todoList = []

    def __getattr__(self, item):
        if self.model:
            return getattr(self.model, item)
        else:
            wrapper = Wrapper(item)
            self.todoList.append(wrapper)
            return wrapper

    def __setattr__(self, key, value):
        if key in ('callback', 'model', 'todoList'):
            self.__dict__[key] = value
        elif self.model:
            setattr(self.model, key, value)
        else:
            wrapper = Wrapper(key)
            wrapper.__set__(self, value)
            self.todoList.append(wrapper)