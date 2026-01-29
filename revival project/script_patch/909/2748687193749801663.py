# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCFTLabelTTFAtlasWithFormat.py
from __future__ import absolute_import
import six
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import ccc3FromHex, ccc3
from common.utils.ui_utils import calc_pos
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.color_table import get_color_val, format_color_replace
from common.uisys.font_utils import GetMultiLangFontName

@ProxyClass(cc.CCFTLabelTTFAtlasWithFormat)
class CCFTLabelTTFAtlasWithFormat(CCNode):

    def __init__(self, node):
        super(CCFTLabelTTFAtlasWithFormat, self).__init__(node)
        self._text_id = None
        return

    @classmethod
    def Create(cls, text='', fontName=None, fontSize=24, fWidth=10, color=None, bScaleEmoteByHd=False, bEnableRewardIcon=False):
        if fontName is None:
            fontName = ''
        fontName = GetMultiLangFontName(fontName)
        if color is None:
            color = ccc3(255, 255, 255)
        return cls(cls.create(text, fontName, fontSize, fWidth, color, bScaleEmoteByHd, bEnableRewardIcon))

    def SetContentSize(self, sw, sh):
        pass

    def SetFontSize(self, fontSize):
        pass

    def SetString(self, s, *args):
        if isinstance(s, int):
            self._text_id = s
            s = get_text_by_id(s)
        if s == self._obj.getString():
            return s
        if len(args) > 0:
            self._obj.setString(format_color_replace(str(s) % args))
        else:
            self._obj.setString(format_color_replace(str(s)))

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        self.setColor(ccc3FromHex(color))

    def RawSetString(self, s, *args):
        if not isinstance(s, (str, six.text_type)):
            s = str(s)
        self.get().setString(s, *args)


class CCFTLabelTTFAtlasWithFormatCreator(CCNodeCreator):
    COM_NAME = 'CCFTLabelTTFAtlasWithFormat'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     ('fontSize', 24),
     ('width', 100),
     (
      'hAlign', cc.TEXTHALIGNMENT_LEFT),
     ('text', ''),
     ('color', '#SW')]

    @staticmethod
    def create(parent, root, fontName, fontSize, hAlign, text, color, opacity, width):
        parent_width, parent_height = parent.GetContentSize()
        num_width = calc_pos(width, parent_width)
        obj = CCFTLabelTTFAtlasWithFormat.Create('11111', fontName, fontSize, num_width, ccc3FromHex(get_color_val(color)), False, False)
        obj.SetColor(color)
        obj.SetString(text)
        obj.setHorizontalAlignment(hAlign)
        obj.setOpacity(opacity)
        return obj