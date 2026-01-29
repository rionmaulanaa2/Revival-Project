# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCHorzAsyncContainer.py
from __future__ import absolute_import
from common.uisys.ui_proxy import ProxyClass
from .CCAsyncContainer import CCAsyncContainer
from common.utils.cocos_utils import CCSizeZero, CCSize
from .CCNode import CCNode

@ProxyClass()
class CCHorzAsyncContainer(CCAsyncContainer):

    def _refreshItemPos(self):
        if len(self._child_item) == 0:
            return CCSizeZero
        else:
            ctrlW, ctrlH = self._ctrlSize.width, self._ctrlSize.height
            nHorzSpace = ctrlW + self._nHorzIndent
            nVertSpace = ctrlH + self._nVertIndent
            oX = self._nHorzBorder
            W = self._nUnit * (ctrlW + self._nHorzIndent) - self._nHorzIndent + 2 * self._nHorzBorder
            H = self._nNumPerUnit * (ctrlH + self._nVertIndent) - self._nVertIndent + 2 * self._nVertBorder
            size = CCSize(W, H)
            self.setContentSize(size)
            oY = -self._nVertBorder
            row, col, offY = (0, 0, 0)
            self._arrUpdatePos = []
            for v in self.GetAllItem():
                pos = [
                 oX + col, oY - offY]
                if isinstance(v, CCNode):
                    self._arrUpdatePos.append(None)
                    v.setPosition(*pos)
                else:
                    self._arrUpdatePos.append(pos)
                row += 1
                offY += nVertSpace
                if row == self._nNumPerUnit:
                    row = 0
                    offY = 0
                    col += nHorzSpace

            self._nodeContainer.SetPosition(0, H)
            return size