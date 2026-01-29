# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLoadingBar.py
from __future__ import absolute_import
from __future__ import print_function
import ccui
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import CCRect, ccp

@ProxyClass(ccui.LoadingBar)
class CCLoadingBar(CCNode):
    TAG_OF_UPDATE = 999

    def __init__(self, node):
        super(CCLoadingBar, self).__init__(node)
        self._cur_path = None
        self._tailCCBFile = None
        return

    def _registerInnerEvent(self):
        super(CCLoadingBar, self)._registerInnerEvent()
        self.UnBindMethod('OnSetPercentage')

    def _OnSetPercentage(self, percentage, bTriggerEvent=True):
        percentage = min(max(percentage, 0), 100)
        self.setPercent(percentage)
        self._UpdateTailFramePosition()
        if bTriggerEvent:
            self.OnSetPercentage(percentage)

    def StopPercentAni(self):
        self.stopActionByTag(self.TAG_OF_UPDATE)

    def StopPercentageAni(self):
        self.stopActionByTag(self.TAG_OF_UPDATE)

    def SetPercent(self, target_percent, time=0, tick_cb=None, end_cb=None):
        if time <= 0:
            self._OnSetPercentage(target_percent)
            return
        start_percent = self.getPercent()
        diff_percent = target_percent - start_percent
        per_tick = 0.05
        tick_times = time / per_tick
        step_percent = diff_percent / tick_times

        def callback():
            self._OnSetPercentage(self.getPercent() + step_percent)
            if tick_cb is not None:
                tick_cb()
            return

        def finalCallback():
            self._OnSetPercentage(target_percent)
            if tick_cb is not None:
                tick_cb()
            if end_cb is not None:
                end_cb()
            return

        seq_action = cc.Sequence.create([cc.DelayTime.create(per_tick), cc.CallFunc.create(callback)])
        repeat_action = cc.Repeat.create(seq_action, int(tick_times))
        final_action = cc.Sequence.create([repeat_action, cc.CallFunc.create(finalCallback)])
        final_action.setTag(self.TAG_OF_UPDATE)
        self.stopActionByTag(self.TAG_OF_UPDATE)
        self.runAction(final_action)

    def SetPercentage(self, percent):
        self.SetPercent(percent)

    def SetPath(self, plist, path):
        self.LoadTexture(path)

    def LoadTexture(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadTexture(path, tag)

    def GetPercentagePosition(self, percentage=None):
        if percentage is None:
            percentage = self.getPercent()
        vec = self.ConvertToWorldSpacePercentage(percentage, 0)
        return (
         vec.x, vec.y)

    def SetPercentageWithAni(self, percentage, duration_sec, end_cb=None):
        self.SetPercent(percentage, duration_sec, end_cb=end_cb)

    def SetTailCCBFile(self, tailCCBFile):
        if self._tailCCBFile:
            self._tailCCBFile.Destroy()
            self._tailCCBFile = None
        if tailCCBFile:
            self._tailCCBFile = global_data.uisystem.load_template_create(tailCCBFile, self)
            self._tailCCBFile.setLocalZOrder(100)
            self._UpdateTailFramePosition()
        return

    def GetTail(self):
        return self._tailCCBFile

    def _UpdateTailFramePosition(self):
        if not self._tailCCBFile:
            return
        direction = self.getDirection()
        percent = self.getPercent()
        sz = self.getContentSize()
        if direction == ccui.LOADINGBAR_DIRECTION_LEFT:
            anchor_x = 1
        else:
            anchor_x = 0
        self._tailCCBFile.setAnchorPoint(ccp(anchor_x, 0.5))
        if direction == ccui.LOADINGBAR_DIRECTION_LEFT:
            cur_point = percent / 100.0
        else:
            cur_point = 1 - percent / 100.0
        x, y = self._tailCCBFile.CalcPosition(sz.width * cur_point, '50%')
        self._tailCCBFile.setPosition(x, y)

    def SetContentSize(self, sw, sh):
        super(CCLoadingBar, self).SetContentSize(sw, sh)
        self._UpdateTailFramePosition()


class CCLoadingBarCreator(CCNodeCreator):
    COM_NAME = 'CCLoadingBar'
    DYNAMIC_ARGS = {'is9sprite': '9sprite'
       }
    DYNAMIC_ARGS.update(CCNodeCreator.DYNAMIC_ARGS)
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      '9sprite', True),
     (
      'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
     (
      'displayFrame', {'plist': '','path': 'gui/default/progressbar.png'}),
     ('direction', 0),
     ('percentage', 100),
     ('tailCCBFile', '')]
    ATTR_INIT = CCNodeCreator.ATTR_INIT + ['tailCCBFile']

    @staticmethod
    def create(parent, root, displayFrame, direction, percentage, is9sprite, capInsets, opacity):
        obj = CCLoadingBar.Create()
        obj.LoadTexture(displayFrame['path'])
        obj.setScale9Enabled(is9sprite)
        capInsets = CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height'])
        obj.setCapInsets(capInsets)
        obj.setDirection(direction)
        obj.setPercent(percentage)
        obj.setOpacity(opacity)
        return obj

    @staticmethod
    def check_config--- This code section failed: ---

 176       0  LOAD_CONST            1  '9sprite'
           3  LOAD_FAST             0  'conf'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    23  'to 23'

 177      12  POP_JUMP_IF_FALSE     1  'to 1'
          15  BINARY_SUBSCR    
          16  BINARY_SUBSCR    
          17  BINARY_SUBSCR    
          18  BINARY_SUBSCR    
          19  STORE_SUBSCR     
          20  JUMP_FORWARD          0  'to 23'
        23_0  COME_FROM                '20'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 12

    @staticmethod
    def set_attr_group_tailCCBFile(obj, parent, root, tailCCBFile):
        obj.SetTailCCBFile(tailCCBFile)