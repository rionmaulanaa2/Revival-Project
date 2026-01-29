# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCEditBoxExt.py
from __future__ import absolute_import
import ccui
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCUIWidget import CCUIWidget
from common.uisys.font_utils import GetMultiLangFontName, get_force_font_trans
from common.utils.cocos_utils import ccc4FromHex
from common.uisys.color_table import get_color_val
from logic.gcommon.common_utils.local_text import get_lang_shrink_font_size

@ProxyClass(ccui.TextField)
class CCEditBoxExt(CCUIWidget):

    @classmethod
    def Create(cls, *args):
        return cls(cls.create(*args))

    def _registerInnerEvent(self):
        self.UnBindMethod('OnEditBegan')
        self.UnBindMethod('OnEditEnded')
        self.UnBindMethod('OnEditChanged')
        self.UnBindMethod('OnEditReturn')

        def func(edit, event):
            text = self.getString()
            if event == 0:
                self.OnEditBegan(text)
            elif event == 2 or event == 3:
                self.OnEditChanged(text)
            elif event == 1:
                self.OnEditReturn(text)

        self.addEventListener(func)

    def SetContentSize(self, sw, sh):
        sz = super(CCEditBoxExt, self).SetContentSize(sw, sh)
        self.setTouchSize(sz)
        self.setTouchAreaEnabled(True)
        return sz

    def SetText(self, text):
        if isinstance(text, int):
            text = get_text_local_content(text)
        self.setString(text)
        return text

    def InsertText(self, text):
        if hasattr(ccui.TextField, 'insertText'):
            self.insertText(text)

    def SetPlaceHolder(self, text):
        if isinstance(text, int):
            text = get_text_local_content(text)
        self.setPlaceHolder(text)

    def SetTextColor(self, col):
        self._text_col = get_color_val(col)
        self.setTextColor(self._text_col)

    def GetTextColor(self):
        return self._text_col


class CCEditBoxExtCreator(CCNodeCreator):
    COM_NAME = 'CCEditBoxExt'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('text', ''),
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     ('colText', '#SW'),
     ('placeHolder', ''),
     ('colPlaceHolder', '#SW'),
     ('fontSize', 24),
     ('placeHolderFontSize', 24),
     ('nMaxLength', -1),
     (
      'hAlign', cc.TEXTHALIGNMENT_LEFT),
     (
      'vAlign', cc.TEXTVALIGNMENT_CENTER)]

    @staticmethod
    def create(parent, root, text, fontName, colText, placeHolder, colPlaceHolder, nMaxLength, fontSize, hAlign, vAlign):
        placeHolder = get_text_local_content(placeHolder) if isinstance(placeHolder, int) else placeHolder
        if get_force_font_trans():
            fontName = GetMultiLangFontName(fontName)
        obj = CCEditBoxExt.Create(placeHolder, fontName, get_lang_shrink_font_size(fontSize))
        col = ccc4FromHex(get_color_val(colText))
        obj.SetTextColor(col)
        obj.setPlaceHolderColor(ccc4FromHex(get_color_val(colPlaceHolder)))
        obj.setMaxLength(nMaxLength)
        obj.SetText(text)
        obj.setTextHorizontalAlignment(hAlign)
        obj.setTextVerticalAlignment(vAlign)
        return obj