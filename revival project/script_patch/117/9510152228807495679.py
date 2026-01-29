# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCHorzScrollPage.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCHorzContainer import CCHorzContainerCreator
from .CCHorzTemplateList import CCHorzTemplateList
import time

@ProxyClass()
class CCHorzScrollPage(CCHorzTemplateList):

    def __init__(self, node):
        super(CCHorzScrollPage, self).__init__(node)
        self._nCurViewPage = -1
        self._bBeginAnimate = False
        self.bBeginScroll = False
        self.begin_tick = None
        self.begin_offset = None
        return

    def _registerInnerEvent(self):
        super(CCHorzScrollPage, self)._registerInnerEvent()
        self.setBounceEnabled(False)
        self.UnBindMethod('OnViewPage')

        @self.callback()
        def OnScrolling(ctrl):
            if self.GetItemCount() == 0:
                return
            if self.isDragging():
                self._bBeginAnimate = False
                if self.bBeginScroll is False:
                    self.bBeginScroll = True
                    self.begin_tick = time.time()
                    self.begin_offset = self.getContentOffset()
            else:
                if self._bBeginAnimate or not self.bBeginScroll:
                    return
                self.bBeginScroll = False
                focusedIndex = self._calcCurFocusePos()
                if focusedIndex != self._nCurViewPage:
                    self.SetViewPage(focusedIndex, True, True)
                else:
                    speed = (self.getContentOffset().x - self.begin_offset.x) / max(time.time() - self.begin_tick, 1e-05)
                    page_turn_factor = self.getViewSize().width / 4
                    if speed < -page_turn_factor:
                        self.SetViewPage(focusedIndex + 1, True, True)
                    elif speed > page_turn_factor:
                        self.SetViewPage(focusedIndex - 1, True, True)
                    else:
                        self.SetViewPage(focusedIndex, True, True)

    def GetCurPageIndex(self):
        return self._nCurViewPage

    def _calcCurFocusePos(self):
        centerPos = self.getViewSize().width / 2 - self.getContentOffset().x
        allItem = self.GetAllItem()
        focusedIndex = 0
        focusedX = allItem[focusedIndex].getPosition().x
        for idx in range(1, self.GetItemCount()):
            if abs(focusedX - centerPos) > abs(allItem[idx].getPosition().x - centerPos):
                focusedIndex = idx
                focusedX = allItem[focusedIndex].getPosition().x

        return focusedIndex

    def SetViewPage(self, index, is_animate, bTriggerEvent=False):
        if self._nCurViewPage == index:
            return
        count = self.GetItemCount()
        if count == 0:
            return
        self.getContainer().stopAllActions()
        self.LocatePosByItem(index, 0.15 if is_animate else 0)
        self._bBeginAnimate = is_animate
        self._nCurViewPage = index
        self.OnViewPage(index)

    def BindPagePointer(self, pagePointer):

        @self.callback()
        def OnViewPage(ctrl, index):
            if pagePointer:
                pagePointer.SetTotalPage(self.GetItemCount())
                pagePointer.SetCurrentPage(index)

        OnViewPage(self, self._nCurViewPage)

        def _func():
            self.UnBindMethod('OnViewPage')

        return _func


class CCHorzScrollPageCreator(CCNodeCreator):
    COM_NAME = 'CCHorzScrollPage'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('horzBorder', 0),
     ('vertBorder', 0),
     ('horzIndent', 0),
     ('template', 'default/ccbfile_default'),
     ('initCount', 0),
     (
      'initCountEditorOnly', True),
     (
      'template_info', {}),
     (
      'customize_info', {})]

    @staticmethod
    def create(parent, root, horzBorder, vertBorder, horzIndent, template, initCount, template_info, customize_info, initCountEditorOnly):
        obj = CCHorzScrollPage.Create()
        CCHorzContainerCreator.container_set_attr(obj, 1, horzBorder, vertBorder, horzIndent, 0, template_info, template, customize_info, initCount, initCountEditorOnly)
        return obj