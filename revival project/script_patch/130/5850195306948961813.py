# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareTemplateFactory.py
from __future__ import absolute_import
from common.framework import Singleton

class ShareCreatorFactory(Singleton):

    def init(self):
        self.creator_dict = {}

    def regist_creator(self, cls):
        if cls.__name__ == 'ShareTemplateBase':
            return
        if hasattr(cls, 'KIND') and cls.KIND:
            self.creator_dict[cls.KIND] = cls
        else:
            log_error('Error, share creator should have KIND Attribute')

    def get_creator(self, KIND):
        return self.creator_dict.get(KIND, None)


class RegisterCreatorMeta(type):

    def __init__(cls, name, bases, dic):
        super(RegisterCreatorMeta, cls).__init__(name, bases, dic)
        ShareCreatorFactory().regist_creator(cls)