# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCUIButton.py
from __future__ import absolute_import
import ccui
from .CCUIWidget import CCUIWidget
from .CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED, STATE_MOUSE_HOVER
import cc
import time
from common.uisys.ui_proxy import ProxyClass
from common.utils.cocos_utils import ccc3FromHex, ccc4FromHex, CCSize, ccc4
from common.uisys.color_table import get_color_val
from common.const.cocos_constant import BUTTON_CLICK_ANIM_TAG
from common.uisys.ui_proxy import trans2ProxyObj

@ProxyClass(ccui.Button)
class CCUIButton(CCUIWidget):

    def __init__(self, node):
        super(CCUIButton, self).__init__(node)
        self._curState = STATE_NORMAL
        self._zoomScale = True
        self.__oldScale = None
        self._bCustomState = False
        self.__orgClickState = None
        self._display_opacities = {}
        self._cur_paths = {STATE_MOUSE_HOVER: None
           }
        self._state_changed_cb = None
        self._text = trans2ProxyObj(node.getTitleRenderer())
        self._bEnableText = True
        self._bUse9Spt = self.isScale9Enabled()
        self._text.CheckAutoShrinkFont()
        self._text_offset = None
        self._click_zone_offset = {'x': '50%','y': '50%'}
        self._click_zone_size = {'width': '100%','height': '100%'}
        return

    def GetStatus(self):
        if self.isBright():
            if self.isHighlighted():
                return STATE_SELECTED
            else:
                return STATE_NORMAL

        return STATE_DISABLED

    def _registerInnerEvent(self):
        super(CCUIButton, self)._registerInnerEvent()
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
        if self._bUse9Spt:
            size = super(CCUIButton, self).SetContentSize(sw, sh)
            self.UpdateSpriteSize(size)
        else:
            spt = self.getButtonNormalRenderer()
            if spt and spt.getSprite():
                size = spt.getContentSize()
                self.setContentSize(size)
            else:
                size = super(CCUIButton, self).SetContentSize(sw, sh)
        if self._text is not None:
            if not self._text_offset:
                from common.uisys.cocomate import do_cocomate_layout
                do_cocomate_layout(self._text.get(), True, False)
            else:
                self._text.SetPosition(self._text_offset['x'], self._text_offset['y'])
        return size

    def UpdateSpriteSize(self, size):
        self.setContentSize(size)

    def IsEnableText(self):
        return self._bEnableText

    def SetZoomScale(self, scale):
        self._zoomScale = scale

    def SetText(self, text, font_size=None, color1=None, color2=None, color3=None, font_name=None, dimensions=None, skew=None):
        if self._bEnableText is False:
            return
        else:
            if self._text is None:
                return
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
            self.setTitleNormalTextColor(ccc3FromHex(get_color_val(color1)))
            self.setTitlePressedTextColor(ccc3FromHex(get_color_val(color2)))
            self.setTitleDisableTextColor(ccc3FromHex(get_color_val(color3)))
        else:
            self.setTitleNormalTextColor(ccc3FromHex(get_color_val('#SW')))
            self.setTitlePressedTextColor(ccc3FromHex(get_color_val('#SW')))
            self.setTitleDisableTextColor(ccc3FromHex(get_color_val('#SW')))
        return

    def SetTextShadows(self, enable, color1=None, color2=None, color3=None, opacity=255, offset=CCSize(2, -2)):
        self._shadowOffset = offset
        if enable:
            shadowColor = self._text.getShaodwColor()
            shadowOpacity = self._text.getShadowOpacity() * 255
            self._text.enableShadow(True, ccc4(shadowColor.r, shadowColor.g, shadowColor.b, shadowOpacity), offset)
            self.setTitleNormalShadowColor(ccc4FromHex(get_color_val(color1), opacity))
            self.setTitlePressedShadowColor(ccc4FromHex(get_color_val(color2), opacity))
            self.setTitleDisableShadowColor(ccc4FromHex(get_color_val(color3), opacity))
        else:
            self._text.enableShadow(False, ccc4FromHex(get_color_val('#SK'), opacity), self._text.getShadowOffset())

    def SetTextFontSizes(self, enable, fontSize, fontSize1, fontSize2):
        self.setEnableStateFontSize(enable)
        self.setTitleNormalFontSize(fontSize)
        self.setTitlePressedFontSize(fontSize1)
        self.setTitleDisableFontSize(fontSize2)

    def GetTextFontSizes(self):
        return (
         self.getEnableStateFontSize(),
         self.getTitleNormalFontSize(), self.getTitlePressedFontSize(), self.getTitleDisableFontSize())

    def SetTextOffset(self, text_offset):
        self._text_offset = text_offset
        if self._text is not None:
            self._text.SetPosition(self._text_offset['x'], self._text_offset['y'])
        return

    def SetTextSkew(self, skew):
        pass

    def SetFrames(self, plist, paths, b9Spt=None, rect=None):
        self._plist = plist
        self._paths = paths
        if b9Spt is None:
            b9Spt = self._bUse9Spt
        self._bUse9Spt = b9Spt
        if rect is None:
            rect = self._9rect
        self._9rect = rect
        funcs = [self.loadTextureNormal, self.loadTexturePressed, self.loadTextureDisabled]
        for state, path in enumerate(paths):
            if path:
                path, plist = global_data.uisystem.GetSpritePathAndPlist(path, plist)
                funcs[state](path, ccui.WIDGET_TEXTURERESTYPE_PLIST if plist else ccui.WIDGET_TEXTURERESTYPE_LOCAL)
            else:
                self.ClearFrame(state)

        self.setScale9Enabled(b9Spt)
        self.setCapInsets(rect)
        self._updateCurState()
        return

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
        funcs = [
         self.clearTextureNormal, self.clearTexturePressed, self.clearTextureDisabled]
        if state < len(funcs):
            funcs[state]()

    def ClearAllFrames(self):
        self.clearTextureNormal()
        self.clearTexturePressed()
        self.clearTextureDisabled()

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
            if self._display_opacities:
                self._obj.setOpacity(self._display_opacities[curState])
        if curState == STATE_SELECTED:
            if not self.isBright():
                self.setBright(True)
            self.setHighlighted(True)
        elif curState == STATE_NORMAL:
            if not self.isBright():
                self.setBright(True)
            self.setHighlighted(False)
        elif curState == STATE_DISABLED:
            if self.isBright():
                self.setBright(False)
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

    def SetClickZoneSize(self, size):
        self._click_zone_size = size

    def UpdateCustomClickZone(self):
        if not self.getCustomClickZoneEnable():
            return
        else:
            if self.getCustomClickZoneNode() is None:
                self.createCustomClickZoneNode()
                self._custom_click_zone = trans2ProxyObj(self.getCustomClickZoneNode())
                self._custom_click_zone.SetPosition(self._click_zone_offset['x'], self._click_zone_offset['y'])
                self._custom_click_zone.SetContentSize(self._click_zone_size['width'], self._click_zone_size['height'])
            return

    def SetEnableCustomClickZone(self, bEnable):
        self.setCustomClickZoneEnable(bEnable)

    def IsPointIn(self, pt):
        return self.hitTestEx(pt)