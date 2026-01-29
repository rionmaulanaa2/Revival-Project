# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCHorzAsyncList.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCAsyncList import CCAsyncList
from .CCHorzAsyncContainer import CCHorzAsyncContainer
from common.utils.cocos_utils import CCSize

@ProxyClass()
class CCHorzAsyncList(CCAsyncList):

    def __init__(self, node):
        super(CCHorzAsyncList, self).__init__(node, CCHorzAsyncContainer)
        self._lastScrollOffset = None
        self._left_visible_range = 1
        self._right_visible_range = 2
        return

    def _registerInnerEvent(self):
        super(CCHorzAsyncList, self)._registerInnerEvent()
        self.setDirection(ccui.SCROLLVIEW_DIRECTION_HORIZONTAL)

    def SetContentSize(self, sw, sh):
        sz = self.CalcSize(sw, sh)
        W, H = self._container.GetContentSize()
        sz.height = H
        self.setContentSize(sz)
        self._refreshItemPos()
        self._testScrollAndLoad()
        return sz

    def _refreshItemPos(self):
        W, H = self.GetContentSize()
        CW, CH = self._container.GetContentSize()
        if H != CH:
            H = CH
            self.setContentSize(CCSize(W, H))
        sz = CCSize(max(CW, W), max(CH, H))
        self.SetInnerContentSize(sz.width, sz.height)
        self._container.SetPosition(0, sz.height)

    def SetVisibleRange(self, left_range, right_range):
        self._left_visible_range = left_range
        self._right_visible_range = right_range

    def SetInitCount(self, nCurCount, need_load=True):
        super(CCHorzAsyncList, self).SetInitCount(nCurCount)
        if need_load:
            self._testScrollAndLoad()

    def _canAyncLoad(self):
        if self.GetItemCount() == 0:
            return False
        else:
            if self._lastScrollOffset is None:
                self._lastScrollOffset = self.GetContentOffset()
                return True
            offset = self.GetContentOffset()
            if abs(offset.x - self._lastScrollOffset.x) > self._container.GetCtrlSize().width:
                self._lastScrollOffset = offset
                return True
            return False
            return

    def _updateVisibleData(self):
        self._startVisiIndex, self._endVisiIndex = self.GetVisibleRange()

    def GetVisibleRange(self):
        ctrlW, ctrlH = self._container.GetCtrlSize().width, self._container.GetCtrlSize().height
        viewSize = self.getContentSize()
        offset = self.GetContentOffset()
        calcWidth = -offset.x - self._container.GetHorzBorder()
        nWidth = ctrlW + self._container.GetHorzIndent()
        nUnitStart = calcWidth // nWidth
        nUnitEnd = (calcWidth + viewSize.width) // nWidth
        nUnitStart = int((nUnitStart - self._left_visible_range) * self._container.GetNumPerUnit())
        nUnitEnd = int((nUnitEnd + self._right_visible_range) * self._container.GetNumPerUnit())
        maxIndex = self.GetItemCount()
        return (
         min(max(nUnitStart, 0), maxIndex), min(max(nUnitEnd, 0), maxIndex))

    def SetFadeInOut(self, fade_in_out):
        self.use_fade_in_out = fade_in_out


class CCHorzAsyncListCreator(CCNodeCreator):
    COM_NAME = 'CCHorzAsyncList'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('numPerUnit', 1),
     ('horzBorder', 0),
     ('vertBorder', 0),
     ('horzIndent', 0),
     ('vertIndent', 0),
     (
      'template_info', {}),
     ('template', 'default/ccbfile_default'),
     (
      'customize_info', {}),
     ('initCount', 0),
     (
      'initCountEditorOnly', True),
     (
      'bounces', True),
     (
      'fadeInOut', False),
     ('fadeInStartPoint', 0.0),
     ('fadeInEndPoint', 0.0),
     ('fadeOutStartPoint', 1.0),
     ('fadeOutEndPoint', 1.0)]

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, bounces, initCountEditorOnly, fadeInOut, fadeInStartPoint, fadeInEndPoint, fadeOutStartPoint, fadeOutEndPoint):
        obj = CCHorzAsyncList.Create()
        obj.SetNumPerUnit(numPerUnit)
        obj.SetHorzBorder(horzBorder)
        obj.SetVertBorder(vertBorder)
        obj.SetHorzIndent(horzIndent)
        obj.SetVertIndent(vertIndent)
        obj.setBounceEnabled(bounces)
        obj.SetFadeInOutEnabled(fadeInOut, 0, [fadeInStartPoint, fadeInEndPoint, fadeOutStartPoint, fadeOutEndPoint])
        obj.SetTemplate(template, template_info)
        obj.SetCustomizeConf(customize_info)
        if not initCountEditorOnly:
            obj.SetInitCount(initCount)
        else:
            obj.SetInitCount(0)
        return obj