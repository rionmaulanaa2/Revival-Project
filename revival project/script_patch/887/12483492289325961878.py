# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLayerColor.py
from __future__ import absolute_import
import six
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCLayer import CCLayer, CCLayerCreator
from common.utils.cocos_utils import ccc4, ccc3FromHex
from common.uisys.color_table import get_color_val

@ProxyClass(cc.LayerColor)
class CCLayerColor(CCLayer):

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        self.setColor(ccc3FromHex(color))


class CCLayerColorCreator(CCLayerCreator):
    COM_NAME = 'CCLayerColor'
    ATTR_DEFINE = CCLayerCreator.ATTR_DEFINE + [
     ('color', '#SR')]

    @staticmethod
    def create(parent, root, color, opacity):
        color = get_color_val(color)
        return CCLayerColor.Create(ccc4(color >> 16 & 255, color >> 8 & 255, color & 255, opacity))