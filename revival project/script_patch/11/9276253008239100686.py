# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCButton.py
from __future__ import absolute_import
import six_ex
import six
import cc
import time
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from .CCLayer import CCLayer
from .CCUIText import CCUIText
from .CCScale9Sprite import CCScale9Sprite
from .CCSprite import CCSprite
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, CCSize
from common.uisys.color_table import get_color_val
from common.const.cocos_constant import BUTTON_CLICK_ANIM_TAG
STATE_NORMAL = 0
STATE_SELECTED = 1
STATE_DISABLED = 2
STATE_MOUSE_HOVER = 3

@ProxyClass()
class CCButton(CCLayer):

    def __init__(self, node):
        super(CCButton, self).__init__(node)
        self._display_spts = {}
        self._bUse9Spt = True
        self._plist = ''
        self._paths = []
        self._9rect = None
        self._bEnableText = True
        self._text = None
        self._text_offset = {'x': '50%','y': '50%'}
        self._text_skew = {'x': 0,'y': 0}
        self._display_textsColors = {}
        self._display_textsShadows = {}
        self._bEnableStateFontSize = False
        self._display_textsFontSize = {}
        self._bTextShadow = False
        self._shadowOffset = None
        self._bEnable = True
        self._curState = STATE_NORMAL
        self._zoomScale = True
        self.__oldScale = None
        self._bCustomState = False
        self.__orgClickState = None
        self._display_opacities = {}
        self._cur_paths = {STATE_NORMAL: None,
           STATE_SELECTED: None,
           STATE_DISABLED: None,
           STATE_MOUSE_HOVER: None
           }
        self._bCustomClickZone = False
        self._click_zone_offset = {'x': '50%','y': '50%'}
        self._click_zone_size = {'width': '100%','height': '100%'}
        self._custom_click_zone = None
        self._text_hAlign = cc.TEXTHALIGNMENT_LEFT
        self._text_vAlign = cc.TEXTVALIGNMENT_TOP
        self._state_changed_cb = None
        self._need_check_size = False
        return

    def _registerInnerEvent(self):
        super(CCButton, self)._registerInnerEvent()
        self.BindMethod('OnHoverEnter', self._sDefaultOnHoverEnter)
        self.BindMethod('OnHoverExit', self._sDefaultOnHoverExit)

    def _OnBegin(self, touch):
        ret = self.OnBegin(touch)
        if not (ret and self._bCustomState):
            if self._curState != STATE_DISABLED:
                state = STATE_SELECTED if 1 else STATE_DISABLED
                if self.__orgClickState is None:
                    self.__orgClickState = self._curState
                self._updateCurState(state, True, True)
        return ret

    def _OnEnd(self, touch):
        if self._bCustomState or self.__orgClickState is not None:
            state = self.__orgClickState if 1 else STATE_NORMAL
            self._updateCurState(state, True, False)
            self.__orgClickState = None
        return self.OnEnd(touch)

    def _OnCancel(self, touch):
        if self._bCustomState or self.__orgClickState is not None:
            state = self.__orgClickState if 1 else STATE_NORMAL
            self._updateCurState(state, True, False)
            self.__orgClickState = None
        return self.OnCancel(touch)

    @staticmethod
    def _sDefaultOnHoverEnter(self):
        dst_state = STATE_MOUSE_HOVER
        if self._curState == STATE_NORMAL:
            self._updateCurState(dst_state)
        if self.__orgClickState is not None:
            self.__orgClickState = dst_state
        return

    def DefaultOnHoverEnter(self):
        self._sDefaultOnHoverEnter(self)

    @staticmethod
    def _sDefaultOnHoverExit(self):
        dst_state = STATE_NORMAL
        if self._curState == STATE_MOUSE_HOVER:
            self._updateCurState(dst_state)
        if self.__orgClickState is not None:
            self.__orgClickState = dst_state
        return

    def DefaultOnHoverExit(self):
        self._sDefaultOnHoverExit(self)

    def SetContentSize(self, sw, sh):
        if self._bUse9Spt or len(self._display_spts) == 0:
            size = super(CCButton, self).SetContentSize(sw, sh)
            self.UpdateSpriteSize(size)
        elif global_data.enable_ui_add_image_async and STATE_NORMAL not in self._display_spts:
            size = super(CCButton, self).SetContentSize(sw, sh)
        else:
            spt = self._display_spts[STATE_NORMAL]
            if spt:
                size = spt.getContentSize()
                self.setContentSize(size)
            else:
                size = super(CCButton, self).SetContentSize(sw, sh)
        if self._text is not None:
            self._text.SetPosition(self._text_offset['x'], self._text_offset['y'])
        return size

    def UpdateSpriteSize(self, size):
        if self._bUse9Spt or len(self._display_spts) == 0:
            for spt in six.itervalues(self._display_spts):
                if spt is not None and getattr(spt, 'setPreferredSize', None):
                    spt.setPreferredSize(size)

        return

    def SetEnableText(self, bEnable):
        self._bEnableText = bEnable

    def IsEnableText(self):
        return self._bEnableText

    def SetZoomScale(self, scale):
        self._zoomScale = scale

    def SetText(self, text, font_size=None, color1=None, color2=None, color3=None, font_name=None, dimensions=None, skew=None):
        if self._bEnableText is False:
            return
        else:
            if self._text is None:
                if not dimensions:
                    dimensions = CCSizeZero
                self._text = CCUIText.Create(text, font_size or 25, dimensions, self._text_hAlign, self._text_vAlign, font_name)
                self._text.setAnchorPoint(ccp(0.5, 0.5))
                self.AddChild(None, self._text, 1)
            else:
                self._text.SetString(text)
                if skew:
                    self._text.setSkewX(skew['x'])
                    self._text.setSkewY(skew['y'])
                if font_size:
                    self._text.SetFontSize(font_size)
                if dimensions:
                    self._text.setTextAreaSize(dimensions)
                if font_name:
                    self._text.SetFontName(font_name)
            if color1:
                self.SetTextColor(color1, color2, color3)
            return

    def SetTextColor(self, color1=None, color2=None, color3=None):
        if color1 is not None:
            self._display_textsColors[STATE_NORMAL] = ccc3FromHex(get_color_val(color1))
            self._display_textsColors[STATE_SELECTED] = ccc3FromHex(get_color_val(color2))
            self._display_textsColors[STATE_DISABLED] = ccc3FromHex(get_color_val(color3))
        else:
            self._display_textsColors[STATE_NORMAL] = ccc3FromHex(get_color_val('#SW'))
            self._display_textsColors[STATE_SELECTED] = ccc3FromHex(get_color_val('#SW'))
            self._display_textsColors[STATE_DISABLED] = ccc3FromHex(get_color_val('#SW'))
        return

    def GetTextColor(self):
        return (
         self._display_textsColors[STATE_NORMAL], self._display_textsColors[STATE_SELECTED], self._display_textsColors[STATE_DISABLED])

    def SetTextShadows(self, enable, color1=None, color2=None, color3=None, opacity1=255, opacity2=255, opacity3=255, offset=CCSize(2, -2)):
        self._bTextShadow = enable
        self._shadowOffset = offset
        if enable:
            self._display_textsShadows[STATE_NORMAL] = ccc4FromHex(get_color_val(color1), opacity1)
            self._display_textsShadows[STATE_SELECTED] = ccc4FromHex(get_color_val(color2), opacity2)
            self._display_textsShadows[STATE_DISABLED] = ccc4FromHex(get_color_val(color3), opacity3)
        else:
            self._display_textsShadows[STATE_NORMAL] = ccc4FromHex(get_color_val('#SK'), opacity1)
            self._display_textsShadows[STATE_SELECTED] = ccc4FromHex(get_color_val('#SK'), opacity2)
            self._display_textsShadows[STATE_DISABLED] = ccc4FromHex(get_color_val('#SK'), opacity3)

    def SetTextFontSizes(self, enable, fontSize, fontSize1, fontSize2):
        self._bEnableStateFontSize = enable
        self._display_textsFontSize[STATE_NORMAL] = fontSize
        self._display_textsFontSize[STATE_SELECTED] = fontSize1
        self._display_textsFontSize[STATE_DISABLED] = fontSize2

    def GetTextFontSizes(self):
        return (
         self._bEnableStateFontSize,
         self._display_textsFontSize.get(STATE_NORMAL, 0), self._display_textsFontSize.get(STATE_SELECTED, 0), self._display_textsFontSize.get(STATE_DISABLED, 0))

    def SetTextOffset(self, text_offset):
        self._text_offset = text_offset
        if self._text is not None:
            self._text.SetPosition(self._text_offset['x'], self._text_offset['y'])
        return

    def SetTextSkew(self, skew):
        self._text_skew = skew

    def SetFrames(self, plist, paths, b9Spt=None, rect=None, force_sync=False):
        self._plist = plist
        self._paths = paths
        if b9Spt is None:
            b9Spt = self._bUse9Spt
        self._bUse9Spt = b9Spt
        if rect is None:
            rect = self._9rect
        self._9rect = rect

        def _cb(frame, path, state):
            if not self.get():
                return
            else:
                spt = None
                if frame is not None:
                    if b9Spt:
                        size_w, size_h = self.GetContentSize()
                        spt = CCScale9Sprite.CreateWithSpriteFrame(frame, rect)
                        spt.SetContentSize(size_w, size_h)
                    else:
                        spt = CCSprite.CreateWithSpriteFrame(frame)
                    global_data.uisystem.RecordSpriteUsage(plist, path, self)
                    spt.setAnchorPoint(ccp(0, 0))
                    self.ClearFrame(state)
                    self.AddChild(None, spt, -1)
                    self._display_spts[state] = spt
                else:
                    self.ClearFrame(state)
                    self._display_spts[state] = None
                if state == STATE_NORMAL and spt and self._need_check_size:
                    old_size = self.getContentSize()
                    new_size = spt.getContentSize()
                    if old_size.width <= 0 or old_size.height <= 0 or old_size.width != new_size.width or old_size.height != new_size.height:
                        self.SetContentSize(new_size.width, new_size.height)
                        self.ChildResizeAndPosition()
                        if self._custom_click_zone:
                            self._custom_click_zone.SetPosition(self._click_zone_offset['x'], self._click_zone_offset['y'])
                            self._custom_click_zone.SetContentSize(self._click_zone_size['width'], self._click_zone_size['height'])
                        if self._text is not None:
                            self._text.SetPosition(self._text_offset['x'], self._text_offset['y'])
                    self._need_check_size = False
                if global_data.enable_ui_add_image_async:
                    self._updateCurState()
                return

        for state, path in enumerate(paths):
            if self._cur_paths[state] == path:
                continue
            if path:
                if global_data.enable_ui_add_image_async and not force_sync and not global_data.temporary_force_image_sync:

                    def _cb_async(frame, path, _state):
                        if not self._paths or _state >= len(self._paths) or path != self._paths[_state]:
                            return
                        _cb(frame, path, _state)

                    global_data.uisystem.GetSpriteFrameByPathAsync(path, plist, lambda _frame, _path=path, _state=state: _cb_async(_frame, _path, _state))
                else:
                    frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
                    _cb(frame, path, state)
            else:
                self.ClearFrame(state)
                self._display_spts[state] = None
            self._cur_paths[state] = path

        self._updateCurState()
        return

    def SetNeedCheckSize(self, val):
        self._need_check_size = val

    def GetFramePaths(self):
        return self._paths

    def SetMouseHoverFrame(self, path):
        if not global_data.feature_mgr.is_support_pc_mouse_hover():
            return
        paths = self._paths[:]
        if len(paths) == STATE_MOUSE_HOVER:
            paths.append(path)
        elif len(paths) > STATE_MOUSE_HOVER:
            paths[STATE_MOUSE_HOVER] = path
        else:
            return
        self.SetFrames(self._plist, paths, self._bUse9Spt, self._9rect)

    def ClearFrame(self, state):
        if state in self._display_spts and self._display_spts[state]:
            self._display_spts[state].Destroy()
            self._display_spts[state] = None
            self._cur_paths[state] = None
        return

    def ClearAllFrames(self):
        for state in six_ex.keys(self._display_spts):
            self.ClearFrame(state)

    def GetText(self):
        if self._text is None:
            return ''
        else:
            return self._text.getString()
            return

    def SetEnable(self, enable):
        if enable == self._enable:
            return
        self._enable = enable
        self.SetEnableTouch(enable)
        self.SetShowEnable(enable)

    def IsEnable(self):
        return self._enable

    def _playBeginAnim(self):
        self.stopActionByTag(BUTTON_CLICK_ANIM_TAG)
        start_time = time.time()
        anim_duration = 0.099
        if self.__oldScale is None:
            self.__oldScale = (
             self._obj.getScaleX(), self._obj.getScaleY())

        def zoom():
            passed_time = time.time() - start_time
            if passed_time >= anim_duration:
                self.stopActionByTag(BUTTON_CLICK_ANIM_TAG)
                self._obj.setScaleX(self.__oldScale[0] * 0.97)
                self._obj.setScaleY(self.__oldScale[1] * 0.97)
            else:
                scale = 1.0 - passed_time / anim_duration * 0.03
                self._obj.setScaleX(self.__oldScale[0] * scale)
                self._obj.setScaleY(self.__oldScale[1] * scale)

        act = self.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(zoom),
         cc.DelayTime.create(0.03)])))
        act.setTag(BUTTON_CLICK_ANIM_TAG)
        return

    def _playEndAnim(self):
        self.stopActionByTag(BUTTON_CLICK_ANIM_TAG)
        start_time = time.time()
        zoom_up_duration = 0.066
        zoom_down_duration = 0.066
        zoom_duration = 0.132

        def zoom():
            passed_time = time.time() - start_time
            if passed_time <= zoom_up_duration:
                scale = 0.97 + passed_time / zoom_up_duration * 0.05
                self._obj.setScaleX(self.__oldScale[0] * scale)
                self._obj.setScaleY(self.__oldScale[1] * scale)
            elif zoom_up_duration < passed_time < zoom_duration:
                scale = 1.02 - (zoom_duration - passed_time) / zoom_down_duration * 0.02
                self._obj.setScaleX(self.__oldScale[0] * scale)
                self._obj.setScaleY(self.__oldScale[1] * scale)
            else:
                self.stopActionByTag(BUTTON_CLICK_ANIM_TAG)
                self._obj.setScaleX(self.__oldScale[0])
                self._obj.setScaleY(self.__oldScale[1])
                self.__oldScale = None
            return

        act = self.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(zoom),
         cc.DelayTime.create(0.03)])))
        act.setTag(BUTTON_CLICK_ANIM_TAG)

    def set_state_changed_cb(self, cb):
        self._state_changed_cb = cb

    def _updateCurState(self, setState=None, need_scale=False, scale_state=False):
        if setState is not None:
            self._curState = setState
        if hasattr(self._obj, 'getIgnorePause'):
            need_scale = not self.getIgnorePause()
        if global_data.is_key_mocking_ui_event:
            need_scale = False
        curState = self._curState
        if curState != STATE_MOUSE_HOVER:
            if self._text is not None:
                self._text._obj.setColor(self._display_textsColors[curState])
                if self._bTextShadow:
                    self._text._obj.enableShadow(self._display_textsShadows[curState], self._shadowOffset, 0)
                if self._bEnableStateFontSize:
                    self._text.SetFontSize(self._display_textsFontSize[curState])
            if self._display_opacities:
                self._obj.setOpacity(self._display_opacities[curState])
        for state, spt in six.iteritems(self._display_spts):
            if spt is not None:
                spt._obj.setVisible(state == curState)

        if need_scale:
            if scale_state:
                if self.__oldScale is None:
                    if type(self._zoomScale) == float:
                        if abs(self._zoomScale - 1.0) >= 0.01:
                            self._playBeginAnim()
                    elif self._zoomScale:
                        self._playBeginAnim()
            elif self.__oldScale is not None:
                if type(self._zoomScale) == float:
                    if abs(self._zoomScale - 1.0) >= 0.01:
                        self._playEndAnim()
                elif self._zoomScale:
                    self._playEndAnim()
        if callable(self._state_changed_cb):
            self._state_changed_cb(curState)
        return

    def GetSelect(self):
        return self._curState == STATE_SELECTED

    def SetSelect(self, sel):
        self._updateCurState(STATE_SELECTED if sel else STATE_NORMAL)
        self._updateRecordClickState()

    def _updateRecordClickState(self):
        if self.__orgClickState is not None:
            self.__orgClickState = self._curState
        return

    def SetShowEnable(self, enable):
        if enable:
            if self._in_hover:
                dst_state = STATE_MOUSE_HOVER
            else:
                dst_state = STATE_NORMAL
        else:
            dst_state = STATE_DISABLED
        self._updateCurState(dst_state)
        self._updateRecordClickState()

    def IsEnable(self):
        return self._curState != STATE_DISABLED

    def EnableCustomState(self, enable):
        self._bCustomState = enable

    def IsCustomState(self):
        return self._bCustomState

    def EnableSelectOpacity(self, is_enable, normal_opacity=None, select_opacity=None, disable_opacity=None):
        if is_enable:
            self.SetEnableCascadeOpacityRecursion(True)
            if select_opacity:
                self._display_opacities[STATE_NORMAL] = normal_opacity
                self._display_opacities[STATE_SELECTED] = select_opacity
                self._display_opacities[STATE_DISABLED] = disable_opacity
            else:
                self._display_opacities[STATE_NORMAL] = 255
                self._display_opacities[STATE_SELECTED] = 255
                self._display_opacities[STATE_DISABLED] = 255
        else:
            self._display_opacities = {}

    def SetClickZoneOffset(self, offset):
        self._click_zone_offset = offset

    def SetClickZoneSize(self, size):
        self._click_zone_size = size

    def SetEnableCustomClickZone(self, bEnable):
        self._bCustomClickZone = bEnable
        self.setCustomClickZoneEnable(bEnable)

    def UpdateCustomClickZone(self):
        if not self._bCustomClickZone:
            return
        else:
            if self._custom_click_zone is None:
                self._custom_click_zone = CCNode.Create()
                self.AddChild(None, self._custom_click_zone, 1)
                self._custom_click_zone.setAnchorPoint(ccp(0.5, 0.5))
                self._custom_click_zone.SetPosition(self._click_zone_offset['x'], self._click_zone_offset['y'])
                self._custom_click_zone.SetContentSize(self._click_zone_size['width'], self._click_zone_size['height'])
                self.setCustomClickZoneNode(self._custom_click_zone.get())
            return

    def _SetTextAlignment(self, hAlign, vAlign):
        self._text_hAlign = hAlign
        self._text_vAlign = vAlign

    def IsPointIn(self, pt):
        if self._bCustomClickZone and self._custom_click_zone:
            return (self._clip_object is None or self._clip_object.hitTest(pt)) and self._custom_click_zone.hitTest(pt)
        else:
            return super(CCButton, self).IsPointIn(pt)
            return None


class CCButtonCreator(CCNodeCreator):
    COM_NAME = 'CCButton'
    DYNAMIC_ARGS = {'is9sprite': '9sprite'
       }
    DYNAMIC_ARGS.update(CCNodeCreator.DYNAMIC_ARGS)
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      '9sprite', True),
     (
      'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
     ('plist', ''),
     ('frame1', 'gui/ui_res_2/default/img_useless.png'),
     ('frame2', 'gui/ui_res_2/default/img_useless.png'),
     ('frame3', ''),
     (
      'enableText', True),
     ('text', ''),
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     (
      'bEnableStateFontSize', False),
     ('fontSize', 24),
     ('fontSize1', 24),
     ('fontSize2', 24),
     ('textColor1', '#SW'),
     ('textColor2', '#SW'),
     ('textColor3', '#SW'),
     (
      'textOffset', {'x': '50%','y': '50%'}),
     (
      'textSkew', {'x': 0,'y': 0}),
     (
      'isEnabled', True),
     ('zoomScale', 0.98),
     (
      'swallow', True),
     (
      'noEventAfterMove', False),
     ('move_dist', '10w'),
     (
      'customClickZone', False),
     (
      'clickZoneOffset', {'x': '50%','y': '50%'}),
     (
      'clickZoneSize', {'width': '100%','height': '100%'}),
     (
      'dimensions', {'width': 0,'height': 0}),
     (
      'enableTextShadow', False),
     ('textShadow1', '#SK'),
     ('textShadow2', '#SK'),
     ('textShadow3', '#SK'),
     ('shadowOpacity', 255),
     (
      'shadowOffset', {'width': 2,'height': -2}),
     (
      'hAlign', cc.TEXTHALIGNMENT_CENTER),
     (
      'vAlign', cc.TEXTVALIGNMENT_CENTER)]
    ATTR_INIT = [
     'name', 'pos', '9sprite',
     'size', 'text',
     'child_list']

    @staticmethod
    def create(parent, root, swallow, noEventAfterMove, move_dist):
        obj = CCButton.Create()
        obj.SetSwallowTouch(swallow)
        obj.SetNoEventAfterMove(noEventAfterMove, move_dist)
        return obj

    @staticmethod
    def check_config--- This code section failed: ---

 616       0  LOAD_CONST            1  '9sprite'
           3  LOAD_FAST             0  'conf'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    23  'to 23'

 617      12  POP_JUMP_IF_FALSE     1  'to 1'
          15  BINARY_SUBSCR    
          16  BINARY_SUBSCR    
          17  BINARY_SUBSCR    
          18  BINARY_SUBSCR    
          19  STORE_SUBSCR     
          20  JUMP_FORWARD          0  'to 23'
        23_0  COME_FROM                '20'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 12

    @staticmethod
    def set_attr_group_9sprite(obj, parent, root, is9sprite, capInsets, plist, frame1, frame2, frame3, customClickZone, clickZoneOffset, clickZoneSize):
        capInsets = CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height'])
        obj.SetClickZoneOffset(clickZoneOffset)
        obj.SetClickZoneSize(clickZoneSize)
        obj.SetEnableCustomClickZone(customClickZone)
        if frame1:
            obj.SetNeedCheckSize(True)
        obj.SetFrames(plist, [frame1, frame2, frame3], is9sprite, capInsets)

    @staticmethod
    def set_attr_group_text(obj, parent, root, enableText, text, fontName, fontSize, textColor1, textColor2, textColor3, textOffset, textSkew, isEnabled, zoomScale, dimensions, enableTextShadow, textShadow1, textShadow2, textShadow3, shadowOpacity, shadowOffset, bEnableStateFontSize, fontSize1, fontSize2, hAlign, vAlign):
        from common.utils.ui_utils import calc_pos
        from common.utils.cocos_utils import CCSize
        obj._SetTextAlignment(hAlign, vAlign)
        obj.SetEnableText(enableText)
        obj.SetTextOffset(textOffset)
        obj.SetTextSkew(textSkew)
        obj.SetTextColor(textColor1, textColor2, textColor3)
        obj.SetTextShadows(enableTextShadow, textShadow1, textShadow2, textShadow3, shadowOpacity, shadowOpacity, shadowOpacity, CCSize(shadowOffset['width'], shadowOffset['height']))
        obj.SetTextFontSizes(bEnableStateFontSize, fontSize, fontSize1, fontSize2)
        width, height = obj.GetContentSize()
        w = calc_pos(dimensions['width'], width, obj.getScaleX())
        h = calc_pos(dimensions['height'], height, obj.getScaleY())
        obj.SetText(text, fontSize, font_name=fontName, dimensions=CCSize(w, h))
        if obj._text is not None:
            obj._text.SetPosition(textOffset['x'], textOffset['y'])
            obj._text.setSkewX(textSkew['x'])
            obj._text.setSkewY(textSkew['y'])
        obj.SetEnable(isEnabled)
        obj.SetZoomScale(zoomScale)
        obj._updateCurState()
        return

    @staticmethod
    def set_attr_group_size(obj, parent, root, size):
        obj.SetContentSize(size['width'], size['height'])
        obj.UpdateCustomClickZone()