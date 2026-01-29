# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCVerTemplateList.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from common.utils.cocos_utils import CCSize, ccp
from .ScrollList import ScrollList
from .CCHorzTemplateList import CCHorzTemplateListCreator
from .CCVerContainer import CCVerContainer

@ProxyClass()
class CCVerTemplateList(ScrollList):

    def __init__(self, node):
        super(CCVerTemplateList, self).__init__(node, CCVerContainer)
        self._bottom_margin = 0

    def _registerInnerEvent(self):
        super(CCVerTemplateList, self)._registerInnerEvent()
        self.setDirection(ccui.SCROLLVIEW_DIRECTION_VERTICAL)

    def SetContentSize(self, sw, sh):
        sz = self.CalcSize(sw, sh)
        W, H = self._container.GetContentSize()
        sz.width = W
        self.setContentSize(sz)
        self._refreshItemPos()
        return sz

    def _refreshItemPos(self):
        W, H = self.GetContentSize()
        CW, CH = self._container.GetContentSize()
        if W != CW:
            W = CW
            self.setContentSize(CCSize(W, H))
        sz = CCSize(max(CW, W), max(CH, H))
        self.SetInnerContentSize(sz.width, sz.height + self._bottom_margin)
        self._container.SetPosition(0, sz.height + self._bottom_margin)

    def SetInitCount(self, nCurCount):
        super(CCVerTemplateList, self).SetInitCount(nCurCount)
        self.ScrollToTop()

    def SetExtraBottomMargin(self, margin):
        W, H = self.GetContentSize()
        CW, CH = self._container.GetContentSize()
        width, height = max(CW, W), max(CH, H)
        pos = self.GetContentOffset()
        self.SetInnerContentSize(width, height + margin)
        self._container.SetPosition(0, height + margin)
        old_margin = self._bottom_margin
        self._bottom_margin = margin
        self.SetContentOffset(ccp(pos.x, pos.y - (margin - old_margin)))
        for child in self.GetChildren():
            if child.widget_name != '_container':
                if margin:
                    posy = child.getPositionY()
                    child.setPositionY(posy + (margin - old_margin))
                else:
                    child.ReConfPosition()


class CCVerTemplateListCreator(CCHorzTemplateListCreator):
    COM_NAME = 'CCVerTemplateList'

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, bounces, template_info, customize_info, initCountEditorOnly):
        obj = CCVerTemplateList.Create()
        obj.setBounceEnabled(bounces)
        CCHorzTemplateListCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, initCountEditorOnly)
        return obj