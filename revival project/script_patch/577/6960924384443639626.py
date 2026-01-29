# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCCheckButton.py
from __future__ import absolute_import
import six
from common.uisys.ui_proxy import ProxyClass
from .CCButton import CCButton, CCButtonCreator, STATE_DISABLED, STATE_SELECTED, STATE_NORMAL

@ProxyClass()
class CCCheckButton(CCButton):

    def __init__(self, node):
        super(CCCheckButton, self).__init__(node)
        self._bCheck = False
        self._group = None
        return

    def _registerInnerEvent(self):
        super(CCCheckButton, self)._registerInnerEvent()
        self.UnBindMethod('OnCheck')
        self.UnBindMethod('OnChecked')

        @self.callback()
        def OnClick(btn, pt):
            self.SetCheck(not self._bCheck, True)

    def SetButtonGroup(self, buttons):
        self.SetCheck(False)
        self._group = buttons
        if self not in buttons:
            buttons.append(self)

    def _rawSetCheck(self, bCheck, bUpdate):
        self._bCheck = bCheck
        if bUpdate:
            self._updateCurState()

    def SetCheck(self, bCheck, bTriggerEvent=False):
        if self._bCheck == bCheck:
            return
        else:
            if self._group is None:
                if bTriggerEvent:
                    ret = self.OnCheck(bCheck, None)
                    if ret is None or bool(ret):
                        self._bCheck = bCheck
                        self.OnChecked(bCheck, None)
                else:
                    self._bCheck = bCheck
            else:
                if not bCheck:
                    return
                if bTriggerEvent:
                    check_index = self._group.index(self)
                    ret = self.OnCheck(True, check_index)
                    if not ret or ret[-1]:
                        for button in self._group:
                            if button.isValid():
                                button._rawSetCheck(False, True)

                        self._bCheck = True
                        self.OnChecked(True, check_index)
                else:
                    for button in self._group:
                        if button.isValid():
                            button._rawSetCheck(False, True)

                    self._bCheck = True
            self._updateCurState()
            return

    def GetCheck(self):
        return self._bCheck

    def GetCheckButton(self):
        if self._group is not None:
            for button in self._group:
                if button.GetCheck():
                    return (button, self._group.index(button))

        return

    def _updateCurState(self, setState=None, need_scale=False, scale_state=False):
        if setState is not None:
            self._curState = setState
        curState = self._curState
        bCheck = self._bCheck
        if self._text is not None:
            if curState == STATE_DISABLED:
                self._text._obj.setColor(self._display_textsColors[curState])
            else:
                self._text._obj.setColor(self._display_textsColors[STATE_SELECTED if bCheck else STATE_NORMAL])
        for state, spt in six.iteritems(self._display_spts):
            if spt is not None:
                if curState == STATE_DISABLED:
                    spt._obj.setVisible(state == curState)
                else:
                    spt._obj.setVisible(state == (STATE_SELECTED if bCheck else STATE_NORMAL))

        if need_scale:
            if scale_state:
                if self.__oldScale is None:
                    self.__oldScale = [
                     self._obj.getScaleX(), self._obj.getScaleY()]
                    self._obj.setScaleX(self.__oldScale[0] * self._zoomScale)
                    self._obj.setScaleY(self.__oldScale[1] * self._zoomScale)
            elif self.__oldScale is not None:
                self._obj.setScaleX(self.__oldScale[0])
                self._obj.setScaleY(self.__oldScale[1])
                self.__oldScale = None
        return


class CCCheckButtonCreator(CCButtonCreator):
    COM_NAME = 'CCCheckButton'
    ATTR_DEFINE = CCButtonCreator.ATTR_DEFINE + [
     (
      '9sprite', False),
     ('plist', ''),
     ('frame1', 'gui/default/check_off.png'),
     ('frame2', 'gui/default/check_on.png'),
     ('frame3', 'gui/default/check_off.png'),
     (
      'check', False)]

    @staticmethod
    def create(parent, root, check, swallow, noEventAfterMove, move_dist):
        obj = CCCheckButton.Create()
        obj.SetCheck(check, False)
        obj.SetSwallowTouch(swallow)
        obj.SetNoEventAfterMove(noEventAfterMove, move_dist)
        return obj