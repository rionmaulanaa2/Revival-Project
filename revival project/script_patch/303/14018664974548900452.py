# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCAnimateSprite.py
from __future__ import absolute_import
from __future__ import print_function
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCSprite import CCSprite
from common.utils.cocos_utils import BlendValue, BlendFactorMap
from common.utils.ui_utils import GetPlistConf
config_animate_sprite_tag = 10000

@ProxyClass()
class CCAnimateSprite(CCSprite):

    def __init__(self, node):
        super(CCAnimateSprite, self).__init__(node)
        self._plist = None
        self._path = None
        self._frame_paths = None
        self._frameDelay = 0.1
        self._playing = False
        self._repeatCount = True
        return

    def _registerInnerEvent(self):
        super(CCAnimateSprite, self)._registerInnerEvent()
        self.UnBindMethod('OnPlayAniEnd')

    def SetFrameDelay(self, frameDelay):
        self._frameDelay = frameDelay
        if self._playing:
            self.ReStart()

    def SetRepeatCount(self, nRepeat):
        self._repeatCount = nRepeat
        if self._playing:
            self.ReStart()

    def SetAniSptDisplayFrameByPath(self, plist, path=None):
        self._plist = plist
        self._path = path
        self.TryLoadFrameNames()
        if self._playing:
            self.ReStart()

    def TryLoadFrameNames(self):
        self._frame_paths = GetPlistConf(self._plist)
        if not self._frame_paths:
            return False
        if self._path not in self._frame_paths:
            self._path = self._frame_paths[0]
        plist = global_data.uisystem.GetAnimPlistByConfig(self._plist)
        cc.SpriteFrameCache.getInstance().addSpriteFrames(plist)
        return True

    def Play(self):
        if self._playing:
            return
        if not self.TryLoadFrameNames():
            return
        self.Stop()
        arrayFrame = []
        for v in self._frame_paths:
            frame = cc.SpriteFrameCache.getInstance().getSpriteFrame(v)
            if not frame:
                print('error frame [%s] not in sprite frame cache' % v)
                break
            arrayFrame.append(frame)

        animation = cc.Animation.createWithSpriteFrames(arrayFrame, self._frameDelay)
        ani = cc.Animate.create(animation)
        if self._repeatCount > 0:
            ani = cc.Repeat.create(ani, self._repeatCount)
        else:
            ani = cc.Repeat.create(ani, 9999999)
        ani = cc.Sequence.create([
         ani,
         cc.CallFunc.create(self._on_play_ani_end)])
        ani.setTag(config_animate_sprite_tag)
        self.runAction(ani)
        self._playing = True

    def _on_play_ani_end(self):
        self.OnPlayAniEnd()

    def Stop(self):
        self.stopActionByTag(config_animate_sprite_tag)
        self._playing = False

    def ReStart(self):
        self.Stop()
        self.Play()

    def SetCurFrame(self, index):
        if not self.TryLoadFrameNames():
            return
        try:
            fn = self._frame_paths[index]
        except IndexError:
            return

        self._path = fn
        self.SetDisplayFrameByPath(self._plist, fn)

    def GetFrameCount(self):
        if not self.TryLoadFrameNames():
            return 0
        return len(self._frame_paths)

    def GetPlayDuration(self):
        return self.GetFrameCount() * self._frameDelay


class CCAnimateSpriteCreator(CCNodeCreator):
    COM_NAME = 'CCAnimateSprite'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('plist', 'gui/default/default_ani.plist'),
     ('frameDelay', 0.1),
     ('repeatCount', -1),
     (
      'isPlay', True),
     (
      'blendFun', {'src': BlendValue['BLEND_ONE'],'dst': BlendValue['BLEND_INVSRCALPHA']})]

    @staticmethod
    def create(parent, root, plist, frameDelay, repeatCount, isPlay, blendFun, opacity):
        obj = CCAnimateSprite.Create()
        obj.SetFrameDelay(frameDelay)
        obj.SetRepeatCount(repeatCount)
        obj.SetAniSptDisplayFrameByPath(plist)
        obj.setBlendFunc((blendFun['src'], blendFun['dst']))
        obj.setOpacity(opacity)
        if isPlay:
            obj.Play()
        return obj

    @staticmethod
    def check_config--- This code section failed: ---

 166       0  LOAD_FAST             0  'conf'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'blendFun'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'blendConf'

 167      18  BUILD_MAP_2           2 
          21  LOAD_GLOBAL           2  'BlendFactorMap'
          24  LOAD_FAST             1  'blendConf'
          27  LOAD_CONST            2  'src'
          30  BINARY_SUBSCR    
          31  BINARY_SUBSCR    
          32  LOAD_CONST            2  'src'
          35  STORE_MAP        
          36  LOAD_GLOBAL           2  'BlendFactorMap'
          39  LOAD_FAST             1  'blendConf'
          42  LOAD_CONST            3  'dst'
          45  BINARY_SUBSCR    
          46  BINARY_SUBSCR    
          47  LOAD_CONST            3  'dst'
          50  STORE_MAP        
          51  STORE_MAP        
          52  STORE_MAP        
          53  STORE_MAP        
          54  STORE_SUBSCR     
          55  LOAD_CONST            0  ''
          58  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 51