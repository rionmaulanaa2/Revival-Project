# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCCheckButtonGroup.py
from __future__ import absolute_import
from common.uisys.ui_proxy import ProxyClass
from .CCDirContainer import CCDirContainer, CCDirContainerCreator

@ProxyClass()
class CCCheckButtonGroup(CCDirContainer):

    def __init__(self, node):
        super(CCCheckButtonGroup, self).__init__(node)
        self._iCheckIndex = None
        return

    def _registerInnerEvent(self):
        super(CCCheckButtonGroup, self)._registerInnerEvent()
        self.UnBindMethod('OnGroupCheck')
        self.UnBindMethod('SetGroupChecked')
        self.UnBindMethod('OnGroupChecked')

    def SetCheck(self, index, bCheck):
        if self._iCheckIndex == index:
            return
        if not bCheck:
            return
        check_index = index
        node = self.GetItem(check_index)
        if node:
            ret = self.OnGroupChecked(node, True, check_index)
            if not ret or ret[-1]:
                for button in self.GetAllItem():
                    if button.isValid():
                        self.SetGroupChecked(button, False, check_index)

                self.SetGroupChecked(node, True, check_index)
                self.OnGroupChecked(node, True, check_index)
        else:
            log_error('CCCheckButtonGroup: Index out of boundary!')

    def GetCheckButton(self):
        return (
         self.GetItem(self._iCheckIndex), self._iCheckIndex)


class CCCheckButtonCreator(CCDirContainerCreator):
    COM_NAME = 'CCCheckButtonGroup'
    ATTR_DEFINE = CCDirContainerCreator.ATTR_DEFINE + [
     ('selIndex', 1)]

    @staticmethod
    def create(parent, root, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template, initCount, template_info, customize_info, bHorizon, initCountEditorOnly):
        obj = CCCheckButtonGroup.Create()
        CCDirContainerCreator.container_set_attr(obj, numPerUnit, horzBorder, vertBorder, horzIndent, vertIndent, template_info, template, customize_info, initCount, bHorizon, initCountEditorOnly)
        return obj

    @staticmethod
    def set_attr_group_selIndex(obj, parent, root, selIndex):
        pass