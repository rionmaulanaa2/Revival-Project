# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCVerContainer.py
from __future__ import absolute_import
from common.uisys.ui_proxy import ProxyClass
from .CCHorzContainer import CCHorzContainerCreator
from common.utils.cocos_utils import CCSizeZero, CCSize
from .CCContainer import CCContainer

@ProxyClass()
class CCVerContainer(CCContainer):

    def __init__(self, node):
        super(CCVerContainer, self).__init__(node)
        self._force_w = None
        return

    def SetForceW(self, height):
        self._force_w = height

    def _refreshItemPos(self, is_cal_scale=False, is_cal_visible=False):
        if len(self._child_item) == 0:
            self.setContentSize(CCSizeZero)
            self._nodeContainer.SetPosition(0, 0)
            return CCSizeZero
        else:
            if self._nNumPerUnit == 1:
                W, H = 2 * self._nHorzBorder, 2 * self._nVertBorder
                oX = self._nHorzBorder
                oY = -self._nVertBorder
                H = H + (self._nUnit - 1) * self._nVertIndent
                w = 0
                for i, v in enumerate(self._child_item):
                    if is_cal_visible and not v.isVisible():
                        continue
                    v.SetPosition(oX, oY)
                    w, h = self._getItemContentSize(i, v)
                    if is_cal_scale:
                        w = w * v.getScaleX()
                        h = h * v.getScaleY()
                    oY = oY - h - self._nVertIndent
                    H = H + h

                W = W + w
                if self._force_w is not None:
                    W = self._force_w
                    for i, v in enumerate(self._child_item):
                        if is_cal_visible and not v.isVisible():
                            continue
                        w, h = self._getItemContentSize(i, v)
                        cur_x, cur_y = v.GetPosition()
                        v.SetPosition(cur_x + 0.5 * (W - w), cur_y)

                size = CCSize(W, H)
                self.setContentSize(size)
                self._nodeContainer.SetPosition(0, H)
                return size
            ctrlW, ctrlH = self._getItemContentSize(0, self._child_item[0])
            nHorzSpace = ctrlW + self._nHorzIndent
            nVertSpace = ctrlH + self._nVertIndent
            oX = self._nHorzBorder
            W = self._nNumPerUnit * (ctrlW + self._nHorzIndent) - self._nHorzIndent + 2 * self._nHorzBorder
            H = self._nUnit * (ctrlH + self._nVertIndent) - self._nVertIndent + 2 * self._nVertBorder
            size = CCSize(W, H)
            self.setContentSize(size)
            oY = -self._nVertBorder
            row, col, offX = (0, 0, 0)
            for v in self.GetAllItem():
                v.SetPosition(oX + offX, oY - row)
                col += 1
                offX += nHorzSpace
                if col == self._nNumPerUnit:
                    col = 0
                    offX = 0
                    row += nVertSpace

            self._nodeContainer.SetPosition(0, H)
            return size


class CCVerContainerCreator(CCHorzContainerCreator):
    COM_NAME = 'CCVerContainer'

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, initCountEditorOnly):
        obj = CCVerContainer.Create()
        CCHorzContainerCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, initCountEditorOnly)
        return obj