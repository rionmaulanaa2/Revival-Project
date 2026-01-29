# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLabelBMFont.py
from __future__ import absolute_import
import six
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.cocos_utils import ccc3FromHex
from common.uisys.color_table import get_color_val

@ProxyClass(ccui.TextBMFont)
class CCLabelBMFont(CCNode):

    @classmethod
    def CreateWithBMFont(cls, text, fntFile):
        return cls(cls.create(text, fntFile))

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

    @staticmethod
    def GetMultiLangString(text):
        if isinstance(text, int):
            text_id = text
            text = get_text_by_id(text_id)
        return text

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color_val = get_color_val(color)
        else:
            color_val = color
        self.getVirtualRenderer().setColor(ccc3FromHex(color_val))

    def setBMFontFilePath(self, fntFile):
        self.setFntFile(fntFile)


class CCLabelBMFontCreator(CCNodeCreator):
    COM_NAME = 'CCLabelBMFont'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('texturePath', 'gui/fonts/yishuzi.fnt'),
     ('text', ''),
     ('color', '#SW')]

    @staticmethod
    def create(parent, root, texturePath, text, color, opacity):
        obj = CCLabelBMFont.CreateWithBMFont(CCLabelBMFont.GetMultiLangString(text), texturePath)
        obj.SetColor(color)
        obj.setOpacity(opacity)
        return obj