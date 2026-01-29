# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCSlider.py
from __future__ import absolute_import
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCUIWidget import CCUIWidget
from common.utils.cocos_utils import CCRect
import cc

@ProxyClass(ccui.Slider)
class CCSlider(CCUIWidget):
    TAG_OF_UPDATE = 210916

    def _registerInnerEvent(self):
        self.UnBindMethod('OnPercentageChanged')

        def func(slider, event):
            if event == 0:
                self.OnPercentageChanged(slider)

        self.addEventListener(func)

    def LoadSlidBallTextureNormal(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadSlidBallTextureNormal(path, tag)

    def LoadSlidBallTexturePressed(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadSlidBallTexturePressed(path, tag)

    def LoadSlidBallTextureDisabled(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadSlidBallTextureDisabled(path, tag)

    def LoadBarTexture(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadBarTexture(path, tag)

    def LoadProgressBarTexture(self, path):
        tag = global_data.uisystem.LoadSpriteFramesByPath(path)
        global_data.uisystem.RecordSpriteUsage('', path, self)
        self.loadProgressBarTexture(path, tag)

    def _OnSetPercentage(self, percentage):
        percentage = min(max(percentage, 0), 100)
        self.setPercent(percentage)

    def SetPercent(self, target_percent, time=0, tick_cb=None, end_cb=None, tick_time=0.05):
        if time <= 0:
            self._OnSetPercentage(target_percent)
            return
        start_percent = self.getPercent()
        diff_percent = target_percent - start_percent
        per_tick = tick_time
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
        repeat_action = cc.Repeat.create(seq_action, tick_times)
        final_action = cc.Sequence.create([repeat_action, cc.CallFunc.create(finalCallback)])
        final_action.setTag(self.TAG_OF_UPDATE)
        self.stopActionByTag(self.TAG_OF_UPDATE)
        self.runAction(final_action)


class CCSliderCreator(CCNodeCreator):
    COM_NAME = 'CCSlider'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'normalBallTex', {'plist': '','path': 'gui/default/sliderthumb.png'}),
     (
      'selectedBallTex', {'plist': '','path': 'gui/default/sliderthumb.png'}),
     (
      'disabledBallTex', {'plist': '','path': 'gui/default/sliderthumb.png'}),
     (
      'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
     (
      'capInsetsProgress', {'x': 0,'y': 0,'width': 0,'height': 0}),
     (
      'barTex', {'plist': '','path': 'gui/default/slidertrack.png'}),
     (
      'progressBarTex', {'plist': '','path': 'gui/default/sliderprogress.png'}),
     ('percentage', 0),
     (
      'scale9Enabled', True)]

    @staticmethod
    def create(parent, root, normalBallTex, selectedBallTex, disabledBallTex, capInsets, capInsetsProgress, barTex, progressBarTex, percentage, scale9Enabled):
        obj = CCSlider.Create()
        obj.setScale9Enabled(scale9Enabled)
        obj.LoadSlidBallTextureNormal(normalBallTex['path'])
        obj.LoadSlidBallTexturePressed(selectedBallTex['path'])
        obj.LoadSlidBallTextureDisabled(disabledBallTex['path'])
        obj.LoadBarTexture(barTex['path'])
        obj.LoadProgressBarTexture(progressBarTex['path'])
        obj.setCapInsetsBarRenderer(CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height']))
        obj.setCapInsetProgressBarRebderer(CCRect(capInsetsProgress['x'], capInsetsProgress['y'], capInsetsProgress['width'], capInsetsProgress['height']))
        obj.setPercent(percentage)
        return obj