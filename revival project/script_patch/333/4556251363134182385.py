# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCDirContainer.py
from __future__ import absolute_import
from .CCContainer import CCContainer
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from common.utils.cocos_utils import CCSizeZero, CCSize

@ProxyClass()
class CCDirContainer(CCContainer):

    def _ver_refreshItemPos(self):
        if len(self._child_item) == 0:
            return CCSizeZero
        if self._nNumPerUnit == 1:
            W, H = 2 * self._nHorzBorder, 2 * self._nVertBorder
            oX = self._nHorzBorder
            oY = -self._nVertBorder
            H = H + (self._nUnit - 1) * self._nVertIndent
            for v in self._child_item:
                v.SetPosition(oX, oY)
                w, h = v.GetContentSize()
                oY = oY - h - self._nVertIndent
                H = H + h

            W = W + w
            size = CCSize(W, H)
            self.setContentSize(size)
            self._nodeContainer.SetPosition(0, H)
            return size
        ctrlW, ctrlH = self._child_item[0].GetContentSize()
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

    def _hor_refreshItemPos(self):
        if len(self._child_item) == 0:
            return CCSizeZero
        if self._nNumPerUnit == 1:
            W, H = 2 * self._nHorzBorder, 2 * self._nVertBorder
            oX = self._nHorzBorder
            oY = -self._nVertBorder
            W = W + (self._nUnit - 1) * self._nHorzIndent
            for v in self._child_item:
                v.SetPosition(oX, oY)
                w, h = v.GetContentSize()
                oX = oX + w + self._nHorzIndent
                W = W + w

            H = H + h
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

    def _refreshItemPos(self):
        if self._bVertical:
            return self._ver_refreshItemPos()
        return self._hor_refreshItemPos()

    def SetVertical(self, bVertical):
        self._bVertical = bVertical


class CCDirContainerCreator(CCNodeCreator):
    COM_NAME = 'CCDirContainer'
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
      'customize_info', {}),
     (
      'bHorizon', True)]

    @staticmethod
    def container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, bHorizon, initCountEditorOnly):
        obj.SetVertical(not bHorizon)
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
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, bHorizon, initCountEditorOnly):
        obj = CCDirContainer.Create()
        CCDirContainerCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, bHorizon, initCountEditorOnly)
        return obj