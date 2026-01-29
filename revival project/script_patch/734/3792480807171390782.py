# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLayerGradient.py
from __future__ import absolute_import
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCLayer import CCLayer, CCLayerCreator
from common.utils.cocos_utils import ccc4, ccp

@ProxyClass(cc.LayerGradient)
class CCLayerGradient(CCLayer):
    pass


class CCLayerGradientCreator(CCLayerCreator):
    COM_NAME = 'CCLayerGradient'
    ATTR_DEFINE = CCLayerCreator.ATTR_DEFINE + [
     ('startColor', 16711680),
     ('endColor', 65280),
     ('startOpacity', 255),
     ('endOpacity', 255),
     (
      'vector', {'x': 1,'y': 0})]

    @staticmethod
    def create(parent, root, startColor, endColor, startOpacity, endOpacity, vector):
        startColor = ccc4(startColor >> 16 & 255, startColor >> 8 & 255, startColor & 255, startOpacity)
        endColor = ccc4(endColor >> 16 & 255, endColor >> 8 & 255, endColor & 255, endOpacity)
        obj = CCLayerGradient.Create(startColor, endColor, ccp(vector['x'], vector['y']))
        return obj