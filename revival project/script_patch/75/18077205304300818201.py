# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLabel.py
from __future__ import absolute_import
import six
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode
from common.utils.cocos_utils import CCSizeZero, CCPointZero
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.cocos_utils import ccc3FromHex
from common.uisys.color_table import get_color_val, format_color_replace
from common.uisys.font_utils import GetMultiLangFontName
from logic.gcommon.common_utils.local_text import get_cur_lang_shrink_setting, get_enable_def_linebreak

@ProxyClass(cc.Label)
class CCLabel(CCNode):

    @classmethod
    def Create(cls, text='', fontSize=25, szDemensions=CCSizeZero, hAlign=cc.TEXTHALIGNMENT_LEFT, vAlign=cc.TEXTVALIGNMENT_TOP, fontName='gui/fonts/fzy4jw.ttf'):
        fontName = GetMultiLangFontName(fontName.lower())
        text_id = None
        if isinstance(text, int):
            text_id = text
            text = get_text_by_id(text_id)
        self = cls(cls.createWithTTF(text, fontName, fontSize, szDemensions, hAlign, vAlign))
        self._fontName = fontName
        self._text_id = text_id
        self._text = text
        self._text_args = None
        self._is_rich_mode = False
        self._nOutLineWidth = 0
        self.CheckAutoShrinkFont()
        return self

    @classmethod
    def CreateWithCharMap(cls, fntFileOrTexPath, charWidth=None, charHeight=None, startChar=None):
        if charWidth is None:
            return cls(cls.createWithCharMap(fntFileOrTexPath))
        else:
            return cls(cls.createWithCharMap(fntFileOrTexPath, charWidth, charHeight, startChar))
            return

    @classmethod
    def CreateWithBMFont(cls, fntFile, text, hAlignment=cc.TEXTHALIGNMENT_LEFT, maxLineWidth=0, imageOffset=CCPointZero):
        return cls(cls.createWithBMFont(fntFile, text, hAlignment, maxLineWidth, imageOffset))

    def SetContentSize(self, w, h):
        return self.getContentSize()

    def SetFontSize(self, fontSize):
        if self._fontName:
            self.setTTFConfig((self._fontName, int(fontSize), self._nOutLineWidth))

    def SetString(self, s, args=None):
        if isinstance(s, int):
            self._text_id = s
            s = get_text_by_id(s, args)
        self._text = s
        if s == self._obj.getString():
            return s
        if self._is_rich_mode:
            s = format_color_replace(s)
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
        self.setColor(ccc3FromHex(color_val))

    def RefreshString(self):
        if self._text_id != None:
            s = get_text_by_id(self._text_id, self._text_args)
            if s == self.getString():
                return s
            self.setString(s)
        return

    def EnableOutline(self, color, width):
        self._nOutLineWidth = width
        self._outLineColor = color
        self.enableOutline(color, width)

    def SetRichMode(self, rich_mode):
        self._is_rich_mode = rich_mode
        self.setRichMode(rich_mode)
        if rich_mode:
            new_s = format_color_replace(self._text)
            if self._text == new_s:
                return
            self.SetString(new_s)

    def CheckAutoShrinkFont(self):
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self.setEnableFontSizeAutoShrink(lang_shrink_setting.bEnableShrink, lang_shrink_setting.iMinFontSize)
        return lang_shrink_setting.bEnableShrink

    def csb_init(self):
        super(CCLabel, self).csb_init()
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self._minFontSize = lang_shrink_setting.iMinFontSize
        if not get_enable_def_linebreak():
            if self.getVirtualRenderer():
                self.getVirtualRenderer().setLineBreakWithoutSpace(True)
        self.CheckAutoShrinkFont()