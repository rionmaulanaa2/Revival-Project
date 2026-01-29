# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/wanfa/WanfaManager.py
from __future__ import absolute_import
import six_ex
from common.framework import Singleton

def init_wanfa(wanfa_name):
    wanfa_dict = {'ControlBattle': WanfaControlBattle
       }
    wanfa_cls = wanfa_dict.get(wanfa_name, WanfaDefaultBattle)
    return wanfa_cls(wanfa_name)


class WanfaManagerBase(Singleton):

    def init(self, name):
        super(WanfaManagerBase, self).init()
        self.name = name
        self.wanfa_dict = {}
        self.on_init_mgr()

    def on_init_mgr(self):
        raise NotImplementedError

    def destroy(self):
        self.clear_wanfa()
        self.__class__.finalize()

    def add_sub_wanfa(self, wanfa_name, module_path='logic.wanfa.sub_wanfa'):
        if wanfa_name in self.wanfa_dict:
            log_error('wanfa %s has been added before' % wanfa_name)
            return
        else:
            mconf = __import__(module_path, globals(), locals(), [wanfa_name], -1)
            if not mconf:
                log_error('no wanfa class %s in %s' % (wanfa_name, module_path))
                return
            module = getattr(mconf, wanfa_name, None)
            wanfa_cls = getattr(module, wanfa_name, None)
            if not wanfa_cls:
                log_error('wanfa name dont match dialog class name %s' % wanfa_name)
                return
            self.wanfa_dict[wanfa_name] = wanfa_cls()
            return

    def clear_wanfa(self):
        keys = six_ex.keys(self.wanfa_dict)
        for key in keys:
            self.del_sub_wanfa(key)

    def del_sub_wanfa(self, wanfa_name):
        if wanfa_name in self.wanfa_dict:
            self.wanfa_dict[wanfa_name].destroy()
            del self.wanfa_dict[wanfa_name]


class WanfaControlBattle(WanfaManagerBase):

    def on_init_mgr(self):
        pass


class WanfaDefaultBattle(WanfaManagerBase):

    def on_init_mgr(self):
        pass