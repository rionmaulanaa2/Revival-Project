# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCParticleSystemQuad.py
from __future__ import absolute_import
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator

@ProxyClass(cc.ParticleSystemQuad)
class CCParticleSystemQuad(CCNode):
    pass


class CCParticleSystemQuadCreator(CCNodeCreator):
    COM_NAME = 'CCParticleSystemQuad'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('particleFile', 'gui/default/particle_texture.plist'),
     (
      'stop', False)]

    @staticmethod
    def create(parent, root, particleFile, stop):
        obj = CCParticleSystemQuad.Create(particleFile)
        global_data.uisystem.RecordSpriteUsage(particleFile, '', obj)
        if stop:
            obj.stopSystem()
        return obj