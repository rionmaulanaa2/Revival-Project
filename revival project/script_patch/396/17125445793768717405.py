# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCUILayout.py
from __future__ import absolute_import
import six
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect
from common.uisys.color_table import get_color_val
from .CCUIWidget import CCUIWidget

@ProxyClass(ccui.Layout)
class CCUILayout(CCUIWidget):

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        color_val = ccc3FromHex(color)
        self.setColor(color_val)
        bgColorType = self.getBackGroundColorType()
        if bgColorType == ccui.LAYOUT_BACKGROUNDCOLORTYPE_SOLID:
            self.setBackGroundColor(color_val)
        elif bgColorType == ccui.LAYOUT_BACKGROUNDCOLORTYPE_GRADIENT:
            pass

    def _refreshItemPos(self, is_cal_scale=False):
        self.forceDoLayout()
        if is_cal_scale:
            pass


class CCUILayoutCreator(CCNodeCreator):
    COM_NAME = 'CCUILayout'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'spriteFrame', {'plist': '','path': ''}),
     (
      'scale9Enabled', False),
     (
      'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
     ('bgColorType', 0),
     ('bgColor', '#SW'),
     ('bgOpacity', 255),
     ('startColor', '#SR'),
     ('endColor', '#SG'),
     (
      'vector', {'x': 1,'y': 0}),
     (
      'clippingEnable', True),
     (
      'touchEnabled', False)]

    @staticmethod
    def create(parent, root, spriteFrame, capInsets, bgColor, bgOpacity, scale9Enabled, clippingEnable, vector, bgColorType, startColor, endColor):
        layout = CCUILayout.Create()
        spriteFramePath = spriteFrame['path']
        spriteFramePlist = spriteFrame['plist']
        if spriteFramePath:
            if False:

                def _cb(frame, obj):
                    if obj and obj.get() and frame:
                        obj.setSpriteFrame(frame)

                global_data.uisystem.GetSpriteFrameByPathAsync(spriteFramePath, spriteFramePlist, lambda _frame, _obj=layout: _cb(_frame, _obj))
            else:
                spriteFrameObj = global_data.uisystem.GetSpriteFrameByPath(spriteFramePath, spriteFramePlist)
                global_data.uisystem.RecordSpriteUsage(spriteFramePlist, spriteFramePath, spriteFrameObj)
                if spriteFrameObj:
                    if spriteFramePlist == '':
                        layout.setBackGroundImage(spriteFramePath, 0)
                    else:
                        layout.setBackGroundImage(spriteFramePath, 1)
                    layout.setBackGroundImageScale9Enabled(scale9Enabled)
                    if scale9Enabled:
                        capInsets = CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height'])
                        layout.setBackGroundImageCapInsets(capInsets)
        layout.setBackGroundColor(ccc3FromHex(get_color_val(bgColor)))
        layout.setBackGroundColorOpacity(bgOpacity)
        layout.setBackGroundColorVector(ccp(vector['x'], vector['y']))
        layout.setBackGroundColorType(bgColorType)
        layout.setBackGroundColor(ccc3FromHex(get_color_val(startColor)), ccc3FromHex(get_color_val(endColor)))
        layout.setClippingEnabled(clippingEnable)
        layout.setClippingType(1)
        return layout