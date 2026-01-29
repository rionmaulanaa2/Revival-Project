# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/UIObjectBaseCreator.py
from __future__ import absolute_import
import six
from common.uisys.uisystem import UISystem

class UIObjectMeta(type):

    def __init__(cls, name, bases, dic):
        from common.uisys.UICreatorConfig import UICreatorConfig
        super(UIObjectMeta, cls).__init__(name, bases, dic)
        if name != 'UIObjectBaseCreator':
            uisys = UISystem()
            UICreatorConfig(cls, uisys)


class UIObjectBaseCreator(six.with_metaclass(UIObjectMeta, object)):
    COM_NAME = 'UIObjectBase'