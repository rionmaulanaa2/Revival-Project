# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLabelAtlas.py
from __future__ import absolute_import
import six
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.cocos_utils import ccc3FromHex
from common.uisys.color_table import get_color_val

@ProxyClass(ccui.TextAtlas)
class CCLabelAtlas(CCNode):

    @classmethod
    def CreateWithCharMap(cls, text, fntFileOrTexPath, charWidth=None, charHeight=None, startChar=None):
        if charWidth is None:
            return cls(cls.create(text, fntFileOrTexPath))
        else:
            return cls(cls.create(text, fntFileOrTexPath, charWidth, charHeight, startChar))
            return

    def SetContentSize(self, w, h):
        return self.getContentSize()

    def SetString(self, s, args=None):
        if isinstance(s, int):
            self._text_id = s
            s = get_text_by_id(s, args)
        self._text = s
        if s == self._obj.getString():
            return s
        self._obj.setString(s)
        return s

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color_val = get_color_val(color)
        else:
            color_val = color
        self.getVirtualRenderer().setColor(ccc3FromHex(color_val))


class CCLabelAtlasCreator(CCNodeCreator):
    COM_NAME = 'CCLabelAtlas'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('fntFile', None),
     ('text', ''),
     ('color', '#SW'),
     ('charWidth', 30),
     ('charHeight', 37),
     ('startChar', '0'),
     ('texturePath', 'gui/fonts/atlas_num.png')]

    @staticmethod
    def create(parent, root, fntFile, text, color, opacity, charWidth, charHeight, startChar, texturePath):
        if fntFile is not None:
            obj = CCLabelAtlas.CreateWithCharMap(text, fntFile)
        else:
            if not isinstance(startChar, int) and not texturePath.endswith('png'):
                startChar = ord(startChar)
            obj = CCLabelAtlas.CreateWithCharMap(text, texturePath, charWidth, charHeight, startChar)
            global_data.uisystem.RecordSpriteUsage('', texturePath, obj)
        obj.SetColor(color)
        obj.setOpacity(opacity)
        return obj