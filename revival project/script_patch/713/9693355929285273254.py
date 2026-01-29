# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCVerAsyncList.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCAsyncList import CCAsyncList
from .CCVerAsyncContainer import CCVerAsyncContainer
from common.utils.cocos_utils import CCSize
from .CCHorzAsyncList import CCHorzAsyncListCreator

@ProxyClass()
class CCVerAsyncList(CCAsyncList):

    def __init__(self, node):
        super(CCVerAsyncList, self).__init__(node, CCVerAsyncContainer)
        self._lastScrollOffset = None
        return

    def SetContentSize(self, sw, sh):
        sz = self.CalcSize(sw, sh)
        W, H = self._container.GetContentSize()
        sz.width = W
        self.setContentSize(sz)
        self._refreshItemPos()
        self._testScrollAndLoad()
        return sz

    def _refreshItemPos(self):
        W, H = self.GetContentSize()
        CW, CH = self._container.GetContentSize()
        if W != CW:
            W = CW
            self.setContentSize(CCSize(W, H))
        sz = CCSize(max(CW, W), max(CH, H))
        self.SetInnerContentSize(sz.width, sz.height)
        self._container.SetPosition(0, sz.height)

    def SetInitCount(self, nCurCount, need_load=True):
        super(CCVerAsyncList, self).SetInitCount(nCurCount)
        if need_load:
            self._testScrollAndLoad()

    def _registerInnerEvent(self):
        super(CCVerAsyncList, self)._registerInnerEvent()
        self.setDirection(ccui.SCROLLVIEW_DIRECTION_VERTICAL)

    def _canAyncLoad(self):
        if self.GetItemCount() == 0:
            self._lastScrollOffset = None
            return False
        else:
            if self._lastScrollOffset is None:
                self._lastScrollOffset = self.GetContentOffset()
                return True
            if self.getContentSize().height >= self.GetInnerContentSize().height:
                return True
            if self.getContentSize().height + 2 * self._container.GetCtrlSize().height >= self.GetInnerContentSize().height:
                return True
            offset = self.GetContentOffset()
            if abs(offset.y - self._lastScrollOffset.y) > self._container.GetCtrlSize().height:
                self._lastScrollOffset = offset
                return True
            return False
            return

    def _updateVisibleData(self):
        self._startVisiIndex, self._endVisiIndex = self.GetVisibleRange()

    def GetVisibleRange(self):
        ctrlH = self._container.GetCtrlSize().height
        contentSize = self.GetInnerContentSize()
        viewSize = self.getContentSize()
        offset = self.GetContentOffset()
        calcHeight = contentSize.height + offset.y - self._container.GetVertBorder()
        nHeight = ctrlH + self._container.GetVertIndent()
        nUnitStart = (calcHeight - viewSize.height) // nHeight
        nUnitEnd = calcHeight // nHeight
        nUnitStart = int((nUnitStart - 1) * self._container.GetNumPerUnit())
        nUnitEnd = int((nUnitEnd + 3) * self._container.GetNumPerUnit())
        maxIndex = self.GetItemCount()
        return (
         min(max(nUnitStart, 0), maxIndex), min(max(nUnitEnd, 0), maxIndex))


class CCVerAsyncListCreator(CCHorzAsyncListCreator):
    COM_NAME = 'CCVerAsyncList'

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, bounces, initCountEditorOnly, fadeInOut, fadeInStartPoint, fadeInEndPoint, fadeOutStartPoint, fadeOutEndPoint):
        obj = CCVerAsyncList.Create()
        obj.SetNumPerUnit(numPerUnit)
        obj.SetHorzBorder(horzBorder)
        obj.SetVertBorder(vertBorder)
        obj.SetHorzIndent(horzIndent)
        obj.SetVertIndent(vertIndent)
        obj.setBounceEnabled(bounces)
        obj.SetFadeInOutEnabled(fadeInOut, 1, [fadeInStartPoint, fadeInEndPoint, fadeOutStartPoint, fadeOutEndPoint])
        obj.SetTemplate(template, template_info)
        obj.SetCustomizeConf(customize_info)
        if not initCountEditorOnly:
            obj.SetInitCount(initCount)
        else:
            obj.SetInitCount(0)
        return obj