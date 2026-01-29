# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCHorzContainer.py
from __future__ import absolute_import
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from common.utils.cocos_utils import CCSizeZero, CCSize
from .CCContainer import CCContainer

@ProxyClass()
class CCHorzContainer(CCContainer):

    def __init__(self, node):
        super(CCHorzContainer, self).__init__(node)
        self._force_h = None
        return

    def SetForceH(self, height):
        self._force_h = height

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
                W = W + (self._nUnit - 1) * self._nHorzIndent
                max_h = 0
                for i, v in enumerate(self._child_item):
                    if is_cal_visible and not v.isVisible():
                        continue
                    w, h = self._getItemContentSize(i, v)
                    if is_cal_scale:
                        w = w * v.getScaleX()
                        h = h * v.getScaleY()
                    v.SetPosition(oX, oY)
                    if h > max_h:
                        max_h = h if 1 else max_h
                        oX = oX + w + self._nHorzIndent
                        W = W + w

                H = H + max_h
                if self._inverse_order:
                    for i, v in enumerate(self._child_item):
                        if is_cal_visible and not v.isVisible():
                            continue
                        x, y = v.GetPosition()
                        w, h = self._getItemContentSize(i, v)
                        if is_cal_scale:
                            w = w * v.getScaleX()
                        v.SetPosition(W - x - w, y)

                if self._force_h is not None:
                    H = self._force_h
                    for i, v in enumerate(self._child_item):
                        if is_cal_visible and not v.isVisible():
                            continue
                        w, h = self._getItemContentSize(i, v)
                        cur_x, cur_y = v.GetPosition()
                        v.SetPosition(cur_x, cur_y + 0.5 * (h - H))

                size = CCSize(W, H)
                self.setContentSize(size)
                self._nodeContainer.SetPosition(0, H)
                return size
            ctrlW, ctrlH = self._child_item[0].GetContentSize()
            nHorzSpace = ctrlW + self._nHorzIndent
            nVertSpace = ctrlH + self._nVertIndent
            oX = self._nHorzBorder
            W = self._nUnit * (ctrlW + self._nHorzIndent) - self._nHorzIndent + 2 * self._nHorzBorder
            H = self._nNumPerUnit * (ctrlH + self._nVertIndent) - self._nVertIndent + 2 * self._nVertBorder
            size = CCSize(W, H)
            self.setContentSize(size)
            oY = -self._nVertBorder
            row, col, offY = (0, 0, 0)
            for v in self.GetAllItem():
                v.SetPosition(oX + col, oY - offY)
                row += 1
                offY += nVertSpace
                if row == self._nNumPerUnit:
                    row = 0
                    offY = 0
                    col += nHorzSpace

            self._nodeContainer.SetPosition(0, H)
            return size


class CCHorzContainerCreator(CCNodeCreator):
    COM_NAME = 'CCHorzContainer'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('numPerUnit', 1),
     ('horzBorder', 0),
     ('vertBorder', 0),
     ('horzIndent', 0),
     ('vertIndent', 0),
     ('template', 'default/ccbfile_default'),
     (
      'template_info', {}),
     ('initCount', 0),
     (
      'initCountEditorOnly', True),
     (
      'customize_info', {})]

    @staticmethod
    def container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, initCountEditorOnly):
        obj.SetNumPerUnit(numPerUnit)
        obj.SetHorzBorder(horzBorder)
        obj.SetVertBorder(vertBorder)
        obj.SetHorzIndent(horzIndent)
        obj.SetVertIndent(vertIndent)
        obj.SetTemplate(template, template_info)
        obj.SetCustomizeConf(customize_info)
        if not initCountEditorOnly:
            obj.SetInitCount(initCount)
        else:
            obj.SetInitCount(0)

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, initCountEditorOnly):
        obj = CCHorzContainer.Create()
        CCHorzContainerCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, initCountEditorOnly)
        return obj