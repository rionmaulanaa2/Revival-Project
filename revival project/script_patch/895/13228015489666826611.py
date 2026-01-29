# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCClippingNode.py
from __future__ import absolute_import
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import ccp

@ProxyClass(cc.ClippingNode)
class CCClippingNode(CCNode):

    def SetStencil(self, stencileNode):
        if isinstance(stencileNode, CCNode):
            stencileNode = stencileNode.get()
        self.setStencil(stencileNode)
        self.setContentSize(stencileNode.getContentSize())
        stencileNode.setAnchorPoint(ccp(0, 0))

    def SetMaskFrameByPath(self, plist, path):
        frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
        global_data.uisystem.RecordSpriteUsage(plist, path, self)
        stencil = self.getStencil()
        stencil.setSpriteFrame(frame)

    def SetOptimize(self, flag):
        if hasattr(self._obj, 'setOptimize'):
            self._obj.setOptimize(flag)

    def csb_init(self):
        super(CCClippingNode, self).csb_init()
        from common.uisys import cocomate
        nd = self.getStencil()
        if nd.getFileName():
            wrap_node = cocomate.get_cocomate_node_by_cocos_node(nd)
            cocomate.bind_names(None, nd, None, None, None)
        return


def Create_Sprite(plist, path):
    if path is None:
        nd = cc.Sprite.create()
        return nd
    else:
        frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
        obj = cc.Sprite.createWithSpriteFrame(frame)
        global_data.uisystem.RecordSpriteUsage(plist, path, obj)
        return obj
        return


class CCClippingNodeCreator(CCNodeCreator):
    COM_NAME = 'CCClippingNode'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'displayFrame', {'plist': '','path': ''}),
     ('alphaThreshold', 0.9),
     (
      'inverted', False),
     ('ccbFile', 'default/ccbfile_default'),
     (
      'template_info', {})]

    @staticmethod
    def create(parent, root, displayFrame, alphaThreshold, inverted, ccbFile, template_info):
        obj = CCClippingNode.Create()
        if displayFrame['path']:
            spt = Create_Sprite(displayFrame['plist'], displayFrame['path'])
            if not spt:
                spt = Create_Sprite(None, None)
                log_error('Create_Sprite failed', displayFrame)
            obj.SetStencil(spt)
        else:
            tempFile = global_data.uisystem.load_template_create(ccbFile, None, None, template_info)
            obj.SetStencil(tempFile)
        obj.setAlphaThreshold(alphaThreshold)
        obj.setInverted(inverted)
        if hasattr(obj._obj, 'setOptimize'):
            obj._obj.setOptimize(False)
        return obj