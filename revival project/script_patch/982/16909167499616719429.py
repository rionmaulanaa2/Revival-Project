# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCHorzTemplateList.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCHorzContainer import CCHorzContainer, CCHorzContainerCreator
from common.utils.cocos_utils import CCSize
from .ScrollList import ScrollList

@ProxyClass()
class CCHorzTemplateList(ScrollList):

    def __init__(self, node):
        super(CCHorzTemplateList, self).__init__(node, CCHorzContainer)

    def _registerInnerEvent(self):
        super(CCHorzTemplateList, self)._registerInnerEvent()
        self.setDirection(ccui.SCROLLVIEW_DIRECTION_HORIZONTAL)

    def SetContentSize(self, sw, sh):
        sz = self.CalcSize(sw, sh)
        W, H = self._container.GetContentSize()
        sz.height = H
        self.setContentSize(sz)
        self._refreshItemPos()
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


class CCHorzTemplateListCreator(CCHorzContainerCreator):
    COM_NAME = 'CCHorzTemplateList'
    ATTR_DEFINE = CCHorzContainerCreator.ATTR_DEFINE + [
     (
      'bounces', True)]

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, bounces, template_info, customize_info, initCountEditorOnly):
        obj = CCHorzTemplateList.Create()
        obj.setBounceEnabled(bounces)
        CCHorzContainerCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, initCountEditorOnly)
        return obj