# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCUIWidget.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCLayer import CCLayer

@ProxyClass(ccui.Widget)
class CCUIWidget(CCLayer):

    def __init__(self, node):
        super(CCUIWidget, self).__init__(node)

    def csb_init(self):
        super(CCUIWidget, self).csb_init()
        if self.isTouchEnabled():
            self.SetEnableTouchWithoutCheck(True)
            if self.IsSupportTouch():
                self.SetNoEventAfterMove(self.getNoEnventAfterMove(), self.getMoveCancelDist())
        self._propagateTouchEvents = True