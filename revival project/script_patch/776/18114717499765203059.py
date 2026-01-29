# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCVerAsyncContainer.py
from __future__ import absolute_import
from common.uisys.ui_proxy import ProxyClass
from .CCAsyncContainer import CCAsyncContainer
from .CCNode import CCNode
from common.utils.cocos_utils import CCSize, CCSizeZero

@ProxyClass()
class CCVerAsyncContainer(CCAsyncContainer):

    def _refreshItemPos(self):
        if len(self._child_item) == 0:
            return CCSizeZero
        else:
            ctrlW, ctrlH = self._ctrlSize.width, self._ctrlSize.height
            nHorzSpace = ctrlW + self._nHorzIndent
            nVertSpace = ctrlH + self._nVertIndent
            oX = self._nHorzBorder
            W = self._nNumPerUnit * (ctrlW + self._nHorzIndent) - self._nHorzIndent + 2 * self._nHorzBorder
            H = self._nUnit * (ctrlH + self._nVertIndent) - self._nVertIndent + 2 * self._nVertBorder
            size = CCSize(W, H)
            self.setContentSize(size)
            oY = -self._nVertBorder
            row, col, offX = (0, 0, 0)
            self._arrUpdatePos = []
            for v in self.GetAllItem():
                pos = [
                 oX + offX, oY - row]
                if isinstance(v, CCNode):
                    self._arrUpdatePos.append(None)
                    v.setPosition(*pos)
                else:
                    self._arrUpdatePos.append(pos)
                col += 1
                offX += nHorzSpace
                if col == self._nNumPerUnit:
                    col = 0
                    offX = 0
                    row += nVertSpace

            self._nodeContainer.SetPosition(0, H)
            return size