# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCSkeletonNode.py
from __future__ import absolute_import
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from .CCSprite import CCSprite
from common.utils.ui_utils import get_scale
import six
if global_data.feature_mgr and global_data.feature_mgr.is_support_spine_3_8():
    from cocosui import sp

    @ProxyClass(sp.SkeletonAnimation)
    class CCSkeletonNode(CCNode):

        @classmethod
        def Create(cls, aniPath, atlas, scale):
            if six.PY3:
                obj = cls(cls.createWithJsonFile(aniPath, atlas, scale))
            else:
                obj = cls(cls.createWithFile(aniPath, atlas, scale))
            return obj


class CCSkeletonNodeCreator(CCNodeCreator):
    COM_NAME = 'CCSkeletonNode'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('aniPath', 'ccm_resources/default/cat01/cat01.json'),
     ('aniName', ''),
     (
      'loop', True),
     (
      'fallbackSprite', {'plist': '','path': 'gui/default/default_sprite.png'})]

    @staticmethod
    def create(parent, root, aniPath, aniName, loop, scale, fallbackSprite):
        if global_data.feature_mgr.is_support_spine_3_8():
            atlasPath = aniPath.replace('.json', '.atlas')
            if not (cc.FileUtils.getInstance().isFileExist(aniPath) and cc.FileUtils.getInstance().isFileExist(atlasPath)):
                log_error('File not exist!', aniPath, atlasPath)
                obj = CCNode.Create()
                return obj
            obj = CCSkeletonNode.Create(aniPath, atlasPath, get_scale(scale['x']))
            obj.setAnimation(0, aniName, loop)
        else:
            frame = global_data.uisystem.GetSpriteFrameByPath(fallbackSprite['path'], fallbackSprite['plist'])
            obj = CCSprite.CreateWithSpriteFrame(frame)
            global_data.uisystem.RecordSpriteUsage(fallbackSprite['plist'], fallbackSprite['path'], obj)
        return obj