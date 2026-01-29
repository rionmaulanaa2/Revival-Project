# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/MechaSpeedWindow.py
from __future__ import absolute_import
import cc
import cocosui

class MechaSpeedWindow(object):
    DEBUG_NODE_NAME = '__MechaSpeedWindow__'
    enable = False

    @classmethod
    def Clear(cls):
        if cls.logicNode:
            cls.logicNode.removeFromParent()
        cls.logicNode = None
        cls.nodeInfoLayer = None
        cls.nodeInfoLayerDrawNode = None
        cls.enable = False
        return

    @classmethod
    def Init(cls):
        if cls.enable:
            return
        cls.enable = True
        cls.logicNode = cc.Node.create()
        cls.logicNode.setName(cls.DEBUG_NODE_NAME)
        global_data.cocos_scene.addChild(cls.logicNode, 1000)
        cls.drawNode = cc.DrawNode.create()
        cls.logicNode.addChild(cls.drawNode, 1000)
        cls.nodeInfoLayer = cc.Node.create()
        cls.logicNode.addChild(cls.nodeInfoLayer)
        drawNode = cc.DrawNode.create()
        cls.nodeInfoLayer.addChild(drawNode)
        cls.nodeInfoLayerDrawNode = drawNode
        cls.textInfo = cocosui.ccui.Text.create('', '', 18)
        cls.textInfo.setAnchorPoint(cc.Vec2(0, 0))
        cls.textInfo.setPosition(cc.Vec2(300, 250))
        cls.nodeInfoLayer.addChild(cls.textInfo)
        cls.logicNode.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(cls._update_speed_text),
         cc.DelayTime.create(0.2)])))

    @classmethod
    def _update_speed_text(cls):
        from logic.entities.MechaTrans import MechaTrans
        from logic.gcommon.common_const import mecha_const as mconst
        text = cls.textInfo
        mecha = global_data.mecha
        if isinstance(mecha, MechaTrans):
            speed = global_data.mecha.logic.ev_g_vehicle_speed()
            pattern = global_data.mecha.logic.ev_g_pattern()
            if pattern == mconst.MECHA_PATTERN_VEHICLE:
                text.setString('\xe5\xbd\x93\xe5\x89\x8d\xe9\x80\x9f\xe5\xba\xa6:%.2f\n\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6:%s' % tuple(speed))
            else:
                text.setString('\xe9\x9d\x9e\xe9\xa9\xbe\xe9\xa9\xb6\xe5\xbd\xa2\xe6\x80\x81')
        else:
            text.setString('')